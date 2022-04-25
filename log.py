import logging
from sys import platform
from logging.handlers import SocketHandler

log = logging.getLogger(platform)
log.setLevel(1)
socket_handler = SocketHandler('127.0.0.1', 19996)
log.addHandler(socket_handler)
