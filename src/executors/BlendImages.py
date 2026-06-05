"""
    BlendImages Executor

    İki resmi karıştırır (blend) ve fark (difference) görselini üretir.
    2 input (2 resim), 2 output (karışım + fark).
"""

import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.Package.src.utils.response import build_blend_response
from components.Package.src.models.PackageModel import PackageModel


class BlendImages(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        self.image1 = self.request.get_param("inputImage1")
        self.image2 = self.request.get_param("inputImage2")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def blend(self, img1, img2):
        """
        İki resmi eşit oranda karıştırır (alpha=0.5).
        İkinci resim birinci resmin boyutuna yeniden boyutlandırılır.
        """
        h, w = img1.shape[:2]
        img2_resized = cv2.resize(img2, (w, h))
        blended = cv2.addWeighted(img1, 0.5, img2_resized, 0.5, 0)
        return blended

    def difference(self, img1, img2):
        """
        İki resim arasındaki mutlak farkı hesaplar.
        İkinci resim birinci resmin boyutuna yeniden boyutlandırılır.
        """
        h, w = img1.shape[:2]
        img2_resized = cv2.resize(img2, (w, h))
        diff = cv2.absdiff(img1, img2_resized)
        return diff

    def run(self):
        # İlk resmi al ve işle
        frame1 = Image.get_frame(img=self.image1, redis_db=self.redis_db)
        frame2 = Image.get_frame(img=self.image2, redis_db=self.redis_db)

        # Karışım sonucu
        blended_value = self.blend(frame1.value, frame2.value)
        frame1.value = blended_value
        self.blended_image = Image.set_frame(
            img=frame1, package_uID=self.uID, redis_db=self.redis_db
        )

        # Fark sonucu
        diff_value = self.difference(
            Image.get_frame(img=self.image1, redis_db=self.redis_db).value,
            Image.get_frame(img=self.image2, redis_db=self.redis_db).value
        )
        frame2.value = diff_value
        self.difference_image = Image.set_frame(
            img=frame2, package_uID=self.uID, redis_db=self.redis_db
        )

        packageModel = build_blend_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()
