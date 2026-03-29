from odoo import models, fields

class WellnessQuestion(models.Model):
    _name = 'wellness.question'
    _description = 'Wellness Question'
    _order = 'sequence, id'

    name = fields.Char(string='Question', required=True)
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)
