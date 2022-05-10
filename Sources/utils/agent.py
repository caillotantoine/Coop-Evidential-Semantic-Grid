import json
import numpy as np
from utils.Tmat import TMat
from utils.bbox import Bbox2D, Bbox3D
from utils.vector import vec2, vec3, vec4
from typing import List, Tuple
import cv2 as cv
from tqdm import tqdm

import utils.projector as prj
import matplotlib.pyplot as plt

class Agent:
    def __init__(self, dataset_path:str, id:int) -> None:
        self.dataset_path:str = dataset_path
        self.dataset_json_path:str = dataset_path + f'/information.json'
        self.Tpose:TMat = TMat()
        self.sensorTPoses:List[TMat] = []
        self.bbox3d:Bbox3D = None
        self.myid = id

        with open(self.dataset_json_path) as dataset_json:
            info = json.load(dataset_json)
            agents = info['agents']

            self.mypath:str = self.dataset_path + '/' + agents[id]['path']
            self.label:str = agents[id]['type']

    def __str__(self):
        return f'{self.label} @ {self.mypath}'

    def get_state(self, frame:int): 
        jsonpath = self.mypath  + f'infos/{frame:06d}.json'
        # print(jsonpath)
        with open(jsonpath) as f:
            state_json = json.load(f)

            #
            #   Get pose of the agent
            #
            if self.label == "vehicle":
                pose = np.array(state_json['vehicle']['T_Mat'])
                self.Tpose.set(pose)
                self.Tpose.handinessLeft2Right()

            elif self.label == "pedestrian":
                pose = np.array(state_json['sensors'][0]['T_Mat'])
                self.Tpose.set(pose)
                self.Tpose.handinessLeft2Right()

            elif self.label == "infrastructure":
                self.Tpose = None


            #
            #   Get pose of the sensors
            #
            if self.label == "vehicle" or self.label == "infrastructure":
                self.sensorTPoses.clear()
                for sens in state_json["sensors"]:
                    pose = np.array(sens['T_Mat'])
                    out = TMat()
                    out.set(pose)
                    out.handinessLeft2Right()
                    self.sensorTPoses.append(out)

            #                       
            #   Get bounding box   /!\  MUST BE RELATED WITH Agent's pose.
            #                     
            if self.label == "vehicle" or self.label == "pedestrian":
                raw_bbox = state_json["vehicle"]["BoundingBox"]
                sx = raw_bbox["extent"]["x"]
                sy = raw_bbox["extent"]["y"]
                sz = raw_bbox["extent"]["z"]
                ox = raw_bbox["loc"]["x"] - sx
                oy = raw_bbox["loc"]["y"] - sy
                oz = raw_bbox["loc"]["z"] - sz
                bboxsize = vec3(sx*2.0, sy*2.0, sz*2.0)
                bbox_pose = vec3(ox, oy, oz)
                self.bbox3d = Bbox3D(bbox_pose, bboxsize, self.label)
                self.bbox3d.set_TPose(self.Tpose)


                #   Fix the Tpose for pedestrian (they're flying)    
                if self.label == "pedestrian":
                    self.Tpose.tmat[2,3] = sz
        return self

        # DEBUG
        #
        # print(self.bbox3d)
        # print(self.Tpose)
        # for s in self.sensorTPoses:
        #     print(s)

    # def get_bbox_w(self):
    #     return self.Tpose * self.bbox3d

    def get_bbox3d(self) -> Bbox3D:
        return self.bbox3d

    def get_pose(self) -> TMat:
        return self.Tpose

    # def get_rgb(self, frame=None) -> np.ndarray:
    #     if frame == None:
    #         return None
    #     img = cv.imread(f'{self.mypath}camera_rgb/{frame:06d}.png')
    #     return img

    def get_pred(self, frame:int) -> List[Bbox3D]:
        self.get_state(frame)
        if self.label == "pedestrian":
            raise Exception("Pedestrian do not have sensors.")
        pred_path = f"{self.mypath}/Prediction/{frame:06d}.json"
        print(self.mypath)
        # print(pred_path)
        with open(pred_path) as json_file:
            jsonData = json.load(json_file)
            # print(jsonData)
            cnt = 0
            boxes:List[Bbox3D] = []
            while True:
                try: 
                    dim = np.array(jsonData[f"{cnt}"]["dimensions (whl)"], dtype=float)
                    label = "vehicle" if jsonData[f"{cnt}"]["class"] == "car" else jsonData[f"{cnt}"]["class"]
                    Tpose = np.array(jsonData[f"{cnt}"]["K_obj2world"], dtype=float)
                    cnt += 1

                    bbox = Bbox3D(vec3(Tpose[0][3], Tpose[1][3], Tpose[2][3]), vec3(dim[0], dim[1], dim[2]), label=label)
                    bbox_pose = TMat()
                    bbox_pose.set(Tpose)
                    bbox.set_TPose(bbox_pose)
                    boxes.append(bbox)
                    # print(dim)
                    # print(label)
                    # print(Tpose)
                except Exception as e:
                    break
            return boxes
        return None

    def get_kmat(self, raw=False, rgbcam=False) -> np.ndarray or TMat:
        """Get the camera matrix of the agent.

        Args:
            raw (bool, optional): Output a np.ndarray format. Defaults to False.
            rgbcam (bool, optional): read the rgb cam matrix of the segmentation semantic camera matrix. Defaults to False.

        Returns:
            np.ndarray or TMat: Camera matrix of the agent.
        """
        if rgbcam:
            kmat_path = self.mypath + "/camera_rgb/cameraMatrix.npy"
        else:
            kmat_path = self.mypath + "/camera_semantic_segmentation/cameraMatrix.npy"
        k_mat = prj.load_k(kmat_path, raw)
        return k_mat

    def get_sensor_pose(self, id:int) -> TMat:
        """Get the pose of one of the agent's sensor

        Args:
            id (int): the id of the sensor

        Returns:
            TMat: the pose of the sensor
        """
        if id == None:
            raise ValueError("id must be an integer")
        if id >= len(self.sensorTPoses):
            raise ValueError(f"Sensor id {id} is out of range.")
        return self.sensorTPoses[id]

    def get_sem(self, frame:int) -> np.ndarray:
        """Read the image of the semantic segmentation folder

        Args:
            frame (int): frame number

        Returns:
            np.ndarray: image
        """
        if frame == None:
            raise ValueError("Frame number must be specified.")
        return cv.imread(self.mypath+f'camera_semantic_segmentation/{frame:06d}.png') 

    def get_rgb(self, frame:int) -> np.ndarray:
        """Read the image of the rgb folder

        Args:
            frame (int): frame number

        Returns:
            np.ndarray: image
        """
        if frame == None:
            raise ValueError("Frame number must be specified.")
        return cv.cvtColor(cv.imread(self.mypath+f'camera_rgb/{frame:06d}.png'), cv.COLOR_BGR2RGB)


    def get_visible_bbox(self, frame:int, plot:plt = None, drawBBOXonImg=False, bbox_noise=(0.0, 0.0, 0.0, 0.0)) -> Tuple[List[Bbox2D], TMat, TMat, str, np.ndarray]:
        """
        get the visible bounding box from the agent's perspective.
        """
        if self.label == "pedestrian":
            raise Exception("Pedestrian do not have sensors.")
        k_mat = self.get_kmat()

        self.get_state(frame)
        camPose = self.get_sensor_pose(0)

        with open(self.dataset_json_path) as dataset_json:
            raw_json = json.load(dataset_json)

            #every idx where idx != my id and where type is not an infrastructure
            visible_user_idx:int = [idx for idx, data in enumerate(raw_json["agents"]) if (data["type"]!="infrastructure" and idx != self.myid)]
            agents = [Agent(self.dataset_path, idx) for idx in visible_user_idx]
            for agent in agents:
                agent.get_state(frame)

            img = cv.imread(self.mypath+f'camera_semantic_segmentation/{frame:06d}.png') 

            bbox2:List[Bbox2D] = []
            bbox3pts:List[List[vec2]] = []
            for a in agents:
                a.get_state(frame)
                # print(f'Frame {frame} - {a}')
                projected = prj.projector_filter(a.get_bbox3d(), a.get_pose(), k_mat, camPose, img)
                if projected is None:
                    continue

                (bbox, points) = projected
                bbox3pts.append(points)
                # ======================= ADD NOISE : hjdfhjbjhbvfbjhbqsdf

                (pose_noise, size_noise, class_noise, drop_probability) = bbox_noise
                # pose_noise = 0.10
                # size_noise = 0.10
                # class_noise = 0.3
                # drop_probability = 0.3

                # random.uniform = [0, 1.0) Uniform distribution
                # 1 - [0, 1.0) = [1.0, 0.0)
                # [1.0, 0.0) < 10% -> 10% drop 90% pass
                if 1-np.random.uniform() < drop_probability:
                    continue

                if 1-np.random.uniform() < class_noise:
                    if bbox.label == "vehicle":
                        bbox.label = "pedestrian"
                    elif bbox.label == "pedestrian":
                        bbox.label = "vehicle"
                    else:
                        pass
                
                size:vec2 = bbox.get_size()
                bbox.set_size(vec2(x=np.random.normal(size.x(), size.x()*size_noise), y=np.random.normal(size.y(), size.y()*size_noise)))

                pose:vec2 = bbox.get_pose()
                bbox.set_pose(vec2(x=np.random.normal(pose.x(), size.x()*pose_noise), y=np.random.normal(pose.y(), size.y()*pose_noise)))

                # ======================= ADD NOISE : hjdfhjbjhbvfbjhbqsdf
                bbox2.append(bbox)
                

            # (w,h) = np.shape(img)
            h, w,_ = img.shape

            camBBox = Bbox2D(vec2(0, 0), vec2(w, h), label='terrain')
                
            bbox2 = [box for box in bbox2 if box != None]
            bbox2.insert(0, camBBox)
            # print(bbox2)
            
            img = cv.imread(self.mypath+f'camera_rgb/{frame:06d}.png')
            img = cv.cvtColor(img, cv.COLOR_BGR2RGB)

            if drawBBOXonImg:
                # Bounding box 2D
                color = (0, 255, 0)
                thickness = 2
                for box in bbox2:
                    if box.label == 'vehicle':
                        color = (0, 255, 0)
                    elif box.label == 'pedestrian':
                        color = (255, 128, 0)
                    else:
                        color = (255, 0, 0)
                    points = box.get_pts()
                    pts = [tuple(np.transpose(pt.get())[0].astype(int).tolist()) for pt in points]
                    # print(pts)
                    for i in range(len(pts)):
                        img = cv.line(img, pts[i], pts[(i+1)%len(pts)], color, thickness)

                # Bounding box 3D
                color = (0, 0, 255)
                thickness = 1
                for points in bbox3pts:
                    pts = [tuple(np.transpose(pt.get())[0].astype(int).tolist()) for pt in points]
                    # print(pts)
                    for i in range(len(pts)):
                        img = cv.line(img, pts[i], pts[(i+1)%len(pts)], color, thickness)

            if plot is not None:                    
                plot.imshow(img)
                plot.draw()
                plt.pause(0.001)

            return (bbox2, k_mat, camPose, self.label, img)
                


if __name__ == "__main__":
    dataset_path:str = '/home/caillot/Documents/Dataset/CARLA_Dataset_B'
    v0 = Agent(dataset_path=dataset_path, id=18)
    print(v0)
    # v0.get_state(56)
    for i in tqdm(range(1, 100)):
        # v0.get_visible_bbox(i)
        print(v0.get_pred(i))
        
    
    # cv.waitKey(0)
    # cv.destroyAllWindows()