class Singleton(object):
    def __init__(self, cls):
        self._cls = cls;
        self._instances = {}

    def __call__(self, *args, **kwargs):
        if self._cls not in self._instances:
            self._instances[self._cls] = self._cls()

        return self._instances[self._cls]