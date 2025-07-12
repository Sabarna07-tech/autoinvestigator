import sqlite3
import os

class TickerManager:
    """
    A class to manage a SQLite database of company names, tickers, and CIKs.
    """
    def __init__(self):
        self.db_file = "server/resources/knowledge_base/ticker.db"
        self.conn = sqlite3.connect(self.db_file)
        self.cursor = self.conn.cursor()
        self._create_table()

    def _create_table(self):
        """Creates the 'tickers' table with a new 'cik_number' column."""
        try:
            # MODIFIED: Added cik_number column
            query = """
            CREATE TABLE IF NOT EXISTS tickers (
                company_name TEXT PRIMARY KEY,
                ticker_name TEXT NOT NULL,
                cik_number TEXT NOT NULL
            );
            """
            self.cursor.execute(query)
            self.conn.commit()
        except sqlite3.Error as e:
            print(f"Database error: {e}")

    def upload_data(self, company_name, ticker_name, cik_number):
        """
        Uploads a new company with its ticker and CIK to the database.
        MODIFIED: Accepts and inserts cik_number.
        """
        try:
            query = "INSERT OR IGNORE INTO tickers (company_name, ticker_name, cik_number) VALUES (?, ?, ?)"
            # MODIFIED: Pass cik_number to the query
            self.cursor.execute(query, (company_name.lower(), ticker_name, str(cik_number)))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Failed to upload data for {company_name}: {e}")
            return False

    def get_company_info(self, company_name):
        """
        Retrieves the ticker and CIK for a given company name.
        MODIFIED: Returns a dictionary with both ticker and CIK, or None if not found.
        """
        try:
            query = "SELECT ticker_name, cik_number FROM tickers WHERE company_name = ?"
            self.cursor.execute(query, (company_name.lower(),))
            result = self.cursor.fetchone()
            if result:
                return {"ticker": result[0], "cik": result[1]}
            return None
        except sqlite3.Error as e:
            print(f"Failed to retrieve data: {e}")
            return None

    def update_ticker(self, company_name, new_ticker_name):
        """Updates the ticker for an existing company."""
        try:
            query = "UPDATE tickers SET ticker_name = ? WHERE company_name = ?"
            self.cursor.execute(query, (new_ticker_name, company_name.lower()))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Failed to update ticker: {e}")
            return False

    def close(self):
        if self.conn:
            self.conn.close()

