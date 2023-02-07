import math
import numpy as np
from geopy import distance
from matplotlib import pyplot as plt

"""SandBox : 
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

point = Point(stops[3])
polygon = Polygon(pts)
print(polygon.contains(point))
"""


def distance_in_meters(pt1, pt2):
    """ Return the distance in meters between pt1 and pt2.
    wellington = (-41.32, 174.81)
    salamanca = (40.96, -5.50)
    print(distance.distance(wellington, salamanca).km)"""
    return distance.distance(pt1, pt2).m


def distance_from_all(ind_pts, list_pts):
    """Return the distance in meters of a point with the index ind_pts from all other points of the list."""
    dist_from_all = []
    for i in range(len(list_pts)):
        dist_from_all.append(distance_in_meters(list_pts[ind_pts], list_pts[i]))
    return dist_from_all


def matrix_of_distances(list_pts):
    """Create a matrix with all the distance from each other points.
    Example: Distance between the point with the index 1 and the point 5 => mat[1][5] or mat[5][1]."""
    mat = []
    for i in range(len(list_pts)):
        mat.append(distance_from_all(i, list_pts))
    return mat


def neighbours_of(ind_pts, list_pts):
    """Return the 2 indexes of the closest neighbours of the point with the index ind_pts.
    The first one is the closest."""
    dist_from_all = distance_from_all(ind_pts, list_pts)
    if ind_pts == 0:
        'In that case our value to test is the first one of the list (index 0), so the 2 first neighbours are the ' \
        'second and the third (index 1 and 2). We need to begin testing at i = 3 (fourth value).'
        neighbours = [1, 2]
        first_i = 3
    elif ind_pts == 1:
        'In that case our value to test is the second one (index 1), so the 2 first neighbours are 0 and 2.' \
        'We need to begin testing at i = 3.'
        neighbours = [0, 2]
        first_i = 3
    else:
        'In that case, our value isnt on the 2 firsts positions so we begin the testing at i = 2'
        neighbours = [0, 1]
        first_i = 2
    # print(neighbours)

    if dist_from_all[neighbours[1]] < dist_from_all[neighbours[0]]:
        neighbours = [neighbours[1], neighbours[0]]
    # print(neighbours)

    for i in range(first_i, len(list_pts)):
        # print("i =", i)
        '''There we test that we don't take the point as a neighbour of himself. And that '''
        if dist_from_all[i] != 0:  # Test that we don't take the point as a neighbour
            if dist_from_all[i] < dist_from_all[neighbours[0]]:
                "Test that the point i is closer than the first neighbour"
                neighbours[1] = neighbours[0]
                neighbours[0] = i
            else:
                if dist_from_all[i] < dist_from_all[neighbours[1]]:
                    neighbours[1] = i
        # print(neighbours)
    return neighbours


def all_neighbours(list_pts):
    neighbours = []
    for i in range(len(list_pts)):
        neighbours.append(neighbours_of(i, list_pts))
    return neighbours


def longest_distance(list_pts):
    """Longest distance between two points. Return the 2 points and the distance."""
    mat_dist = matrix_of_distances(list_pts)
    longest_dist = np.max(mat_dist)
    np_index = np.where(mat_dist == longest_dist)[0]
    points = np_index.tolist()
    return points, longest_dist


def stops_on_a_line(pt1, pt2, dist):
    """Calculate points on a line between pt1 and pt2 with a distance of dist between each stop. From pt1 to pt2
    stops = stops_on_a_line(pts[1], pts[2], 25)
    print(stops)
    plot_pts(stops, style='-', color='r')"""
    # TODO : verify latitude and longitude for the coherence
    stops_points = []
    dist_between_points = distance_in_meters(pt1, pt2)
    number_of_stops = math.ceil(dist_between_points / dist)
    dlat = (pt2[0] - pt1[0]) / number_of_stops
    dlong = (pt2[1] - pt1[1]) / number_of_stops
    for i in range(0, number_of_stops):
        stops_points.append((pt1[0] + i * dlat, pt1[1] + i * dlong))
    stops_points.append(pt2)
    return stops_points


def sorted_points(list_pts):
    """Return the list_pts sorted.
    print(pts)
    print(all_neighbours(pts))
    sorted_pts = sorted_points(pts)
    print(sorted_pts)
    print(all_neighbours(sorted_pts))"""
    nb_pts = len(list_pts)
    neighbours = all_neighbours(list_pts)
    sorted_list = [list_pts[0], list_pts[neighbours[0][0]]]  # the first point and the closest neighbour
    i = 1
    ex_index = [0, neighbours[0][0]]
    # print('Sorted =', sorted_list)
    # print('Ex_ind =', ex_index)
    while i < nb_pts - 1:
        """We look the neighbours of the point."""
        # print('i =', i)
        if list_pts[neighbours[ex_index[i]][0]] == sorted_list[i - 1]:
            """If the closest neighbour is already on the sorted list, we add the other one."""
            sorted_list.append(list_pts[neighbours[ex_index[i]][1]])
            ex_index.append(neighbours[ex_index[i]][1])
        elif list_pts[neighbours[ex_index[i]][1]] == sorted_list[i - 1]:
            """If the other neighbour is already on the sorted list, we add the first one."""
            sorted_list.append(list_pts[neighbours[ex_index[i]][0]])
            ex_index.append(neighbours[ex_index[i]][0])
        else:
            print("Error sorted_point.")
        # print('Ex_ind =', ex_index)
        # print('Sorted =', sorted_list)
        i = i + 1
    return sorted_list


