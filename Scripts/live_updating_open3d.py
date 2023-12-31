
import open3d as o3d
import subprocess
import time

# Define the file paths of the Python scripts you want to run
script1_path = "video_to_pointcloud_no_output.py"
script2_path = "visualize_ply_file_in_open3d.py"
pointcloud = "pointCloudDeepLearning.ply"
pointcloud2 = "pointCloud.ply"



# Specify the path to your PLY file
ply_file_path = 'your_point_cloud.ply'  # Replace with your file path

# Load the PLY file
point_cloud = o3d.io.read_point_cloud(pointcloud)
point_cloud2 = o3d.io.read_point_cloud(pointcloud2)


# Create a Visualizer instance
visualizer = o3d.visualization.Visualizer()
# Add the point cloud to the visualizer
visualizer.create_window()
visualizer.add_geometry(point_cloud)

#visualizer.add_geometry(point_cloud2)

iteration = 100

for i in range(iteration):
    visualizer.update_geometry(point_cloud)
    visualizer.poll_events()
    visualizer.update_renderer()

point_cloud = o3d.io.read_point_cloud(pointcloud2)
visualizer.add_geometry(point_cloud)


iteration2 = 100
for i in range(iteration2):

    visualizer.update_geometry(point_cloud)
    visualizer.poll_events()
    visualizer.update_renderer()



visualizer.destroy_window()  # Close the window when done
