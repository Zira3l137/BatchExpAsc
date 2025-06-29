from enum import IntEnum
from pathlib import Path
from sys import argv

import bpy
from krximpexp.BatAscImp import (DEFAULT_SAMPLE_MESH_DIR, ASCParser, AscType,
                                 BatAscImp)
from krximpexp.KrxAscExp import KrxAscExp
from krximpexp.scene import SceneMode

DEFAULT_EXPORT_DIR = Path().home().resolve() / "BatchAscExp"
EXPORT_FORMAT = {0: "fbx", 1: "asc"}


def get_armature():
    for obj in bpy.data.objects:
        if obj.type == "ARMATURE":
            return obj


class ExportType(IntEnum):
    FBX = 0
    ASC = 1


class NotAnAnimation(Exception):
    def __init__(self, message="") -> None:
        super().__init__(message)


class BatchExpAsc:
    def __init__(
        self,
        body_path: str,
        anim_path: str,
        # Following parameters are optional
        export_dir: str | None = None,
        export_type: int = ExportType.ASC,
        import_body: bool = True,
        file_name: str | None = None,
        export_from_frame: int | None = None,
        export_to_frame: int | None = None,
        for_ue: bool = False,
    ):
        self.body_path = Path(body_path)
        self.anim_path = Path(anim_path)
        self.export_dir = (
            Path(export_dir) if export_dir else DEFAULT_EXPORT_DIR / self.anim_path.stem
        )
        self.export_type = export_type
        self.import_body: bool = import_body
        self.file_name: str | None = file_name
        self.start: int | None = export_from_frame
        self.end: int | None = export_to_frame
        self.for_ue: bool = for_ue

        if self.import_body:
            self._import_body()
        if not self.anim_path.is_dir():
            self._export_anim(self.anim_path)
        else:
            self.anim_count = 0
            for anim in self.anim_path.iterdir():
                if anim.is_file() and anim.suffix.lower() == ".asc":
                    self.anim_count += 1
                    self._export_anim(anim)

    def _import_body(self):
        BatAscImp(
            str(self.body_path),
            scene_mode=SceneMode.REPLACE,
            model_prefix="",
            sample_meshes_directory=DEFAULT_SAMPLE_MESH_DIR,
        )

    def _import_anim(self, anim_path: str):
        self.asc_parser = ASCParser(filename=anim_path)
        if self.asc_parser.model_type != AscType.DYNAMIC_ANIM:
            raise NotAnAnimation

        start_frame = self.asc_parser.time_transform.min_frame_in_file
        end_frame = self.asc_parser.time_transform.max_frame_in_file
        BatAscImp(
            anim_path,
            parser_handle=self.asc_parser,
            scene_mode=SceneMode.REPLACE_ANIM,
            model_prefix="",
            start_frame_in_file=start_frame,
            end_frame_in_file=end_frame,
            start_frame_in_scene=start_frame,
            end_frame_in_scene=end_frame,
        )

    def _set_frame_range(self):
        context = bpy.context
        if not context:
            raise RuntimeError("No context")
        obj = context.active_object
        if not obj:
            raise RuntimeError("No object selected")
        obj_anim_data = obj.animation_data
        obj_action = obj_anim_data.action
        if obj_anim_data and obj_action:
            first_frame = self.start if self.start else 0
            last_frame = (
                self.end
                if self.end
                else self.asc_parser.time_transform.end_frame_in_file
            )
            context.scene.frame_start = first_frame
            context.scene.frame_end = last_frame

    def _get_final_path(self, anim_path: Path) -> str:
        file_stem = anim_path.stem if not self.file_name else self.file_name
        suffix = EXPORT_FORMAT[self.export_type]
        self.export_dir.mkdir(parents=True, exist_ok=True)
        return str((self.export_dir / f"{file_stem}.{suffix}").resolve())

    def _export_anim(self, anim_path: Path):
        try:
            self._import_anim(str(anim_path))
        except NotAnAnimation:
            print(f"{str(anim_path)} is not an animation, skipping...")
            return
        self._set_frame_range()
        export_file_name = self._get_final_path(anim_path)
        if self.export_type == ExportType.FBX:
            self._export_to_fbx(export_file_name)
            return
        self._export_to_asc(export_file_name)

    def _export_to_fbx(self, export_file_name: str):
        bpy.ops.object.select_all(action="SELECT")
        if self.for_ue:
            bpy.ops.export_scene.fbx(
                filepath=export_file_name,
                bake_anim=True,
                mesh_smooth_type="EDGE",
                axis_forward="X",
                axis_up="Z",
                object_types={"ARMATURE", "MESH"},
                use_selection=True,
                add_leaf_bones=False,
            )
        else:
            bpy.ops.export_scene.fbx(
                filepath=export_file_name,
                bake_anim=True,
                object_types={"ARMATURE", "MESH"},
                use_selection=True,
            )

    def _export_to_asc(self, export_file_name: str):
        armature = get_armature()
        if not armature:
            raise RuntimeError("No armature found")
        bones = armature.data.bones
        selected_nodes = [bone.name for bone in bones]
        for obj in bpy.data.objects:
            if obj.parent_bone in selected_nodes:
                selected_nodes.append(obj.name)
        KrxAscExp(
            export_file_name,
            export_anim=True,
            selected_objects_param=selected_nodes,
            start_frame_in_file=self.asc_parser.time_transform.start_frame_in_file,
            end_frame_in_file=self.asc_parser.time_transform.end_frame_in_file,
            start_frame_in_scene=self.asc_parser.time_transform.start_frame_in_scene,
            end_frame_in_scene=self.asc_parser.time_transform.end_frame_in_scene,
        )


def parse_commandline_arguments() -> dict[str, str]:
    try:
        separator_index = argv.index("--")
        user_args = argv[separator_index + 1 :]
    except ValueError:
        raise RuntimeError("Expected '--' to separate Blender and script arguments.")

    if len(user_args) < 4:
        raise ValueError("Not enough arguments passed to script.")

    return {
        "anim_path": user_args[0],
        "export_dir": user_args[1],
        "export_type": user_args[2],
        "body_path": user_args[3] if len(user_args) > 3 else None,
    }


if __name__ == "__main__":
    arguments = parse_commandline_arguments()
    BatchExpAsc(
        body_path=arguments["body_path"],
        anim_path=arguments["anim_path"],
        export_dir=arguments["export_dir"],
        export_type=int(arguments["export_type"]),
        import_body=bool(arguments["body_path"]),
    )
