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
            ('borrador', 'Borrador'),
            ('espera', 'En espera'),
            ('atendido', 'Atendido'),
            ('cancelado', 'Cancelado'),
        ],
        string='Estado',
        default='borrador',
        required=True,
        copy=False,
    )
    
    fecha = fields.Date(
        string='Fecha',
        default=fields.Date.context_today,
    )

    # --- Métodos de Acción para los Botones ---
    def action_espera(self):
        """Pasa la cita a En espera"""
        for record in self:
            record.estado = 'espera'

    def action_atendido(self):
        """Marca la cita como Atendido"""
        for record in self:
            record.estado = 'atendido'

    def action_cancelado(self):
        """Cancela la cita"""
        for record in self:
            record.estado = 'cancelado'

    def action_borrador(self):
        """Regresa la cita a Borrador"""
        for record in self:
            record.estado = 'borrador'

