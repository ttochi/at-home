# Pipeline

마이크로프로세스..?

## Overview

**주목적** CPU 성능 향상
한 번에 여러 개의 명령을 동시에 CPU에서 실행시키겠다!

### MIPS에 적용

1. instruction fetch && PC+4
2. instruction decode and register fetch && PC+(imm16<<2)
3. execution (R-type) / memory 주소 계산 (I-type) / PC update (BEQ)
4. write (R-type) / memory access (I-type)
5. write-back (lw)

1. IF
2. ID
3. EX
4. MEM
5. WB

5배의 speed up!!

multi cycle에서는 각 명령어의 latency가 가변이었던 반면,
pipeline은 모든 명령어가 5개 clock cycle latency를 갖도록 한다.

latency로는 멀티보다 안좋을 것 같지만
throughput 측면으로는 훨씬 성능 굳

### Pipeline하기 좋은 조건

1. 모든 instruction의 길이가 32비트로 통일 --> 일정한 속도로 fetch 가능 --> IF 실행속도가 동일
2. instruction의 format이 몇 개 안됨 --> ID에 걸리는 시간도 일정한 편
3. memory access가 load, store로 국한되어있다 -->

RISC - 명령어가 규칙적이고 실행되는 시간이 예측가능
MIPS는 RISC의 특징을 잘 따르고 있기 때문에 pipeline하기 용이한 구조이다

### Pipeline하기 어려운 조건

1. structure hazard
: instruction 메모리 + data 메모리가 하나의 메모리로 구성되어있으면 파이프라이닝하기 어려움
: IF 단계에서 메모리에 계속 엑세스 + MEM 단계에서도 메모리에 계속 엑세스
: 메모리가 하나라면 IF에서 엑세스 하는 것과 MEM 단계에서 엑세스 하는 것이 충돌
--> 구조적인 해저드
--> 실제에선 둘로 쪼개서 쓴다

2. data hazard
: 서로 다른 명령어 간의 디펜던시가 있는 경우
: 어떤 명령을 실행하기 위해 이전 명령의 결과를 받아와야 하는 상황
: 이전 명령이 끝날 때 까지 기다려야하면 파이프라이닝 할 수 없음

3. control hazard
: 파이프라인은 명령이 순차적으로 실행될 때를 가정하여 fetch를 미리미리 함
: 점프명령, beq 명령은 명령의 순서를 바꿈 --> 파이프라이닝을 깨지게 함

이를 어떻게 극복할 것인가!

+ 마이크로프로세서에서는 exception handling과 out-of-order execution도 파이프라인을 방해하는 요인임


### 요약
- instruction을 여러 stage로 쪼갠다
- 동일한 시간동안 각 명령의 다른 step을 실행한다
- speedup은 가장 긴 파이프라인 스테이지에 의해 / 쪼개진 스테이지 수에 의해 결정된다
- 스테이지 수가 많을 수록 그에 비례해서 speedup

가장 이상적인 것: 동일한 사이즈로 가장 많이 쪼갠 것

* Single-cycle: Instuction per clock 높음 / Clock cycle time 느림
* Multi-cycle: Instuction per clock 낮음 / Clock cycle time 빠름
* Pipeline: Instuction per clock 높음 (throughput) / Clock cycle time 빠름

* Single-cycle: HW specialized / CPI=1
* Multi-cycle: HW shared / CPI=several
* Pipeline: HW specialized / CPI=several

-----------------------------

## Datapath

싱글사이클 Datapathㄹ

각각의 스텝에서 instruction이 섞이지 않도록 명확하게 stage를 구분해야 함
세탁기와 건조기 사이에 바구니가 필요 --> pipeline 사이에 register 필요!!

IF/ID   ID/EX   EX/MEM    MEM/WB

## Controller

파이프라인은 동시에 5개의 제어신호를 보내야 한다. 어떻게?
**컨베이어벨트 예제** 자동차 겉에다가 각 스텝에서 해야할 일들을 적어주고 컨베이어 벨트에 태운다

컨트롤 reigster는 IF/ID에서는 안필요

ID 단에서 이후 스텝에서 사용할 제어신호를 한꺼번에 생성한다.
그러고서 파이프라인을 따라가면서 reigster에 계속 태워서 보낸다.


-----------------------------

