# SuperDuperTradingBot

## 목표
- 주식 연평균 수익률 10%
- 증권사 API와 연결해 자동 거래
- 임의의 시장에 적용할 수 있도록 제작(종준이가 하는 게임, 이름이 뭐였지)

## 무엇을 해야하는가
### PPO 알고리즘
Proximal Policy Optimization 알고리즘은 강화학습의 최신 알고리즘이다.
이거 구현하기만 해도 절반의 성공이라고 볼 수 있다.
이론은 어려울 수 있지만, 코드 짜는 것은 그보다 쉬워보인다. 와! \\(ㅇㅁㅇ)/

### 기사 요약 및 텍스트 벡터 변환
사실 CNN이라 종준이에게 맡겼지만, 이것이 아마 프로젝트의 가장 큰 난제로 보여진다.
주식 그래프에서 뽑아낸 참값을 이용해 학습해야 하지만, 주식 차트에는 기본적으로 노이즈가 껴있기 마련이다.
결국 방법은 2가지다. 데이터를 어마만치하게 때려박거나, 아니면 코드를 엄청 잘 짜던가. 오~

추후 작성함 ~~