노트랑 같이보자...

# 1. Memory Hierarchy

- Memory Hierarchy: 메모리의 크기, 접근속도 등을 고려해서 계층을 정함
- Locality
  - Temporal Locality: 최근에 사용한 data는 그 다음에도 access할 가능성이 큼
  - Spatial Locality: 최근에 사용한 data 근처의 data도 access할 가능성이 큼

# 2. Basics of cache

## 2.1 Cache Mapping

이슈: cache 안에 access할 데이터가 존재하는가!

### 1. Direct Mapped Cache

특정 메모리 주소를 특정 캐시 주소에 할당

> xx001 주소를 가진 데이터는 001 캐시 주소에 할당한다 (mod 연산으로)

### 2. N-way Set Associative

direct mapped cache에서 캐시 주소에 이미 데이터가 존재할 때
다른 빈 곳이 있음에도 victimize 해야하는 문제가 발생

--> mapping 할 수 있는 address를 n개 준다

### 3. Fully Associative

cache entry가 빈 곳을 찾아서 맵핑시키는 방법
한 번 찾을 때 모든 entry를 비교해야하는 오버헤드가 발생

**issue**
하나의 캐시 주소와 맵핑될 수 있는 memory 주소가 많다!
memory의 어떤 block이 cache에 저장되었는 지 어떻게 알아?
--> Tag (cache에 data와 함께 block address를 저장)

**issue**
cache의 data가 useful data인 지 어떻게 알아?
--> Valid bit

## 2.2 계산

1 word => 4 byte => 32 bit
address: 32bit

cache가 1024 word를 가짐 --> index가 1024개 --> 10bit

Tag size: 32(all) - 10(index) - 2(word offset) = 20bit

20(tag) + 1(valid) + 32(word) = 53bit
Cache size: 1024 * 53


## 2.3 Write Policy

Cache에 data를 write한 경우, main memory에는 어떻게 업데이트 할 것이냐?

### write-through
write될 때마다 memory update

- 문제: write할 때, cache도 업데이트하고 memory도 업데이트 해야해 --> 오래걸린다
- write buffer를 사용!
- cache에도 쓰고 memory에도 쓰고가 아니라
- cache에도 쓰고 memory에 쓸 write buffer에 집어넣고 cpu는 다음동작으로 넘어가

### write-back
write될 때 **dirty bit**에 1을 주고, block이 cache에서 나올 때 memory update


### Write Miss일 때?

write할 data가 cache에 없다면?

- fetch: 해당 블록을 memory 차원에서 update하고 cache에 allocate
- don't fetch: memory update만 하고 cache에 가져오지 말자 (쓰고 다시 안부르는 경우 많아서)

> write-back일 때는 보통 fetch


# 3. Cache Performance
- Block size
- Three placement policies
- replacement algorithm
- multi-level cache

## 3.1 Block Size

cache는 locality를 활용함

word 단위로 데이터를 가져오게 된다면 temporal locality 활용!
근데 spatial locality는?!

--> Block 단위로 cache를 가져오자!

> Q. 과연 4개를 다 가져오는게 이득이냐? Miss 나면..?
> A. 이득임. 1개 word 가져오는 시간과 4개 word 가져오는 시간이 그래 차이 안남 (인접한거 읽어오면 가속효과)

### Block의 장점
1. spatial locality 활용
2. 4개 word가 동일한 tag, valid data를 공유함


### 블락사이즈와 miss ratio, miss penalty 관계

Block이 커지면
- miss ration는 줄어들고
- miss penalty는 커지고

하지만 block 사이즈가 특정 사이즈를 넘어가게 되면 miss ratio는 올라간다
- 블락 갯수가 적어짐
- 블락 안에서의 spatial locality가 줄어듬
- miss penalty가 커짐

### 성능 계산

- I-cache miss rate = 2%
- D-cache miss rate = 4%
- Miss penalty = 100 cycle
- base CPI = 2 cycle
- Load & store 비율 = 36%

miss CPI for I-cache = 0.02 * 100 = 2 cycle
miss CPI for D-cache = 0.36 * 0.04 * 100 = 1.44 cycle
actual CPI = 2 + 2 + 1.44 = 5.44

cache miss가 아예 발생하지 않은 상황 대비 2.72배로 느림


## 3.2 Three placement policies

### 1. Direct Mapped Cache

특정 메모리 주소를 특정 캐시 주소에 할당

direct mapped cache에서 캐시 주소에 이미 데이터가 존재할 때
다른 빈 곳이 있음에도 victimize 해야하는 문제가 발생

### 2. Fully Associative

cache entry가 빈 곳을 찾아서 맵핑시키는 방법 (tag가 곧 주소가 되는!)
한 번 찾을 때 모든 entry를 비교해야하는 오버헤드가 발생하고 비쌈

