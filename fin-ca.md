컴퓨터 구조에서는 Pipeline, Memory Hierarchy 내용을 다룬다.
개요에서 등장하는 ISA, Microarchitecture와 같은 개념을 물어볼 수도 있다.

# Single cycle
clock의 rising edge에서 업데이트가 한번에 일어난다

# Multi cycle

## 장점
- 명령어마다 실행시간이 각각 다른 것을 해결할 수 있다.
  - 길게 걸리는 명령에 clock cycle을 많이 할당
- 하드웨어 리소스 공유가 가능 (Reusing)
  - 하나의 연산기를 여러 시간에 나눠서 쓸 수 있음
  - instruction memory, data memory를 같이 쓸 수 있음

## 단점
- 제어 신호가 복잡해짐
  - 단순 조합회로로 만들 수 없음 --> finite state machine
  - 회로의 current state를 함께 저장해야하는 구조
- 이전 클럭 사이클에서 실행한 결과를 이어받기 위한 레지스터가 더 필요
  - ALUSrcA / ALUSrcB 가 추가 (ALU가 뭘 계산할 지 결정)
  - PCWrite 추가 (싱글일 때는 매 클락마다 PC를 업데이트하지만 지금은 5사이클에 한번 씩 업데이트해야해서)
  - IRWrite 추가 (위와 마찬가지)
- 추가적인 mux도 필요

# Pipeline

-   파이프라인 구조 설계 시 주의해야할 요소들?
-   각 요소들이 제대로 다뤄지지 않았을 경우 생길 수 있는 문제점들과 해결책
-   파이프라인 구현을 어렵게하는 3가지 hazard를 설명하고 각각을 어떻게 해결하는 지?
-   branch prediction와 forwarding 유닛이 없을 때와 있을 때, 주어진 instrucion들을 수행하는데 걸리는 cycle을 계산하는 문제

## Pipeline in MIPS

파이프라인은 latency는 좀 떨어질 수 있지만, throughput은 훨씬 커짐

MIPS의 경우, RISC ISA의 특징을 잘 따르고 있기에 1)모든 instruction 크기가 동일하고 2)instruction format도 몇 개 안되어서 실행 시간을 일정하게 통일시킬 수 있다.

파이프라인 하기 좋은 구조

### Pipeline Datapath

각각의 스텝을 명확하게 구분 --> pipeline 사이에 register 필요!!
IF/ID   ID/EX   EX/MEM    MEM/WB

### Controller
ID 단에서 이후 스텝에서 사용할 제어신호를 한꺼번에 생성한다.
그러고서 파이프라인을 따라가면서 reigster에 계속 태워서 보낸다. (컨베이어 벨트)

## 파이프라인 구현을 어렵게하는 3가지 hazard

### Structure Hazard
resource를 2개 이상의 instruction이 동시에 요구하게 될 때 발생

1. Stall
2. Memory 영역을 instrucion / data로 분리

### Data Hazard
- 서로 다른 명령어 간의 디펜던시가 있는 경우
- data를 두 instrucion이 read/write하려 할 때 발생

#### 1. Stall

이전 명령의 결과가 레지스터에 입력될 때까지 stall

#### 2. Fowarding

레지스터 업데이트 시점은 WB 이지만, EX단만 거치면 나중에 뭐가 들어갈 지는 알 수 있다

EX에서 나온 결과를 다음 EX의 입력으로 받자 --> 단, 그에 따른 mux 추가

하지만 lw와 디펜던시가 있는 경우, MEM까지 가줘야 값을 알 수 있다.
이 때는 1번의 stall이 필요해 (한클락 낭비ㅠ)
MEM에서 나온 결과를 다음 EX의 입력으로 받자

#### 3. Compiler Scheduling

- nop 인스트럭션을 의존 관계가 있는 두 인스트럭션 사이에 추가 (2개)
- 또는 nop 삽입 대신 명령어에 디펜던시가 없는 명령어가 들어가도록 수정

똑똑한 어셈블러나 컴파일러가 필요

### Control Hazard
- 파이프라인은 명령이 순차적으로 실행될 때를 가정하여 fetch를 미리미리 함
- 점프명령, beq 명령은 명령의 순서를 바꿈 --> 파이프라이닝을 깨지게 함

