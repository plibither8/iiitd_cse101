"""
CSE101: Introduction to Programming
Assignment 3

Name        : Mihir Chaturvedi
Roll-no     : 2019061
"""



import math
import random



def dist(p1, p2):
    """
    Find the euclidean distance between two 2-D points

    Args:
        p1: (p1_x, p1_y)
        p2: (p2_x, p2_y)

    Returns:
        Euclidean distance between p1 and p2
    """

    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

def sort_points_by_X(points):
    """
    Sort a list of points by their X coordinate

    Args:
        points: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]

    Returns:
        List of points sorted by X coordinate
    """

    return sorted(points, key = lambda p: p[0])



def sort_points_by_Y(points):
    """
    Sort a list of points by their Y coordinate

    Args:
        points: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]

    Returns:
        List of points sorted by Y coordinate
    """

    return sorted(points, key = lambda p: p[1])



def naive_closest_pair(plane):
    """
    Find the closest pair of points in the plane using the brute
    force approach

    Args:
        plane: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]

    Returns:
        Distance between closest pair of points and closest pair
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """

    closest_dist = float('inf')
    closest_pair = []

    number_of_points = len(plane)

    for i in range(number_of_points):
        for j in range(i + 1, number_of_points):
            current_dist = dist(plane[i], plane[j])
            if current_dist < closest_dist:
                closest_dist = current_dist
                closest_pair = [plane[i], plane[j]]

    return [closest_dist, *closest_pair]

closest_points = []

def closest_pair_in_strip(points, d):
    """
    Find the closest pair of points in the given strip with a
    given upper bound. This function is called by
    efficient_closest_pair_routine

    Args:
        points: List of points in the strip of interest.
        d: Minimum distance already found found by
            efficient_closest_pair_routine

    Returns:
        Distance between closest pair of points and closest pair
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)] if
        distance between p1 and p2 is less than d. Otherwise
        return -1.
    """

    global closest_points
    points = sort_points_by_Y(points)
    min_found = False

    for i in range(len(points)):
        point1 = points[i]

        for point2 in points[i + 1 : i + 6]:
            current_dist = dist(point1, point2)

            if (current_dist < d):
                d = current_dist
                closest_points = [point1, point2]
                min_found = True

    return [d, *closest_points] if min_found else -1


def efficient_closest_pair_routine(points):
    """
    This routine calls itself recursivly to find the closest pair of
    points in the plane.

    Args:
        points: List of points sorted by X coordinate

    Returns:
        Distance between closest pair of points and closest pair
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """

    if len(points) is 2:
        return [dist(*points), *points]

    inflectionPointIndex = len(points) // 2
    inflectionPoint = points[inflectionPointIndex]

    s1 = points[0:inflectionPointIndex]
    s2 = points[inflectionPointIndex:]

    s1_closest = efficient_closest_pair_routine(s1) if len(s1) > 1 else [float('inf'), *s1]
    s2_closest = efficient_closest_pair_routine(s2)

    global closest_points
    d, p1, p2 = sorted([s1_closest, s2_closest], key = lambda s: s[0])[0]
    closest_points = [p1, p2]

    strip_points = list(filter(lambda point: abs(point[0] - inflectionPoint[0]) <= d, points))
    return closest_pair_in_strip(strip_points, d)


def efficient_closest_pair(points):
    """
    Find the closest pair of points in the plane using the divide
    and conquer approach by calling efficient_closest_pair_routine.

    Args:
        plane: List of points [(p1_x, p1_y), (p2_x, p2_y), ...]

    Returns:
        Distance between closest pair of points and closest pair
        of points: [dist_bw_p1_p2, (p1_x, p1_y), (p2_x, p2_y)]
    """

    points = sort_points_by_X(points)
    return efficient_closest_pair_routine(points)



def generate_plane(plane_size, num_pts):
    """
    Function to generate random points.

    Args:
        plane_size: Size of plane (X_max, Y_max)
        num_pts: Number of points to generate

    Returns:
        List of random points: [(p1_x, p1_y), (p2_x, p2_y), ...]
    """

    gen = random.sample(range(plane_size[0] * plane_size[1]), num_pts)
    random_points = [(i % plane_size[0] + 1, i // plane_size[1] + 1) for i in gen]

    return random_points



if __name__ == "__main__":
    #number of points to generate
    num_pts = 10
    #size of plane for generation of points
    plane_size = (10, 10)
    plane = generate_plane(plane_size, num_pts)
    naive_closest_pair(plane)
    efficient_closest_pair(plane)
