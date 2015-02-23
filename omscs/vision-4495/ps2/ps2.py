# ps2
import os
import numpy as np
import cv2
import time
## 1-a
# Read images
L = cv2.imread(os.path.join('input', 'pair0-L.png'), 0) * (1.0 / 255.0)  # grayscale, [0, 1]
R = cv2.imread(os.path.join('input', 'pair0-R.png'), 0) * (1.0 / 255.0)

# Compute disparity (using method disparity_ssd defined in disparity_ssd.py)
from disparity_ssd import disparity_ssd
D_L = disparity_ssd(L, R)
D_R = disparity_ssd(R, L)
print np.amax(D_L), np.amax(D_R)
#cv2.imshow("L", D_R*(1.0)/np.max(D_R))
#time.sleep(30)

from disparity_ncorr import disparity_ncorr
Dn_L = disparity_ncorr(L, R)
Dn_R = disparity_ncorr(R, L)
print np.amax(D_L), np.amax(D_R)
#cv2.imshow("L", D_R*(1.0)/np.max(D_R))

# TODO: Save output images (D_L as output/ps2-1-a-1.png and D_R as output/ps2-1-a-2.png)
# Note: They may need to be scaled/shifted before saving to show results properly

# TODO: Rest of your code here
