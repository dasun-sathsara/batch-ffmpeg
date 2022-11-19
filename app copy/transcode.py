from pathlib import Path
from rich.console import Console
from helper_functions import *
import ffmpeg


class EncodeError(Exception):
    """Raised when an error occured while encoding."""

    def __str__(self):
        return f"Encoding error."


def transcode(video: Path, dst: str):

    input_str = str(video)
    output_str = str(Path(file_name_output(video, dst), f"{video.stem}.mp4"))

    try:
        (
            ffmpeg.input(input_str)
            .output(
                output_str,
                movflags="use_metadata_tags",
                max_muxing_queue_size=1024,
                vcodec="libx265",
                pix_fmt="yuv420p10le",
                map_metadata=0,
                acodec="libopus",
                audio_bitrate="128K",
                preset="fast",
                crf="23",
                **{
                    "x265-params": "aq-mode=2:repeat-headers=0:strong-intra-smoothing=1:bframes=4:b-adapt=2:frame-threads=0:colorprim=bt709:transfer=bt709:colormatrix=bt709:hdr10_opt=0:hdr10=0:chromaloc=0"
                },
                **{"filter:v": "scale=1280:-2"},
            )
            .global_args("-movflags", "faststart")
            # .global_args("-report")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

    except ffmpeg.Error as e:
        error_str = e.stderr.decode().replace("\r\n", "\n")
        print(error_str)
        log_error_file_name("error_files.txt", video)
        log_stderr(f"stderr_log.txt", video, error_str)
        raise EncodeError


if __name__ == "__main__":
    from rich.console import Console

    console = Console()
    transcode(Path("src/daemon.mp4"), "Conv")
