내가 배운 지식들을 어떻게 잘 조합해서 말하냐!!
내가 아는 범위에서 잘 조합해서 말할 것!!

크게 CPU (프로세스), 메모리 (가상 메모리), 디스크 (파일 시스템) 파트로 나뉜다.
기출에 의하면 프로세스와 메모리 중심으로 면접이 이루어지는 것으로 보인다.
출처: https://hello-cruiser.tistory.com/entry/4-운영체제-기출-핵심-응용 [크루저의 쉼터:티스토리]

---

# 1. Overview

```
Q. 컴퓨터가 켜지기 전, memory에는 어떠한 data도 들어있지 않은 상태이다.
컴퓨터를 켜게 되면, 어떠한 과정을 거쳐서 우리가 컴퓨터를 사용할 수 있는 상태가 되는가?
System call이나 interrupt가 발생 시 어떻게 처리를 할 수 있게 되는지를 설명하면 됩니다.
=> NVM 하드에 저장되어있는 부팅 프로그램을 메모리에 최초 로드 --> 부트로더는 OS를 메모리에 로딩
=> 프로세스 context에 커널 코드가 가상적으로 추가되어, system call이나 interrupt 발생 시 유저모드, 커널모드 스위칭을 가볍게 할 수 있다.
```

## 1.1 멀티프로세싱? 멀티프로그래밍?

```
Q. 멀티프로그래밍의 정의와 그 이점?
Q. 멀티코어 등장에 따라 아래 기능들에 대해 운영체제가 어떤 기능이 바뀌어야 하는 지? 지금 그대로 이용해도 좋은 지?
  1) interrupt handling
  2) Scheduling data structure PCB, queue, etc.)
  3) Caching policy
  4) File system
```

1. CPU: instruction을 실행하는 하드웨어
2. Processor: 하나 이상의 CPU를 포함하는 칩 (걍 CPU로 보자)
3. Core: CPU의 컴퓨팅 유닛
4. 멀티코어: 하나의 CPU에 여러 컴퓨팅 코어가 포함된 것
5. 멀티프로세싱: 여러 CPU 프로세서가 협력적으로 일하는 것
6. 멀티프로그래밍: 동일한 시간에 여러 프로그램을 돌리는 것
7. 멀티태스킹
8. 멀티쓰레딩

**Concurrency**
CPU 자원을 효율적으로 사용하고, 사용자에 대한 응답 시간을 줄이는 목적

1. 멀티프로그래밍: 동시에 여러 개의 프로그램을 메모리에 상주하여 실행
2. 멀티프로세싱: 여러 개의 CPU Core에서 여러 명령어를 여러 Core에서 동시에 실행하는 것
3. 시분할(time-sharing): 여러 개의 프로세스가 하나의 CPU를 시간상으로 분할하여 사용하는 것

---

# 2. Process and Thread

- Process
  - 프로세스 주소공간
  - Process State
  - Process Switching
- IPC
- Thread
  - Process vs Thread
  - Multi-threading
  - Threading Issue

## 2.1 Process

```
Q. 프로세스가 IO 작업으로 대기할 때는 어떤 프로세스 상태(process state)를 가지는가? 작업이 완료된 후에는 어떤 프로세스 상태를 가지는가?
Q. 프로세스 상태가 running에서 ready로 바뀌는 원인은?
```

### 2.1.1 프로세스 주소공간

#### 프로세스 주소공간

code, data, heap, stack ...

프로그램이 실행될 때 메모리에 올라가서 작업이 수행된다

#### PCB (Process Control Block)

PID, process state, program counter, CPU register ...

프로세스가 생성 --> PCB가 생성되어 메인 메모리에 유지
프로세스가 완료 --> 제거

PCB는 프로세스의 중요한 정보를 포함하고 있으므로 일반 사용자는 접근하지 못하는 보호된 메모리 영역에 존재한다.

### 2.1.2 Process State

```
New --> Ready <---> Running --> Exit
         <-- Waiting <--
```

ready queue, blocked queue에 **linked list 형태로 PCB를 관리**

-   Running -> Ready
    :running 중인 프로세스가 time quantum을 모두 소비

-   Running -> Waiting -> Ready
    :I/O에 의해 블락되어 waiting 상태로 들어가고 작업이 끝난 후 ready에 들어간 경우

-   Ready -> Running
    :ready 상태에서 CPU 스케줄링을 통해 다음 running에 들어갈 프로세스 선택

### 2.1.3 Process Switching

1. 현재 프로세스의 context를 저장
2. 현재 프로세스의 상태를 결정
3. PCB를 적절한 상태 queue에 넣고
4. 다음 프로세스를 결정
5. ready queue에서 PCB를 가져와서 running으로 업데이트
6. 해당 프로세스의 context를 restore

PCB에 저장되어있는 프로세스 상태정보를 CPU에 로드
--> 프로세스 스위칭은 무거운 작업이다.

**유저모드 vs 커널모드**

-   유저모드: user program을 돌리는 process
-   커널모드: kernel을 돌리는 process, system과 관련한 작업을 처리

mode 스위칭과 process 스위칭 관계

-   process 스위칭은 mode 스위칭을 반드시 동반한다 (T)
-   mode 스위칭은 process 스위칭을 반드시 동반한다 (F)
    > system call이 들어오면 유저모드에서 커널모드로 넘어가지만 running중인 프로세스는 계속 돈다.

**Kernel도 프로세스인가? 어떻게 실행하는가?**

