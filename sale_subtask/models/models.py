from odoo import api, fields, models, SUPERUSER_ID, _

class SaleOrderLineSubtask(models.Model):
    _name = "sale.order.line.subtask"
    name = fields.Char(string='Tarea')
    line_id = fields.Many2one('sale.order.line',string="Linea")

class SaleOrderLineTask(models.Model):
    _name = "sale.order.line"
    subtask_ids = fields.One2many('sale.order.line.subtask', 'line_id', string='Sub Tareas')

    def button_task(self):
        return {
            'name': 'Sale Subtask',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': 'sale_order_line_wizard_form',
            'res_model': 'sale.order.line.wizard',
            'domain': [],
            'type': 'ir.actions.act_window',
            'target': 'new',
        }

class SaleOrderLineTaskWizardTree(models.TransientModel):
    _name = "sale.order.line.wizard.tree"
    name = fields.Char(string='Tarea')
    wizard_id = fields.Many2one('sale.order.line.wizard', string='Tarea de linea de venta')

class SaleOrderLineTaskWizard(models.TransientModel):
    _name = "sale.order.line.wizard"
    
    sale_id = fields.Many2one('sale.order.line', string='Linea de Venta')
    subtask_ids = fields.One2many('sale.order.line.subtask', 'wizard_id', string='Sub Tareas')
