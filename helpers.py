import numpy as np

C2N = {\
    'blue': 2,\
    'orange': 4,\
    'green': 5,\
    'red': 3,\
    'yellow': 6,\
    'white': 1,\
    ' ':''\
        }

N2C = {\
    2:'blue',\
    4:'orange',\
    5:'green',\
    3:'red',\
    6:'yellow',\
    1:'white',\
    '':' '\
    }

class face():
    def __init__(self,color,N=3):
        self.N = N
        self.state = np.array([[color for _ in range(N)] for _ in range(N)], dtype='object')
        self.type = type(color)

    def rotate(self, prime = False):
        """
        rotates a face in place
        """
        theta = np.radians(90 if prime else -90)
        
        rot_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                        [np.sin(theta), np.cos(theta)]], dtype=int)


        y_coords, x_coords = np.meshgrid(np.arange(self.N),np.arange(self.N))
        coords = np.vstack([x_coords.flatten(), y_coords.flatten()])

        c = (self.N/2 - 0.5) * np.ones_like(coords)
        rotated_coords = rot_matrix @ (coords- c) + c
        rotated_coords = rotated_coords.astype(int)

        self.state[rotated_coords[0], rotated_coords[1]] = self.state.flatten()

    def hor_flip(self):
        """
        flips face across y axis in place
        """
        self.state = np.array([[self.state[i,-(j+1)] for j in range(self.N)] for i in range(self.N)], dtype = 'object')

    def ver_flip(self):
        """
        flips face acros x axis in place
        """
        self.state = np.array([self.state[-1-i] for i in range(self.N)], dtype = 'object')
        
    def as_int(self):
        """
        converts entries to integer type
        """

        if self.type == int:
            return
        
        for i in range(self.N):
            for j in range(self.N):
                self.state[i,j] = C2N[self.state[i,j]]

        self.type = int
                
    def as_str(self):
        """
        converts entries to strings
        """

        if self.type == str:
            return
        
        for i in range(self.N):
            for j in range(self.N):
                self.state[i,j] = N2C[self.state[i,j]]

        self.type = str
    

def rotate(arr, prime = False):
    """
    rotates a face in place
    """
    N = len(arr)
    theta = np.radians(270 if prime else 90)
    
    rot_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                       [np.sin(theta), np.cos(theta)]], dtype=int)


    y_coords, x_coords = np.meshgrid(np.arange(N),np.arange(N))
    coords = np.vstack([x_coords.flatten(), y_coords.flatten()])

    c = (N/2 - 0.5) * np.ones_like(coords)
    rotated_coords = rot_matrix @ (coords- c) + c
    rotated_coords = rotated_coords.astype(int)

    arr[rotated_coords[0], rotated_coords[1]] = arr.flatten()

def hor_flip(arr):
    """
    flips face across y axis, not in place
    """
    N = len(arr)
    return [[arr[i,-(j+1)] for j in range(N)] for i in range(N)]

def ver_flip(arr):
    pass

if __name__=='__main__':
    N=3
    x = np.array(range(N**2)).reshape(N,N)
    print(x)
    rotate(x,False)
    print(x)