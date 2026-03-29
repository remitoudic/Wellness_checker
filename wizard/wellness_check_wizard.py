from odoo import models, fields, api

class WellnessCheckWizard(models.Model):
    """ 
    Daily Wellness Pulse Check Wizard.
    
    This transient model provides the user interface for the daily popup.
    It dynamically pulls active questions from the wellness.question model 
    and presents them to the employee.
    
    Data Privacy: After the survey is submitted, the logic creates a 
    disconnected 'wellness.check' record to ensure anonymity.
    """
    _name = 'wellness.check.wizard'
    _description = 'Wellness Check Wizard'

    def _default_questions(self):
        """ Fetch the top 3 active questions sorted by sequence. """
        questions = self.env['wellness.question'].search([('active', '=', True)], limit=3, order='sequence, id')
        return questions

    # Labels generated dynamically from the wellness.question configuration
    q1_label = fields.Char(compute='_compute_questions')
    q2_label = fields.Char(compute='_compute_questions')
    q3_label = fields.Char(compute='_compute_questions')

    mood_score = fields.Integer(
        string='On a scale of 1 to 10, how are you feeling today?', 
        default=5,
        help="Main numerical sentiment metric (1-10)."
    )
    
    q1_answer = fields.Text(string='Answer 1')
    q2_answer = fields.Text(string='Answer 2')
    q3_answer = fields.Text(string='Answer 3')

    @api.depends()
    def _compute_questions(self):
        """ Maps active question text to the wizard labels. """
        questions = self._default_questions()
        self.q1_label = questions[0].name if len(questions) > 0 else 'How are you today?'
        self.q2_label = questions[1].name if len(questions) > 1 else 'What was the highlight of your day?'
        self.q3_label = questions[2].name if len(questions) > 2 else 'Any suggestions for morale improvement?'

    def action_submit(self):
        """ 
        Submits the survey and ensures anonymity.
        1. Creates a disconnected wellness.check record.
        2. Marks the user's login date to prevent multiple prompts today.
        """
        self.env['wellness.check'].create({
            'q1_answer': self.q1_answer,
            'q2_answer': self.q2_answer,
            'q3_answer': self.q3_answer,
            'mood_score': self.mood_score or 5,
        })
        # Record completion to stop daily popups
        self.env.user.last_wellness_check_date = fields.Date.context_today(self)
        return {'type': 'ir.actions.act_window_close'}

    def action_skip(self):
        """ 
        Dismisses the survey for the current day. 
        Marks the day as 'checked' but does not create a sentiment record.
        """
        self.env.user.last_wellness_check_date = fields.Date.context_today(self)
        return {'type': 'ir.actions.act_window_close'}
