from logging import StreamHandler, getLogger, Formatter, DEBUG, INFO
from sys import stdout

logger = getLogger("inqbus.bokeh.leaflet")
formatter = Formatter('%(asctime)s %(levelname)-8s %(message)s',
                      "%Y-%m-%d %H:%M:%S")



__all__ = ["logger"]

consoleHandler = StreamHandler(stdout)

consoleFormatter = formatter
consoleHandler.setFormatter(consoleFormatter)
consoleHandler.setLevel(INFO)

logger.addHandler(consoleHandler)

logger.propagate = False
logger.setLevel(DEBUG)
