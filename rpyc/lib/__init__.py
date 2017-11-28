"""
A library of various helpers functions and classes
"""
import sys
import logging
import logging.handlers


class MissingModule(object):
    __slots__ = ["__name"]
    def __init__(self, name):
        self.__name = name
    def __getattr__(self, name):
        if name.startswith("__"): # issue 71
            raise AttributeError("module %r not found" % (self.__name,))
        raise ImportError("module %r not found" % (self.__name,))
    def __bool__(self):
        return False
    __nonzero__ = __bool__

def safe_import(name):
    try:
        mod = __import__(name, None, None, "*")
    except ImportError:
        mod = MissingModule(name)
    except Exception:
        # issue 72: IronPython on Mono
        if sys.platform == "cli" and name == "signal": #os.name == "posix":
            mod = MissingModule(name)
        else:
            raise
    return mod

def setup_logger(quiet = False, logfile = None):
    log_format = "%(asctime)s|%(threadName)-25s|%(name)-30s|%(levelname)-5s|%(funcName)-30s |%(message)s"
    log_level = logging.ERROR if quiet else logging.DEBUG
    logging.basicConfig(format=log_format, level=log_level)
    if logfile:
        max_size = 50 * 1024 * 1024  # 50 MB
        formatter = logging.Formatter(fmt=log_format)
        rotating_file_handler = logging.handlers.RotatingFileHandler(logfile, maxBytes=max_size, backupCount=1)
        rotating_file_handler.setFormatter(formatter)
        logging.root.addHandler(rotating_file_handler)
