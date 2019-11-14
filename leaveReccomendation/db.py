import psycopg2

# Update connection string information
host = "hike-a-thon-postgres.postgres.database.azure.com"
dbname = "postgres"
user = "aabccd021@hike-a-thon-postgres"
password = "aabccd3.14159265"
sslmode = "require"

# Construct connection string
conn_string = "host={0} user={1} dbname={2} password={3} sslmode={4}".format(host, user, dbname, password, sslmode)
conn = psycopg2.connect(conn_string) 
print("Connection established")

cursor = conn.cursor()

# Fetch all rows from table
cursor.execute("SELECT * FROM leave;")
rows = cursor.fetchall()

# Print all rows
    print("Data row = (%s, %s, %s)" %(str(row[0]), str(row[1]), str(row[2])))

# Cleanup
conn.commit()
cursor.close()
conn.close()