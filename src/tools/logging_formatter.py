from enum import Enum
from datetime import datetime
import sys


class AnsiColor(Enum):
    """ANSI color codes for terminal output"""

    GREEN = "\033[92m"
    GW = "\x1b[0;38;5;151;49m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    WHITE = "\033[97m"
    RESET = "\033[0m"
    ORANGE = "\033[38;5;208m"


class LogMode(Enum):
    """Log severity modes with priority levels"""

    priority: int

    TRACE = (0, "TRACE")
    DEBUG = (1, "DEBUG")
    INFO = (2, "INFO")
    LOG = (3, "LOG")
    WARNING = (4, "WARNING")
    ERROR = (5, "ERROR")
    CRITICAL = (6, "CRITICAL")

    def __new__(cls, priority, label):
        obj = object.__new__(cls)
        obj.priority = priority
        obj._value_ = label
        return obj

    def __str__(self):
        return self.value


class Log:
    # Mapping log modes to their colors
    MODE_COLORS = {
        LogMode.TRACE: AnsiColor.WHITE,
        LogMode.DEBUG: AnsiColor.CYAN,
        LogMode.INFO: AnsiColor.WHITE,
        LogMode.LOG: AnsiColor.WHITE,
        LogMode.WARNING: AnsiColor.YELLOW,
        LogMode.ERROR: AnsiColor.RED,
        LogMode.CRITICAL: AnsiColor.MAGENTA,
    }

    def __init__(
        self,
        operation_name: str,
        log_level: LogMode = LogMode.TRACE,
        is_timestamp: bool = False,
    ):
        """
        Initialize the Log class

        Args:
            operation_name: Name of the operation for logging context
            log_level: Minimum log level to display (default: TRACE shows everything)
            is_timestamp: Whether to include timestamps in log messages

            TRACE (0)    → Shows everything
            DEBUG (1)    → Shows DEBUG and above
            INFO (2)     → Shows INFO and above
            LOG (3)      → Shows LOG and above
            WARNING (4)  → Shows WARNING and above
            ERROR (5)    → Shows ERROR and above
            CRITICAL (6) → Shows only CRITICAL
        """

        self.operation_name = operation_name
        self.log_level = log_level
        self.is_timestamp = is_timestamp

    def set_log_level(self, log_level: LogMode):
        """Set the minimum log level to display"""
        self.log_level = log_level

    def _get_timestamp(self) -> str:
        """Generate formatted timestamp"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def _should_log(self, mode: LogMode) -> bool:
        """Check if the message should be logged based on current log level"""
        return mode.priority >= self.log_level.priority

    def _format_message(self, message: str, mode: LogMode) -> str:
        """
        Format the log message with color only on mode and message

        Format: [GREEN_TIMESTAMP][operation_name:ALIGNED_COLORED_MODE]: COLORED_MESSAGE
        """
        color = self.MODE_COLORS.get(mode, AnsiColor.WHITE)
        reset = AnsiColor.RESET.value
        green = AnsiColor.GREEN.value

        parts = []

        # Timestamp in green (if enabled)
        if self.is_timestamp:
            parts.append(f"[{green}{self._get_timestamp()}{reset}]")

        # Operation name (no color) + colored mode
        mode_padded = mode.value
        parts.append(f"[{self.operation_name}: {color.value}{mode_padded}{reset}")
        parts.append(f"]")

        # Colored message
        parts.append(f": {color.value}{message}{reset}")

        return "".join(parts)

    def _log(self, message: str, mode: LogMode):
        """
        Core logging method that handles printing with colors

        Args:
            message: The log message
            mode: The severity mode of the log
        """
        if not self._should_log(mode):
            return

        formatted_msg = self._format_message(message, mode)

        # Print to stderr for errors and critical, stdout for everything else
        if mode in (LogMode.ERROR, LogMode.CRITICAL):
            print(formatted_msg, file=sys.stderr)
        else:
            print(formatted_msg)

    def trace(self, message: str):
        """Print a trace log message"""
        self._log(message, LogMode.TRACE)

    def log(self, message: str):
        """Print a general log message"""
        self._log(message, LogMode.LOG)

    def error(self, message: str):
        """Print an error log message"""
        self._log(message, LogMode.ERROR)

    def warning(self, message: str):
        """Print a warning log message"""
        self._log(message, LogMode.WARNING)

    def info(self, message: str):
        """Print an info log message"""
        self._log(message, LogMode.INFO)

    def debug(self, message: str):
        """Print a debug log message"""
        self._log(message, LogMode.DEBUG)

    def critical(self, message: str):
        """Print a critical log message"""
        self._log(message, LogMode.CRITICAL)

    @staticmethod
    def print(message: str, color: AnsiColor = AnsiColor.GREEN):
        """Static method for simple colored output (maintained from original)"""
        print(f"{color.value}{message}{AnsiColor.RESET.value}")


if __name__ == "__main__":
    print("=== All messages (TRACE level) ===")
    logger = Log(
        operation_name="DataProcessor", log_level=LogMode.TRACE, is_timestamp=True
    )
    logger.trace("This is a trace message")
    logger.debug("Memory usage: 45MB")
    logger.info("Loading configuration file")
    logger.log("Processing started")
    logger.warning("Disk space running low")
    logger.error("Failed to connect to database")
    logger.critical("System shutdown imminent")

    print("\n=== Only WARNING and above ===")
    logger.set_log_level(LogMode.WARNING)
    logger.trace("This trace won't show")
    logger.debug("This debug won't show")
    logger.info("This info won't show")
    logger.log("This log won't show")
    logger.warning("Disk space running low")
    logger.error("Failed to connect to database")
    logger.critical("System shutdown imminent")

    print("\n=== Only CRITICAL ===")
    logger.set_log_level(LogMode.CRITICAL)
    logger.warning("This warning won't show")
    logger.error("This error won't show")
    logger.critical("System shutdown imminent")

    print("\n=== Dynamic level change ===")
    logger.set_log_level(LogMode.DEBUG)
    logger.trace("Still won't show trace")
    logger.debug("Now showing debug again")
    logger.error("Errors always show")
