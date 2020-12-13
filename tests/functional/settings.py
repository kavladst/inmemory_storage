from decouple import config

CLIENT_HOST: str = config('CLIENT_HOST', default='0.0.0.0')
CLIENT_PORT: str = config('CLIENT_PORT', default='8080')
