# **Model Tasarım Şartnamesi**

Pydantic kütüphanesini kullanarak “Package Model” oluştururken standart yapıya uymak için bazı şartlar belirlenmiştir. Bu doküman tüm kapsüllerin belirli bir standartta yazılmasını sağlamak amaçlı oluşturulmuştur. Bu sayede model şartlarına uyan geliştiricilerin tamamı belirli bir yapıda model oluşturabilecektir. 

1. ##  **Package Model**

Modelde  bir  adet “PackageModel” sınıfı bulunmalıdır. Birden fazla olamaz. Package Model type değeri yalnızca capsule, widget veya component olabilir.

| class PackageModel(Package): configs:PackageConfigs type : Literal\["capsule"\] \= "capsule" name: Literal\["ExampleName"\] \= "ExampleName" |
| :---- |

*Kod1.*   
Her PackageModel “PackageConfigs” sınıfı bulundurmalıdır. Yapıda oluşturduğumuz executorlar, “PackageModel” sınıfına “PackageConfigs” sınıfı ile bağlanır. Yapıda bir veya birden fazla executor bulunabilir. 

| class PackageConfigs(Configs): executor1: ConfigExecutor configType: ConfigType |
| :---- |

*Kod2.* 

2. ##  **Executors**

Executor seçimi yapılabilmesi için “ConfigExecutor” sınıfı oluşturulur. Eğer birden fazla executor varsa value kısmında Union içerisinde isimleri eklenir.  
Tek executor içeren örnek:  
Tek executor bulunması durumunda kullanıcı bir executor seçmeyeceği için schema\_extra targetının value olarak verilmesi gerekir. 

| class ConfigExecutor(Config):    name: Literal\["ConfigExecutor"\] \= "ConfigExecutor"    value: Union\[ExampleExecutor\]    type: Literal\["executor"\] \= "executor"    field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist"    class Config:        title \= "Task"        schema\_extra \= {            "target": "value"        } |
| :---- |

*Kod3.*   
Birden fazla executor içeren örnek:  
Birden fazla executor olması durumunda kullanıcı executor seçeceği için target belirtmeye gerek yoktur.

| class ConfigExecutor(Config):    name: Literal\["ConfigExecutor"\] \= "ConfigExecutor"    value: Union\[ExampleExecutor1, ExampleExecutor2, ExampleExecutor3\]    type: Literal\["executor"\] \= "executor"    field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist"     class Config:        title \= "Task" |
| :---- |

*Kod4.*   
*Şekil1* Web tarafında kullanılan örnek bir Executor yapısı.	  
Her executor için bir class oluşturulmalıdır. Her executor istek alıp cevap oluşturabilmek için ExecutorRequest ve ExecutorResponse sınıflarını içermelidir. Executor requeste bağlanacağı için value değeri requestin index numarası olan 0 değeri olarak girilir.

| class ExampleExecutor (Config): name: Literal\["ExampleExecutor"\] \= "ExampleExecutor" value: Union\[ExampleExecutorRequest, ExampleExecutorResponse\] type: Literal\["object"\] \= "object" field: Literal\["option"\] \= "option" class Config:     title \= "Example"     schema\_extra \= {     "target": {     "value": 0     }     } |
| :---- |

*Kod5.* 

3. ## **Request**

Executorların requestleri inputs ve configs opsiyonel değerlerini içerebilir. Örneğin executor bir inputs değeri almıyorsa inputs sınıfı oluşturulmaz.

Configs İçeren Executorun Requesti :

| class ExampleExecutorRequest(Request): inputs: Optional\[ExampleExecutorInputs\] configs: Optional\[ExampleExecutorConfigs\] class Config:     schema\_extra \= {     "target": "configs"     } |
| :---- |

*Kod6.* 

Configs İçermeyen Executorun Requesti :

| class ExampleExecutorRequest(Request): inputs: Optional\[ExampleExecutorInputs\] |
| :---- |

*Kod7.* 

4. ## **Response**

Her executorun responseu Outputs sınıfı içermek zorundadır. 

| class ExampleExecutorResponse(Response): outputs: ExampleExecutorOutputs |
| :---- |

*Kod8.*   
 Eğer executorun Inputsu var ise Inputsların alındığı bir sınıf yazılır.

| class ExampleExecutorInputs(Inputs): input1: Input1 input2: Input2 |
| :---- |

*Kod9.* 

5. ## **Inputs**

Her Input için yeni bir sınıf oluşturulmalıdır. Her Input name, value, type ve field alanlarını içermelidir. Desteklenmeyen type ve field kullanımları hataya sebep olmaktadır. 

