# -*- coding: utf-8 -*-
# © <2017> <Quadit, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{

    'name': 'Purchase Order Custom Report',
    'version': '8.0.1.0.0',
    'category': 'Report',
    'website': 'https://www.quadit.mx',
    'author': 'Quadit, S.A. de C.V., Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'application': False,
    'installable': True,
    'summary': 'Purchase Order Report Custom',
    'external_dependencies': {
        'python': [],
        'bin': [],
    },
    'depends': [
        'purchase',
    ],
    'data': [
        'reports/custom_purchase_order.xml',
    ],
}