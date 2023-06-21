# Facial-Expression-Practice-System
안면 인식 / 근육 장애인을 위한 표정연습시스템 (2023-1 데이터분석캡스톤디자인)

## 연구 개요
국내 안면신경장애 환자수는 2020년 8만9천여명으로 10년새 42% 증가한 수치를 보였습니다. 이러한 안면 신경 장애 및 안면 인식 장애인의 빠른 사회적응을 위한 표정 연습 시스템을 제작하였습니다.

## 연구 주요 내용
표정 분석을 효율적으로 진행하고자 dlib의 shape_predictor_68_face_landmark를 통해 표정 데이터에서 얼굴의 랜드마크 좌표들을 추출하여 표정 분석을 진행하였습니다. 데이터는 neutral 2410장, happy 2327장, sad 2244장으로 총 6981장의 데이터를 사용하였습니다.

모델은 hyper parameter들을 변경해가며 ResNet18, MobileNetV2, EfficientNet-B0 총 3가지 모델을 통해 실험을 진행하였습니다. 최종적으로 아래와 같이 79.4% 의 test accuracy를 보인 EfficientNet-B0 모델을 사용하였습니다.
<br><br><img src = "https://github.com/jeongmin1217/Facial-Expression-Practice-System/assets/79658037/54337efc-4a46-4e4f-ab33-afcfb6ba58e8" width="70%" height="30%">
<br><br>
위의 모델을 서버에 담은 표정 연습 시스템을 개발하였습니다. 백엔드는 django로, 프론트앤드는 react로, 데이터베이스는 SQLite로 개발을 진행하였습니다.
<br><br><img src = "https://github.com/jeongmin1217/Facial-Expression-Practice-System/assets/79658037/64974ea1-74e8-4de2-9df4-8a7cf72aea96" width="70%" height="25%">

## 연구 수행 결과
<h5>메인 화면에서 표정 연습하러가기 버튼 클릭시 동작 예시</h5>
<img src = "https://github.com/jeongmin1217/Facial-Expression-Practice-System/assets/79658037/78eb4946-4e20-400a-8439-0f5447da37b6" width="30%" height="40%">
<img src = "https://github.com/jeongmin1217/Facial-Expression-Practice-System/assets/79658037/02d6af8f-ecdc-486d-9e75-59ea36600935" width="30%" height="40%">
<img src = "https://github.com/jeongmin1217/Facial-Expression-Practice-System/assets/79658037/82e48dc2-8cc7-43d8-9c56-a97bfda89792" width="30%" height="40%">
<img src = "https://github.com/jeongmin1217/Facial-Expression-Practice-System/assets/79658037/22030351-2431-4469-9ea9-8a13375dcfc8" width="40%" height="40%">
<img src = "https://github.com/jeongmin1217/Facial-Expression-Practice-System/assets/79658037/0486760a-07da-44ee-baf5-4420a268637d" width="40%" height="40%">
<img src = "https://github.com/jeongmin1217/LookAtMe/assets/79658037/aa79cbdc-a511-4dc0-a8b9-c3a09e461f33" width="25%" height="40%">
<img src = "https://github.com/jeongmin1217/LookAtMe/assets/79658037/ac40d15f-c36a-444d-adf4-883bc56beca9" width="25%" height="40%"> <br>

## Main Functions
1. Score data in calendar
2. Score changes in realtime
3. Stats of score which can give user feedback

## More To Do
1. Consider the case when user do many times of recording in one day
2. Provide the stats of score when you click the score of specific date on calendar
3. Consider more accurate & diverse factors about calculating the concentration score
