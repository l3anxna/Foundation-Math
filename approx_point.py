import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def trilaterate(anchors, distances):
    n = len(anchors)
    if n < 3:
        raise ValueError("Need at least 3 anchor points")
    
    x1, y1 = anchors[0]
    
    A = np.zeros((n-1, 2))
    b = np.zeros(n-1)
    
    for i in range(1, n):
        xi, yi = anchors[i]
        A[i-1, 0] = 2 * (xi - x1)
        A[i-1, 1] = 2 * (yi - y1)
        
        b[i-1] = distances[0]**2 - distances[i]**2 + xi**2 - x1**2 + yi**2 - y1**2
    
    solution, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    return solution

def compute_distances(anchors, true_point, noise_std=0):
    distances = []
    for anchor in anchors:
        dist = np.sqrt(np.sum((anchor - true_point)**2))
        if noise_std > 0:
            dist += np.random.normal(0, noise_std)
        distances.append(dist)
    return np.array(distances)

def visualize_trilateration(anchors, true_point, estimated_point, distances):
    plt.figure(figsize=(10, 8))
    
    plt.scatter(anchors[:, 0], anchors[:, 1], color='blue', marker='^', s=100, label='Anchors')
    
    plt.scatter(true_point[0], true_point[1], color='green', marker='o', s=100, label='True position')
    plt.scatter(estimated_point[0], estimated_point[1], color='red', marker='x', s=100, label='Estimated position')
    
    ax = plt.gca()
    for i, anchor in enumerate(anchors):
        circle = Circle(anchor, distances[i], fill=False, color='gray', alpha=0.3)
        ax.add_patch(circle)
    
    for anchor in anchors:
        plt.plot([estimated_point[0], anchor[0]], [estimated_point[1], anchor[1]], 'k--', alpha=0.3)
    
    error = np.sqrt(np.sum((true_point - estimated_point)**2))
    plt.title(f'2D Trilateration\nEstimation Error: {error:.4f}')
    
    plt.grid(True)
    plt.legend()
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def trilaterate_from_data(coordinates, distances):
    n = len(coordinates)
    if n < 3:
        raise ValueError("Need at least 3 anchor points")
    
    x1, y1 = coordinates[0][0], coordinates[0][1]
    
    A = np.zeros((n-1, 2))
    b = np.zeros(n-1)
    
    for i in range(1, n):
        xi, yi = coordinates[i][0], coordinates[i][1]
        A[i-1, 0] = 2 * (xi - x1)
        A[i-1, 1] = 2 * (yi - y1)
        
        b[i-1] = distances[0]**2 - distances[i]**2 + xi**2 - x1**2 + yi**2 - y1**2
    
    solution, residuals, rank, s = np.linalg.lstsq(A, b, rcond=None)
    return solution

if __name__ == "__main__":
    data = pd.read_csv('multilateration-data.csv', header=None)

    distances = data.iloc[:, 0].values
    coordinates = data.iloc[:, 1:4].values

    print('Distances:', distances)
    print('Coordinates of Detectors:', coordinates)

    estimated_position = trilaterate_from_data(coordinates, distances)
    
    print(f"Estimated position: {estimated_position}")

