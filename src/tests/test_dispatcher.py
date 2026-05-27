from pathlib import Path
import sys

SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from core.dispatcher import yt_dispatcher
from core.yt_dlp_extractor import *
from core.segment_writer import write_segment_to_file
from tools.logger import LogMode, Log
from tools.run_id import generate_run_id

logger = Log(operation_name="Main", is_timestamp=False, log_level=LogMode.DEBUG)


def disp_data_out(sr: SegmentResult) -> None:
    if sr.success:
        logger.info(
            f"Segment {sr.start_index}-{sr.end_index} succeeded with {len(sr.tracks)} tracks."
        )
        write_segment_to_file(Path(f"temp/{generate_run_id()}.jsonl"), sr)
    else:
        logger.error(
            f"Segment {sr.start_index}-{sr.end_index} failed with error: {sr.error}"
        )


if __name__ == "__main__":
    # ? single video example:
    url: str = "https://music.youtube.com/watch?v=DZ0oir_DLao&si=ssSIQErl9xiUyj55"
    # ? playlist example:
    # url: str = (
    #     "https://www.youtube.com/playlist?list=PLKXe1HzhulvNHCI_v3aYjFNOdA947qru9"
    # )
    yt = yt_dispatcher(
        url=url,
        on_segment=disp_data_out,
    )
    print(yt)
