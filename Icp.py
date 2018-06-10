import numpy as np
import cv2
import math
import operator

K = 5

def edge(img):
    blurred = cv2.GaussianBlur(img,(3,3),0)
    gray=cv2.cvtColor(blurred,cv2.COLOR_RGB2GRAY)
    xgrad=cv2.Sobel(gray,cv2.CV_16SC1,1,0)
    ygrad=cv2.Sobel(gray,cv2.CV_16SC1,0,1)
    edge_output=cv2.Canny(xgrad,ygrad,50,150)
    return edge_output
    
def getShort(x, y, Tedge):
    if Tedge[x, y] != 0:
        return x, y, 0
    for i in range(1,100000):
        if Tedge[x + i, y] != 0:
            return x + i, y, i
        if Tedge[x, y + i] != 0:
            return x ,y + i, i
        if Tedge[x - i, y] != 0:
            return x - i, y, i
        if Tedge[x, y - i] != 0:
            return x ,y - i, i
        if Tedge[x + i, y + i] != 0:
            return x + i ,y + i, i
        if Tedge[x + i, y - i] != 0:
            return x + i ,y - i, i
        if Tedge[x - i, y + i] != 0:
            return x - i,y + 1, i
        if Tedge[x -i, y - i] != 0:
            return x - i,y - i, i
    
def afterImg(theta,dx,dy):
    return cv2.imread("D:\\Desktop\\TM\\bm.jpg")

def icp(TImg, SImg, theta = 0, dx = 0, dy = 0):
    Tedge = edge(TImg)
    Sedge = edge(SImg)
    height = Sedge.shape[0]
    width = Sedge.shape[1]
    theta = theta / 180 * math.pi
    outPoint = []
    for crink in range(K):
        r = np.array([[math.cos(theta), -math.sin(theta)], [math.sin(theta), math.cos(theta)]])
        t = np.array([[dx], [dy]])
        radi = []
        ci = {}
        for i in range(width):
            for j in range(height):
                x = np.array([[i],[j]])
                q = r * x + t
                if Sedge[q[0, 0], q[1, 0]] == 0 or ((q[0, 0], q[1, 0]) in outPoint):
                    continue
                x1, y1, rad = getShort(q[0, 0], q[1, 0], Tedge)
                ci[(i, j)] = (x1, y1)
                radi[(i, j)] = rad
        radList = sorted(radi.items(),key = lambda x:x[1],reverse = True)
        for i in len(radList):
            if i < len(radList)/2:
                outPoint.append(radList[i])
        x_ = 0
        y_ = 0
        x_1 = 0
        y_1 = 0
        s_xx = 0
        s_yy = 0
        s_xy = 0
        s_yx = 0
        n = len(ci)
        for point in ci:
            x_ += 1/n*point[0]
            y_ += 1/n*point[1]
            x_1 += 1/n*ci[point][0]
            y_1 += 1/n*ci[point][1]
        for point in ci:
            s_xx += (point[0] - x_)*(ci[point][0] - x_1)
            s_yy += (point[1] - y_)*(ci[point][1] - y_1)
            s_xy += (point[0] - x_)*(ci[point][1] - y_1)
            s_yy += (point[1] - y_)*(ci[point][0] - x_1)
        theta = math.acot(s_xx + s_yy)/(s_xy - s_yx)
        dx = x_1 - (x_*math.cos(theta) - y_*math.sin(theta))
        dy = y_1 - (x_*math.sin(theta) + y_*math.cos(theta))
    return theta,dx,dy
