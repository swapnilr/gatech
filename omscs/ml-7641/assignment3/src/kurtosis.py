from sklearn.decomposition import FastICA
import numpy
import string
import scipy

data = numpy.genfromtxt(open("modifiedLetter2.data"),delimiter=",")
print data.shape
X = numpy.delete(data, -1,1)
print X.shape
ica = FastICA()
ica_sources = ica.fit_transform(X)
print scipy.stats.kurtosis(ica_sources)
