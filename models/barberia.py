from odoo import models, fields, api, exceptions

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
    porcentaje_comision = fields.Float(
        string='% Comisión Barbero',
        default=40.0,
    )
    
    comision_barbero = fields.Float(
        string='Ganancia del Barbero',
        compute='_compute_comision',
        store=True,
    )

    @api.depends('precio', 'porcentaje_comision')
    def _compute_comision(self):
        """Calcula automáticamente la comisión del barbero"""
        for record in self:
            record.comision_barbero = record.precio * (record.porcentaje_comision / 100.0)
    
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
    notas = fields.Html(
        string='Notas y Preferencias',
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
            
    @api.constrains('precio')
    def _check_precio_positivo(self):
        """Impide guardar precios menores o iguales a cero"""
        for record in self:
            if record.precio <= 0:
                raise exceptions.ValidationError(
                    "¡El precio del corte debe ser mayor a 0 dólares!"
                )

