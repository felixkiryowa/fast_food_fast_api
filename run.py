"""
This Module runs flask application
"""
from connection import APP
from api.app.views import OrderApiUrls




APP.env = 'development'

APP.testing = True

OrderApiUrls.get_all_urls(APP)

if __name__ == '__main__':
    APP.run(debug=True)
