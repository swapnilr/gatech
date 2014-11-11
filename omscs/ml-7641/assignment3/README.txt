The analysis for this paper was done using a number of different frameworks.
I used ABAGAIL, WEKA as well as scikit.

Most of the tests were performed using WEKA. Most of the test code is accessible from MainExperiment.java, which has a main function and can be run from the command line.
I also performed some experiments using ABAGAIL, and the ICAClusteringExperiments.java, DimensionalityReductionClusteringTests.java, ClusteringTests.java and RandomizedClusteringExperiments.java contains most of the test code.

For the kurtosis calculation of ICA, I used scikit. python kurtosis.py gives the kurtosis for the letter recognition dataset, and python kurtosis2.py gives the kurtosis for the waveform dataset
