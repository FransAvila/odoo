from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Campo para escribir los usuarios que se van a monitorear 
    monitored_user_setting = fields.Char(
        string="IDs de Usuarios", 
        config_parameter='notifications_products.monitored_user_ids'
                ) 
    
    # Campo para poner el correo donde se enviaran la notificacion de productos nuevos
    notification_email = fields.Char(
        string="Correo de Notificación",
        help="Dirección de correo donde se enviarán los avisos de nuevos productos",
        config_parameter='notifications_products.notification_email'
    )
    
    # Seleccion de los usuarios a monitorear
    monitored_user_ids = fields.Many2many(
        'res.users', 
        string="Usuarios a monitorear"
    )

    
    @api.model 
    # Cargar los usuarios que se seleccionen
    def get_values(self):
        res = super(ResConfigSettings,self).get_values()
        ids_str = self.env['ir.config_parameter'].sudo().get_param('notifications_products.monitored_user_ids', '')
        if ids_str:
            res.update(monitored_user_ids=[(6, 0, [int(i) for i in ids_str.split(',') if i])])
        return res
    # Guardar los usuarios seleccionados
    def set_values(self):
        super(ResConfigSettings,self).set_values()
        ids_str = ','.join(map(str, self.monitored_user_ids.ids))
        self.env['ir.config_parameter'].sudo().set_param('notifications_products.monitored_user_ids', ids_str)
