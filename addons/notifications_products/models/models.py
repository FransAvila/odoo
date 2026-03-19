from weakref import ref

from odoo import api, fields, models

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_new_product = fields.Boolean(string="¿Es nuevo?", default=False, copy=False)
    created_by_user_id = fields.Many2one('res.users', string="Creado por", readonly=True)
    
    @api.model
    def create(self, vals):
        config_user_ids = self.env['ir.config_parameter'].sudo().get_param('notifications_products.monitored_user_ids', '')
        monitored_ids = [int(id) for id in config_user_ids.split(',') if id]

        res = super(ProductTemplate, self).create(vals)

        if self.env.uid in monitored_ids:
            res.write({
                'is_new_product': True,
                'created_by_user_id': self.env.uid
            })

            res._send_new_product_notification() 
        
        return res
     
    # Funcion para validar el producto, es la que elimina el liston del documento 
    def action_remove_new_label(self):
        self.write({'is_new_product': False})
    
    # Funcion para enviar la notificacion de la creacion del nuevo producto
    def _send_new_product_notification(self):
        email_to = self.env['ir.config_parameter'].sudo().get_param('notifications_products.notification_email')
        if not email_to:
            return

        product_name = self.name or ''
        sku = self.default_code or 'No asignado'
        barcode = self.barcode or 'N/A'
        user_name = self.created_by_user_id.name if self.created_by_user_id else 'Usuario'

        body_html = f"""
        <div style="margin: 0px; padding: 15px; font-family: Arial, sans-serif; background-color: #f9f9f9;">
            <p>Hola, el Usuario <strong>{user_name}</strong>, ha creado un nuevo producto.</p>
            <p>Los datos del producto son los siguientes:</p>
            <table style="width: 100%; border-collapse: collapse; margin-top: 10px; border: 1px solid #ddd;">
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Nombre:</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{product_name}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>SKU / Ref:</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{sku}</td>
                </tr>
                <tr style="background-color: #f5f5f5;">
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>Código Barras:</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{barcode}</td>
                </tr>
                <tr>
                    <td style="padding: 8px; border: 1px solid #ddd;"><strong>ID Producto:</strong></td>
                    <td style="padding: 8px; border: 1px solid #ddd;">{self.id}</td>
                </tr>
            </table>
        </div>
        """

        mail_values = {
            'subject': f'Nuevo Producto Creado: {product_name}',
            'email_to': email_to,
            'body_html': body_html,
            'email_from': self.company_id.email_formatted if self.company_id else self.env.user.email,
        }

        if self.created_by_user_id and self.created_by_user_id.email:
            mail_values['email_cc'] = self.created_by_user_id.email

        mail = self.env['mail.mail'].sudo().create(mail_values)
        mail.send()
