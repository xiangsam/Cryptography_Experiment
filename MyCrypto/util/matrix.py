# -*- coding: utf-8 -*-
class Matrix():
    """
    matrix class
    """

    def __init__(self, L, etype=int):
        assert isinstance(L, list) and isinstance(L[0], list)
        self.row = len(L)
        self.col = len(L[0])
        self.etype = etype
        self._element = [
            [etype(L[i][j]) for j in range(self.col)] for i in range(self.row)
        ]

    def __repr__(self):
        return '[\n' + ''.join([(str(line) + '\n').replace('[', '').replace(
            ']', '') for line in self._element]) + ']'

    def __getitem__(self, index):
        return self._element[index[0]][index[1]]

    def __setitem__(self, index, value):
        assert isinstance(value, self.etype)
        self._element[index[0]][index[1]] = value

    def __add__(self, other):
        assert isinstance(other, Matrix)
        assert self.shape == other.shape
        out = Matrix.zero(self.row, self.col, self.etype)
        for i in range(self.row):
            for j in range(self.col):
                out[i, j] = self[i, j] + other[i, j]
        return out

    def __sub__(self, other):
        assert isinstance(other, Matrix)
        assert self.shape == other.shape
        out = Matrix.zero(self.row, self.col, self.etype)
        for i in range(self.row):
            for j in range(self.col):
                out[i, j] = self[i, j] - other[i, j]
        return out

    def __mul__(self, other):
        if isinstance(other, self.etype):  #element multiply matrix
            out = Matrix.zero(self.row, self.col, self.etype)
            for i in range(self.row):
                for j in range(self.col):
                    out[i, j] = self[i, j] * other
            return out
        assert isinstance(other, Matrix) and self.col == other.row
        out = Matrix.zero(self.row, other.col, self.etype)
        for i in range(self.row):
            for j in range(other.col):
                temp = self.etype(0)
                for k in range(self.col):
                    temp = temp + self[i, k] * other[k, j]
                out[i, j] = temp
        return out

    def __mod__(self, other):
        assert isinstance(other, self.etype)
        out = Matrix.zero(self.row, self.col)
        for i in range(self.row):
            for j in range(self.col):
                out[i, j] = self[i, j] % other
        return out

    def copy(self):
        ans = Matrix.zero(self.row, self.col,self.etype)
        for i in range(self.row):
            for j in range(self.col):
                ans[i,j] = self[i,j]
        return ans

    def getColumn(self, index):
        assert 0 <= index < self.col
        ans = []
        for row in range(self.row):
            ans.append(self[row, index])
        return ans
    def getRow(self, index):
        assert 0 <= index < self.row
        ans = []
        for col in range(self.col):
            ans.append(self[index, col])
        return ans

    def slice(self, r_index, c_index):
        """
        design to get subMatrix
        remove r-th row and c-th column(r,c begin at 0)
        """
        out = Matrix.zero(self.row - 1, self.col - 1, self.etype)
        for i in range(self.row):
            for j in range(self.col):
                if i == r_index:
                    break
                if j == c_index:
                    continue
                new_i = i if i < r_index else i - 1
                new_j = j if j < c_index else j - 1
                out[new_i, new_j] = self[i, j]
        return out

    @staticmethod
    def identity(dim, etype=int):
        """
        return the identity matrix whose dim is n
        """
        List = [[1 if i == j else 0 for j in range(dim)] for i in range(dim)]
        return Matrix(List, etype)

    @staticmethod
    def zero(row_len, col_len, etype=int):
        L = [[0 for c in range(col_len)] for r in range(row_len)]
        return Matrix(L, etype)

    @property
    def shape(self):
        return (self.row, self.col)

    @property
    def isSquare(self):
        return self.row == self.col

    def transpose(self):
        out = Matrix.zero(self.col, self.row, self.etype)
        for i in range(self.row):
            for j in range(self.col):
                out[j, i] = self[i, j]
        return out

    def det(self):
        assert self.isSquare
        if self.row == 1:
            return self[0, 0]
        if self.row == 2:
            return self[0, 0] * self[1, 1] - self[0, 1] * self[1, 0]
        ans = self.etype(0)
        for j in range(self.col):
            if j % 2 == 0:
                ans = ans + self[0, j] * self.slice(0, j).det()
            else:
                ans = ans - self[0, j] * self.slice(0, j).det()
        return ans

    def adjoint_matrix(self):
        assert self.row == self.col
        out = Matrix.zero(self.row, self.col, self.etype)
        for i in range(self.row):
            for j in range(self.col):
                if (i+j)%2 == 0:
                    out[i, j] = self.etype(0) + self.slice(i, j).det()
                else:
                    out[i, j] = self.etype(0) - self.slice(i, j).det()
        return out.transpose()

    def inverse(self):
        assert self.row == self.col
        det = self.det()
        ad_m = self.adjoint_matrix()
        for i in range(ad_m.row):
            for j in range(ad_m.col):
                ad_m[i, j] = self.etype(ad_m[i, j] / det)
        return ad_m


if __name__ == '__main__':
    m = Matrix([[1, 2, 3], [4, 5, 6]])
    print(m.row)
    print(m*2)
    a = Matrix([[100, 10], [10, 100], [1, 1000]])
    b = Matrix.identity(3)
    t = Matrix([[1, 3, 5, 9], [1, 3, 1, 7], [4, 3, 9, 7], [5, 2, 0, 9]])
    tt = Matrix([[3, 2, 1], [1, 1, 1], [1, 0, 1]])
    k = Matrix([[10,5,12],[3,14,21],[8,9,11]])
    print(a.slice(1, 0))
    print(m * a)
    print(t.det())
    print(k.adjoint_matrix() % 26)
    print(tt.inverse())
    k = Matrix([[443, 442, 442], [858, 495, 780], [494, 52, 365]])
    print(k % 26)
