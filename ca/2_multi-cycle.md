# multiple clock cycle

하나의 사이클에 모든 걸 끝내지말고 쪼개자
짧은거 여러개로 긴거 하나를 대체하자

## 장점
- 명령어마다 실행시간이 각각 다른 것을 해결할 수 있다.
: 길게 걸리는 명령에 clock cycle을 많이 할당

- 하드웨어 리소스 공유가 가능 (Reusing)
: 하나의 연산기를 여러 시간에 나눠서 쓸 수 있음
: instruction memory, data memory를 같이 쓸 수 있음

## 단점
- 제어 신호가 복잡해짐
: 시간 정보도 같이 있어야... 단순 조합회로로 만들 수 없음 --> finite state machine

- 이전 클럭 사이클에서 실행한 결과를 이어받기 위한 레지스터가 더 필요

- 추가적인 mux도 필요


## Data Path

instruction을 여러 step으로 나눈다 --> 각각의 스텝이 한 사이클

쪼갤 때 가능한 같은 크기로 자른다

- 메모리가 하나 (instruction + data)
- ALU가 하나
- 레지스터 추가


아래는 각 클락별로,,
1. 메모리에서 inst load
2. register read
3. 메모리 주소 계산
4. 메모리 읽어서 DR에 저장
5. DR에 있는 것을 register에 저장

## Controller

기존 컨트롤 신호보다
- ALUSrcA / ALUSrcB 가 추가 (ALU가 뭘 계산할 지 결정)
- PCWrite 추가 (싱글일 때는 매 클락마다 PC를 업데이트하지만 지금은 5사이클에 한번 씩 업데이트해야해서)
- IRWrite 추가 (위와 마찬가지)


**finite state machie**
회로의 current state를 함께 저장해야하는 구조 (Moore)
(참고) 3번째 클럭까지 가야 controll이 계산된다고 함


### 싱글사이클 대비

1. Single memory
2. Single ALU
3. Severall registers
4. Mux for memory, Mux for ALU


## 명령어 별 실행

1. instruction fetch && PC+4
2. instruction decode and register fetch && PC+(imm16<<2)
3. execution (R-type) / memory 주소 계산 (I-type) / PC update (BEQ)
4. write (R-type) / memory access (I-type)
5. write (lw)


## 예제

lw 10개
sw 10개
R타입 20개
branch 10개

싱글사이클타임: 90ns, 멀티사이클타임: 20ns 일 때 토탈 처리 시간은?

사이클 수? 50개 / 10x5 + 10x4 + 20x4 + 10x3 = 200개

50*90 = 4500
20*200 = 4000

==> 멀티플이 더 빠르다

참고) CPI? 1.0 / 200/50=4.0
