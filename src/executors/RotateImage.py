import os
import cv2
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../../'))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor
from components.ImageFiltersEmre.src.utils.response import build_rotate_response
from components.ImageFiltersEmre.src.models.PackageModel import PackageModel


class RotateImage(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)
        self.request.model = PackageModel(**(self.request.data))
        try:
            self.rotation_degree = int(self.request.model.configs.executor.value.value.configs.degree.value)
        except Exception:
            deg = self.request.get_param("Degree") or self.request.get_param("degree")
            try:
                self.rotation_degree = int(deg) if deg is not None else 0
            except ValueError:
                self.rotation_degree = 0
        self.image = self.request.get_param("inputImage")

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def rotation(self, image):
        height, width = image.shape[:2]
        image_center = (width / 2, height / 2)

        rotation_arr = cv2.getRotationMatrix2D(
            image_center, self.rotation_degree, 1
        )

        abs_cos = abs(rotation_arr[0, 0])
        abs_sin = abs(rotation_arr[0, 1])

        bound_w = int(height * abs_sin + width * abs_cos)
        bound_h = int(height * abs_cos + width * abs_sin)

        rotation_arr[0, 2] += bound_w / 2 - image_center[0]
        rotation_arr[1, 2] += bound_h / 2 - image_center[1]

        img_rotation = cv2.warpAffine(
            image, rotation_arr, (bound_w, bound_h)
        )

        # DEBUG: Write the received degree on the image to see what is actually coming from the platform
        cv2.putText(img_rotation, f"Received Deg: {self.rotation_degree}", (30, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 0), 3)

        return img_rotation

    def run(self):
        img = Image.get_frame(img=self.image, redis_db=self.redis_db)
        img.value = self.rotation(img.value)
        self.image = Image.set_frame(
            img=img, package_uID=self.uID, redis_db=self.redis_db
        )
        packageModel = build_rotate_response(context=self)
        return packageModel


if "__main__" == __name__:
    Executor(sys.argv[1]).run()