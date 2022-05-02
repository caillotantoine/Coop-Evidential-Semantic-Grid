import numpy as np
from projection.vec3 import vec3
from typing import List
from projection.matrix_utils import left2RightHand

class BoundingBox:
    """Container for bounding boxes"""
    size:vec3
    """Size of the bounding box"""
    loc:vec3
    """Location of the bounding box from the center of the vehicle"""
    pose:np.ndarray
    """Pose of the vehicle"""

    def __str__(self) -> str:
        """Returns the bounding box as a string"""
        return f'Size : {self.size}, Loc: {self.loc}'

    def get_point_world_RH(self) -> List[vec3]:

        """
        Returns the points of the bounding box in world coordinates (righ hand, normalised after transformation).
        $$\\begin{bmatrix} x_{world} \\\\\\ y_{world} \\\\\\ z_{world} \\\\\\ 1\\end{bmatrix} = {^WT_V}\\cdot\\begin{bmatrix} x_{vehicle} \\\\\\ y_{vehicle} \\\\\\ z_{vehicle} \\\\\\ 1\\end{bmatrix}$$
        Points are normalized into a vec3 object.

        Returns:
            List[vec3]: List of points of the bounding box
        """
        
        out:List[vec3] = []
        pts = self.get_points() # Get the list of points
        wTv = left2RightHand(self.pose) # Get the transformation matrix right handded
        for pt in pts: # for each point
            p = vec3()
            pTrans = wTv @ pt.get_array4() # Transform the point from the vehicle to world
            # place the points in the vec3 format after normalisation (should be a division by 1)
            p.x = pTrans[0][0] / pTrans[3][0] 
            p.y = pTrans[1][0] / pTrans[3][0]
            p.z = pTrans[2][0] / pTrans[3][0]
            out.append(p) # Add the transformed and normalized point to the list
        return out

    def get_points(self) -> List[vec3]:
        """Returns the points of the bounding box
        
        Returns:
            List[vec3]: List of points of the bounding box
        """
        points = []
        pt = vec3()
        pt.x = self.loc.x - self.size.x
        pt.y = self.loc.y - self.size.y
        pt.z = self.loc.z - self.size.z
        points.append(pt)
        pt = vec3()
        pt.x = self.loc.x + self.size.x
        pt.y = self.loc.y - self.size.y
        pt.z = self.loc.z - self.size.z
        points.append(pt)
        pt = vec3()
        pt.x = self.loc.x + self.size.x
        pt.y = self.loc.y + self.size.y
        pt.z = self.loc.z - self.size.z
        points.append(pt)
        pt = vec3()
        pt.x = self.loc.x - self.size.x
        pt.y = self.loc.y + self.size.y
        pt.z = self.loc.z - self.size.z
        points.append(pt)


        pt = vec3()
        pt.x = self.loc.x - self.size.x
        pt.y = self.loc.y + self.size.y
        pt.z = self.loc.z + self.size.z
        points.append(pt)
        pt = vec3()
        pt.x = self.loc.x + self.size.x
        pt.y = self.loc.y + self.size.y
        pt.z = self.loc.z + self.size.z
        points.append(pt)
        pt = vec3()
        pt.x = self.loc.x + self.size.x
        pt.y = self.loc.y - self.size.y
        pt.z = self.loc.z + self.size.z
        points.append(pt)
        pt = vec3()
        pt.x = self.loc.x - self.size.x
        pt.y = self.loc.y - self.size.y
        pt.z = self.loc.z + self.size.z
        points.append(pt)
        return points


if __name__ == "__main__":
    """Unit test for BoundingBox"""
    bbox = BoundingBox()
    bbox.size = vec3()
    bbox.size.x = 1.0
    bbox.size.y = 1.0
    bbox.size.z = 1.0
    bbox.loc = vec3()
    bbox.loc.x = 0.0
    bbox.loc.y = 0.0
    bbox.loc.z = 0.0
    bbox.pose = np.array([[1.0, 0.0, 0.0, 0.0], [0.0, 1.0, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]])
    print(bbox)
    for pt in bbox.get_points():
        print(pt)