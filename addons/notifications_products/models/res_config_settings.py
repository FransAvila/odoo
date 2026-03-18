from odoo import models, fields, api

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    # Usar el campo para escribir los usuarios a monitoriar
    monitored_user_setting = fields.Char(
        string="IDs de Usuarios", 
        config_parameter='notifications_products.monitored_user_ids'
                ) 
    
    # Campo para ingresar el correo donde se enviaran las notificaciones 
    notification_email = fields.Char(
        string="Correo de Notificación",
        help="Dirección de correo donde se enviarán los avisos de nuevos productos",
        config_parameter='notifications_products.notification_email'
    )
    
    # Interfaz para elegir los usuarios a monitorear
    monitored_user_ids = fields.Many2many(
        'res.users', 
        string="Usuarios a monitorear"
    )

    
    @api.model 
    # Cargar los usuarios seleccionados al abrir la configuración
    def get_values(self):
        res = super(ResConfigSettings,self).get_values()
        ids_str = self.env['ir.config_parameter'].sudo().get_param('notifications_products.monitored_user_ids', '')
        if ids_str:
            res.update(monitored_user_ids=[(6, 0, [int(i) for i in ids_str.split(',') if i])])
        return res
    # Guardar los usuarios seleccionados para guardar en la configuración
    def set_values(self):
        super(ResConfigSettings,self).set_values()
        # Convertir la lista de IDs a un string para guardar
        ids_str = ','.join(map(str, self.monitored_user_ids.ids))
        self.env['ir.config_parameter'].sudo().set_param('notifications_products.monitored_user_ids', ids_str)
