from odoo import models, fields, api

class ResUsers(models.Model):
    _inherit = 'res.users'

    last_wellness_check_date = fields.Date(string='Last Wellness Check Date')

    @api.model
    def check_wellness_prompt(self):
        # Only for human users in the backend
        if self.env.user.id == self.env.ref('base.public_user').id:
            return False
            
        today = fields.Date.context_today(self)
        if not self.env.user.last_wellness_check_date or self.env.user.last_wellness_check_date < today:
            return True
        return False
