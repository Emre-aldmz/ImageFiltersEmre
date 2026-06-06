import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src/models'))

from PackageModel import PackageModel

data = {
  "type": "component",
  "name": "ImageFiltersEmre",
  "configs": {
    "executor": {
      "name": "ConfigExecutor",
      "value": {
        "name": "RotateImage",
        "value": {
          "configs": {
            "degree": {
              "name": "Degree",
              "value": 30,
              "type": "number",
              "field": "textInput"
            }
          }
        },
        "type": "object",
        "field": "option"
      },
      "type": "executor",
      "field": "dependentDropdownlist"
    }
  }
}

model = PackageModel(**data)
print("Degree value:", model.configs.executor.value.value.configs.degree.value)
