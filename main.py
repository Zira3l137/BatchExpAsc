from argparse import ArgumentParser, Namespace
from concurrent.futures import ProcessPoolExecutor, as_completed
from configparser import ConfigParser
from os import cpu_count
from pathlib import Path
from subprocess import run
from time import time


def parse_commandline_arguments() -> Namespace:
    parser = ArgumentParser()
    parser.add_argument(
        "--config_path",
        "-c",
        help="Path to the INI config file",
        type=str,
        default=Path(__file__).parent / "config.ini",
    )
    parser.add_argument(
        "--max_processes",
        "-m",
        help="Maximum number of processes to spawn",
        type=int,
        default=0,
    )
    return parser.parse_args()


def get_path(path: str) -> str:
    if '"' in path:
        return path.replace('"', "")
    return path


def spawn_instance(args: tuple) -> int:
    blender_path, script_path, body_path, anim_path, export_dir, export_type = args
    return run(
        [
            blender_path,
            "--background",
            "--python",
            script_path,
            body_path,
            anim_path,
            export_dir,
            export_type,
        ],
    ).returncode


def batch_process_anims(
    blender_path: str,
    script_path: str,
    body_path: str,
    anims_dir: str,
    export_dir: str,
    export_type: str,
    max_workers: int,
):
    anims_query = [
        (blender_path, str(script_path), body_path, str(anim), export_dir, export_type)
        for anim in Path(anims_dir).iterdir()
        if anim.suffix.lower() == ".asc"
    ]

    executor = ProcessPoolExecutor(max_workers=max_workers)
    start = time()
    try:
        results = executor.map(spawn_instance, anims_query, chunksize=1, timeout=20)
        executor.shutdown(wait=True)
    except (OSError, KeyboardInterrupt, AttributeError):
        executor.shutdown(wait=False, cancel_futures=True)
        raise
    end = time()
    print(f"\n\nTotal time: {end - start:.2f}")
    return list(results)

    # with ProcessPoolExecutor(max_workers=max_workers) as executor:
    #     futures = [executor.submit(spawn_instance, args) for args in anims_query]
    #     start = time()
    #     for future in as_completed(futures):
    #         if exception := future.exception():
    #             print(exception)
    #     end = time()
    #     print(f"\n\nTotal time: {end - start:.2f}")


def main():
    arguments = parse_commandline_arguments()
    config = ConfigParser()
    config.read(arguments.config_path)
    max_processes = arguments.max_processes
    if max_processes == 0:
        max_processes = max(1, (cpu_count() or 1) * 2)

    SCRIPT_PATH = str(Path(__file__).parent / "BatchExpAsc.py")
    BLENDER_PATH = get_path(config["Paths"]["blender_exe_path"])
    BODY_PATH = get_path(config["Paths"]["body_asc_path"])
    ANIMS_DIR = get_path(config["Paths"]["anims_dir"])
    EXPORT_DIR = get_path(config["Paths"]["output_dir"])
    EXPORT_TYPE = get_path(config["Paths"]["export_format"])

    batch_process_anims(
        script_path=SCRIPT_PATH,
        blender_path=BLENDER_PATH,
        body_path=BODY_PATH,
        anims_dir=ANIMS_DIR,
        export_dir=EXPORT_DIR,
        export_type=EXPORT_TYPE,
        max_workers=max_processes,
    )


if __name__ == "__main__":
    main()