### 3. N-way Set Associative

절충안!

--> mapping 할 수 있는 address를 n개 준다


## 3.3 Replacement Policy

fully, set associative에서 슬롯에 데이터가 다 차있을 때!

1. Random

2. FIFO
- 가장 오래된 것을 내보낸다
- timestamp가 필요 (처음 들어온 시간)
- but.. 가장 오래됐다는 거는 가장 많이 쓴다는 뜻일수도?

3. LRU
- Least Recently Used
- 가장 오래 쓰지 않은 것을 내보낸다
- timestamp가 필요 (얘는 access 할 때마다 업데이트 되어야 함)
- timestamp 업데이트하는 데에 오버헤드가 있음
- 얘가 보통 많이 쓰임

4. LFU
- Least Frequently Used
- 가장 빈번히 사용되지 않은 애를 내보낸다
- counter 필요
- 가장 최근에 들어온 애가 쫓겨나는 문제가 있음


## 3.4 Multi-level cache

Miss penalty를 줄이기 위함이 목적!
L1 cache
L2 cache

### 성능 계산

CPI = 1, clock rate = 4GHz
L1 캐시 miss rate = 2% + main memory까지 100ns
L2 캐시 miss rate = 0.5% + L2 캐시까지 5ns

얼마나 빨라지나요?

100ns / 0.25ns/cycle --> 400 clock cycle
5ns --> 20 clock cycle

L1만 있을 때 CPI = 1 + 0.02x400 = 9
L2도 있을 때 CPI = 1 + 0.02x20 + 0.005x400 = 3.4



# 4. Virtual Memory
- Virtual memory general
- Page table
- TLB


## 4.1 Virtual memory

- 상위 레벨의 스피드와 하위 레벨의 사이즈의 이점을 다 챙겨가자
- 메모리를 공유하는 프로세스 간의 memory protection
- 각 프로세스가 자신만의 메모리를 쓰는 것 처럼 하자 (logical memory)

- virtual address: 프로세스의 메모리 주소공간에 접근하기 위한 주소
- physical address: 하드웨어가 물리 메모리에 접근하기 위한 주소

32비트 메모리 주소 --> 4GB의 메모리를 가지고 놀 수 있다
하지만 실제 메모리는 1GB 언더일 수도?
"가상메모리" 개념을 통해 프로세스 각각이 메모리를 가질 수 있도록 한다 --> 멀티프로그래밍 시스템


메인메모리는 하드디스크의 캐시같이 동작
가상주소 미스가 발생한다면? (page fault)
OS에서 소프트웨어적으로 핸들링한다 --> 하드디스크에서 페이지 찾아서 메인메모리에서 페이지 교체하고 page table update


## 4.2 Page Table

(page, offset) 32bit = 20bit + 12bit
(frame, offset) 30bit = 18bit + 12bit

page --> frame 맵핑!

#### Page fault
page fault가 발생하면 매우 오래걸림 --> page fault를 줄이자!!
비싸더라도 miss fanalty가 너무 큼 --> LRU 알고리즘을 권장

캐시미스는 하드웨어에서 처리하지만, 페이지폴트는 소프트웨어적으로 처리한다 (자주일어나지 않고 처리할 때 좀 더 복잡해서)

write through는 매우 비쌈!
write back을 사용함 (디스크 엑세스는 가급적 피하도록)


> Segmentation
세그먼트 길이는 가변적임 but protection을 더 정교하게 함

#### Page table

page number가 인덱스가 됨

page table도 메인 메모리에 있다!
PTBR (page table register) 얘는 메인메모리에서의 물리 주소를 갖고 있는 레지스터

PTBR + page number로 메모리에서 인덱스를 찾아감

#### Page table entries

- Reference bit
: 어떤 시간 간격에 reference 했으면 1, 시간이 지나면 0이 됨
: page 교체 정책에서 대략적인 LRU를 판단하기 위함

- Dirty bit
: 해당하는 페이지가 메인메모리에 올라온 이후로 수정되었는 지 여부

- Valid bit
: 1이면 main memory, 0이면 disk storage에 있다


## 4.3 TLB

#### Cache에 저장되는 주소는 가상주소일까 물리주소일까?

가상주소면 좋을텐데!
page table이 메인메모리에 있어서 가상주소를 물리주소로 변환하고 cache에 접근하면 비용이 많이 들거니까
cache를 쓰는게 메인메모리를 안쓰기 위함인걸

근데 그렇게 쓰면 안된다!
2개의 서로 다른 가상주소가 같은 물리주소를 가리키는 경우!
읽기면 상관없지만 쓰기를 하면 문제가 됨! (캐시에 써놓고 엎어쓸 때)

