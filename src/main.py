from dispatcher import yt_dispatcher
from core.yt import *
from tools.logging_formatter import LogMode, Log

logger = Log(operation_name="Main", is_timestamp=False, log_level=LogMode.DEBUG)


def process(sr: SegmentResult) -> None:
    if sr.success:
        logger.info(
            f"Segment {sr.start_index}-{sr.end_index} succeeded with {len(sr.tracks)} tracks."
        )
    else:
        logger.error(
            f"Segment {sr.start_index}-{sr.end_index} failed with error: {sr.error}"
        )


if __name__ == "__main__":
    # ? single video example:
    # url: str = "https://music.youtube.com/watch?v=DZ0oir_DLao&si=ssSIQErl9xiUyj55"
    # ? playlist example:
    url: str = (
        "https://www.youtube.com/watch?v=EUffJAcHT7k"
    )
    yt = yt_dispatcher(
        url=url,
        on_segment=process,
    )
    # print(yt)
