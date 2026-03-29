from odoo import models, fields, api
import datetime

class WellnessCheck(models.Model):
    _name = 'wellness.check'
    _description = 'Anonymous Wellness Check-in'
    _order = 'date desc'

    date = fields.Date(string='Date', default=fields.Date.context_today, readonly=True)
    q1_answer = fields.Text(string='Answer 1')
    q2_answer = fields.Text(string='Answer 2')
    q3_answer = fields.Text(string='Answer 3')
    
    # Sentiment & Analysis
    mood_score = fields.Integer(string='Mood Score (1-10)', default=5)
    sentiment = fields.Selection([
        ('happy', 'Happy'),
        ('neutral', 'Neutral'),
        ('sad', 'Sad')
    ], string='Sentiment', compute='_compute_sentiment', store=True)
    analysis = fields.Text(string='Automated Analysis', compute='_compute_sentiment', store=True)

    @api.depends('q1_answer', 'q2_answer', 'q3_answer', 'mood_score')
    def _compute_sentiment(self):
        # Keyword dictionaries
        positive_keywords = ['happy', 'great', 'good', 'excellent', 'love', 'nice', 'smooth', 'efficient', 'motivated', 'well', 'fine', 'thanks', 'cool', 'perfect', 'awesome', 'excited', 'progress', 'team', 'help', 'happy']
        negative_keywords = ['sad', 'bad', 'poor', 'stress', 'tired', 'burnt', 'hard', 'difficult', 'noise', 'annoying', 'busy', 'pressure', 'broken', 'wait', 'slow', 'boring', 'angry', 'unhappy', 'lonely', 'stressful', 'exhausted']

        for record in self:
            text = f"{(record.q1_answer or '')} {(record.q2_answer or '')} {(record.q3_answer or '')}".lower()
            
            # Simple scoring
            pos_count = sum(1 for word in positive_keywords if word in text)
            neg_count = sum(1 for word in negative_keywords if word in text)
            
            score = pos_count - neg_count
            
            # Combine with mood score
            if record.mood_score >= 8 or (score > 1 and record.mood_score >= 6):
                record.sentiment = 'happy'
            elif record.mood_score <= 4 or (score < -1 and record.mood_score <= 5):
                record.sentiment = 'sad'
            else:
                record.sentiment = 'neutral'
                
            # Generate Analysis Text
            summary = ""
            if record.sentiment == 'happy':
                summary = "Employee seems to be in good spirits. "
                if pos_count > 0:
                    summary += f"Positive keywords detected ({pos_count})."
            elif record.sentiment == 'sad':
                summary = "Employee feedback shows lower morale. "
                if neg_count > 0:
                    summary += f"Negative keywords detected ({neg_count})."
            else:
                summary = "Employee has a neutral sentiment."
            
            record.analysis = summary