def rectangle_flight_plan(pt1, pt2, d, d_width=None):
    """Return a list of points in the rectangle {pt1, pt2} with a distance between 2 points of d in the length and
    d_with in the width.
    rectangle_fp = rectangle_flight_plan(pt1, pt2, 5, d_width=20)
    print(rectangle_fp)
    plot_pts(rectangle_fp, style='-.', color='r')"""
    d_length = d
    if d_width is None:
        d_width = d
    corners = [pt1, (pt1[0], pt2[1]), pt2, (pt2[0], pt1[1])]  # The 4 corners.
    fp = []
    if distance_in_meters(corners[0], corners[1]) > distance_in_meters(corners[0], corners[3]):
        length_points = stops_on_a_line(corners[0], corners[1], d_length)
        length_points_bis = stops_on_a_line(corners[3], corners[2], d_length)
    else:
        length_points = stops_on_a_line(corners[0], corners[3], d_length)
        length_points_bis = stops_on_a_line(corners[1], corners[2], d_length)
    i = 0
    while i < len(length_points):
        if i % 2 == 0:
            fp += stops_on_a_line(length_points[i], length_points_bis[i], d_width)
        else:
            fp += stops_on_a_line(length_points_bis[i], length_points[i], d_width)
        i += 1
        # print(i, 'ème étape, fp =', fp)
    return fp


def plot_pts(list_pts, style='solid', color="b", wait=False):
    """Function to plot graphs with a list of points."""
    x = []
    y = []
    for pt in list_pts:
        x.append(pt[0])  # longitude
        y.append(pt[1])  # latitude
    plt.plot(x, y, linestyle=style, color=color)
    if not wait:
        plt.show()


def point_on_with_x(pt1, pt2, x):
    """Return the point on the segment [pt1, pt2] with the abscissa x."""
    if not min(pt1[0], pt2[0]) < x < max(pt1[0], pt2[0]):
        print('No point with this abscissa on this segment.')
    m = (pt2[1] - pt1[1]) / (pt2[0] - pt1[0])
    b0 = pt1[1] - m * pt1[0]
    y = m * x + b0
    point = x, y
    return point


def point_on_with_vectors(O, u, v, pt1, pt2, x_on_ld):
    """O, P the 2 points from the longest distance segment. Pt1 and Pt2 the segment of the side. x the abscissa of
    the point on the longest distance."""
    # pt1_x, pt2_x = pt1[0], pt2[0]  # abscissas of the segment
    Opt1 = vect(O, pt1)
    Opt2 = vect(O, pt2)
    u_norm = math.sqrt(np.dot(u, u))
    print('u_norm : ', u_norm)
    print('u in meters :', distance_in_meters(O, add_vect(O, u)))
    fact = distance_in_meters(O, pt1) / distance_in_meters(O, add_vect(O, u))
    pt1_u = np.dot(Opt1, u) / u_norm**2
    pt2_u = np.dot(Opt2, u) / u_norm**2
    print('pt1_u : ', pt1_u)
    print('pt2_u : ', pt2_u)
    pt1_on_ld = add_vect(O, u, pt1_u)
    pt2_on_ld = add_vect(O, u, pt2_u)
    print('pt1 on ld :', pt1_on_ld)
    print('pt2 on ld :', pt2_on_ld)
    # plot_pts([O, pt1_on_ld, pt1, pt2_on_ld, pt2], color='y', wait=True)
    '''x_on_segment = pt1[0] + (x_on_ld - pt1_on_ld[0]) * (pt2[0] - pt1[0]) / (pt2_on_ld[0] - pt1_on_ld[0])  
    # y = y1 + (x-x1)(y2-y1)/(x2-x1)'''
    print('x on ld : ', x_on_ld)

    frac = (x_on_ld - pt1_on_ld[0]) / (pt2_on_ld[0] - pt1_on_ld[0])
    # distance_in_meters(pt1_on_ld, point_on_with_x(pt1_on_ld, pt2_on_ld, x_on_ld)) / distance_in_meters(pt1_on_ld, pt2_on_ld)
    x_on_segment = pt1[0] + frac * (pt2[0] - pt1[0])
    print(frac)
    print('x_on_seg:', x_on_segment)
    return point_on_with_x(pt1, pt2, x_on_segment)


def flight_plan(list_pts, d, d_width=None):
    d_length = d
    if d_width is None:
        d_width = d
    list_pts = sorted_points(list_pts)
    (x, stop), max_dist = longest_distance(list_pts)
    # vx, vy = vectorise(pt1, pt2, d_length, d_width=d_width)
    fp = [x]
    return fp


