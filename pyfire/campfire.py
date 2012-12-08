import operator, urllib, requests

from .message import Message
from .user import User
from .room import Room

class RoomNotFoundException(Exception):
    pass
class UserNotFoundException(Exception):
    pass

class Campfire(object):
    """ Campfire API """
    
    def __init__(self, subdomain, username, password, ssl=False, currentUser=None):
        """ Initialize.

        Args:
            subdomain (str): Campfire subdomain
            username (str): User
            password (str): pasword

        Kwargs:
            ssl (bool): enabled status of SSL
            currentUser (:class:`User`): If specified, don't auto load current user, use this one instead
        """
        self.base_url = "http%s://%s.campfirenow.com" % ("s" if ssl else "", subdomain)
        self._settings = {
            "subdomain": subdomain,
            "username": username,
            "password": password,
            "ssl": ssl
        }
        self._user = currentUser
        self._users = {}
        self._rooms = {}

        if not self._user:
            user_request = requests.get("{}/users/me.json".format(self.base_url), auth=(username, password))
            if user_request.status_code == 200:
                user = user_request.json['user']

                self._user = User(self, user["id"], user_data=user, current=True)
                self._user.token = user["api_auth_token"]
            else:
                raise UserNotFoundException();

    def call_api(self, method, url, **kwargs):
        combined_url = "{}/{}.json".format(self.base_url, url)
        kwargs['auth'] = (self._user.token, "x",)

        return requests.request(method, combined_url, **kwargs)


    def __copy__(self):
        """ Clone.

        Returns:
            :class:`Campfire`. Cloned instance
        """
        return Campfire(
            self._settings["subdomain"],
            self._settings["username"],
            self._settings["password"],
            self._settings["ssl"],
            self._user
        )

    def get_rooms(self, sort=True):
        """ Get rooms list.

        Kwargs:
            sort (bool): If True, sort rooms by name

        Returns:
            array. List of rooms (each room is a dict)
        """
        response = self.call_api("get", "rooms")
        rooms = response.json["rooms"]

        if sort:
            rooms.sort(key=operator.itemgetter("name"))
        return rooms

    def get_room_by_name(self, name):
        """ Get a room by name.

        Returns:
            :class:`Room`. Room

        Raises:
            RoomNotFoundException
        """
        rooms = self.get_rooms()
        for room in rooms or []:
            if room["name"] == name:
                return self.get_room(room["id"])
        raise RoomNotFoundException("Room %s not found" % name)

    def get_room(self, id):
        """ Get room.

        Returns:
            :class:`Room`. Room
        """
        if id not in self._rooms:
            self._rooms[id] = Room(self, id)
        return self._rooms[id]

    def get_user(self, id = None):
        """ Get user.

        Returns:
            :class:`User`. User
        """
        if not id:
            id = self._user.id

        if id not in self._users:
            self._users[id] = self._user if id == self._user.id else User(self, id)

        return self._users[id]

    def search(self, terms):
        """ Search transcripts.

        Args:
            terms (str): Terms for search

        Returns:
            array. Messages
        """
        messages_response = self.call_api("get", "search/{}".format(urllib.quote_plus(terms)))
        messages = messages_response.json["messages"]

        if messages:
            messages = [Message(self, message) for message in messages]
        return messages

