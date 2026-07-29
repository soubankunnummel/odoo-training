from odoo import models,fields


class Studnet_class(models.Model):
    _name = "student.class"
    _discription = "Student Class"

    name = fields.Char(string="Name")


    
