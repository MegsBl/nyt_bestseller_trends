from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# API keys
NYT_BOOK_API = os.getenv("BOOKS_API")