import math
import numpy as np
from geopy import distance
from matplotlib import pyplot as plt


def distance_in_meters(point_1, point_2):
    """ Return the distance in meters between pt1 and pt2."""
    '''wellington = (-41.32, 174.81)
    salamanca = (40.96, -5.50)
    print(distance.distance(wellington, salamanca).km)'''
    return distance.distance(point_1, point_2).m


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


def angle_BAC(point_A, point_B, point_C):
    """Return the angle BAC. Using the cos theorem (c²=a²+b²-2.a.b.cos(alpha))."""
    if point_A == point_B or point_A == point_C or point_B == point_C:
        return 0
    a = distance_in_meters(point_B, point_C)
    # math.sqrt((point_C[0] - point_B[0]) ** 2 + (point_C[1] - point_B[1]) ** 2)
    b = distance_in_meters(point_A, point_C)
    # = math.sqrt((point_A[0] - point_C[0]) ** 2 + (point_A[1] - point_C[1]) ** 2)
    c = distance_in_meters(point_B, point_A)
    # math.sqrt((point_B[0] - point_A[0]) ** 2 + (point_B[1] - point_A[1]) ** 2)
    alpha = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c))
    return alpha


def neighbours_of(ind_pts, list_pts):
    if len(list_pts) <= 2:
        return 'No neighbours'
    two_neighbours = [0, 1]
    angle_neighbours = angle_BAC(list_pts[ind_pts], list_pts[two_neighbours[0]], list_pts[two_neighbours[1]])
    for i in range(len(list_pts)):
        '''We're searching for the greatest angle. To have one certain neighbour.'''
        for j in range(len(list_pts)):
            angle = angle_BAC(list_pts[ind_pts], list_pts[i], list_pts[j])
            if angle > angle_neighbours:
                angle_neighbours = angle
                two_neighbours = [i, j]
    vectorial_product = (list_pts[two_neighbours[1]][0] - list_pts[ind_pts][0]) * \
                        (list_pts[two_neighbours[0]][1] - list_pts[ind_pts][1]) - \
                        (list_pts[two_neighbours[1]][1] - list_pts[ind_pts][1]) * \
                        (list_pts[two_neighbours[0]][0] - list_pts[ind_pts][0])
    if vectorial_product > 0:
        two_neighbours[0], two_neighbours[1] = two_neighbours[1], two_neighbours[0]
    return two_neighbours


def all_neighbours(list_pts):
    neighbours = []
    for i in range(len(list_pts)):
        neighbours.append(neighbours_of(i, list_pts))
    return neighbours


def sorted_points(list_pts):
    """Return the list_pts sorted. Rotational sorting."""
    '''pts = [(41.275827, 1.987712), (41.277231, 1.988347), (41.275716, 1.988816),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.276788, 1.987478)]  #
    for i, point in enumerate(pts):
        plt.text(point[0], point[1], str(i))
    plt.axis('equal')
    plot_pts(pts, style='-', color='y', wait=True)
    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, style=':', color='b', wait=True)'''
    nb_pts = len(list_pts)
    neighbours = all_neighbours(list_pts)
    sorted_list = [list_pts[0], list_pts[neighbours[0][0]]]  # the first point and the closest neighbour
    i = 1
    ex_index = [0, neighbours[0][0]]
    # print('Sorted =', sorted_list)
    # print('Ex_ind =', ex_index)
    while i < nb_pts - 1:
        """We look the neighbours of the point."""
        ex_index.append(neighbours[ex_index[i]][0])
        sorted_list.append(list_pts[ex_index[i + 1]])
        # print('Ex_ind =', ex_index)
        # print('Sorted =', sorted_list)
        i = i + 1
    return sorted_list