1. Kernel을 user process context 안에 포함시켜서 돌린다!

    - user code 안에 OS code를 가상적으로.. (메모리에 kernel space를 할당)
    - mode switching이 process 안에서 일어남

2. Kernel도 하나의 프로세스로 돌린다
    - mode 스위칭을 할 때마다 process 스위칭을 해줘야 함

## 2.2 IPC

```
Q. IPC는 무엇인가? 시그널, 파이프, 공유메모리에 대해서 간단히 설명하라.
```

**프로세스간의 통신을 위한 방법**
프로세스는 커널이 제공하는 IPC를 통해 통신을 할 수 있게 된다.

2가지 모델이 존재

-   Shared Memory
-   Message Passing

https://doitnow-man.tistory.com/110

1. Pipe: 부모 프로세스와 자식 프로세스의 단방향 통신 (파일기반)
2. Named Pipe: 단방향 통신 (파일기반)
3. Message Queue: 단방향 통신 (메모리)
4. Shared Memory: 양방향 통신 (메모리) --> 빠르나 구현복잡
5. Socket: 다른 시스템감 양방향 통신 (네트워크)

## 2.3 Thread

### 2.3.1 Process vs Thread

```
Q. 리눅스에서의 PCB는 어떤 자료구조인가? TCB는 어떤 정보를 가지는가?
Q. thread가 process보다 가벼운 이유는?
```

**Process**는 실행 중인 프로그램
process는 program image와 context를 들고 있음 (heavy-weight)

**Thread**는 프로세스 내의 실행 흐름의 단위
thread는 프로세스 주소공간 중 code, data, heap 영역을 공유하고 stack 영역을 따로 할당받음
각각 thread context(register set, program counter ..)를 들고 있음

> 한 process에 여러 thread의 SP(stack pointer), PC(program counter)가 관리됨

#### Thread의 장점

-   싸다: process의 context switch보다 빠르다
-   리소스공유: 여러 thread가 같은 process의 주소 공간을 사용하여 메모리 공유 (IPC X)
-   멀티프로세서: 한 프로세스가 여러 thread를 병렬로 돌림으로써 멀티프로세서의 장점을 이용할 수 있음

### 2.3.2 Multi-threading

#### PCB? TCB?

-   **PCB**: process 실행 정보를 저장
-   **TCB**: thread별로 program counter, stack pointer, register set을 가지며 PCB를 가리키는 포인터를 가짐

TCB가 PCB보다 작고 싸다

> 현대적으로는 context switching은 사실상 TCB의의 교환을 의미
> 현대적으로는 process 스케줄링이 아니라 kernel thread 스케줄링!

-   같은 프로세스 TCB 스위칭: 프로세스 주소공간 변경 X
-   다른 프로세스 TCB 스위칭: 프로세스 주소공간 변경 O

#### 유저스레드? 커널스레드?

-   user thread: 커널 위에서 관리
-   kernel thread: os에 직접적으로 관리

user thread와 kernel thread를 어떻게 엮느냐에 따라

-   Many-to-One Model
-   One-to-One Model
-   Many-to-Many Model

### 2.3.3 Threading Issue

```
Q. 프로세스, 스레드를 생성, 종료, 종료를 기다리는 system call을 말해보라.
Q. 스레드에서 fork, exec을 호출할 경우 어떻게 되는가?
Q. 스레드에서 system call을 호출해도 문제가 없는가? 스택과 관련하여 설명하라.
```

> Process: fork(), exit(), wait(), exec()
> Thread: pthread_create(), pthread_exit(), pthread_join()

#### 1. fork() 및 exec() system call

thread에서 fork를 호출하는 경우
해당 thread만 있는 single thread process를 복사할 지?
전체 process(모든 thread)를 복사할 지?

-   fork를 부르고나서 exec를 호출한다면, 해당 프로세스는 다른 프로그램으로 대체됨
-   이 때는 모든 thread를 다 복사하는게 의미가 없음!
-   하지만 exec를 호출하는 게 아니라면 thread를 다 복사해줘야 할 것

#### 2. Cancellation

thread가 작업이 끝나기 전에 종료되는 경우
해당 thread의 shared data를 안전하게 처리하고 종료되어야 한다
thread가 자신이 취소되어도 된다고 판단하는 시점에 자신의 취소 여부를 주기적으로 검사

#### 3. Signal handling

thread간의 신호 처리를 어떻게 할 지?

#### 4. Thread Pool

thread를 미리 생성해두고 작업이 들어오면 할당
thread 생성 시간 아끼고 한계 설정이 가능

---

# 3. CPU Scheduling

- Basic Concept
  - Preemptive? Non-preemptive?
  - CPU bound? IO bound?
- 스케줄링 알고리즘
  - FCFS, Round Robin, SJF, SRTF, MLQ, MLFQ

```
Q. CPU 스케줄링 알고리즘은 compute bound 프로그램과 I/O bound 프로그램 중 어느 프로그램에게 CPU 우선 사용권을 주는 가?
Q. 이 원칙을 구현시키는 스케줄링 알고리즘의 이름?

Q. ready 상태에 있는 compute bound와 I/O bound 중 어느 thread를 먼저 dispatch해야 하는가?
```

## 3.1 Basic Concept

#### Preemptive? Non-preemptive?

-   Non-preemptive: 하던거 다 끝내고 자발적으로 나오게 (비선점형)
-   Preemptive: 강제로 뺏자 (선점형)

#### CPU bound? IO bound?

