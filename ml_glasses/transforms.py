import random
import time

import dlib
import numpy as np
import torch
from imutils import opencv2matplotlib
from imutils.face_utils import FaceAligner
from torchvision.transforms import CenterCrop, functional as F
from PIL import ImageFilter


class FaceAlignTransform:
    def __init__(self, detector_model='../mmod_human_face_detector.dat',
                 shape_predictor='../shape_predictor_68_face_landmarks.dat',
                 desired_face_width=120, desired_left_eye=(0.35, 0.5)):
        self.detector = dlib.cnn_face_detection_model_v1(detector_model)
        # it does something during the first call, so I call a dummy detection in __init__
        self.detector(np.zeros((256, 256), dtype=np.uint8), 1)

        self.predictor = dlib.shape_predictor(shape_predictor)
        self.aligner = FaceAligner(self.predictor, desiredFaceWidth=desired_face_width, desiredLeftEye=desired_left_eye)
        self.fallback_crop = CenterCrop(desired_face_width)

    def __call__(self, image):
        image = F.resize(image, 256)
        gray = np.array(F.to_grayscale(image))

        detections = self.detector(gray, 1)
        if not detections:
            return self.fallback_crop(image)

        face_rect = detections[0].rect
        aligned_face = self.aligner.align(opencv2matplotlib(np.array(image)), gray, face_rect)
        return opencv2matplotlib(aligned_face)


class RandomHorizontalFlip:
    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, image):
        if random.random() < self.p:
            image = F.hflip(image)

        return image


class RandomGaussianBlur:
    def __call__(self, image):
        dice_roll = random.random()
        if dice_roll < 0.02:
            image = image.filter(ImageFilter.GaussianBlur(radius=2))
        elif dice_roll < 0.1:
            image = image.filter(ImageFilter.GaussianBlur(radius=1))

        return image


class ToTensor:
    def __call__(self, image):
        image = np.array(image)
        image = image.transpose((2, 0, 1))
        image = torch.from_numpy(image).float() / 255

        return image
