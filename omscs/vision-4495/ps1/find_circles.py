from hough_circles_acc import hough_circles_acc
from hough_peaks import sorted_hough_peaks
from Queue import PriorityQueue
import math

def find_circles(BW, radius_range, numCircles=10):
    optima = PriorityQueue()
    for radius in radius_range:
        print "Trying radius %d" % radius
        H = hough_circles_acc(BW, radius)
        peaks = sorted_hough_peaks(H)
        while not peaks.empty():
            val, loc = peaks.get()
            optima.put((val, (loc, radius)))
    centers = []
    radii =[]

    i = 0
    while i < numCircles:
        if optima.empty():
            break
        center, radius = optima.get()[1]
        isValid = True
        for point in centers:
            if dist(point, center) < radius_range[0]:
                isValid = False
                break
        if not isValid:
            continue
        i += 1
        centers.append(center)
        radii.append(radius)
    return centers, radii


def dist(pos1, pos2):
    y0, x0 = pos1
    y1, x1 = pos2
    return math.sqrt((y1-y0)**2 + (x1-x0)**2)