즉 물리주소를 써야 한다.
Address Translation이 Cache보다 앞에 들어가야 한다
그럼... 메인메모리 접근을 해야하는건가?!


#### TLB

Address Translation을 위한 Cache (page table cache)

최근에 접근하던 page는 대부분 TLB에서 hit가 발생한다 --> 얘도 locality 때문에 가능하다~

최악: TLB miss --> page fault
- disk의 데이터를 physical memory에 카피
- 페이지테이블 업데이트하고
- TLB에 업데이트하고


#### TLB Entry Structure

TLB cache는 fully associative 구조를 갖는다
page table entry와 마찬가지로 reference bit, dirty bit, valid bit를 가짐



# 5. Cache + Virtual Memory

Cache + TLB + virtual memory

위 3개 시스템에서의 hit와 miss에 대해서...

> TLB hit + memory miss 는 있을 수 없다!
> cache hit + memory miss 는 있을 수 없다!
> 메모리 계층에서 윗쪽에 있는 것은 반드시 아래에 있다!

셋다 miss면 page fault

### Handling TLB miss and page fault

TLB Miss
- page가 메모리에 있는 경우, TLB 엔트리를 업데이트
- page가 메모리에 없는 경우, OS에서 page fault를 처리하도록 하게 하자

Page Fault
- page fault 는 주로 pipeline의 MEM 단계에서 발생할 것
- page fault가 발생하면 WB 단계로 제어가 넘어가지 못하도록 만들어야 함
- 명령어의 진행을 정지시키고 page fault가 난 위치를 기억시켜서 withdraw
- OS의 page fault를 해결하기 위한 명령어를 실행
- 실행 후에 아까의 명령을 다시 재실행

Page Fault by OS
1. page table의 도움을 받아서 디스크의 page 위치를 찾는다
2. page를 메인메모리의 어디에 넣을 지 정해야 함 (페이지 교체정책)
3. 있던 놈을 뺄 때, dirty bit가 채워져 있으면 write back
4. 디스크의 page를 메모리에 읽어온다
5. page fault가 발생한 명령부터 다시 실행


### TLB Miss가 났을 때 실제로 일어나는 일

1. 하드웨어가 처리하는 경우
- TLB miss일 때, MMU 안의 하드웨어가 page table에 접근
- page table entry가 유효하면 TLB를 채움 (프로세서가 모르게!)
- 유효하지 않으면 page fault가 발생 --> OS에 제어권을 넘겨서 처리

2. 소프트웨어가 처리하는 경우
- TLB miss일 때, 프로세서는 TLB fault를 받고 커널이 page table을 찾으러 감
- page table entry가 유효하면 TLB를 채움
- 유효하지 않으면 내부적으로 page fault를 핸들링

==> 하는 일은 똑같은데 하드웨어로 할 때는 프로세서가 모르게...
==> 현대의 대부분의 칩셋들은 하드웨어로 처리 (소프트웨어가 더 오래걸림)


### Context switching과 관련해서

P1 --> P2로 context switching이 발생할 때, TLB를 그냥 두면 안된다! (page protection...!)

어떻게 할거냐?

1. TLB의 모든 엔트리를 invalid 시키자
: 단순하지만 비싸
: P1 --> P2 --> P1 이면..? 금방 다시 돌아와서 내 TLB가 맞는데도 invalid

2. TLB에 pid를 추가하자
: 기존에 가상주소 + 물리주소 로 구성되어있던 TLB 엔트리..
: pid + 가상주소 + 물리주소로 구성하고 `pid + 가상주소`를 태그로 사용하자
: 하드웨어 변경이 필요...


### 왜 virtual memory가 protection에 용이한지

권한제어...
A 프로세스는 read, write 가능하다
B 프로세스는 read만 가능하다....

access 정보를 추가해서 가상 메모리 공간을 공유하기도 하고, 접근권한도 관리할 수 있다.

### two-level page table

page table이 너무 클 때, 멀티 레벨을 사용하게 되면 메모리를 덜 쓸 수 있다

### cache access time 줄이기

cpu에서 cache에 접근할 때, 중간에 address translation이 들어감

스텝이 늘어나면 시간이 드는데 이 시간을 아껴보자!

virtual ( page, offset ) --> physical ( frame, offset )

우리는 cache에서 주로 n-way set을 쓰기 때문에 offset만 가지고도 cache index를 찾을 수 있다!

기존에 순차적으로 하던 lookup을 병렬적으로 진행하자
- TLB lookup --> cache lookup --> hit/miss
- TLB lookup + cache lookup --> hit/miss


VIPT (virtually indexed physically tagged)

> 단, cache index size가 offset의 비트수를 넘어가는 경우에는 적용할 수 없음!
> offset을 넘어가면 결국 physical 주소를 알아야 인덱싱이 가능하기 때문이지
