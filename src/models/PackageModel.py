from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Images, Inputs, Configs, Outputs,
    Response, Request, Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Image
    type: Literal["Image"] = "Image"


class Degree(Config):
    name: Literal["Degree"] = "Degree"
    value: Union[int, str] = 0
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Angle"


class RotateImageInputs(Inputs):
    inputImage: InputImage
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class RotateImageConfigs(Configs):
    degree: Degree
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Image
    type: Literal["Image"] = "Image"


class RotateImageOutputs(Outputs):
    outputImage: OutputImage
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"


class RotateImageRequest(Request):
    inputs: Optional[RotateImageInputs]
    configs: RotateImageConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class RotateImageResponse(Response):
    outputs: RotateImageOutputs


class RotateImageExecutor(Config):
    name: Literal["RotateImage"] = "RotateImage"
    value: Union[RotateImageRequest, RotateImageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Rotate Image"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class InputImage1(Input):
    name: Literal["inputImage1"] = "inputImage1"
    value: Image
    type: Literal["Image"] = "Image"


class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Image
    type: Literal["Image"] = "Image"


class BlendImagesInputs(Inputs):
    inputImage1: InputImage1
    inputImage2: InputImage2
    value: str = "Inputs"
    type: Literal["object"] = "object"
    field: Literal["input"] = "input"


class OutputBlended(Output):
    name: Literal["outputBlended"] = "outputBlended"
    value: Image
    type: Literal["Image"] = "Image"


class OutputDifference(Output):
    name: Literal["outputDifference"] = "outputDifference"
    value: Image
    type: Literal["Image"] = "Image"


class BlendImagesOutputs(Outputs):
    outputBlended: OutputBlended
    outputDifference: OutputDifference
    type: Literal["object"] = "object"
    field: Literal["output"] = "output"


class BlendImagesRequest(Request):
    inputs: Optional[BlendImagesInputs]


class BlendImagesResponse(Response):
    outputs: BlendImagesOutputs


class BlendImagesExecutor(Config):
    name: Literal["BlendImages"] = "BlendImages"
    value: Union[BlendImagesRequest, BlendImagesResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blend Images"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[RotateImageExecutor, BlendImagesExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor
    value: str = "Configs"
    type: Literal["object"] = "object"
    field: Literal["config"] = "config"


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["ImageFiltersEmre"] = "ImageFiltersEmre"
