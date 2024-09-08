import os

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings:
    def __init__(self):
        self.environment = os.getenv("ENVIRONMENT", "production")

        if self.environment == "test_db":
            self.database_url = os.getenv("DATABASE_URL_TEST_DB")
        elif self.environment == "test_api":
            self.database_url = os.getenv("DATABASE_URL_TEST_API")
        elif self.environment == "production":
            self.database_url = os.getenv("DATABASE_URL_PRODUCTION")
        else:
            raise ValueError(f"Invalid environment : {self.environment}" )

settings = Settings()