모든 프로세스는 CPU 버스트와 IO 버스트의 반복이다!

-   CPU-bound process: CPU brust가 더 많은 프로세스 (ex. 데이터마이닝)
-   IO-bound process: IO brust가 더 많은 프로세스 (ex. 백엔드 서버)

보통 IO bound 프로세스가 우선순위가 높음 (IO bound는 CPU 사용시간이 짧기 때문)

#### 롱텀 스케줄러? 숏텀 스케줄러?

밑에서는 주로 숏텀 스케줄러를 얘기함

-   Long-term scheduler: 어떤 프로그램를 메모리로 로드할 지! (new --> ready)
-   Short-term scheduler: 메모리에 있는 어떤 프로세스를 프로세서에 할당할 지! (ready --> running)

## 3.2 스케줄링 알고리즘

### 3.2.1 FCFS (First Come First Served)

-   Non-preemptive, 선입선출
-   CPU bound prefered --> IO bound 프로세스는 CPU 사용량에 비해 기다리는 시간이 많아짐

### 3.2.2 Round Robin

-   Preemptive FCFS (with time quantum)

타임퀀텀을 얼마나 줄거냐?
--> 너무 크면 FIFO, 너무 작으면 context 스위치 많아짐

### 3.2.3 SJF (Shorted Job First)

-   수행시간 작은 놈이 앞으로
-   IO bound prefered --> CPU bound starvation (역차별이!)

가장 optimal! but, 다음 프로세스의 수행시간을 어떻게 예측해?
--> 과거 데이터를 기반으로 지수적 평균을 내자!
--> (최근일수록 weight를 크게 주기)

### 3.2.4 SRTF (Shortest Remain Time First)

-   Preemptive SJF

프로세스가 돌고 있는데, 남은 시간보다 더 짧은 프로세스가 새로 들어왔다면?
--> 강제로 쫓아내자! Preemptive!

### 3.2.5 Priority Based

-   priority를 부여하여 먼저 수행 (우선순위가 같으면 FCFS)

낮은 우선순위는 starvation이 발생
--> aging (오래된 process에 우선순위를 점점 높여주자)

> SJF도 Priority based scheduling으로 볼 수 있음 (시간 적은거에 높은 우선순위)

#### 1. Round Robin + Priority

기본적으로 round-robin을 하면서 다음 프로세스 선정 시 우선순위를 부여하겠다

#### 2. MLQ (Multi Level Queue)

우선순위별로 큐를 분리하여 스케줄링하자

#### 3. MLFQ (Multi Level Feedback Queue)

한 큐의 output을 다른 큐의 input으로 넣자
MLQ에서도 starvation이 발생하기 때문에, 큐 별로 타임퀀텀을 다르게 잡고 다음 큐에서 CPU brust를 더 길게 잡도록 하자

### 3.2.6 ETC

프로세스 집합 단위의 스케줄링

-   Fair-share: 집합 별로 CPU를 할당받자
-   Gang scheduling: 집합을 한꺼번에 할당하자

---

# 4. Synchronization

- 동기화란?
  - Race Condition
  - Critical Section
- 유저모드에서의 동기화 방법
  - Peterson Algorithm
  - 하드웨어 서포트
- 커널모드에서의 동기화
  - Mutex Lock
  - Semaphore
  - Monitor
- 동기화 문제들
  - Bounded-Buffer
  - Reader-Writer
  - 철학자의 식사문제

```
Q.synchronization 관련 간단 코드 (flag[2] 세우고 들어가는 상호배제 해결)
코드에서 무슨 문제가 발생하는지!
Q. synchronization 관련 코드 (lock, conditional variable, remove, insert 함수)
코드에서 잘못된 것 고치고 class의 목적을 말하라는 문제..
Q.철학자의 식사에서 데드락 방지 방법? (나오려나..?)
```

## 4.1 동기화란?

### Race Condition

여러 프로세스/스레드가 concurrent하게 동일한 데이터에 접근하면
실행의 결과가 access 순서에 디펜던시를 갖는다

경쟁상황을 피하기 위해서는, 특정 시간 동안 shared data를 하나의 프로세스만 다뤄야함 --> **synchronization**

### Critical Section

여러 프로세스가 공유 자원에 접근하는 특정 코드 영역

Ciritical Section Problem을 해결하는 3가지 조건

1. Mutual Exclusion (상호배제): 어떤 프로세스가 critical section을 실행 중일 때, 다른 프로세스는 진입할 수 없게 하자
2. Aviod deadlock: critical section에 아무도 진입하지 못하는 상황이 생기면 안됨
3. Avoid starvation: starvation을 막기 위해 기다리는 시간에 bound를 두어야 함.

## 4.2 유저모드에서의 동기화 방법

프로그램 코드에서의 동기화 기법

### 4.2.1 Peterson Algorithm

`turn`: ciritical section에 진입하는 프로세스 번호
`flag`: critical section에 진입할 준비가 되었는 지 여부

```cpp
while (true) {
  flag[i] = true;
  turn = j;
  while(flag[j] && turn==j);
  // 임계 구역
  flag[i]=false;
  // 나머지 구역
}
```

1. `turn=j`는 atomic --> 동시에 접근하더라도 하드웨어에 의해 순서가 결정됨 --> progress
2. Pi가 임계구역이면 `flag[i] == ture` 이므로 Pj는 임계구역에 진입할 수 없음 --> 상호배제
3. Pj가 임계구역에 있고 Pi가 busy waiting --> Pj가 임계구역을 나오면서 `flag[j]=false`로 바꿔줌 --> bounded-waiting

