import numpy as np
import cv2
import time
import cv
import math
import random
PIC_A = "pic_a.jpg"
PIC_A_2D = "pts2d-pic_a.txt"
PIC_A_2D_NORM = "pts2d-norm-pic_a.txt"
PIC_B = "pic_b.jpg"
PIC_B_2D = "pts2d-pic_b.txt"
SCENE = "pts3d.txt"
SCENE_NORM = "pts3d-norm.txt"

def main():
    part1_calibration()
    part2_matrix()
    #testLeastSquares()
    #testMatrixEst()
    #print readFile("input/" + PIC_A_2D)

def readFile(filename):
    with open(filename) as f:
        lines = f.readlines()
        pts = []
        for line in lines:
            pts.append(map(float, line.split()))
    return np.array(pts)    

def leastSquares(twoD, threeD):
    points0, dim0 = twoD.shape
    points1, dim1 = threeD.shape
    assert points0 == points1
    assert dim0 == 2
    assert dim1 == 3
    A = np.zeros((2*points0, 11))
    b = np.zeros((2*points0, 1))
    for i in range(points0):
        b[i*2, 0] = twoD[i, 0]
        b[i*2 + 1, 0] = twoD[i, 1]
    for i in range(points0):
        u = twoD[i, 0]
        v = twoD[i, 1]
        X = threeD[i, 0]
        Y = threeD[i, 1]
        Z = threeD[i, 2]
        A[i*2, 0] = X
        A[i*2, 1] = Y
        A[i*2, 2] = Z
        A[i*2, 3] = 1
        A[i*2, 8] = -(u*X)
        A[i*2, 9] = -(u*Y)
        A[i*2, 10] = -(u*Z)
        A[i*2 + 1, 4] = X
        A[i*2 + 1, 5] = Y
        A[i*2 + 1, 6] = Z
        A[i*2 + 1, 7] = 1
        A[i*2 + 1, 8] = -(v*X)
        A[i*2 + 1, 9] = -(v*Y)
        A[i*2 + 1, 10] = -(v*Z)
    #print A
    #print b
    return np.linalg.lstsq(A,b)

def svd(twoD, threeD):
    points0, dim0 = twoD.shape
    points1, dim1 = threeD.shape
    assert points0 == points1
    assert dim0 == 2
    assert dim1 == 3
    A = np.zeros((2*points0, 12))
    b = np.zeros((2*points0, 1))
    for i in range(points0):
        u = twoD[i, 0]
        v = twoD[i, 1]
        X = threeD[i, 0]
        Y = threeD[i, 1]
        Z = threeD[i, 2]
        A[i*2, 0] = X
        A[i*2, 1] = Y
        A[i*2, 2] = Z
        A[i*2, 3] = 1
        A[i*2, 8] = -(u*X)
        A[i*2, 9] = -(u*Y)
        A[i*2, 10] = -(u*Z)
        A[i*2, 11] = -u
        A[i*2 + 1, 4] = X
        A[i*2 + 1, 5] = Y
        A[i*2 + 1, 6] = Z
        A[i*2 + 1, 7] = 1
        A[i*2 + 1, 8] = -(v*X)
        A[i*2 + 1, 9] = -(v*Y)
        A[i*2 + 1, 10] = -(v*Z)
        A[i*2 + 1, 11] = -v
    u, s, v = np.linalg.svd(A)
    #print v
    return v[-1]

def svd22(twoD, twoD2):
    points0, dim0 = twoD.shape
    points1, dim1 = twoD2.shape
    assert points0 == points1
    #assert dim0 == 2
    #assert dim1 == 2
    A = np.zeros((points0, 9))
    for i in range(points0):
        u = twoD[i, 0]
        v = twoD[i, 1]
        up = twoD2[i, 0]
        vp = twoD2[i, 1]
        A[i, 0] = up * u
        A[i, 1] = up * v
        A[i, 2] = up
        A[i, 3] = vp * u
        A[i, 4] = vp * v
        A[i, 5] = vp
        A[i, 6] = u
        A[i, 7] = v
        A[i, 8] = 1
    u, s, v = np.linalg.svd(A)
    #print v
    return v[-1]    

