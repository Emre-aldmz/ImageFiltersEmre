from pydantic import Field, validator
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Inputs, Configs, Outputs,
    Response, Request, Output, Input, Config
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"


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
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"


class RotateImageOutputs(Outputs):
    outputImage: OutputImage


class RotateImageRequest(Request):
    inputs: Optional[RotateImageInputs]
    configs: RotateImageConfigs

    class Config:
        schema_extra = {
            "target": "configs"
        }


class RotateImageResponse(Response):
    outputs: RotateImageOutputs


class RotateImageExecutor(Config):
    name: Literal["RotateImageExecutor"] = "RotateImageExecutor"
    value: Union[RotateImageRequest, RotateImageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Rotate Image"
        schema_extra = {
            "target": {
                "value": 0
            }
        }


class InputImage1(Input):
    name: Literal["inputImage1"] = "inputImage1"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"


class InputImage2(Input):
    name: Literal["inputImage2"] = "inputImage2"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"


class BlendImagesInputs(Inputs):
    inputImage1: InputImage1
    inputImage2: InputImage2


class OutputBlended(Output):
    name: Literal["outputBlended"] = "outputBlended"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"


class OutputDifference(Output):
    name: Literal["outputDifference"] = "outputDifference"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get('value')
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"


class BlendImagesOutputs(Outputs):
    outputBlended: OutputBlended
    outputDifference: OutputDifference


class BlendImagesRequest(Request):
    inputs: Optional[BlendImagesInputs]


class BlendImagesResponse(Response):
    outputs: BlendImagesOutputs


class BlendImagesExecutor(Config):
    name: Literal["BlendImagesExecutor"] = "BlendImagesExecutor"
    value: Union[BlendImagesRequest, BlendImagesResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Blend Images"
        schema_extra = {
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
    name: Literal["ImageFilters"] = "ImageFilters"
