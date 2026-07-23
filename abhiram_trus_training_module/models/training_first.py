from odoo import models, fields


class TrainingOne(models.Model):
    _name = 'training.one'
    _description = 'Training One'
    
    name = fields.Char(string="Name")