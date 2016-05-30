# -*- coding: utf-8 -*-
import os
import sys
import traceback
import datetime
import pytz
import hashlib
from functools import partial

from monu.conf import conf
from monu.logger import getLogger

log = getLogger(__file__)


def file_as_string(path):
    out = ''
    for line in readfile(path):
        out += line
    return out.strip()


def readfile(path):
    with open(path) as fh:
        for line in fh:
            yield line


def pretty_dict(dct, removeNone=True):
    clean = {}
    for key, value in dct.items():
        if removeNone is True and value is None:
            continue
        clean[key] = value
    return clean


def hashit(algo='sha256', delimit='-', *args):
    """Concatain and hash args list
    """
    hl = hashlib.new("sha256")
    for s in args:
        hl.update('-%s' % s)
    return hl.hexdigest()


def trace(e):
    _etype, _value, tb = sys.exc_info()
    log.critical('%s', traceback.format_exception(type(e), e, tb))


def unlink(path):
    """Efface le ficher désigné par path si il existe
    """
    if not os.path.exists(path):
        return False
    log.error('Error: File exists, unlinling path: %s', path)
    os.unlink(path)
    return True


def hashit_fs(fh, kind='sha256', fmt='hexdigest'):
    m = getattr(hashlib, kind)()
    offset = fh.tell()
    fh.seek(0)
    size = 0
    for chunk in iter(partial(fh.read, 8192), ''):
        size += len(chunk)
        m.update(chunk)
    fh.seek(offset)
    return getattr(m, fmt)(), size


def get_upload_path(name):
    return os.path.join(conf.get('frontend.upload', 'path'), name)


def utcnow():
    return datetime.datetime.now(tz=pytz.utc)


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def i2b(n):
    if isinstance(n, bool):
        return n
    if isinstance(n, basestring):
        if n.lower().strip() in ['0', 'false']:
            return False
        return True
    return bool(n)
