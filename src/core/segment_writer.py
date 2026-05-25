import json
from pathlib import Path
from core.yt_dlp_extractor import SegmentResult


def write_segment_to_file(file: Path, segment: SegmentResult) -> None:
    """Append all tracks from a completed segment to the JSONL file."""
    with file.open("a", encoding="utf-8") as f:
        for title, webpage_url, duration, sound_url in segment.tracks:
            record = {
                "title": title,
                "webpage_url": webpage_url,
                "duration": duration,
                "sound_url": sound_url,
            }
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
