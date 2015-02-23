import numpy as np
import cv2

def disparity_ssd(L, R):
    """Compute disparity map D(y, x) such that: L(y, x) = R(y, x + D(y, x))
    
    Params:
    L: Grayscale left image
    R: Grayscale right image, same size as L

    Returns: Disparity map, same size as L, R
    """
    rows, columns = L.shape
    DSI = np.zeros((rows, columns, columns))
    boxsize = 5
    im_filter = np.ones((boxsize, boxsize)) / (boxsize * boxsize)
    for d in range(0, columns):
        rshift = np.roll(R, -d , axis = 1)
        #rshift = np.pad(R, ((0,0), (0,d)), mode='symmetric')[:,d:]
        diff = np.subtract(L, rshift)
        diff = np.power(diff, 2)
        ssd = cv2.filter2D(diff, ddepth=-1, kernel=im_filter)
        DSI[:,:,d] = ssd
    D = np.argmin(DSI, axis=2)
    for y in range(rows):
        for x in range(columns):
            if D[y,x] + x > columns:
                D[y,x] = D[y,x] - columns
    return D
