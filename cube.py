import numpy as np
import tabulate

from helpers import face



class rubiks_cube():

    def __init__(self, N=3):
        """
        self.left, self.front, self.right and self.up ordered as though looking squarely at the face
        self.down is oriented so that self.front would be on top
        self.back is oriented as though looking through a transparent front
        """
        self.N = N

        self.front = face('blue', self.N)
        self.back = face('green', self.N)
        self.left = face('orange', self.N)
        self.right = face('red', self.N)
        self.up = face('yellow', self.N)
        self.down = face('white', self.N)
        self.empty = face(' ' , self.N)
        self.faces = [self.front, self.back, self.left, self.right, self.up, self.down, self.empty]
        self.state = str

    def show_state(self):
        """
        prints the current state of the cube as though opened as a net
        cross point is the front face
        """
        row1 = np.concatenate((self.empty.state, self.back.state, self.empty.state), axis = 1)
        row2 = np.concatenate((self.empty.state, self.up.state, self.empty.state), axis = 1)
        row3 = np.concatenate((self.left.state, self.front.state, self.right.state), axis = 1)
        row4 = np.concatenate((self.empty.state, self.down.state, self.empty.state), axis = 1)
        state = np.concatenate((row1, row2, row3, row4))
        table = tabulate.tabulate(state,stralign = 'center', numalign = 'center',tablefmt='plain')
        print(table, '\n')

    def as_int(self):
        """
        converts tile names to integers
        """
        if self.state == int:
            return
        for face in self.faces:
            face.as_int()

    def as_str(self):
        """
        convers tile names to integers
        """
        if self.state == str:
            return
        for face in self.faces:
            face.as_str()

    # axis rotations
    def x(self, prime = False):
        """
        left and right held constant
        rotates clockwise when facing right
        """
        state = np.array([self.front, self.up, self.back, self.down], dtype='object')
        state = np.roll(state, -1 if prime else 1,0)
        self.front, self.up, self.back, self.down = state
        self.back.ver_flip()
        self.down.ver_flip()
        self.right.rotate()
        self.left.rotate(True)


    def y(self, prime = False):
        """
        up and down held constant
        rotates clockwise when facing top
        """
        state = np.array([self.front, self.left, self.back, self.right], dtype='object')
        state = np.roll(state, -1 if prime else 1, 0)
        self.front, self.left, self.back, self.right = state
        self.back.hor_flip()
        self.right.hor_flip()
        self.up.rotate(prime)
        self.down.rotate(not prime)

    def z(self, prime = False):
        """
        hold front and back constant
        rotate clockwise when facing front
        """
        state = np.array([self.left, self.up, self.right, self.down], dtype='object')
        state = np.roll(state, -1 if prime else 1,0)
        self.left, self.up, self.right, self.down = state
        self.front.rotate(prime)
        self.back.rotate(not prime)
        self.left.rotate(prime)
        self.up.rotate(prime)
        self.right.rotate(prime)
        self.down.rotate(prime)


    # basic move
    def F(self, prime = False):
        """
        moves front clockwise. If prime them moves anticlockwise
        """
        self.front.rotate(prime)
        layer = np.array([\
            np.array([l[-1] for l in self.left.state], dtype = 'object'),\
            self.up.state[-1],\
            np.array([l[0] for l in self.right.state], dtype = 'object'),\
            self.down.state[0]
            ], dtype='object')
        layer = np.roll(layer, -1 if prime else 1, 0)
        self.left.state[:,-1] = layer[0].transpose()
        self.right.state[:,0] = layer[2].transpose()
        self.up.state[-1] = layer[1]
        self.down.state[0] = layer[3]

    # remaining moves in terms of self.F
    def B(self, prime = False):
        """
        moves back clockwise. If prime them moves anticlockwise
        """
        self.y()
        self.y()
        self.F(prime)
        self.y()
        self.y()

    def L(self, prime = False):
        """
        moves left clockwise. If prime them moves anticlockwise
        """
        self.y(True)
        self.F(prime)
        self.y(False)

    def R(self, prime = False):
        """
        moves right clockwise. If prime them moves anticlockwise
        """
        self.y(False)
        self.F(prime)
        self.y(True)

    def U(self, prime = False):
        """
        moves up clockwise. If prime them moves anticlockwise
        """
        self.x(True)
        self.F(prime)
        self.x(False)

    def string_to_move_list(self, move_string):
        """
        converts move string to list to accommodate primes
        """
        move_list = []
        idx = 0
        while idx < len(move_string):
            move = move_string[idx]
            idx += 1
            if idx < len(move_string):
                if move_string[idx] == "'":
                    move += "'"
                    idx += 1
            move_list.append(move)
        return move_list

    def move(self, move_string, show_states=False):
        """
        implements list of moves
        """
        move_list = self.string_to_move_list(move_string)
        for move in move_list:
            prime = False
            if move[-1] == "'":
                prime = True
            if move[0].upper() == 'U':
                self.U(prime)
            if move[0].upper() == 'B':
                self.B(prime)
            if move[0].upper() == 'L':
                self.L(prime)
            if move[0].upper() == 'R':
                self.R(prime)
            if move[0].upper() == 'F':
                self.F(prime)
            if move[0].upper() == 'B':
                self.B(prime)
            if move[0].lower() == 'x':
                self.x(prime)
            if move[0].lower() == 'y':
                self.y(prime)
            if move[0].lower() == 'z':
                self.z(prime)
            if show_states:
                self.show_state()




if __name__=='__main__':
    x = rubiks_cube()
    S = "RUR'U'"
    x.as_int()
    x.move(S,show_states=True)
