from apiflask import APIFlask
from pkg.setting import setting


class Aurora(APIFlask):
    """A custom APIFlask app for Aurora"""
    def __init__(self, *args, **kwargs):
        super(Aurora, self).__init__(__name__, *args, **kwargs)
        self.version = setting.VERSION
        self.title = setting.SERVER_NAME


