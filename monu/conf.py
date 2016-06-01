# -*- coding: utf-8 -*-

from os import path
from os.path import expanduser
import ConfigParser

from monu import base_path
import monu.disk as disk

class Configuration(ConfigParser.ConfigParser):
    name = 'app.conf'

    def __init__(self):
        home = expanduser("~")
        ConfigParser.ConfigParser.__init__(self)
        paths = [
            path.join(base_path, 'monu', 'data', self.name),
            path.join('etc', 'monu', self.name),
            path.join(home, '.config', 'tmpy', self.name),
            path.join(home, '.%s' % self.name)
        ]
        self.read(paths)

    def g(self, _path, separator='.'):
        args = _path.split(separator, 1)
        if len(args) < 2:
            raise ValueError('Unvalid path %s (<section>%s<key>)' % (_path, separator))
        return self.get(*args)

    def get(self, section, path):
        value = ConfigParser.ConfigParser.get(self, section, path)
        if value is None:
            if section == 'main' and path == 'data_path':
                return path.join(base_path, 'data')
            return None
        value = value.replace('%base_path%', base_path)
        if section is not 'main' and path is not 'data_path':
            value = value.replace('%data_path%', self.get('main', 'data_path'))
        return value

    def getbytes(self, section, path):
        return disk.human2bytes(self.getint(section, path))

    def dump(self):
        out = {}
        current = None
        for section in self._sections:
            current = self._sections[section]
            out[section] = {}
            for key in current:
                if key in ['__name__']:
                    continue
                out[section][key] = current[key]
        return out


conf = Configuration()
conf.set('main', 'base_path', base_path)
