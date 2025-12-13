import os
import psycopg2
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        try:
            self.connection_pool = psycopg2.pool.SimpleConnectionPool(
                1, 20,
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASS'),
                host=os.getenv('DB_HOST'),
                port=os.getenv('DB_PORT'),
                database=os.getenv('DB_NAME')
            )
            if self.connection_pool:
                print("Connection pool created successfully")
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error while connecting to PostgreSQL", error)
            raise error

    def get_connection(self):
        return self.connection_pool.getconn()

    def release_connection(self, conn):
        self.connection_pool.putconn(conn)

    def save_credit_limit_request(self, request_data: Dict) -> int:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                INSERT INTO credit_limit_rq (
                    code_client_backoffice, code_client_obt, name, loc_validacion,
                    value, currency, product, description, payment_type, mail_user, status
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'PENDING'
                ) RETURNING id_credit_limit_rq;
            """
            
            values = (
                request_data.get('CodeClientBackOffice'),
                request_data.get('CodeClientOBT'),
                request_data.get('Name'),
                request_data.get('locValidacion'),
                request_data.get('value'),
                request_data.get('Currency'),
                request_data.get('product'),
                request_data.get('description'),
                request_data.get('paymentType'),
                request_data.get('mailUser')
            )
            
            cursor.execute(query, values)
            id_request = cursor.fetchone()[0]
            conn.commit()
            cursor.close()
            return id_request

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Database error saving request: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)

    def update_credit_limit_status(
        self,
        credit_limit_id: int,
        status: str,
        message: str
    ) -> None:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            query = """
                UPDATE credit_limit_rq 
                SET status = %s, message_validation = %s
                WHERE id_credit_limit_rq = %s
            """
            
            cursor.execute(query, (status, message, credit_limit_id))
            conn.commit()
            cursor.close()

        except Exception as e:
            if conn:
                conn.rollback()
            raise Exception(f"Database error updating status: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)

    def get_client_requests(self, code_client_backoffice: str) -> List[Dict]:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT id_credit_limit_rq, value, status, currency
                FROM credit_limit_rq
                WHERE code_client_backoffice = %s
            """
            
            cursor.execute(query, (code_client_backoffice,))
            rows = cursor.fetchall()
            cursor.close()
            
            # Convert RealDictRow to dict
            return [dict(row) for row in rows]

        except Exception as e:
            raise Exception(f"Database error getting client requests: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)

    def get_request_by_id(self, credit_limit_id: int) -> Optional[Dict]:
        conn = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor(cursor_factory=RealDictCursor)
            
            query = """
                SELECT *
                FROM credit_limit_rq
                WHERE id_credit_limit_rq = %s
            """
            
            cursor.execute(query, (credit_limit_id,))
            row = cursor.fetchone()
            cursor.close()
            
            return dict(row) if row else None

        except Exception as e:
            raise Exception(f"Database error getting request by ID: {str(e)}")
        finally:
            if conn:
                self.release_connection(conn)