> 실제로는 조건문이 atomic하지 않아서 잘 동작하지 않지만 알고리즘적으로 의미있음

### 4.2.2 하드웨어 서포트

Atomicity(원자성): 더 이상 쪼갤 수 없는 operation 단위
`test_and_set()` and `compare_and_swap()`

> ex) 두 값을 swap하는 것을 하나의 회로로, cpu 1 clock으로 처리되도록 만들어보자

mutual exclusion 보장 (deadlock, starvation은 보장하진 못하지만)

## 4.3 커널모드에서의 동기화

커널에서 제공하는 동기화 기법 (커널모드로 변경이 필요하긴 함)

-   뮤텍스락: 2개의 상호배제 해결
-   세마포어: n개의 상호배제 해결
-   Monitor: 위 두 솔루션의 단점 보완
-   Liveness: 상호배제랑 같이 데드락도 해결해보자

### 4.3.1 Mutex Lock

열쇠를 갖고 critical section에 들어가고, 나갈 때 열쇠를 반납한다

커널에서 제공하는 `acquire()` `release()` 함수 / `available` 변수
**위 함수들은 atomically하게 동작한다**

> deadlock과 starvation은 해결되지 않지만 상호배제를 해결하는 것으로도 충분함

### 4.3.2 Semaphore

S개의 열쇠를 제공하고 S가 0보다 작으면 빌려주지 않겠다
S=1이면 mutex ==> binary semaphore

커널에서 제공하는 `wait()` `signal()` 함수
P1에서 signal을 보내야 P2가 실행한다

#### Spin Lock

wait은 내부적으로 busy waiting을 하고있음 --> 스핀락

이를 해결하기 위해 busy waiting 대신, 프로세스를 아예 status queue로 보내버리는 방법이 있음

> wait() 일 때 waiting queue로, signal() 일 때 ready queue로

critical section이 길면 queue로 보내는게 방법이지만,
짧으면 context switchiing이 자주 일어나니 busy waiting이 나음

### 4.3.3 Monitor

뮤텍스, 세마포어는 타이밍 이슈가 발생할 수 있음 (ex. wait -> signal 순서가 안지켜지는 경우)
이런 휴먼에러를 낮춰주자 --> 모니터!

모니터는 Abstract Data Type
Monitor라는 Data Type 안에 함수들을 선언하면, 이 함수들은 동기화된 함수들이다

#### Conditional Variable

모니터에서 추가적인 동기화 메커니즘을 구현하기 위해 필요함
wait, signal 거는 변수를 여러 개 둘 수 있게 하자

```
conditions x, y;
x.wait();
x.signal();
```

## 4.4 동기화 문제들

### 4.4.1 Bounded-Buffer

Producer-Comsumer 문제를 mutex와 semaphore로 해결하기

```cpp
// Producer
while (true) {
    wait(empty); // empty가 있을 때 까지 대기, empty--
    wait(mutex); // 다른 P가 접근하지 못하도록 뮤텍스 락

    // buffer에 아이템 추가

    signal(mutex); // 뮤텍스 반납
    signal(full); // full++
}

// Consumer
while(true) {
    wait(full); // full이 있을 때 까지 대기, full--
    wait(mutex); // 다른 C가 접근하지 못하도록 뮤텍스 락

    // buffer에 아이템 삭제

    signal(mutex); // 뮤텍스 반납
    signal(empty); // empty++
}
```

### 4.4.2 Reader-Writer

Read-only랑 Read-write 프로세스가 concurrent

-   writer가 임계영역일 때, 다른 reader, writer들을 막아야 함
-   reader는 읽기만 하므로 다른 reader들이 함께 읽어도 됨. 하지만 writer는 데이터를 수정하니 막아야 함

```cpp
// Writer
while (true) {
    wait(rw_mutex); // rw_mutex가 있을 때 까지 대기 후 lock

    // writing...

    signal(rw_mutex); // lock 반납
}

// Reader
while(true) {
    wait(mutex); // 다른 reader가 reader_count 건들지 못하게 lock
    reader_count++;
    if(reader_count == 1)
        wait(rw_mutex) // reader가 1일 땐 rw_mutex에 락걸기, 그 이상일 땐 이미 걸려있으니 패쓰
    signal(mutex)

    // reading...

    wait(mutex); // 다른 reader가 reader_count 건들지 못하게 lock
    reader_count--;
    if(reader_count == 0)
        signal(rw_mutex) // reader가 0일 땐 rw_mutex에 락 해제, 그 이상일 땐 아직 읽고있는 놈들 있으니 패쓰
    signal(mutex)
}
```

### 4.4.3 철학자의 식사문제

https://dkswnkk.tistory.com/412
https://letsmakemyselfprogrammer.tistory.com/114

#### Semaphore solution

자신의 양 옆 젓가락에 세마포어 걸기
상호배제는 해결하나, deadlock, starvation은 해결하지 못함

데드락을 해결하려면?

1. 최대 4명의 철학자만이 테이블에 동시에 앉을 수 있도록
2. 젓가락 두 개를 모두 집을 수 있을 때만 젓가락을 집도록
3. 비대칭 해결안 (홀수는 왼쪽 젓가락 먼저, 짝수는 오른쪽 젓가락 먼저)

하지만 starvation은 발생 가능

#### Monitor solution

위에서 데드락을 해결하기 위해 철학자는 양쪽 젓가락 모두 얻을 수 있을 때만 젓가락을 집을 수 있다는 제한을 강제

