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
        self.ws_connection = websocket.create_connection(self.ws_link)

    def reconnect(self):
        """Recreate websocket object
        """
        self.ws_connection.close()
        self.ws_connection = websocket.create_connection(self.ws_link)
   
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

    def get_data(self):
        """Returns data recevied through websocket
        """
        signal.signal(signal.SIGALRM,self.timeout_handler)
        while True:
            signal.alarm(2)
            try:
                data = self.ws_connection.recv()
            except TimeoutException:
                self.reconnect()
            else:
                signal.alarm(0)
                content = self.get_fenstring(data)
                    if content:
                        return content

