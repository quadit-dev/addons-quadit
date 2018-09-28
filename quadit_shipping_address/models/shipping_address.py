# -*- coding: utf-8 -*-
# © <2017> <Quadit, S.A. de C.V.>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    shipping_address = fields.Char(string='Direccion de Envio')