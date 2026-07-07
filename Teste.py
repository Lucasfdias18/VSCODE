import psycopg2
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
DATABASE_URL= "postgresql://postgres.mgickjwfczdfxbnyflbr:EstoquePLUS@aws-1-sa-east-1.pooler.supabase.com:5432/postgres"

# Connect to the database
connection = psycopg2.connect(DATABASE_URL)