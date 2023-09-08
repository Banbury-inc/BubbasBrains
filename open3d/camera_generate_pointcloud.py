import open3d as o3d
import numpy as np
import cv2

# Initialize the Open3D visualizer
vis = o3d.visualization.Visualizer()
vis.create_window()

# Create an empty PointCloud object
pcd = o3d.geometry.PointCloud()

# Initialize the camera (you can replace this with your camera configuration)
camera = cv2.VideoCapture(0)  # Use the default camera (change index if needed)

try:
    while True:
        # Capture a frame from the camera
        ret, frame = camera.read()
        if not ret:
            break

        # Convert the RGB image into a numpy array
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create an Open3D Image from the RGB numpy array
        img = o3d.geometry.Image(rgb_image)

        # Access the width and height directly
        width = img.width
        height = img.height

        # Create a pinhole camera intrinsic (modify these values as per your camera)
        intrinsic = o3d.camera.PinholeCameraIntrinsic(
            width, height, 525.0, 525.0, width / 2, height / 2
        )

        # Create a RGBD image (depth information is not provided here)
        rgbd = o3d.geometry.RGBDImage.create_from_color_and_depth(
            img, o3d.geometry.Image(width, height, np.zeros((height, width), dtype=np.uint16))
        )

        # Create a point cloud from the RGBD image and camera intrinsic
        pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
            rgbd, intrinsic
        )

        # Update the Open3D visualizer
        vis.clear_geometries()
        vis.add_geometry(pcd)
        vis.update_geometry(pcd)
        vis.poll_events()
        vis.update_renderer()

except KeyboardInterrupt:
    pass

# Close the camera and Open3D visualizer
camera.release()
vis.destroy_window()
