# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Gabriel López <Developer>)
# Copyright 2019 Quadit (Lázaro Rodríguez <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class StockPicking(models.Model):
    _inherit = "stock.picking"

    is_validate = fields.Boolean(string='Payment Validated?')
    validated_by = fields.Many2one(comodel_name='res.users',
                                   string='Validated by',
                                   readonly=True)

    @api.multi
    def button_validate(self):
        if not self.is_validate:
            raise ValidationError(
                _('You do not have permission to validate the transfer!'))
        return super(StockPicking, self).button_validate()

    @api.multi
    def write(self, values):
        if 'is_validate' in values:
            values['validated_by'] = self.env.uid
        return super(StockPicking, self).write(values)
