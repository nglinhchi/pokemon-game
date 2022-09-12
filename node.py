""" Implementation of a node in linked lists. """

from typing import TypeVar, Generic
T = TypeVar('T')

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'

class Node(Generic[T]):
    """ Simple linked node. It contains an item and has a reference to next node. """

    def __init__(self, item: T = None) -> None:
        """ Node initialiser. """
        self.item = item
        self.next = None

def get_node_at_index(head: Node[T], index: int):
    """ Return the node at a given position. """
    current = head
    for i in range(index):
        current = current.next
    return current

def index(head: Node[T], item: T) -> int:
        """ Find the position of a given item in the list. """
        current = head
        index = 0
        while current is not None and current.item != item:
            current = current.next
            index += 1
        if current is None:
            raise ValueError('Item is not in list')
        else:
            return index