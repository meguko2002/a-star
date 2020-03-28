import cv2
import numpy as np
import sys

sys.path.append ( "../" )
import pyastar
from os.path import join
image_path = '../mazes'
MAZE_FPATH = join ( image_path, '4777.png' )
# MAZE_FPATH = join(image_path, 'maze_small.png')
# MAZE_FPATH = join(image_path, 'maze_large.png')

start = np.zeros(2)  # [y, x]
end = np.zeros(2)

select_point = 0
THICK = 1


def root_finder(maze, start, end):
    grid = cv2.cvtColor ( maze , cv2.COLOR_BGR2GRAY ).astype ( np.float32 )
    grid[grid == 0] = np.inf
    grid[grid == 255] = 1

    assert grid.min () == 1 , 'cost of moving must be at least 1'
    # ルート探索
    root = pyastar.astar_path ( grid , start , end , allow_diagonal=False)
    return root


def draw_circle(event,x,y,flags,param):
    global start, end, maze, mode, select_point
    if event == cv2.EVENT_LBUTTONDOWN and mode:
        if select_point == 0:
            print("start set")
            start = np.array([y, x])
            color = (255, 0, 0)
        elif select_point == 1:
            print("goal set")
            end = np.array([y, x])
            color = (0, 0, 255)
        cv2.circle(maze,(x,y),5,color,-1)
        select_point =1-select_point

def reset_state():
    global start, end, mode
    start = np.zeros ( 2 )  # [y, x]
    end = np.zeros ( 2 )
    mode = True


def start_adventure():
    global maze

    for i in range ( len ( root ) ):
        maze[root[i , 0] - THICK:root[i , 0] + THICK , root[i , 1] - THICK:root[i , 1] + THICK] = (255 , 0 , 0)
        cv2.imshow ( "Loaded image" , maze )
        if cv2.waitKey ( 1 ) == ord ( 'q' ):
            break
    key = cv2.waitKey ( 0 )
    cv2.imshow ( "Loaded image" , maze )
    # TODO goalまで到達してるはずだからマウスで次のゲームのスタート設定するのとreturnが同じタイミングが使いやすい
    if key == ord ( 'q' ):
        return

maze = cv2.imread ( MAZE_FPATH )
original_image = maze.copy()
if maze is None:
    print ( 'no file found')
    exit()

cv2.namedWindow("Loaded image")
cv2.setMouseCallback("Loaded image" ,draw_circle)

mode = True
while True:
    cv2.imshow ( "Loaded image" , maze )
    cv2.waitKey(1)
    if end[0]!=0 and end[1]!=0:   # end が設定されたら
        cv2.imshow ( "Loaded image" , maze )   # end地点を表示
        root = root_finder ( maze , start , end )  # ルート探索
        reset_state()
        if len(root) == 0:
            print ( "no root found" )
        else:
            print("trace start" )
            mode = False
            start_adventure()
            mode = True
        maze = original_image.copy ()



