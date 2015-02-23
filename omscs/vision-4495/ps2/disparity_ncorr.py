import numpy as np
import cv2

def disparity_ncorr(L, R):
    """Compute disparity map D(y, x) such that: L(y, x) = R(y, x + D(y, x))
    
    Params:
    L: Grayscale left image
    R: Grayscale right image, same size as L

    Returns: Disparity map, same size as L, R
    """
    rows, columns = L.shape
    DSI = np.zeros((rows, columns, columns))
    boxsize = 5
    im_filter = np.ones((boxsize, boxsize)) #/ (boxsize * boxsize)
    #s = np.sqrt((L*L) * (R*R))
    for d in range(0, columns):
        rshift = np.roll(R, -d, axis = 1)
        Rtx = cv2.filter2D(L * rshift, ddepth=-1, kernel=im_filter)
        Rxx = cv2.filter2D(L * L, ddepth=-1, kernel=im_filter)
        Rtt = cv2.filter2D(rshift * rshift, ddepth=-1, kernel=im_filter)
        mult = Rtx / np.sqrt(Rxx * Rtt) 
        #ncorr = cv2.filter2D(mult, ddepth=-1, kernel=im_filter)
        DSI[:,:,d] = mult #ncorr #cv2.filter2D(Rxx * Rtt, ddepth=-1, kernel=im_filter))
    D = np.argmax(DSI, axis=2)
    for y in range(rows):
        for x in range(columns):
            if D[y,x] + x > columns:
                D[y,x] = D[y,x] - columns
    print D.shape
    return D
