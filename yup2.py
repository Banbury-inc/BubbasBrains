import cv2
import open3d as o3d
import subprocess
import time
import numpy as np
import torch
def first():
    visualizer = o3d.visualization.Visualizer()
    visualizer.create_window()
    

    pointcloud = "pointCloud.ply"
    point_cloud = o3d.io.read_point_cloud(pointcloud)
    # Create a Visualizer instance
    
    # Add the point cloud to the visualizer
    
    visualizer.add_geometry(point_cloud)
#    vertices = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
#    colors = np.array([[255, 0, 0], [0, 255, 0]])
#    ply_data = create_output(vertices, colors)
#    pointcloud2 = ply_data
#    point_cloud2 = o3d.io.read_point_cloud(pointcloud2)
#    visualizer.add_geometry(point_cloud2)

    time.sleep(20)
    return visualizer

def initialize(visualizer):

    # Q matrix - Camera parameters - Can also be found using stereoRectify
    Q = np.array(([1.0, 0.0, 0.0, -160.0],
                [0.0, 1.0, 0.0, -120.0],
                [0.0, 0.0, 0.0, 350.0],
                [0.0, 0.0, 1.0/90.0, 0.0]),dtype=np.float32)


    # Load a MiDas model for depth estimation
    model_type = "DPT_Large"     # MiDaS v3 - Large     (highest accuracy, slowest inference speed)
    #model_type = "DPT_Hybrid"   # MiDaS v3 - Hybrid    (medium accuracy, medium inference speed)
    #model_type = "MiDaS_small"  # MiDaS v2.1 - Small   (lowest accuracy, highest inference speed)

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

        #Mask colors and points 
        output_points = points_3D[mask_map]
        output_colors = img[mask_map]

        end = time.time()
        totalTime = end - start

        fps = 1 / totalTime

        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        
        depth_map = (depth_map*255).astype(np.uint8)
        depth_map = cv2.applyColorMap(depth_map , cv2.COLORMAP_MAGMA)


        cv2.putText(img, f'FPS: {int(fps)}', (20,70), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0,255,0), 2)
        cv2.imshow('Image', img)
        cv2.imshow('Depth Map', depth_map)

        # Example usage:
        vertices = np.array([[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]])
        colors = np.array([[255, 0, 0], [0, 255, 0]])
        ply_data = create_output(vertices, colors)
        pointcloud = "pointCloudDeepLearning.ply"
        
        # Load the PLY file
        point_cloud = o3d.io.read_point_cloud(pointcloud)
        point_cloud2 = o3d.io.read_point_cloud(ply_data)
        # Now, 'ply_data' contains the point cloud data as a string
        print(ply_data)

        visualizer.update_geometry(point_cloud2)
        visualizer.poll_events()
        visualizer.update_renderer()


        if cv2.waitKey(5) & 0xFF == 27:
            break



# --------------------- Create The Point Clouds ----------------------------------------

# Function to create point cloud data as a string
def create_output(vertices, colors):
    colors = colors.reshape(-1, 3)
    vertices = np.hstack([vertices.reshape(-1, 3), colors])

    ply_header = '''ply
    format ascii 1.0
    element vertex %(vert_num)d
    property float x
    property float y
    property float z
    property uchar red
    property uchar green
    property uchar blue
    end_header
    '''

    ply_data = (ply_header % dict(vert_num=len(vertices))) + '\n'.join([' '.join(map(str, row)) for row in vertices])
    return ply_data


def main():
    visualizer = first()
    # initialize(visualizer)


if __name__ == "__main__":
    main()
