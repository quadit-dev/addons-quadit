# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Leticia González <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import time
from datetime import timedelta, datetime
from pytz import timezone
from odoo import api, fields, models


class account_invoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice']

    @api.one
    @api.depends('invoice_line_ids.price_unit', 'invoice_line_ids.discount', 'invoice_line_ids.quantity')
    def descuentos(self):
        for line in self.invoice_line_ids:
            perc2 = line.price_unit * line.discount / 100
            descuentos = sum(l.amount_discount for l in self.invoice_line_ids)
            self.discounts = descuentos

    discounts = fields.Float(
        string='Descuentos', digits=(14, 2), compute="descuentos")


class account_invoice_line(models.Model):
    _name = 'account.invoice.line'
    _inherit = ['account.invoice.line']

    amount_discount = fields.Float(compute='_compute_amount_discount')

    @api.one
    @api.depends('price_unit', 'discount', 'quantity')
    def _compute_amount_discount(self):
        for record in self:
            record.amount_discount = (
                record.price_unit * record.discount / 100) * record.quantity


class FactuParser(models.AbstractModel):
    """Class for report"""
    _name = "report.account_invoice_custom_format.invoice_pdf"
    _description = __doc__

    @api.multi
    def _get_report_values(self, docids, data=None):
        invoice_obj = self.env['account.invoice']
        invoice = invoice_obj.browse(docids)
        return {
            "doc_ids": docids,
            "doc_model": 'account.invoice',
            "docs": invoice,
            'time': time,
            'int': int,
            'datetime': datetime,
            'get_invoice_line': self.get_invoice_line,
            'get_local_tax': self.get_local_tax,
            'get_taxes': self.get_taxes,
            'get_cfdi_folio': self.get_cfdi_folio,
            'get_uso_cfdi': self.get_uso_cfdi,
            'get_fecha_emision': self.get_fecha_emision,
            'get_tipo_comprobante': self.get_tipo_comprobante,
            'get_regimen': self.get_regimen,
            'get_cantidad_letra': self.get_cantidad_letra,
            'get_subtotal': self.get_subtotal,
            'get_descuentos': self.get_descuentos,
            'get_total': self.get_total,
        }

    def get_invoice_line(self, invoice):
        line = []
        lines = []
        # Para cada linea de factura
        for invoice_line in invoice.invoice_line_ids:
            line.append(invoice_line.product_id.default_code)
            line.append(invoice_line.name)
            line.append(invoice_line.quantity)
            line.append(invoice_line.uom_id.name)
            line.append('{:20,.2f}'.format(invoice_line.price_unit))
            line.append('{:20,.2f}'.format(invoice_line.price_subtotal))
            line.append(invoice_line.multiple_discount)
            line.append(invoice_line.claveserv_id.name or '01010101')
            line.append(invoice_line.uom_id.claveuni_id.clave or 'H87')
            taxes_list = []
            for tax in invoice_line.invoice_line_tax_ids:
                taxes_list.append({
                    'name': tax.name,
                    'amount': '%.2f' % (
                        invoice_line.price_subtotal * (tax.amount / 100)),
                })
            line.append(taxes_list)
            lines.append(line)
            line = []
        return lines

    def get_cfdi_folio(self, invoice):
        if not invoice.sign:
            return ""
        try:
            tree = invoice.cfdi_etree()
            tfd = invoice._get_stamp_data(tree)
            return tfd.get('SelloCFD', '')
        except:
            "SIN SELLO"

    def get_taxes(self, invoice):
        taxes_list = []
        for tax in invoice.tax_line_ids:
            taxes_list.append({
                'name': tax.name,
                'amount': '{:20,.2f}'.format(tax.amount)
            })
        return taxes_list

    def get_uso_cfdi(self, invoice):
        if invoice.sign:
            try:
                tree = invoice.cfdi_etree()
                uso_cfdi = tree.Receptor.get('UsoCFDI')
                # Buscamos el uso en los catálogos
                res_uso_cfdi_row = self.env['res.uso.cfdi'].search([
                    ('name', '=', uso_cfdi)])
                uso_cfdi_text = uso_cfdi + " - " + res_uso_cfdi_row.description or ""
                return uso_cfdi_text
            except:
                return "SIN USO CFDI"
        else:
            return "SIN USO CFDI"

    def _get_time_zone(self):
        res_users_obj = self.env['res.users']
        userstz = res_users_obj.browse(self._uid).tz
        a = 0
        if userstz:
            hours = timezone(userstz)
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            now = datetime.now()
            loc_dt = hours.localize(datetime(now.year, now.month, now.day,
                                             now.hour, now.minute, now.second))
            timezone_loc = (loc_dt.strftime(fmt))
            diff_timezone_original = timezone_loc[-5:-2]
            timezone_original = int(diff_timezone_original)
            s = str(datetime.now(timezone(userstz)))
            s = s[-6:-3]
            timezone_present = int(s)*-1
            a = timezone_original + ((
                timezone_present + timezone_original)*-1)
        return a

    def get_fecha_emision(self, invoice):
        time_zone = self._get_time_zone()
        if invoice.invoice_datetime_33:
            dte = fields.Datetime.from_string(invoice.invoice_datetime_33)
        else:
            dte = datetime.strptime(
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                '%Y-%m-%d %H:%M:%S')
        return (dte + timedelta(hours=time_zone))

    def get_tipo_comprobante(self, invoice):
        if invoice.sign:
            try:
                tree = invoice.cfdi_etree()
                tipo = tree.get('TipoDeComprobante', '')
                if tipo == 'I':
                    tipo += " - Ingreso"
                if tipo == 'E':
                    tipo += " - Egreso"
                return tipo
            except:
                return "SIN TIPO"
        else:
            return ""

    def get_regimen(self, invoice):
        reg = invoice.company_emitter_id.partner_id.property_account_position_id  # noqa
        return reg.name

    def get_cantidad_letra(self, invoice):
        currency = invoice.currency_id.name.upper()
        # M.N. = Moneda Nacional (National Currency)
        # M.E. = Moneda Extranjera (Foreign Currency)
        currency_type = 'M.N' if currency == 'MXN' else 'M.E.'
        # Split integer and decimal part
        amount_i, amount_d = divmod(invoice.amount_total, 1)
        amount_d = round(amount_d, 2)
        amount_d = int(round(amount_d * 100, 2))
        words = invoice.currency_id.with_context(
            lang=invoice.partner_id.lang or 'es_ES').amount_to_text(
                amount_i).upper()
        return '%(words)s %(amount_d)02d/100 %(curr_t)s' % dict(
            words=words, amount_d=amount_d, curr_t=currency_type)

    def get_subtotal(self, invoice):
        return '{:20,.2f}'.format(invoice.amount_untaxed)

    def get_descuentos(self, invoice):
        return '{:20,.2f}'.format(invoice.discounts)

    def get_total(self, invoice):
        return '{:20,.2f}'.format(invoice.amount_total)

    def get_local_tax(self):
        local_taxes = []
        if self.dic:
            local_taxes = self.dic.get('cfdi:Complemento', {}).get(
                'implocal:ImpuestosLocales', {}).get('implocal:RetencionesLocales', [])
        taxes_list = []
        for tax in local_taxes:
            taxes_list.append({'importe': tax.get('@Importe', 0.0), 'name': tax.get(
                '@ImpLocRetenido', ''), 'tasa': tax.get('@TasadeRetencion', '')})
        return taxes_list or []
