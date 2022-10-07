# single clock cycle

single clock cycle을 위한 datapath

- PC
- instruction memory
- register file
- ALU

instruction의 모든 작업이 한 clock에 끝난다
업데이트 되어야 할 부분이 PC랑 Reigster file 2개 --> 같은 clock을 씀

clock의 rising edge에서 업데이트가 한번에 일어난다

single cycle은 fetch --> decode --> execute가 한 클락 사이클에서 다 일어나는 것

(하지만 보통은 여러 클락이 걸려..? 지금은 중간에 레지스터가 암것도 없는 구조라서 가능)


### R-type(add, sub ...)
```
op rs rt rd shamt funct
 6  5  5  5  5   6
```

- PC
- instruction memory
- register file
- ALU

### lw, sw
```
op rs rt immediate
6  5  5    16

IR <- mem[PC]   # fetch instruction from memory
Addr <- R[rs] + SignExt(imm16)    # 16비트 상수를 32비트로 만들고
R[rt] <- Mem[Addr]
PC <- PC + 4
```

- PC
- instruction memory
- register file
- ALU
- data memory (with mux)

### beq
```
op rs rt immediate
6  5  5    16

IR <- mem[PC]   # fetch instruction from memory
Cond <- R[rs] + ~R[rt] + 1    # rs, rt 비교 (빼면 0?)
PC <- Cond ? PC + 4 : PC + 4 + (SignExt(imm16) << 2)    # 명령어의 주소는 4의 배수이기 때문
```

- PC
- instruction memory
- register file
- ALU
- branch 신호?


###

mux가 매우 많은데 이 mux 신호는 누가 관리해? --> op 코드에서! (제어부)

- mux select 신호
- data memory에 읽기? 쓰기?
- ALU에서 무슨 계산을 할 건지?

control


한비트 한비트로 할 수 있는 게 무궁무진....


## 문제

cycle time은 가장 오래걸리는 path에 맞춰져야 함 --> load(600ps) --> cloak은 600ps 이상

solution: multi-cycle
중간중간 register를 두어서 clock 사이클에 필요한 path를 줄인다
clock 사이클 수는 늘지만 clock 주기는 짧게할 수 있다.
