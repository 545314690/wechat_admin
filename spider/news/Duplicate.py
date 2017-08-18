from abc import abstractmethod, ABCMeta


class Duplicate():
    __metaclass__ = ABCMeta

    @abstractmethod
    def is_duplicate(self, item):
        pass

    @abstractmethod
    def put(self, item):
        pass
