from django.shortcuts import render
from .models import Detection
from .serializers import DetectionSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt  # CSRF 보안 임시 해제
from django.utils.decorators import method_decorator
from .stringToRGB import stringToRGB
from django.http import JsonResponse
import os
import cv2
import numpy as np
from PIL import Image
from django.conf import settings
from datetime import datetime
import pygame
from django.views import View
from django.utils import timezone
import imutils
import dlib
from mlxtend.image import extract_face_landmarks
import warnings
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
from .analyze import ImageAnalyzer
from PIL import Image

face_landmarks = os.path.abspath('static/shape_predictor_68_face_landmarks.dat')

# Create your views here.
class DetectionViewSet(viewsets.ModelViewSet):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    def get(self, request):
        dummy = Detection.objects.all()
        serializer = DetectionSerializer(dummy, many=True)
        return Response(serializer.data)
    
@method_decorator(csrf_exempt, name='dispatch')
class LatestDetectionView(View):
    queryset = Detection.objects.all()
    serializer_class = DetectionSerializer

    def get(self, request):
        latest_detection = Detection.objects.latest('start_time')
        serializer = DetectionSerializer(latest_detection)
        return JsonResponse(serializer.data)

def downsampling(img):
    g_down = []
    g_down.append(img)

    for i in range(3):
        tmp = cv2.pyrDown(img)
        g_down.append(tmp)
        img = tmp

    cv2.waitKey(0)
    cv2.destroyAllWindows()

    return g_down[1]

@method_decorator(csrf_exempt, name='dispatch')
def upload_image(request):
    if request.method == 'POST':
        image_url = request.POST.get('data') #이미지 가져오기
        person_result = request.POST.get('result') #사람 있는지없는지 유무
        print(person_result)
        rgb = stringToRGB(image_url.split(',')[1])
        rgb.save("static/image.jpg")

        image = "static/image.jpg"
        image_list = []

        if image.endswith(".jpg"):
            image_path = os.path.join(image)
            try:
                # 이미지 파일 열기
                img = Image.open(image_path)
                # 이미지 리스트에 추가
                image_list.append(img)
            except Exception as e:
                # 이미지 파일 열기에 실패한 경우 예외 처리
                print(f"Failed to open image: {image_path}\nError: {str(e)}")

        image_np = cv2.cvtColor(np.array(image_list[0]), cv2.COLOR_RGB2BGR)
        downsample_face = downsampling(image_np)
        
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(face_landmarks)
        image = imutils.resize(downsample_face, width=500)
        landmarks = extract_face_landmarks(image)

        fig = plt.figure(figsize=(15, 5))
        ax = fig.add_subplot(1, 3, 2)
        ax.scatter(landmarks[:, 0], -landmarks[:, 1], alpha=0.8)

        # 결과 이미지 파일 경로
        output_file = "static/image1.jpg"

        fig.savefig(output_file)
        plt.close(fig)

        image = cv2.imread("static/image1.jpg")

        x,y = 590, 50
        w,h = 370, 400

        # 이미지 자르기
        cropped_image = image[y:y+h, x:x+w]
        # 저장할 파일 경로 생성
        output_path = "static/image2.jpg"
        # 이미지 저장
        cv2.imwrite(output_path, cropped_image)

        # 랜드마크 이미지로 변환하는 파일 만들고
        # 그 파일 안에서 모델 호출해서 분석까지 마치고
        # 여기서는 분석 마친 결과만 출력해서 사용할 수 있도록 하기.
        analyzer = ImageAnalyzer()
        predicted_class = analyzer.analyze_image(output_path)

        # gaze_analyzer = GazeAnalyzer()
        # result = gaze_analyzer.analyze("static/image.jpg")

        # active detection이 있으면
        active_detection = Detection.objects.filter(end_time__isnull=True).latest('start_time')
        if not active_detection:
            # active detection 없으면 create a new one
            detection = Detection.objects.create()
        else:
            detection = active_detection


        if person_result == "person":
            if predicted_class == "happy":
                print("happy")
                detection.happy += 1
            elif predicted_class == "neutral":
                print("neutral")
                detection.neutral += 1
            else:
                print("sad")
                detection.sad += 1
        else:
            print("detectionError")
            detection.detectionError += 1

        # if detection.happy >= 5:
        #     detection.emotion == "happy"
        #     detection.happy == 0
        #     detection.sad == 0
        #     detection.neutral == 0

        # elif detection.sad >= 5:
        #     detection.emotion == "sad"
        #     detection.happy == 0
        #     detection.sad == 0
        #     detection.neutral == 0

        # elif detection.neutral >= 5:
        #     detection.emotion == "neutral"
        #     detection.happy == 0
        #     detection.sad == 0
        #     detection.neutral == 0

        # else:
        #     detection.emotion == "collecting"
        
        detection.update_emotion()
        detection.save()

        if os.path.exists("static/image.jpg"):
            os.remove("static/image.jpg")

        if os.path.exists("static/image1.jpg"):
            os.remove("static/image1.jpg")

        if os.path.exists("static/image2.jpg"):
            os.remove("static/image2.jpg")
        

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'POST error.'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
def end_detection(request):
    if request.method == 'POST':
        # Check if there is an active detection
        active_detection = Detection.objects.filter(end_time__isnull=True).latest('start_time')

        if active_detection:
            # Set the end time of the active detection
            active_detection.end_time = timezone.now()
            active_detection.save()
        else:
            # Create a new detection object
            detection = Detection.objects.create(start_time=timezone.now())
            detection.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': 'POST error.'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
def start_detection(request):
    if request.method == 'POST':
        
        # Create a new detection object
        detection = Detection.objects.create(start_time=timezone.now())
        detection.save()

        return JsonResponse({'message': 'Detection started'})
    else:
        return JsonResponse({'message': 'POST error.'}, status=400)
