from .entity import CampfireEntity

class User(CampfireEntity):
    """ Campfire user """
    
    def __init__(self, campfire, id, user_data=None, current=False):
        """ Initialize.

        Args:
            campfire (:class:`Campfire`): Campfire instance
            id (str): User ID

        Kwargs:
            current (bool): Wether user is current user, or not
        """
        super(User, self).__init__(campfire)
        if user_data:
            self.set_data(user_data)
        else:
            self.set_data(campfire.call_api("get", "users/{}".format(id)).json["user"])
        
        self.current = current
