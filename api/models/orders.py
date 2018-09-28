"""This is orders class defining the class constructor """

class Orders(object):
    """This is orders class"""

    def __init__(self,order_id, order_items, order_status, user_id):
        """This is orders class constructor"""
        self.order_id = order_id
        self.order_items = order_items
        self.order_status = order_status
        self.user_id = user_id
        
        
