from django.db import models

# Create your models here.


class Detection(models.Model):
    happy = models.IntegerField(default=0)
    sad = models.IntegerField(default=0)
    neutral = models.IntegerField(default=0)
    detectionError = models.IntegerField(default=0)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    emotion = models.CharField(max_length=5, default="")

    def update_emotion(self):
        if self.happy >= 2 and self.happy <= 3:
            self.emotion = "행복"
            self.save()
        elif self.happy > 3:
            self.emotion = "행복"
            self.happy = 0
            self.sad = 0
            self.neutral = 0
            self.save()
        elif self.sad >= 2 and self.sad <= 3:
            self.emotion = "슬픔"
            self.save()
        elif self.sad > 3:
            self.emotion = "슬픔"
            self.happy = 0
            self.sad = 0
            self.neutral = 0
            self.save()
        elif self.neutral >= 2 and self.neutral <= 3:
            self.emotion = "중립"
            self.save()
        elif self.neutral > 3:
            self.emotion = "중립"
            self.happy = 0
            self.sad = 0
            self.neutral = 0
            self.save()
        else:
            self.emotion = ""
            self.save()

