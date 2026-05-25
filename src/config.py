from tools.logger import Log, LogMode

yt_log_config = Log(
    operation_name="Extractor", is_timestamp=False, log_level=LogMode.DEBUG
)

dispatcher_log_config = Log(
    operation_name="Dispatcher", is_timestamp=False, log_level=LogMode.DEBUG
)
