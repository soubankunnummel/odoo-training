from odoo import fields, models


class ResUsersInherit(models.Model):
    _inherit = 'res.users'

    student_rank = fields.Selection([
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ], string='Student Rank', default='beginner')