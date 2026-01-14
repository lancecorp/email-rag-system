from dotenv import load_dotenv
import os

class LoadEnvironment:

    load_dotenv()
    IMAP_SERVER = os.getenv("IMAP_SERVER")
    EMAIL_USER_NAME = os.getenv("EMAIL_USER_NAME")
    EMAIL_USER_PASSWORD = os.getenv("EMAIL_USER_PASSWORD")
    DOCKER_USER_NAME = os.getenv("DOCKER_USER_NAME")
    DOCKER_USER_PASSWORD = os.getenv("DOCKER_USER_PASSWORD")
    MODEL_NAME = os.getenv("MODEL_NAME")
    DOCKER_HOST = os.getenv("DOCKER_HOST")
    DOCKER_PORT = os.getenv("DOCKER_PORT")
