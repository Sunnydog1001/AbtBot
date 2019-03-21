class DEX(object):
    def __init__(self):
        self._tokens = {}  # TokenName : TokenObject

    def sortby(self, attribute):
        return