import numpy as np
import math
import matplotlib.pyplot as plt
from collections import Counter
import sys
sys.path.append("/mnt/disks/disk0/deep_moon_working_dir/DeepCrater/utils")
import template_match_target as tmt
from scipy.spatial import distance

def convert_ctrs_to_mask(rows_number, cols_number, ctrs):
    my_mask = np.zeros((rows_number, cols_number))
    for c in ctrs:
        assert len(c) == 3
        plot_circle_in_matrix(my_mask, c[0], c[1], c[2])
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

def show_two_binary_matrices(ref_mat,test_mat):
    [rows1, cols1] = ref_mat.shape
    [rows2, cols2] = test_mat.shape
    assert rows1 == rows2
    assert cols1 == cols2
    d3_mat = np.zeros((rows1, cols1, 3))
    d3_mat[:, :, 0] = ref_mat
    d3_mat[:, :, 1] = test_mat
    plt.imshow(d3_mat)
    plt.title("red - ref. green - test. yellow - overlap")
    plt.show()


def compare_two_matrices(ref_mat, test_mat):
    assert ref_mat.shape == test_mat.shape
    c = zip(ref_mat.flatten(), test_mat.flatten())
    my_dict = Counter(c) 
    true_neg_count = my_dict[(0,0)]
    false_pos_count = my_dict[(0,1)]
    false_neg_count = my_dict[(1,0)]
    true_pos_count = my_dict[(1,1)]
    return [true_neg_count, false_pos_count, false_neg_count,true_pos_count]

def extract_rings_using_model(model, img):
    pred = model.predict(img)
    extracted_rings = tmt.template_match_t(pred[0].copy(), minrad=2.)
    return extracted_rings

def smallercirclearea(r1, r2):
    radsmaller = min(r1, r2)
    return math.pi * radsmaller * radsmaller

def calcAreaIntersectingCircles(d, rad1, rad2):
    rad1 = float(rad1)
    rad2 = float(rad2)
    d = float(d)

    rad1sqr = rad1 * rad1
    rad2sqr = rad2 * rad2

    #if the circle centers are the same
    if d == 0:       
        return smallercirclearea(rad1,rad2)

    angle1 = (rad1sqr + (d * d) - rad2sqr) / (2 * rad1 * d)
    angle2 = (rad2sqr + (d * d) - rad1sqr) / (2 * rad2 * d)

    # Check to see if the circles are overlapping
    if ((angle1 < 1 and angle1 >= -1) or (angle2 < 1 and angle2 >= -1)):
        theta1 = (math.acos(angle1) * 2)
        theta2 = (math.acos(angle2) * 2)

        area1 = (0.5 * theta2 * rad2sqr) - (0.5 * rad2sqr * math.sin(theta2))
        area2 = (0.5 * theta1 * rad1sqr) - (0.5 * rad1sqr * math.sin(theta1))

        return area1 + area2
    elif angle1 == 1 and angle2 == 1:        
        return 0
    elif angle1 < -1 or angle2 < -1:        
        return smallercirclearea(rad1,rad2)
    else:        
        return -1


def area_of_circle(r):
    return math.pi*r*r


#a and b are vectrors with length 3 that represent:
#x,y and radius
def compare_circles(a,b):
    assert len(a) == 3
    assert len(b) == 3
    rad_a = a[2]
    rad_b = b[2]
    dst = distance.euclidean((a[0], a[1]), (b[0], b[1]))
    if rad_a+rad_b < dst:
        return 0
    a_b_intersect_area = calcAreaIntersectingCircles(dst, rad_a, rad_b)
    a_b_union_area = area_of_circle(rad_a) + area_of_circle(rad_b) - a_b_intersect_area
    return a_b_intersect_area / a_b_union_area


def find_best_match_for_circles_list(list1, list2):
    n1 = len(list1)
    n2 = len(list2)
    m1 = np.zeros((n1, 2))
    m2 = np.zeros((n2, 2))
    for i in range(n1):
        for j in range(n2):
            p = compare_circles(list1[i],list2[j])
            if m1[i][1] < p:
                m1[i]= [j, p]
            if m2[j][1] < p:
                m2[j] = [i, p]
    return [m1, m2]

def match_circle_lists(list1, list2, min_p):
    [m1, m2] = find_best_match_for_circles_list(list1, list2)
    n1 = len(list1)
    n2 = len(list2)
    match = []
    no_match1 = set(range(n1))
    no_match2 = set(range(n2))
    for i in range(n1):
        if m1[i][1] > min_p:
            best_match = int(m1[i][0])
            if m2[best_match][0] == i:
                assert m2[best_match][1] == m1[i][1]
                match.append([i, best_match])
                no_match1.remove(i)
                no_match2.remove(best_match)
    return [match, no_match1, no_match2]


