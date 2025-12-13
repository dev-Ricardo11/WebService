import unittest
from unittest.mock import MagicMock, patch
from database import DatabaseManager
import app

class TestDatabaseManager(unittest.TestCase):
    @patch('database.psycopg2.pool.SimpleConnectionPool')
    def setUp(self, mock_pool):
        # Mock the connection pool and connection
        self.mock_pool_instance = MagicMock()
        mock_pool.return_value = self.mock_pool_instance
        self.mock_conn = MagicMock()
        self.mock_pool_instance.getconn.return_value = self.mock_conn
        self.mock_cursor = MagicMock()
        self.mock_conn.cursor.return_value = self.mock_cursor
        
        self.db_manager = DatabaseManager()

    def test_save_credit_limit_request(self):
        # Setup mock return
        self.mock_cursor.fetchone.return_value = [123] # Mock returned ID

        data = {
            'CodeClientBackOffice': 'C001',
            'CodeClientOBT': 'OBT001',
            'Name': 'Test Client',
            'locValidacion': 'LOC1',
            'value': 1000.0,
            'Currency': 'USD',
            'product': 'Prod1',
            'description': 'Test Desc',
            'paymentType': 'Cash',
            'mailUser': 'test@example.com'
        }

        result_id = self.db_manager.save_credit_limit_request(data)
        
        self.assertEqual(result_id, 123)
        self.assertTrue(self.mock_cursor.execute.called)
        # Verify commit was called
        self.assertTrue(self.mock_conn.commit.called)

    def test_get_client_requests(self):
        # Setup mock return for select
        mock_rows = [
            {'id_credit_limit_rq': 1, 'value': 500, 'status': 'PENDING', 'currency': 'USD'},
            {'id_credit_limit_rq': 2, 'value': 100, 'status': 'APPROVED', 'currency': 'USD'}
        ]
        self.mock_cursor.fetchall.return_value = mock_rows

        requests = self.db_manager.get_client_requests('C001')
        
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]['value'], 500)

class TestAppLogic(unittest.TestCase):
    def test_validate_credit_limit_logic(self):
        # Test logic without DB calls first
        from app import validate_credit_limit_logic
        
        # Mock the db_manager used in app.py
        with patch('app.db_manager') as mock_db_manager:
            # Case 1: Limit not exceeded
            mock_db_manager.get_client_requests.return_value = [] # No prior requests
            
            request_data = {
                'CodeClientBackOffice': 'C001',
                'value': 1000.0,
                'paymentType': 'Cash'
            }
            
            result = validate_credit_limit_logic(request_data)
            self.assertEqual(result['status'], 'OK')

            # Case 2: Limit exceeded
            # Imagine total pending is 999,000, adding 2000 makes 1,001,000 (> 1,000,000)
            mock_db_manager.get_client_requests.return_value = [
                {'value': 999000.0, 'status': 'PENDING'}
            ]
            
            request_data_exceed = {
                'CodeClientBackOffice': 'C001',
                'value': 2000.0,
                'paymentType': 'Cash'
            }
            
            result_exceed = validate_credit_limit_logic(request_data_exceed)
            self.assertEqual(result_exceed['status'], 'NO-OK')
            self.assertIn('limite de credito ha sido excedido', result_exceed['message'])

if __name__ == '__main__':
    unittest.main()
