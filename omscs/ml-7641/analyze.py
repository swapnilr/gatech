with open("ProblemsFourPeaks.txt") as f:
  with open("FourPeaks.csv", "w") as f2:
    T = "0"
    N = "0" 
    line = f.readline()
    while line:
      splits = line.split()
      if len(splits) == 4:
        T = splits[2]
      elif len(splits) == 3:
        N = splits[2]
      else:
        f2.write("%s,%s,%s\n" % (T,N,splits[0]))
      line = f.readline()