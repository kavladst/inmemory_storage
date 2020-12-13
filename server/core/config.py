from decouple import config

STORAGE_PATH = config('STORAGE_PATH', default='.')
