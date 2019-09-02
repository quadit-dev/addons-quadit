# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Gabriel López <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_validate = fields.Boolean(string='Payment Validate?')

    @api.multi
    def button_validate(self):
        if not self.is_validate:
            raise ValidationError(
                _('You do not have permission to validate the transfer!'))
        return super(StockPicking, self).button_validate()
