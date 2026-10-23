from odoo import models, fields, api

class MiBarberia(models.Model):
    _name = 'mi.barberia'
    _description = 'Gestión del Cliente'
    
    name = fields.Char(
        string='Nombre del Cliente',
        required=True,
    )
    
    tipo_corte = fields.Selection(
        selection=[
            ('degradado', 'Degradado'),
            ('clasico', 'Clásico'),
            ('barba', 'Barba'),
            ('servicio_completo', 'Servicio Completo')
        ],
        string='Tipo de Corte',
    )
    
    precio = fields.Float(
        string='Precio',
    )
    
    estado = fields.Selection(
        selection=[
            ('espera', 'En espera'),
            ('atendido', 'Atendido')
        ],
        string= 'Estado',
        default='espera',
    )
    
    fecha = fields.Date(
        string= 'Fecha'
    )