# Data Hazard
```
: 서로 다른 명령어 간의 디펜던시가 있는 경우
: 어떤 명령을 실행하기 위해 이전 명령의 결과를 받아와야 하는 상황
: 이전 명령이 끝날 때 까지 기다려야하면 파이프라이닝 할 수 없음
```

## 1. Freezing

이전 명령의 결과가 레지스터에 입력되기 전에 연산을 하려하면 안됨.
해저드를 없애는 법? --> 뒤에 따라오는 명령을 늦춘다!
명령이 더 이상 앞으로 나가지 못하도록 freeze!

+ PC도 업데이트 못하게 freeze

## 2. Fowarding

레지스터 업데이트 시점은 WB 이지만,
EX단만 거치면 나중에 뭐가 들어갈 지는 알 수 있다
EX에서 나온 결과를 다음 EX의 입력으로 받자
--> 단, 그거에 따른 mux가 추가되어야 한다

하지만 lw와 디펜던시가 있는 경우,
MEM까지 가줘야 값을 알 수 있다...
이 때는 1번의 stall이 필요해 (한클락 낭비ㅠ)
MEM에서 나온 결과를 다음 EX의 입력으로 받자

## 3. Compiler Scheduling

- nop 인스트럭션을 의존 관계가 있는 두 인스트럭션 사이에 추가 (2개)
- 또는 nop 삽입 대신 명령어에 디펜던시가 없는 명령어가 들어가도록 수정

똑똑한 어셈블러나 컴파일러가 필요


-----------------------------

# Control hazard
```
: 파이프라인은 명령이 순차적으로 실행될 때를 가정하여 fetch를 미리미리 함
: 점프명령, beq 명령은 명령의 순서를 바꿈 --> 파이프라이닝을 깨지게 함
```

1. stall
2. optimized branch processing: 1 클락 줄여주는 것
3. branch prediction: 얘가 브랜치될 앤지 추측
4. deplayed branch: nop 삽입

## 1. stall

branch가 어디로 될 지 여부는 MEM 단에서 결정됨
MEM이 실행될 때 까지 3 클락을 stall --> 3클락의 손해

15% branch frequency: CPIP = 1 + 0.15*3 = 1.45


## 2. optimized branch processing

- branch가 발생할 지??
- 한다면 어디로 가는 지??

위의 2개를 최대한 앞으로 땡기자! --> ID!

이렇게 땡길 수만 있다면 버리는 클락이 1개만 발생함

어떻게 땡기냐?
- 브랜치 계산용 ALU는 ID로 이동 가능
- rd, rt를 비교하기 위한 ALU는 앞으로 이동할 수 없어!
  --> 비교에 ALU를 쓰지 말고 비교기를 만들어서 ID 스텝에 넣자


## 3. branch prediction

이렇게 줄여놨는데 그마저도 손해 안보는 법!

항상 브랜치가 발생하지 않는다고 예측한다!
이 경우는 **Static prediction**

브랜치가 안일어나면 손해 X
예측이 잘못된 경우, IF단에 들어온 명령어를 무효화시킨다! --> bubble(nop)

예측이 잘못된 경우에만 한 클락 손해보겠다..

**Dynamic prediction**
브랜치가 발생한 경우를 예측하는 방법을 이전 예측상황이 맞았는지 여부에 따라 바꾸자


## 4. Delayed Branch

2번 optimized branch processing의 구조에서
hazard detection을 하드웨어에서 신경쓰지 않겠다!
(2번에서는 hazard detector가 추가되어서 IF/ID 레지스터를 비워줬음)

- 대신, 컴파일러에서 nop를 beq 다음에 무조건 삽입해주자!
- 또는, 한발 더 나아가서 유용한 명령을 껴주자 (branch가 되도 안되어도 어쨋든 수행되어야 하는 명령..?)

Delay slot에 어떤 유용한 명령을?
1. 브랜치 이전에 실행할 명령을 둔다
2. 브랜치 직후에 실행할 명령을 둔다 (먼소리야,,,)
3. 브랜치와 관계없는 멀리 있는 명령을 둔다..



# Structure Hazard
```
: instruction 메모리 + data 메모리가 하나의 메모리로 구성되어있으면 파이프라이닝하기 어려움
: IF 단계에서 메모리에 계속 엑세스 + MEM 단계에서도 메모리에 계속 엑세스
: 메모리가 하나라면 IF에서 엑세스 하는 것과 MEM 단계에서 엑세스 하는 것이 충돌
```
memory를 여러 개 사용하여 해결 (?!)
