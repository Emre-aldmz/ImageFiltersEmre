# **Package Geliştirici Kılavuzu**

Kapsül geliştirme işlemi için “Package” adı verilen template modeli bulunmaktadır. Bu model git ortamında public olarak tüm geliştirilere açıktır. Geliştiriciler bu package yapısından template alarak yeni modeller oluşturacaktır. Package yapısından template alınan paket içerisinde gerekli geliştirme işlemleri yapılacaktır. Bu işlemler geliştirilirken image adı verilen geliştirme ortamları bulunmaktadır. Geliştirme işlemine göre ilgili image seçilerek geliştirme işlemi için ortam oluşturulur. Image içerisinde capsul ve component adı verilen klasörler bulunmaktadır. Geliştirilecek kapsülün yapısına göre ilgili klasörün altına oluşturulan paket eklenecektir. Bu kısımda gerekli geliştirme işlemleri yapılmaya başlanır. 

## **1.1. Image (Docker)**

Image (İmaj), geliştirme işlemlerinin yapıldığı genel alanlardır. Her bir kapsül veya komponent geliştirilmesi yapılması için image yapılarına ihtiyaç duyulur. Bu durumlar için oluşturulmuş image yapıları bulunmaktadır. Ayrıca uygun image bulunmaması durumunda image adı verdiğimiz depoyu kullanılarak kendi imajlarını oluşturabilmektedir.   
Image yapısının içinde Capsules, Components, Sdks, Dockerfile, Requirements, Service.py, Widgets ve Modules dosyaları bulunmaktadır. Genel olarak image yapısı aşağıdaki şekilde görülmektedir. Image içerisinde zorunlu olarak bulunması gereken dosyalar capsules, components, sdks, Dockerfile.dev, Dockerfile.prod, requirements.dev.txt, requirements.prod.txt, service.py ve README.md dosyalarıdır. Widgets ve Modules dosyaları gerekli duyulması halinde kullanılan dosyalardır.   
![][image1]

Bu dosyaların genel yapısı maddeler halinde açıklanmıştır.

**capsules:** Proje içerisinde yer alan kapsül adı verilen modellerin geliştirildiği klasör yapısıdır. Burada ilgili kapsüllerin depoları çekilerek geliştirme işlemi yapılır. Örnek bir kapsül yapısı Bölüm 2.1’de açıklanmıştır.

**components:** Proje içerisinde yer alan komponent adı modellerin geliştirildiği klasör yapısıdır. Burada ilgili komponentlerin depoları çekilerek geliştirme işlemi yapılır.Örnek bir komponent yapısı Bölüm 2.1’de açıklanmıştır.

**sdks:** Projenin geliştirilmesinde kullanılan ve kapsüllerin ve komponentlerin bağımlı olduğu dosyaları içeren Python kütüphanesidir. Sdks kapsülünün ayrıntılı açıklaması Bölüm 3.1’de açıklanmıştır.

**dockerfile:** Projenin docker ortamında kurulumunu sağlayan linux komutlarının bulunduğu dosyadır. Bu Dockerfile.prod ve Dockerfile.Dev olarak iki farklı modu bulunmaktadır. Dockerfile.prod ile kullanıcılar için gerekli komutlar bulunmaktadır. Dockerfile.Dev  altında ise geliştiriciler için gerekli komutlar bulunmaktadır. Örnek Komutlar aşağıdaki gibidir. 

**FROM ubuntu:20.04**  
**ARG DEBIAN\_FRONTEND=noninteractive**  
**WORKDIR /opt/project**  
**ADD . /opt/project**  
**RUN rm /usr/bin/pip**  
**RUN apt-get update**  
**RUN ln \-s /usr/bin/python3 /usr/bin/python**  
**RUN ln \-s /usr/bin/pip3 /usr/bin/pip**  
**RUN apt install git \-y**  
**RUN pip install \-r requirements.dev.txt**

**requirements:** Projenin geliştirilmesinde gerekli olan Python kütüphanelerinin yer aldığı txt dosyasıdır. Bu dosya geliştirici ve kullanıcı için iki farklı dosya şeklindedir. Requirements.prod ve Requirements.dev olarak iki dosya bulunmaktadır. Örnek Dosya içeriği aşağıdaki gibidir. Burada gerekli kütüphane isimleri ve sürüm bilgileri yazılmaktadır.

requests\==2.25.1  
urllib3  
pydantic\==1.10.8  
setuptools  
fastapi\==0.88.0  
hypercorn\==0.14.3  
uvicorn\==0.20.0  
opencv-python\==4.5.5.64  
opencv-contrib-python\>=4.5.5.64

**service.py:** FastApi mikroservis framework aktif olarak çalışması için gerekli service kodlarının yer aldığı Python modülüdür.  Örnek bir Service kodu aşağıdaki gibidir. 

**import uvicorn**  
**from fastapi import FastAPI,Request**  
**import json**  
**From capsules.capsule.src.executors.segmentation import UnetInferrer**  
**from sdks.novavision.src.base.service import Service**  
**from sdks.novavision.src.base.bootstrap import Bootstrap**  
**app \= FastAPI()**

**executors \={'Segmentation':{"Segmentation":UnetInferrer}}**  
**btstrp \= Bootstrap(executors)**  
**bootstrap \= btstrp.run()**

**@app.post('/api')**  
**async def api(request: Request):**  
    **json\_data \= await request.json()**  
    **json\_data \= json.dumps(json\_data)**  
    **resp \= Service(json\_data, executors, bootstrap).run()**  
    **return resp**

**if \_\_name\_\_ \== "\_\_main\_\_":**  
    **uvicorn.run(app, host="0.0.0.0", port=8000)**

Burada FastApi kütüphanesinin import edilmesi işlemi yapılmaktadır. Executors içerisine çalıştırılacak kapsül bilgileri ve executor ismi yazılmalıdır. Servis /api kökü ile istek beklemektedir. İsteğin içeriğine göre kapsüllere yönlendirme işlemi yapmaktadır. 

