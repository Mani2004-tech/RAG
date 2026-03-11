import psycopg2
from psycopg2.extras import RealDictCursor

conn = psycopg2.connect(
    host="localhost",
    database="rag_index",
    user="postgres",
    password="slk@SOFT123",
    cursor_factory=RealDictCursor
)

def get_cursor():
    return conn.cursor()