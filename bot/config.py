import os

from dotenv import load_dotenv


load_dotenv()

ADMIN_TG_ID = os.getenv('ADMIN_TG_ID')
TOKEN = os.getenv('TOKEN')

LANGUAGE_LIST = ['python', 'go', 'rust']
