import os
from typing import Literal

# Valid yt-dlp top-level keys only
_BASE: dict = {
    "quiet": True,
    "no_warnings": True,
    "ignoreerrors": True,
    "verbose": False,
    "format": "bestaudio/best",
    "noplaylist": False,
    "skip_unavailable_fragments": True,
}


def build_options(
    mode: Literal["info", "download", "playlist_discover"],
    playlist: bool = True,
    debug: bool = False,
    download_folder: str = r"\Temp",
    playlist_items: str | None = None,  # e.g. "1-20", "3", "1,5,7" — None = full
) -> dict:
    """
    mode:
        'playlist_discover' — discover playlist items without downloading
        'info'     — extract video metadata only, no download
        'download' — download and convert to mp3

    playlist_items:
        yt-dlp playlist_items string. None = no restriction (full playlist).
        Examples: "1-20", "3", "1,3,5-10"
    """

    opts = _BASE.copy()

    if not playlist:
        opts["noplaylist"] = True

    if debug:
        opts.update(
            {
                "quiet": False,
                "no_warnings": False,
                "verbose": True,
            }
        )

    if mode == "playlist_discover":
        opts["extract_flat"] = True
        opts["playlist_items"] = "1"  # Only need the first item to get the count

    if mode == "info":
        # extract_flat: True = fast metadata only (no format resolution)
        # set False if you need the resolved direct audio stream URL
        opts["extract_flat"] = False

    elif mode == "download":
        opts["outtmpl"] = os.path.join(download_folder, "%(title)s.%(ext)s")
        opts["keepvideo"] = False
        opts["postprocessors"] = [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ]

    if playlist_items is not None:
        opts["playlist_items"] = playlist_items

    return opts
