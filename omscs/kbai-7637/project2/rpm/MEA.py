from FigureDelta import FigureDelta

def computeDelta(initial, goal, ignoreAddedRemoved):
    initialObjs = initial.getObjects()
    goalObjs = goal.getObjects()
    size = max(len(initialObjs), len(goalObjs))

    figDelta = new FigureDelta(initial, goal)
    figDelta.setIngoreAddedRemoved(ignoreAddedRemoved)
    
    for i in range(size):
        initialObj = None
        goalObj = None
        objName = None

            if (i >= initialObjs.size()) {
                goalObj = goalObjs.get(i);
                objName = goalObj.getName();
                initialObj = new RavensObject(objName);
            } else if (i >= goalObjs.size()) {
                initialObj = initialObjs.get(i);
                objName = initialObj.getName();
                goalObj = new RavensObject(objName);
            } else {
                initialObj = initialObjs.get(i);
                goalObj = goalObjs.get(i);
                objName = initialObj.getName();
            }
            ObjectDelta objDelta = MeansEndsAnalysis.computeDelta(initialObj, goalObj,
                    ignoreAddedRemoved);
            objDelta.setObjectIndex(i);
            figDelta.add(objDelta);
            figDelta.getIndexMap().put(objName, i);
        }

        return figDelta;
    }

    private static ObjectDelta computeDelta(RavensObject initial, RavensObject goal,
            boolean ignoreAddedRemoved) {
        Map<String, String> beforeMap = RavenUtils.convert2Map(initial);

        Map<String, String> afterMap = RavenUtils.convert2Map(goal);
        Set<String> removedKeys = null;
        Set<String> addedKeys = null;
        if (!ignoreAddedRemoved) {
            removedKeys = new HashSet<String>(beforeMap.keySet());
            removedKeys.removeAll(afterMap.keySet());

            addedKeys = new HashSet<String>(afterMap.keySet());
            addedKeys.removeAll(beforeMap.keySet());
        }
        Set<Entry<String, String>> changedEntriesFrom = new HashSet<Entry<String, String>>(
                beforeMap.entrySet());
        changedEntriesFrom.removeAll(afterMap.entrySet());

        Set<Entry<String, String>> changedEntriesTo = new HashSet<Entry<String, String>>(
                afterMap.entrySet());
        changedEntriesTo.removeAll(beforeMap.entrySet());
        ObjectDelta delta = new ObjectDelta(initial, goal, addedKeys, removedKeys,
                changedEntriesFrom, changedEntriesTo);
        return delta;

    }

    static Set<String> computeAddedValues(RavensFigure initial, RavensFigure goal) {
        Set<String> addedKeys = new HashSet<String>(
                RavenUtils.convert2ListOfName(goal.getObjects()));
        addedKeys.removeAll(RavenUtils.convert2ListOfName(initial.getObjects()));
        return addedKeys;
    }

    static Set<String> computeRemovedValues(RavensFigure initial, RavensFigure goal) {

        Set<String> removedKeys = new HashSet<String>(RavenUtils.convert2ListOfName(initial
                .getObjects()));
        removedKeys.removeAll(RavenUtils.convert2ListOfName(goal.getObjects()));
        return removedKeys;
    }

    public static boolean isObjectDeltasSameIgnoreInsertionOrder(FigureDelta a1, FigureDelta a2) {
        Collection<ObjectDelta> col1 = a1.getObjectDeltas().values();
        Collection<ObjectDelta> col2 = a2.getObjectDeltas().values();
        return CollectionsUtil.collectionsEqualsStringsIgnoreOrder(col1, col2);
    }

    public static void printDelta(HashMap<String, RavensFigure> figures, String fromName,
            String toName) {
        System.out.println(fromName + " to " + toName);

        RavensFigure from = figures.get(fromName);
        RavensFigure to = figures.get(toName);
        FigureDelta delta = computeDelta(from, to, false);
        System.out.println(delta);
    }
}
