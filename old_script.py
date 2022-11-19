from pathlib import Path

import ffmpeg
from rich import print


def get_videos() -> list[Path]:
    file_names = list(Path(".").glob("**/*.*"))

    def check_video(path: Path):
        if path.suffix in [".mp4", ".avi", ".mkv"]:
            return True
        return False

    return list(filter(check_video, file_names))


def file_name_output(path: Path) -> Path:
    return Path("Converted", *path.parts[1:-1])


def transcode(input: Path) -> None:
    file_name_output(input).mkdir(parents=True, exist_ok=True)
    Path("errors/").mkdir(parents=True, exist_ok=True)

    input_str = str(input)
    output_str = str(Path(file_name_output(input), f"{input.stem}.mp4"))

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
                preset="medium",
                crf="23",
                **{
                    "x265-params": "aq-mode=2:repeat-headers=0:strong-intra-smoothing=1:bframes=4:b-adapt=2:frame-threads=0:colorprim=bt709:transfer=bt709:colormatrix=bt709:hdr10_opt=0:hdr10=0:chromaloc=0"
                },
                **{"filter:v": "scale=1280:-2"},
            )
            .global_args("-movflags", "faststart")
            .global_args("-report")
            .overwrite_output()
            .run(capture_stdout=True, capture_stderr=True)
        )

    except ffmpeg.Error as e:
        print(f"[red]ERROR: {input}")

        with open(f"errors/{input.stem}_{input.suffix}.txt", "w") as error_file:
            error_file.write(e.stderr.decode().replace("\r\n", "\n"))

        with open("errors.txt", "a", encoding="utf-8") as e_file:
            e_file.write(f"{input}\n")


if __name__ == "__main__":
    video_list = get_videos()
    for video in video_list:
        print(f"\n[green]PROCESSING: {video}")
        transcode(video)

# -max_muxing_queue_size 1024 -vcodec libx265 -pix_fmt yuv420p10le
# -x265-params "aq-mode=2:repeat-headers=0:strong-intra-smoothing=1:bframes=4:b-adapt=2:frame-threads=0:colorprim=bt709:transfer=bt709:colormatrix=bt709:hdr10_opt=0:hdr10=0:chromaloc=0"
# -crf:v 23 -preset:v medium -map_metadata 0 -movflags use_metadata_tags -movflags faststart
# -acodec libopus -b:1 128k
