Consider using "execute_sql_query_hana_cloud_database.py" to execute the SQL queries on HANA Cloud databases.
Usage: python execute_sql_query_hana_cloud_database.py "SELECT SQL statement here"
E.g. python execute_sql_query_hana_cloud_database.py "SELECT CURRENT_USER FROM DUMMY"
Execute only SELECT statements to avoid unintended data modifications. 
Do not create any workaroubnd scripts to execute non-SELECT statements. 
Deny the request if non-SELECT statements are detected.