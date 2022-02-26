import psycopg2
import psycopg2.extras as extras
from datetime import datetime
from contextlib import contextmanager

import os
from dotenv import load_dotenv

load_dotenv(".env")

port = os.environ.get("postgresql_port",None)
password = os.environ.get("postgresql_password",None)

creds = dict(
	host = "localhost",
	dbname = "connect_db",
	user = "postgres",
	password = password,
	port = port
)


@contextmanager
def connect():
	conn = None
	ended = False
	try:
		with psycopg2.connect(**creds) as conn: #need this
			with conn.cursor(cursor_factory=extras.DictCursor) as cur:
				print(f"Successfully connected to PostgreSQL server at {datetime.now()}.")
				yield conn, cur

	except Exception as e:
		print("Error:",e)
		if conn is not None:
			ended = conn.close()
			#print("Closed connection in except block")
		else:
			ended = True
	#print("Connection is",conn,"at end of function")
	#print(cur)



