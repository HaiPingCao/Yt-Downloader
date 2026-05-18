from core.yt_parallel import *


def yt_dispatcher(url: str) -> None:
    segment_size = 5
    concurrent_threshold = 10

    if get_playlist_count(url) >= segment_size:
        tracks, segments = asyncio.run(
            extract_info_parallel(
                url=url,
                segment_size=segment_size,
                max_concurrent=concurrent_threshold,
                output_dir=None,
            )
        )
        print(f"Extracted {len(tracks)} tracks in {len(segments)} segments.")
