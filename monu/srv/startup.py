from os import path, mkdir

from monu.conf import conf


def on_start():
    data_path = conf.get('main', 'data_path')
    print('DataPath: %s' % data_path)
    #     mode = conf.getint('main', 'directory_mode')
    if not path.exists(data_path):
        mkdir(data_path)


if __name__ == '__main__':
    on_start()
