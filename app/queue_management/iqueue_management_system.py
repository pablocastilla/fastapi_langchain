# generic interface for the queue management system logic
from abc import ABC, abstractmethod


class IQueueManagementSystem(ABC):
    """
    Abstract implementation of the client that is responsible for the logic of the Queue Management System.
    """
    @abstractmethod
    def enqueue(self, name: str, urgency: int) -> str:
        pass

    @abstractmethod
    def dequeue(self) -> str:
        pass
