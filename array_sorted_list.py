"""
    Array-based implementation of SortedList ADT.
    Items to store should be of time ListItem.
"""

from referential_array import ArrayR
from sorted_list import *

__author__ = 'Maria Garcia de la Banda and Brendon Taylor. Modified by Alexey Ignatiev and Graeme Gange'
__docformat__ = 'reStructuredText'

class ArraySortedList(SortedList[T]):
    """ SortedList ADT implemented with arrays. """
    MIN_CAPACITY = 1

    def __init__(self, max_capacity: int) -> None:
        """ ArraySortedList object initialiser. """

        # first, calling the basic initialiser
        SortedList.__init__(self)

        # initialising the internal array
        size = max(self.MIN_CAPACITY, max_capacity)
        self.array = ArrayR(size)

    def reset(self):
        """ Reset the list. """
        SortedList.__init__(self)

    def __getitem__(self, index: int) -> T:
        """ Magic method. Return the element at a given position. """
        return self.array[index]

    def __setitem__(self, index: int, item: ListItem) -> None:
        """ Magic method. Insert the item at a given position,
            if possible (!). Shift the following elements to the right.
        """
        if self.is_empty() or \
                (index == 0 and item.key <= self[index].key) or \
                (index == len(self) and self[index - 1].key <= item.key) or \
                (index > 0 and self[index - 1].key <= item.key <= self[index].key):

            if self.is_full():
                self._resize()

            self._shuffle_right(index)
            self.array[index] = item
        else:
            # the list isn't empty and the item's position is wrong wrt. its neighbourghs
            raise IndexError('Element should be inserted in sorted order')

    def __contains__(self, item: ListItem):
        """ Checks if value is in the list. """
        for i in range(len(self)):
            if self.array[i] == item:
                return True
        return False

    def _shuffle_right(self, index: int) -> None:
        """ Shuffle items to the right up to a given position. """
        for i in range(len(self), index, -1):
            self.array[i] = self.array[i - 1]

    def _shuffle_left(self, index: int) -> None:
        """ Shuffle items starting at a given position to the left. """
        for i in range(index, len(self)):
            self.array[i] = self.array[i + 1]

    def _resize(self) -> None:
        """ Resize the list. """
        # doubling the size of our list
        new_array = ArrayR(2 * len(self.array))

        # copying the contents
        for i in range(self.length):
            new_array[i] = self.array[i]

        # referring to the new array
        self.array = new_array

    def delete_at_index(self, index: int) -> ListItem:
        """ Delete item at a given position. """
        if index >= len(self):
            raise IndexError('No such index in the list')
        item = self.array[index]
        self.length -= 1
        self._shuffle_left(index)
        return item

    def index(self, item: ListItem) -> int:
        """ Find the position of a given item in the list. """
        pos = self._index_to_add(item)
        if pos < len(self) and self[pos] == item:
            return pos
        raise ValueError('item not in list')

    def is_full(self):
        """ Check if the list is full. """
        return len(self) >= len(self.array)

    def add(self, item: ListItem) -> None:
        """ Add new element to the list. """
        if self.is_full():
            self._resize()

        # find where to place it
        position = self._index_to_add(item)

        self[position] = item
        self.length += 1

    def _index_to_add(self, item: ListItem) -> int:
        """ Find the position where the new item should be placed. """
        low = 0
        high = len(self) - 1

        while low <= high:
            mid = (low + high) // 2
            if self[mid].key < item.key:
                low = mid + 1
            elif self[mid].key > item.key:
                high = mid - 1
            else:
                return mid

        return low
    
    # def stable_index_to_add(self,item) -> int:
        
    #     low = self._index_to_add(self,item)
    #     high = len(self)-1
    #     mid = (low + high) // 2

    #     if(mid == high or item.key < self[mid+1]) and self[mid] == item.key:
    #         return mid
    #     elif item.key < self[mid]:

    
    def add_stable(self, item: ListItem) -> None:
        """ 
        Add new element to the list. Replaces the default add method when
        array is meant to be kept stable.
        """
        if self.is_full():
            self._resize()

        # find where to place it
        position = self.stable_index_to_add(item)

        self[position] = item
        self.length += 1
    
    def stable_index_to_add(self, item: ListItem) -> int:
        """ 
        Find the position where the new item should be placed. Makes
        sure index is the last occurrence of item.
        :pre: array is not full
        """
        if self.is_full() == True:
            raise ValueError("Array is full")
        low = 0
        high = len(self) - 1
        
        while low <= high:
            
            mid = (low + high) // 2
            # print(low, mid, high)
            if self[mid].key < item.key:
                # print("low")
                low = mid + 1
            elif self[mid].key > item.key:
                # print("high")
                high = mid - 1
            
            elif (mid == high or self[mid+1].key != item.key):
                # print("mid")
                return mid + 1
            elif self[mid+1].key == item.key:
                # print("new cond")
                low = mid + 15
                

        # print("low")
        return low

    # def get_last_index(self, low, high, searchkey):

        # """
        # Returns index of last occurrence of searchkey. If invalid returns -1.
        # TODO user facing check of low high inputs.
        # :param low: the index to search from
        # :param high: the end index (length of array)
        # :param searchkey: the key to search for
        # """
        # n = len(self)
        # #n = length of array
        # if high >= low:
 
        # # low + (high - low)/2
        #     mid = (low + high)//2
    
        #     if(mid == len(self) - 1 or searchkey < self[mid+1].key) and self[mid].key == searchkey :
        #         return mid
        #     elif searchkey < self[mid].key:
        #         return self.get_last_index(low, (mid -1), searchkey)
        #     else:
        #         return self.get_last_index((mid + 1), high, searchkey)    
        # return -1
    def get_last_index(self, key: int):
        return self.stable_index_to_add(ListItem(None, key)) - 1  #returns index of last occurence of item with same key. Value set to none as does not matter

    def reverse_order(self):
        """
        Takes input array sorted in ascending order and reverses it using the same key
        so that the array is descending.
        :out: descending sorted array
        """
        reverse_arr = ArraySortedList(len(self))
        for item in self:
            reverse_arr.add(ListItem(item.value, (item.key * -1)))
        return reverse_arr


    def tiebreak(self, start_idx,last_idx):
        """
        Breaks ties by pokemon order for specified instance of tie
        :param start_idx: start of tie
        :param last_idx: end of tie
        """
        if not (last_idx - start_idx) + 1 > 1:  #check if start and end index contain items (add 1 to include start index)
            raise ValueError("Invalid range for tiebreak")
        pokeorder_list = ArraySortedList((last_idx-start_idx)+1)
        while start_idx <= last_idx:
            pokemon = self[start_idx].value
            key = pokemon.POKE_NO
            pokeorder_list.add(ListItem(pokemon,key))

