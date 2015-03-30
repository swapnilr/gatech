import cv2
import numpy as np
THRESHOLD = 100 
BLUR_SIZE = 5
FILTER_SIZE = 17
def lk_flow(image1, image2):
    """
    image1, image2 expected as float matrices scaled to [0.0, 1.0]

    returns U,V as float matrics
    """
    image1 = cv2.GaussianBlur(image1, (BLUR_SIZE, BLUR_SIZE), 0)
    image2 = cv2.GaussianBlur(image2, (BLUR_SIZE, BLUR_SIZE), 0)

    It = image2 - image1
    Ix = cv2.Sobel(image1, cv2.CV_32F, 1, 0)
    Iy = cv2.Sobel(image1, cv2.CV_32F, 0, 1)
    Ix2 = Ix * Ix
    Iy2 = Iy * Iy
    Ixy = Ix * Iy
    Ixt = Ix * It
    Iyt = Iy * It

    Ix2 = cv2.boxFilter(Ix2, cv2.CV_32F, (FILTER_SIZE, FILTER_SIZE))
    Iy2 = cv2.boxFilter(Iy2, cv2.CV_32F, (FILTER_SIZE, FILTER_SIZE))
    Ixy = cv2.boxFilter(Ixy, cv2.CV_32F, (FILTER_SIZE, FILTER_SIZE))
    Ixt = cv2.boxFilter(Ixt, cv2.CV_32F, (FILTER_SIZE, FILTER_SIZE))
    Iyt = cv2.boxFilter(Iyt, cv2.CV_32F, (FILTER_SIZE, FILTER_SIZE))

    rows, columns = image1.shape

    U = np.zeros((rows, columns), dtype=np.float32)
    V = np.zeros((rows, columns), dtype=np.float32)

    A = np.zeros((2,2))
    b = np.zeros((2,1))

    for y in range(rows):
        for x in range(columns):
            A[0,0] = Ix2[y,x]
            A[0,1] = Ixy[y,x]
            A[1,0] = Ixy[y,x]
            A[1,1] = Iy2[y,x]
            b[0,0] = -Ixt[y,x]
            b[1,0] = -Iyt[y,x]
            w,v = np.linalg.eig(A)
            #print w
            if w[0] == 0 or w[1] == 0 or w[0]/w[1] > THRESHOLD or w[1]/w[0] > THRESHOLD:
                U[y,x] = 0
                V[y,x] = 0
            
            else:
                uv = np.linalg.lstsq(A, b)[0]
                U[y,x] = uv[0]
                V[y,x] = uv[1]
    return U,V
