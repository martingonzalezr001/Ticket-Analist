from dotenv import load_dotenv
import os

load_dotenv()

DEBUG = os.getenv("DEBUG", "False") == "True"
APP_NAME = os.getenv("APP_NAME", "TicketAnalyzer")
