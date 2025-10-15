import asyncio
from typing import List, Literal, Optional, Union
from PIL import Image

from utils.video import download_video


class VideoOutput:
    fmt: Literal["url"]
    ext: str = "mp4"
    data: Union[str, Image.Image]

    def __init__(
        self,
        fmt: Literal["url"],
        ext: str,
        data: str,
    ):
        self.fmt = fmt
        self.ext = ext
        self.data = data

    def save_url(self, path: str) -> None:
        """Download and save a video from a URL to the specified path.

        Args:
            path (str): Path where the video will be saved.
        """
        download_video(self.data, path)

    def save(self, path: str) -> None:
        save_func = getattr(self, f"save_{self.fmt}")
        save_func(path)

