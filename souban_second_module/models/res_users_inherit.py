from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    student_rank = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], string='Student Rank', default='beginner')

    commission_eligible = fields.Boolean(string="Commission Eligible", default=False)
    commission_percentage = fields.Float(string="Commission %", default=0.0)

    @api.constrains('commission_eligible', 'commission_percentage')
    def _check_commission_percentage(self):
        for record in self:
            if record.commission_eligible and record.commission_percentage > 60:
                raise ValidationError("Commission percentage cannot exceed 60%!")
            if record.commission_percentage < 0:
                raise ValidationError("Commission percentage cannot be negative!")
            if record.commission_percentage > 100:
                raise ValidationError("Commission percentage cannot exceed 100%!")

    def write(self, vals):
        res = super().write(vals)
        if 'commission_eligible' in vals:
            group = self.env.ref('souban_second_module.group_commission_eligible')
            for user in self:
                if vals['commission_eligible']:
                    user.write({'group_ids': [(4, group.id)]})
                else:
                    user.write({'group_ids': [(3, group.id)]})
        return res
