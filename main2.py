import cv2
import numpy as np

img_path = "scale_2400.jfif" 
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
clone = img.copy()

cv2.namedWindow("Выдели 4 точки (Парнас)", cv2.WINDOW_NORMAL)
cv2.resizeWindow("Выдели 4 точки (Парнас)", 1200, 800)


points = []
def click_event(event, x, y, flags, param):
    global points
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 8, (255, 0, 0), -1)
        cv2.imshow(param, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))

def get_transformed(title, width, height):
    global points, img
    points = []
    img[:] = clone
    cv2.imshow(title, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
    cv2.setMouseCallback(title, click_event, title)
    cv2.waitKey(0)
    cv2.destroyWindow(title)
    if len(points) != 4:
        raise ValueError("Нужно выбрать ровно 4 точки!")
    pts_src = np.float32(points)
    pts_dst = np.float32([[0,0],[width-1,0],[0,height-1],[width-1,height-1]])
    M = cv2.getPerspectiveTransform(pts_src, pts_dst)
    warped = cv2.warpPerspective(clone, M, (width, height))
    return warped


parnassus = get_transformed("Выдели 4 точки (Парнас)", 1000, 600)
cv2.imwrite("parnassus.jpg", cv2.cvtColor(parnassus, cv2.COLOR_RGB2BGR))
print("Сохранено: parnassus.jpg")


school = get_transformed("Выдели 4 точки (Афинская школа)", 1000, 600)
cv2.imwrite("school.jpg", cv2.cvtColor(school, cv2.COLOR_RGB2BGR))
print("Сохранено: school.jpg")

floor = get_transformed("Выдели 4 точки (Пол комнаты)", 1000, 600)
cv2.imwrite("floor.jpg", cv2.cvtColor(floor, cv2.COLOR_RGB2BGR))
print("Сохранено: floor.jpg")

cv2.destroyAllWindows()
