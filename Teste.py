import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
DATABASE_URL = os.getenv("postgresql://postgres:EstoquePLUS@db.mgickjwfczdfxbnyflbr.supabase.co:5432/postgres")

# Connect to the database
connection = psycopg2.connect(DATABASE_URL)