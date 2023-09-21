# in memory implementation of the queue management system
from typing import List
from app.queue_management.iqueue_management_system import IQueueManagementSystem


class MemoryQueueManagementSystem(IQueueManagementSystem):
    """
    Implementation of the client that is responsible for the logic of the Queue Management System.
    """

    def __init__(self) -> None:
        self.queue: List[str] = []

    def enqueue(self, name: str, urgency: int) -> str:
        """
        Enqueue a patient in the queue management system.
        :param name: name of the patient
        :param urgency: urgency level of the patient, 1 is the most urgent, 5 is the least urgent
        :return: the position of the patient in the queue
        """
        self.queue.append(name)
        return str(len(self.queue))

    def dequeue(self) -> str:
        """
        Dequeue a patient from the queue management system.
        :return: the name of the patient that has been dequeued
        """
        return self.queue.pop(0)
