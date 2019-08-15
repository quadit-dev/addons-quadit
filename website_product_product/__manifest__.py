# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Gabriel López <Developer>)
# Copyright 2019 Quadit (Lázaro Rodríguez <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Website product attachments',
    'summary': 'Show product attachments on website product form',
    'version': '12.0.1.0.0',
    'category': 'Website',
    'author': 'Quadit, ',
    'website': 'https://www.quadit.mx',
    'license': 'LGPL-3',
    'depends': ['stock', 'website_sale'],
    'sequence': 501,
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/product_view.xml',
        'views/template.xml'
    ],
    'development_status': 'Beta',
    'maintainers': [
        'kuro088'
        'gabrielsnader',
    ],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
