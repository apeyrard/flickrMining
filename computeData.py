#!/usr/bin/env python2
# -*- coding: utf-8 -*-

print(__doc__)

import numpy as np
import pandas as pd
import json
from sklearn.cluster import MeanShift, estimate_bandwidth
from flask import Flask, render_template
from modele import cluster

app = Flask(__name__)
X = []
labels = []
cluster_centers = []
clusterDict = dict()

def initialize():
    df = pd.read_csv('./data.csv', sep='\t')
    return df


def computeClusters(df):
    # select latitude and longitude
    X = df.ix[:, 7:9].values
    ###########################################################################
    # Compute clustering with MeanShift

    # The following bandwidth can be automatically detected using
    bandwidth = estimate_bandwidth(X, quantile=0.0005, n_samples=20000)

    ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=False)
    ms.fit(X)
    labels = ms.labels_
    cluster_centers = ms.cluster_centers_

    return X, labels, cluster_centers

def unique(a):
    order = np.lexsort(a.T)
    a = a[order]
    diff = np.diff(a, axis=0)
    ui = np.ones(len(a), 'bool')
    ui[1:] = (diff != 0).any(axis=1)
    return a[ui]


@app.route('/')
def mainHtml():
    return render_template('js.html')

@app.route('/data')
def markers():    
    global clusterDict
    return json.dumps([clusterDict[item].__dict__ for item in clusterDict.keys()])


if __name__ == '__main__':
    df = initialize()
    global X
    global labels
    global cluster_centers
    global clusterDict
    X, labels, cluster_centers = computeClusters(df)
    X = X.tolist()
    labels = labels.tolist()
    cluster_centers = cluster_centers.tolist()
    total = 0
    for i, item in enumerate(cluster_centers):
        print("adding" + str(i))
        clusterDict[i] = cluster(i, item[0], item[1])
        print(json.dumps(clusterDict[i].__dict__))

    for i, item in enumerate(X):
        if labels[i] != -1:
            clusterDict[labels[i]].addMarker([item[0], item[1]])
            print("adding" + str(item[0]) + str(item[1]) + " to " + str(labels[i]))
            total+=1
            print(total)
    app.run(debug=True)
