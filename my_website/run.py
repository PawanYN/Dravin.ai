import os

from dotenv import load_dotenv

from app import create_app
from app.database import init_db

# Load environment variables from .env file
load_dotenv() # THIS MUST BE CALLED EARLY
# Accessing environment variables
app = create_app()
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

if app.config['SECRET_KEY'] is None:
    raise ValueError("No FLASK_SECRET_KEY set for Flask application. Please set it via environment variable or .env file.")

if __name__ == '__main__':
    init_db()  # Creates DB if it doesn’t exist
    app.run(debug=True)

