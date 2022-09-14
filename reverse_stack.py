from referential_array import ArrayR
from stack_adt import Stack, T

class ArrayReversedStack(Stack[T]):
    
    MIN_CAPACITY = 1

    def __init__(self, max_capacity: int) -> None:
        Stack.__init__(self)
        self.array = ArrayR(max(self.MIN_CAPACITY, max_capacity))

    def is_full(self) -> bool:
        return len(self) ==  len(self.array)

    def push(self, item: T) -> None:
        """
        - shift all items right by 1 position
        - assign value of first position to item
        - increment length by 1
        """
        if self.is_full():
            raise Exception("Stack is full")
        for i in range (self.length,0,-1):
            self.array[i] = self.array[i-1]
        self.array[0] = item
        self.length += 1
        

    def pop(self) -> T:
        """
        - make a copy of first item 
        - shift all items left by 1 position
        - decrement length by 1
        - return the saved item
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        item = self.array[0]
        for i in range (self.length-1):
            self.array[i] = self.array[i+1]
        self.length -= 1
        return item

    def peek(self) -> T:
        """
        - return the first item
        """
        if self.is_empty():
            raise Exception("Stack is empty")
        return self.array[0]
