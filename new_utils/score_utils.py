import numpy as np
import math
import matplotlib.pyplot as plt
from collections import Counter

def convert_ctrs_to_mask(rows_number, cols_number, ctrs):
    my_mask = np.zeros((rows_number, cols_number))
    for c in ctrs:
        assert len(c) == 3
        plot_circle_in_matrix(my_mask, c[1], c[0], c[2])
    return my_mask

def draw_pixel_in_matrix(m, row, col):
    [rows_number, cols_number] = m.shape
    if col>=0 and col<cols_number and row>=0 and row<rows_number:
        #print "pixel ({} {})".format(row,col)
        m[row][col] = 1


def plot_circle_in_matrix(m, x0, y0, r):
    for x in range(x0-r, x0+r+1):
        s = round(math.sqrt(r**2 - (x-x0)**2))
        draw_pixel_in_matrix(m, int(y0 - s), x)
        draw_pixel_in_matrix(m, int(y0 + s), x)


def convert_to_binary(a, th):
    a[a < th] = 0
    a[a >= th] = 1
    return a

def verify_binary(a):
    b=np.unique(a)
    assert len(b) == 2
    assert b[0] == 0
    assert b[1] == 1

def show_two_binary_matrices(m1,m2):
    [rows1, cols1] = m1.shape
    [rows2, cols2] = m2.shape
    assert rows1 == rows2
    assert cols1 == cols2
    d3_mat = np.zeros((rows1, cols1, 3))
    d3_mat[:, :, 0] = m1
    d3_mat[:, :, 1] = m2
    plt.imshow(d3_mat)
    plt.show()


def compare_two_matrices(ref_mat, test_mat):
    assert ref_mat.shape == test_mat.shape
    c = zip(ref_mat.flatten(), test_mat.flatten())
    k = Counter(c).keys()
    v = Counter(c).values()
    true_pos_count  = v[k.index((1,1))]
    true_neg_count  = v[k.index((0,0))]
    false_pos_count  = v[k.index((0,1))]
    false_neg_count  = v[k.index((1,0))]
    return [true_pos_count, true_neg_count, false_pos_count, false_neg_count]

