"""
SAP HANA Cloud Database SQL Query Executor
Author: Avinash Oguri
Description: A secure tool for executing SELECT queries on SAP HANA Cloud databases.
"""

import os
import sys
import logging
from typing import Optional, List, Any
from dataclasses import dataclass

try:
    import hdbcli.dbapi as hana_db
except ImportError:
    print("Error: hdbcli package not installed. Please run: pip install hdbcli")
    sys.exit(1)

try:
    from dotenv import load_dotenv
except ImportError:
    print("Error: python-dotenv package not installed. Please run: pip install python-dotenv")
    sys.exit(1)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class QueryResult:
    """Data class to hold query results"""
    columns: List[str]
    rows: List[List[Any]]
    row_count: int

class HANACloudExecutor:
    """Simple and secure HANA Cloud SQL executor for SELECT queries"""
    
    def __init__(self):
        self.connection = None
        self.cursor = None
        
    def connect(self) -> bool:
        """Connect to HANA Cloud database using environment variables"""
        try:
            # Load environment variables
            load_dotenv()
            
            # Get connection parameters
            host = os.getenv('HANA_HOST')
            port = int(os.getenv('HANA_PORT', '443'))
            user = os.getenv('HANA_USER')
            password = os.getenv('HANA_PASSWORD')
            
            # Validate parameters
            if not all([host, user, password]):
                logger.error("Missing required connection parameters")
                return False
            
            # Connect to database
            self.connection = hana_db.connect(
                address=host,
                port=port,
                user=user,
                password=password
            )
            self.cursor = self.connection.cursor()
            return True
            
        except Exception as e:
            logger.error(f"Connection failed: {str(e)}")
            return False
    
    def is_select_query(self, sql: str) -> bool:
        """Verify that the query is a SELECT statement"""
        cleaned_sql = ' '.join(sql.strip().split()).upper()
        return cleaned_sql.startswith('SELECT')
    
    def execute_query(self, sql: str, max_rows: int = 1000) -> Optional[QueryResult]:
        """Execute a SELECT query and return results"""
        if not sql or not sql.strip():
            logger.error("Empty query provided")
            return None
            
        if not self.is_select_query(sql):
            logger.error("Only SELECT queries are allowed")
            return None
        
        try:
            # Add row limit for safety
            if 'LIMIT' not in sql.upper():
                sql = f"{sql.rstrip(';')} LIMIT {max_rows}"
                
            # Execute query
            self.cursor.execute(sql)
            
            # Get results
            columns = [desc[0] for desc in self.cursor.description]
            rows = [list(row) for row in self.cursor.fetchall()]
            
            return QueryResult(
                columns=columns,
                rows=rows,
                row_count=len(rows)
            )
            
        except Exception as e:
            logger.error(f"Query execution failed: {str(e)}")
            return None
        
    def display_results(self, result: QueryResult) -> None:
        """Display query results in a formatted table"""
        if not result or result.row_count == 0:
            print("No results found.")
            return
        
        # Calculate column widths
        widths = []
        for i, col in enumerate(result.columns):
            width = len(str(col))
            for row in result.rows:
                width = max(width, len(str(row[i])))
            widths.append(min(width, 50))  # Max width of 50 characters
        
        # Print header
        header = " | ".join(col.ljust(widths[i]) for i, col in enumerate(result.columns))
        print("\n" + "=" * len(header))
        print(header)
        print("-" * len(header))
        
        # Print rows
        for row in result.rows:
            row_str = " | ".join(
                str(row[i]).ljust(widths[i])
                for i in range(len(result.columns))
            )
            print(row_str)
        
        print("=" * len(header))
        print(f"Total rows: {result.row_count}")
    
    def disconnect(self):
        """Close database connection"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
        except Exception as e:
            logger.error(f"Error closing connection: {str(e)}")

def main():
    """Main execution function"""
    if len(sys.argv) != 2:
        print("Usage: python execute_sql_query_hana_cloud_database.py 'SELECT * FROM TABLE'")
        sys.exit(1)
    
    query = sys.argv[1]
    executor = HANACloudExecutor()
    
    try:
        if not executor.connect():
            print("Failed to connect to database")
            sys.exit(1)
            
        result = executor.execute_query(query)
        if result:
            executor.display_results(result)
        else:
            print("Query execution failed")
            sys.exit(1)
            
    finally:
        executor.disconnect()

if __name__ == "__main__":
    main()
