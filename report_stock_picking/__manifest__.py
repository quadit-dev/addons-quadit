# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Gabriel López <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Inventory Incident Report',
    'summary': 'Add custom format in stock picking ',
    'version': '12.0.1.0.0',
    'category': 'Inventory',
    'author': 'Quadit, ',
    'website': 'https://www.quadit.mx',
    'license': 'LGPL-3',
    'depends': ['stock'],
    'sequence': 501,
    'demo': [],
    'data': [
        'report/stock_report.xml',
    ],
    'qweb': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
