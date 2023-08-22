import sys
import logging  # type: ignore
from autologging import logged, traced, TRACE  # type: ignore
from flask import Flask
from flask_restful import Resource, Api
from api.table_data import *
from api.users import *
from api.report_data import *
from api.status_check import *
from api.check_report import *
from prometheus_client import start_http_server, Summary, Counter
from flask_cors import CORS

logging.basicConfig(level=TRACE, stream=sys.stdout,
                    format="%(levelname)s:%(name)s:%(funcName)s:%(message)s")

app = Flask(__name__) #create Flask instance

api = Api(app) #api router
CORS(app)

#test url
#http://127.0.0.1:5000/user_data?check_id=000000000000001&emp_id=aa3ac2cd-3da8-477c-800c-3b054d9fea35

api.add_resource(StatusCheck, '/')
api.add_resource(UserCount, '/users')
api.add_resource(table_data, '/table_data')
api.add_resource(report_data, '/report_data')
api.add_resource(check_report, '/check_report')

if __name__ == '__main__':
    print("Starting flask")
    #start_http_server(8005) #prometheus

    app.run(debug=False), #starts Flask locally
    #app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3306))) #prod 
