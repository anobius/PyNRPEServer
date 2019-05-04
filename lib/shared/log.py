#!/usr/bin/env python
#-*- coding: utf-8 -*-

'''
@author: Nico
'''


import logging
import logging.config
import threading
import inspect
import traceback
import sys

#logging.config.fileConfig('logger.ini')

_logger = logging.getLogger("fapplicator")
_logger.setLevel(logging.DEBUG)
_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s","%Y-%m-%d %H:%M:%S")
_handler = logging.StreamHandler()
_handler.setFormatter(_formatter)

_logger.addHandler(_handler)

_tLocal = threading.local();


class logIntf(object):
    @staticmethod
    def info(message,ID=None):
        ID=id(threading.current_thread()) if not ID else ID;
        if message.strip():
            callerstack = inspect.stack()[1];
            fLocals = callerstack[0].f_locals;
            if "self" in fLocals:
                _logger.info("%s::%s(0x%x): %s" % (fLocals["self"].__class__,callerstack[3],ID,message))
                return;
            _logger.info("%s(0x%x): %s" % (callerstack[3],ID,message))

    @staticmethod
    def warn(message,ID=None):
        ID=id(threading.current_thread()) if not ID else ID;
        if message.strip():
            callerstack = inspect.stack()[1];
            fLocals = callerstack[0].f_locals;
            if "self" in fLocals:
                _logger.warn("%s::%s(0x%x): %s" % (fLocals["self"].__class__,callerstack[3],ID,message))
                return;
            _logger.warn("%s(0x%x): %s" % (callerstack[3],ID,message))

    @staticmethod
    def critical(message,ID=None):
        ID=id(threading.current_thread()) if not ID else ID;
        if message.strip():
            callerstack = inspect.stack()[1];
            fLocals = callerstack[0].f_locals;
            if "self" in fLocals:
                _logger.critical("%s::%s(0x%x): %s" % (fLocals["self"].__class__,callerstack[3],ID,message))
                return;
            _logger.critical("%s(0x%x): %s" % (callerstack[3],ID,message))

    @staticmethod
    def error(message,ID=None):
        ID=id(threading.current_thread()) if not ID else ID;
        if message.strip():
            callerstack = inspect.stack()[1];
            fLocals = callerstack[0].f_locals;
            if "self" in fLocals:
                _logger.info("%s::%s(0x%x): %s" % (fLocals["self"].__class__,callerstack[3],ID,message))
                return;
            _logger.error("%s(0x%x): %s" % (callerstack[3],ID,message))

    @staticmethod
    def debug(message,ID=None):
        ID=id(threading.current_thread()) if not ID else ID;
        if message.strip():
            callerstack = inspect.stack()[1];
            fLocals = callerstack[0].f_locals;
            if "self" in fLocals:
                _logger.debug("%s::%s(0x%x): %s" % (fLocals["self"].__class__,callerstack[3],ID,message))
                return;
            _logger.debug("%s(0x%x): %s" % (callerstack[3],ID,message))

    @staticmethod
    def getlasterrortraceback():
        return traceback.format_exc();

    @staticmethod
    def getlasterrormsg():
        print(sys.exc_info())
        exception = sys.exc_info()[1];
        return exception.message if exception else "Message missing !";

    @staticmethod
    def setLastMessage(message):
        _tLocal.message = message;

    @staticmethod
    def getLastMessage():
        try:
            return _tLocal.message;
        except:
            return None;

