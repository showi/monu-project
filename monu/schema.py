# -*- coding: utf-8 -*-

SCHEMA = {
    'ingredient': {
        'type': 'object',
        'title': 'Ingredient',
        'format': 'tabs',
        '_id': {'type': 'string'},
        'name': {'type': 'string'},
        'language': {'type': 'string'},
        'tag': {
            'type': 'object',
            "format": "table",
            "title": "Tagssss",
            "uniqueItems": True,
            "properties": {
                'name': {
                    'title': 'tags',
                    '$ref': '/api/schema/tag'
                },
                'location': {
                    '$ref': '/api/tag?noHeader=1'
                },
            },
        },
    },
    'tag': {
        'type': 'object',
        'title': 'Etiquette',
        'format': 'tabs',
    },
    'recipe': {
        'type': 'object',
        'title': 'Recette',
        'format': 'tabs',
    }
}
ingredient = SCHEMA['ingredient']
tag = SCHEMA['tag']
