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
