import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add project root to sys.path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from crew import WeekendPlanner
from main import run_weekend

class TestWeekendCrew(unittest.TestCase):

    def setUp(self):
        # Ensure environment variables are set if needed, or mock them
        pass

    def test_weekend_planner_initialization(self):
        """Test that WeekendPlanner can be instantiated and has the expected agents/tasks methods."""
        planner = WeekendPlanner()
        
        # Check if agent methods exist
        self.assertTrue(hasattr(planner, 'weather_specialist'))
        self.assertTrue(hasattr(planner, 'calendar_analyst'))
        self.assertTrue(hasattr(planner, 'local_scout'))
        self.assertTrue(hasattr(planner, 'recommendation_curator'))
        self.assertTrue(hasattr(planner, 'transport_planner'))
        self.assertTrue(hasattr(planner, 'calendar_scheduler'))
        self.assertTrue(hasattr(planner, 'itinerary_designer'))

        # Check if task methods exist
        self.assertTrue(hasattr(planner, 'fetch_weather'))
        self.assertTrue(hasattr(planner, 'analyze_calendar'))
        self.assertTrue(hasattr(planner, 'explore_local_options'))
        self.assertTrue(hasattr(planner, 'craft_recommendations'))
        self.assertTrue(hasattr(planner, 'plan_transport'))
        self.assertTrue(hasattr(planner, 'schedule_calendar_entry'))
        self.assertTrue(hasattr(planner, 'build_itinerary'))

    @patch('crew.WeekendPlanner.crew')
    def test_run_weekend_execution(self, mock_crew_method):
        """Test the run_weekend function with mocked crew execution."""
        
        # Setup the mock
        mock_crew_instance = MagicMock()
        mock_crew_method.return_value = mock_crew_instance
        
        mock_result = MagicMock()
        mock_result.raw = "Mocked Result"
        mock_crew_instance.kickoff.return_value = mock_result

        # Test inputs
        location = "横浜"
        interests = "中華街"
        budget = "1万円"
        companions = "家族"
        weather = "晴れ"

        # Execute
        run_weekend(location, interests, budget, companions, weather)

        # Verify kickoff was called with correct inputs
        # Note: run_weekend adds current_date, so we check if inputs contains our keys
        args, kwargs = mock_crew_instance.kickoff.call_args
        inputs = kwargs.get('inputs')
        
        self.assertIsNotNone(inputs)
        self.assertEqual(inputs['location'], location)
        self.assertEqual(inputs['interests'], interests)
        self.assertEqual(inputs['budget'], budget)
        self.assertEqual(inputs['companions'], companions)
        self.assertEqual(inputs['weather'], weather)
        self.assertIn('current_date', inputs)

if __name__ == '__main__':
    unittest.main()
