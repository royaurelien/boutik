# -*- coding: utf-8 -*-
# from odoo import http


# class Blank(http.Controller):
#     @http.route('/blank/blank/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/blank/blank/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('blank.listing', {
#             'root': '/blank/blank',
#             'objects': http.request.env['blank.blank'].search([]),
#         })

#     @http.route('/blank/blank/objects/<model("blank.blank"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('blank.object', {
#             'object': obj
#         })
