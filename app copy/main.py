from helper_functions import replicate_folder_structure, get_videos
from transcode import transcode, EncodeError
from rich_helpers import print_error, print_info
from rich.console import Console
from pathlib import Path

src_folder = input(": ")
dst_folder = input(": ")
replicate_folder_structure(src_folder, dst_folder, exclude_file_patterns=["*.mp4", "*.mkv"])

all_videos = get_videos(Path(src_folder))
remaining_videos = all_videos.copy()

console = Console()

for video in all_videos:
    print_info(console, video, all_videos, remaining_videos, dst_folder)

    try:
        transcode(video, dst_folder)
    except EncodeError:
        print_error(console, video)

    remaining_videos.remove(video)
