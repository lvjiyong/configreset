# -*- coding: UTF-8 -*-
# lvjiyong on 2016/5/7.
import logging

import sys

_log_console = logging.StreamHandler(sys.stderr)
_formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
_log_console.setFormatter(_formatter)
logger = logging.getLogger('configreset')
logger.setLevel(logging.ERROR)
logger.addHandler(_log_console)

__all__ = ['logger']
