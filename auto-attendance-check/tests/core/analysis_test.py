import sys
import glob
import cv2
from core.analysis import face_detection

sys.path.append("../../..")


def test_face_detection():
    images = glob.glob("auto-attendance-check/tests/core/images/*.jpg")
    for image in images:
        img = cv2.imread(image)
        assert face_detection(img)
    assert True
