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


    def __init__(self, datasets_folder: str = '/Users/caillotantoine/Datasets', dataset_name: str = 'CARLA_Dataset_A', frame: int = 180):
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
    cwTc = getCwTc()
    wTc = camera_pose @ cwTc
    cTw = np.linalg.inv(wTc)

    bbox_pts = bbox.get_point_world_RH()
    cam_pts:List[Tuple(int, int)] = []
    for pt in bbox_pts:
        cwTc = getCwTc() 
        wTc = camera_pose @ cwTc
        cTw = np.linalg.inv(wTc)

        print(pt)

        pt_cam_ref = cTw @ pt.get_array4()

        print(pt_cam_ref)

        pt_cam = camera_matrix @ pt_cam_ref[:3,:]
        pt_cam = pt_cam / pt_cam[2]

        cam_pts.append((int(pt_cam[0]), int(pt_cam[1])))

    for i in range(len(cam_pts)):
        cv.line(img, cam_pts[i], cam_pts[(i+1)%len(cam_pts)], (0,255,0), 2)

    cv.line(img, cam_pts[0], cam_pts[3], (0,255,0), 2)
    cv.line(img, cam_pts[2], cam_pts[5], (0,255,0), 2)
    cv.line(img, cam_pts[1], cam_pts[6], (0,255,0), 2)
    cv.line(img, cam_pts[4], cam_pts[7], (0,255,0), 2)

    # vec0 = vec3()
    # vec0.x = 0.0
    # vec0.y = 0.0
    # vec0.z = 0.7

    # wTv =  left2RightHand(bbox.pose)
    # v_center = wTv @ vec0.get_array4()

    # v_cam = cTw @ v_center

    # v_image = camera_matrix @ v_cam[:3,:]
    # v_image = v_image / v_image[2]

    # cv.circle(img, (int(v_image[0]), int(v_image[1])), 30, (0,0,255), -1)

    return img
    


def draw_scene(state: State) -> np.ndarray:
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


def main():
    state = State()
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