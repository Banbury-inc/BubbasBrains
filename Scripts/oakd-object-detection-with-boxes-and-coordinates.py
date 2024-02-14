import blobconverter
import numpy as np
import depthai as dai
from depthai_sdk import OakCamera
from depthai_sdk.classes import Detections


def decode(nn_data: dai.NNData) -> Detections:
    """
    Custom decode function for the NN component. Decode function has to accept NNData argument.
    The return type should preferably be a class that inherits from depthai_sdk.classes.GenericNNOutput,
    which support visualization. But this is not required, i.e. the function can return arbitrary type.

    The decoded output can be accessed from the packet object in the callback function via packet.img_detections.
    """
    layer = nn_data.getFirstLayerFp16()
    results = np.array(layer).reshape((1, 1, -1, 7))
    dets = Detections(nn_data)
    for result in results[0][0]:
        if result[2] > 0.85:
            '''
            15 = person
            5 = bottle
            20 = tv monitor

            '''
            label = int(result[1])
            if label == 15:
                label = "Person"

            conf = result[2]
            bbox = result[3:]
            det = dai.ImgDetection()
            det.confidence = conf
            #det.label = label
            '''
            xmin, ymin, xmax, ymax

            xmin = how far left
            ymin = how far down
            xmax = how far right
            ymax = how far up

            for both xmin and xmax:
                0.00 = all the way to left
                0.99 = all the way to the right

            for both ymin and ymax:
                0.00 = all the way up
                0.99 = all the way down
            '''
            det.xmin = bbox[0]
            det.ymin = bbox[1]
            det.xmax = bbox[2]
            det.ymax = bbox[3]
            
            #print(f'xmin:{det.xmin} ymin:{det.ymin} xmax: {det.xmax} ymax: {det.ymax}')
            print(f'coordinates:{bbox} label: {label}')
            dets.detections.append(det)
        

            center_of_object = (det.xmax + det.xmin) / 2
            print(center_of_object)
            if center_of_object > 0.3: 
                if center_of_object < 0.7:
                    print("Object is in the center of the screen")
            if center_of_object < 0.3:
                    print("Object is on left side of screen")
            if center_of_object > 0.7:
                    print("Object is on right side of screen")








    return dets



with OakCamera() as oak:
    color = oak.create_camera('color')

    #nn_path = blobconverter.from_zoo(name='person-detection-0200', version='2021.4', shaves=6)
    nn_path = blobconverter.from_zoo(name='mobilenet-ssd', shaves=4)
    nn = oak.create_nn(nn_path, color, decode_fn=decode)
    oak.visualize(nn)
    oak.start(blocking=True)
