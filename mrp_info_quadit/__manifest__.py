# -*- coding: utf-8 -*-
# © <2017> <Quadit, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).


{
    "name": "MRP Info Quadit",
    "summary": "Agrega la descripcion del producto",
    "version": "10.0.2.2",
    "category": "Manufacturing",
    "website": "https://www.quadit.mx",
    "author": 'Quadit, S.A. de C.V., Odoo Community Association (OCA)',
    "license": "AGPL-3",
    "application": False,
    'installable': True,
    "depends": [
        "dvit_mrp_sale_info"
    ],
    "data": [
        "reports/quadit_mrp_report.xml"
    ]
}
