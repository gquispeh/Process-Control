from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import AccessError, UserError, ValidationError
import logging
_logger = logging.getLogger("info")

class SaleOrderLineSubtask(models.Model):
    _name = "sale.order.line.subtask"
    name = fields.Char(string='Tarea')
    line_id = fields.Many2one('sale.order.line',string="Linea")
    state = fields.Selection([
        ('0', 'borrador'),
        ('1', 'activo')]
    , string='Estado'
    ,default='0')

class SaleOrderLineTask(models.Model):
    _inherit = "sale.order.line"
    subtask_ids = fields.One2many('sale.order.line.subtask', 'line_id', string='Sub Tareas')
    
    def button_task(self):
        product_type = self.product_id.type
        if product_type == 'service':
            return {
                    "type": "ir.actions.act_window",
                    'target': 'new',
                    'res_model': 'sale.order.line.wizard',
                    "view_id": self.env.ref('sale_subtask.sale_order_line_wizard_form').id,
                    'view_mode': 'form',
                    'name': u'Sub Tareas',
                    "context": {"default_line_id": self.id,
                                "search_default_line_id": self.id},
                }
        else:
            raise UserError(_('Este producto no es un servicio'))

class SaleOrderLineTaskWizard(models.TransientModel):
    _name = "sale.order.line.wizard"
    line_id = fields.Many2one('sale.order.line',
                            readonly=True,
                            string='Linea de Venta')
    subtask_ids = fields.Many2many('sale.order.line.subtask',
                                    readonly=False,
                                    string='Sub Tareas')
    
    @api.onchange('line_id')
    def compute_sutask_lines(self):
        lines = self.env['sale.order.line.subtask'].search([('line_id', '=', self.line_id.id)]).ids
        self.write({'subtask_ids': [(6, 0, lines)]})

    def added(self):
        subtask = self.subtask_ids.ids
        for line in self.subtask_ids:
            line.write({'line_id': self.line_id.id})
        self.line_id.write({'subtask_ids': [(6, 0, subtask)]})