#### 1. Stall

branch가 어디로 될 지 여부는 MEM 단에서 결정됨
MEM이 실행될 때 까지 3 클락을 stall --> 3클락의 손해

15% branch frequency: CPIP = 1 + 0.15*3 = 1.45

#### 2. Optimized branch processing

branch 발생 여부 확인을 최대한 앞 stage로 끌고오자 --> ID로!
그럼 버리는 클락이 1개만 발생함

#### 3. Branch prediction

**Static prediction**: 항상 브랜치가 발생하지 않는다고 예측한다!

예측이 잘못된 경우에만, IF단에 들어온 명령어를 무효화시킨다! --> bubble(nop)

**Dynamic prediction**: 브랜치가 발생한 경우를 예측하는 방법을 이전 예측상황이 맞았는지 여부에 따라 바꾸자

#### 4. Delayed Branch
2번 구조에서 hazard detection 처리를 해줘야 함  
(2번에서는 hazard detector가 추가되어서 IF/ID 레지스터를 비워줬음)

- 대신, 컴파일러에서 nop를 beq 다음에 무조건 삽입해주자!
- 또는, nop 대신 유용한 명령을 껴주자

```
**상황문제**

1단계: IF-ID-EXEC
2단계: MEM
3단계: WB

파이프라인에 관한 질문이었는데 파이프라인이 위와 같이 주어졌을 때, Data hazard가 존재하는가?
답은 존재한다고 했고 IF-ID의 target/source register의 데이터가 MEM-WB의 레지스터의 데이터와 동일할 경우 data hazard가 발생한다고 했습니다.

다음 질문으로는 Control hazard가 존재하는가? 였는데 이에 대한 답은 존재하지 않는다 였습니다. 브랜치 콘트롤은 EXEC 단계에서 이미 계산이 되어 브랜치 결정을 할 때 넘길 수 있기 때문입니다.

마지막 질문은 한 컴퓨터 구조에서 TLB를 없앴는데 이러한 결정을 하게 된 결정적인 이유에 대해서 대답하는 것이었습니다. 저는 시간적 지역성을 얘기하며 가장 최근에 접근한 데이터가 다시 쓰일 일이 드물어 TLB에 사상해둘 필요가 없기 때문이라고 대답했습니다.
```

# Memory hierarchy

- Memory Hierarchy: 메모리의 크기, 접근속도 등을 고려해서 계층을 정함
- Locality
  - Temporal Locality: 최근에 사용한 data는 그 다음에도 access할 가능성이 큼
  - Spatial Locality: 최근에 사용한 data 근처의 data도 access할 가능성이 큼

## Cache

### Tag and valid bit

**issue**  
하나의 캐시 주소와 맵핑될 수 있는 memory 주소가 많다!\
memory의 어떤 block이 cache에 저장되었는 지 어떻게 알아?\
--> Tag (cache에 data와 함께 block address를 저장)

**issue**  
cache의 data가 useful data인 지 어떻게 알아?\
--> Valid bit

```
1 word => 4 byte => 32 bit
cache가 1024 word를 가짐 --> index가 1024개 --> 10bit
Tag size: 32(all) - 10(index) - 2(word offset) = 20bit
20(tag) + 1(valid) + 32(word) = 53bit
Cache size: 1024 * 53
```

### Write Policy

Cache에 data를 write한 경우, main memory에는 어떻게 업데이트 할 것이냐?

### write-through
write될 때마다 memory update

- 문제: write할 때, cache도 업데이트하고 memory도 업데이트 해야해 --> 오래걸린다
- write buffer를 사용!
- cache에도 쓰고 memory에도 쓰고가 아니라
- cache에도 쓰고 memory에 쓸 write buffer에 집어넣고 cpu는 다음동작으로 넘어가

### write-back
write될 때 **dirty bit**에 1을 주고, block이 cache에서 나올 때 memory update

## Cache Performance

### Block size?
cache는 locality를 활용함

word 단위로 데이터를 가져오게 된다면 temporal locality 활용!
근데 spatial locality는?!

