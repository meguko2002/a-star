import cv2
import numpy as np
import sys

sys.path.append ( "../" )
import pyastar
from os.path import basename , join , splitext
image_path = '../mazes'
MAZE_FPATH = join ( image_path, '4777.png' )
# MAZE_FPATH = join(image_path, 'maze_small.png')


def root_finder(maze):
    grid = cv2.cvtColor ( maze , cv2.COLOR_BGR2GRAY ).astype ( np.float32 )
    grid[grid == 0] = np.inf
    grid[grid == 255] = 1
    assert grid.min () == 1 , 'cost of moving must be at least 1'
    start_j , = np.where ( grid[0 , :] == 1 )
    start = np.array ( [0 , start_j[0]] )

    # end_i, = np.where(grid[:, -1] == 1)
    # end = np.array([end_i[0], grid.shape[0] - 1])
    start = np.array ( [33 , 65] )  # [y, x]
    end = np.array ( [56 , 880] )

    root = pyastar.astar_path ( grid , start , end , allow_diagonal=False )
    return root


maze = cv2.imread ( MAZE_FPATH )
if maze is None:
    print ( 'no file found')
    exit()
cv2.imshow ( "Loaded image" , maze )
cv2.waitKey ( 1000 )
root = root_finder ( maze )

THICK = 1
for i in range ( len ( root ) ):
    maze[root[i , 0] - THICK:root[i , 0] + THICK , root[i , 1] - THICK:root[i , 1] + THICK] = (255 , 0 , 0)
    cv2.imshow ( "Loaded image" , maze )
    if cv2.waitKey ( 1 ) == 27:
        break
cv2.imshow ( "Loaded image" , maze )
cv2.waitKey ( 3000 )
cv2.destroyAllWindows ()
