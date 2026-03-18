# -*- coding: utf-8 -*-
# from odoo import http


# class NotificationsProducts(http.Controller):
#     @http.route('/notifications_products/notifications_products', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/notifications_products/notifications_products/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('notifications_products.listing', {
#             'root': '/notifications_products/notifications_products',
#             'objects': http.request.env['notifications_products.notifications_products'].search([]),
#         })

#     @http.route('/notifications_products/notifications_products/objects/<model("notifications_products.notifications_products"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('notifications_products.object', {
#             'object': obj
#         })

