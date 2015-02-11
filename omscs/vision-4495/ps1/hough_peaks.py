import numpy as np
import math
from Queue import PriorityQueue

def hough_peaks(H, numpeaks=1, Threshold=None, NHoodSize=None):
    if Threshold is None:
        Threshold = 0.5 * np.amax(H)
    if NHoodSize is None:
        NHoodSize = np.floor(np.asarray(H.shape) / 100.0) * 2 + 1
    H_copy = H.copy()
    # TODO: Compute peaks: Qx2 array with row, col indices of peaks
    # from i to number of peaks:
    peaks = []
    for i in range(numpeaks):
        peak_location = np.unravel_index(np.argmax(H_copy), H_copy.shape)
        peak = H_copy[peak_location]
        if peak < Threshold:
            break
        peaks.append(peak_location)
        min_row = max(peak_location[0] - int(NHoodSize[0]/2.0), 0)
        max_row = min(peak_location[0] + int(NHoodSize[0]/2.0) + 1, H.shape[0])
        min_col = max(peak_location[1] - int(NHoodSize[1]/2.0), 0)
        max_col = min(peak_location[1] + int(NHoodSize[1]/2.0) + 1, H.shape[1])
        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                H_copy[row, col] = 0
    peaks = np.array(peaks)
    return peaks

def hough_peaks2(H, numpeaks=1, Threshold=None, NHoodSize=None):
    if Threshold is None:
        Threshold = 0.5 * np.amax(H)
    height, width = H.shape
    # Find local optima
    optima = PriorityQueue()
    for y in range(height):
        for x in range(width):
            val = H[y][x]
            y_cond = (y < height - 1 and val > H[y+1][x]) and (y > 0 and val > H[y-1][x]) 
            x_cond = (x < width - 1 and val > H[y][x+1]) and (x > 0 and val > H[y][x-1])
            if val > Threshold and y_cond and x_cond:
                optima.put((-val, (y,x)))
    optimaList = []
    #for i in range(numpeaks):
    #    if optima.empty():
    #        break
    #    optimaList.append(optima.get()[1])
    return optimaList, optima
