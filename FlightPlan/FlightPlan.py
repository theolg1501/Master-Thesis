import math
import numpy as np
from geopy import distance
from matplotlib import pyplot as plt
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def distance_in_meters(pt1, pt2):
    """
    wellington = (-41.32, 174.81)
    salamanca = (40.96, -5.50)
    print(distance.distance(wellington, salamanca).km)"""
    return distance.distance(pt1, pt2).m


def distance_from_all(ind_pts, list_pts):
    dist_from_all = []
    for i in range(len(list_pts)):
        dist_from_all.append(distance_in_meters(list_pts[ind_pts], list_pts[i]))
    return dist_from_all


def matrices_of_distances(list_pts):
    mat = []
    for i in range(len(list_pts)):
        mat.append(distance_from_all(i, list_pts))
    return mat


def neighbours_of(ind_pts, list_pts):
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
    mat_dist = matrices_of_distances(list_pts)
    longest_dist = np.max(mat_dist)
    np_index = np.where(mat_dist == longest_dist)[0]
    points = np_index.tolist()
    return points, longest_dist


def stops_on_a_line(pt1, pt2, dist):
    """Calculate points on a line between pt1 and pt2 with a distance of dist between each stop. From pt1 to pt2
    stops = stops_on_a_line(pts[1], pts[2], 25)
    print(stops)"""
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


def plot_pts(list_pts, style='solid', color="b", wait=False):
    x = []
    y = []
    for pt in list_pts:
        x.append(pt[0])
        y.append(pt[1])
    plt.plot(x, y, linestyle=style, color=color)
    if not wait:
        plt.show()


def vectorise(pt1, pt2, dist):
    max_dist = distance_in_meters(pt1, pt2)
    vx_lat = dist * (pt2[0] - pt1[0]) / max_dist
    vx_long = dist * (pt2[1] - pt1[1]) / max_dist
    vx = [vx_lat, vx_long]
    vy_lat = - vx_long
    vy_long = vx_lat
    vy = [vy_lat, vy_long]
    return tuple(vx), tuple(vy)


def create_flight_plan(list_points, dist):
    polygon = Polygon(list_points)
    points_out, dist_max = longest_distance(list_points)
    pt1 = list_points[points_out[0]]
    pt2 = list_points[points_out[1]]
    flight_plan = [pt1]
    next_point = pt1
    vx, vy = vectorise(pt1, pt2, dist)
    while (next_point[1]-pt2[1])**2 + (next_point[0]-pt2[0])**2 > vx[1]**2 + vx[0]**2:  #distance_in_meters(next_point, pt2) > dist
        while polygon.contains(Point(next_point)):
            # next_point = next_point + vy
            flight_plan.append(next_point)
        # next_point = next_point + vx
        # vy = (-vy[0], - vy[1])
        # vy(1) = -vy(0), -vy(1)
        flight_plan.append(next_point)
    flight_plan.append(pt2)
    return flight_plan


if __name__ == "__main__":
    """6 points of the drone lab in the EETAC in Castelldefels"""
    pts = [(41.276788, 1.987478), (41.275723, 1.988664), (41.276965, 1.989399),
           (41.276264, 1.989522), (41.277231, 1.988347), (41.276098, 1.987644)]

    sorted_pts = sorted_points(pts)
    plot_pts(sorted_pts, wait=True)

    fp = create_flight_plan(sorted_pts, 15)
    plot_pts(fp, style='.', color='r')
    # stops = stops_on_a_line(sorted_pts[1], sorted_pts[3], 5)
    # plot_pts(stops, style='-', color='r')

    # print(vectorise(sorted_pts[0], sorted_pts[4], 5))

    # print(np.dot(vectorise(sorted_pts[0], sorted_pts[4], 5)[0], vectorise(sorted_pts[0], sorted_pts[4], 5)[1]))

    # point = Point(stops[3])
    # polygon = Polygon(pts)
    # print(polygon.contains(point))

    """Test :
    neighbours_of()
    print(distance_from_all(2, points_test))
    print(neighbours_of(2, points_test))
    
    print(all_neighbours(points_test))
    
    print(longest_distance(points_test))
    """
