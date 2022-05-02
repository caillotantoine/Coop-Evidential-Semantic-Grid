import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
from bbox import BoundingBox
from dataset_reader import *
from vec3 import vec3
from matrix_utils import getCwTc, left2RightHand
from threading import Thread, Lock
import matplotlib.animation as animation
from matplotlib.widgets import Slider

class State:
    datasets_folder: str
    """Path to the dataset folder"""
    dataset_name: str
    """Name of the dataset"""
    frame: int
    """Frame to observe"""
    mutex: Lock
    """Mutex to read and write the State object"""

    def __init__(self, datasets_folder: str = '/home/caillot/Documents/Datasets', dataset_name: str = 'CARLA_Dataset_A', frame: int = 180):
        self.datasets_folder = datasets_folder
        self.dataset_name = dataset_name
        self.frame = frame
        self.mutex = Lock()

    def read_vars(self) -> Tuple[str, str, int]:
        """
        Read the State object

        Returns:
            (str, str, int): (datasets_folder, dataset_name, frame)
        """
        self.mutex.acquire()
        datasets_folder = self.datasets_folder
        dataset_name = self.dataset_name
        frame = self.frame
        self.mutex.release()
        return datasets_folder, dataset_name, frame

def project_bbox3D_img(bbox:BoundingBox, camera_pose:np.ndarray, camera_matrix:np.ndarray, img:np.ndarray) -> np.ndarray:
    """
    Project a 3D bounding box in the image plane

    Args:
        bbox: BoundingBox object
        camera_pose: Camera pose
        camera_matrix: Camera matrix
        img: Image to draw on

    Returns:
        np.ndarray: Image with the bounding box projected
    """

    # Get the matrix to transform the points from the world referential to the camera referential
    cwTc = getCwTc()
    wTc = camera_pose @ cwTc
    cTw = np.linalg.inv(wTc)

    # Get the points of the bounding box in the world referential
    bbox_pts = bbox.get_point_world_RH()
    cam_pts:List[Tuple(int, int)] = []
    for pt in bbox_pts:
        # Transform the point from the world referential to the camera referential
        pt_cam_ref = cTw @ pt.get_array4()

        # if the point is behind the camera
        if pt_cam_ref[2] < 0:
            return img

        # Project the point in the image plane
        pt_cam = camera_matrix @ pt_cam_ref[:3,:]
        pt_cam = pt_cam / pt_cam[2] # Normalize the point (z = 1)

        # Convert the point to pixel coordinates
        cam_pts.append((int(pt_cam[0]), int(pt_cam[1])))

    # Draw the bounding box (some lines are forgotten and added later)
    for i in range(len(cam_pts)):
        cv.line(img, cam_pts[i], cam_pts[(i+1)%len(cam_pts)], (0,255,0), 2)

    # Add the extra lines to the bounding box
    cv.line(img, cam_pts[0], cam_pts[3], (0,255,0), 2)
    cv.line(img, cam_pts[2], cam_pts[5], (0,255,0), 2)
    cv.line(img, cam_pts[1], cam_pts[6], (0,255,0), 2)
    cv.line(img, cam_pts[4], cam_pts[7], (0,255,0), 2)

    return img
    


def draw_scene_oldDataset(state: State) -> np.ndarray:
    """
    Read the dataset and draw the scene

    Args:
        state: State object

    Returns:
        np.ndarray: Image of the scene
    """
    datasets_folder, dataset_name, frame = state.read_vars()

    V0_bbox = get_bbox(datasets_folder, dataset_name, 'V0', frame)
    V1_bbox = get_bbox(datasets_folder, dataset_name, 'V1', frame) 
    V2_camera_pose = get_camera_pose(datasets_folder, dataset_name, 'V2', frame)
    V2_camera_pose = left2RightHand(V2_camera_pose)
    k = get_camera_matrix(f'{datasets_folder}/{dataset_name}/Embed/V2/cameraRGB/cameraMatrix.npy')

    img = cv.imread(f'{datasets_folder}/{dataset_name}/Embed/V2/cameraRGB/{frame:06d}.png')
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    img = project_bbox3D_img(V0_bbox, V2_camera_pose, k, img)
    img = project_bbox3D_img(V1_bbox, V2_camera_pose, k, img)

    return img


def draw_scene_newDataset(state: State) -> np.ndarray:
    """
    Read the dataset and draw the scene

    Args:
        state: State object

    Returns:
        np.ndarray: Image of the scene
    """
    datasets_folder, dataset_name, frame = state.read_vars()

    V0_bbox = get_bbox(datasets_folder, dataset_name, 'V000', frame, old=False)
    V1_bbox = get_bbox(datasets_folder, dataset_name, 'V001', frame, old=False) 
    V2_camera_pose = get_camera_pose(datasets_folder, dataset_name, 'V002', frame, old=False)
    V2_camera_pose = left2RightHand(V2_camera_pose)
    k = get_camera_matrix(f'{datasets_folder}/{dataset_name}/V002/camera_rgb/cameraMatrix.npy')

    img = cv.imread(f'{datasets_folder}/{dataset_name}/V002/camera_rgb/{frame:06d}.png')
    img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

    img = project_bbox3D_img(V0_bbox, V2_camera_pose, k, img)
    img = project_bbox3D_img(V1_bbox, V2_camera_pose, k, img)

    return img

def draw_scene(state: State) -> np.ndarray:
    """
    Read the dataset and draw the scene

    Args:
        state: State object
    
    Returns:
        np.ndarray: Image of the scene
    """
    return draw_scene_newDataset(state)

def main():
    state = State()
    state.dataset_name = 'CARLA_Dataset_original'
    fig, ax = plt.subplots(2, gridspec_kw={'height_ratios': [7, 1]})
    # plt.ion()
    img = draw_scene(state)
    ax[0].imshow(img)

    # axamp = plt.axes([0.25, .03, 0.50, 0.02])
    samp = Slider(ax[1], 'frame', 51, 577, valinit=180, valfmt="%d")

    def update(val):
        state.mutex.acquire()
        state.frame = int(samp.val)
        state.mutex.release()
        img = draw_scene(state)
        ax[0].imshow(img)
        fig.canvas.draw_idle()


    samp.on_changed(update)
    # draw_scene(state)

    
    plt.show()
    

if __name__ == '__main__':
    main()