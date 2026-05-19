import asyncio
from collections.abc import Callable
from core import yt
from core.yt import TrackInfoTuple, SegmentResult


def yt_dispatcher(
    url: str,
    *,  # The * forces everything after it to be keyword-only arguments.
    segment_size: int = 5,
    max_concurrent: int = 10,
    on_segment: Callable[[SegmentResult], None] | None = None,
    parallel_threshold: int = 10,
) -> list[TrackInfoTuple]:
    try:
        count = yt.get_playlist_count(  # pyright: ignore[reportAttributeAccessIssue]
            url
        )  # pyright: ignore[reportAttributeAccessIssue]
    except Exception as ex:
        print(f"[dispatcher] Failed to get playlist count: {ex}")
        return []

    if count >= parallel_threshold:
        tracks, failed = asyncio.run(
            yt.extract_info_parallel(  # pyright: ignore[reportAttributeAccessIssue]
                url=url,
                on_segment=lambda segment: print(
                    f"[dispatcher] Processing segment {segment.start_index}-{segment.end_index}"
                ),
                segment_size=segment_size,
                max_concurrent=max_concurrent,
            )
        )
        if failed:
            print(
                f"[dispatcher] {len(failed)} segment(s) failed "
                f"(indices: {', '.join(f'{s.start_index}-{s.end_index}' for s in failed)})"
            )
        print(f"[dispatcher] Extracted {len(tracks)} tracks in parallel.")
    else:
        tracks = yt.extract_info(url)  # pyright: ignore[reportAttributeAccessIssue]
        print(f"[dispatcher] Extracted {len(tracks)} track(s).")

    return tracks


def process(sr: SegmentResult) -> None:
    if sr.success:
        print(
            f"Segment {sr.start_index}-{sr.end_index} succeeded with {len(sr.tracks)} tracks."
        )
    else:
        print(f"Segment {sr.start_index}-{sr.end_index} failed with error: {sr.error}")


if __name__ == "__main__":
    # ? single video example:
    # url: str = "https://music.youtube.com/watch?v=DZ0oir_DLao&si=ssSIQErl9xiUyj55"
    # ? playlist example:
    url: str = (
        "https://www.youtube.com/playlist?list=PLKXe1HzhulvPXy5o3DgA1Lbl2SCyz55Ez"
    )
    yt = yt_dispatcher(
        url=url,
        on_segment=process,
    )
    # print(yt)
