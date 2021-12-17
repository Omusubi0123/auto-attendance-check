import mediapipe as mp
import cv2
import numpy as np


class Analysis(object):
    """
    画像解析用のクラス
    """

    Image = np.ndarray
    WEBCAM_ID = 0

    def __init__(self) -> None:
        pass

    def TakePhoto(self) -> Image:
        cap = cv2.VideoCapture(self.WEBCAM_ID)
        success, image = cap.read()
        if not success:
            raise Exception("画像のキャプチャに失敗")
        return image

    def FaceDetection(image: Image):
        mp_face_detection = mp.solutions.face_detection
        mp_drawing = mp.solutions.drawing_utils

        with mp_face_detection.FaceDetection(
            model_selection=0, min_detection_confidence=0.5
        ) as face_detection:
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)

            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)
            cv2.imshow("MediaPipe Face Detection", cv2.flip(image, 1))
