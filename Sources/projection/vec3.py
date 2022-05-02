import numpy as np

class vec3:
    """Container for 3D vectors"""
    x:float
    """X coordinate"""
    y:float
    """Y coordinate"""
    z:float
    """Z coordinate"""

    def get_array3(self):
        """Returns the vector as a numpy array"""
        return np.array([[self.x], [self.y], [self.z]])

    def get_array4(self):
        """Returns the vector as a numpy array"""
        return np.array([[self.x], [self.y], [self.z], [1]])

    def __str__(self) -> str:
        """Returns the vector as a string"""
        return f'<{self.x:.2e}, {self.y:.2e}, {self.z:.2e}>'