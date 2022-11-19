import fnmatch
from pathlib import Path
from shutil import copytree


def get_videos(path: Path = Path(".")) -> list[Path]:
    file_names = list(path.glob("**/*.*"))

    def check_video(path: Path):
        if path.suffix in [".mp4", ".avi", ".mkv"]:
            return True
        return False

    return list(filter(check_video, file_names))


def replicate_folder_structure(src: str, dst: str, copy_files: bool = True, exclude_file_patterns: list = []) -> None:
    """Replicate source folder structure.

    Args:
        src (str): Source folder
        dst (str): Destination Folder
        copy_files (bool, optional): If true, copies all the files from source to destination, essentially replicating the src. Defaults to True.
        exclude_file_patterns (list, optional): Ignores files that corresponds to patterns when copying. Defaults to [].
    """

    if not copy_files:
        patterns = ["*.*"]
    else:
        patterns = exclude_file_patterns

    def _logpath(path, names):
        print(f"Working in:{path}")
        ignored_names = []
        for pattern in patterns:
            ignored_names.extend(fnmatch.filter(names, pattern))
        return set(ignored_names)

    copytree(src, dst, ignore=_logpath, dirs_exist_ok=True)


def get_total_size(paths: list[Path]) -> float:
    """Return the total tize of files in MB"""
    total_bytes = 0
    for path in paths:
        total_bytes += path.stat().st_size

    return round(total_bytes / 2**20, 2)


def log_stderr(fp: str, file_name: str | Path, error: str):
    """Append the error message (with the file name) to errors log file."""

    if isinstance(file_name, Path):
        file_name = str(file_name)

    with open(fp, "a", encoding="utf-8") as e_file:
        e_file.write(f"-------------------{file_name}-------------------")
        e_file.write("\n\n")
        e_file.write(error)
        e_file.write("----------------------------------------------------\n\n")


def log_error_file_name(fp: str, file_name: str | Path):

    if isinstance(file_name, Path):
        file_name = str(file_name)

    with open(fp, "a", encoding="utf-8") as e_file:
        e_file.write(f"{file_name}\n")


def file_name_output(path: Path, dst: str) -> Path:
    path = Path(dst, *path.parts[1:-1])
    # path.mkdir(parents=True, exist_ok=True)
    return path
