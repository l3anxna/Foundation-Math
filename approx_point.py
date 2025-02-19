import numpy as np
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
    
    plt.scatter(anchors[:, 0], anchors[:, 1], color='orange', marker='^', s=100, label='Anchors')
    
    plt.scatter(true_point[0], true_point[1], color='blue', marker='o', s=100, label='True position')
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
    plt.savefig('trilateration.png')
    plt.show()

if __name__ == "__main__":
    anchors = np.array([
        [0, 0],
        [10, 0],
        [5, 8],
        [2, 6]
    ])
    
    true_point = np.array([4, 4])
    
    print("=== Test with no noise ===")
    exact_distances = compute_distances(anchors, true_point, noise_std=0)
    exact_estimation = trilaterate(anchors, exact_distances)
    exact_error = np.sqrt(np.sum((true_point - exact_estimation)**2))
    
    print(f"True position: {true_point}")
    print(f"Estimated position: {exact_estimation}")
    print(f"Error: {exact_error:.4f}")
    
    visualize_trilateration(anchors, true_point, exact_estimation, exact_distances)
    
    print("\n=== Test with noise ===")
    noise_level = 0.1
    noisy_distances = compute_distances(anchors, true_point, noise_std=noise_level)
    noisy_estimation = trilaterate(anchors, noisy_distances)
    noisy_error = np.sqrt(np.sum((true_point - noisy_estimation)**2))
    
    print(f"True position: {true_point}")
    print(f"Estimated position (with noise={noise_level}): {noisy_estimation}")
    print(f"Error: {noisy_error:.4f}")
    
    visualize_trilateration(anchors, true_point, noisy_estimation, noisy_distances)
    
    print("\n=== Experimenting with different noise levels ===")
    noise_levels = [0, 0.01, 0.1, 0.5, 1.0]
    errors = []
    
    for noise in noise_levels:
        noisy_distances = compute_distances(anchors, true_point, noise_std=noise)
        est_point = trilaterate(anchors, noisy_distances)
        error = np.sqrt(np.sum((true_point - est_point)**2))
        errors.append(error)
        print(f"Noise level: {noise:.2f}, Error: {error:.4f}")
    
    plt.figure(figsize=(8, 5))
    plt.plot(noise_levels, errors, 'o-')
    plt.xlabel('Noise Level (std)')
    plt.ylabel('Position Error')
    plt.title('Trilateration Error vs. Measurement Noise')
    plt.grid(True)
    plt.savefig('trilateration_error_vs_noise.png')
    plt.show()
