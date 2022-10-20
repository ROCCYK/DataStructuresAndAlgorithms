import ctypes  # provides low-level arrays
import matplotlib.pyplot as plt
from time import time
import time

class DynamicArray:
    """A dynamic array class akin to a simplified Python list."""

    def __init__(self):
        """Create an empty array."""
        self._n = 0  # count actual elements
        self._capacity = 1  # default array capacity
        self._A = self._make_array(self._capacity)  # low-level array
        self.cost = 0 # added cost var
        self.costlin = 0 # added cost var for linear
        self.costgeo = 0 # added cost var for geometric
        self.costlist = [] # added cost var list to store cost var
        self.timelist = [] # added time var list to store elapsed time

    def __len__(self):
        """Return number of elements stored in the array."""
        return self._n

    def __getitem__(self, k):
        """Return element at index k."""
        if not 0 <= k < self._n:
            raise IndexError('invalid index')
        return self._A[k]  # retrieve from array

    def append(self, obj, lingeo='linear'): # added lingeo input and defaulted to linear
        """Add object to end of the array."""
        if self._n == self._capacity:  # not enough room
            if lingeo.lower() == 'linear': # linear if input is 'linear'
                self._resize(self._capacity + 10)  # adds 10 to total capacity
                # self.costlin += (self._capacity + 10) # adds + 10 to costlin var whenever we resize using linear
                self.costlin = (self._capacity + 10)  # sets costlin equal to the total capacity + 10
                self.costlist.append(self.costlin) # appends costlin var to total cost list
            elif lingeo.lower() == 'geometric': # geometric if input is 'geometric'
                self._resize(2 * self._capacity)  # so double capacity
                # self.costgeo += (2 * self._capacity) # adds 2 * the capacity of the array whenever we resize using geometric
                self.costgeo = (2 * self._capacity)  # sets costgeo equal to the total capacity multiplied by 2
                self.costlist.append(self.costgeo)# appends costgeo var to total cost list
        self._A[self._n] = obj
        self._n += 1
        self.cost = 1 # everytime we use the append() method we append $1 to cost list
        self.costlist.append(self.cost) # store each cost var in a cost var list

    def _resize(self, c):  # nonpublic utitity
        """Resize internal array to capacity c."""
        B = self._make_array(c)  # new (bigger) array
        for k in range(self._n):  # for each existing value
            B[k] = self._A[k]
        self._A = B  # use the bigger array
        self._capacity = c

    def _make_array(self, c):  # nonpublic utitity
        """Return new array with capacity c."""
        return (c * ctypes.py_object)()  # see ctypes documentation

    def insert(self, k, value):
        """Insert value at index k, shifting subsequent values rightward."""
        # (for simplicity, we assume 0 <= k <= n in this verion)
        if self._n == self._capacity:  # not enough room
            self._resize(2 * self._capacity)  # so double capacity
        for j in range(self._n, k, -1):  # shift rightmost first
            self._A[j] = self._A[j - 1]
        self._A[k] = value  # store newest element
        self._n += 1

    def remove(self, value):
        """Remove first occurrence of value (or raise ValueError)."""
        # note: we do not consider shrinking the dynamic array in this version
        for k in range(self._n):
            if self._A[k] == value:  # found a match!
                for j in range(k, self._n - 1):  # shift others to fill gap
                    self._A[j] = self._A[j + 1]
                self._A[self._n - 1] = None  # help garbage collection
                self._n -= 1  # we have one less item
                return  # exit immediately
        raise ValueError('value not found')  # only reached if no match

    def getcostlist(self): # created a function to display cost list
        return self.costlist # returns self.costlist

    def time_cost(self, n, lingeo='linear'): # created time cost function that takes n input and linear or geometric
        for i in range(n): # iterates through n times
            start_time = time.time_ns() # records start time in nanoseconds
            self.append(i,lingeo=lingeo.lower()) # appends n times
            end_time = time.time_ns() # records end time in nanoseconds
            elapsed_time = (end_time - start_time) * 100000 # elapsed time is end - start multiplied by 100000 to see a bigger time
            self.timelist.append(str(round(elapsed_time, 2))) # rounded elapsed time to 2 decimal places and appended it to time cost list
        return self.timelist,self.costlist[:len(self.timelist)] # returns a tuple of time list and cost list

    def num_cost(self, n, lingeo='linear'): # created number of items and cost function that takes n input and either 'linear' or ' 'geometric'
        for i in range(n): # iterates through n times
            self.append(i,lingeo=lingeo.lower()) # appends n times
        n = len(self.getcostlist()) # reassigns n to len of cost list
        return list(range(1,n+1)), self.getcostlist() # returns number of items and cost list

    def rationalize(self): # created a rationalize function
        return round(sum(self.getcostlist())/len(self.getcostlist()),2) # returns sum of the cost list divided by length of cost list for average cost

if __name__ == '__main__':
    linear = DynamicArray() # created linear object of DynamicArray class
    geometric = DynamicArray() # created geometric object of DynamicArray class
# be aware when dealing with a large n matplotlib.pylot sometimes gets overwhelmed and causes missing data on graph
    n = 300 # set number of items to 10000

    linear_num_cost = linear.num_cost(n,lingeo='linear') # set linear_num_cost to store tuple of num of items list and cost list
    plt.bar(linear_num_cost[0],linear_num_cost[1]) # plotted x = num of items, y = cost list
    plt.title('Linear Num-Cost Graph') # titled graph
    plt.xlabel('# of items') # labeled x axis
    plt.ylabel('Cost in $') # labelled y axis
    plt.savefig('Linear Num-Cost Graph.jpg') # saved the plot in the same directory as the py file
    plt.show() # showed the plot

    geometric_num_cost = geometric.num_cost(n,lingeo='geometric') # set geometric_num_cost to store tuple of num of items list and cost list
    plt.bar(geometric_num_cost[0], geometric_num_cost[1]) # plotted x = num of items, y = cost list
    plt.title('Geometric Num-Cost Graph') # titled graph
    plt.xlabel('# of items') # labeled x axis
    plt.ylabel('Cost in $') # labelled y axis
    plt.savefig('Geometric Num-Cost Graph.jpg') # saved the plot in the same directory as the py file
    plt.show() # showed the plot

    linear_time_cost = linear.time_cost(n,lingeo='linear') # set linear_time_cost to store tuple of time list and cost list
    plt.plot(linear_time_cost[0], linear_time_cost[1]) # plotted x = time list, y = cost list
    plt.title('Linear Time-Cost Graph') # titled graph
    plt.xlabel('Time in Nanoseconds') # labeled x axis
    plt.ylabel('Cost in $') # labelled y axis
    plt.savefig('Linear Time-Cost Graph.jpg') # saved the plot in the same directory as the py file
    plt.show() # showed the plot

    geometric_time_cost = geometric.time_cost(n, lingeo='geometric') # set geometric_time_cost to store tuple of time list and cost list
    plt.plot(geometric_time_cost[0], geometric_time_cost[1]) # plotted x = time list, y = cost list
    plt.title('Geometric Time-Cost Graph') # titled graph
    plt.xlabel('Time in Nanoseconds') # labeled x axis
    plt.ylabel('Cost in $') # labelled y axis
    plt.savefig('Geometric Time-Cost Graph.jpg') # saved the plot in the same directory as the py file
    plt.show() # showed the plot

    print(f'Linear cost on average: ${linear.rationalize()} for {n} items')
    print(f'Geometric cost on average: ${geometric.rationalize()} for {n} items')

    print('Therefore Geometric is better than linear when dealing with a large number of items.')


