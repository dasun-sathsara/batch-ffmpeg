from pathlib import Path
from subprocess import run, CalledProcessError, PIPE
from tempfile import TemporaryFile
from rich.console import Console
from helper_functions import *


class EncodeError(Exception):
    """Raised when an error occured while encoding."""

    def __str__(self):
        return f"Encoding error."


def transcode(video: Path, dst: str):

    input_str = str(video)
    output_str = str(Path(file_name_output(video, dst), f"{video.stem}.mp4"))

    stderr_file = TemporaryFile()
    try:
        cp = run(
            [
                "ffmpeg",
                "-i",
                input_str,
                "-b:a",
                "128K",
                "-acodec",
                "libopus",
                "-crf",
                "23",
                "-filter:v",
                "scale=1280:-2",
                "-map_metadata",
                "0",
                "-max_muxing_queue_size",
                "1024",
                "-movflags",
                "use_metadata_tags",
                "-pix_fmt",
                "yuv420p10le",
                "-preset",
                "medium",
                "-vcodec",
                "libx265",
                "-x265-params",
                "aq-mode=2:repeat-headers=0:strong-intra-smoothing=1:bframes=4:b-adapt=2:frame-threads=0:colorprim=bt709:transfer=bt709:colormatrix=bt709:hdr10_opt=0:hdr10=0:chromaloc=0",
                "-movflags",
                "faststart",
                "-report",
                "-y",
                output_str,
            ],
            stderr=stderr_file,
            check=True,
            encoding="utf-8",
        )

    except CalledProcessError:
        stderr_file.seek(0)
        str_stderr = stderr_file.read().decode("utf-8")

        log_error_file_name("error_files.txt", video)
        log_stderr(f"stderr_log.txt", video, str_stderr)
        raise EncodeError
    finally:
        stderr_file.close()


if __name__ == "__main__":
    from rich.console import Console

    console = Console()
    transcode(Path("src/daemon.mp4"), "Conv")
