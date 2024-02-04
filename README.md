# 🚗 2023_Self_Driving

> 지능형자동차부품진흥원에서 주최한 『[2023 대구모형전기자율주행차 경진대회](http://www.kiapi.or.kr/pages/board/view.php?board_sid=1&data_sid=723&page_num=2&skey=&sval=)』에 참가하여 OpenCV를 이용해 모형 자동차의 주행 기능을 개발 과정을 기록한 저장소입니다.
<br/>

# 👐 소개
- ## 주제 : 자율주행 모형차를 이용한 미션 수행 및 경기장 주행
-  제공된 코드를 수정하여 모형차가 **"직선 및 곡선 주행"**, **"장애물 회피"**, **"오르막 주행"**, **"신호등 인식"** 을 수행할 수 있도록 합니다.
- 차량의 컨셉을 정하고, 그에 맞는 차체를 제작하여 주행합니다.
- 가장 빠른 시간 내에 경기장을 주행하는 팀이 우승하는 대회입니다.
<br/>

https://github.com/wvssm/2023_Self_Driving/assets/52875244/9a7991bf-d41a-4be2-9dd6-697c2f2a9915

<!--- ## 차량사진
|대각선|정면|
|:---:|:---:|
|![차량사진1](./images/car_1.jpg)|![차량사진2](./images/car_2.jpg)|-->

# 개발 환경 및 언어
<img src="https://img.shields.io/badge/Ubuntu-E95420?style=for-the-badge&logo=ubuntu&logoColor=white"> <img src="https://img.shields.io/badge/ROS-22314E?style=for-the-badge&logo=ros&logoColor=white"> <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">

<br/>

# 🧑‍💻 참가 및 역할 분담
|강수민|팀원 1|팀원 2|
|:---|:---|:---|
|정보컴퓨터공학부|기계공학부|산업공학과|
|• 차선 인식 기능 개선 (Python, OpenCV)<br>• 장애물 회피 기능 개선 (Python, LiDAR)<br>• 신호등 인식 기능 개선 (Python, OpenCV)<br>| • 차체 모델링(Creo CAD)<br> • 차체 설계파일(.step) 제작<br> • 차량 주행 기능 개선 방안 제안<br> • 차량 컨셉 제안<br>| • 차체 모형 디자인<br> • 주행 연습 도로 제작<br> • 차량 주행 기능 개선 방안 제안<br> • 차량 주행 영상 촬영 및 피드백<br>|
<br/>

# 🚩대회 진행 과정
_대회 과정은 "[블로그](https://wvssm.tistory.com/category/%F0%9F%93%81Project/2023%20%EB%8C%80%EA%B5%AC%EB%AA%A8%ED%98%95%EC%A0%84%EA%B8%B0%EC%9E%90%EC%9C%A8%EC%A3%BC%ED%96%89%EC%B0%A8%EA%B2%BD%EC%A7%84%EB%8C%80%ED%9A%8C)"에 기록해두었습니다._
> #### 일정 
> - 참가 신청 : ~ 2023.07.07(금)
> - 팀원 결성 : 2023.06.30(금)
> - 서류 작성 : 2023.07.01(토) ~ 2023.07.07(금)
> - 합격자 발표 : 2023.07.28(금)
> - 오리엔테이션 및 차량 배부 : 2023.08.25(금)
> - 1차 연습 : 2023.09.01(금) - 연습 도로 제작, 라인트레이싱
> - 2차 연습 : 2023.09.08(금) - 라인트레이싱 성공
> - 3차 연습 : 2023.09.09(토) - 장애물 회피 기능 구현
> - 차체 제작 : 2023.09.15(금) - 우드락으로 차체 틀 제작
> - 4차 연습 : 2023.09.17(일) - 차체 착용 후 주행 연습
> - 5차 연습 : 2023.09.22(금) - 차체 꾸미기 및 주행 속도 상승
> - 6차 연습 : 2023.09.23(토) - 장애물 회피시 흔들림(라이다 이슈) 문제 분석
> - 중간 점검(7차 연습) : 2023.10.06(금) - 장애물 회피 시 흔들림 문제 해결 
> - 8차 연습 : 2023.10.07(토) - 주행 속도 높이기 작업
> - 9차 연습 : 2023.10.13(금) - 도로 재제작, 오르막 주행 연습, 차량 속도 상승
> - 10차 연습 : 2023.10.14(토) - 신호등 인식
> - 11차 연습 : 2023.10.15(일) - 신호등 인식을 포함하여 주행
> - 리허설(12차 연습) : 2023.10.19(목) - 경기장 환경 탐색
> - 13차 연습 : 2023.10.20(금) - 경기장 경로에 맞게 경로 조정, 장애물 회피 다시 구현
> - 경진 대회 : 2023.10.21(토) - 30팀 중 7위 <br><br>


# 🚨 문제 발생과 해결 방법
### 문제
- 이전 1주차 연습에서는 모형차가 라인트레싱을 정상적으로 수행하였는데, 장소를 바꾸어 2주차 연습을 진행할 때는 차량이 라인트레이싱을 정상적으로 수행하지 못했다.
### 해결
- 기존의 검출 화면을 확장하여 차선이 차량의 중심에서 멀리 떨어져 있더라도 이를 인식 할 수 있도록 만들었다.
- 차량이 오차값에 비례해서 방향이 꺾이는데, 비례 상수 값을 키워 동일 오차값에 대해 차량이 각도를 좀 더 많이 꺾도록 작성했다. 
  
### 문제
- 직선에서는 속력이 빠르나 곡선에서는 주행 속력이 느려진다.
### 해결
- 현재 코드는 직선 주행 시 기존 속력에 변화가 없으나, 곡선 주행 시 차선과의 오차값이 클 수록 차량의 조향각은 비례해서 커지고, 속력은 반비례하여 느려진다.
  - 따라서 **기본 속력이 커질수록 직선 주행 속력과 곡선 주행 속력의 격차가 커져서** 커브 구간에 버벅거리는 현상이 발생한 것이다.
  
- 직선 주행 속력과 곡선 주행 속력을 동일하게 정하지 않고, 각 상황에 맞게 적절한 값을 설정해야 한다.
  - 직선 주행 속력은 가능한 빠르게 설정하고, 곡선 주행 속도는 커브링이 부드럽게 되는 정도까지 속력을 올렸다.


### 문제
- 장애물 회피 시 차량이 휘청거렸다.
### 해결

 - 차량이 장애물을 지나는 구간에 장애물을 제대로 인식하지 못해서 발생한 동작이었다.
 - 라이다를 발사하는 범위를 넓혔다. ex) 정면 기준 오른쪽 10도 ~ 90도 -> 정면 기준 0도 ~ 90도로 수정
   - 차량이 장애물을 이전보다 빠르게 인식하여, 장애물 충돌 없이 원활하게 회피할 수 있게 되었다.
  
