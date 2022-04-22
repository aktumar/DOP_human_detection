import logging

from PyQt5 import QtWidgets


def create_logger(path, widget: QtWidgets.QTextEdit):
    log = logging.getLogger('main')
    log.setLevel(logging.DEBUG)

    file_formatter = logging.Formatter(
        ('#%(levelname)-s, %(pathname)s, line %(lineno)d, [%(asctime)s]: '
         '%(message)s'), datefmt='%Y-%m-%d %H:%M:%S'
    )
    console_formatter = logging.Formatter(('#%(levelname)-s, %(pathname)s, '
                                           'line %(lineno)d: %(message)s'))

    log_window_formatter = logging.Formatter(
        '#%(levelname)-s, %(message)s\n'
    )

    file_handler = logging.FileHandler(path)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(console_formatter)

    log_window_handler = logging.Handler()
    log_window_handler.emit = lambda record: widget.insertPlainText(
        log_window_handler.format(record)
    )
    log_window_handler.setLevel(logging.DEBUG)
    log_window_handler.setFormatter(log_window_formatter)

    log.addHandler(file_handler)
    log.addHandler(console_handler)
    log.addHandler(log_window_handler)


def test():
    logger = logging.getLogger('main')
    logger.error('ошибка 1')
    logger.error('ошибка 2')
    logger.critical('критическая ошибка 1')


app = QtWidgets.QApplication([])
win = QtWidgets.QTextEdit()
win.setReadOnly(True)
win.show()

create_logger('./log', win)
test()

app.exec_()