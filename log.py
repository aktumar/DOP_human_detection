import logging
import config
from sys import platform
from logging.handlers import SocketHandler

log = logging.getLogger(platform)
log.setLevel(1)
socket_handler = SocketHandler(config.LOG_IP, config.LOG_PORT)
log.addHandler(socket_handler)
