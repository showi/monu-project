from monu.conf import conf
from monu.srv.application import application as _application

application = _application.app

if __name__ == '__main__':
    host = conf.get('uwsgi', 'host')
    port = conf.getint('uwsgi', 'port')
    application.run(port=port, host=host, debug=True)
