import os
from sqlmodel import create_engine
from dotenv import load_dotenv

load_dotenv()

# Get Neon DB URL from .env
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./test.db')

# Create engine with SSL mode for Neon
engine = create_engine(DATABASE_URL, echo=False, connect_args={'sslmode': 'require'} if 'neon' in DATABASE_URL else {})
