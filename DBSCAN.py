import numpy as np
import matplotlib.pyplot as plt
import queue
import pandas as pd
import random
#Define different point groups
NOISE = 0
UNASSIGNED = 0
core=-1
edge=-2



#Function to find all neighboring points in radius
def neighbor_points(data, pointId, radius):
    points = []
    for i in range(len(data)):
        if np.linalg.norm(data[i] - data[pointId]) <= radius:
            points.append(i)
    return points

#DBScan algorithm
def dbscan(data, Eps, MinPt):
    
    pointlabel  = [UNASSIGNED] * len(data)
    pointcount = []
    #initialize list for core/non-core point
    corepoint=[]
    noncore=[]
    
    #Find neighbors of all points
    for i in range(len(data)):
        pointcount.append(neighbor_points(train,i,Eps))
    
    #Find all core point, edgepoint and noise points
    for i in range(len(pointcount)):
        if (len(pointcount[i])>=MinPt):
            pointlabel[i]=core
            corepoint.append(i)
        else:
            noncore.append(i)

    for i in noncore:
        for j in pointcount[i]:
            if j in corepoint:
                pointlabel[i]=edge

                break
            
    #start assigning points to class
    cl = 1
    #Queue the neighboring points and find the neighbor of the adjacent points
    for i in range(len(pointlabel)):
        q = queue.Queue()
        if (pointlabel[i] == core):
            pointlabel[i] = cl
            for x in pointcount[i]:
                if(pointlabel[x]==core):
                    q.put(x)
                    pointlabel[x]=cl
                elif(pointlabel[x]==edge):
                    pointlabel[x]=cl
            #Stop when all points in the queue have been checked
            while not q.empty():
                neighbors = pointcount[q.get()]
                for y in neighbors:
                    if (pointlabel[y]==core):
                        pointlabel[y]=cl
                        q.put(y)
                    if (pointlabel[y]==edge):
                        pointlabel[y]=cl            
            cl=cl+1 #skip to next classification
           
    return pointlabel,cl
    
#plot result
def plotRes(data, clusterRes, clusterNum):
    nPoints = len(data)
    scatterColors = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) #random color
             for i in range(clusterNum)]
    for i in range(clusterNum):
        if (i==0):
            #Color the noises black
            color='black'
        else:
            color = scatterColors[i % len(scatterColors)]
        x1 = [];  y1 = []
        for j in range(nPoints):
            if clusterRes[j] == i:
                x1.append(data[j, 0])
                y1.append(data[j, 1])
        plt.scatter(x1, y1, c=color, alpha=1, marker='.')


#Dataset upload
data = pd.read_csv("Mall_Customers.csv") #Dataset name
train = data.loc[:, ['Annual Income (k$)',
                 'Spending Score (1-100)']].values

#EPS and minpoint determination
epss = [4]
minptss = [5]
plt.show()
# Finding and plotting/printing all classes and outliers
for eps in epss:
    for minpts in minptss:
        print('Set eps = ' +str(eps)+ ', Minpoints = '+str(minpts))
        pointlabel,cl = dbscan(train,eps,minpts)
        plotRes(train, pointlabel, cl)
        plt.show()
        print('number of cluster found: ' + str(cl-1))
        outliers  = pointlabel.count(0)
        print('numbrer of outliers found: '+str(outliers) +'\n')