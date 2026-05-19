from datetime import datetime


def generate_run_id() -> str:
    now = datetime.now()
    return now.strftime("fetched_%H-%M_%d-%m-%Y")
