import cv2
import numpy as np
from collections import namedtuple
import math
import functools
import time

FILES = ['pres_debate.avi', 'noisy_debate.avi', 'pedestrians.avi']

Model = namedtuple('Model', ['x', 'y', 'w', 'h'], verbose=True)

NUM_PARTICLES = 1000
SIGMA_MSE = 10
ALPHA = 0.95

def getHandModel():
    return Model(x=520, y=385, w=90, h=130)

def getModel(index=0):
    return createModel(getTextFile(getFilename(index)))

def createModel(filename):
    with open(filename) as f:
        x, y = map(float, f.readline().split())
        w, h = map(float, f.readline().split())
        model = Model(x=x, y=y, w=w, h=h)
    return model

def getTextFile(filename):
    return '%s.txt' % filename[:-4]

def getFilename(index=0):
    return 'input/%s' % FILES[index]

def upscale(image):
    return (image * 255).astype(np.uint8)

def downscale(image):
    return image.astype(np.float) / 255

class Filter():

    def __init__(self, image, template):
        self.image = image
        self.template = template

    # Model should take in 2 templates, the current template and the best guess
    def setAppearanceModel(self, model):
        self.appearance_model = model

    # Model is a function that takes in an (y,x) tuple and returns another
    # (y,x) tuple.
    def setDynamicsModel(self, model):
        self.dynamics_model = model

    # Model is a function that takes in an image, a template and an (y,x) tuple
    # and returns a float.
    def setSensorModel(self, model):
        self.sensor_model = model

    # Particles is an array of (y,x) locations
    def compute(self, particles):
        probs = np.zeros(len(particles))
        new_particles = [0.] * len(particles)
        #print particles
        for index, particle in enumerate(particles):
            probs[index] = self.sensor_model(self.image, self.template, particle)
            new_particles[index] = self.dynamics_model(particle)
        # Normalize probs
        probs = probs/np.sum(probs)
        # Resample
        instances = np.random.multinomial(len(particles), probs)
        final_particles = [0.] * len(particles)
        loc = 0
        for index, val in enumerate(instances):
            for j in range(val):
                final_particles[loc] = new_particles[index]
                loc += 1

        height, width = self.template.shape
        pindex = np.argmax(probs)
        particle = new_particles[pindex]
        v = particle[0] - height/2
        u = particle[1] - width/2
        patch = self.image[v:v+height,u:u+width]
        self.template = self.appearance_model(self.template, patch)
        return final_particles, particle, self.template

def simpleAppearanceModel(template, best, alpha=ALPHA):
    return template

def alphaAppearanceModel(template, best, alpha=ALPHA):
    return alpha * best + (1 - alpha) * template

def gaussNoiseDynamicsModel(particle, sigma=1.0):
    return np.around(np.random.normal(scale=sigma,size=2) + particle)


def MSESensorModel(image, template, particle, sigma_mse=SIGMA_MSE):
    height, width = template.shape
    MSE = 0.
    #print particle
    v = max(0, particle[0] - height/2)
    u = max(0, particle[1] - width/2)
    if v + height > image.shape[0]:
        v = image.shape[0] - (v + height)
    if u + width > image.shape[1]:
        u = image.shape[1] - (u + width)
    #print particle, height, width, v, u

    patch = image[v:v+height,u:u+width]
    #print template.shape, patch.shape
    th, tw = patch.shape
    if th != height or tw != width:
        print "Size is wrong"
        print particle, height, width, v, u
        patch = np.zeros((template.shape))
    MSE = np.mean(((template - patch)**2))
    #for y in range(height):
    #    for x in range(width):
    #        #print template[y,x], image[y+v, x+u]
    #        MSE += (template[y,x] - image[y+v, x+u])**2
    #MSE = MSE/(height*width)
    #print MSE
    return math.exp(-MSE/(2 * (sigma_mse ** 2)))

