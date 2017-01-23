# -*- coding: utf-8 -*-
# © <2016> <QuadIT>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class HotelReservation(models.Model):

    _inherit = 'hotel.reservation'

    @api.model
    def create(self, values):
        res = super(HotelReservation, self).create(values)
        email_template_obj = self.env['email.template']
        template_ids = email_template_obj.search([
            ('model', '=', 'hotel.reservation'),
            ('create_reservation', '=', True),
        ], limit=1)
        if template_ids:
            values = email_template_obj.generate_email(template_ids.id, res)
            mail_mail_obj = self.env['mail.mail']
            msg_id = mail_mail_obj.create(values)
            if msg_id:
                msg_id.send()
        return res

    @api.model
    def write(self, values):
        res = super(HotelReservation, self).write(values)
        res = super(HotelReservation, self).create(values)
        email_template_obj = self.env['email.template']
        template_ids = email_template_obj.search([
            ('model', '=', 'hotel.reservation'),
            ('update_reservation', '=', True),
        ], limit=1)
        if template_ids:
            values = email_template_obj.generate_email(template_ids.id, res)
            mail_mail_obj = self.env['mail.mail']
            msg_id = mail_mail_obj.create(values)
            if msg_id:
                msg_id.send()
        return res
