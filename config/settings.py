import os
from dotenv import load_dotenv

load_dotenv()


SECRET_KEY = os.getenv('SECRET_KEY')


EXCEPTION_ROUTES = ['/users/register', '/users/login']


# Database name
DATABASE_NAME = 'Project_1'

# Collections names
USER_COLLECTION = 'User'