def q1():
    # Part A
    test(simpleAppearanceModel, stopPoints=[28,84,144], savePatchFile=True, sigma_mse=2)
    # Part B
    test(simpleAppearanceModel, stopPoints=[14,32,46], part='e', imgNum=1)

def q2():
    # Part A
    test(alphaAppearanceModel, sigma=4.1, alpha=0.9, 
         dynamicsModel=functools.partial(gaussNoiseDynamicsModel, sigma=4.1),
         stopPoints=[15,50,140], model=getHandModel(), savePatchFile=True,
         qn=2)
    # Part B
    test(alphaAppearanceModel, sigma=4.4, alpha=0.95, 
         dynamicsModel=functools.partial(gaussNoiseDynamicsModel, sigma=4.4),
         stopPoints=[15,50,140], model=getHandModel(), savePatchFile=True,
         qn=2, part='b', imgNum=1)

def test(appearanceModel, sigma=0.0,
         dynamicsModel=gaussNoiseDynamicsModel, stopPoints=None, 
         model=None, alpha=ALPHA, savePatchFile=False, qn=1,part='a', 
         imgNum=0, sigma_mse=SIGMA_MSE):
    stopPoints = stopPoints or []
    debate = cv2.VideoCapture(getFilename(imgNum))
    index = 1
    ret, frame = debate.read()
    frame = (cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)).astype(np.float)
    model = model or getModel(imgNum)
    template = frame[int(math.floor(model.y)):int(math.ceil(model.y+model.h)), int(math.floor(model.x)):int(math.ceil(model.x+model.w)) ]
    index += 1

    count = 1
    if savePatchFile:
        cv2.imwrite("output/ps6-%d-%s-%d.png" % (qn, part, count), upscale(template))
        count += 1
    #import time
    #time.sleep(15)

    particles = []
    size = int(math.ceil(math.sqrt(NUM_PARTICLES)))
    rows, columns = frame.shape
    ys = np.around(np.linspace(int(model.h/2) + 1, rows-int(model.h/2) - 1, size, endpoint=False))
    xs = np.around(np.linspace(int(model.w/2) + 1, columns-int(model.w/2) - 1, size, endpoint=False))
    #ys = np.around(np.linspace(int(model.y), int(model.y+model.h), size, endpoint=False))
    #xs = np.around(np.linspace(int(model.x), int(model.x+model.w), size, endpoint=False))
    #print ys
    #print xs
    for y in ys:
        for x in xs:
            particles.append(np.array((y,x)))

    while debate.isOpened():
        ret, frame = debate.read()
        orig = frame
        if not ret:
            print "ret is False at index %d" % index
            break
        frame = (cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)).astype(np.float)
        f = Filter(frame, template)
        f.setAppearanceModel(functools.partial(appearanceModel, alpha=alpha))
        f.setDynamicsModel(dynamicsModel)
        f.setSensorModel(functools.partial(MSESensorModel, sigma_mse=sigma_mse))
        particles, best, template = f.compute(particles)
        if index in stopPoints:
            frame = cv2.cvtColor(upscale(frame), cv2.COLOR_GRAY2RGB)
            for particle in particles:
                pt = (int(particle[1]), int(particle[0]))
                cv2.circle(orig, pt, 1, (0, 0, 255))
            pt = (int(best[1]), int(best[0]))
            cv2.circle(orig, pt, 5, (255, 0, 0))
            height, width = template.shape
            top = (pt[0] - width/2, pt[1] - height/2)
            bottom = (pt[0]+width/2, pt[1] + height/2)
            cv2.rectangle(orig, top, bottom, (255, 0, 0))
            cv2.imwrite("output/ps6-%d-%s-%d.png" % (qn, part, count), orig)
            count += 1
            time.sleep(5)
        index += 1
        if index > 150:
            break
        #print index

def main():
    q1()
    q2()

if __name__ == '__main__':
    main()
