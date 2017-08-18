from abc import abstractmethod, ABCMeta


class Pipeline():
    __metaclass__ = ABCMeta

    @abstractmethod
    def put(self, item):
        pass
