"""
Unit Test for the Projector. We have found that the projection suffer of errors. 
Thus, in this file, we run a serie of unit tests in order to find and fix the problem. 
These unit tests are linked to the one foundable in the Playground/unit_test/projection folder.
"""

from utils.projector import project3Dpoint, getCwTc

from utils.Tmat import TMat
from utils.vector import *
from utils.agent import Agent

import numpy as np

from projection.bbox import BoundingBox as verif_Bbox
from projection.dataset_reader import get_bbox, get_camera_pose
from projection import matrix_utils

dataset_path = "/home/caillot/Documents/Datasets/CARLA_Dataset_original"


def UT_0000(frame=130):
    """
    Test reading the same values with previously made unit tests.
    """
    frame = 130
    vehicles:List[Agent] = []
    vehicles.append(Agent(dataset_path, 1))
    vehicles.append(Agent(dataset_path, 2))
    
    vehiclesUT:List[verif_Bbox] = []
    vehiclesUT.append(get_bbox('/home/caillot/Documents/Datasets/', 'CARLA_Dataset_original', 'V000', frame, old=False))
    vehiclesUT.append(get_bbox('/home/caillot/Documents/Datasets/', 'CARLA_Dataset_original', 'V001', frame, old=False))


    pov_agent = Agent(dataset_path=dataset_path, id=3) # V2 -> id = 3
    print(pov_agent)
    
    vehicles = [v.get_state(frame) for v in vehicles]
    bboxes = [v.get_bbox3d() for v in vehicles]
    pov_agent.get_state(frame)


    pov_agent_pose = pov_agent.get_sensor_pose(0)
    pov_agent_pose_v = matrix_utils.left2RightHand(get_camera_pose('/home/caillot/Documents/Datasets/', 'CARLA_Dataset_original', 'V002', frame, old=False))

    # verification de la matrice de transformation wTcw
    if np.allclose(pov_agent_pose_v, pov_agent_pose.get()):
        print("POV agent pose: \033[92mpassed\033[0m")
    else:
        print("POV agent pose: \033[91mFAILED\033[0m")
        print(pov_agent_pose_v)
        print(pov_agent_pose)
        return False

    
    cwTw_v = matrix_utils.getCwTc()
    cwTw = getCwTc()

    wTc = pov_agent_pose * cwTw
    cTw = wTc.inv()

    wTc_v = pov_agent_pose_v @ cwTw_v
    cTw_v = np.linalg.inv(wTc_v)

    # verification de la matrice de transformation cTw
    if np.allclose(cTw_v, cTw.get()):
        print("cTw: \033[92mpassed\033[0m")
    else:   
        print("cTw: \033[91mFAILED\033[0m")
        print(cTw_v)
        print(cTw)
        return False

    # verification de la lecture des BBox
    for i, _ in enumerate(bboxes):
        print(bboxes[i])
        # print(f'Tpose of type {type(bboxes[i].get_TPose())} with a value of \n{bboxes[i].get_TPose()}')
        print(vehiclesUT[i])
        bbox = bboxes[i].get_pts()
        bbox_v = vehiclesUT[i].get_points()
        for j in range(8):
            if not np.allclose(bbox[j].get(), bbox_v[j].get_array3()):
                print('Failed: bounding box are differents')
                print(bbox[j])
                print(bbox_v[j])
                return False
        
    # verification du placement des BBox dans le monde
    for i, _ in enumerate(bboxes):
        # print(bboxes[i])
        # print(vehiclesUT[i])
        bbox = bboxes[i].get_pts_world()
        bbox_v = vehiclesUT[i].get_point_world_RH()
        for j in range(8):
            if not np.allclose(bbox[j].get(), bbox_v[j].get_array3()):
                print('Failed: bounding box are positionned differently')
                print(bbox[j])
                print(bbox_v[j])
                return False

    # verification de lecture des matrice caméra
    krgb:TMat = pov_agent.get_kmat(raw=False, rgbcam=True)
    ksem:TMat = pov_agent.get_kmat(raw=False, rgbcam=False)
    
    if not np.allclose(krgb.get(), ksem.get()):
        print("K matrix are different: error")
        print(krgb)
        print(ksem)
        return False

    # Test entre matrice camera 4x4 et 3x3
    krgb3 = krgb.get()[:3,:3]
    print(krgb3)


    # Verification de la projection avec des matrices caméra differentes
    for i, _ in enumerate(bboxes):
        # print(bboxes[i])
        # print(vehiclesUT[i])
        bbox = bboxes[i].get_pts_world()
        for j in range(8):
            pt4 = bbox[j].vec4()

            pt_cam_ref = cTw * pt4
            pt_cam_ref_v = cTw_v @ pt4.get()

            if np.allclose(pt_cam_ref_v, pt_cam_ref.get()):
                print("pt_cam_ref: \033[92mpassed\033[0m")
            else:
                print("pt_cam_ref: \033[91mFAILED\033[0m")
                print(pt_cam_ref_v)
                print(pt_cam_ref)
                return False

            pt_cam = krgb * pt_cam_ref
            pt_cam3 = pt_cam.vec3()
            pt_cam2 = pt_cam3.nvec2()
            pt_cam_v = krgb3 @ pt_cam_ref_v[:3, :]
            pt_cam2_v = pt_cam_v[:2, :]/pt_cam_v[2, :]

            if np.allclose(pt_cam2_v, pt_cam2.get()):
                print("pt_cam2: \033[92mpassed\033[0m")
            else:
                print("pt_cam2: \033[91mFAILED\033[0m")
                print(pt_cam2_v)
                print(pt_cam2)
                return False

    
    return True

