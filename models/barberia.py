from odoo import models, fields, api

class MiBarberia(models.Model):
    _name = 'mi.barberia'
    _description = 'Gestión del Cliente'
    _rec_name = 'cliente_id'
    
    cliente_id = fields.Many2one(
        comodel_name='res.partner',
        string='Cliente',
        required=True,
        ondelete='restrict',
    )
    
    name = fields.Char(
        string='Nombre',
        related='cliente_id.name',
        store=True,
        readonly=True,
    )
    
    telefono = fields.Char(
        related='cliente_id.phone',
        string='Teléfono',
        readonly=True,
    )
    
    correo = fields.Char(
        related='cliente_id.email',
        string='Correo Electrónico',
        readonly=True,
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

