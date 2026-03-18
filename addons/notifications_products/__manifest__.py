  
{
    'name': "Notificación de nuevos productos",
    'version': '17.0.1.0.0',
    'author': "Frans Avila",
    'depends': ['base', 'product', 'stock', 'mail', 'base_setup'],
    'data': [
        'views/views.xml',
        'views/templates.xml',
    ],
    'license': 'LGPL-3',
    'installable': True,
    'application': False,
}

