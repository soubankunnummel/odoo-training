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



class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'

    commission_eligible = fields.Boolean(
        string="Commission Eligible",
        compute='_compute_commission_data',
        store=True,
    )
    commission_percentage = fields.Float(
        string="Commission %",
        compute='_compute_commission_data',
        store=True,
    )
    commission_amount = fields.Float(
        string="Commission Amount",
        compute='_compute_commission_data',
        store=True,
    )

    @api.depends('price_unit', 'order_id.user_id')
    def _compute_commission_data(self):
        for line in self:
            user = line.order_id.user_id
            if user and user.commission_eligible and line.price_unit > 500:
                line.commission_eligible = True
                line.commission_percentage = user.commission_percentage
                line.commission_amount = (line.price_unit * user.commission_percentage) / 100
            else:
                line.commission_eligible = False
                line.commission_percentage = 0.0
                line.commission_amount = 0.0