**widgets:** Platforma göre verilerin görselleştirilmesinde kullanılan araçtır. Ayrıntılı bir şekilde Bölüm 4.1’de açıklanmıştır.  
**modules:** Package template ile oluşturulmuş ancak capsule ya da component formatında hizmet vermeyen, Gateway gibi ağ tabanlı işlemlerin yapıldığı dosyadır.

Geliştiriciler ilgili uygun image kullanarak Capsules ve Components altına kendi kapsülerini ekleyerek geliştirme işlemi yapması gereklidir. 

**1.2. Package**

Package, geliştiricilerin kapsül ve komponent geliştirmesi için kullandıkları yapıdır. Bu yapının git ortamında şablonu bulunmaktadır. Bu şablon kullanılarak kendi geliştirme ortamlarını oluşturulmaları gereklidir. Geliştiriciler kullanıcıları image altına capsules veya components klasörleri altına oluşturdukları paketleri eklenmelidir. 

Package deposu içinde apps, notebooks, resources, tests, src klasörleri yer almaktadır. Ayrıca src klasörü içerisinde classes,configs, executors, models, utils, dataloaders ve weights klasörleri yer almaktadır.  Örnek dosya yapısı aşağıdaki gibidir.

![][image2]  
Örnek dosya içerisinde capsule adında yeni bir paket oluşturulmuştur. Bu paket içerisinde  apps, notebooks, resources, tests, src klasörleri yer almaktadır. Apps, notebooks, resources, tests ve src klasörleri kapsüllerde bulunmak zorundadır. Ayrıca src klasörü altında classes,configs executors, models, utils, dataloaders ve weights klasörleri bulunmaktadır. Her kapsülde src altında executors ve models klasörleri bulunmak zorundadır. Diğer kalan classes,configs, utils, dataloaders ve weights klasörleri kapsül yapısına göre eklenip çıkarılabilir. 

Bu dosyaların genel yapısı maddeler halinde açıklanmıştır.

**apps:** Geliştirilen model için gerekli uygulamaların yer aldığı dosyadır. Dosya içerisinde service erişim sağlayan istemci (client) kodları  vb dosyalar yer almaktadır. Örnek bir istemci kodu aşağıdaki gibidir.

**import requests**  
**import json**

**ENDPOINT\_URL \= "http://127.0.0.1:8000/api"**  
**def inference():**  
    **request={...}**  
    **request\_json \= json.loads(request.json())**  
    **response \= requests.post(ENDPOINT\_URL, json \=request\_json)**  
    **print(response.raise\_for\_status())**  
    **print(response.json())**  
**if \_\_name\_\_ \=="\_\_main\_\_":**  
    **inference()**

Bu kod içerisinde service istek gönderilmektedir. Bu gönderme işlemi ile Endpoint\_url istek gönderilip cevap beklenmektedir. 

**notebooks:** Geliştirilen modelin Colab veya Jupiter üzerinden çalışması için gerekli ipynb kodlarının yer aldığı dosyadır.

**resources:** Geliştirilen modele ait verilerin ve veritabanının tutulduğu proje dosyasıdır.

**tests:** Geliştirilen modelin test işlemi için gerekli kodların tutulduğu proje dosyasıdır.

**src:** Kaynak klasörlerinin bulunduğu proje dosyasıdır. 

**classes:** Geliştirilen proje ait sınıf yapılarının tutulduğu proje dosyasıdır. Bu dosya içerisinde projenin içinde yer alan ve kullanılan sınıf nesnelerinin tutulmaktadır.  Örnek class yapısı aşağıdaki gibidir.  
**from abc import ABC, abstractmethod**  
**class BaseModel(ABC):**  
    **"""Abstract Model classes that is inherited to all models"""**  
    **def \_\_init\_\_(self, cfg):**  
        **self.config \= Config.from\_json(cfg)**  
    **@abstractmethod**  
    **def load\_data(self):**  
        **pass**  
    **@abstractmethod**  
    **def build(self):**  
        **pass**  
    **@abstractmethod**  
    **def train(self):**  
        **pass**  
    **@abstractmethod**  
    **def evaluate(self):**  
        **pass**

**configs:** Geliştirilen proje ait yapılandırma dosyalarının tutulduğu proje dosyasıdır. Bu dosya içerisinde gerekli yapılandırma dosyaları tutulmaktadır. Bu yapılandırma dosyaları; şemalar, Json ..vb dosyalardır. Örnekler aşağıdaki gibidir.

**CFG \= {**  
    **"data": {**  
        **"path": "oxford\_iiit\_pet:3.2.0",**  
        **"image\_size": 128,**  
        **"load\_with\_info": True**  
    **},**  
    **"train": {**  
        **"batch\_size": 64,**  
        **"buffer\_size": 1000,**  
        **"epoches": 20,**  
        **"val\_subsplits": 5,**  
        **"optimizer": {**  
            **"type": "adam"**  
        **},**  
        **"metrics": \["accuracy"\]**  
    **},**  
    **"model": {**  
        **"input": \[128, 128, 3\],**  
        **"up\_stack": {**  
            **"layer\_1": 512,**  
            **"layer\_2": 256,**  
            **"layer\_3": 128,**  
            **"layer\_4": 64,**  
            **"kernels": 3**  
        **},**  
        **"output": 3**  
    **},**  
    **"project": {**  
        **"path": "/opt/project"**  
    **}**  
**}**

