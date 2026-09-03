from odoo import models, fields, api


class SaleOrderInherit(models.Model):
    _inherit = 'sale.order'

    total_commission = fields.Float(
        string="Total Commission",
        compute='_compute_total_commission',
        store=True,
    )

    @api.depends('order_line.commission_amount')
    def _compute_total_commission(self):
        for order in self:
            order.total_commission = sum(order.order_line.mapped('commission_amount'))
