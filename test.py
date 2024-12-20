import os

from dotenv import load_dotenv

print("hello world")
load_dotenv()
filename = os.getenv('LOG_FILE')
print(filename)