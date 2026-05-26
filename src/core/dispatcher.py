import asyncio
from collections.abc import Callable
from log_config import dispatcher_log_config
from core.yt_dlp_extractor import *

log = dispatcher_log_config


def yt_dispatcher(
    url: str,
    *,  # The * forces everything after it to be keyword-only arguments.
    segment_size: int = 5,
    max_concurrent: int = 10,
    on_segment: Callable[[SegmentResult], None] | None = None,
    parallel_threshold: int = 10,
) -> list[TrackInfoTuple]:
    try:
        count = get_playlist_count(  # pyright: ignore[reportAttributeAccessIssue]
            url
        )  # pyright: ignore[reportAttributeAccessIssue]
        log.info(f"Playlist has {count} track(s).")
    except Exception as ex:
        log.error(f"Failed to get playlist count: {ex}")
        return []

    if count >= parallel_threshold:
        tracks, failed = asyncio.run(
            extract_info_parallel(  # pyright: ignore[reportAttributeAccessIssue]
                url=url,
                on_segment=on_segment,
                # on_segment=lambda segment: print(
                #     f"[dispatcher] Processing segment {segment.start_index}-{segment.end_index}"
                # ),
                segment_size=segment_size,
                max_concurrent=max_concurrent,
            )
        )
        if failed:
            log.error(
                f"{len(failed)} segment(s) failed "
                f"(indices: {', '.join(f'{s.start_index}-{s.end_index}' for s in failed)})"
            )
        log.info(f"Extracted {len(tracks)} tracks in parallel.")
    else:
        tracks = extract_info(url)  # pyright: ignore[reportAttributeAccessIssue]
        if on_segment is not None:
            on_segment(
                SegmentResult(
                    start_index=1,
                    end_index=len(tracks),
                    success=True,
                    tracks=tracks,
                )
            )
        log.info(f"Extracted {len(tracks)} track(s).")

    return tracks
