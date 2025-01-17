import sys
import os

# Add the project's root directory to the sys.path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Add the src directory to the path if needed
sys.path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), 'src'))

# Import the main function from the main.py (located outside the src directory)
from main import main  # Import the main function from main.py

# This function will be called when the server starts, and you may want to handle bot logic separately.
def application(environ, start_response):
    # Ensure the bot function gets executed when the server is started.
    main()  # Run the bot from the main.py
    
    start_response("200 OK", [("Content-Type", "text/plain")])
    return [b"Bot is running..."]
