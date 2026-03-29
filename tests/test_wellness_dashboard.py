from odoo.tests.common import TransactionCase
from odoo import fields
from datetime import timedelta

class TestWellnessDashboard(TransactionCase):

    def setUp(self):
        super(TestWellnessDashboard, self).setUp()
        self.Dashboard = self.env['wellness.dashboard']
        self.Check = self.env['wellness.check']
        
        # Clear data to avoid conflicts with existing records
        self.Check.search([]).unlink()
        
        # Ensure the singleton exists (id=1)
        self.singleton = self.Dashboard.search([], limit=1)
        if not self.singleton:
            self.singleton = self.Dashboard.create({})

    def test_refresh_pulse_basic(self):
        """Test calculation of participation and mood avg for the current day."""
        today = fields.Date.today()
        
        # Create 3 checks for today
        self.Check.create({'mood_score': 10, 'sentiment': 'happy', 'date': today})
        self.Check.create({'mood_score': 5, 'sentiment': 'neutral', 'date': today})
        self.Check.create({'mood_score': 3, 'sentiment': 'sad', 'date': today})
        
        # Trigger refresh
        self.singleton._refresh_pulse()
        
        # 3 participants, avg mood: (10+5+3)/3 = 6.0
        # Happy: 33%, Neutral: 33%, Sad: 34% (due to integer rounding logic 100-33-33=34)
        self.assertEqual(self.singleton.participation_today, 3)
        self.assertEqual(self.singleton.avg_mood_today, 6.0)
        self.assertEqual(self.singleton.happy_percent, 33)
        self.assertEqual(self.singleton.neutral_percent, 33)
        self.assertEqual(self.singleton.sad_percent, 34)

    def test_refresh_pulse_fallback(self):
        """Test the fallback feature when today has no data."""
        yesterday = fields.Date.subtract(fields.Date.today(), days=1)
        
        # Create data only for yesterday
        self.Check.create({'mood_score': 10, 'sentiment': 'happy', 'date': yesterday})
        
        # Trigger refresh
        self.singleton._refresh_pulse()
        
        # Should pick yesterday's data
        self.assertEqual(self.singleton.participation_today, 1)
        self.assertEqual(self.singleton.avg_mood_today, 10.0)
        self.assertEqual(self.singleton.happy_percent, 100)

    def test_pulse_signs(self):
        """Verify the pulse sign logic based on sentiment dominancy."""
        # Dominant Happy: (+)
        self.Check.create({'mood_score': 10, 'sentiment': 'happy', 'date': fields.Date.today()})
        self.singleton._refresh_pulse()
        self.assertEqual(self.singleton.sign_today, '+')

        # Clear records
        self.Check.search([]).unlink()
        
        # Dominant Sad: (-)
        self.Check.create({'mood_score': 2, 'sentiment': 'sad', 'date': fields.Date.today()})
        self.singleton._refresh_pulse()
        self.assertEqual(self.singleton.sign_today, '-')
