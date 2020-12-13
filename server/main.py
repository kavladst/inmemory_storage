import atexit

from flask import Flask
from flask_restplus import Api
from apscheduler.schedulers.background import BackgroundScheduler

from api.authentification import api_authentification
from api.user_storage import api_user_storage, users_storage

app = Flask(__name__)
api = Api(app, title='In-memory Storage')
api.add_namespace(api_authentification)
api.add_namespace(api_user_storage)

if __name__ == '__main__':
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        func=users_storage.delete_if_ttl_is_gone,
        trigger="interval",
        seconds=1
    )
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    app.run(host='0.0.0.0', port=8000)
