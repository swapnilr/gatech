import cv2

def get(figure):
    x = cv2.imread(figure.fullpath)
    return str(x.data)