def rectangle_flight_plan(point_1, point_2, d, d_width=None):
    """Return two lists of points in the rectangle {pt1, pt2}. First is the flight plan with only the extremity. And
    the second is the list of stops point. The distance between 2 points is d in the length and d_with in the
    width."""
    '''Test : 
    pts = [(41.275827, 1.987712), (41.276788, 1.987478), (41.275843, 1.988352),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.277231, 1.988347)]

    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, style=':', wait=True)

    pt_0, pt_1, pt_2 = sorted_pts[0], sorted_pts[1], sorted_pts[2]
    pt_3, pt_4 = sorted_pts[3], sorted_pts[4]

    fp_points, stops_points = rectangle_flight_plan(pt_1, pt_3, 20, 10)

    print('Number of points in the flight plan : ', len(fp_points), '\nNumber of stops points : ', len(stops_points))

    plot_pts(fp_points, style='-', color='r', wait=True)
    plot_pts(stops_points, style='--', color='g', wait=False)'''
    d_length = d
    if d_width is None:
        d_width = d
    corners = [point_1, (point_1[0], point_2[1]), point_2, (point_2[0], point_1[1])]  # The 4 corners.
    flight_points = []
    stops = []
    if distance_in_meters(corners[0], corners[1]) > distance_in_meters(corners[0], corners[3]):

        length_points = stops_on_a_line(corners[0], corners[1], d_length)
        length_points_bis = stops_on_a_line(corners[3], corners[2], d_length)
    else:
        length_points = stops_on_a_line(corners[0], corners[3], d_length)
        length_points_bis = stops_on_a_line(corners[1], corners[2], d_length)
    i = 0
    while i < len(length_points):
        if i % 2 == 0:
            stops += stops_on_a_line(length_points[i], length_points_bis[i], d_width)
            flight_points.append(length_points[i])
            flight_points.append(length_points_bis[i])
        else:
            stops += stops_on_a_line(length_points_bis[i], length_points[i], d_width)
            flight_points.append(length_points_bis[i])
            flight_points.append(length_points[i])
        i += 1
        # print(i, 'rd step, fp =', fp)
    return flight_points, stops


def longest_distance(list_pts):
    """Longest distance between two points. Return the 2 points and the distance."""
    mat_dist = matrix_of_distances(list_pts)
    longest_dist = np.max(mat_dist)
    np_index = np.where(mat_dist == longest_dist)[0]
    points = np_index.tolist()
    return points, longest_dist


def stops_on_a_line(point_1, point_2, dist):
    """Calculate points on a line between pt1 and pt2 with a distance of dist between each stop. From pt1 to pt2."""
    '''
    pts = [(41.275827, 1.987712), (41.276788, 1.987478), (41.275843, 1.988352),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.277231, 1.988347)]

    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, style=':', wait=True)

    (i_pt1, i_pt2), d_max = longest_distance(sorted_pts)

    pt1, pt2 = sorted_pts[i_pt1], sorted_pts[i_pt2]

    stops = stops_on_a_line(pt1, pt2, 25)
    plot_pts(stops, style=':', color='g', wait=False)'''
    stops = [point_1]
    if point_1 != point_2:
        dist_between_points = distance_in_meters(point_1, point_2)
        number_of_stops = math.ceil(dist_between_points / dist)
        # print(number_of_stops)
        delta_latitude = (point_2[0] - point_1[0]) / number_of_stops
        delta_longitude = (point_2[1] - point_1[1]) / number_of_stops
        for i in range(1, number_of_stops):
            stops.append((point_1[0] + i * delta_latitude, point_1[1] + i * delta_longitude))
        stops.append(point_2)
    return stops


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


def point_on_with_x(point_1, point_2, x):
    """Return the point on the segment [pt1, pt2] with the abscissa x."""
    on_this_segment = True
    if not min(point_1[0], point_2[0]) < x < max(point_1[0], point_2[0]):
        on_this_segment = False
        # print('No point with this abscissa on this segment.')
    m = (point_2[1] - point_1[1]) / (point_2[0] - point_1[0])
    b0 = point_1[1] - m * point_1[0]
    y = m * x + b0
    point = x, y
    # print(on_this_segment)
    return on_this_segment, point


