#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Return disk usage statistics about the given path as a (total, used, free)
namedtuple.  Values are expressed in bytes.
"""
# Author: Giampaolo Rodola' <g.rodola [AT] gmail [DOT] com>
# License: MIT

import os
import collections
import re

_ntuple_diskusage = collections.namedtuple('usage', 'total used free')

if hasattr(os, 'statvfs'):  # POSIX
    def usage(path):
        st = os.statvfs(path)
        free = st.f_bavail * st.f_frsize
        total = st.f_blocks * st.f_frsize
        used = (st.f_blocks - st.f_bfree) * st.f_frsize
        return _ntuple_diskusage(total, used, free)

elif os.name == 'nt':  # Windows
    import ctypes
    import sys


    def usage(path):
        _, total, free = ctypes.c_ulonglong(), ctypes.c_ulonglong(), \
                         ctypes.c_ulonglong()
        if sys.version_info >= (3,) or isinstance(path, unicode):
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExW  # @UndefinedVariable
        else:
            fun = ctypes.windll.kernel32.GetDiskFreeSpaceExA  # @UndefinedVariable
        ret = fun(
            path, ctypes.byref(_), ctypes.byref(total), ctypes.byref(free))
        if ret == 0:
            raise ctypes.WinError()
        used = total.value - free.value
        return _ntuple_diskusage(total.value, used, free.value)
else:
    raise NotImplementedError("platform not supported")

usage.__doc__ = __doc__

__SYMBOLS__ = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
__PREFIX__ = {}

for i, s in enumerate(__SYMBOLS__):
    __PREFIX__[s] = 1 << (i + 1) * 10


def bytes2human(n):
    for s in reversed(__SYMBOLS__):
        if n >= __PREFIX__[s]:
            value = float(n) / __PREFIX__[s]
            return '%.1f%s' % (value, s)
    return "%sB" % n


re_human_bytes = re.compile('^([\d+.]+)\s*(%s)?\s*$' % '|'.join(__SYMBOLS__),
                            re.IGNORECASE)


def human2bytes(n):
    m = re_human_bytes.match(n)
    if m is None:
        raise RuntimeError('Invalid human size: %s' % n)
    size = long(m.group(1))
    prefix = m.group(2).upper()
    if prefix:
        size *= __PREFIX__[prefix]
    return size


if __name__ == '__main__':
    print usage(os.getcwd())
    for n in ['235K', '1M', '1G', '123G']:
        print '%s: %sB' % (n, human2bytes(n))
