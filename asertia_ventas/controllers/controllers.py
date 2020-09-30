# -*- coding: utf-8 -*-
from odoo import http

# class AsertiaVentas(http.Controller):
#     @http.route('/asertia_ventas/asertia_ventas/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/asertia_ventas/asertia_ventas/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('asertia_ventas.listing', {
#             'root': '/asertia_ventas/asertia_ventas',
#             'objects': http.request.env['asertia_ventas.asertia_ventas'].search([]),
#         })

#     @http.route('/asertia_ventas/asertia_ventas/objects/<model("asertia_ventas.asertia_ventas"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('asertia_ventas.object', {
#             'object': obj
#         })