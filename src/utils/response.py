"""
    Response builder fonksiyonları.

    Her executor için ayrı bir build_response fonksiyonu bulunur.
"""

from sdks.novavision.src.helper.package import PackageHelper
from components.Package.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    # RotateImage executor model sınıfları
    RotateImageOutputs,
    RotateImageResponse,
    RotateImageExecutor,
    OutputImage,
    # BlendImages executor model sınıfları
    BlendImagesOutputs,
    BlendImagesResponse,
    BlendImagesExecutor,
    OutputBlended,
    OutputDifference,
)


def build_rotate_response(context):
    """RotateImage executor için response oluşturur."""
    outputImage = OutputImage(value=context.image)
    outputs = RotateImageOutputs(outputImage=outputImage)
    response = RotateImageResponse(outputs=outputs)
    executor = RotateImageExecutor(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(
        packageModel=PackageModel, packageConfigs=packageConfigs
    )
    packageModel = package.build_model(context)
    return packageModel


def build_blend_response(context):
    """BlendImages executor için response oluşturur."""
    outputBlended = OutputBlended(value=context.blended_image)
    outputDifference = OutputDifference(value=context.difference_image)
    outputs = BlendImagesOutputs(
        outputBlended=outputBlended,
        outputDifference=outputDifference
    )
    response = BlendImagesResponse(outputs=outputs)
    executor = BlendImagesExecutor(value=response)
    configExecutor = ConfigExecutor(value=executor)
    packageConfigs = PackageConfigs(executor=configExecutor)
    package = PackageHelper(
        packageModel=PackageModel, packageConfigs=packageConfigs
    )
    packageModel = package.build_model(context)
    return packageModel