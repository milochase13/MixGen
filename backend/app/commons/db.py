import psycopg2

def create_db_connection():
    conn = psycopg2.connect(
        host="localhost",
        port="5432",
        user="your_username",
        password=os.environ['DB_USERNAME'],
        database=os.environ['DB_PASSWORD'],
    )
    return conn

def store_txn(conn, prompt, response):
    # Store result in PostgreSQL
    # cursor = conn.cursor()
    # cursor.execute("INSERT INTO results (response) VALUES (%s)", (response))
    # conn.commit()
    # cursor.close()
    return