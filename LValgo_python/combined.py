class RMQ:
    def __init__(self, input_array):
        self.A = input_array
        self.n = len(self.A)
        self.M = [[0]*self.n for _ in range(self.n)]
        self.fill_M()

    def fill_M(self):
        for i in range(self.n):
            for j in range(i, self.n):
                if i == j:
                    self.M[i][j] = i
                else:
                    self.M[i][j] = j if self.A[j] < self.A[self.M[i][j-1]] else self.M[i][j-1]
                self.M[j][i] = self.M[i][j]

    def query(self, i, j):
        return self.M[i][j]

class Suffix:
    def __init__(self, text, index):
        self.text = text
        self.index = index

    def __lt__(self, other):
        # Python's sort uses < comparison by default
        return self.text[self.index:] < other.text[other.index:]

    def length(self):
        return len(self.text) - self.index

    def char_at(self, i):
        return self.text[self.index + i]

class SuffixArray:
    def __init__(self, s):
        self.suffixes = [Suffix(s, i) for i in range(len(s))]
        self.suffixes.sort()
        self.lcp = self.build_lcp(s)

    def build_lcp(self, s):
        n = len(self.suffixes)
        lcp = [0] * n
        for i in range(1, n):
            lcp[i] = self.lcp_suffix(self.suffixes[i - 1], self.suffixes[i])
        return lcp

    def lcp_suffix(self, s1, s2):
        i = 0
        while i < s1.length() and i < s2.length() and s1.char_at(i) == s2.char_at(i):
            i += 1
        return i

class MatrixL:
    def __init__(self, max_errors, text, pattern):
        self.k = max_errors
        self.n = len(text)
        self.m = len(pattern)
        self.str = self.concat(text, pattern)
        self.suffix_array = SuffixArray(self.str)  # Assuming SuffixArray class is defined
        self.matrix = [[0] * (self.k + 1) for _ in range(self.n - self.m + self.k + 1)]

    def concat(self, string1, string2):
        return string1 + '#' + string2

    def compute_matrix_l(self):
        self.init_step_two()
        self.init_step_three()
        self.fill_matrix()
        self.print_matrix()

    def init_step_two(self):
        j = self.k
        for d, i in zip(range(-j, -1), range(1, j)):
            self.matrix[self.transform(d, j)][j - i] = j - i

    def init_step_three(self):
        j = self.k
        for d, i in zip(range(-j, 0), range(1, j + 1)):
            self.matrix[self.transform(d, j)][j - i + 1] = j - i + 1

    def transform(self, x, k):
        return x + (self.n - self.m + k) // 2  # Assuming centering transform


    def fill_matrix(self):
        for e in range(self.k + 1):
            for d in range(-e + 1, self.n - self.m + 1):
                print(f"\nlogical d: {d} physical d: {self.transform(d, self.k)} e: {e}")
                if e == 0:
                    upper_left = immediate_left = lower_left = -1
                    print(f"Immediate left (initialized): {immediate_left}")
                    print(f"Lower left (initialized): {lower_left}")
                    print(f"Upper left (initialized): {upper_left}")
                else:
                    immediate_left = self.matrix[self.transform(d, self.k)][e-1]
                    print(f"Immediate left: {immediate_left}")
                    upper_left = self.matrix[self.transform(d-1, self.k)][e-1]
                    print(f"Upper left: {upper_left}")
                    if self.transform(d, self.k) < self.transform(self.n - self.m, self.k):
                        lower_left = self.matrix[self.transform(d+1, self.k)][e-1]
                        print(f"Lower left: {lower_left}")
                    else:
                        print(f"Cannot read from spot to bottom left at: {self.transform(d+1, self.k)} {e-1}")
                        is_bottom_row = True

                if is_bottom_row:
                    row = max(upper_left + 1, immediate_left + 1)
                    print(f"max: {row}")
                    is_bottom_row = False
                else:
                    row = max(max(immediate_left + 1, lower_left), upper_left + 1)
                    print(f"max: {row}")

                row = min(row, self.m)
                print(f"m: {self.m}")
                print(f"row: {row}")
                lcp = self.suffix_array.calculate_lcp(self.str, row + d, row + self.n + 1, self.n, self.m)
                print(f"lcp: {lcp}")
                self.matrix[self.transform(d, self.k)][e] = row + lcp
                print(f"matrix element: {self.matrix[self.transform(d, self.k)][e]}")


    def print_matrix(self):
        for row in self.matrix:
            print(" ".join(map(str, row)))

# Example usage
text = "some_text_here"
pattern = "pattern_here"
ml = MatrixL(3, text, pattern)
ml.compute_matrix_l()