| class Image(Config): uID: str mimeType: Literal\["image/jpg", "image/png", "image/gif"\] encoding: Literal\["base64"\] value: Union\[str\]class Images(Config): value: List\[Image\]class InputImage(Config): name: Literal\["inputImage"\] \= "inputImage" value: Images type: Literal\["Images"\] \= "Images" |
| :---- |

*Kod10.* 

6. ## **Configs**

Eğer executorun configsi varsa parametreler configs sınıfı altında yazılır.

| class VehicleConfigs(Configs):  configParameter1: ConfigParameter1  configParameter2: ConfigParameter2  configParameter3: ConfigParameter3  |
| :---- |

*Kod11.*   
Her parametre için yeni bir class oluşturulmalıdır. Oluşturulan classların bazı özellikleri sınıfın içerisinde gösterilmelidir. Bunlar name, value, type ve field olmak üzere dörde ayrılır.Desteklenmeyen type ve field kullanımları hataya sebep olmaktadır. 

**name:** Ulaşacağımız sınıfın ismini gösterir. İsimde programlama dillerindeki isimlendirme standartlarına uymalıdır. Yani boşluk .,/)(%+\! gibi ifadeler içeremez.  
[https://www.w3.org/TR/2014/REC-html5-20141028/forms.html\#dom-form-elements](https://www.w3.org/TR/2014/REC-html5-20141028/forms.html#dom-form-elements)  
[https://www.w3.org/TR/2014/REC-html5-20141028/infrastructure.html\#reflect](https://www.w3.org/TR/2014/REC-html5-20141028/infrastructure.html#reflect)  
**value:** Sınıfın aldığı değeri gösterir.  
**type:** Sınıfın veri tipini gösterir.   
**field:** Sınıfların web tarafındaki görünürlüğünü ifade eden attribute.

1. ### **Desteklenen Kullanımlar** 

**Type:** object, string, number, bool, list, dict

**Nova Type:** Images, Detections, BoundingBox, Image, Detection, Executor, Package, Response, Request, Inputs, Outputs, Configs, Model

**Field:** textInput, dropdownlist , dependentDropdownlist, selectBox, widget, option, hiddenInput

| class ConfigDrawBBoxTrue(Config): name: Literal\["True"\] \= "True" value: Literal\[True\] \= True type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option" class Config:     title \= "Enable"class ConfigDrawBBoxFalse(Config): name: Literal\["False"\] \= "False" value: Literal\[False\] \= False type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option" class Config:     title \= "Disable"class ConfigDrawBBox(Config): name: Literal\["DrawBBox"\] \= "DrawBBox" value: Union\[ConfigDrawBBoxTrue, ConfigDrawBBoxFalse\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist" class Config:     title \= "Drawing BBox" |
| :---- |

*Kod12.* 

7. ## **Outputs**

Executorun outputlarının alındığı bir class yazılmalıdır. Her executorın en az bir tane outputu olmak zorundadır. Outputs sınıfında gösterilen parametre ne ise o outputun sınıfındaki name değeri de o olmalıdır.

| class Output1(Output):    name: Literal\["output1"\] \= "output1"    value: Images    type: Literal\["Images"\] \= "Images" class ExampleExecutorOutputs(Outputs): output1: Output1 |
| :---- |

*Kod13.*   
Her output için bir class oluşturulmalıdır. Outputlar name, value ve type içermek zorundadır. Outputların valueları istenilen değişkenleri içeren bir class oluşturularak da verilebilmektedir.

Örnek 1:

| class Detects(Output): value: list imgUID: strclass OutputDetect(Output): name: Literal\["OutputDetect"\] \= "OutputDetect" value: List\[Detects\] type: Literal\["Detections"\] \= "Detections" |
| :---- |

*Kod14.* 

Örnek 2:

| class Reason(Output): name: Literal\["Reason"\] \= "Reason" value: List type: Literal\["list"\] \= "list"class OutputReason(Output): name: Literal\["OutputReason"\] \= "OutputReason" value: Reason type: Literal\["list"\] \= "list" |
| :---- |

*Kod15.* 

8. ## **Fields**

   1. ### **textInput**

| class ConfigParams(Config): name: Literal\["ConfigParams"\] \= "ConfigParams" value: float \= Field(ge=0, le=1) type: Literal\["number"\] \= "number" field: Literal\["textInput"\] \= "textInput" class Config:     title="Params"class ExecutorConfigs(Configs): configParams: ConfigParams |
| :---- |

*Kod18.*   
*Şekil2* Web tarafında kullanılan örnek bir textInput parametresi.             

2. ### **dropdownlist**

| class OptionCar(Config): name: Literal\["OptionCar"\] \= "OptionCar" value: Literal\["Car"\] \= "Car" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Car" class OptionMotor(Config): name: Literal\["OptionMotor"\] \= "OptionMotor" value: Literal\["Motor"\] \= "Motor" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Motor"class OptionTruck(Config): name: Literal\["OptionTruck"\] \= "OptionTruck" value: Literal\["Truck"\] \= "Truck" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Truck" class ConfigParams(Config): name: Literal\["ConfigParams"\] \= "ConfigParams" value: Union\[OptionCar, OptionMotor, OptionTruck\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist" class Config:     title \= "Params"class ExampleConfigs(Configs): configParams: ConfigParams |
| :---- |

*Kod19.* 

*Şekil3* Web tarafında kullanılan örnek bir dropdownlist parametresi*.*

3. ### **selectBox**

| class OptionCar(Config): name: Literal\["OptionCar"\] \= "OptionCar" value: Literal\["Car"\] \= "Car" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Car"class OptionMotor(Config): name: Literal\["OptionMotor"\] \= "OptionMotor" value: Literal\["Motor"\] \= "Motor" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Motor"class OptionTruck(Config): name: Literal\["OptionTruck"\] \= "OptionTruck" value: Literal\["Truck"\] \= "Truck" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Truck"class ConfigParams(Config): name: Literal\["ConfigParams"\] \= "ConfigParams" value: List\[Union\[OptionCar, OptionMotor, OptionTruck\]\] type: Literal\["object"\] \= "object" field: Literal\["selectBox"\] \= "selectBox" class Config:     title \= "Params"class ExampleConfigs(Configs):  configParams: ConfigParams  |
| :---- |

*Kod20.*   
Not : ConfigParams classının value değeri List\[Union\[\]\] olarak kullanılmak zorundadır.

*Şekil4* Web tarafında kullanılan selectBox parametresi. 

4. ### **dependentDropdownlist**

|  class OptionTrue(Config): name: Literal\["OptionTrue"\] \= "OptionTrue" value: Literal\[True\] \= True type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option"   class Config:     title="Enable" class OptionFalse(Config): name: Literal\["OptionFalse"\] \= "OptionFalse" value: Literal\[False\] \= False type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option"   class Config:     title="Disable" class Example1(Config): name: Literal\["Example1"\] \= "Example1" value: float type: Literal\["number"\] \= "number" field: Literal\["textInput"\] \= "textInput"   class Config:     title="Example1" class ConfigParam2(Config): name: Literal\["ConfigParam2"\] \= "ConfigParam2" value: Union\[OptionTrue,OptionFalse\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist"   class Config:     title="Param2"class ConfigParam1(Config): name: Literal\["ConfigParam1"\] \= "ConfigParam1" example: Example1 value: Literal\["ConfigParam1"\] \= "ConfigParam1" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option"  class Config:     title="Param1"class ConfigParams(Config): name: Literal\["ConfigParams"\] \= "ConfigParams" value:Union\[ConfigParam1,ConfigParam2\] type: Literal\["object"\] \= "object" field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist"  class Config:     title="Params" class ExecutorConfigs(Configs): configParams: ConfigParams |
| :---- |

*Kod21.*   
*Şekil5* Web tarafında kullanılan dependentDropdownlist parametresi.  
*Şekil6* Web tarafında kullanılan dependentDropdownlist parametresi ile açılan textInput.

*Şekil7* Web tarafında kullanılan dependentDropdownlist parametresi ile açılan dropdownlist .  

5. ### **widget**

|  class ConfigParam(Config):    name: Literal\["ConfigParam"\] \= "ConfigParam"    value: str    type: Literal\["string"\] \= "string"    field: Literal\["widget"\] \= "widget"*\#widget oluşturmak için schema extra altında 2 alana ihtiyaç vardır. bunlar "class" ve "options" alanlarıdır. class alanı web tarafında yazılan widgetın yoludur. options alanı ise alabileceği optionlar olur.*      class Config:        schema\_extra \= {            "class": "\\portalium\\storage\\widgets\\widget",            "options": {                "multiple": 0,                "returnAttribute": \[                    "name"                \],                "name": "app::logo\_wide"                *\#\# İkinci bir widget kullanıldığında name değeri farklı verilmek zorundadır.*            }        }        title \= "Example" class ExecutorConfigs(Configs): configParam:ConfigParam  |
| :---- |

*Kod22.*   
*Şekil8*  Web tarafında kullanılan widget parametresi*.*

6. ### **Value**

Bir sınıfın field alanı, dropdownlist veya dependentDropdownlist olarak belirtilmiş ise o sınıfın value alanı Union olmalıdır.

| class ConfigExample(Param): name: Literal\["ConfigExample"\] \= "ConfigExample" value: Union\[Apple, Banana, Orange\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist"    class Config:        title \= " ConfigExample " |
| :---- |

*Kod23.* 

7. ### **Value (Bağlı)**

Bir sınıfın field alanı dropdownlist veya dependentDropdownlist ise o sınıfın value değerlerinin bağlı olduğu sınıfların value değerleri 0 olamaz. 

| class ExampleClass1(Config): name: Literal\["ExampleClass1"\] \= "ExampleClass1" value: Literal\["1"\] \= "1" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option"class ExampleClass2(Config): name: Literal\["ExampleClass2"\] \= "ExampleClass2" value: Literal\["2"\] \= "2" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option"class ExampleClass3(Config): name: Literal\["ExampleClass3"\] \= "ExampleClass3" value: Literal\["3"\] \= "3" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option"class ExampleModel(Config): field: Literal\["dropdownlist"\] \= "dropdownlist" value: Union\[ExampleClass1, ExampleClass2, ExampleClass3\] class Config:     schema\_extra \= {     "target": "value"     } |
| :---- |

*Kod25.* 

8. ### **Group**

Belirli form ögelerinin gruplandırılmak ve sekmeli yapıda gösterilmek istenildigi durumlarda 'group' anahtar kelimesi ile bir özellik eklenmelidir. Eğer herhangi bir sekmeye dahil edilmek istenmiyor ise; ya group parametresinin value değeri 'default' olmalıdır ya da group parametresi eklenmemelidir. Aşağıdaki örnekte ExampleModel1 ve ExampleModel2 parametreleri ExampleGroup1 sekmesinde gösterilecektir. ExampleModel3 ve ExampleModel4 parametreleri ExampleGroup2 sekmesinde gösterilecektir. ExampleModel5 parametresi herhangi bir sekmede gösterilmeyecektir, ana yapıda gösterilecektir.

| class ExampleModel1(Config): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup1"\] \= "ExampleGroup1" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel2(Config): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup1"\] \= "ExampleGroup1" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel3(Config): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup2"\] \= "ExampleGroup2" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel4(Config): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup2"\] \= "ExampleGroup2" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel5(Config): name: Literal\["Example"\] \= "Example" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist" |
| :---- |

*Kod26.* 

9. ## **İsimlendirme**

Sınıfların name, type ve field alanları her zaman Literal tipinde belirtilmelidir. 

| class ExampleConfig(Config): name: Literal\["Example"\] \= "Example" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist" |
| :---- |

*Kod16.* 

Web tarafı için verilen attributeların hepsi CamelCase’e uygun olmalıdır.

| class ExecutorInputs(Inputs):    inputImage: InputImage |
| :---- |

*Kod17.*   
Bütün Classların baş harfleri büyük harf ile başlamalıdır.

10. ## **Title**

Bir parametreyi ya da executoru ifade eden classlarda title değeri bulunmalıdır. Title değeri o sınıfın web tarafındaki görünür kısmını ifade etmektedir.

| class OptionCar(Config):  name: Literal\["OptionCar"\] \= "OptionCar"  value: Literal\["Car"\] \= "Car"  type: Literal\["string"\] \= "string"  field: Literal\["option"\] \= "option"   class Config:      title \= "Car"   class OptionMotor(Config):  name: Literal\["OptionMotor"\] \= "OptionMotor"  value: Literal\["Motor"\] \= "Motor"  type: Literal\["string"\] \= "string"  field: Literal\["option"\] \= "option"   class Config:      title \= "Motor"   class OptionTruck(Config):  name: Literal\["OptionTruck"\] \= "OptionTruck"  value: Literal\["Truck"\] \= "Truck"  type: Literal\["string"\] \= "string"  field: Literal\["option"\] \= "option"   class Config:      title \= "Truck"  class ConfigParams(Config):  name: Literal\["ConfigParams"\] \= "ConfigParams"  value: Union\[OptionCar, OptionMotor, OptionTruck\]  type: Literal\["object"\] \= "object"  field: Literal\["dropdownlist"\] \= "dropdownlist"    class Config:      title \= "Params" |
| :---- |

*Kod24.* 

11. ## **Yapı**

Package Model yapısı, aşağıdan yukarıya doğru yazılarak oluşturulur. Bunun sebebi tanımlanmayan bir öğe başka bir öğenin girdisi olarak kullanılamamasıdır. En uç noktadaki obje ilk sıraya yazılır. Başka bir objenin girdisi olan bir obje yukarıda verilmelidir ki girdi olarak kullanılabilsin.  
Input, output gibi parametreler önce yazılır. Ardından executorların request ve responseları ve en son executorlar ile package sınıfları yazılır. Ana iskelet, [Örnek Package Model 1](#package-model)’de gösterilmiştir.

# **Örnek Uygulamalar**

1. ## **Package Model**  {#package-model}

| from typing import Optional, Union, Literalfrom sdks.novavision.src.base.model import Package, Images, Inputs, Configs, Outputs, Response, \\    Request, Config, Input, Outputclass InputImage(Input):    name: Literal\["inputImage"\] \= "inputImage"    value: Images    type: Literal\["Images"\] \= "Images"class OutputImage(Output):    name: Literal\["outputImage"\] \= "outputImage"    value: Images    type: Literal\["Images"\] \= "Images"class ExampleFunctionTrue(Config):    name: Literal\["True"\] \= "True"    value: Literal\[True\] \= True    type: Literal\["bool"\] \= "bool"    field: Literal\["option"\] \= "option"    class Config:        title \= "Enable"class ExampleFunctionFalse(Config):    name: Literal\["False"\] \= "False"    value: Literal\[False\] \= False    type: Literal\["bool"\] \= "bool"    field: Literal\["option"\] \= "option"    class Config:        title \= "Disable"class ExampleFunction(Config):    name: Literal\["ExampleFunction"\] \= "ExampleFunction"    value: Union\[ExampleFunctionTrue, ExampleFunctionFalse\]    type: Literal\["object"\] \= "object"    field: Literal\["dropdownlist"\] \= "dropdownlist"    class Config:        title \= "ExampleFunction"class ExampleExecutorConfigs(Configs):    exampleFuntion: ExampleFunctionclass ExampleExecutorInputs(Inputs):    inputImage: InputImageclass ExampleExecutorOutputs(Outputs):    outputImage: OutputImageclass ExampleExecutorRequest(Request):    inputs: Optional\[ExampleExecutorInputs\]    configs: ExampleExecutorConfigs    class Config:        schema\_extra \= {            "target": "configs"        }class ExampleExecutorResponse(Response):    outputs: ExampleExecutorOutputsclass ExampleExecutor(Config):    name: Literal\["ExampleExecutor"\] \= "ExampleExecutor"    value: Union\[ExampleExecutorRequest, ExampleExecutorResponse\]    type: Literal\["object"\] \= "object"    field: Literal\["option"\] \= "option"    class Config:        title \= "Example"        schema\_extra \= {            "target": {                "value": 0            }        }class ConfigExecutor(Config):    name: Literal\["ConfigExecutor"\] \= "ConfigExecutor"    value: Union\[ExampleExecutor\]    type: Literal\["executor"\] \= "executor"    field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist"    class Config:        title \= "Task"        schema\_extra \= {            "target": "value"        }class PackageConfigs(Configs):    executor: ConfigExecutorclass PackageModel(Package):    configs: PackageConfigs    type: Literal\["capsule"\] \= "capsule"    name: Literal\["ExampleName"\] \= " ExampleName "    uID \= "1331112" |
| :---- |

*Kod27.* 

2. ## **Package Model**

| *\# ExampleExecutor3 sadece Configs sınıfını içeriyor.*class ExampleExecutor3Configs(Configs):    configType: ConfigType*\# ExampleExecutor2 sadece Inputs sınıfını içeriyor.*class ExampleExecutor2Inputs(Inputs):    input1: Input1    input2: Input2*\# ExampleExecutor1 hem Inputs hem de Configs sınıfını içeriyor.**\# Sınıflar içerisinde yapılan konfigürasyonlar Configs sınıfında bir araya getirilir.*class ExampleExecutor1Configs(Configs):    configType: ConfigType*\# Kullanıcıdan alınan bir input varsa Inputs sınıfı oluşturulur ve inputların alındığı sınıf buraya eklenir.**\# Bu örnekte alınan inputların sınıfı gösterilmemiştir.**\# Girdilerin sınıfları bu sınıfa eklenmelidir.**\# İhtiyaca göre farklı sayıda input sınıfı eklenebilir.*class ExampleExecutor1Inputs(Inputs):    input1: Input1    input2: Input2class ExampleExecutor3Outputs(Outputs):    output1: Output1    class ExampleExecutor2Outputs(Outputs):    output1: Output1    output2: Output2*\# Her executorın çıktıları için Outputs sınıfı oluşturulur. Oluşturulan çıktıların sınıfı Outputs sınıfına eklenir.**\# \#Bu örnekte sadece çıktıların toplandığı sınıf olan Outputs gösterilmiştir.**\# Çıktıların sınıfları bu sınıfa eklenmelidir.**\# İhtiyaca göre farklı sayıda output sınıfı eklenebilir.*class ExampleExecutor1Outputs(Outputs):    output1: Output1    output2: Output2    output3: Output3class ExampleExecutor3Response(Response):    outputs: ExampleExecutor3Outputsclass ExampleExecutor3Request(Request):    configs: ExampleExecutor3Configs    class Config:        schema\_extra \= {            "target": "configs"        }class ExampleExecutor2Response(Response):    outputs: ExampleExecutor2Outputsclass ExampleExecutor2Request(Request):    inputs: Optional\[ExampleExecutor2Inputs\]    class Config:        schema\_extra \= {            "target": "configs"        }*\# Output(lar) response sınıfına eklenerek response sınıfı oluşturulur.*class ExampleExecutor1Response(Response):    outputs: ExampleExecutor1Outputs*\# Varsa input ve config sınıf(lar)ı request sınıfına eklenerek request sınıfı oluşturulur.*class ExampleExecutor1Request(Request):    inputs: Optional\[ExampleExecutor1Inputs\]    configs: ExampleExecutor1Configs    class Config:        schema\_extra \= {            "target": "configs"        }class ExampleExecutor3(Config):    name: Literal\["ExampleExecutor3"\] \= "ExampleExecutor3"    value: Union\[ExampleExecutor3Request, ExampleExecutor3Response\]    type: Literal\["object"\] \= "object"    field: Literal\["option"\] \= "option"    class Config:        title \= " Example "        schema\_extra \= {            "target": {                "value": 0            }        }class ExampleExecutor2(Config):    name: Literal\["ExampleExecutor2"\] \= "ExampleExecutor2"    value: Union\[ExampleExecutor2Request, ExampleExecutor2Response\]    type: Literal\["object"\] \= "object"    field: Literal\["option"\] \= "option"    class Config:        title \= " Example "        schema\_extra \= {            "target": {                "value": 0            }        }*\# Her executora istek alıp cevap oluşturabilmesi için bir request ve bir response sınıfı eklenir.**\# Bu sınıflara ulaşabilmek adına value kısmında index olarak belirtilir.**\# schema\_extra'da value kısmında belirtilen değer  verilen seçeneklerden hangisine gidileceğini gösterir.**\# Örneğin ExampleExecutor1'in gideceği alan aşağıda verilen kodda 0 olarak verilerek ExampleExecutor1Request'e yönlendirilmiştir.*class ExampleExecutor1(Config):    name: Literal\["ExampleExecutor1"\] \= "ExampleExecutor1"    value: Union\[ExampleExecutor1Request, ExampleExecutor1Response\]    type: Literal\["object"\] \= "object"    field: Literal\["option"\] \= "option"    class Config:        title \= " Example "        schema\_extra \= {            "target": {                "value": 0            }        }class ConfigExecutor(Config):    name: Literal\["ConfigExecutor"\] \= "ConfigExecutor"    value: Union\[ExampleExecutor1, ExampleExecutor2, ExampleExecutor3\]    type: Literal\["executor"\] \= "executor"    field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist"    class Config:        title \= "Task"*\# PackageModel'de tek bir executor sınıfı bulundurmak için tüm executorlar PackageExecutor sınıfı altında toplanır.*class PackageConfigs(Configs):    executor1: ConfigExecutor    configType: ConfigType*\# Bütün sınıflar PackageModel üzerine kurulacağı için önce bu sınıf yazılır.**\# typelarda belirtilen tipler haricinde bir tip barındıramaz.**\# Typelara verilebilecek değerler model kılavuzunda belirtilmiştir.*class PackageModel(Package):    configs: PackageConfigs    type: Literal\["capsule"\] \= "capsule"    name: Literal\["ExampleName"\] \= " ExampleName "    uID \= "1331112" |
| :---- |

*Kod28.* 

