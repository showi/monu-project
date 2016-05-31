# -*- coding: utf-8 -*-

from monu.logger import getLogger
from datetime import datetime

log = getLogger(__name__)

__FORMAT_GMT__ = '%a, %d %b %Y %H:%M:%S GMT'


def sgetattr(resource, name):
    try:
        return getattr(resource, name)
    except Exception as e:
        log.critical('Error: %s', e)
    return None


def column_convert(column, output):
    """Convertit les données en fonction du type de colonne
    """
    if output is None:
        return None
    if column.name in ['until', 'created_on', 'respond_on', 'updated_on']:
        return output.strftime(__FORMAT_GMT__)
    return output


def res2dct(resource, safe=True, debug=True):
    """Database row to dictionary"""
    data = {}
    if safe is True:
        def skipit(name):
            if name not in __SAFE_PROPERTY__:
                if debug:
                    log.warn('(res2dct) Property not in safe list: %s', name)
                return True
            return False
    else:
        def skipit(name):
            return False
    for column in resource.__table__.columns:
        if skipit(column.name):
            continue
        data[column.name] = column_convert(
            column, sgetattr(resource, column.name))
    return data


def time2http(t):
    """Helper"""
    return t.strftime(__FORMAT_GMT__)


def datetime2second(d, fmt='%Y-%m-%d %H:%M:%S'):
    """Helper"""
    now = datetime.utcnow()
    seconds = (d - now).total_seconds()
    return seconds


def digestify(doc, keyring=['ingredient', 'child', 'step']):
    if 'child' in doc:
        for child in doc['child']:
            digestify(child, keyring)
    for key in keyring:
        if key in doc:
            del doc[key]
