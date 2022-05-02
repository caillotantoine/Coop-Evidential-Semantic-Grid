"""
Unit Test for the Projector. We have found that the projection suffer of errors. 
Thus, in this file, we run a serie of unit tests in order to find and fix the problem. 
These unit tests are linked to the one foundable in the Playground/unit_test/projection folder.
"""

from anyio import fail_after
from utils.projector import project3Dpoint, getCwTc

from utils.Tmat import TMat
from utils.vector import *
from utils.agent import Agent

import numpy as np

from projection.bbox import BoundingBox as verif_Bbox
from projection.dataset_reader import get_bbox

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
        
    # print("WORLD REF")
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

    krgb = pov_agent.get_kmat(raw=True, rgbcam=True)
    ksem = pov_agent.get_kmat(raw=True, rgbcam=False)
    
    if not np.allclose(krgb, ksem):
        print("K matrix are different: error")
        print(krgb)
        print(ksem)
        return False
    return True

def main():
    failcnt = 0
    for i in range(100, 150, 1):
        if UT_0000(i):
            print(f"frame {i:02d}: \033[92mpassed\033[0m")
        else:
            print(f"frame {i:02d}: \033[91mFAILED\033[0m")
            failcnt = failcnt + 1
    print(f'Fail count: {failcnt}')
    

if __name__ == "__main__":
    main()