# -*- coding: utf-8 -*-

from flask_restful import reqparse


def parser_factory(namespace='main', locations=['headers', 'values', 'json']):
    """Parsing HTTP request parameters (headers, forms, query string)
    
        Note: On devrait parse en fonction de la requête browse/get
        command/get...
    """
    parser = reqparse.RequestParser(trim=True, bundle_errors=True)

    def addarg(*a, **ka):
        """helper"""
        if 'location' not in ka:
            ka['location'] = locations
        parser.add_argument(*a, **ka)

    if namespace in ['main', 'ingredient', 'tag']:
        addarg('noHeader', type=bool, required=False, default=False)
    # if namespace in ['main', 'browse.post']:
    #     addarg('computername', required=False)
    #     addarg('username', required=False)
    #     addarg('platform', required=False)
    #     addarg('auth', required=False)
    #     addarg('getcmd', required=False, type=bool)
    #     addarg('keys', required=False)
    #     addarg('type', required=False)  
    #     addarg('action', required=False)
    #     addarg('command_id', required=False, type=int)
    #     addarg('command', required=False, type=int)
    #     addarg('client_id', required=False, type=int)
    #     addarg('sort', required=False, choices=['asc', 'desc'], default='asc')
    #     addarg('order_by', required=False, choices=['created_on', 'respond_on'],
    #            default='created_on')
    #     addarg('last_id', required=False, type=int)
    #     addarg('limit', required=False, default=10, type=int)
    #     addarg('offset', required=False, default=0, type=int)
    # elif namespace in 'entrypoint':
    #     addarg('computername', required=True)
    #     addarg('username', required=True)
    #     addarg('platform', required=True)
    #     addarg('auth', required=True)
    #     addarg('getcmd', required=False, type=bool)
    #     addarg('keys', required=False)
    #     addarg('type', required=False)  
    #     addarg('response', required=False)
    #     addarg('mode', required=False)
    #     addarg('client', required=False)
    #     addarg('client_id', required=False, type=int)
    #     addarg('command', required=False)
    #     addarg('command_id', required=False, type=int)
    #     addarg('error_code', required=False, type=int)
    #     addarg('error', required=False)                        
    # elif namespace == 'browse.get':
    #     addarg('path', required=True)
    #     addarg('mode', required=True)
    #     addarg('preview', required=False)
    #     addarg('client_id', required=True, type=int)
    # elif namespace == 'command.post':
    #     addarg('client_id', required=True, type=int)
    #     addarg('command', required=True)
    #     addarg('type', required=True)
    #     addarg('action', required=True)
    # elif namespace == 'command.put':
    #     addarg('response', required=False)
    #     addarg('error', required=False)
    #     addarg('error_code', required=False, type=int)
    # elif namespace == 'file':
    #     addarg('mime', required=False, default="application/octet-stream")
    else:
        raise RuntimeError('Unknow namespace:%s' % namespace)
    return parser
