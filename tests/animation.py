import cv2
import numpy as np
import sys

sys.path.append ( "../" )
import pyastar
from os.path import join

image_path = '../mazes'
# MAZE_FPATH = join ( image_path , '4777.png' )
# MAZE_FPATH = join(image_path, 'maze_large.png')
MAZE_FPATH = join(image_path, 'mitsuoka_rockstar_01i.png')

start = np.zeros ( 2 )  # [y, x]
end = np.zeros ( 2 )

select_point = 0
THICK = 1
mode = {'startset': 0 , 'endset': 0 , 'ready': 0}


def root_finder(maze , start , end):
    grid = cv2.cvtColor ( maze , cv2.COLOR_BGR2GRAY ).astype ( np.float32 )
    grid[grid == 0] = np.inf
    grid[grid == 255] = 1

    assert grid.min () == 1 , 'cost of moving must be at least 1'
    # ルート探索
    root = pyastar.astar_path ( grid , start , end , allow_diagonal=False )
    return root


def draw_circle(event , x , y , flags , param):
    global start , end , maze , mode
    if mode['ready'] == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            if mode['startset'] == 0:
                print ( "start set" )
                maze = original_image.copy ()
                start = np.array ( [y , x] )
                cv2.circle ( maze , (x , y) , 5 , (255 , 0 , 0) , -1 )
                mode['startset'] = 1
            elif mode['endset'] == 0:
                print ( "goal set" )
                end = np.array ( [y , x] )
                cv2.circle ( maze , (x , y) , 5 , (0 , 0 , 255) , 1 )
                mode['endset'] = 1


def start_adventure():
    global maze

    for i in range ( len ( root ) ):
        maze[root[i , 0] - THICK:root[i , 0] + THICK , root[i , 1] - THICK:root[i , 1] + THICK] = (255 , 0 , 0)
        cv2.imshow ( "Loaded image" , maze )
        if cv2.waitKey ( 1 ) == ord ( 'q' ):
            break


maze = cv2.imread ( MAZE_FPATH )
# todo 二値化
original_image = maze.copy ()  # 元画像をコピーしておく
if maze is None:
    print ( 'no file found' )
    exit ()

cv2.namedWindow ( "Loaded image" )
cv2.setMouseCallback ( "Loaded image" , draw_circle )

while True:
    cv2.imshow ( "Loaded image" , maze )
    key = cv2.waitKey ( 1 )
    # if key == #todo keyで中断
    if mode['startset'] == 1 and mode['endset'] == 1:
        root = root_finder ( maze , start , end )  # ルート探索

        if len ( root ) == 0:
            print ( "no root found" )
            mode['endset'] = 0

        else:
            x = end[1]
            y = end[0]
            cv2.circle ( maze , (x , y) , 5 , (0 , 0 , 255) , -1 )
            print ( "trace start" )
            mode['ready'] = 1
            start_adventure ()
            mode['ready'] = 0
            mode['startset'] = 0
            mode['endset'] = 0
