import cv2
import numpy as np
import open3d as o3d

# Initialize the camera capture (change the device index if necessary)
cap = cv2.VideoCapture(0)

# Create an Open3D PointCloud object to store the point cloud data
point_cloud = o3d.geometry.PointCloud()

while True:
    # Capture a frame from the camera
    ret, frame = cap.read()

    # Convert the frame to grayscale (optional)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Perform depth sensing or disparity mapping to obtain depth information (replace this with your depth estimation method)
    # For simplicity, this example assumes depth is obtained from the grayscale image
    depth = gray

    # Convert depth values to 3D coordinates
    rows, cols = depth.shape
    fx = fy = 500  # Focal lengths (adjust as needed)
    cx, cy = cols / 2, rows / 2  # Principal point (adjust as needed)
    scaling_factor = 0.1  # Adjust to scale depth values

    # Create a 3D point cloud from the depth information
    points = []
    for y in range(rows):
        for x in range(cols):
            z = depth[y, x] * scaling_factor
            if z > 0:
                x3d = (x - cx) * z / fx
                y3d = (y - cy) * z / fy
                points.append([x3d, y3d, z])

    # Add points to the Open3D PointCloud
    point_cloud.points = o3d.utility.Vector3dVector(points)

    # Visualize the point cloud (optional)
    o3d.visualization.draw_geometries([point_cloud])

    # Save the point cloud as a PLY file (you can change the filename)
  #  o3d.io.write_point_cloud("point_cloud.ply", point_cloud)

    # Exit the loop by pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the Open3D visualization window
cap.release()
cv2.destroyAllWindows()
