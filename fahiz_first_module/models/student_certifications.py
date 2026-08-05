from odoo import models,fields

class CertificationModel(models.Model):
    _name= "certification.one"
    _description = "this is certification model"

    name= fields.Char(string="Certification Name")