--> Block 단위로 cache를 가져오자!

> Q. 과연 4개를 다 가져오는게 이득이냐? Miss 나면..?  
> A. 이득임. 1개 word 가져오는 시간과 4개 word 가져오는 시간이 그래 차이 안남 (인접한거 읽어오면 가속효과)

### Three placement policies

```
Q. N-way Set Associative Cache의 구성 및 동작 방식을 설명하시오
Q. N-way Set Associative Cache의 성능에 영향을 미치는 인자 3가지? 어떤 영향?
Q. 64KiB의 4-way Set Associative Cache가 있고, 캐쉬 블럭이 16바이트, Physical Address로 32비트를 사용한다고 할 때 Cache Tag는 몇 비트인가? 18bit!

Q. cpu cache memory의 성능을 높이기 위한 기법 3개 이상 (?)
Q. 각 기법이 hit time, miss rate, miss penalty에 어떤 영향?
```

#### 1. Direct Mapped Cache

특정 메모리 주소를 특정 캐시 주소에 할당

direct mapped cache에서 캐시 주소에 이미 데이터가 존재할 때
다른 빈 곳이 있음에도 victimize 해야하는 문제가 발생

#### 2. Fully Associative

cache entry가 빈 곳을 찾아서 맵핑시키는 방법 (tag가 곧 주소가 되는!)
한 번 찾을 때 모든 entry를 비교해야하는 오버헤드가 발생하고 비쌈

#### 3. N-way Set Associative

절충안 --> mapping 할 수 있는 address를 n개 준다

### Replacement Policy

fully, set associative에서 슬롯에 데이터가 다 차있을 때!

#### 1. Random

#### 2. FIFO
- 가장 오래된 것을 내보낸다
- timestamp가 필요 (처음 들어온 시간)
- but.. 가장 오래됐다는 거는 가장 많이 쓴다는 뜻일수도?

#### 3. LRU
- Least Recently Used
- 가장 오래 쓰지 않은 것을 내보낸다
- timestamp가 필요 (얘는 access 할 때마다 업데이트 되어야 함)
- timestamp 업데이트하는 데에 오버헤드가 있음
- 얘가 보통 많이 쓰임

#### 4. LFU
- Least Frequently Used
- 가장 빈번히 사용되지 않은 애를 내보낸다
- counter 필요
- 가장 최근에 들어온 애가 쫓겨나는 문제가 있음

### Multi-level cache

```
Q. average memory access를 결정하는 3가지 factor? multi-level cpu cache가 이 3가지 측면에서 어떤 장점이 있는 지?
```
Miss penalty를 줄이기 위함이 목적!
L1 cache
L2 cache

### 성능 계산

- CPI = 1, clock rate = 4GHz
- L1 캐시 miss rate = 2% + main memory까지 100ns
- L2 캐시 miss rate = 0.5% + L2 캐시까지 5ns
- 100ns / 0.25ns/cycle --> 400 clock cycle
- 5ns --> 20 clock cycle

얼마나 빨라지나요?
- L1만 있을 때 CPI = 1 + 0.02x400 = 9
- L2도 있을 때 CPI = 1 + 0.02x20 + 0.005x400 = 3.4


## Virtual Memory

- virtual address: 프로세스의 메모리 주소공간에 접근하기 위한 주소
- physical address: 하드웨어가 물리 메모리에 접근하기 위한 주소

- 4G 논리메모리: (page, offset) 32bit = 20bit + 12bit
- 1G 물리메모리: (frame, offset) 30bit = 18bit + 12bit

page --> frame 맵핑!

### Page fault
page fault가 발생하면 매우 오래걸림 --> page fault를 줄이자!!

캐시미스는 하드웨어에서 처리하지만, 페이지폴트는 OS에서 소프트웨어적으로 처리한다  
(자주일어나지 않고 처리할 때 좀 더 복잡해서)

write through는 매우 비싸서 write back을 사용함 (디스크 엑세스는 가급적 피하도록)

### Page table
page number가 인덱스가 됨 --> 2^20KB = 4MB나되네?

page table도 메인 메모리에 있다!

