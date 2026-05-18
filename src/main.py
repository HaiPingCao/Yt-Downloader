import asyncio
import subprocess

from core import yt
from core.yt import TrackTuple


def yt_dispatcher(
    url: str,
    *,
    segment_size: int = 5,
    max_concurrent: int = 10,
    parallel_threshold: int = 10,
    output_dir: str | None = None,
) -> list[TrackTuple]:
    """Fetch track info from *url*, choosing the parallel path automatically.

    When the playlist contains more entries than *parallel_threshold* the work
    is split into segments of *segment_size* and up to *max_concurrent*
    segments are fetched at the same time.  Smaller playlists (or single
    videos) fall back to the simpler `extract_info` call.

    Returns the flat list of extracted tracks.
    """
    try:
        count = yt.get_playlist_count(url)
    except (ValueError, subprocess.CalledProcessError):
        # Not a playlist (single video) or yt-dlp couldn't resolve a count.
        count = 1

    if count >= parallel_threshold:
        tracks, failed = asyncio.run(
            yt.extract_info_parallel(
                url=url,
                segment_size=segment_size,
                max_concurrent=max_concurrent,
                output_dir=output_dir,
            )
        )
        if failed:
            print(
                f"[dispatcher] {len(failed)} segment(s) failed "
                f"(indices: {', '.join(f'{s.start_index}-{s.end_index}' for s in failed)})"
            )
        print(f"[dispatcher] Extracted {len(tracks)} tracks in parallel.")
    else:
        tracks = asyncio.run(yt.extract_info(url))
        print(f"[dispatcher] Extracted {len(tracks)} track(s).")

    return tracks
