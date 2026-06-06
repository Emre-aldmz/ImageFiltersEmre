from sdks.novavision.src.helper.package import PackageHelper
from components.ImageFiltersEmre.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    RotateImageOutputs,
    RotateImageResponse,
    RotateImageExecutor,
    OutputImage,
    BlendImagesOutputs,
    BlendImagesResponse,
    BlendImagesExecutor,
    OutputBlended,
    OutputDifference,
)


def build_rotate_response(context):
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