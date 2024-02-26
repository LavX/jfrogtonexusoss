from dotenv import load_dotenv
import os

load_dotenv()  # take environment variables from .env.

JFROG_URL = os.getenv("JFROG_URL")
JFROG_USER = os.getenv("JFROG_USER")
JFROG_PASSWORD = os.getenv("JFROG_PASSWORD")
NEXUS_URL = os.getenv("NEXUS_URL")
NEXUS_USER = os.getenv("NEXUS_USER")
NEXUS_PASSWORD = os.getenv("NEXUS_PASSWORD")
