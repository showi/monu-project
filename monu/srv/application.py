import os.path as path
from flask import Flask, send_from_directory
from flask_restful import Api
# import flask.ext.uploads as uploads  # @UnresolvedImport @UnusedImport


from monu.conf import conf
import monu.logger
from monu.srv import res as resource
log = monu.logger.getLogger('srv.application')

allowed_extensions = ('fs', )


class Application(object):
    def __init__(self):
        log.info('[%s] Init', self.__class__.__name__)
        self.app = Flask(__name__,
                         static_url_path=conf.get('ui', 'static_folder'))
        self.api = Api(self.app)
        self.debug = True
        self.init_configure()
        self.init_api()
        # self.init_storage()
        self.init_static()

    def init_configure(self):
        log.info('[%s] Init configure', self.__class__.__name__)
        self.app.config['SECRET_KEY'] = conf.get('backend', 'secret')
        self.app.config['BUNDLE_ERRORS'] = True
        # self.app.config['UPLOAD_FOLDER'] = conf.get('backend.storage', 'path')

    def init_api(self):
        log.info('[%s] Init api', self.__class__.__name__)
       # self.api.add_resource(resource.Ref,
       #                       '/api/ref/<string:collection>/<string:key>/<string:value>')
        self.api.add_resource(resource.Tag,
                              '/api/tag',
                              '/api/tag/<string:key>/<string:value>')
        self.api.add_resource(resource.Ingredient,
                              '/api/ingredient',
                              '/api/ingredient/<string:key>/<string:value>')
        self.api.add_resource(resource.Recipe,
                              '/api/recipe',
                              '/api/recipe/<string:key>/<string:value>')
        self.api.add_resource(resource.Schema,
                              '/api/schema',
                              '/api/schema/<string:name>')

    def init_storage(self):
        log.info('[%s] Init Storage', self.__class__.__name__)
        self.fileSet = uploads.UploadSet('files', uploads.ALL)
        self.app.config['UPLOADED_FILES_DEST'] = conf.get('backend.storage',
                                                          'path')
        uploads.configure_uploads(self.app, (self.fileSet,))
        uploads.patch_request_class(self.app, 512 * 1024 * 1024)  # Set max file upload 512MiB

    def init_static(self):
        if not conf.getboolean('ui', 'serve_static'):
            log.info('[-] not serving static')
            return False
        static_folder = conf.get('ui', 'static_folder')
        dist = path.basename(static_folder).lower() == 'dist'
        log.info('dist: %s', dist)
        component_folder = path.abspath(path.join(static_folder,
                                                  path.pardir,
                                                  'bower_components'))
        log.info('[%s] Init static', self.__class__.__name__)
        log.info(' - static_folder: %s', static_folder)
        if not dist:
            log.info(' - component_folder: %s', component_folder)

            @self.app.route('/bower_components/<path:path>')
            def send_components(path):
                return send_from_directory(component_folder, path)

        @self.app.route('/<path:path>')
        def send_html(path):
            return send_from_directory(static_folder, path)

        @self.app.route('/')
        def root():
            return send_from_directory(static_folder, 'index.html')

    def run(self, *a, **ka):
        if not 'debug' in ka:
            ka['debug'] = self.debug
        if not 'host' in ka:
            ka['host'] = conf.get('backend', 'host')
        if not 'port' in ka:
            ka['port'] = conf.get('backend', 'port')
        return self.app.run(*a, **ka)


application = Application()

if __name__ == '__main__':
    application.run(debug=True)