def point_on_with_vectors(point_0, vect_u, point_1, point_2, x_on_ld):
    """O, P the 2 points from the longest distance segment. Pt1 and Pt2 the segment of the side. x the abscissa of
    the point on the longest distance."""
    '''Example : 
    pts = [(41.275827, 1.987712), (41.276788, 1.987478), (41.275843, 1.988352),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.277231, 1.988347)]

    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, style=':', wait=True)

    (i_pt1, i_pt2), d_max = longest_distance(sorted_pts)
    print('Distance max : ', d_max)

    pt1, pt2 = sorted_pts[i_pt1], sorted_pts[i_pt2]
    print('pt1 & pt2 :', pt1, pt2)

    plot_pts([pt1, pt2], style=':', color='g', wait=True)

    pt_0, pt_1, pt_2, pt_3, pt_4 = sorted_pts[0], sorted_pts[1], sorted_pts[2], sorted_pts[3], sorted_pts[4]

    u, v = vectorise(pt1, pt2, 10, 20)

    plt.axis('equal')

    print('abscissas', pt_1[0], pt_2[0])

    abscissa = 41.276200  # 41.276200
    print('x =', abscissa)

    pt_on_longest_dist = point_on_with_x(pt1, pt2, abscissa)[1]
    print('pt_long_dist :', pt_on_longest_dist)

    pt_on_segment_with_x = point_on_with_x(pt_1, pt_2, abscissa)[1]
    print('pt_segment_with_x :', pt_on_segment_with_x)

    plot_pts([pt_on_longest_dist, pt_on_segment_with_x], color='r', wait=True)

    pt_on_segment_with_vect = point_on_with_vectors(pt1, u, pt_1, pt_2, abscissa)[1]
    print('pt_segment_with_vect :', pt_on_segment_with_vect)

    plot_pts([pt_on_longest_dist, pt_on_segment_with_vect], color='r', wait=True)'''
    'Creation of the segments [pt0, pt1] and [pt0, pt2].'
    seg_pt0_pt1 = vect(point_0, point_1)
    seg_pt0_pt2 = vect(point_0, point_2)
    'Definition of the norm of the vector of the plan.'
    u_norm = math.sqrt(np.dot(vect_u, vect_u))
    'Proportion of the distance of the segment on the scalar product with the vector, with the norm of the vector.'
    pt1_u = np.dot(seg_pt0_pt1, vect_u) / u_norm ** 2
    pt2_u = np.dot(seg_pt0_pt2, vect_u) / u_norm ** 2
    'Creation of orthogonal projection point of pt1 and pt2.'
    pt1_on_ld = add_vect(point_0, vect_u, pt1_u)
    pt2_on_ld = add_vect(point_0, vect_u, pt2_u)  # plot_pts([O, pt1_on_ld, pt1, pt2_on_ld, pt2], color='y', wait=True)
    'Use of this relation : y = y1 + (x-x1)(y2-y1)/(x2-x1).'
    if pt2_on_ld[0] - pt1_on_ld[0] != 0:
        directing_coefficient = (x_on_ld - pt1_on_ld[0]) / (pt2_on_ld[0] - pt1_on_ld[0])
    else:
        directing_coefficient = np.inf
    # directing_coefficient = (x_on_ld - pt1_on_ld[0]) / (pt2_on_ld[0] - pt1_on_ld[0])
    x_on_segment = point_1[0] + directing_coefficient * (point_2[0] - point_1[0])
    return point_on_with_x(point_1, point_2, x_on_segment)


def vect(point_1, point_2):
    return point_2[0] - point_1[0], point_2[1] - point_1[1]


def vectorise(point_1, point_2, d, d_width=None):
    """Return 2 vectors, u and v to form our orthogonal grid."""
    '''
    pts = [(41.275827, 1.987712), (41.276788, 1.987478), (41.275843, 1.988352),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.277231, 1.988347)]

    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, style=':', wait=True)

    (i_pt1, i_pt2), d_max = longest_distance(sorted_pts)

    pt1, pt2 = sorted_pts[i_pt1], sorted_pts[i_pt2]

    u, v = vectorise(pt1, pt2, 10, 5)
    print('u & v :', u, v)
    plt.axis('equal')

    plot_pts([pt1, add_vect(pt1, u)], color='black', wait=True)
    plot_pts([pt1, add_vect(pt1, v)], color='black', wait=False)'''
    d_length = d
    if d_width is None:
        d_width = d
    distance_max = distance_in_meters(point_1, point_2)
    # print('d_max =', d_max)
    # print('d_length =', d_length)
    # print('d_width =', d_width)
    dx = (point_2[0] - point_1[0])
    dy = (point_2[1] - point_1[1])
    norm = math.sqrt(dx ** 2 + dy ** 2)
    theta = math.atan(dy / dx)
    # print('theta : ', theta)
    vect_u = d_length * norm * math.cos(theta) / distance_max, d_length * norm * math.sin(theta) / distance_max
    vect_v = d_width * norm * (- math.sin(theta)) / distance_max, d_width * norm * math.cos(theta) / distance_max
    return vect_u, vect_v


def add_vect(pt, vector, nb=1):
    """Return the point. After having added nb times the vector."""
    value_x = nb * vector[0]
    value_y = nb * vector[1]
    ptx = pt[0] + value_x
    pty = pt[1] + value_y
    # for i in range(0, nb):
    #     ptx += vect[0]
    #     pty += vect[1]
    return ptx, pty


