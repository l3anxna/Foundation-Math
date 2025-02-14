import numpy as np
import matplotlib.pyplot as plt
from skimage import io, color, filters

# 1. Load the image
image = io.imread(
    "/Users/arm/Downloads/manyhearts.jpeg"
)  # Replace with your image filename

# 2. Convert to grayscale
#    If there's an alpha channel, take only the first 3 channels (RGB).
if image.shape[-1] == 4:
    image = image[..., :3]  # discard alpha
gray = color.rgb2gray(image)

# 3. Apply Sobel filter to get gradient magnitude
edge_sobel = filters.sobel(gray)

# 4. Threshold the gradient magnitude to isolate edges
#    Adjust threshold as needed based on your image.
threshold = 0.2
edges = edge_sobel > threshold

# 5. Extract the coordinates of the edge points
edge_points = np.column_stack(np.nonzero(edges))

# 6. Display results
fig, axes = plt.subplots(1, 3, figsize=(12, 4))
axes[0].imshow(image)
axes[0].set_title("Original Image")
axes[0].axis("off")

axes[1].imshow(edge_sobel, cmap="gray")
axes[1].set_title("Sobel Gradient Magnitude")
axes[1].axis("off")

axes[2].imshow(edges, cmap="gray")
axes[2].set_title("Thresholded Edges")
axes[2].axis("off")

plt.tight_layout()
plt.show()

print("Number of edge points detected:", len(edge_points))
