import numpy as np
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs

plt.figure(figsize=(12, 12))

n_samples = 1500
random_state = 170
X, y = make_blobs(n_samples=n_samples, random_state=random_state)

print X
print type(X)
print X.shape
print y
# Incorrect number of clusters
y_pred = KMeans(n_clusters=3, precompute_distances=True, random_state=3).fit_predict(X)

plt.subplot(221)
plt.scatter(X[:, 0], X[:, 1], c=y_pred)

plt.show()

print y_pred