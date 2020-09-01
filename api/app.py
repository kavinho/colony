import os
from flask import Flask

from v1.api import api_v1
from database import init_db
from v1.models import Base
from storage import SQLStorage
import logging
logging.basicConfig(level=logging.INFO)

# flask boiler plate init code
app = Flask(__name__)

app.config['SECRET_KEY']=b'_5#y2L"F4Q8z\n\xec]/'
app.config.from_object(os.environ.get('APP_ENV_CONFIG'))

db_session = init_db(app, Base)
app.config['db_session'] = db_session
app.config['storage'] = SQLStorage(db_session)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

# register blueprints here
app.register_blueprint(api_v1, url_prefix='/v1')

#DEVELOPMENT TIME
if __name__=='__main__':
    print('Flask app running fro main ....')
    app.run(host="0.0.0.0", debug=True, port=5000)

"""
How to run the app
project/api  APP_ENV_CONFIG=configuration.TestConfig python -m unittest -v tests.test_models

"""
