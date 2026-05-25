import asyncio
import yt_dlp
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from collections.abc import Callable
from core.yt_dlp_options import build_options
from yt_dlp.utils import DownloadError
from config import yt_log_config

log = yt_log_config


def extract_info(
    url,
    option=build_options(mode="info", playlist=False, debug=False),
    # write_json:bool=False
):
    """
    return: video_title, webpage_url, duration, sound_url, info_dict
    """
    try:
        with yt_dlp.YoutubeDL(option) as info:
            info_dict = info.extract_info(url, download=False)
            return_list = []

            entries = info_dict.get("entries", [info_dict])
            for entry in entries:
                if not entry:
                    continue
                # print(entry)
                video_title = entry.get("title", None)
                webpage_url = entry.get("webpage_url", None)
                duration = entry.get("duration", None)
                sound = None
                if entry and "formats" in entry and entry["formats"]:
                    sound = next(
                        (
                            f["url"]
                            for f in entry["formats"]
                            if f
                            and "ext" in f
                            and "url" in f
                            and f["ext"] in ["m4a", "webm"]
                            and f.get("vcodec") == "none"
                        ),
                        None,
                    )
                return_list.append((video_title, webpage_url, duration, sound))

            return return_list

    except DownloadError as e:
        log.error(f"Error extracting info: {e}")
        return []


def get_playlist_count(url: str) -> int:
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
        "extract_flat": "in_playlist",  # equivalent to --flat-playlist
        "playlist_items": "1",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:  # pyright: ignore[reportArgumentType]
        info = ydl.extract_info(url, download=False)
        list_count = info.get("playlist_count")
        if list_count is None:
            return 1  # Not a playlist or count not available; treat as single video.
    return list_count  # pyright: ignore[reportGeneralTypeIssues]


# Split playlist extraction into index ranges, fetch those ranges concurrently,
# and optionally stream successful results to a JSONL file in playlist order.
type TrackInfoTuple = tuple[str | None, str | None, float | None, str | None]


@dataclass
class SegmentResult:
    start_index: int
    end_index: int
    success: bool
    tracks: list[TrackInfoTuple] = field(default_factory=list)
    error: str | None = None


def _extract_segment_blocking(
    url: str, start_index: int, end_index: int
) -> list[TrackInfoTuple]:
    # yt-dlp work is isolated in this synchronous helper so the async caller can
    # run several playlist ranges through a thread pool without blocking the
    # event loop.
    opts = build_options(
        mode="info",
        playlist=True,
        playlist_items=(
            f"{start_index}"
            if start_index == end_index
            else f"{start_index}-{end_index}"
        ),
    )
    return extract_info(url, option=opts)


# fetch a playlist segment in a thread pool and return the results asynchronously.
async def _fetch_segment(
    url: str,
    start_index: int,
    end_index: int,
    semaphore: asyncio.Semaphore,
    executor: ThreadPoolExecutor,
) -> SegmentResult:
    # The semaphore limits active extractor jobs even though all segment tasks
    # are scheduled up front.
    async with semaphore:
        loop = asyncio.get_running_loop()
        try:
            tracks = await loop.run_in_executor(
                executor,
                _extract_segment_blocking,
                url,
                start_index,
                end_index,
            )
            return SegmentResult(
                start_index=start_index,
                end_index=end_index,
                success=True,
                tracks=tracks,
            )
        except Exception as ex:
            return SegmentResult(
                start_index=start_index,
                end_index=end_index,
                success=False,
                error=str(ex),
            )


async def extract_info_parallel(
    url: str,
    *,
    on_segment: Callable[[SegmentResult], None] | None = None,
    start_index: int = 1,
    end_index: int | None = None,
    segment_size: int = 5,
    max_concurrent: int = 4,
) -> tuple[list[TrackInfoTuple], list[SegmentResult]]:

    # Resolve the playlist length only when the caller wants the full tail.
    if end_index is None:
        end_index = get_playlist_count(url)

    segments: list[tuple[int, int]] = []
    # force index to start from 1 or higher
    start = max(start_index, 1)
    while start <= end_index:
        # Build inclusive playlist index ranges: 1-5, 6-10, etc.
        end = min(start + segment_size - 1, end_index)
        segments.append((start, end))
        start = end + 1
    # The semaphore limits how many segments can be extracting at the same time
    semaphore = asyncio.Semaphore(max_concurrent)
    all_results: list[SegmentResult] = []
    failed: list[SegmentResult] = []

    # Hold completed segments until all earlier ranges have finished so the
    # output file stays in playlist order even when later tasks complete first.
    buffer: dict[int, SegmentResult] = {}
    next_expected: int = segments[0][0]  # first segment's start_index

    with ThreadPoolExecutor(max_workers=max_concurrent) as executor:
        # Schedule every segment immediately; max_concurrent controls how many
        # are allowed to extract at the same time.
        tasks = [
            asyncio.ensure_future(_fetch_segment(url, s, e, semaphore, executor))
            for s, e in segments
        ]

        for coro in asyncio.as_completed(tasks):
            result: SegmentResult = await coro
            all_results.append(result)

            # Successful segments may arrive out of order, so buffer them before
            # flushing. Failed segments are reported and returned for retry or
            # inspection by the caller.
            if result.success:
                buffer[result.start_index] = result
                while next_expected in buffer:
                    segm = buffer.pop(next_expected)
                    #! START: Operation to do with completed segment (e.g. write to file, print info, etc.)
                    on_segment(segm) if on_segment is not None else None
                    #! END: Operation to do with completed segment
                    if on_segment is not None:
                        on_segment(segm)
                    next_expected = segm.end_index + 1
            else:
                failed.append(result)
                log.error(
                    f"Segment [{result.start_index}-{result.end_index}] failed: {result.error}"
                )

    all_results.sort(key=lambda r: r.start_index)
    tracks: list[TrackInfoTuple] = []
    for r in all_results:
        if r.success:
            tracks.extend(r.tracks)
    return tracks, failed
