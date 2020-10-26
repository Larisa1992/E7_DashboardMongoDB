MONGO_HOST = 'mongodb'
MONGO_PORT = 27017
MONGO_DBNAME = 'board'

DATE_FORMAT = '%Y-%m-%d'

HATEOAS = False

# допустимые методы для пути
# /document/
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']

# допустимые методы для пути
# /document/<ObjectId>
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

    # Описываем ресурс `/document`
document = {
        
    'schema': {
        'title': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 100,
        },
        'date': {
            'type': 'datetime',
        },
        'message': {
            'type': 'string',
            'minlength': 1,
            'maxlength': 250,
        },
        'author': {                
            'type': 'string',
        },
        'images': {
            'type': 'list', # тип: список
        },
        'tags': {
            'type': 'list',
        },
        'comments': {
            'type': 'list',
        }
    }
}

DOMAIN = {'document': document,}