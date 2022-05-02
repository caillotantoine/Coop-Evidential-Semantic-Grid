import numpy as np
from scipy.spatial.transform import Rotation as R

def left2RightHand(Tmat:np.ndarray) -> np.ndarray:
    """
    Transform a transformation matrix from left hand to right hand

    - $$y = -y$$
    - $$rot(x) = -rot(x)$$
    - $$rot(z) = -rot(z)$$
    
    Args:
        Tmat (np.ndarray): Transformation matrix, left hand
    
    Returns:
        np.ndarray: Transformation matrix from right hand
    """

    out = Tmat.copy()

    r = R.from_matrix(Tmat[:3, :3])
    r_euler = R.as_euler(r, 'xyz')
    out[1, 3] = -Tmat[1, 3]
    r_euler[0]=- r_euler[0]
    r_euler[2]=- r_euler[2]
    out[:3, :3] = R.from_euler('xyz', r_euler).as_matrix()

    return out

def getCwTc() -> np.ndarray:
    """
    Get the transformation matrix from the camera to the world frame

    $$^{C_W}T_C = \\begin{pmatrix}0   & 0     & 1     & 0  \\\\\\ -1   & 0     & 0     & 0 \\\\\\ 0   & -1    & 0     & 0     \\\\\\ 0   & 0     & 0     & 1 \\end{pmatrix}$$

    Returns:
        np.ndarray: Transformation matrix from the camera to the world frame
    """
    # matout = np.array([[0.0,   -1.0,   0.0,   0.0,], [0.0,   0.0,  -1.0,   0.0,], [1.0,   0.0,   0.0,   0.0,], [0.0,   0.0,   0.0,   1.0,]])
    matout = np.array([[0.0,   0.0,   1.0,   0.0,], [-1.0,   0.0,  0.0,   0.0,], [0.0,   -1.0,   0.0,   0.0,], [0.0,   0.0,   0.0,   1.0,]])
    return matout