def UT_0001(frame=130):
    """Test the projection function

    Args:
        frame (int, optional): The frame to read. Defaults to 130.
    """
    vehicles:List[Agent] = []
    vehicles.append(Agent(dataset_path, 1))
    vehicles.append(Agent(dataset_path, 2))

    vehiclesUT:List[verif_Bbox] = []

    
    vehicles = [v.get_state(frame) for v in vehicles]
    bboxes = [v.get_bbox3d() for v in vehicles]

    pov_agent = Agent(dataset_path=dataset_path, id=3) # V2 -> id = 3
    pov_agent.get_state(frame)
    pov_agent_pose = pov_agent.get_sensor_pose(0)

    cwTw = getCwTc()
    wTc = pov_agent_pose * cwTw
    cTw = wTc.inv()

    krgb:TMat = pov_agent.get_kmat(raw=False, rgbcam=True)

    # Verification de la projection avec des matrices caméra differentes et entre Tmat et un np.array
    for i, _ in enumerate(bboxes):
        # print(bboxes[i])
        # print(vehiclesUT[i])
        bbox = bboxes[i].get_pts_world()
        for j in range(8):
            pt4 = bbox[j].vec4()
            pt_cam_ref = cTw * pt4
            pt_cam = krgb * pt_cam_ref
            pt_cam3 = pt_cam.vec3()
            pt_cam2 = pt_cam3.nvec2()

            pt_test = project3Dpoint(pt4, krgb, pov_agent_pose)

            if np.allclose(pt_test.get(), pt_cam2.get()):
                print("pt_cam2: \033[92mpassed\033[0m")
            else:
                print("pt_cam2: \033[91mFAILED\033[0m")
                print(pt_test)
                print(pt_cam2)
                return False
    return True


def main():
    failcnt = 0
    for i in range(100, 150, 1):
        if UT_0001(i):
            print(f"UT_0000 {i:02d}: \033[92mpassed\033[0m")
        else:
            print(f"UT_0000 {i:02d}: \033[91mFAILED\033[0m")
            failcnt = failcnt + 1
    print(f'Fail count: {failcnt}')
    

if __name__ == "__main__":
    main()