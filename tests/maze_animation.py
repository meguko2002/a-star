import cv2
import numpy as np
import os
import PySimpleGUI as sg
import pyastar


"""file choice widget"""
layout = [[sg.Text ( '迷路の画像を探しましょう' )] ,
          [sg.Input ('../mazes/4777.png') , sg.FileBrowse ('選択', file_types=(("Text Files","*.png" or "*.jpeg" ),))] ,
          [sg.OK ('実行')]]

window = sg.Window ( 'Get filename example' , layout )
event , image_file = window.read ()
window.close ()

save_path ='../solns'
blue = (255 , 0 , 0)
red = (0 , 0 , 255)
start = np.zeros ( 2 )  # [y, x]
goal = np.zeros ( 2 )
THICK = 1
mode = {'startset': 0 , 'endset': 0 , 'ready': 0 , 'inout': 0}


def root_finder(maze , start , goal):
    grid = cv2.cvtColor ( maze , cv2.COLOR_BGR2GRAY ).astype ( np.float32 )

    _ , grid = cv2.threshold ( grid , 127 , 255 , cv2.THRESH_BINARY )
    grid[grid == 0] = np.inf
    grid[grid == 255] = 1

    assert grid.min () == 1 , 'cost of moving must be at least 1'
    # ルート探索
    root = pyastar.astar_path ( grid , start , goal , allow_diagonal=False )
    return root


def draw_circle(event , x , y , flags , param):
    global start , goal , maze , mode
    if mode['ready'] == 0:
        if event == cv2.EVENT_LBUTTONDOWN:
            if mode['startset'] == 0:
                print ( "start set" )
                if mode['inout'] == 0:  # モード0なら毎回画面クリア
                    maze = original_image.copy ()
                start = np.array ( [y , x] )
                cv2.circle ( maze , (x , y) , 5 , blue , -1 )
                mode['startset'] = 1
            elif mode['endset'] == 0:
                print ( "goal set" )
                goal = np.array ( [y , x] )
                cv2.circle ( maze , (x , y) , 5 , red , 1 )
                mode['endset'] = 1


def start_adventure():
    global maze
    color = blue
    for i in range ( len ( root ) ):
        maze[root[i , 0] - THICK:root[i , 0] + THICK , root[i , 1] - THICK:root[i , 1] + THICK] = color
        cv2.imshow ( "Loaded image" , maze )
        if cv2.waitKey ( 1 ) == ord ( 'q' ):
            break


maze = cv2.imread ( image_file[0])
original_image = maze.copy ()  # 元画像をコピーしておく
if maze is None:
    print ( 'no file found' )
    exit ()

cv2.namedWindow ( "Loaded image" )
cv2.setMouseCallback ( "Loaded image" , draw_circle )

while True:
    cv2.imshow ( "Loaded image" , maze )
    key = cv2.waitKey ( 1 )
    if key == ord ( 'q' ):
        break
    elif key == ord ( 's' ):
        cv2.imwrite ( os.path.join ( save_path , image_file ) , maze )
        break

    if mode['startset'] == 1 and mode['endset'] == 1:
        root = root_finder ( original_image , start , goal )  # ルート探索

        if len ( root ) == 0:
            print ( "no root found" )
            mode['endset'] = 0

        else:
            x = goal[1]
            y = goal[0]
            cv2.circle ( maze , (x , y) , 5 , (0 , 0 , 255) , -1 )
            print ( "trace start" )
            mode['ready'] = 1
            start_adventure ()
            mode['ready'] = 0
            mode['startset'] = 0
            mode['endset'] = 0

cv2.destroyAllWindows ()