def create_flight_plan(list_pts_unsorted, d, d_width=None):
    """Return two lists, the first one with the different points of the flight plan and the second is the list of all
    stops needed for the completed photo."""
    '''Example :
    pts = [(41.275827, 1.987712), (41.276788, 1.987478), (41.275843, 1.988352),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.277231, 1.988347)]

    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, style=':', wait=True)

    plt.axis('equal')

    fp_points, stops_points = create_flight_plan(pts, 5, 10)
    print('create_flight_plan() :', len(fp_points), len(stops_points))

    plot_pts(fp_points, style='-', color='r', wait=True)
    plot_pts(stops_points, style='--', color='g', wait=False)'''
    d_length = d
    if d_width is None:
        d_width = d
    list_pts = sorted_points(list_pts_unsorted)
    neighbours = all_neighbours(list_pts)
    (start, stop), max_dist = longest_distance(list_pts)
    first_point = list_pts[start]
    last_point = list_pts[stop]
    vect_u, vect_v = vectorise(first_point, last_point, d, d_width)
    up_segment = start, neighbours[start][0]
    down_segment = start, neighbours[start][1]
    flight_points = [first_point]
    stops = [first_point]
    for i in range(1, math.ceil(max_dist / d_length)):
        x = add_vect(first_point, vect_u, i)[0]
        up_on, point_up = point_on_with_vectors(first_point, vect_u,
                                                list_pts[up_segment[0]], list_pts[up_segment[1]], x)
        down_on, point_down = point_on_with_vectors(first_point, vect_u,
                                                    list_pts[down_segment[0]], list_pts[down_segment[1]], x)
        # print('Loop step on_up : ', up_on)
        if not up_on:
            '''If the point isn't  on the side of the area. We need to change the up_segment.'''
            # print('In the loop because False')
            a, b = up_segment
            if neighbours[b][0] == a:
                # print('if')
                up_next_neighbour = neighbours[b][1]
            else:
                # print('else')
                up_next_neighbour = neighbours[b][0]
            up_segment = b, up_next_neighbour
            up_on, point_up = point_on_with_vectors(first_point, vect_u,
                                                    list_pts[up_segment[0]], list_pts[up_segment[1]], x)
            # print('Test step on_up : ', up_on)
        if not down_on:
            '''If the point isn't on the side of the area. We need to change the down_segment.'''
            a, b = down_segment
            if neighbours[b][0] == a:
                down_next_neighbour = neighbours[b][1]
            else:
                down_next_neighbour = neighbours[b][0]
            down_segment = b, down_next_neighbour
            down_on, point_down = point_on_with_vectors(first_point, vect_u,
                                                        list_pts[down_segment[0]], list_pts[down_segment[1]], x)
        if i % 2 == 0:
            stops += stops_on_a_line(point_up, point_down, d_width)
            flight_points.append(point_up)
            flight_points.append(point_down)
        else:
            stops += stops_on_a_line(point_down, point_up, d_width)
            flight_points.append(point_down)
            flight_points.append(point_up)
    flight_points.append(list_pts[stop])
    stops.append(list_pts[stop])
    return flight_points, stops


if __name__ == "__main__":
    """6 points of the drone lab in the EETAC in Castelldefels"""
    pts = [(41.275827, 1.987712), (41.277231, 1.988347), (41.275716, 1.988816),
           (41.276965, 1.989399), (41.276264, 1.989522), (41.276788, 1.987478)]  #

    for i, point in enumerate(pts):
        plt.text(point[0], point[1], str(i))

    plt.axis('equal')

    print('Neighbours unsorted list : \n', all_neighbours(pts))

    plot_pts(pts, style='-', color='y', wait=True)

    sorted_pts = sorted_points(pts)
    print('Sorted list of points : \n', sorted_pts)
    print('Neighbours sorted list : \n', all_neighbours(sorted_pts))

    plot_pts(sorted_pts, style=':', color='b', wait=True)

    (i_pt1, i_pt2), d_max = longest_distance(sorted_pts)

    pt1, pt2 = sorted_pts[i_pt1], sorted_pts[i_pt2]

    stops = stops_on_a_line(pt1, pt2, 25)
    plot_pts(stops, style=':', color='g', wait=True)

    fp_points, stops_points = create_flight_plan(pts, 15, 30)
    print('Number of points in the flight plan :', len(fp_points),
          '\nNumber of points in the stops point list : ', len(stops_points))

    plot_pts(fp_points, style='-', color='r', wait=True)
    plot_pts(stops_points, style='--', color='g', wait=False)
