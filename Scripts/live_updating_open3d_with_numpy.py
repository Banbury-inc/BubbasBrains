import open3d as o3d
import numpy as np
import cv2
import time
import torch
import tkinter as tk
import psutil
import threading


# Function to update system information
def update_info():
    cpu_load.set(f"CPU Load: {psutil.cpu_percent()}%")
    memory_load.set(f"Memory Load: {psutil.virtual_memory().percent}%")
    # You can add GPU load information using GPUtil or other GPU monitoring tools here
    # gpu_load.set(f"GPU Load: {get_gpu_load()}%")
    root.after(1000, update_info)  # Schedule the next update

# Function to start the GUI in a separate thread
def start_gui():
    global root, cpu_load, memory_load
    root = tk.Tk()
    root.title("System Monitor")
    
    # Variables to store system information
    cpu_load = tk.StringVar()
    memory_load = tk.StringVar()
    
    # Label widgets to display system information
    cpu_label = tk.Label(root, textvariable=cpu_load)
    memory_label = tk.Label(root, textvariable=memory_load)
    # Add a label for GPU load if needed
    # gpu_label = tk.Label(root, textvariable=gpu_load)
    
    # Pack labels into the window
    cpu_label.pack()
    memory_label.pack()
    # Pack GPU label if needed
    # gpu_label.pack()
    
    # Start updating system information
    update_info()

    root.mainloop()

# Start the GUI in a separate thread
gui_thread = threading.Thread(target=start_gui)
gui_thread.daemon = True  # Set the thread as a daemon so it exits when the main program exits
gui_thread.start()


# Initialize empty arrays
all_points_3D = [[0,0,0]]
all_colors = [[1,0,0]]


# Specify the path to your PLY files
ply_file_path1 = "pointCloudDeepLearning.ply"
ply_file_path2 = "pointCloud.ply"

# Load the PLY files into NumPy arrays
point_cloud1 = o3d.io.read_point_cloud(ply_file_path1)
point_cloud2 = o3d.io.read_point_cloud(ply_file_path2)

# Convert Open3D PointCloud objects to NumPy arrays
numpy_array1 = np.asarray(point_cloud1.points)
numpy_array2 = np.asarray(point_cloud2.points)

combined_points_3D = all_points_3D
combined_colors = all_colors

# Create an Open3D PointCloud object from your combined_points_3D
point_cloud = o3d.geometry.PointCloud()
point_cloud.points = o3d.utility.Vector3dVector(np.vstack(all_points_3D))
point_cloud.colors = o3d.utility.Vector3dVector(np.vstack(all_colors))



# Create images using Open3D
# (You can customize this part based on your specific visualization needs)
visualizer = o3d.visualization.Visualizer()
visualizer.create_window()
visualizer.add_geometry(point_cloud1)


iteration = 500

for i in range(iteration):
    visualizer.update_geometry(point_cloud1)
    visualizer.poll_events()
    visualizer.update_renderer()


visualizer.add_geometry(point_cloud2)
iteration2 = 500

for i in range(iteration2):
    visualizer.update_geometry(point_cloud1)
    visualizer.update_geometry(point_cloud2)
    visualizer.poll_events()
    visualizer.update_renderer()

visualizer.add_geometry(point_cloud)

# Q matrix - Camera parameters - Can also be found using stereoRectify
Q = np.array(([1.0, 0.0, 0.0, -160.0],
              [0.0, 1.0, 0.0, -120.0],
              [0.0, 0.0, 0.0, 350.0],
              [0.0, 0.0, 1.0/90.0, 0.0]),dtype=np.float32)


# Load a MiDas model for depth estimation
#model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
#model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

midas = torch.hub.load("intel-isl/MiDaS", model_type)

# Move model to GPU if available
device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
midas.to(device)
midas.eval()

# Load transforms to resize and normalize the image
midas_transforms = torch.hub.load("intel-isl/MiDaS", "transforms")

if model_type == "DPT_Large" or model_type == "DPT_Hybrid":
    transform = midas_transforms.dpt_transform
else:
    transform = midas_transforms.small_transform


# Open up the video capture from a webcam
cap = cv2.VideoCapture(0)

while cap.isOpened():

    success, img = cap.read()

    start = time.time()

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Apply input transforms
    input_batch = transform(img).to(device)

    # Prediction and resize to original resolution
    with torch.no_grad():
        prediction = midas(input_batch)

        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=img.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()

    depth_map = prediction.cpu().numpy()

    depth_map = cv2.normalize(depth_map, None, 0, 1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    #Reproject points into 3D
    points_3D = cv2.reprojectImageTo3D(depth_map, Q, handleMissingValues=False)


    #Get rid of points with value 0 (i.e no depth)
    mask_map = depth_map > 0.4

    #Mask colors and points. 
    output_points = points_3D[mask_map]
    output_colors = img[mask_map]

    # Append the current frame's points and colors to the arrays
    all_points_3D.append(output_points)
    all_colors.append(output_colors)
    
    # Combine all the collected point cloud data into single arrays
    combined_points_3D = np.vstack(all_points_3D)
    combined_colors = np.vstack(all_colors)

   # Update the geometry of the existing point cloud object
    point_cloud.points = o3d.utility.Vector3dVector(np.vstack(all_points_3D))
    point_cloud.colors = o3d.utility.Vector3dVector(np.vstack(all_colors))
    visualizer.poll_events()
    visualizer.update_renderer()


    end = time.time()

    totalTime = end - start

    fps = 1 / totalTime

    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    
    depth_map = (depth_map*255).astype(np.uint8)
    depth_map = cv2.applyColorMap(depth_map , cv2.COLORMAP_MAGMA)


    cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
    cv2.imshow('Image', img)
    cv2.imshow('Depth Map', depth_map)

    if cv2.waitKey(5) & 0xFF == 27:
        break


# Save the combined point cloud data as NumPy arrays
np.save("pointCloud3D.npy", combined_points_3D)
np.save("pointCloudColors.npy", combined_colors)





visualizer.destroy_window()  # Close the window when done
