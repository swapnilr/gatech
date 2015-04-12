import cv2
import numpy as np
from collections import namedtuple
import math

FILES = ['pres_debate.avi', 'noisy_debate.avi', 'pedestrians.avi']

Model = namedtuple('Model', ['x', 'y', 'w', 'h'], verbose=True)

NUM_PARTICLES = 196
SIGMA_MSE = 10

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

class Filter():

    def __init__(self, image, template):
        self.image = image
        self.template = template

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
        return final_particles

def gaussNoiseDynamicsModel(particle):
    return np.around(np.random.normal(size=2) + particle)

def MSESensorModel(image, template, particle):
    height, width = template.shape
    MSE = 0.
    #print particle
    v = particle[0] - height/2
    u = particle[1] - width/2
    #print particle, height, width, v, u 
    patch = image[v:v+height,u:u+width]
    #print template.shape, patch.shape
    MSE = ((template - patch)**2).mean()
    #for y in range(height):
    #    for x in range(width):
    #        #print template[y,x], image[y+v, x+u]
    #        MSE += (template[y,x] - image[y+v, x+u])**2
    #MSE = MSE/(height*width)
    #print MSE
    return math.exp(-MSE/(2 * (SIGMA_MSE ** 2)))

def q1():
    debate = cv2.VideoCapture(getFilename(0))
    index = 1
    ret, frame = debate.read()
    frame = (cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)).astype(np.float)
    model = getModel(0)
    template = frame[int(math.floor(model.y)):int(math.ceil(model.y+model.h)), int(math.floor(model.x)):int(math.ceil(model.x+model.w)) ]
    index += 1

    particles = []
    size = int(math.ceil(math.sqrt(NUM_PARTICLES)))
    rows, columns = frame.shape
    ys = np.linspace(int(model.h/2) + 1, rows-int(model.h/2) - 1, size, endpoint=False)
    xs = np.linspace(int(model.w/2) + 1, columns-int(model.w/2) - 1, size, endpoint=False)
    for y in ys:
        for x in xs:
            particles.append(np.array((y,x)))

    while debate.isOpened():
        ret, frame = debate.read()
        if not ret:
            print "ret is False at index %d" % index
            break
        frame = (cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)).astype(np.float)
        f = Filter(frame, template)
        f.setDynamicsModel(gaussNoiseDynamicsModel)
        f.setSensorModel(MSESensorModel)
        particles = f.compute(particles)
        if index == 28 or index == 84 or index == 144:
            frame = cv2.cvtColor(upscale(frame), cv2.COLOR_GRAY2RGB)
            for particle in particles:
                pt = (int(particle[1]), int(particle[0]))
                cv2.circle(frame, pt, 1, (0, 0, 255))
            cv2.imshow("%d" % index, frame)
            import time
            time.sleep(5)
        index += 1
        #print index

def main():
    q1()

if __name__ == '__main__':
    main()
