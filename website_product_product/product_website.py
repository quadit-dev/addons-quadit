# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _


class product_product_image(models.TransientModel):
	_name = 'product.product.image'

	img_product = fields.Binary('')
	img_id = fields.Many2one('product.template', readonly=False)


class product_product_pdf(models.TransientModel):
	_name = 'product.product.pdf'

	pdf_product = fields.Binary('')
	pdf_id = fields.Many2one('product.template', 'ID Ref', invisible=True)


class product_product_text(models.TransientModel):
	_name = 'product.product.text'

	txt_product = fields.Binary('')
	txt_id = fields.Many2one('product.template', 'ID Ref', invisible=True)


class product_product(models.Model):
	_inherit = 'product.template'

	pdf_ids = fields.One2many('product.product.pdf', 'pdf_id', 'PDFs')
	img_ids = fields.One2many('product.product.image', 'img_id', 'Images')
	txt_ids = fields.One2many('product.product.text', 'txt_id', 'Txt')

