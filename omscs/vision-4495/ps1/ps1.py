# % ps1
import cv2
from find_circles import find_circles
from hough_circles_acc import hough_circles_acc
from hough_peaks import hough_peaks
from hough_lines_acc import hough_lines_acc
from hough_lines_draw import hough_lines_draw

# %% 1-a
img = cv2.imread('input\ps1-input0.png', cv2.IMREAD_UNCHANGED)  # already grayscale
# %% TODO: Compute edge image img_edges
cv2.imwrite('output\ps1-1-a-1.png', img_edges) # save as output/ps1-1-a-1.png

# %% 2-a
(H, theta, rho) = hough_lines_acc(img_edges);  # defined in hough_lines_acc.py
# %% TODO: Plot/show accumulator array H, save as output/ps1-2-a-1.png

# %% 2-b
peaks = hough_peaks(H, 10);  # defined in hough_peaks.py
# %% TODO: Highlight peak locations on accumulator array, save as output/ps1-2-b-1.png

# %% TODO: Rest of your code here
