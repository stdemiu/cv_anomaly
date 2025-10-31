import cv2
import numpy as np
import matplotlib.pyplot as plt


img_path = "Ambassadors.jpg"
img = cv2.imread(img_path)
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
scale = 0.5
img = cv2.resize(img, (0, 0), fx=scale, fy=scale)

clone = img.copy()
points = []



def select_points(event, x, y, flags, param):
    global points, img
    if event == cv2.EVENT_LBUTTONDOWN:
        points.append((x, y))
        cv2.circle(img, (x, y), 10, (255, 0, 0), -1)
        cv2.imshow("Выделите 4 точки вокруг аномалии (черепа)", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))


cv2.imshow("Выделите 4 точки вокруг аномалии (черепа)", cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
cv2.setMouseCallback("Выделите 4 точки вокруг аномалии (черепа)", select_points)
cv2.waitKey(0)
cv2.destroyAllWindows()

if len(points) != 4:
    raise ValueError("Нужно выбрать ровно 4 точки!")


pts_src = np.float32(points)
width, height = 600, 1200
pts_dst = np.float32([
    [0, 0],
    [width - 1, 0],
    [0, height - 1],
    [width - 1, height - 1]
])

M = cv2.getPerspectiveTransform(pts_src, pts_dst)
warped = cv2.warpPerspective(clone, M, (width, height))

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
plt.imshow(clone)
plt.title("Оригинальная картина")
plt.axis("off")

plt.subplot(1, 2, 2)
plt.imshow(warped)
plt.title("Преобразованная аномалия (череп)")
plt.axis("off")

plt.tight_layout()
plt.show()
