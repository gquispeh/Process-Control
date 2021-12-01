from odoo import api, fields, models, SUPERUSER_ID, _

class SaleOrderLineSubtask(models.Model):
    _name = "sale.order.line.subtask"
    name = fields.Char(string='Tarea')
    line_id = fields.Many2one('sale.order.line',string="Linea")

class SaleOrderLineTask(models.Model):
    _name = "sale.order.line"
    subtask_ids = fields.One2many('sale.order.line.subtask', 'line_id', string='Sub Tareas')

    def button_task(self):
        print('button task')

class SaleOrderLineTaskWizard(models.TransientModel):
    _name = "sale.order.line.wizard"
    
    sale_id = fields.Many2one('sale.order.line', string='Linea de Venta')
