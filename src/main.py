import asyncio

from core import yt
from core.yt import TrackTuple


def yt_dispatcher(
    url: str,
    *,  # The * forces everything after it to be keyword-only arguments.
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
    except Exception as ex:
        print(f"[dispatcher] Failed to get playlist count: {ex}")
        return []

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


if __name__ == "__main__":
    url: str = "https://music.youtube.com/watch?v=DZ0oir_DLao&si=ssSIQErl9xiUyj55"
    yt = yt_dispatcher(url=url)
    print(yt)
