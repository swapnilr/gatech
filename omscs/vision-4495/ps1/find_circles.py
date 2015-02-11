from hough_circles_acc import hough_circles_acc2
from hough_peaks import hough_peaks2
from Queue import PriorityQueue

#def find_circles(BW, radius_range):
#    for radius in radius_range:
#        hough_circles_acc(radius)
#        Do something with the output 

def find_circles(BW, edges, radius_range):
    # % Find circles in given radius range using Hough transform.
    # %
    # % BW: Binary (black and white) image containing edge pixels
    # % radius_range: Range of circle radii [min max] to look for, in pixels
                     
    # % TODO: Your code here

    optima = PriorityQueue()
    for radius in radius_range:
        print radius
        H = hough_circles_acc2(BW, edges, radius)
        peaks = hough_peaks2(H, 10)[1]
        while not peaks.empty():
            val, loc = peaks.get()
            optima.put((val, (loc, radius)))
    centers = 0;
    radii = 0;
                                    
    return optima #centers, radii
