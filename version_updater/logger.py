import logging
import daiquiri
import daiquiri.formatter


def identify_debug_level(level: str) -> int:
    try:
        return getattr(logging, level)
    except AttributeError:
        return 10


def logger(level: str = "DEBUG"):
    daiquiri.setup(
        level=identify_debug_level(level),
        outputs=(
            daiquiri.output.Stream(
                formatter=daiquiri.formatter.ColorFormatter(
                    fmt="%(asctime)s  %(filename)s: %(lineno)4s  [%(levelname)5s]  %(message)s"
                )
            ),
        ),
    )
    return daiquiri.getLogger(__name__)