**PTBR** (page table register)  
얘는 메인메모리에서의 물리 주소를 갖고 있는 레지스터

PTBR + page number로 메모리에서 인덱스를 찾아감

### Page table entries

- Reference bit
  - 어떤 시간 간격에 reference 했으면 1, 시간이 지나면 0이 됨
  - page 교체 정책에서 대략적인 LRU를 판단하기 위함
- Dirty bit
  - 해당하는 페이지가 메인메모리에 올라온 이후로 수정되었는 지 여부
- Valid bit
  - 1이면 main memory, 0이면 disk storage에 있다

## TLB
Address Translation을 위한 Cache (page table cache)

최근에 접근하던 page는 대부분 TLB에서 hit가 발생한다 --> locality!!

### TLB entries

TLB cache는 fully associative 구조를 갖는다

page table entry와 마찬가지로 reference bit, dirty bit, valid bit를 가짐


## TLB + Cache + Virtual Memory

```
page fault, data cache miss, tlb miss 가 동시에 발생할 수 있는가? 있다면 발생 순서대로 설명해보라.
1. Virtual Address를 Physical Address로 변환하는 과정에서 TLB Miss 발생 가능
2. 변환된 Physical Address를 참조할 때 캐쉬에 없는 경우 Cache Miss 발생 가능
3. 캐쉬에 데이터를 로드하기 위해 메모리를 참조하는 과정에서 Page Fault 발생 가능
```

TLB Miss
- page가 메모리에 있는 경우, TLB 엔트리를 업데이트
- page가 메모리에 없는 경우, OS에서 page fault를 처리하도록 하게 하자

Page Fault
- page fault가 발생하면 명령어의 진행을 정지시키고 page fault가 난 위치를 기억시켜서 withdraw
- OS의 page fault를 해결하기 위한 명령어를 실행
- 실행 후에 아까의 명령을 다시 재실행

Page Fault by OS
1. page table의 도움을 받아서 디스크의 page 위치를 찾는다
2. page를 메인메모리의 어디에 넣을 지 정해야 함 (페이지 교체정책)
3. 있던 놈을 뺄 때, dirty bit가 채워져 있으면 write back
4. 디스크의 page를 메모리에 읽어온다
5. page fault가 발생한 명령부터 다시 실행

### Context switching과 관련해서

P1 --> P2로 context switching이 발생할 때, TLB를 그냥 두면 안된다! (page protection...!)

어떻게 할거냐?

1. TLB의 모든 엔트리를 invalid 시키자
: 단순하지만 비싸
: P1 --> P2 --> P1 금방 다시 돌아와도 entry가 다 invalid

2. TLB에 pid를 추가하자
: 기존에 가상주소 + 물리주소 로 구성되어있던 TLB 엔트리
: pid + 가상주소 + 물리주소로 구성하고 `pid + 가상주소`를 태그로 사용하자
: 하드웨어 변경이 필요

### Memory Protection
PTE에 해당 가상 페이지에 대한 접근 권한 정보를 추가해주면 프로세스별로 각 가상 페이지에 대한 접근을 통제하는 것이 매우 쉬워진다

### Cache access time 줄이기

우리는 cache에서 주로 n-way set을 쓰기 때문에 offset만 가지고도 cache index를 찾을 수 있다!

기존에 순차적으로 하던 lookup을 병렬적으로 진행하자
- TLB lookup --> cache lookup --> hit/miss
- TLB lookup + cache lookup --> hit/miss

VIPT (virtually indexed physically tagged)

> 단, cache index size가 offset의 비트수를 넘어가는 경우에는 적용할 수 없음!

```
-   Cache의 Cold Miss의 개념은 무엇이고, Cold Miss를 줄이는 방법은 무엇인가?
    => 데이터를 첫 번째 참조할 때 발생하는 miss이며, 줄이는 방법은 없다.

-   Multi-Core 환경에서 Cache를 사용할 때 발생할 수 있는 문제점은 무엇인가?
    => L1 Cache는 보통 코어 내부에 포함되기 때문에 CPU Scheduling을 통해 서로 다른 코어에서 프로세스가 실행될 경우 Miss Rate이 올라갈 수 있음
```
