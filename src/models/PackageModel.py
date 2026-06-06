from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Images, Inputs, Configs, Outputs,
    Response, Request, Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Images
    type: Literal["Images"] = "Images"


class Degree(Config):
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359, le=359, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Angle"


class RotateImageInputs(Inputs):
    inputImage: InputImage


class RotateImageConfigs(Configs):
    degree: Degree


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Images
    type: Literal["Images"] = "Images"


class RotateImageOutputs(Outputs):
    outputImage: OutputImage


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
    value: Images
    type: Literal["Images"] = "Images"


class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Images
    type: Literal["Images"] = "Images"


class BlendImagesInputs(Inputs):
    inputImage1: InputImage1
    inputImage2: InputImage2


class OutputBlended(Output):
    name: Literal["outputBlended"] = "outputBlended"
    value: Images
    type: Literal["Images"] = "Images"


class OutputDifference(Output):
    name: Literal["outputDifference"] = "outputDifference"
    value: Images
    type: Literal["Images"] = "Images"


class BlendImagesOutputs(Outputs):
    outputBlended: OutputBlended
    outputDifference: OutputDifference


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


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["ImageFiltersEmre"] = "ImageFiltersEmre"
