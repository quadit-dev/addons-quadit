# -*- coding: utf-8 -*-
# © <2017> <Quadit, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{

    'name': 'Sale Order Custom Report',
    'version': '8.0.1.0.0',
    'category': 'Report',
    'website': 'https://www.quadit.mx',
    'author': 'Quadit, S.A. de C.V.',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'summary': 'Sale Order Report Custom',
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'sale',
    ],
    'data': [
        'reports/custom_sale_order.xml',
    ],
}