def vect(pt1, pt2):
    return pt2[0] - pt1[0], pt2[1] - pt1[1]


def vectorise(pt1, pt2, d, d_width=None):
    """ Return 2 vectors to form our grid."
    vx, vy = vectorise(pt1, pt2, 20, 5)
    print(vx, vy)
    plot_pts([add_vect(pt1, vx), add_vect(pt1, vy)], color='r')"""
    d_length = d
    if d_width is None:
        d_width = d
    d_max = distance_in_meters(pt1, pt2)
    # print('d_max =', d_max)
    # print('d_length =', d_length)
    # print('d_width =', d_width)
    dx = (pt2[0] - pt1[0])  # coord
    dy = (pt2[1] - pt1[1])  # coord
    norm = math.sqrt(dx ** 2 + dy ** 2)
    theta = math.atan(dy / dx)
    print('theta : ', theta)
    u = d_length * norm * math.cos(theta) / d_max, d_length * norm * math.sin(theta) / d_max
    v = d_width * norm * (- math.sin(theta)) / d_max, d_width * norm * math.cos(theta) / d_max
    return u, v


def add_vect(pt, vect, nb=1):
    ptx = pt[0]
    pty = pt[1]
    value_x = nb * vect[0]
    value_y = nb * vect[1]
    ptx = pt[0] + value_x
    pty = pt[1] + value_y
    # for i in range(0, nb):
    #     ptx += vect[0]
    #     pty += vect[1]
    return ptx, pty


# def create_flight_plan_old(list_points, dist):
#     polygon = Polygon(list_points)
#     points_out, dist_max = longest_distance(list_points)
#     pt2 = list_points[points_out[1]]
#     flight_plan = [pt1]
#     next_point = pt1
#     vx, vy = vectorise(pt1, pt2, dist)
#     while (next_point[1]-pt2[1])**2 + (next_point[0]-pt2[0])**2 > vx[1]**2 + vx[0]**2:  #distance_in_meters(next_point, pt2) > dist
#         while polygon.contains(Point(next_point)):
#             # next_point = next_point + vy
#             flight_plan.append(next_point)
#         # next_point = next_point + vx
#         # vy = (-vy[0], - vy[1])
#         # vy(1) = -vy(0), -vy(1)
#         flight_plan.append(next_point)
#     flight_plan.append(pt2)
#     return flight_plan


if __name__ == "__main__":
    """6 points of the drone lab in the EETAC in Castelldefels"""
    pts = [(41.275827, 1.987712), (41.276788, 1.987478), (41.275843, 1.988352),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.277231, 1.988347)]

    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, style=':', wait=True)

    (i_pt1, i_pt2), d_max = longest_distance(sorted_pts)
    print('Distance max : ', d_max)

    pt1, pt2 = sorted_pts[i_pt1], sorted_pts[i_pt2]
    print('pt1 & pt2 :', pt1, pt2)

    stops = stops_on_a_line(pt1, pt2, 25)
    plot_pts(stops, style=':', color='g', wait=True)

    u, v = vectorise(pt1, pt2, 10, 5)
    print('u & v :', u, v)
    plt.axis('equal')

    plot_pts([pt1, add_vect(pt1, u)], color='black', wait=True)
    plot_pts([pt1, add_vect(pt1, v)], color='black', wait=True)

    '''Test find on segment with vector'''

    pt_0, pt_1, pt_2 = sorted_pts[0], sorted_pts[1], sorted_pts[2]
    pt_3, pt_4 = sorted_pts[3], sorted_pts[4]
    print('abscissas', pt_1[0], pt_2[0])

    abscissa = 41.276200
    print('x =', abscissa)
    pt_on_longest_dist = point_on_with_x(pt1, pt2, abscissa)
    print('pt_long_dist :', pt_on_longest_dist)

    pt_on_segment_with_x = point_on_with_x(pt_1, pt_2, abscissa)
    print('pt_segment_with_x :', pt_on_segment_with_x)

    plot_pts([pt_on_longest_dist, pt_on_segment_with_x], color='r', wait=True)

    pt_on_segment_with_vect = point_on_with_vectors(pt1, u, v, pt_1, pt_2, abscissa)
    print('pt_segment_with_vect :', pt_on_segment_with_vect)

    plot_pts([pt_on_longest_dist, pt_on_segment_with_vect], color='r')

    # point_1 = 0, 0
    # point_on_with_vectors(pt1, u, v, pt_5, pt_4, 1.988434)
    # pt_on_seg_1 = point_on_with_x(pt_5, pt_4, x_1)

    # pt_1, pt_2 = sorted_pts[1], sorted_pts[2]  # ATTENTION changer les noms
    # point_2 = point_on_with_vectors(pt1, u, v, pt_1, pt_2, 1.988434)
    # pt_on_seg_2 = point_on_with_x(pt_1, pt_2, x_2)

    # pt_on_seg_0 = point_on_with_x(pt1, pt2, 1.988434)
    #
    # plot_pts([pt_on_seg_0, point_1], color='gray')