def part1_calibration():
    # Part A
    print "Part 1"
    print "======"
    print "Part A"
    print "------"
    twoD = readFile("input/" + PIC_A_2D_NORM)
    threeD = readFile("input/" + SCENE_NORM)
    M = leastSquares(twoD, threeD)[0]
    div = M[0,0]/(-0.4583)
    M_norm = M/div # last value is 1/div
    M2 =  svd(twoD, threeD)
    div = M2[0]/(-0.4583)
    M_norm = M2/div
    print "Matrix M"
    print M2.reshape((3,4))
    print "Normalized Matrix"
    print M_norm.reshape((3,4))
    d = np.zeros((4,1))
    d[0:3, 0] = threeD[-1]
    d[3] = 1
    M = M2.reshape((3,4))
    pt2d = np.dot(M, d)
    pt2d_norm = pt2d/pt2d[-1]
    print "Normalized point"
    print np.transpose(pt2d_norm[:2,])

    def getResidual(index, M):
        d = np.zeros((4,1))
        d[0:3, 0] = threeD[index]
        d[3] = 1
        pt2d = np.dot(M, d)
        pt2d_norm = pt2d/pt2d[-1]
        def residual(pt1, pt2):
            rows, columns = pt1.shape
            res = 0
            for r in range(rows):
                res += (pt1[r,0] - pt2[r])**2
            return math.sqrt(res)
        return residual(pt2d[:2,], twoD[index])

    print "Residual"
    print getResidual(-1, M2.reshape((3,4)))
    print

    # Part B
    print "Part B"
    print "------"
    min_residual = float('inf') #max infinitiy
    bestM = None
    for size in [8, 12, 16]:
        for trial in range(10):
            indices = range(20)
            random.shuffle(indices)
            points = indices[:size]
            to_delete = indices[size:]
            test_sample = indices[16:]
            test_to_delete = indices[:16]
            smallTwoD = np.delete(twoD, to_delete, 0)
            smallThreeD = np.delete(threeD, to_delete, 0)
            smallM = svd(smallTwoD, smallThreeD).reshape((3,4))
            average_residual = 0
            for index in test_sample:
                average_residual += getResidual(index, smallM)
            average_residual /= 4
            if average_residual < min_residual:
                min_residual = average_residual
                bestM = smallM
    print "Best Matrix"
    print bestM
    print "Min residual"
    print min_residual
    print

    # Part C
    print "Part C"
    print "------"
    print "Camera location with best M"
    Q = bestM[:, 0:3]
    m4 = bestM[:, 3]
    C = np.dot((-(np.linalg.inv(Q))),  m4)
    print C
    print

def part2_matrix():
    print "Part 2 - Fundamental Matrix Esimation"
    print "======"
    print "Part A"
    print "------"
    twoD = readFile("input/" + PIC_A_2D)
    twoD2 = readFile("input/" + PIC_B_2D)
    def getF(img1, img2):
        F_tilda = svd22(img1, img2)
        F_tilda = F_tilda.reshape((3,3))
        U, s, V = np.linalg.svd(F_tilda)
        S = np.zeros((3,3))
        S[:3, :3] = np.diag(s)
        sp = s
        sp[np.argmin(s)] = 0
        Sp = np.zeros((3,3))
        Sp[:3, :3] = np.diag(sp)
        F = np.dot(np.dot(U, Sp), V)
        return F_tilda, F
    F_tilda, F = getF(twoD, twoD2)
    print "F_tilda"
    print F_tilda
    print 
    print "Part B"
    print "------"
    print "F"
    print F
    print

    print "Part C"
    print "------"
    points, irr = twoD.shape

    def draw(img_name, points, F):
        img = cv2.imread("input/" + img_name)
        rows, columns, rgb = img.shape
        for point in points:
            p = np.zeros((3,1))
            p[2, 0] = 1
            p[0:2, 0] = np.transpose(point)
            lp = np.dot(F, p)
            def solve(x):
                return  (-lp[2] - (lp[0]*x))/lp[1] # ax + by + c = 0 => y = -c/b - (ax/b)
            cv2.line(img,(0,solve(0)),(columns,solve(columns)),cv.CV_RGB(0,255,0))
        return img
    imgA = draw(PIC_A, twoD2, np.transpose(F))
    imgB = draw(PIC_B, twoD, F)
    print "Writing Files"
    cv2.imwrite("output/ps3-2-c-1.png", imgA)
    cv2.imwrite("output/ps3-2-c-2.png", imgB)

    def getHeterogeneous(points):
        ptsSize, dim = points.shape
        newPoints = np.zeros((ptsSize, dim + 1))
        newPoints[:,:2] = points
        newPoints[:,2] = 1
        return newPoints

    def scale(points):
        mean = np.mean(points, 0)
        cu = mean[0]
        cv = mean[1]
        maxes = 1/np.amax(points)
        l = np.zeros((3,3))
        r = np.zeros((3,3))
        l[0,0] = maxes
        l[1,1] = maxes
        l[2,2] = 1
        r[0,0] = 1
        r[1,1] = 1
        r[2,2] = 1
        r[0,2] = -cu
        r[1,2] = -cv
        T = np.dot(l, r)
        scaled = np.dot(T, np.transpose(getHeterogeneous(points)))
        return T, np.transpose(scaled)
    print "Part D"
    print "------"
    Ta, scaledD = scale(twoD)
    Tb, scaledD2 = scale(twoD2)
    F_cap =  getF(scaledD, scaledD2)[1]
    print "Ta"
    print Ta
    print "Tb"
    print Tb
    print "F_hat"
    print F_cap

    print
    print "Part E"
    print "------"
    F = np.dot(np.dot(np.transpose(Tb), F_cap), Ta)
    print "F"
    print F
    print "Writing images"
    imgA = draw(PIC_A, twoD2, np.transpose(F))
    imgB = draw(PIC_B, twoD, F)
    cv2.imwrite("output/ps3-2-e-1.png", imgA)
    cv2.imwrite("output/ps3-2-e-2.png", imgB)

if __name__ == '__main__':
    main()


