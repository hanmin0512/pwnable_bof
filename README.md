# pwnable_bof pwnable.kr의(CTF) buffer overflow 문제이다. 
## 풀이 순서
- 코드 분석
- 문제 분석
- 어셈블리언어 분석
- attack

## 코드 분석 bof.c
> bof.c <br>
![스크린샷 2023-07-27 오전 12 09 37](https://github.com/hanmin0512/pwnable_bof/assets/37041208/fe8fe4c9-9535-4238-a81e-dfb17c694d69)
- 코드는 대체적으로 간단하다.
- 프로그램 시작과 동시에 16진수 0xdeadbeef를 func 함수인자 값으로 전달한다.
- func 함수는 0xdeadbeef를 key의 인자값으로 받으며 호출된다.
- 사용자의 입력 값을  overflowme 라는 32bytes 버퍼가 할당된다.
- printf 함수 호출로 "overflow me : "가 출력된다.
- 사용자의 입력값을 overflowme 버퍼에 값으로 할당한다.
- 만약 인자값으로 받은 key가 0xcafebabe라면 쉘을 획득하여 cat flag를 실행 시킬수 있다.
- 그렇지 않다면 쉘을 획득할 수 없다.

## 문제 분석
> 이 문제는 0xdeadbeef가 func 함수의 key의 값으로 전달 되지만 buffer over flow를 이르켜 key의 값을 0xcafebabe로 변조시켜야 한다.
> 함수는 stack프레임을 사용하므로 stack과 overflowme 버퍼를 잘활용해야 한다.

## 어셈블리언어 분석
> gdb 사용 (set disassembly-flavor intel 명령어를 사용하여 intel형식의 assembly언어로 설정)
> main() <br>
![1](https://github.com/hanmin0512/pwnable_bof/assets/37041208/daddcdf3-f1cc-49af-bc03-70544facdda1)
- <+0>: EBP 레지서터의 값을 스택에 저장
- <+1>: ESP 레지스터의 값을 EBP에 복사하여 EBP가 현재 스택 프레임의 베이스 주소를 가리키게 됨
- <+3>: ESP 레지스터의 하위 4비트를 0으로 설정하여 16바이트로 정렬.
- <+6>: ESP 레지스터에서 16바이트를 빼서 스택 공간 할당
- <+9>: 스택에 0xdeadbeef값을 저장
- <+16>: func 함수 호출
- <+21>: EAX 레지스터에 0저장
- <+26>: 스택프레임 복귀, EBP를 ESP로 설정하고, 이전 EBP값을 EBP로 복원하는 과정
- <+27> 함수 종료

> func() <br>
![2](https://github.com/hanmin0512/pwnable_bof/assets/37041208/1230e3e7-ed3b-4802-8a2b-0b86f239333c)
- <+0>: EBP에 값을 스택에 저장
- <+1>: ESP값을 EBP에 복사
- <+3>: ESP레지스터에서 72바이트를의 공간을 할당
- <+6>: GS 세그먼트의 0x14오프셋 주소에 저장된 값을 EAX에 저장
- <+12>: EAX값을 EBP- 0xc 주소에 저장
- <+15>: EAX값을 0으로 설정
- <+17>: 스택에 0x78c 값을 저장
- <+24> func+25 주소로 점프하여 함수를 호출 (printf 함수 호출)
- <+29> EBP - 0x2c 주소를 EAX 레지스터에 로드하기. …(gets 함수의 인자로 전달될 주소 overflowme 변수 주소로 이 변수를 시작으로 buffer over flow를 해야한다.)
- <+32> EAX값을 스택에 저장
- <+35> func+36 주소로 점프하여 함수 호출 (gets 함수)
- <+40> 함수의 인자로 전달된 key값과 0xcafebabe 값 비교 (key변수의 시작위치 ebp+0x8)
- <+47> 값이 다르다면 0x66b 주소로 점프하여 분기
- <+49> 스택에 0x79b 값을 저장
- <+56> func+57 주소로 점프하여 함수 호출.
- <+61> 0x677주소로 무조건 점프
- <+63> 스택에 0x7a3 값을 저장
- <+70> func+71 주소로 점프하여 함수를 호출
- <+75> EBP - 0xc 주소에 저장된 값을 EAX 레지스터에 저장.
- <+78> GS 세그먼트의 0x14 오프셋 주소에 저장된 값을 EAX 레스터와 XOR 연산
- <+85> 두 값이 같으면 0x688 주소로 점프하여 분기
- <+87> func + 88 주소로 점프
- <+92> 스택 프레임을 복원
- <+93> 함수 종료

## 정리
- key 변수의 주소는 [ebp + 0x8] 이고 buffer overflow시켜야 하는 지점은 overflowme 변수의 시작주소인 [ebp - 0x2c] 이다.
- [ebp + 0x8]주소를 시작으로 [ebp-0x2c] 지점에 0xcafebabe를 넣으면된다.
- 0x8 - (-0x2c) = 52 <br>
![3](https://github.com/hanmin0512/pwnable_bof/assets/37041208/59635d6b-120c-4fa9-85e5-dee485d52ebb)
- 즉 overflowme[32]버퍼에 32개이상 52개의 아무문자를 넣고 이후에 0xcafebabe를 넣으면된다.
- 코드는 payload.py를 실행시켰다.
![4](https://github.com/hanmin0512/pwnable_bof/assets/37041208/b0404160-e2cf-4f0a-9c92-f0f0dcbe3aac)
  
