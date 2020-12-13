from decouple import config

API_URL = config('API_URL', default='http://0.0.0.0:8000/')
