import numpy as np
import matplotlib.pyplot as plt
from collections import Counter


points = {"blue": [[2,4], [1,3], [2,3], [3,2], [2,1]], 
          "red": [[5,6], [4,5], [4,6], [6,6], [5,4]]}

new_point = [4,4]

def euclidean_distance(point1, point2):
    return np.sqrt(np.sum((np.array(point1) - np.array(point2)) ** 2))

class KNearestNeighbors:

    def __init__(self, k=3):
        self.k = k
        self.point = None

    def fit(self, points):
        self.points = points

    def predict(self, new_point):
        distances = []
        for category in self.points:
            for point in self.points[category]:
                distance = euclidean_distance(point, new_point)
                distances.append((distance, category))

        categories = [category[1] for category in sorted(distances)[:self.k]]
        result = Counter(categories).most_common(1)[0][0]
        return result
    
clf = KNearestNeighbors()
clf.fit(points)

print(clf.predict(new_point))

# Visualization
ax = plt.subplot()
ax.grid(True, color='#323232')
ax.figure.set_facecolor('#121212')
ax.tick_params(axis="x", colors='white')
ax.tick_params(axis="y", colors='white')

for point in points["blue"]:
    plt.scatter(point[0], point[1], color='blue', s=60)

for point in points["red"]:
    plt.scatter(point[0], point[1], color='red', s=60)

new_class = clf.predict(new_point)
color = '#FF0000' if new_class == "red" else '#104DCA'
ax.scatter(new_point[0], new_point[1], color=color, s=200, marker='*')

for point in points["blue"]:
    ax.plot([new_point[0], point[0]], [new_point[1], point[1]], color='#104DCA', linestyle='dashed', linewidth=1)

for point in points["red"]:
    ax.plot([new_point[0], point[0]], [new_point[1], point[1]], color='#FF0000', linestyle='dashed', linewidth=1)

plt.show()