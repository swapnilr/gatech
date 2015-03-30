import numpy as np
import cv2

def warp2(i2, vx, vy):
    """
    this is a "backwards" warp:
    if vx,vy are correct then warpI2==i1
    """
    M, N = i2.shape
    x = np.linspace(1, N, N)
    y = np.linspace(1, M, M)
    xv, yv= np.meshgrid(x,y)
    #print (xv + vx).type()
    #cv2.convertMaps(xv + vx, yv + vy, cv2.CV_32FC1)
    warpI3=cv2.remap(i2, (xv+vx).astype(np.float32),(yv+vy).astype(np.float32),cv2.INTER_NEAREST)
    warpI2=cv2.remap(i2, (xv+vx).astype(np.float32),(yv+vy).astype(np.float32),cv2.INTER_LINEAR)
    I=np.where(np.isnan(warpI2))
    warpI2[I]=warpI3[I]
    return warpI2

def warp(image, U, V):
    [M, N] = image.shape
    X, Y = np.meshgrid(xrange(N), xrange(M))
    map_x = (X + U).astype('float32')
    map_y = (Y + V).astype('float32')

    warp1 = cv2.remap(image, map_x, map_y, interpolation = cv2.INTER_LINEAR)
    warp2 = cv2.remap(image, map_x, map_y, interpolation = cv2.INTER_NEAREST)
    fail = np.isnan(warp1)
    warp1[fail] = warp2[fail]
    return warp1
