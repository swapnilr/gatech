import numpy as np

PIC_A = "pic_a.jpg"
PIC_A_2D = "pts2d-pic_a.txt"
PIC_A_2D_NORM = "pts2d-norm-pic_a.txt"
PIC_B = "pic_b.jpg"
PIC_B_2D = "pts2d-pic_b.txt"
SCENE = "pts3d.txt"
SCENE_NORM = "pts3d-norm.txt"

def main():
    testLeastSquares()
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
    assert dim0 == 2
    assert dim1 == 2
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

def testLeastSquares():
    twoD = readFile("input/" + PIC_A_2D_NORM)
    threeD = readFile("input/" + SCENE_NORM)
    #print twoD
    #print threeD
    M = leastSquares(twoD, threeD)[0]
    div = M[0,0]/(-0.4583)
    print M/div
    print 1/div
    M2 =  svd(twoD, threeD)
    div = M2[0]/(-0.4583)
    print M2/div
    d = np.zeros((4,1))
    d[0:3, 0] = threeD[-1]
    d[3] = 1
    #np.resize(M, (12,1))
    #M[11, 0] = 1
    #print M
    M = M2.reshape((3,4))
    pt2d = np.dot(M, d)
    print pt2d/pt2d[-1]
    Q = M[:, 0:3]
    m4 = M[:, 3]
    C = np.dot((-(np.linalg.inv(Q))),  m4)
    print C

    print "-----Fundamental Matrix Esimation-----"
    twoD = readFile("input/" + PIC_A_2D)
    twoD2 = readFile("input/" + PIC_B_2D)
    F_tilda = svd22(twoD, twoD2)
    #print F_tilda
    F_tilda = F_tilda.reshape((3,3))
    #print F_tilda
    U, s, V = np.linalg.svd(F_tilda)
    S = np.zeros((3,3))
    S[:3, :3] = np.diag(s)
    #print s, np.diag(s), S
    #print U.shape
    #print s.shape
    #print V.shape
    #print np.dot(np.dot(U,S),V)
    #smallest = np.amin(s)
    #print s, np.amin(s), np.argmin(s)
    sp = s
    sp[np.argmin(s)] = 0
    Sp = np.zeros((3,3))
    Sp[:3, :3] = np.diag(s)
    F = np.dot(np.dot(U, Sp), V)

if __name__ == '__main__':
    main()


