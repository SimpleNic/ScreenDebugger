import cv2
import pyautogui
import os
import keyboard
import numpy as np
import time

COLOR_BGR = [(0,0,255),(0,127,255),(0,255,255),
             (0,255,127),(0,255,0),(127,255,0),
             (255,255,0),(255,127,0),(255,0,0),
             (255,0,127),(255,0,255),(127,0,255)]

COLOR_BGR_NAME = ['RED','ORANGE','YELLOW',
                  'LIME','GREEN','TURQUOISE',
                  'CYAN','OCEAN','BLUE',
                  'VIOLET','MAGENTA','RASBERRY']
def end(key):
    global ended
    ended = True
    print('Results:')
    for pos,circle in enumerate(circles):
        print(f'Circle: {COLOR_BGR_NAME[pos]:10} Position: {circle[0]:<3} {circle[1]:<6} RGB: {np.flip(img[circle[1]][circle[0]])}')
    time.sleep(1000000)

def move_pixel_up(key):
    modifier = 10
    if key.name == 'w': modifier = 1
    if len(circles) > 0:
        circle = circles[-1]
        x = circle[0]
        y = circle[1]-modifier
        if y > 0:
            circles[-1] = (x,y)
        else:
            circles[-1] = (x,0)

def move_pixel_down(key):
    modifier = 10
    if key.name == 's': modifier = 1
    if len(circles) > 0:
        circle = circles[-1]
        x = circle[0]
        y = circle[1]+modifier
        if y < bounds_img:
            circles[-1] = (x,y)
        else:
            circles[-1] = (x,bounds_img-1)

def move_pixel_left(key):
    modifier = 10
    if key.name == 'a': modifier = 1
    if len(circles) > 0:
        circle = circles[-1]
        x = circle[0]-modifier
        y = circle[1]
        if x > 0:
            circles[-1] = (x,y)
        else:
            circles[-1] = (0,y)

def move_pixel_right(key):
    modifier = 10
    if key.name == 'd': modifier = 1
    if len(circles) > 0:
        circle = circles[-1]
        x = circle[0]+modifier
        y = circle[1]
        if x < bounds_img:
            circles[-1] = (x,y)
        else:
            circles[-1] = (bounds_img-1,y)

def new_screen_around_mouse(key):
    global img, img_draw, circles, bounds_img
    name = key.name
    if not name.isnumeric(): return

    bounds_img = int(name) * 100 + 100
    pos_mouse = pyautogui.position()

    x = pos_mouse[0]-bounds_img//2
    y = pos_mouse[1]-bounds_img//2

    box = (x,y,bounds_img,bounds_img)
    pyautogui.screenshot('tmp.png',box)
    img = cv2.imread('tmp.png')
    img_draw = img.copy()
    os.remove('tmp.png')

    cv2.namedWindow(window_name)
    circles.clear()

def read_pixel(key):
    if len(circles) > 0:
        circle = circles[-1]
        print(f'Circle: {COLOR_BGR_NAME[len(circles)-1]:10} Position: {circle[0]:<3} {circle[1]:<7}RGB: {np.flip(img[circle[1]][circle[0]])}')

def draw_circles(event, x, y, flags, param):
    if ended: return
    if event == cv2.EVENT_LBUTTONDOWN:
        circles.append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:
        if len(circles) > 0:
            circles.pop()

if __name__ == '__main__':
    circles = []
    bounds_img = 1000
    ended = False

    pyautogui.screenshot('tmp.png',(0,0,bounds_img,bounds_img))
    img = cv2.imread('tmp.png')
    img_draw = img.copy()
    os.remove('tmp.png')
    
    window_name = 'screen'
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name,draw_circles)
    
    keyboard.on_press_key('up',move_pixel_up)
    keyboard.on_press_key('down',move_pixel_down)
    keyboard.on_press_key('left',move_pixel_left)
    keyboard.on_press_key('right',move_pixel_right)
    keyboard.on_press_key('w',move_pixel_up)
    keyboard.on_press_key('s',move_pixel_down)
    keyboard.on_press_key('a',move_pixel_left)
    keyboard.on_press_key('d',move_pixel_right)
    keyboard.on_press(new_screen_around_mouse)
    keyboard.on_press_key('r',read_pixel)
    keyboard.on_press_key('e',end)
    
    while True:
        cv2.imshow(window_name,img_draw)
        img_draw = img.copy()

        if len(circles) == 0 or len(circles) > 12:
            circles.clear()
        for pos,circle in enumerate(circles):
            cv2.circle(img=img_draw, center=(circle), radius=20, color=COLOR_BGR[pos], thickness=2)

        if cv2.waitKey(10) == 113:
            break