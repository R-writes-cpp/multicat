# DYNAMIC PROGRAMMING / 2D ARRAYS: line 13
# HEAP / PRIORITY QUEUE / RECURSION / OBJECT-ORIENTED PROGRAMMING: line 34

def clamp(min_x, x, max_x): # basic function to clamp a value into a given range. needed for calculation descriptor affinities as part of the recommendation algorithm
    if x < min_x:
        return min_x

    if x > max_x:
        return max_x

    return x

def levenshtein(a, b): # see Design for explanation of algorithm. the following comments explain the specific implementation rather than the algorithm itself
    a = a.upper()
    b = b.upper() # put them in the same case. whether it's upper- or lowercase is arbitrary

    rows, cols = len(a), len(b)
    last_dp = [i + (0 if a[0] == b[0] else 1) for i in range(cols)] # optimisation which stores dp[i-1]

    for i in range (1, rows):
        current_dp = [] # stores dp[i]
        current_dp.append(last_dp[0] + 1)

        for j in range (1, cols):
            if a[i] == b[j]:
                current_dp.append(last_dp[j-1]) # if they're the same, then that means the score doesn't change and we can just use the best score from before the current characters
            else:
                current_dp.append(1 + min(last_dp[j], current_dp[j-1], last_dp[j-1])) # we can either remove, edit, or add a character to resolve the character difference

        last_dp = current_dp

    return last_dp[-1]

class priority_queue(list):
    def __init__(self, arr, **kwargs):
        if 'weight' in kwargs: # used to pass a custom weighing function for our priority queue. used most notably in the Levenshtein search
            self.custom_weight = True
            self.weight = kwargs['weight']

        if 'copy' in kwargs:
            self.copy = kwargs['copy']
        else:
            self.copy = self.custom_weight

        if 'desc' in kwargs:
            self.desc = kwargs['desc']

        if self.copy: # should we create a copy of the corresponding weight? say each element in the queue is a string. if we were to calculate the Levenshtein distance from a given string from every element, then this would be an O(n^2) operation and so it's best to cache the result in a copy. however if our weighing function is something short and O(1) like x -> -x then we don't need to create copies
            super().__init__(
                [None] +
                list (map (lambda x : (x, self.weight(x)), arr))
            )
        else:
            super().__init__([None] + arr)

        self.construct_heap()

    custom_weight = False
    copy = False
    desc = True
    weight = staticmethod(lambda x : x)

    def cmp(self, x, y):
        if self.custom_weight:
            if self.copy:
                return (x[1] > y[1]) if self.desc else (x[1] < y[1]) # compare the weights which are stored at index 1 in a tuple
            else:
                return (self.weight(x) > self.weight(y)) if self.desc else (self.weight(x) < self.weight(y)) # no tuples used because we're not copying, so just call the weighing function directly
        else:
            return (x > y) if self.desc else (x < y) # default operation is just to treat the values as the weighing function. used for basic ascending/descending sorting

    def construct_heap(self):
        for i in range (len(self) // 2, 0, -1):
            self.heapify(i) # progressively sorts the heap tree, starting from the leaves and moving up to the root. works to fully sort the tree in the same way that an insertion sort does; if you sort [0..1], then [0..2], [0..3] etc. until [0..n] then you'll attain a fully sorted array/tree

    def heapify(self, i): # treats the node indicated by i as a root and ensures that it and all its descendents are sorted via a recursive algorithm
        left = 2 * i
        right = 2 * i + 1

        largest_idx = i

        if left < len(self) and self.cmp(self[left], self[largest_idx]):
            largest_idx = left

        if right < len(self) and self.cmp(self[right], self[largest_idx]):
            largest_idx = right

        if largest_idx != i: # i.e., i (the parent) is not the largest of three indices scanned, and so at least one child is greater
            self[i], self[largest_idx] = self[largest_idx], self[i]
            self.heapify(largest_idx) # now we're moving to one of the child indices. remember that largest_idx, if not already i, points to either the left or right child. i.e., we are going down the tree with this recursion.

    def append(self, n):
        if self.copy:
            super().append((n, self.weight(n)))
        else:
            super().append(n) # push to the end of the heap; the last child in the last row.

        self.heapify(1) # sort starting from the top

    def pop(self):
        top = self[1][0] if self.copy else self[1]

        self[1] = self[-1]
        super().pop()

        self.heapify(1)

        return top

    def get_top_n(self, n):
        top_n = []

        while len(self) > 1 and len(top_n) < n:
            top_n.append (self.pop())

        return top_n
