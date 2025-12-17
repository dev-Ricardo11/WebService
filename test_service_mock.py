import unittest
from unittest.mock import MagicMock, patch
import sys

# CRITICAL: Mock psycopg2 BEFORE importing app or database
# This prevents the real connection attempt when app.py runs `db_manager = DatabaseManager()`
mock_psycopg2 = MagicMock()
sys.modules['psycopg2'] = mock_psycopg2
sys.modules['psycopg2.pool'] = MagicMock()
sys.modules['psycopg2.extras'] = MagicMock()

# Now it is safe to import
from database import DatabaseManager
import app

class TestDatabaseManager(unittest.TestCase):
    def setUp(self):
        # We need to re-instantiate or mock internal components because the global import 
        # might have used a different mock instance if we are not careful.
        # But here we are testing the class directly.
        pass

    def test_save_credit_limit_request(self):
        # We need to mock the connection pool behavior explicitly for this test instance
        # Since we mocked the MODULE, DatabaseManager() will get the mock from sys.modules
        
        db_mgr = DatabaseManager()
        # The __init__ called psycopg2.pool.SimpleConnectionPool(...) which returned a MagicMock
        
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        # Setup the chain: pool.getconn() -> conn -> cursor() -> cursor
        db_mgr.connection_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_cursor.fetchone.return_value = [123] # Mock returned ID

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

        result_id = db_mgr.save_credit_limit_request(data)
        
        self.assertEqual(result_id, 123)
        self.assertTrue(mock_cursor.execute.called)
        self.assertTrue(mock_conn.commit.called)

    def test_get_client_requests(self):
        db_mgr = DatabaseManager()
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        
        db_mgr.connection_pool.getconn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        # Setup mock return for select
        mock_rows = [
            {'id_credit_limit_rq': 1, 'value': 500, 'status': 'PENDING', 'currency': 'USD'},
            {'id_credit_limit_rq': 2, 'value': 100, 'status': 'APPROVED', 'currency': 'USD'}
        ]
        mock_cursor.fetchall.return_value = mock_rows

        requests = db_mgr.get_client_requests('C001')
        
        self.assertEqual(len(requests), 2)
        self.assertEqual(requests[0]['value'], 500)

class TestAppLogic(unittest.TestCase):
    def setUp(self):
        # Logic uses the global 'app.db_manager'. We must mock it.
        self.mock_db = MagicMock()
        app.db_manager = self.mock_db
        
    def test_validate_credit_limit_logic(self):
        # Case 1: Limit not exceeded
        self.mock_db.get_client_requests.return_value = [] # No prior requests
        
        request_data = {
            'CodeClientBackOffice': 'C001',
            'value': 1000.0,
            'paymentType': 'Cash'
        }
        
        result = app.validate_credit_limit_logic(request_data)
        self.assertEqual(result['status'], 'OK')

        # Case 2: Limit exceeded
        self.mock_db.get_client_requests.return_value = [
            {'value': 999000.0, 'status': 'PENDING'}
        ]
        
        request_data_exceed = {
            'CodeClientBackOffice': 'C001',
            'value': 2000.0,
            'paymentType': 'Cash'
        }
        
        result_exceed = app.validate_credit_limit_logic(request_data_exceed)
        self.assertEqual(result_exceed['status'], 'NO-OK')
        self.assertIn('limite de credito ha sido excedido', result_exceed['message'])

if __name__ == '__main__':
    unittest.main()
