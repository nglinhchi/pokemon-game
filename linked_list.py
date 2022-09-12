""" Linked-node based implementation of List ADT. """
import node
from abstract_list import List, T

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev'
__docformat__ = 'reStructuredText'

class LinkedList(List[T]):
    """ List ADT implemented with linked nodes. """
    def __init__(self, dummy_capacity=1) -> None:
        """ Linked-list object initialiser. """
        super(LinkedList, self).__init__()
        self.head = None

    def clear(self):
        """ Clear the list. """
        # first call clear() for the base class
        super(LinkedList, self).clear()
        self.head = None

    def __setitem__(self, index: int, item: T) -> None:
        """ Magic method. Insert the item at a given position. """
        node_at_index = self.__get_node_at_index(index)
        node_at_index.item = item

    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        node_at_index = self.__get_node_at_index(index)
        return node_at_index.item

    def index(self, item: T) -> int:
        """ Find the position of a given item in the list. """
        return node.index(self.head, item)

    def __get_node_at_index(self, index: int) -> node.Node[T]:
        """ Get node object at a given position. """
        if 0 <= index and index < len(self):
            return node.get_node_at_index(self.head, index)
        else:
            raise ValueError('Index out of bounds')

    def delete_at_index(self, index: int) -> T:
        """ Delete item at a given position. """
        try:
            previous_node = self.__get_node_at_index(index-1)
        except ValueError as e:
            if self.is_empty():
                raise ValueError('List is empty')
            elif index == 0:
                item = self.head.item
                self.head = self.head.next
            else:
                raise e
        else:
            item = previous_node.next.item
            previous_node.next = previous_node.next.next
        self.length -= 1
        return item

    def insert(self, index: int, item: T) -> None:
        """ Insert an item at a given position. """
        new_node = node.Node(item)
        if index == 0:
            new_node.next = self.head
            self.head = new_node
        else:
            previous_node = self.__get_node_at_index(index - 1)
            new_node.next = previous_node.next
            previous_node.next = new_node
        self.length += 1