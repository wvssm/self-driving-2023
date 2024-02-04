# 🚗 2023_Self_Driving

> 지능형자동차부품진흥원에서 주최한 『[2023 대구모형전기자율주행차 경진대회](http://www.kiapi.or.kr/pages/board/view.php?board_sid=1&data_sid=723&page_num=2&skey=&sval=)』에 참가하여 OpenCV를 이용해 모형 자동차의 주행 기능을 개발 과정을 기록한 저장소입니다.
<br/>

# 👐 소개
- ## 주제 : 자율주행 모형차를 이용한 미션 수행 및 경기장 주행
-  제공된 코드를 수정하여 모형차가 **"직선 및 곡선 주행"**, **"장애물 회피"**, **"오르막 주행"**, **"신호등 인식"** 을 수행할 수 있도록 한다.
- 차량의 컨셉을 정하고, 그에 맞는 차체를 제작하여 주행한다.
- 가장 빠른 시간 내에 경기장을 주행하는 팀이 수상한다.
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
|:-----|:-----|:-----|
|정보컴퓨터공학부|기계공학부|산업공학과|
|• 차선 인식 기능 개선 (Python, OpenCV)<br>• 장애물 회피 기능 개선 (Python, LiDAR)<br>• 신호등 인식 기능 개선 (Python, OpenCV)<br>| • 차체 모델링(Creo CAD)<br> • 차체 설계파일(.step) 제작<br> • 차량 주행 기능 개선 방안 제안<br> • 차량 컨셉 제안<br>| • 차체 모형 디자인<br> • 주행 연습 도로 제작<br> • 차량 주행 기능 개선 방안 제안<br> • 차량 주행 영상 촬영 및 피드백<br>|
<br/>

# 🚩대회 진행 과정
_대회 과정을 "[블로그](https://wvssm.tistory.com/category/%F0%9F%93%81Project/2023%20%EB%8C%80%EA%B5%AC%EB%AA%A8%ED%98%95%EC%A0%84%EA%B8%B0%EC%9E%90%EC%9C%A8%EC%A3%BC%ED%96%89%EC%B0%A8%EA%B2%BD%EC%A7%84%EB%8C%80%ED%9A%8C)"에 기록해두었습니다._
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
> - 경진 대회 : 2023.10.21(토) - 30팀 중 7위
> <br>
> #### 수상
> - 
> <br><br>


# 🚨 문제 발생과 해결 방법
### 문제
- 이전 1주차 연습에서는 모형차가 라인트레싱을 정상적으로 수행하였는데, 장소를 바꾸어 2주차 연습을 진행할 때는 차량이 라인트레이싱을 정상적으로 수행하지 못했다.
### 해결
- 기존의 검출 화면을 확장하여 차선이 차량의 중심에서 멀리 떨어져 있더라도 이를 인식 할 수 있도록 도왔다.
- 오차값에 비례해서 차량의 방향이 꺾이는데, 비례 상수 값을 키워, 차량이 동일 오차값에 대해 차량이 각도를 좀 더 많이 꺾도록 작성함. 
  
### 문제
- 직선에서는 속도가 빠르나 곡선에서는 속도가 느려짐
### 해결
- 직선 주행과 곡선 주행을 분리하여 각각의 속도 설정
- 곡선 주행시, 오차값에 따라 속도가 변화되는데 기본 속도가 너무 높다면, 각 순간마다 속도 값의 변화가 커져서 버퍼링이 걸려 오히려 차량이 삐걱돼 속도가 느려짐


### 문제
장애물 회피시 차량이 휘청거림
### 해결
1) 라이다 범위 및 발사하는 전자파 개수 수정
2) 오차값에 대한 차량의 꺾임(ang_z)
- 라이다 발사 범위를 넓히니 장애물 지나는 동안 장애물을 지속적으로 인식할 수 있게 되었다.
- 또한 기존에 뚝뚝 끊기는 주행은 주행 라인은 따라가야하고, 오차값만큼 또 바퀴가 꺾여줘야하고 이 두 가지가 충돌하여 뚝뚝 끊기는 주행을 만든 것이다.

### 문제
주행중에 장애물도 없는데 차량이 삐끗된다.

### 해결
물체 인식 거리를 크게 지정해놓아서 멀리 있는 책상을 인식해서 차량이 비틀된 것이다.



<br/>


# 🤔 느낀점 및 개선하고 싶은 점
### 좋았던 점
### 아쉬웠던 점
### 개선하고 싶은 점
<br/>

# 🎯 프로젝트의 발전 방향
<br/>
