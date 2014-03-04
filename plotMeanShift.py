#!/usr/bin/env python2
# -*- coding: utf-8 -*-

print(__doc__)

import numpy as np
import pandas as pd
import pygmaps
import webbrowser
from sklearn.cluster import MeanShift, estimate_bandwidth
from random import sample

###############################################################################
# Read data
df = pd.read_csv('./cleanedData.csv', encoding='latin1')

# select latitude and longitude
X = df[['longitude', 'latitude']].values
###############################################################################
# Compute clustering with MeanShift

# The following bandwidth can be automatically detected using
bandwidth = estimate_bandwidth(X,quantile = 0.0001, n_samples=20000)

ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
ms.fit(X)
labels = ms.labels_
cluster_centers = ms.cluster_centers_

labels_unique = np.unique(labels)
n_clusters_ = len(labels_unique)

print("number of estimated clusters : %d" % n_clusters_)

mymap = pygmaps.maps(45.45, 4.5, 10)
#X = sample(X, 10000)


def unique(a):
    order = np.lexsort(a.T)
    a = a[order]
    diff = np.diff(a, axis=0)
    ui = np.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1)
    return a[ui]
print(len(X))
X = unique(X)
print(len(X))

for item in X:
    print(item[1], item[0])
    mymap.addradpoint(item[1], item[0], 10, "#0000FF")
for item in cluster_centers:
    mymap.addradpoint(item[1], item[0], 10, "#FF00FF")
mymap.draw('./mymap.draw.html')
url = './mymap.draw.html'
webbrowser.get('chromium').open_new_tab(url)
