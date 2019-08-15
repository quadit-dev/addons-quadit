# Copyright 2019 Quadit, S.A. de C.V. - https://www.quadit.mx
# Copyright 2019 Quadit (Gabriel López <Developer>)
# Copyright 2019 Quadit (Lázaro Rodríguez <Developer>)
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

import base64
import io
from werkzeug.utils import redirect
from werkzeug.exceptions import NotFound

from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSale(WebsiteSale):

    @http.route(['/shop/product/<model("product.template"):product>'],
                type='http', auth="public", website=True)
    def product(self, product, category='', search='', **kwargs):
        if not product.can_access_from_current_website():
            raise NotFound()

        add_qty = int(kwargs.get('add_qty', 1))

        product_context = dict(request.env.context, quantity=add_qty,
                               active_id=product.id,
                               partner=request.env.user.partner_id)
        ProductCategory = request.env['product.public.category']

        if category:
            category = ProductCategory.browse(int(category)).exists()

        attrib_list = request.httprequest.args.getlist('attrib')
        attrib_values = [[int(x) for x in v.split("-")] for v in attrib_list if v]
        attrib_set = {v[1] for v in attrib_values}

        keep = QueryURL('/shop', category=category and category.id, search=search, attrib=attrib_list)

        categs = ProductCategory.search([('parent_id', '=', False)])

        pricelist = request.website.get_current_pricelist()

        def compute_currency(price):
            return product.currency_id._convert(price, pricelist.currency_id, product._get_current_company(pricelist=pricelist, website=request.website), fields.Date.today())

        if not product_context.get('pricelist'):
            product_context['pricelist'] = pricelist.id
            product = product.with_context(product_context)

        attachments = request.env['ir.attachment'].search(
            [('res_model', '=', 'product.template'),
             ('res_id', '=', product.id)], order='id')
        pdfs = request.env['product.product.pdf'].search_read(
            [('product_tmpl_id', '=', product.id)], ['filename', 'pdf_product'])
        print("=>pdfs", pdfs)

        values = {
            'search': search,
            'category': category,
            'pricelist': pricelist,
            'attrib_values': attrib_values,
            # compute_currency deprecated, get from product
            'compute_currency': compute_currency,
            'attrib_set': attrib_set,
            'keep': keep,
            'categories': categs,
            'main_object': product,
            'product': product,
            'add_qty': add_qty,
            'optional_product_ids': [p.with_context({'active_id': p.id}) for p in product.optional_product_ids],  # noqa
            # get_attribute_exclusions deprecated, use product method
            'get_attribute_exclusions': self._get_attribute_exclusions,
            'attachments': attachments,
            'pdfs': pdfs
        }
        return request.render("website_sale.product", values)

    @http.route(['/attachment/download'], type='http', auth='public')
    def download_attachment(self, attachment_id):
        # Check if this is a valid attachment id
        attachment = request.env['ir.attachment'].sudo().search_read(
            [('id', '=', int(attachment_id))],
            ["name", "datas", "file_type", "res_model", "res_id",
             "type", "url"]
        )

        if attachment:
            attachment = attachment[0]
        else:
            return redirect('/shop')

        if attachment["type"] == "url":
            if attachment["url"]:
                return redirect(attachment["url"])
            else:
                return request.not_found()
        elif attachment["datas"]:
            # decode = base64.b64decode(attachment["datas"])
            datas = io.BytesIO(base64.standard_b64decode(attachment["datas"]))
            return http.send_file(datas, filename=attachment['name'],
                                  as_attachment=True)
        else:
            return request.not_found()

    @http.route(['/pdf/download'], type='http', auth='public')
    def download_pdf(self, pdf_id):
        print("PDF ID", pdf_id)
        pdf = request.env['product.product.pdf'].search_read(
            [('id', '=', pdf_id)], ['filename', 'pdf_product'])[0]
        print("DOWNLOAD PDF", pdf)
        if pdf:
            datas = io.BytesIO(base64.standard_b64decode(pdf['pdf_product']))
            return http.send_file(datas, filename=pdf['filename'],
                                  as_attachment=True)
        else:
            return request.not_found()
