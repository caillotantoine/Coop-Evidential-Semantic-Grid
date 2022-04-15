import json
import numpy as np
from typing import List, Tuple
from vec3 import vec3
from bbox import BoundingBox

def get_camera_matrix(file_path:str) -> np.ndarray:
    """
    Get the camera matrix of a camera.
    $$k=\\begin{pmatrix}692.& 0.& 692.\\\\\\ 0. & 692. & 516. \\\\\\  0. & 0. & 1. \\end{pmatrix}$$

    Args:
        file_path (str): Path to the camera calibration file
    
    Returns:
        np.ndarray: Camera matrix (3x3)
    """
    return np.load(file_path)

def get_bbox(datasets_folder:str, dataset_name:str, vehicle:str, frame:int) -> BoundingBox:
    """
    Get the bounding box of a vehicle in a frame

    Args:
        vehicle (str): Name of the vehicle (e.g. 'V0')
        frame (int): Frame to observe
    
    Returns:
        BoundingBox: Bounding box of the vehicle in the frame containing the transformation matrix of the vehicle in the world frame (left handed)
         
    """
    with open(f'{datasets_folder}/{dataset_name}/Embed/{vehicle}/VehicleInfo/{frame:06d}.json') as f:
        rawdata = json.load(f)

    vehicle_pose = np.array(rawdata["vehicle"]["T_Mat"])
    """Transformation matrix from the vehicle frame to the world frame, left handed"""
    extent = vec3()
    extent.x = rawdata["vehicle"]["BoundingBox"]["extent"]["x"]
    extent.y = rawdata["vehicle"]["BoundingBox"]["extent"]["y"]
    extent.z = rawdata["vehicle"]["BoundingBox"]["extent"]["z"]

    loc = vec3()
    loc.x = rawdata["vehicle"]["BoundingBox"]["loc"]["x"]
    loc.y = rawdata["vehicle"]["BoundingBox"]["loc"]["y"]
    loc.z = rawdata["vehicle"]["BoundingBox"]["loc"]["z"]

    bbox = BoundingBox()
    bbox.size = extent
    bbox.loc = loc
    bbox.pose = vehicle_pose

    return bbox

def get_camera_pose(datasets_folder:str, dataset_name:str, vehicle:str, frame:int) -> np.ndarray:
    """
    Get the camera pose of a vehicle in a frame

    Args:
        vehicle (str): Name of the vehicle (e.g. 'V0')
        frame (int): Frame to observe
    
    Returns:
        np.ndarray: Transformation matrix from the camera to the vehicle frame (left handed)
    """
    with open(f'{datasets_folder}/{dataset_name}/Embed/{vehicle}/VehicleInfo/{frame:06d}.json') as f:
        rawdata = json.load(f)

    camera_pose = np.array(rawdata["sensor"]["T_Mat"])
    """Transformation matrix from the vehicle frame to the world frame, left handed"""
    return camera_pose

if __name__ == "__main__":
    datasets_folder = '/Users/caillotantoine/Datasets' 
    """Path to the dataset folder"""
    dataset_name = 'CARLA_Dataset_A'
    """Name of the dataset"""
    frame = 180
    """Frame to observe"""

    vehicle = 'V0'
    """Name of the vehicle (e.g. 'V0')"""

    bbox = get_bbox(datasets_folder, dataset_name, vehicle, frame)

    print(bbox)
    print(bbox.pose)