# SAP HANA Cloud Database SQL Query Executor

A lightweight and secure Python tool for executing SELECT queries on SAP HANA Cloud databases. This tool is designed with security in mind and only allows SELECT queries to prevent any accidental data modifications.

## Author
Avinash Oguri

## Features

- ✅ Secure execution of SELECT queries only
- 🔒 Built-in protection against non-SELECT operations
- 📊 Clean and formatted table output
- 🚀 Simple and straightforward usage
- 🔍 Automatic row limit for large queries
- 📝 Comprehensive logging
- 🔌 Easy database connection management using environment variables

## Prerequisites

- Python 3.7 or higher
- SAP HANA Cloud database access
- Required Python packages:
  ```
  pip install hdbcli python-dotenv
  ```

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/avinashoguri/ai-connector-for-hana-cloud.git
   cd ai-connector-for-hana-cloud
   ```

2. Create a `.env` file in the project directory with your HANA Cloud credentials:
   ```
   HANA_HOST=your-hana-host.com
   HANA_PORT=443
   HANA_USER=your-username
   HANA_PASSWORD=your-password
   ```

## Usage

Run a query directly from command line:
```bash
python execute_sql_query_hana_cloud_database.py "SELECT * FROM MY_TABLE"
```

## Example Output

```
=====================================
ID    | NAME  | EMAIL
-------------------------------------
1     | John  | john@example.com
2     | Alice | alice@example.com
=====================================
Total rows: 2
```

## Security Features

- Restricts execution to SELECT queries only
- Automatically adds row limits to prevent memory issues
- Secure credential management through environment variables
- No interactive mode to prevent arbitrary query execution
- Basic query validation before execution

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For bugs, questions, and discussions, please use the [GitHub Issues](https://github.com/avinashoguri/ai-connector-for-hana-cloud/issues).

## Disclaimer

This tool is provided "as is" without warranty of any kind. Always test queries in a safe environment before running them on production databases.
