import signal
import websocket
import json

class TimeoutException(Exception):
    """Custom timeout exception class
    """
    pass

class Interface(object):
    """An interface to the websocket to extract currrent board state.
    """
    def __init__(self,ws_link):
        """Return an Interface object ---
        """
        self.ws_link = ws_link
        # TODO : Get ws link from game url
        self.ws_connection = websocket.create_connection(self.ws_link, origin="https://lichess.org")

    def timeout_handler(self,signum,frame):
        """Custom signal handler
        """
        raise TimeoutException

    def get_fenstring(self,content):
        """Returns only the fenstring
        """
        data = json.loads(content)
        if "d" in data:
            if "fen" in data['d']:
                return data['d']['fen']
            raise Exception
        raise Exception

    def get_turn(self, content):
        data = json.loads(content)
        if "d" in data:
            if "ply" in data['d']:
                return data['d']['ply'] % 2
            raise Exception
        raise Exception



    def get_data(self):
        """Returns data recevied through websocket
        """
        data = self.ws_connection.recv()
        self.ws_connection.send("null") 
        print(data)
        content = self.get_fenstring(data)
        isWhite = self.get_turn(data)
        return content, isWhite
