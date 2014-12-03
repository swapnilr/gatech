All the tests can be run from LearningAlgorithms.java

After compiling the code, the code can be run with
javac edu.gatech.ml.assignment4.tutorial.LearningAlgorithms

with burlap.jar on the classpath.

Within the java file, you can run different algorithms with some modifications:

1. Currently the program will run each of Value Iteration, Policy Iteration and Q-Learning on the large grid. To run these on the smaller grid, comment out line 240 - int size = setLargeDomain(); and uncoment line 239 - int size = setSmallDomain();
2. To produce the graphs in the pdf, the experimenterAndPlotter function should be called with modifications appropriate to the graph being generated. 

To not increase the size of the zip, burlap.jar has been uploaded separately.