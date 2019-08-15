# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Gabriel López <Developer>)
# Copyright 2019 Quadit (Lázaro Rodríguez <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ProductProductImage(models.Model):
    _name = 'product.product.image'

    img_product = fields.Binary()
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template')


class ProductProductPdf(models.Model):
    _name = 'product.product.pdf'
    _rec_name = 'filename'

    filename = fields.Char()
    pdf_product = fields.Binary()
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template')


class ProductProductText(models.Model):
    _name = 'product.product.text'

    txt_product = fields.Binary()
    product_tmpl_id = fields.Many2one(
        comodel_name='product.template',
        string='Product Template')


class ProductProduct(models.Model):
    _inherit = 'product.template'

    pdf_ids = fields.One2many('product.product.pdf', 'product_tmpl_id', 'PDFs')
    img_ids = fields.One2many('product.product.image', 'product_tmpl_id', 'Images')
    txt_ids = fields.One2many('product.product.text', 'product_tmpl_id', 'Txts')
