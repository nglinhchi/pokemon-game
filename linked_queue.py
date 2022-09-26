from typing import TypeVar
from queue_adt import Queue
from node import Node
T = TypeVar('T')

class LinkQueue(Queue[T]):

    def __init__(self) -> None:
        Queue.__init__(self)
        self.front = None
        self.rear = None

    def is_empty(self) -> bool:
        return self.front is None
    
    def is_full(self) -> bool:
        return False

    def clear(self) -> None:
        Queue.clear()
        self.front = None
        self.rear = None

    def append(self, item: T) -> None:
        new_node = Node(item)
        if self.is_empty():
            self.front = new_node
        else:
            self.rear.link = new_node
        self.rear = new_node
        self.length += 1

    def serve(self) -> T:
        if not self.is_empty():
            item = self.front.item
            self.front = self.front.link
            self.length -= 1
            if self.is_empty():
                self.rear = None
            return item
        else:
            raise ValueError("Queue is empty")