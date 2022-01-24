import sys
import glob

import cv2
import numpy as np

from core.analysis import face_detection, split_image

sys.path.append("../../..")

def test_split_image():
    image: str = glob.glob("auto-attendance-check/tests/core/images/*.jpg")[0]
    image: np.ndarray = cv2.imread(image)
    height, width, _ =  image.shape
    areas = [
        [[0, 0], [width // 2, height // 2]],
        [[width // 2, 0], [width, height // 2]],
        [[0, height // 2], [width // 2, height]],
        [[width // 2, height // 2], [width, height]]
    ]
    res = split_image(image, areas)
    assert True

def test_face_detection():
    images = glob.glob("auto-attendance-check/tests/core/images/*.jpg")
    for image in images:
        img = cv2.imread(image)
        assert face_detection(img)
    assert True

"""
# 実際に画像を表示させながらテストする場合はこれを実行する
# pytestだと動かないのでコメントアウト

def test_split_image():
    image: str = "auto-attendance-check/tests/core/images/test.JPG"
    image: np.ndarray = cv2.imread(image)
    width, height, _ =  image.shape
    areas = [
        [[0, 0], [width // 3, height // 2]],
        [[width // 3, 0], [width, height // 2]],
        [[0, height // 2], [width // 3, height]],
        [[width // 3, height // 2], [width, height]]
    ]
    res = split_image(image, areas)
    for i, t in enumerate(res):
        t = cv2.resize(t, (200, 200))
        print(i, face_detection(t))
    assert True
test_split_image()
"""