import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt
import math
from itertools import groupby, product
from scipy.spatial.transform import Rotation as Ro


def absolute_distance(val1, val2):
    return abs(val1[0] - val2[0]) + abs(val1[1] - val2[1])


def grouping(corne):
    abs_tuples = [sorted(corners) for corners in product(corne, repeat=2)
                  if absolute_distance(*corners) <= 20]
    result_dict = {i: {i} for i in corne}
    for val1, val2 in abs_tuples:
        result_dict[val1] |= result_dict[val2]
        result_dict[val2] = result_dict[val1]

    result = [[*next(values)] for key, values in groupby(
        sorted(result_dict.values(), key=id), id)]
    a = []
    for i in result:
        a.append((np.mean(i, axis=0, dtype=int)))
    return a


def HoughTransform(img, Coordinates):
    Maxdist = int(np.round(np.sqrt((img.shape[1])**2 + (img.shape[0]) ** 2)))
    thetas = (np.arange(0, 181))
    d = {}
    for item in Coordinates:
        for k in range(len(thetas)):
            r = (item[1]*np.cos(thetas[k]*(math.pi/180)) +
                 item[0]*np.sin(thetas[k]*(math.pi/180)))
            if round(r) <= Maxdist:
                if (round(r), thetas[k]) not in d:
                    d[(round(r), thetas[k])] = 0
                d[(round(r), thetas[k])] += 1
    return d


def intersection(rthe):
    sorted_rthe = sorted(rthe.items(), key=lambda x: x[1])[-8:]
    indices = list([list(x[0]) for x in sorted_rthe])
    RT = np.vstack(indices)
    points = []
    i = 0
    for one in RT:
        d1, t1 = one
        for two in RT[i:]:
            d2, t2 = two
            if abs(t1 - t2) >= 85 and abs(t1-t2) <= 95:
                x, y = find_xy(d1, t1, d2, t2)
                x, y = abs(x), abs(y)
                points.append((x, y))
        i += 1
    return points


def find_xy(d1, t1, d2, t2):
    theta_1 = t1
    theta_2 = t2
    A = np.matrix([[np.cos(theta_1*(math.pi/180)), np.sin(theta_1*(math.pi/180))],
                  [np.cos(theta_2*(math.pi/180)), np.sin(theta_2*(math.pi/180))]])
    B = np.matrix([[d1], [d2]])
    X = np.linalg.inv(A) @ B
    x1 = round(float(X[0][0]))
    y1 = round(float(X[1][0]))
    center = (x1, y1)
    return center


def homography(corn):
    corn = sorted(corn, key=lambda x: x[0])
    x1, x2, x3, x4 = 0, 21.6, 0, 21.6
    y1, y2, y3, y4 = 0, 0, 27.9, 27.9
    x_1, x_2, x_3, x_4 = corn[0][0], corn[1][0], corn[2][0], corn[3][0]
    y_1, y_2, y_3, y_4 = corn[0][1], corn[1][1], corn[2][1], corn[3][1]
    A = np.matrix([[x1, y1, 1, 0, 0, 0, -(x1*x_1), -(y1*x_1), -x_1],
                   [0, 0, 0, x1, y1, 1, -(x1*y_1), -(y1*y_1), -y_1],
                   [x2, y2, 1, 0, 0, 0, -(x2*x_2), -(y2*x_2), -x_2],
                   [0, 0, 0, x2, y2, 1, -(x2*y_2), -(y2*y_2), -y_2],
                   [x3, y3, 1, 0, 0, 0, -(x3*x_3), -(y3*x_3), -x_3],
                   [0, 0, 0, x3, y3, 1, -(x3*y_3), -(y3*y_3), -y_3],
                   [x4, y4, 1, 0, 0, 0, -(x4*x_4), -(y4*x_4), -x_4],
                   [0, 0, 0, x4, y4, 1, -(x4*y_4), -(y4*y_4), -y_4]])
    w, v = np.linalg.eigh(np.transpose(A) @ A)
    H = np.reshape(v[:, 0], (3, 3))
    H = (1 / H.item(8)) * H
    return H


def rot_trans(Homo):
    K = np.matrix([[1382.58398, 0, 945.743164],
                   [0, 1382.58398, 527.04834],
                   [0, 0, 1]])
    A = np.linalg.inv(K) @ Homo
    w = A[0, 2]
    lambda_1 = np.linalg.norm(A[:, 0])
    lambda_2 = np.linalg.norm(A[:, 1])
    lambda_i = (lambda_1 + lambda_2) / 2
    A = A/lambda_i
    r1 = (A[:, 0])
    r2 = (A[:, 1])
    r3 = np.cross(r1, r2, axis=0)
    R = np.hstack((r1, r2, r3))
    t = A[:, 2]
    return R, t


q = 0
w = 0
x = []
y = []
z = []
x1 = []
y1 = []
z1 = []

paper = cv.VideoCapture(0)

while (True):
    ret, frame = paper.read()
    if not ret:
        break
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blurred_img = cv.GaussianBlur(gray, (15, 15), 0)
    lower_white = 75
    upper_white = 150

    edge = cv.Canny(blurred_img, lower_white, upper_white)
    coordinates = (np.column_stack(np.where(edge != 0)))
    rtheta = HoughTransform(edge, coordinates)
    corners_clusteer = intersection(rtheta)
    corners = grouping(corners_clusteer)
    if len(corners) == 4:
        Homograph = homography(corners)
        R, t = rot_trans(Homograph)
        x1.append(float(t[0]))
        y1.append(float(t[1]))
        z1.append(float(t[2]))
        w += 1
        r = Ro.from_matrix(R)
        z.append(r.as_euler('zyx', degrees=True)[0])
        y.append(r.as_euler('zyx', degrees=True)[1])
        x.append(r.as_euler('zyx', degrees=True)[2])
    for ele in corners:
        cv.circle(frame, (ele[0], ele[1]), 6, (0, 0, 255), -1)
    cv.imshow('frame', frame)
    # cv.imshow('edge', edge)
    # cv.imshow('res',res)
    q += 1
    k = cv.waitKey(5) & 0xFF
    if k == 27:
        break

frames_size = np.arange(1, 148, 1)

fig, ax = plt.subplots(1, 2, figsize=(10, 20))
ax[0].plot(frames_size, x, label='roll')
ax[0].plot(frames_size, y, label='pitch')
ax[0].plot(frames_size, z, label='yaw')
ax[0].legend()
ax[1].plot(frames_size, x1, label='translation-x')
ax[1].plot(frames_size, y1, label='translation-y')
ax[1].plot(frames_size, z1, label='translation-z')
ax[1].legend()
plt.show()

print('No.of frames in the video :', q)
print('No.of frames paper got detected in the video :', w)
cv.destroyAllWindows()
paper.release()