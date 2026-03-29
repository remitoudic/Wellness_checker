from odoo import models, fields, api

class WellnessCheckWizard(models.TransientModel):
    _name = 'wellness.check.wizard'
    _description = 'Wellness Check Wizard'

    def _default_questions(self):
        questions = self.env['wellness.question'].search([('active', '=', True)], limit=3, order='sequence, id')
        return questions

    # We use functional fields to display the questions from the config
    q1_label = fields.Char(compute='_compute_questions')
    q2_label = fields.Char(compute='_compute_questions')
    q3_label = fields.Char(compute='_compute_questions')

    mood_score = fields.Integer(string='On a scale of 1 to 10, how are you feeling today?', default=5)
    q1_answer = fields.Text(string='Answer 1')
    q2_answer = fields.Text(string='Answer 2')
    q3_answer = fields.Text(string='Answer 3')

    @api.depends()
    def _compute_questions(self):
        questions = self._default_questions()
        self.q1_label = questions[0].name if len(questions) > 0 else 'How are you today?'
        self.q2_label = questions[1].name if len(questions) > 1 else 'What is the highlight of your day?'
        self.q3_label = questions[2].name if len(questions) > 2 else 'Any suggestions?'

    def action_submit(self):
        # Create anonymous check
        self.env['wellness.check'].create({
            'q1_answer': self.q1_answer,
            'q2_answer': self.q2_answer,
            'q3_answer': self.q3_answer,
            'mood_score': self.mood_score or 5,
        })
        # Update user record to mark as checked today
        self.env.user.last_wellness_check_date = fields.Date.context_today(self)
        return {'type': 'ir.actions.act_window_close'}

    def action_skip(self):
        # Just update user record to not show it again today
        self.env.user.last_wellness_check_date = fields.Date.context_today(self)
        return {'type': 'ir.actions.act_window_close'}
