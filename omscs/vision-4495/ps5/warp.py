import numpy as np
import cv2

def warp(i2, vx, vy):
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
