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
    metodo_pago = fields.Selection(
        selection=[
            ('efectivo', 'Efectivo'),
            ('tarjeta', 'Tarjeta'),
            ('transferencia', 'Transferencia'),
        ],
        string='Método de Pago',
        readonly=True,
    )
    propina = fields.Float(
        string='Propina',
        readonly=True,
        default=0.0,
    )

    def action_abrir_cobro_wizard(self):
        """Abre la ventana flotante (Wizard) para cobrar"""
        return {
            'name': 'Cobrar Turno',
            'type': 'ir.actions.act_window',
            'res_model': 'cobrar.turno.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_cita_id': self.id},
        }
    
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

class ResPartner(models.Model):
    _inherit = 'res.partner'

    barberia_citas_ids = fields.One2many(
        comodel_name='mi.barberia',
        inverse_name='cliente_id',
        string='Citas de Barbería',
    )
    citas_count = fields.Integer(
        string='Nº de Citas',
        compute='_compute_citas_count',
    )

    def _compute_citas_count(self):
        """Cuenta cuántas citas tiene este cliente en la barbería"""
        for partner in self:
            partner.citas_count = len(partner.barberia_citas_ids)

    def action_view_citas_barberia(self):
        """Abre la pantalla con las citas filtradas solo de este cliente"""
        return {
            'name': 'Citas de Barbería',
            'type': 'ir.actions.act_window',
            'res_model': 'mi.barberia',
            'view_mode': 'kanban,calendar,list,form',
            'domain': [('cliente_id', '=', self.id)],
            'context': {'default_cliente_id': self.id},
        }
        
class CobrarTurnoWizard(models.TransientModel):
    _name = 'cobrar.turno.wizard'
    _description = 'Asistente para Cobrar Cita'

    cita_id = fields.Many2one(
        comodel_name='mi.barberia',
        string='Cita',
        required=True,
    )
    metodo_pago = fields.Selection(
        selection=[
            ('efectivo', 'Efectivo'),
            ('tarjeta', 'Tarjeta'),
            ('transferencia', 'Transferencia'),
        ],
        string='Método de Pago',
        default='efectivo',
        required=True,
    )
    precio = fields.Float(
        related='cita_id.precio',
        string='Precio del Servicio',
        readonly=True,
    )
    propina = fields.Float(
        string='Propina Voluntaria',
        default=0.0,
    )
    total_cobrar = fields.Float(
        string='Total a Cobrar',
        compute='_compute_total_cobrar',
    )

    @api.depends('precio', 'propina')
    def _compute_total_cobrar(self):
        for wizard in self:
            wizard.total_cobrar = wizard.precio + wizard.propina

    def action_confirmar_pago(self):
        """Guarda el cobro en la cita y la marca como Atendida"""
        for wizard in self:
            wizard.cita_id.write({
                'estado': 'atendido',
                'metodo_pago': wizard.metodo_pago,
                'propina': wizard.propina,
            })
        return {'type': 'ir.actions.act_window_close'}