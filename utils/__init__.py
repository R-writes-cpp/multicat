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
        super().__init__([None] + arr)

        if 'cmp' in kwargs:
            self.cmp = kwargs['cmp']

        self.construct_heap()

    cmp = staticmethod(lambda x, y : x > y)

    def construct_heap(self):
        for i in range (len(self) // 2, 0, -1):
            self.heapify(i)

    def heapify(self, i):
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
        super().append(n) # push to the end of the heap; the last child in the last row.
        self.heapify(1)

    def pop(self):
        top = self[1]

        self[1] = self[-1]
        super().pop()

        self.heapify(1)

        return top

def get_top_n(n, pq, l=staticmethod(lambda x : x)):
    top_n = []

    while len(pq) > 1 and len(top_n) < n:
        top_n.append (l (pq.pop()))

    return top_n