**SCHEMA \= {**  
**"type": "object","properties": {image": {"type": "array","items": {"type": "array","items": {"type": "array","items": {"type": "array","items": {"type": "number"}}}}}},"required": \["image"\]}**

Burada CFG adında bir yapılandırma dosyası oluşturulmuştur. Bu yapılandırma dosyası projenin gerekli noktalarından erişerek kullanılmaktadır. Benzer şekilde SCHEMA adında bir şema oluşturulmuştur ve bu dosya proje içinde ilgili yerlerde kullanılmaktadır.

**dataloaders:** Geliştirilen projeye ait gerekli modellerin yüklendiği ve hazır hale getirildiği proje dosyasıdır. Geliştirilen proje içerisinde kullanılacak ssd, yolo gibi modellerin yüklenilmesi sağlayan kodlar yer almaktadır. Örnek kod aşağıdaki gibidir. 

**import tensorflow as tf**  
**import tensorflow\_datasets as tfds**  
**class DataLoader:**  
**"""Data Loader classes"""**

**@staticmethod**  
**def load\_data(data\_config):**  
**"""Loads dataset from path"""**  
**return tfds.load(data\_config.path,with\_info=data\_config.load\_with\_info)**

Burada ilgili datanın yüklenmesi işlemi için örnek bir class oluşturulup fonksiyon içinde yükleme işlemi yapılmıştır.

**executors:** Geliştirilen projenin çalıştırılma işleminin yapıldığı proje dosyasıdır. Projeye ait tüm çalıştırma kodları bu klasör içinde yer almaktadır. Geliştirilen projenin ilk olarak burada yer alan kodlar ile aktif hale gelerek çalışır ve elde edilen sonuç değeri buradan gönderilir. Örnek executors yapısı aşağıdaki gibidir.

**from capsules.capsule.src.utils.config import Config**  
**from capsules.capsule.src.configs.config import CFG**  
**from capsules.capsule.src.models.PackageModel import PackageModel**  
**from sdks.novavision.src.base.response import Response**  
**from sdks.novavision.src.base.capsule import Capsule**  
**class UnetInferrer(Capsule):**  
**def \_\_init\_\_(self, request, bootstrap):**  
**self.error\_list \= \[\]**  
**super().\_\_init\_\_(request)**  
**self.config \= Config.from\_json(CFG)**  
**self.image\_size \= self.config.data.image\_size**  
**self.model \=bootstrap\["Segmentation"\]\["model"\]**  
**self.predict=self.model.signatures\["serving\_default"\]**  
**self.request.model=PackageModel(\*\*(self.request.data)**  
**self.images \= self.request.get\_param("ImageList")**

Executor içerisinde oluşturulan class yapıları Sdk içerisindeki capsul modellerinden extend edilerek oluşturulmalıdır. Bundan dolayı her classın \_init\_,  bootstrap, run fonksiyonları bulunmalıdır. \_init\_ fonksiyonu 2 parametre almak zorundadır. Bunlar request ve bootstrap olarak isimlendirilmektedir. Image içindeki service doğrudan bu class istek atarak kapsülün çalışmasını sağlamaktadır. İstek gönderirken request parametresine gelen isteği, bootstrap parametresi ise ilgi kapsüle ait model ağırlıkları göndermektedir. Fonksiyon içerisinde model ağırlıkları yüklenmekte ve oluşturulan pydantic model yapısı ile request ile gelen istek kontrol edilmektedir. Kontrol edildikten sonra ilgili parametrelere get\_param fonksiyonu kullanılarak girilmektedir.  Class devamında yer alan iki fonksiyon ise aşağıdaki gibidir. 

**@staticmethod**  
**def bootstrap():**  
**config \= Config.from\_json(CFG)**  
**saved\_path=config.project.path+'/capsules/capsule/src/weights/unet'**  
**model \= tf.saved\_model.load(saved\_path)**  
**model \= {"model":model}**  
**return model**  
**def run(self):**  
**executor \= (...)**  
**packageModel \= PackageModel(executor=executor)**  
**return Response(model=packageModel).response()**

Burada bootstrap fonksiyonu ile service çalıştırıldığında model ağırlıklarının yüklenmesi işlemi yapılmaktadır. Daha sonra yüklendikten sonra ilgili kapsül çalıştırıldığında service tarafından model ağırlıkları kapsüle gönderilmektedir. 

Run fonksiyonu ise kapsüle ait tüm çalıştırma işleminin yapıldığı yerdir. Ayrıca service isteğine cevap bu fonksiyon içerisinden döndürülmektedir. Tüm klasörlere veya classlar erişim buradan erişmesi zorunludur. Burada geri dönüş işlemi için sdk içerisindeki Response modeli kullanılmalıdır. Response içerisine ilgili kapsülünün dönüş formatına uygun model oluşturularak verilmelidir. Son olarak response modelinin içindeki response fonksiyonu çalıştırılmalıdır. 

**models:** Geliştirilen proje ait modellerin bulunduğu proje dosyasıdır. Burada geliştirilen proje içerisinde kullanılan modellerin tanımlaması yapılmaktadır. Her Projenin PackageModel’i olması gereklidir.(PackageModel hakkında bilgi için Bölüm 2 bakınız)  Örnek bir PackageModel aşağıdaki gibidir.

**from pydantic import Field, validator**  
**from typing import List, Optional, Union, Any, Dict,Literal**  
**from sdks.novavision.src.base.model import Package, Executor, ImageList, Param, Inputs, Configs, Outputs, Response, Request**

**class PackageModel(Package):**  
**type \= "capsule"**  
**name \= "Segmentation"**  
**uID \= "1221112"**  
**executor: PackageExecutor**  
**field: Literal\["executor"\] \= "executor"**  
**class Config:**  
**schema\_extra \= {"target": "executor"}**  
**class PackageExecutor(Executor):**  
**name \= "executor"**  
**value: Union\[SegmentationExecutor\]**  
**type:Literal\["executor"\] \= "executor"**  
**field:Literal\["dependentDropdownlist"\]="dependentDropdownlist”**  
**class SegmentationExecutor(Executor):**  
**name \= "Segmentation"**  
**value: Union\[SegmentationRequest, SegmentationResponse\]**  
**type: Literal\["Segmentation"\] \= "Segmentation"**  
**field: Literal\["executor"\] \= "executor"**

**class Config:**  
**schema\_extra \= {"target": {"value": 0}}**

**class configTypeSegmentation(Param):**  
**name: Literal\["segmentation"\] \= "segmentation"**  
**value: Literal\["segmentation"\] \= "segmentation"**  
**type: Literal\["string"\] \= "string"**  
**field: Literal\["option"\] \= "option"**

**class ConfigType(Param):**  
**name: Literal\["configType"\] \= "configType"**  
**value:Union\[configTypeSegmentation\]**  
**type: Literal\["object"\] \= "object"**  
**field:Literal\["dependentDropdownlist"\]="dependentDropdownlist"**

**class SegmentationInputs(Inputs):**  
**inputImage: InputImage**  
**value: str**  
**type: Literal\["object"\] \= "object"**  
**field: Literal\["input"\] \= "input"**

**class SegmentationConfigs(Configs):**  
**configType: ConfigType**  
**value: str \= "Configs"**  
**type: Literal\["object"\] \= "object"**  
**field: Literal\["config"\] \= "config"**

**class SegmentationOutputs(Outputs):**  
**OutputData: OutputData**  
**type: Literal\["object"\] \= "object"**  
**field: Literal\["output"\] \= "output"**

**class SegmentationRequest(Request):**  
**inputs: Optional\[SegmentationInputs\]**  
**configs: SegmentationConfigs**  
**class Config:**  
**schema\_extra \= {**  
**"target": "configs"}**  
**class SegmentationResponse(Response):**  
**outputs: SegmentationOutputs**

Burada örnek bir PackageModel verilmiştir. Bu örnekte oluşturulan classlar sdk içerisindeki base modelden extend alınmıştır. Örnek vermek gerekirse Request classı sdk içindeki Request classından extend aldığı görülmüştür. Ayrıntılı örnekler  Bölüm 2 gösterilmiştir. Bölüm 2 inceleyerek gerekli PackageModel bilgisine ulaşabilirsiniz.

**utils:** Geliştirilen proje için gerekli yardımcı kodların yer aldığı proje dosyasıdır. Proje için kullanılacak yardımcı kod parçaları yer almaktadır.

**weights:** Geliştirilen proje içinde yer alan modele ait ağırlıkların tutulduğu proje dosyasıdır. Geliştirilen proje içinde model yapısı yoksa dosya boş olacaktır. 

Geliştiriciler Bu dosya yapıları kullanarak geliştirme işlemi yapacaklardır. İlgili klasör yapılarına dikkat ederek geliştirme işlemi yapılmalıdır. 

**1.3. SDK yapısı**

Kapsül ve komponentlerin geliştirilmesinde kullanılacak yazılım geliştirme için kullanılan python paketidir. Bu paket içerisinde geliştirme ortamına özgü işlevler ve geliştirmeyi hızlandıracak kütüphaneler ve arayüzler bulunmaktadır. Temel olarak base, helper ve media klasörleri yer almaktadır. Base klasörünün altında model, request, response, component, capsule ve exception sınıfları yer almaktadır.  Media altında ise image sınıfı yer almaktadır. Bu Python Paketi tüm geliştirilecek projeler içinde yer alması gerekmektedir.  
![][image3]

Bu dosyaların genel yapısı maddeler halinde açıklanmıştır. 

**Base:** Projenin geliştirilmesinde kullanılan temel kodların yer aldığı dizindir.

**Bootstrap:** Servis aktif olduğunda geliştirilen projeler içinde yer alan modellerin yüklenmesini sağlayan sınıf yapısıdır. Yükleme işleminin yapıldığı class aşağıdaki gibidir. 

**class Bootstrap():**  
**def \_\_init\_\_(self, executors):**  
**self.executors \= executors**

**def run(self):**  
**bootstrap= {}**  
**for key, executor in self.executors.items():**  
**if isinstance(executor, dict):**  
**bootstraps \= {}**  
**for ky,executr in executor.items():**  
**bootstraps\[ky\]=executr.bootstrap()**  
**bootstrap\[key\]=bootstraps**  
**else:**  
**bootstrap\[key\] \= executor.bootstrap()**  
**return bootstrap**

Bu class ile service içinde çalıştırılmaktadır. Service içerisinde Executors listesine eklenen paketlerin bootsrapları çalıştırılır ve model olarak kayıt edilir. 

**Capsule:** Geliştirilecek kapsül yapıları için oluşturulan temel kapsül modeli yer almaktadır. Temel kapsül yapısı aşağıdaki gibidir.

**from abc import ABC, abstractmethod**

**class Capsule(ABC):**  
**"""Abstract Base Capsule classes that is inherited to all classes"""**  
**@abstractmethod**  
**def \_\_init\_\_(self, request):**  
**self.request \= request**

**@staticmethod**  
**def bootstrap():**  
	**pass**  
**@abstractmethod**  
**def run(self):**  
**return \[\]**

**Component:** Geliştirilecek komponent yapıları için oluşturulan temel Component modeli yer almaktadır.Temel komponent yapısı aşağıdaki gibidir.

**from abc import ABC, abstractmethod**

**class Component(ABC):**  
**"""Abstract Base Capsule classes that is inherited to all classes"""**  
**@abstractmethod**  
**def \_\_init\_\_(self, request):**  
**self.request \= request**

**@staticmethod**  
**def bootstrap():**  
	**pass**  
**@abstractmethod**  
**def run(self):**  
**return \[\]**

**Error:** Geliştirilecek projelerin içierisinde oluşabilecek hataların tutulduğu obje yapısıdır.

**Exception:** Geliştirilecek projelerde hataların meydana getirdiği istisnayı durumların tutulduğu obje yapılarıdır.  Bu istinayı yapılar kullanılarak proje geliştirilmesi gerekmektedir.

**Model:** Geliştirilecek projeler için oluşturulan model yapıların tutulduğu obje yapılarıdır. Bu modeller kullanılarak proje geliştirilmelidir.  

**from pydantic import BaseModel**  
**from typing import List, Union, Literal, Optional, Any**  
**class Model(BaseModel):**  
    **"""NovaVision Base Model classes that is inherited to all classes"""**

**class Param(Model):**  
    **name: str**  
    **value: str**  
    **type: str**  
    **field: str**

**class Inputs(Param):**  
    **name: Literal\["Inputs"\]**

**class Outputs(Param):**  
    **name: Literal\["Outputs"\]**

**class Configs(Param):**  
    **name: Literal\["Configs"\]**

**class Image(Param):**  
    **uID: str**  
    **mime\_type: Literal\["image/jpg", "image/png", "image/gif"\]**  
    **encoding: Literal\["base64"\]**  
    **value: Union\[str\]**

**class ImageList(Param):**  
    **value: List\[Image\]**  
**class Request(Model):**  
    **inputs: Optional\[List\[Inputs\]\]**  
    **configs: List\[Configs\]**

**class Response(Model):**  
    **outputs: List\[Param\]**  
**class Executor(Param):**  
    **value: Union\[Request, Response\]**

**class Package(Model):**  
    **type: str**  
    **name: str**  
    **executor: Executor**  
    **uID: str**

    **def new(cls, \*args, \*\*kwargs):**  
        **cls.new \= super().new**  
        **return super().construct()**

Sdk yer alan temel model yapıları yukarıda verilmiştir. Burada Package, Executor, Response, Request, Configs, Outputs, Inputs, Param modelleri bulunmaktadır. Ayrıca model adında genel bir model bulunmaktadır. Bu model pydantic modelden extend edilmiştir. Extend edilen model kullanılarak diğer modeller oluşturulmuştur. Her bir model kullanımı Bölüm 2.1’deki model kısmında örnek şeklinde gösterilmiştir. Ayrıca Bölüm 2 ‘de kullanım hakkında örnekler yer almaktadır. 

**Request:** Servise gelen isteğe ait obje yapısının oluşturulduğu yerdir. Ayrıca request objesine ait erişim fonksiyonları da yer almaktadır. İsteğin obje döndürüldüğü class yapısı ve fonksiyonları aşağıdaki gibidir.

**class Request:**  
**def \_\_init\_\_(self, json\_data):**  
**try:**  
**self.data \= json\_data**  
**self.model \= ""**  
**self.image \= \[\]**  
**except TypeError as e:**  
**print("error",e)**  
**def get\_param(self,name,data=None):**  
	**Pass**  
**…**

Burada service gelen isteği alarak request objesine dönüştürülmektedir. Bu şekilde istek bir objeye dönüştürülmüş olmaktadır. Ayrıca get\_param() gibi fonksiyonlar ile obje içindeki parametrelere erişim sağlanmaktadır.

**Response:** Servis tarafından gönderilecek geri dönüş değerine ait objenin oluşturulduğu yerdir.  Objenin oluşturulduğu class yapısı aşağıdaki gibidir. Burada dönüş modelini alınıp ilgili isteğe dönüş yapılmaktadır.

**class Response:**  
**def \_\_init\_\_(self, model, error=\[\]):**  
**self.error \= error**  
**self.model \= model**  
**def response(self):**  
**try:**  
**self.response\_model \= json.loads(self.model.json())**  
**return self.response\_model**  
**except (AttributeError,TypeError):**  
**self.error.append({"error":"hata2"})**  
**data={'error':self.error}**  
**return data**

**Service:** Fast api servisine gelen isteklerin çalışacak kapsül ve komponent modellerine gönderildiği servis yapısıdır.  Çalıştırılan class yapısı aşağıdaki gibidir.

**import json**  
**from sdks.novavision.src.base.request import Request**  
**class Service():**  
**def \_\_init\_\_(self,data,executors,load):**  
**self.data=json.loads(data)**  
**self.executors \= executors**  
**self.load=load**

**def run(self):**  
**name \= self.data\["name"\]**  
**request \= Request(self.data)**  
**req\_type=self.data\["type"\]**  
**executor=self.data\["executor"\]\["value"\]\["name"\]**  
**res=self.executors\[name\]\[executor\](request, self.load\[name\]).run()**  
**return res**

Burada service gelen isteğin ilgili kapsül veya komponent yönlendirilmesi yapılmaktadır. Service içinden bu class içindeki run fonksiyonu çalıştırılarak işlem gerçekleştirilir. Class ait olan istek, executors listesi ve bootstrap içindeki modeller bu class’a parametre olarak gönderilmektedir. Bu şekilde istek içindeki ilgili kapsül çalıştırılarak istek kapsüle gönderilmekte ve ilgili kapsüle ait bootstrap modeli gönderilmektedir. 

**Helper:** Projeler için kullanılan genel yardımcı kodların yer aldığı dosyadır.

**Array:** Array içerisinde yer alan bilgilere erişim sağlandığı Python kodudur. Bu kod ile json içerisindeki ilgili value değerine ait keyin döndürülmesini sağlamaktadır. Kod aşağıdaki gibidir.

**class ArrayHelper():**

**@staticmethod**  
**def get\_key(value,array):**  
**for key, val in array.items():**  
**if value \== val:**  
**return key**

**Media:** Projeler için kullanılan medya dosyaların tanımlanmasının yapıldığı dosyadır.

**Image:** Proje içinde kullanılan resim dosyasına ait objenin oluşturulduğu yerdir. Ayrıca image objesine ait fonksiyonlar yer almaktadır. 

**import cv2**  
**import base64**  
**import numpy as np**  
**from sdks.novavision.src.base.model import Image as ImageModel**

**class Image:**  
**@staticmethod**  
**def get\_images(data):**  
	**…**  
**return list\_obj**

**@staticmethod**  
**def get\_uID(data,name):**  
	**…**  
**return img.uID**

**@staticmethod**  
**def encode64(image,mime\_type):**  
**…**  
**return data**

**@staticmethod**  
**def decode64( image\_data):**  
**…**  
**return img**

Burada  get\_images fonksiyonu ile Image objesi oluşturulmaktadır. get\_uID fonksiyonu ile image ait objenin uID alınmaktadır. encode64 fonksiyonu ile ise image base64 dönüştürülmektedir. decode64 ile base64 dosyası image formatına dönüştürülmektedir. 

Sdk python paketinin içerisinde geliştirilecek kapsül yapılarına göre eklemeler yapılacaktır. 

**1.4. Widget Yapısı**

Widget, kapsül ve komponentlerin sonucunda elde edilen verilerin kullanıcı arayüzü bileşenleri şeklinde gösterilmesini sağlamaktadır. Bu araçlar ile kapsül ve komponent sonuçları açılır pencere şeklinde gösterilmesini sağlamaktadır.


**2. Model Tasarım İlkeleri**

PackageModel, Pydantic kütüphanesini kullanarak model tasarımı yapılmaktadır.  Genel model yapısı Şekil-1’de gösterilmiştir.

*Şekil 1\. Paket Modelinin Genel Yapısı*

Model tasarımı yaparken dikkat edilmesi gereken kuralları Aşağıda maddeler halinde açıklanmıştır.

**2.1. PackageModel**

Modelde PackageModel classı bulunmalıdır. Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Package Modelden Extend almalıdır. 

| class PackageModel(Package): type : Literal\["capsule"\] \= "capsule" name: Literal\["ExampleName"\] \= " ExampleName " uID \= "1331112" executor: PackageExecutor field: Literal\["executor"\] \= "executor" class Config:     schema\_extra \= {     "target": "executor"     } |
| :---- |

*Kod1.* 

## **2.2. PackageExecutor** 

Modelde PackageExecutor classı bulunmalıdır.Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Executor Modelden Extend almalıdır. 

Modelin içerdiği executorlar value değerinde belirtilmelidir. Eğer model tek bir executor içeriyorsa schema\_extra da target value olarak belirtilmelidir. Birden fazla executorun bulunduğu durumda kullanılmasına gerek yoktur. Web tarafında kullanılan örnek bir Executor yapısı Şekil 2’ de gösterilmiştir.

Tek Executor İçeren Örnek :

| class PackageExecutor(Executor): name :Literal\["executor"\] \= "executor" value: Union\[ExampleExecutor1\] type:Literal\["executor"\] \= "executor" field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist" class Config:     title \= "Task"     schema\_extra \= {     "target": "value"     } |
| :---- |

*Kod2.* 

Birden Fazla Executor İçeren Örnek:

| class PackageExecutor(Executor): name :Literal\["executor"\] \= "executor" value: Union\[ExampleExecutor1, ExampleExecutor2, ExampleExecutor3\] type:Literal\["executor"\] \= "executor" field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist" class Config:     title \= "Task" |
| :---- |

*Kod3.* 

*Şekil 2* Web tarafında kullanılan Executor yapısı. 

## **2.3. Executor** 

Her executor için bir class oluşturulmalıdır. Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Executor Modelden Extend almalıdır.  Her executorun Request ve Response’u olmalıdır.

| class ExampleExecutor (Executor): name: Literal\[" ExampleExecutor "\] \= " ExampleExecutor " value: Union\[ExampleExecutorRequest, ExampleExecutorResponse\] type: Literal\[" ExampleExecutor "\] \= " ExampleExecutor " field: Literal\["executor"\] \= "executor" class Config:     title \= " Example "     schema\_extra \= {     "target": {     "value": 0     }     } |
| :---- |

*Kod4.* 

## 

## **2.4. Request**

Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Request Modelden Extend almalıdır.  

Executorların Requestleri inputs ve configs opsiyonel değerlerini içerebilir. Inputs ve configsden en az bir tanesini içermelidir. Örneğin executor bir inputs değeri almıyorsa inputs değeri yazılmaz.

Configs İçeren Executorun Requesti :

| class ExampleExecutorRequest(Request): inputs: Optional\[ExampleExecutorInputs\] configs: ExampleExecutorConfigs class Config:     schema\_extra \= {     "target": "configs"     } |
| :---- |

*Kod5.* 

Configs İçermeyen Executorun Requesti :

| class ExampleExecutorRequest(Request): inputs: Optional\[ExampleExecutorInputs\] |
| :---- |

*Kod6.* 

## **2.5. Response**

Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Response Modelden Extend almalıdır.  

Her executorun Responses’i outputs içermek zorundadır. 

| class ExampleExecutorResponse(Response): outputs: ExampleExecutorOutputs |
| :---- |

*Kod7.* 

## **2.6. Inputs**

Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Inputs Modelden Extend almalıdır.  

Input parametreleri olması durumunda Inputsların alındığı bir class yazılır.

| class ExampleExecutorInputs(Inputs): Input1: Input1 Input2: Input2 value: str type: Literal\["object"\] \= "object" field: Literal\["input"\] \= "input" |
| :---- |

*Kod8.* 

## **2.6.1. Inputs Parametre Bilgileri**

Her Input için yeni bir class oluşturulmalıdır. Her Input name, value, type ve field alanlarını içermelidir. Desteklenmeyen type ve field kullanımları hataya sebep olmaktadır. 

| class Image(Param): uID: str mime\_type: Literal\["image/jpg", "image/png", "image/gif"\] encoding: Literal\["base64"\] value: Union\[str\]class ImageList(Param): value: List\[Image\]class InputImage(Param): name: Literal\["InputImage"\] \= "InputImage" value: ImageList type: Literal\["imageList"\] \= "imageList" field: Literal\["img"\] \= "img" |
| :---- |

*Kod9.* 

## **2.7. Configs**

Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Configs Modelden Extend almalıdır.  

Configs parametreleri olması durumunda configs classı yazılır.

| class VehicleConfigs(Configs): configParameter1: ConfigParameter1 configParameter2: ConfigParameter2 configParameter3: ConfigParameter3 value: str \= "Configs" type: Literal\["object"\] \= "object" field: Literal\["config"\] \= "config" |
| :---- |

*Kod10.* 

## **2.8. Parametre** 

Her parametre için yeni bir class oluşturulmalıdır. Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Param Modelden Extend almalıdır.  

Her parametre name, value, type ve field alanlarını içermelidir. Desteklenmeyen type ve field kullanımları hataya sebep olmaktadır.

| class ConfigDrawBBoxTrue(Param): name: Literal\["True"\] \= "True" value: Literal\[True\] \= True type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option" class Config:     title \= "Enable" class ConfigDrawBBoxFalse(Param): name: Literal\["False"\] \= "False" value: Literal\[False\] \= False type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option" class Config:     title \= "Disable" class ConfigDrawBBox(Param): name: Literal\["DrawBBox"\] \= "DrawBBox" value: Union\[ConfigDrawBBoxTrue, ConfigDrawBBoxFalse\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist" class Config:     title \= "Drawing BBox" |
| :---- |

*Kod11.* 

## **2.9. Outputs**

Executorun outputlarının alındığı bir class yazılmalıdır.  Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Outputs Modelden Extend almalıdır.  Her executorın en az bir tane outputu olmak zorundadır. Outputların baş harfleri büyük yazılmalıdır.

| class ExampleExecutorOutputs(Outputs): Output1: Output1 Output2: Output2 type: Literal\["object"\] \= "object" field: Literal\["output"\] \= "output" |
| :---- |

*Kod12.* 

## **2.10. Output Parametreleri** 

Her output parametresi  için bir class oluşturulmalıdır.   Bu model SDK kütüphanesi içerisindeki Model dizinin içindeki  Param Modelden Extend almalıdır.  Outputlar name, value, type ve field içermek zorundadır. Outputların valueleri istenilen değişkenleri içeren bir class oluşturulmalıdır.

Örnek 1:

| class Detects(Param): value: list imgUID: strclass OutputDetect(Param): name: Literal\["OutputDetect"\] \= "OutputDetect" value: List\[Detects\] type: Literal\["Detects"\] \= "Detects" field: Literal\["data"\] \= "data" |
| :---- |

*Kod13.* 

Örnek 2:

| class Reason(Param): name: Literal\["Reason"\] \= "Reason" value: List type: Literal\["list"\] \= "list" field: Literal\["data"\] \= "data"class OutputReason(Param): name: Literal\["OutputReason"\] \= "OutputReason" value: Reason type: Literal\["list"\] \= "list" field: Literal\["data"\] \= "data" |
| :---- |

*Kod14.* 

# **2.11. PackageModel Yazım Kuralları**

## **2.11.1. Field Alanı**

Configs Class'ını extend eden her sınıf field alanı barındırmalıdır. Eğer ilgili sınıf herhangi bir form öğesine karşılık gelmiyorsa, field alanı "config" olarak belirtilmelidir.

| class ExampleConfigs(Configs): configType: ConfigType value: str \= "Configs" type: Literal\["object"\] \= "object" field: Literal\["config"\] \= "config" |
| :---- |

*Kod15.* 

## **2.11.2. Literal Kullanımı**

Sınıfların name, type ve field alanları her zaman Literal tipinde belirtilmelidir. 

| class ExampleModel(BaseModel): name: Literal\["Example"\] \= "Example" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist" |
| :---- |

*Kod16.* 

# **2.11.3. Parametre Kuralları**

Desteklenen Field ve Typeler için desteklenen parametreler aşağıda listelenmiştir ve Örnekler ile açıklanmıştır.

**Desteklenen Fieldlar**:  textInput, dropdownlist , dependentDropdownlist, selectBox, FilePicker, option

**Desteklenen Typeler**: object, string, number, bool, img, widget

### **TextInput Örneği (Şekil-3)**

| class ConfigParams(Param): name: Literal\["ConfigParams"\] \= "ConfigParams" value: float \= Field(ge=0, le=1) type: Literal\["number"\] \= "number" field: Literal\["textInput"\] \= "textInput" class Config:     title="Params"class ExecutorConfigs(Configs): configParams: ConfigParams value: str \= "Configs" type: Literal\["object"\] \= "object" field: Literal\["config"\] \= "config" |
| :---- |

*Kod17.*   
*Şekil 3* Web tarafında kullanılan textInput parametresi*.*

### **Dropdownlist Örneği (Şekil-4)**

| class OptionCar(Param): name: Literal\["OptionCar"\] \= "OptionCar" value: Literal\["Car"\] \= "Car" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Car"class OptionMotor(Param): name: Literal\["OptionMotor"\] \= "OptionMotor" value: Literal\["Motor"\] \= "Motor" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Motor"class OptionTruck(Param): name: Literal\["OptionTruck"\] \= "OptionTruck" value: Literal\["Truck"\] \= "Truck" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Truck"class ConfigParams(Param): name: Literal\["ConfigParams"\] \= "ConfigParams" value: Union\[OptionCar, OptionMotor, OptionTruck\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist" class Config:     title \= "Params" class ExampleConfigs(Configs): configParams: ConfigParams value: str \= "Configs" type: Literal\["object"\] \= "object" field: Literal\["config"\] \= "config" |
| :---- |

*Kod18.* 

*Şekil 4* Web tarafında kullanılan dropdownlist parametresi.

### **SelectedBox Örneği (Şekil-5)**

| class OptionCar(Param): name: Literal\["OptionCar"\] \= "OptionCar" value: Literal\["Car"\] \= "Car" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Car"class OptionMotor(Param): name: Literal\["OptionMotor"\] \= "OptionMotor" value: Literal\["Motor"\] \= "Motor" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Motor"class OptionTruck(Param): name: Literal\["OptionTruck"\] \= "OptionTruck" value: Literal\["Truck"\] \= "Truck" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title \= "Truck"class ConfigParams(Param): name: Literal\["ConfigParams"\] \= "ConfigParams" value: List\[Union\[OptionCar, OptionMotor, OptionTruck\]\] type: Literal\["object"\] \= "object" field: Literal\["selectBox"\] \= "selectBox" class Config:     title \= "Params"class ExampleConfigs(Configs):  configParams: ConfigParams  value: str \= "Configs"  type: Literal\["object"\] \= "object"  field: Literal\["config"\] \= "config" |
| :---- |

*Kod19.*   
Not : ConfigParams classının value değeri List\[Uninon\[\]\] olarak kullanılmak zorundadır.

*Şekil 5* Web tarafında kullanılan selectBox parametresi. 

### **dependentDropdownlist Örneği (Şekil-6, Şekil-7, Şekil-8)**

| class OptionTrue(Param): name: Literal\["OptionTrue"\] \= "OptionTrue" value: Literal\[True\] \= True type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option" class Config:     title="Enable" class OptionFalse(Param): name: Literal\["OptionFalse"\] \= "OptionFalse" value: Literal\[False\] \= False type: Literal\["bool"\] \= "bool" field: Literal\["option"\] \= "option" class Config:     title="Disable" class Example1(Param): name: Literal\["Example1"\] \= "Example1" value: float type: Literal\["number"\] \= "number" field: Literal\["textInput"\] \= "textInput" class Config:     title="Example1" class ConfigParam2(Param): name: Literal\["ConfigParam2"\] \= "ConfigParam2" value: Union\[OptionTrue,OptionFalse\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist" class Config:     title="Param2" class ConfigParam1(Param): name: Literal\["ConfigParam1"\] \= "ConfigParam1" example: Example1 value: Literal\["ConfigParam1"\] \= "ConfigParam1" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class Config:     title="Param1"class ConfigParams(Param): name: Literal\["ConfigParams"\] \= "ConfigParams" value:Union\[ConfigParam1,ConfigParam2\] type: Literal\["object"\] \= "object" field: Literal\["dependentDropdownlist"\] \= "dependentDropdownlist" class Config:     title="Params"  class ExecutorConfigs(Configs): configParams: ConfigParams value: str \= "Configs" type: Literal\["object"\] \= "object" field: Literal\["config"\] \= "config" |
| :---- |

*Kod20.* 

*Şekil 6* Web tarafında kullanılan dependentDropdownlist parametresi.  
   
*Şekil 7*  Web tarafında kullanılan dependentDropdownlist parametresi ile açılan textInput.  
   
*Şekil 8* Web tarafında kullanılan dependentDropdownlist parametresi ile açılan dropdownlist . 

### **FilePicker Örneği (Şekil-9)**

| class Example(Param): name: Literal\["Example"\] \= "Example" value: str type: Literal\["widget"\] \= "widget" field: Literal\["FilePicker"\] \= "FilePicker" class Config:     title \= "ID"class ExecutorConfigs(Configs): example:Example value: str \= "Configs" type: Literal\["object"\] \= "object" field: Literal\["config"\] \= "config" |
| :---- |

*Kod21.* 

*Şekil 9* Web tarafında kullanılan FilePicker parametresi*.*  

# **2.11.4. Union Kullanımı**

 Bir sınıfın field alanı, dropdownlist veya dependentDropdownlist olarak belirtilmiş ise o sınıfın value alanı Union olmalıdır.

| class ConfigExample(Param): name: Literal\[" ConfigExample "\] \= " ConfigExample " value: Union\[Apple, Banana, Orange\] type: Literal\["object"\] \= "object" field: Literal\["dropdownlist"\] \= "dropdownlist" class Config:     title \= " ConfigExample " |
| :---- |

*Kod22.* 

**2.11.5. Title Kullanımı**

Bir parametreyi ya da executoru ifade eden classlarda title değeri bulunmalıdır. Title değeri o sınıfın web tarafındaki görünür kısmını ifade etmektedir.

| class OptionCar(Param):  name: Literal\["OptionCar"\] \= "OptionCar"  value: Literal\["Car"\] \= "Car"  type: Literal\["string"\] \= "string"  field: Literal\["option"\] \= "option"   class Config:      title \= "Car"  class OptionMotor(Param):  name: Literal\["OptionMotor"\] \= "OptionMotor"  value: Literal\["Motor"\] \= "Motor"  type: Literal\["string"\] \= "string"  field: Literal\["option"\] \= "option"   class Config:      title \= "Motor"  class OptionTruck(Param):  name: Literal\["OptionTruck"\] \= "OptionTruck"  value: Literal\["Truck"\] \= "Truck"  type: Literal\["string"\] \= "string"  field: Literal\["option"\] \= "option"   class Config:      title \= "Truck"  class ConfigParams(Param):  name: Literal\["ConfigParams"\] \= "ConfigParams"  value: Union\[OptionCar, OptionMotor, OptionTruck\]  type: Literal\["object"\] \= "object"  field: Literal\["dropdownlist"\] \= "dropdownlist"   class Config:      title \= "Params" |
| :---- |

*Kod23.*

 

# **2.10.6. Value Parametresi Kullanımı**

Bir sınıfın field alanı dropdownlist veya dependentDropdownlist ise o sınıfın value degerlerinin bağlı olduğu sınıfların value degerleri 0 olamaz.

| class ExampleClass1(BaseModel): name: Literal\["ExampleClass1"\] \= "ExampleClass1" value: Literal\["1"\] \= "1" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class ExampleClass2(BaseModel): name: Literal\["ExampleClass2"\] \= "ExampleClass2" value: Literal\["2"\] \= "2" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class ExampleClass3(BaseModel): name: Literal\["ExampleClass3"\] \= "ExampleClass3" value: Literal\["3"\] \= "3" type: Literal\["string"\] \= "string" field: Literal\["option"\] \= "option" class ExampleModel(BaseModel): field: Literal\["dropdownlist"\] \= "dropdownlist" value: Union\[ExampleClass1, ExampleClass2, ExampleClass3\] class Config:     schema\_extra \= {     "target": "value"     } |
| :---- |

*Kod24.* 

**2.11.7. Class İsimleri Kullanımı**

Bütün Classların baş harfleri büyük harf ile başlamalıdır.

# **2.11.8. Grup Kullanımı**

Belirli form öğeleri gruplandırma ve Sekmeli yapıda gösterilmesi istenildiği durumlarda 'group' anahtar kelimesi ile bir özellik eklenmelidir. Eğer herhangi bir sekmeye dahil edilmek istenmiyor ise; ya group parametresinin value değeri 'default' olmalıdır veya group parametresi eklenmemelidir. Aşağıdaki örnekte ExampleModel1 ve ExampleModel2 parametreleri ExampleGroup1 sekmesinde gösterilecektir. ExampleModel3 ve ExampleModel4 parametreleri ExampleGroup2 sekmesinde gösterilecektir. ExampleModel5 parametresi herhangi bir sekmede gösterilmeyecektir, ana yapıda gösterilecektir.

| class ExampleModel1(BaseModel): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup1"\] \= "ExampleGroup1" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel2(BaseModel): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup1"\] \= "ExampleGroup1" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel3(BaseModel): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup2"\] \= "ExampleGroup2" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel4(BaseModel): name: Literal\["Example"\] \= "Example" group: Literal\["ExampleGroup2"\] \= "ExampleGroup2" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist"class ExampleModel5(BaseModel): name: Literal\["Example"\] \= "Example" value: str type: Literal\["string"\] \= "string" field: Literal\["dropdownlist"\] \= "dropdownlist" |
| :---- |

*Kod25.* 

[image1]: <data:image/png;base64,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>

[image2]: <data:image/png;base64,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>

[image3]: <data:image/png;base64,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>