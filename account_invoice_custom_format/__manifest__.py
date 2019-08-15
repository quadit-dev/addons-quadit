# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Leticia González <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Account Invoice Custom Format',
    'summary': 'Simple custom format for account invoice cfdi',
    'version': '12.0.1.0.0',
    'category': 'Accounting & Finance',
    'author': 'Quadit, ',
    'website': 'https://www.quadit.mx',
    'license': 'LGPL-3',
    'depends': ['account', 'l10n_mx_facturae_33',
                'account_invoice_discount_formula'],
    'sequence': 501,
    'demo': [],
    'data': [
        'views/report_invoice.xml',
    ],
    'development_status': 'Beta',
    'maintainers': [
        'leti12',
    ],
    'installable': True,
}
