from rich.console import Console, Group
from rich.columns import Columns
from rich.text import Text
from rich.panel import Panel
from pathlib import Path
from helper_functions import get_total_size, get_videos


def print_info(
    console: Console, video: Path, all_videos_list: list[Path], remaining_videos_list: list[Path], dst: str
) -> None:

    seperator = Text.assemble(("|", "cyan"))

    file_name = Text.assemble(("Name: ", "yellow"), str(video))
    file_size = Text.assemble(("Size: ", "yellow"), f"{round(video.stat().st_size / 2**20,2)}MB")
    total_videos = Text.assemble(("Total Videos: ", "yellow"), str(len(all_videos_list)))
    total_size = Text.assemble(("Total Size: ", "yellow"), f"{get_total_size(all_videos_list)}MB")
    remaining_videos = Text.assemble(("Remaining Videos: ", "yellow"), str(len(remaining_videos_list)))
    remaining_size = Text.assemble(("Remaining Size: ", "yellow"), f"{get_total_size(remaining_videos_list)}MB")
    processed_size = Text.assemble(
        ("Transcoded Size: ", "yellow"), f"{get_total_size(get_videos(Path('Converted')))}MB"
    )

    columns = Panel(
        Group(
            file_name,
            Columns(
                [
                    file_size,
                    seperator,
                    total_videos,
                    seperator,
                    remaining_videos,
                    seperator,
                    total_size,
                    seperator,
                    remaining_size,
                    seperator,
                    processed_size,
                ],
                padding=(2, 2),
                title=" ",
            ),
        )
    )
    console.print(columns)


def print_error(console: Console, video: Path) -> None:
    console.print(Panel(Text.assemble((f"Error: {video}"))), style="red bold")


if __name__ == "__main__":
    console = Console()
    print_info(
        console,
        Path("daemon.mp4"),
        [Path("daemon.mp4"), Path("daemon_encoded.mp4")],
        [Path("daemon_encoded.mp4")],
        "Converted",
    )
