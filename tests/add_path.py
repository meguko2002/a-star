import cv2
from os.path import join

image_path = '../mazes'
image_files=['4777.png' ,'maze_small.png','images.jpeg', 'rectangle_large.png','add.png']
MAZE_FPATH = join ( image_path ,image_files[4])

drawing = False # true if mouse is pressed
ix,iy = -1,-1

# mouse callback function
def draw_circle(event,x,y,flags,param):
    global ix,iy,drawing

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        ix,iy = x,y
        cv2.circle (maze, (ix,iy) , 3, (0 , 0 , 0) , -1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle ( maze , (x , y) , 3 , (0 , 0 , 0) , -1 )

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False


cv2.namedWindow ( "Loaded image" )
cv2.setMouseCallback ( "Loaded image" , draw_circle)

maze = cv2.imread ( MAZE_FPATH )
original_image = maze.copy ()  # 元画像をコピーしておく

while True:
    cv2.imshow ( "Loaded image" , maze)
    k = cv2.waitKey ( 1 )
    if k == 27:  # wait for ESC key to exit
        break
    elif k == ord ( 's' ):  # wait for 's' key to save and exit
        cv2.imwrite ( join ( image_path , 'add.png' ), maze )
        break

cv2.destroyAllWindows ()

