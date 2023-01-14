# 프로토콜 사양

## 개요

- MetaArtGallery 에서 받은 Image 를 ML 을 거친 후, 사용자에게 전송하기 위한 Deep-Learning 처리 Server 개발합니다.
- Python의 Flask API를 활용해 REST 기반으로 구축해서, 손쉽게 사용할 수 있도록 범용성을 높였습니다.


## Intro

이 파트에서는 Client 기준으로 Client → Server 로 보내는 명령을 기준으로 정리할 예정입니다.

아래 Code 표시는 python 을 기준으로 설명하는 것이며, REST API를 사용하기 위해 request 패키지를 사용할겁니다.

예시 코드는 아래와 같습니다. 앞으로 파트 설명 후 코드 블럭을 통해 Client → Server 의 예시 코드를 설명드리겠습니다.

```python
import request
META_ART_SERVER = '127.0.0.1:5000'
```

## 서버 상태 체크

서버 상태를 확인하기 위해 “/health” 를 GET으로 가져옵니다. 정상적으로 서버가 켜져있다면 health 라는 문구가 나옵니다.

```python
res = request.get(META_ART_SERVER + '/health')
print(f'>> {res.contents}')
```

```bash
>> b'health'
```

## Image Transfer

서버의 HDD 에 저장되어있는 Image들을 GET으로 가져옵니다. 가져올 수 있는 방법은 크게 두 가지가 있습니다.

- ”/images/<int:num>”
    - 전체 Resource 들 중에서 random 하게 특정 갯수만큼 가져옴
- “/images/<string:section>/<int:num>”
    - 해당 Section 의 이미지를 random 하게 특정 갯수만큼 가져옴

```python
res = request.get(META_ART_SERVER + '/health/20')
data = res.contents
```

POST에 대한 결과로 base64 로 encoding 된 string 이 나오게 됩니다. 이를 실제 Image로 만들기 위해서는 적절한 decode 과정을 거쳐야 합니다. 따라서 decoder 는 아래와 같이 구현할 수 있습니다.

```python
res = []
for i, img_encode in enumerate(data):
	print(f'=> Receive({i}) : {img_encode}')
	res.append(Image.open(BytesIO(base64.b64decode(img_encode))))
return res
```

앞으로 Modeling 의 결과로 Image 가 나올 경우, 위 Decode 함수를 사용해서 Image 로 변환하면 됩니다.

## DALLE

Dalle 모델을 사용하기 위해 “/dalle” 에 json 을 POST를 합니다. 사용하는 Data는 다음과 같습니다.

- text : 우리가 그림으로 변환시키길 원하는 text
- num_image : 요청하는 그림 수

Image 를 주고 받는 방식은 위의 Image Transfer에서의 설명과 동일합니다.

```python
input_ = {'num_images': 5, 'text': 'Smile woman'}
res = request.post(META_ART_SERVER + '/dalle', json=input_)
```