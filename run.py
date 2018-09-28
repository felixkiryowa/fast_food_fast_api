"""
This Module runs flask application
"""
# from instance import APP
# from api.instance import APP


# from instance.views import GetApiUrls

# from update_status_of_a_specific_order.instance.views import GetApiUrls
import flask
from api.app.views import GetApiUrls


APP = flask.Flask(__name__)

APP.env = 'development'

APP.testing = True

GetApiUrls.get_all_urls(APP)


if __name__ == '__main__':
    APP.run(debug=True,port=9999)
