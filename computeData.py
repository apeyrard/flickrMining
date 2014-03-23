#!/usr/bin/env python2
# -*- coding: utf-8 -*-

print(__doc__)

import numpy as np
import pandas as pd
import json
from sklearn.cluster import MeanShift, estimate_bandwidth
from flask import Flask, render_template
app = Flask(__name__)
X = []
labels = []
cluster_centers = []

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

    labels_unique = np.unique(labels)

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

@app.route('/clusters')
def clusters():
    global cluster_centers
    return json.dumps(cluster_centers)

@app.route('/markers')
def markers():    
    global X
    global labels
    data = dict()
    for i, x in enumerate(X):
        data[i] = x + [labels[i]]
    return json.dumps(data)


if __name__ == '__main__':
    df = initialize()
    global X
    global labels
    global cluster_centers
    X, labels, cluster_centers = computeClusters(df)
    X = X.tolist()
    labels = labels.tolist()
    cluster_centers = cluster_centers.tolist()
    app.run(debug=True)