- 발사하는 레이저의 개수를 증가했다.
    - 장애물에 반사해서 돌아오는 레이저 개수가 늘어, 장애물을 인식률을 높일 수 있었다.

### 문제
- 곡선 구간에서 뚝뚝 끊기듯이 주행한다.
### 해결
- 곡선 구간에서 차량은 주행 라인도 따라가야하고, 오차값만큼 또 바퀴를 꺾어주어야한다. 따라서 이 두 가지가 충돌하여 뚝뚝 끊기는 주행이 발생한 것이다.
  
  - 곡선 구간에서 오차값에 따라 꺾이는 값(비례 상수)를 적절하게 조정하여(기존보다 감소시켜) 방향 전환 시 차량이 차선과 극단적으로 멀어지지 않도록 수정하였다.

### 문제
- 초록생 원형의 신호등을 인식해야되는데, 신호등 뒤의 잔디의 초록을 인식하여 신호등이 켜지지 않았는데도 자동차가 출발한다.

### 해결
- 검출화면에서 신호등 부분만을 크롭하여, 뒤에 어떤 색상의 배경이 있든 신호등에 의해서 차량이 출발하도록 조정했다.
  
- 가끔 초록색이 아닌데도 초록으로 검출하는 오류도 존재한다.
  - green_count라는 변수를 설정하여, 초록으로 인식되는 경우가 3 이상일 때, 차량이 출발하도록 설정했다.



<br/>


# 🤔 느낀점 및 개선하고 싶은 점
### 좋았던 점
- 곡률에 따라 모형차의 부드럽게 달릴 수 있는 최적의 설정 값을 지정할 수 있게 되었다.
  
-  리눅스 터미널 환경에 익숙해 졌다.
- HSV의 개념을 알게되었으며, Open CV 라이브러리 통해 색상 추출, 원근 변환, 화면 크기 조정을 할 수 있게 되었다.
### 아쉬웠던 점
- 새로운 알고리즘을 짜기 보다는, 기존 알고리즘을 유지하면서 적절한 설정값을 결정하는 것에 시간을 많이 투자한 것이 아쉽다.
  
- 장애물 회피 연습을 할 때, 25cm 이상 길이의 장애물 회피를 테스트 하지 않은 게 아쉽다.
   
- 대회 하루 전에 모터를 변경하여, 기존의 설정 환경과 다르게 실전 환경에서 주행한 것이 아쉽다.
### 개선하고 싶은 점
- 조향할 때, 오차값에 따라 조향이 비례하도록 비례상수를 사용하는 방법 대신 이를 선형적인 함수를 사용하여 다양한 곡률에서도 부드럽게 조행하도록 개선하고 싶다.
  
- pid 제어 대신 다른 제어방식을 적용해서 조향 기능을 구현해 보고 싶다.
  
- 차선을 점으로 인식하는 방벙 외에 면으로 인식하는 방법을 적용해보고 싶다.

<br/>

# 🎯 프로젝트의 발전 방향
- 실내 물류 전달 기능을 수행하는 로봇으로 발전할 수 있다. (비대면 전달 등)
  
- 실제 자율주행차량의 위험 요소를 미리 테스트 해 볼수 있다.
<br/>