```cpp
enum {THINKING, HUNGRY, EATING} state[5];
condition self[5]; // 원하는 젓가락을 집을 수 없을 때 젓가락 집기를 미룰 수 있게
```

하지만 starvation은 발생 가능

---

# 5. Deadlock

- Deadlock의 필요조건
  - Mutual Exclusion / Hold and Wait / No Preemption / Circular Wait
- Deadlock 문제의 해결
  - Prevention
  - Avoidance (Banker's Algorithm)
  - Detection
  - Recovery

```
Q.deadlock이 발생할 4가지 필요조건?
Q.deadlock과 관련된 4가지 조건은 필요조건인지 충분조건인지
Q.위의 4가지 조건 각각에 대한 deadlock prevent 방법
Q.deadlock avoid 방법
Q.deadlock detection and recover 방법
```

## 5.1 Deadlock의 필요조건

데드락은 각 프로세스가 서로 리소스를 wait하는 상태 (리소스가 한정되어있기 때문에)

#### 데드락의 필요조건

1. Mutual Exclusion(상호배제): 한 리소스를 하나의 프로세스만 사용하도록
2. Hold and Wait(점유하고 대기): 자원을 가지고 있는 상태에서 다른 프로세스가 사용하고 있는 자원의 반납을 기다리는 것
3. No Preemption(선점 불가): 다른 프로세스의 자원을 강제로 가져올 수 없음
4. Circular Wait(순환 대기): 각 프로세스가 순환적으로 다음 프로세스가 요구하는 자원을 가지고 있는 것

#### 왜 필요조건?

-   데드락이 발생하면 위 4가지를 동시에 만족한 상황인 것임
-   그러나 위 4가지 상황이라고 반드시 데드락이 발생하진 않음

## 5.2 Deadlock 문제의 해결

OS 차원에서 데드락을 해결하는 방법!

-   Prevention or Avoidance: 시스템이 절대로 데드락에 빠지지 않게 하자
-   Detection and Recovery: 데드락이 발생했는지 감지하고 이를 바로 해결하자

### 5.2.1 Prevention

데드락 발생을 위한 4가지 필요조건들...
이 중 하나만이라도 false로 만들면 된다!

#### 1. Mutual Exclusion

상호 배제는 일관성을 유지하기 위해 반드시 필요한 조건이므로 제거하기 힘들다.

#### 2. Hold and Wait

프로세스가 리소스를 요청할거라면 아무것도 잡고있지 마라! --> 실용적이지 않음

#### 3. No Preemption

다른 프로세스의 리소스를 뺏어버리자 --> 뺏긴 애는 문제가 발생하므로 실용적이지 X

#### 4. Circular Wait

자원의 할당 순서를 정하고 프로세스는 그 순서대로 자원을 요청하도록 한다
리소스에 priority를 주고 내가 점유한 리소스보다 priority가 높은 애들만 요청할 수 있게 하자

### 5.2.2 Avoidance

Prevention은 사이드 이펙트도 많고 멀티 쓰레딩의 장점을 prevention이 다 까먹음...
Avoidance는 prevention 만큼 강력하진 않지만 좀 더 현실적..
리소스 할당을 좀 더 잘해서 데드락을 피해보자!

#### Banker's Algorithm

**Safe State**: 프로세스를 이런 순서로 실행하면 데드락을 피할 수 있다!
하지만 사전에 process의 max request를 미리 알아야 함

```md
프로세스: 5개
리소스 A: 10개, B: 5개, C: 7개

-   allocation[3]: 현재 P0는 0,1,0 을 잡고 있음
-   max[10][3]: P0는 lifetime 중에 리소스를 최대 7,5,3 요청할 예정
-   available[10][3]: P1~P4가 잡고 있는거 빼면 3,3,2
-   need[10][3]: 앞으로 P0가 리소스를 이만큼 더 가져야한다 (max-allocation)
```

뱅커스 알고리즘에 의하면 현재는 T1, T3, T4, T2, T0 순서로 돌면 safe status
그러던 중 T1이 (1,0,2)를 요청했다?
요청이 들어온다 치고 safety algorithm을 돌려보자

-   safe status를 가질 수 있네? allow!
-   request가 available을 초과하네? reject!
-   safe state 순서가 안나오네? reject!

### 5.2.3 Detection

1. 싱글인스턴스 (리소스당 인스턴스가 하나 인 경우)

-   자원 할당 그래프에서 순환이 있는 지 확인하기

2. 멀티인스턴스 (리소스당 인스턴스가 여러 개인 경우)

-   뱅커스 알고리즘을 활용하기
-   대신 아까처럼 미리 request를 알 수 있는 상황은 아니고 request 자체가 이미 주어진 상황
-   현재의 상황이 deadlock인지 아닌지를 확인하는 것

> 얼마나 detection을 할거냐? 발생하는 빈도에 비해 자주하면 오버헤드가 큼

### 5.2.4 Recovery

1. Process Terminate

-   데드락에 걸린 프로세스를 하나 씩 죽여가며 나머지를 풀자

2. Resource Preemption

-   데드락에 걸린 프로세스를 일시정지 시키고 점유하고 있는 리소스를 다른 프로세스에게 할당

---

# 6. Main Memory

- Address Spaces (logical? physical?)
- Contiguous Memory Allocation
  - Fixed Partitioning
  - Dynamic Partitioning
  - Buddy System
- Paging
  - Page Table
  - Memory Access Overhead (TLB)
  - Handling Large Page Table

```
Q. 가상메모리가 같은 주소를 나타내지만 실제 메모리에서는 그렇지 않다. 어떻게 가능한가?
Q. 실제 메모리에서 프로세스가 같은 주소를 참조할 수 있는가? (shared memory)
Q. page partioning: First-fit / Best-fit / Worst-fit
Q. 페이지를 통해 메모리에 접근하는 시간 계산 (아마 2배?) 연관 레지스터 (TLB?)에 75% hit된다면 시간이 얼마나 주는 지?
Q. 주어진 시스템(64bit 64K page)에 대해서 1단계 Page table translation에 서술하는 문제가 나왔다
Q. TLB 와 Data Cache 중 TLB가 일반적으로 hit rate이 더 높은데, 그 이유는?
```

## 6.1 Memory Allocation

어떻게 여러 프로세스를 물리적인 메모리 공간에 연속적으로 맵핑할거냐?

### 6.1.1 Address Spaces

프로그램을 실행하기 위해서는 메모리에 올려야 한다.

1. 소스코드에서의 주소는 symbolic한 상태이다. (소스코드)
2. 컴파일러는 symbolic 주소를 relocatable 주소로 바인딩한다. (소스파일)
3. linker를 거쳐 logical address를 갖게 되고 (실행파일)
4. loader를 거쳐 physical address를 갖게 된다 (program in memory)

메모리 주소의 형태

-   Symbolic address: 소스코드에서의 주소
-   Logical address: 프로그램이 실제 실행되기 전 첫 주소를 0으로 사용하는 논리 주소
-   Physical address: 하드웨어에 실제 존재하는 주소

### 6.1.2 MMU

OS는 logical address를 physical address로 맵핑해주는 역할해야 함
그 역할을 하는 CPU와 memory 사이의 하드웨어 유닛이 **Memory Management Unit**

> base register, limit register

### 6.1.3 Swapping

프로세스 크기보다도 메모리가 더 작다면?  
괜찮아! 필요한거만 memory에 올리면 되니까!

한정된 물리적 메모리 공간 안에 여러 프로세스 메모리를 올리기 위해  
기존 프로세스를 Backing store에 임시로 옮겨두고 다른 프로세스를 처리  
다시 Backing store에서 프로세스를 불러오는 일련의 과정

메모리에 엑세스해야할 때만 메모리에 올라와라 --> _Swap In_  
아니면 밖에 나가 있어라 --> _Swap Out_

## 6.2 Contiguous Memory Allocation

-   Contiguous Memory Allocation: 프로세스가 메모리에 통짜로 올라감
-   Memory Protection: 프로세스별로 메모리 영역을 분리, 다른 프로세스의 메모리 영역을 접근하면 안됨
-   이를 제어해주는 애가 base register, limit register
-   그러나 이렇게 할당하게 되면 hole이 생겨버림

### 6.2.1 Fixed Partitioning

1. Equal-size: 모든 공간을 균일하게 쪼개서 넣겠다. (큰거 들어오면 못받아)
2. Unequl-size: 효율성을 높이기 위해 방 크기를 제각각으로 쪼개서 넣겠다.
  -   멀티 queue: 사이즈별로 큐 설정. 특정 사이즈 공간에 프로세스가 몰리면 문제
  -   싱글 queue: 멀티프로그래밍 레벨은 올라가지만 internal fragment 높아짐

**Internal Fragment**  
프로세스에 할당된 메모리 공간이 실제 프로세스가 사용하는 공간보다 큰 것

### 6.2.2 Dynamic Partitioning

1. First-Fit: 빈공간 체크해서 가장 처음에 걸리는 놈
2. Best-Fit: 남는 방이 제일 적은 놈
3. Worst-Fit: 남는 방이 많은 놈을 골라서 다음에 다른 거 넣을 가능성 높이기

**External Fragmentation**  
자투리 공간이 여러 개 남는 것. request를 만족하는 공간이 남지만 연속적이지 않아 할당을 못함

### 6.2.3 Buddy System

Fixed는 internal, Dynamic은 external fragmentation --> 이들의 장단점을 적절히 활용하자

- 메모리 전체를 left half / right half로 반복적으로 쪼개기
- 맞는 공간이 생기면 할당
- release 시, 다른 side가 비어있으면 merge

## 6.3 Paging

https://studyandwrite.tistory.com/19?category=1004636

### 6.3.1 Paging

Contiguous Memory allocation 기법은 logical memory를 physical memory에 연속적으로 할당함  
logical memory를 굳이 연속적인 물리 공간에 할당할 필요가 있는가?

-   frame: physical memory를 fixed-size로 쪼갠 것
-   page: logical memory를 위와 동일한 사이즈로 쪼갠 것

(p, n) p번째 page n번째 줄 ==> (f, n) f번째 frame n번째 줄

### 6.3.2 Page Table

p의 값을 table의 index로 쓰는 것

가정: 32bit 머신에서 4KB로 페이징한다.

-   logical memory: 2^32 (4GB)
-   page size: 2^12 (4KB)
-   page 갯수: 2^20 (1MB)
-   page entry size가 4byte라면 page table은 4MB

#### Page Table Structure

Page entry size가 32bit?
offset 제외하면 20bit로 충분한데?
Page table은 단순히 매핑정보 뿐 아니라 다양한 bit flag를 들고 있음

1. Reference bit
  - 어떤 시간 간격에 reference 했으면 1, 시간이 지나면 0이 됨
  - page 교체 정책에서 대략적인 LRU를 판단하기 위함
2. Dirty bit
  - 해당하는 페이지가 메인메모리에 올라온 이후로 수정되었는 지 여부
3. Valid bit
  - 1이면 main memory, 0이면 disk storage에 있다
4. Read, Write access bit
  - 메모리 protection을 위한 접근 권한 제어 비트

### 6.3.3 Memory Access Overhead

Page table을 프로세스가 공유할 수 없음  
프로세스가 CPU에서 나갔다 들어왔을 때, page table이 그대로 있지 X  
프로세스 마다 page table을 가지고 있다

#### PTBR

page table의 시작 번지를 가리키는 레지스터  
page table 자체는 메인메모리에 두고 PTBR만 PCB에 저장해서 context switch!

PTBR + page number로 메모리에서 인덱스를 찾아감.  
근데 이러면 memory access가 2번 발생함

1. page table 접근 (MMU에서 함)
2. 실제 memory access

#### TLB

Translation Lookaside Buffer

- page table 전에 TLB라는 캐시를 둬서 (하드웨어레벨)
- TLB hit 되면 바로 access
- TLB miss나면 page table에서 찾기
- page의 locality가 높기 때문에 hit ratio가 높다!

### 6.3.4 Handling Large Page Table

logical address space 자체가 너무 크다 --> page table 자체가 커진다

#### 1. Multi-level Paging

- page table이 너무 커져서 관리하기 힘들다
- page table도 쪼개서 얘의 page table을 관리하자 (chapter -> page -> offset)
- 메모리 접근을 3번 해야 함

> 2^20개의 page (4*2^20 = 4MB)  
> 1024 page를 하나의 chapter로 나누자 (1024개 chapter)  
> 총 1025개의 page table, 하지만 실제 쓰는건 2개 테이블 (4*2^10\*2개 = 8KB)

#### 2. Hashed Page table

- Page table을 hash table로 관리한다
- hash는 O(1)의 시간복잡도 --> 빠름
- 같은 해시 결과값에 대해 리스트를 이용하여 메모리 문제를 조금 해결할 수 있다

#### 3. Inverted page table

- 기존엔 프로세스 당 하나의 페이지 테이블을 갖고 페이지 번호를 인덱스로 가짐
- 프레임 번호가 인덱스가 되고 어떤 프로세스(pid)가 어떤 페이지를 갖는지 역으로 저장
- 전체 프로세스에 하나의 테이블을 갖지만 검색 시간이 걸리는 단점

---

# 7. Virtual Memory

```
Q. page 교체 알고리즘: LRU, FIFO (LRU가 모든 상황에서 최소 FIFO만큼은 동작한다)

Q. Page replacement policy에 대한 문제들이 나왔다. 시스템에 있는 페이지가 N개이고 회수 알고리즘에 따라 발생하는 page miss를 계산하였다.

Q. working set model은...
-   page X를 언제 fetch하는가? page X는 언제 메모리에서 밀려나는가?
-   몇 개의 page frame을 OS에 요구하는가?
-   working set의 요구를 OS가 다 들어주지 못하면 어떻게 대응?

Q. page fault가 빈번해지는 현상을 뭐라하는가?
```

## 7.1 Demandig Paging

물리 메모리와 논리 메모리를 완전히 분리하자. 프로그래머가 물리 메모리를 아예 모르게 하자.

1. secondary storage 공간에서 main memory 공간으로 로딩
2. 한꺼번에 하는게 아니라 page 단위로 짤라서 올리자
3. 언제 올릴건데? 요청할 때만 올리자

**Concept**
- 어떤 페이지는 memory에 이미 올라가있고 어떤 애는 아직 secondary 스토리지에 있고
- 이 두 상황을 구분하기 위해 valid bit 체크
- valid bit가 0이면? page fault!

### 7.1.1 Page Fault

메모리에 접근할 때,
1. memory에서 page table 확인하고
3. 만약 invalid면, Page Fault가 발생 --> swap in 해야 함
5. process에 exception을 걸고 커널모드로 넘어가서 page fault handler 수행
4. secondary disk에서 page를 읽어온다
5. 빈 frame을 찾아서 페이지를 그 frame에 할당
7. page table을 업데이트 (frame number, valid bit)
8. 유저모드로 넘어가서 insturction을 계속 실행

#### Context switch

Page fault가 일어나면, process에 trap 걸림  
--> process를 wait queue로 보내버려 (context switch)

그럼 다시 context를 reload할 때, 이 프로세스의 page table이 유효한 걸까?  
그 사이에 다른 프로세스가 swap out / swap in 했다면?

즉, process 별로 page table을 잘 관리해야한다. (page table 다 업데이트 해줘야하는 것 같음)

#### Instruction Restart

- instruction을 fetch하다가 page fault 발생 --> reload하고서 instruction을 다시 fetch
- operand를 fetch하다가 page fault 발생 --> reload하고서 instruction부터 다시 fetch

`ADD A, B, C` --> A, B, C를 가져오다가 page fault나면 ADD부터 다시 해야 함 (worst case)

### 7.1.2 Locality

`ADD A, B, C` --> 1개 instruction, 3개 변수 --> 4번의 page fault가 발생할 수도?!
하지만 생각보다 이런일이 잘 일어나지 않는다.

즉, 지역성이 있기에 demand page가 효율이 나쁜 건 아니다! (쓰는 부분만 쓰게 되는 경우가 많음)

## 7.2 Page Replacement Algorithm

목표: page fault의 비율을 낮춰야 한다!

### 7.2.1 FIFO

- 가장 먼저 온 놈을 쫓아내라
- 단점: 내 프로세스에 frame을 더 많이 할당해도 page fault 성능이 개선되지 않음

### 7.2.2 Optimal

- 가장 미래에 사용될 page를 victimize 하자
- 가장 이상적이지만, not possible (reference string을 미리 알아야...)
- 얘는 주로 다른 알고리즘이 성능비교하는 대상으로 쓰임

### 7.2.3 LRU

- CPU 스케줄링의 SJF 처럼, recent past를 통해 near future를 예측하자
- 아주 오랜 기간동안 사용하지 않은 애는 미래에도 사용하지 않지 않을까?!
- Least Recent Used

이 frame이 언제 마지막으로 사용되었는가를 계산해야 함
1. counter: page별로 참조된 횟수를 계산하자 --> 가장 count 값이 작은/많은 애를 victim
2. stack: page 번호를 스택해서 최근에 쓰인 걸 올리자 --> 바닥에 있는애가 젤 오래 안 쓴 애

LRU는 커널레벨에서 구현하기에 오버헤드가 크다 --> 하드웨어의 지원을 받아 approximation 해보자

### 7.2.4 LRU Approximation

#### Additional Reference Bits

일정한 간격으로 reference bit를 기록하는 1byte를 기록하자
8bit의 reference bit 기록이 가장 낮을수록 오랫동안 참조되지 않은 것

#### Second-chance Algorithm

- FIFO를 쓰는데, reference bit를 이용해서 second chance를 주자
- reference bit가 0이면 victimize
- reference bit가 1이면 active할 것이니 skip (단 스킵하면서 0으로 바꿔주는 것)


## 7.3 Frame Allocation

각 프로세스들에게 몇 개의 frame을 배정할거냐?

**Equal vs Proportional**
1. Equal Allocation: 모든 프로세스에게 동일하게 주자
2. Proportional Allocation: 프로세스 사이즈에 비례해서 주자

**Global vs Local**
1. Global replcaement: replacement 할 때, 전체 frame에서 victim을 정할거냐
2. Local replcaement:replacement 할 때, 프로세스 영역 안의 frame에서 victim을 정할거냐

## 7.4 Thrashing

멀티프로그래밍 정도가 높아질수록 CPU 사용량 높아짐.
그러다 갑자기 뚝 떨어진다! 왜?

size of running process's page > total memory size

page fault 발생으로 page를 교체하는 시간이 너무 길어져서!

page가 100개인데 process도 100개다? 그럼 맨날 page fault 남
--> CPU 갔다가 page fault나서 wait queue 가고 반복
--> CPU util은 떨어지고 시스템은 버벅거리고

## 7.5 Working Set Model

memory reference pattern을 살펴보면 특정 페이지를 집중적으로 사용한다
--> 인접해있는 페이지가 같이 사용된다

Working-Set: locality가 있는 set of page

즉, working set 바깥에 있는 애를 victim으로 지정하자는 것

---

# 8. File System

```
-   디스크 스케줄링 문제 (SSTF 스케줄링 알고리즘 계산)

-   디스크 스케줄링 문제 (SCAN 스케줄링은 indefinitely postponed 될 수 있는가? 맞다면 어떤 상황에서?)

-   파일 I/O는 크게 read, write 명령에 의한 I/O와 memory mapped I/O

    -   이들을 설명하고 장단점 비교
    -   read, write의 디스크 엑세스 회수와 latency를 줄이기 위해 buffer cache를 사용하는데, 버퍼캐시를 할당하고 관리하는 정책의 개요 설명하시오.
    -   memmory mapped I/O에도 버퍼캐시를 사용하는 게 좋은가? 왜그런가?

-   DMA가 시스템 성능에 미치는 영향 2가지 이상

-   DMA란 무엇인가?

    -   cache가 있는 시스템에서 DMA에 의해 발생할 수 있는 문제점과 해결책?
    -   Virtual memory가 있는 시스템에서 DMA가 physical address를 이용한다고 가정할 때, 문제점과 해결책?

Q. DMA에 대한 설명과 이를 구현하기 위한 하드웨어에 대한 문제가 나왔다. 운영 체제 책에서는 참고하지 않았던 파트라, 펌웨어 개발할 때 참고했던 Technical reference manual에 기반하여 서술했다...

-   FFS(Fast File System)과 LFS(Log File System)의 차이를 설명하라

-   디스크 속도 vs 네트워크 속도 계산 (이거 뒷장에 나오는 내용 맞나유ㅠ)

-   swap space를 위해서 기존의 파일시스템을 사용하는 것과 별도의 파티션을 사용하는 것의 차이
-   별도의 파티션 사용 시, 성능을 올리기 위한 방법?

Q. 컴퓨터가 file에 data를 쓰던 중, 갑자기 전원이 꺼지는 경우, 다시 켰을 때 그
data를 잃는 문제뿐만 아니라, 해당 file에 전혀 다른 data가 덮어 쓰이는 이상한 현
상이 발생할 수 있다. 이러한 문제들을 해결하기 위해서 어떠한 방법들이 사용되는
지 설명하시오.
// 답은 BIOS 였는데 너무 기초적인거라 솔직히 답 못한게 어이없긴 했습니다.일단 면접은 합격을 했습니다.
```

---

# 9. Security

-   Access control list가 Access control matrics 보다 더 유리한 상황은?
