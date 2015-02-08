import numpy as np
import math

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
        min_row = max(peak_location[0] - int(NHoodSize[0]), 0)
        max_row = min(peak_location[0] + int(NHoodSize[0]) + 1, H.shape[0])
        min_col = max(peak_location[1] - int(NHoodSize[1]), 0)
        max_col = min(peak_location[1] + int(NHoodSize[1]) + 1, H.shape[1])
        for row in range(min_row, max_row):
            for col in range(min_col, max_col):
                H_copy[row][col] = 0
    #  find max
    #  if max < threshold: break
    #  add peak to peaks array
    #  0 everything around found peak in neighborhood
    peaks = np.array(peaks)  # placeholder
    return peaks
