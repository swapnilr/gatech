import cv2
import numpy as np
import collections

Descriptor = collections.namedtuple('Descriptor', ['action','person', 'trial'],verbose=False)

THRESHOLD = 2
TAU = 20

def getFilename(action_number, person_number, trial_number):
    return "input/PS7A%dP%dT%d.avi" % (action_number, 
                                       person_number, 
                                       trial_number)

def getMHI(action_number, person_number, trial_number):
    #print action_number, person_number, trial_number
    return cv2.imread("input/MHI/action%d/person%d/MHI%d.png" % (action_number, 
                                                             person_number, 
                                                             trial_number), 
                      cv2.IMREAD_GRAYSCALE).astype(np.float)

def MHI(action, person, trial, tau=TAU, blur=9, threshold_val=THRESHOLD):
    video = cv2.VideoCapture(getFilename(action, person, trial))
    t = 1
    videoArray = []
    while True:
        ret, frame = video.read()
        if not ret or not video.isOpened():
            break
        frame = (cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)).astype(np.float)
        frame = cv2.GaussianBlur(frame,(blur,blur),0)
        videoArray.append(frame)
        t += 1
    rows, columns = videoArray[0].shape
    numFrames = len(videoArray)
    I = np.zeros((rows, columns, numFrames))
    kernel = np.ones((5,5),np.uint8)
    j = 1
    for index, frame in enumerate(videoArray):
        I[:,:,index] = frame
    B = np.zeros(I.shape)
    MHI = np.zeros(I.shape)
    for i in range(numFrames):
        if i != 0:
            b_orig = np.abs(I[:,:,i] - I[:,:,i-1])
            b = upscale(threshold(b_orig, threshold_val))
            B[:,:,i] = cv2.morphologyEx(b, cv2.MORPH_OPEN, kernel)
            MHI[:,:,i] = np.where(B[:,:,i] == 255, 
                                  tau, 
                                  np.maximum(MHI[:,:,i-1] - 1, 0))
            cv2.imwrite("output/MHI/action%d/person%d/trial%d/%d.png" % (action, 
                                                        person, 
                                                        trial, i), 
                        upscale(MHI[:,:,i]))
        #cv2.imwrite("output/ps7-1-a-%d.png" % j, I)
        #j += 1

def upscale(img):
    #print np.min(img), 
    img = img - np.min(img)
    #print np.max(img)
    img = img/np.max(img)
    return (img * 255).astype(np.uint8)

def getIndexArrays(img):
    rows, columns = img.shape
    x = np.zeros(img.shape)
    y = np.zeros(img.shape)
    x_ind = np.arange(columns).reshape((1, columns))
    x[:,:] = x_ind
    y_ind = np.arange(rows).reshape((rows, 1))
    y[:,:] = y_ind
    return x, y

def moment(img, i, j):
    rows, columns = img.shape
    mom = 0.0
    x, y = getIndexArrays(img)
    mom = np.sum((x ** i) * (y ** j) * img)
    #for y in range(rows):
    #    for x in range(columns):
    #        mom += (x ** i) * (y ** j) * img[y,x]
    return mom

def central_moments(img, p, q):
    M00 = moment(img, 0, 0)
    M01 = moment(img, 0, 1)
    M10 = moment(img, 1, 0)
    avg_x = M10/M00
    avg_y = M01/M00
    mu = 0.0
    img = img.astype(np.float)
    rows, columns = img.shape
    x, y = getIndexArrays(img)
    mu = np.sum( ((x - avg_x) ** p) * ((y - avg_y) ** q) * img)
    #for y in range(rows):
    #    for x in range(columns):
    #        mu += ((x-avg_x)**p) * ((y-avg_y)**q) * img[y,x]
    return mu

def scale_invariant_moments(img, p, q, mu00):
    #mu00 = central_moments(img, 0, 0)
    mupq = central_moments(img, p, q)
    return mupq / (mu00 ** (1 + (p+q)/2.0))

def threshold(img, threshold_val):
    return (img > threshold_val).astype(np.float)

vector_hash = {}

def create_vector(img, desc, use_mu=False):
    global vector_hash
    if desc in vector_hash:
        return vector_hash[desc]
    #print "Creating vector for " + str(desc)
    vector = np.zeros((1,14))
    i = 0
    for im in [img, threshold(img, THRESHOLD)]:
        mu00 = central_moments(img, 0, 0)
        for v in [(2,0), (0,2), (1,2), (2,1), (2,2), (3,0), (0,3)]:
            if use_mu:
                vector[0, i] = central_moments(im, v[0], v[1])
            else:
                vector[0, i] = scale_invariant_moments(im, v[0], v[1], mu00)
            i += 1
    vector_hash[desc] = vector
    return vector

def compare_ssd(vector1, vector2):
    return np.sum((vector1 - vector2)**2)


def confusion_matrix(image_descriptors, include_same=True, use_mu=False):
    """
    Takes a list of image, descriptor pairs
    Returns a confusion matrix.
    """
    matrix = np.zeros((3,3))
    for index, image_desc in enumerate(image_descriptors):
        image, desc = image_desc
        best_action = -1
        best_ssd = float("inf")
        best_desc2 = -1
        vector = create_vector(image, desc, use_mu)
        for index2, image_desc2 in enumerate(image_descriptors):
            image2, desc2 = image_desc2
            if include_same or desc.person != desc2.person:
                ssd = compare_ssd(vector, create_vector(image2, desc2, use_mu))
                if ssd < best_ssd:
                    best_ssd = ssd
                    best_action = desc2.action
                    best_desc2 = desc2
        matrix[desc.action-1, best_action-1] += 1
        if desc.action != best_action:
            print desc, best_desc2
    #total = 9 - (not include_same)
    #matrix /= total
    return matrix

def main():
    #for i in range(1,4):
    #    MHI(1, 3, i, blur=41, threshold_val=15, tau=40)
    #generateMHI()
    generateConfusionMatrix()

def generateMHI():    
    for i in range(1,4):
        for j in range(1,4):
            for k in range(1,4):
                MHI(i,j,k, tau=40, blur=41, threshold_val=15)
    # blur=25, tau = 30

def generateConfusionMatrix():
    image_descriptors = []
    for i in range(1,4):
        for j in range(1,4):
            for k in range(1,4):
                image_descriptors.append((getMHI(i, j, k), Descriptor(action=i,person=j, trial=k)))
    print confusion_matrix(image_descriptors, include_same=False)

if __name__ == '__main__':
    main()
