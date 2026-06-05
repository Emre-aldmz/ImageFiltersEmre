"""
    ImageFilters Package Model

    2 Executor yapısı:
    - RotateImage: 1 input (resim), 1 output (döndürülmüş resim)
    - BlendImages: 2 input (2 resim), 2 output (karışım + fark)

    Yapı aşağıdan yukarıya doğru yazılmıştır (Şartname Bölüm 11).
"""

from pydantic import Field
from typing import List, Optional, Union, Literal
from sdks.novavision.src.base.model import (
    Package, Image, Images, Inputs, Configs, Outputs,
    Response, Request, Output, Input, Config
)


# =====================================================
# Executor 1: RotateImage (1 input, 1 output)
# =====================================================

# --- Input Parametresi ---
class InputImage(Input):
    """Döndürülecek resim girişi."""
    name: Literal["inputImage"] = "inputImage"
    value: Images
    type: Literal["Images"] = "Images"


# --- Config Parametresi: Derece ---
class Degree(Config):
    """
        Resmin döndürüleceği açı değeri.
        Pozitif değerler saat yönünün tersine,
        negatif değerler saat yönünde döndürme yapar.
    """
    name: Literal["Degree"] = "Degree"
    value: int = Field(ge=-359, le=359, default=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Angle"


# --- Inputs ---
class RotateImageInputs(Inputs):
    inputImage: InputImage


# --- Configs ---
class RotateImageConfigs(Configs):
    degree: Degree


# --- Output Parametresi ---
class OutputImage(Output):
    """Döndürülmüş resim çıktısı."""
    name: Literal["outputImage"] = "outputImage"
    value: Images
    type: Literal["Images"] = "Images"


# --- Outputs ---
class RotateImageOutputs(Outputs):
    outputImage: OutputImage


# --- Request ---
class RotateImageRequest(Request):
    inputs: Optional[RotateImageInputs]
    configs: RotateImageConfigs

    class Config:
        schema_extra = {
            "target": "configs"
        }


# --- Response ---
class RotateImageResponse(Response):
    outputs: RotateImageOutputs


# --- Executor ---
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


# =====================================================
# Executor 2: BlendImages (2 input, 2 output)
# =====================================================

# --- Input Parametreleri ---
class InputImage1(Input):
    """Karıştırılacak birinci resim."""
    name: Literal["inputImage1"] = "inputImage1"
    value: Images
    type: Literal["Images"] = "Images"


class InputImage2(Input):
    """Karıştırılacak ikinci resim."""
    name: Literal["inputImage2"] = "inputImage2"
    value: Images
    type: Literal["Images"] = "Images"


# --- Inputs ---
class BlendImagesInputs(Inputs):
    inputImage1: InputImage1
    inputImage2: InputImage2


# --- Output Parametreleri ---
class OutputBlended(Output):
    """İki resmin karışım sonucu."""
    name: Literal["outputBlended"] = "outputBlended"
    value: Images
    type: Literal["Images"] = "Images"


class OutputDifference(Output):
    """İki resim arasındaki fark."""
    name: Literal["outputDifference"] = "outputDifference"
    value: Images
    type: Literal["Images"] = "Images"


# --- Outputs ---
class BlendImagesOutputs(Outputs):
    outputBlended: OutputBlended
    outputDifference: OutputDifference


# --- Request (Configs yok, sadece Inputs) ---
class BlendImagesRequest(Request):
    inputs: Optional[BlendImagesInputs]


# --- Response ---
class BlendImagesResponse(Response):
    outputs: BlendImagesOutputs


# --- Executor ---
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


# =====================================================
# Package Yapısı
# =====================================================

# Birden fazla executor olduğu için ConfigExecutor'da target belirtilmez (Şartname Kod4)
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
