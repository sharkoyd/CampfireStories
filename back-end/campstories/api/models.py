from django.db import models
from django.contrib.auth.models import User
import random 
from django.utils import timezone
import json


# Create your models here.

class Code(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.code
    def save(self, *args, **kwargs):
        number_list=[x for x in range(10)]
        code_items=[]
        for i in range(4):
            num = random.choice(number_list)
            code_items.append(num)
        code_string = "".join(str(item) for item in code_items)
        self.code = code_string
        super(Code, self).save(*args, **kwargs)



class PendingCode(models.Model):
    code = models.CharField(max_length=6)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.code
    


class UserProfile(models.Model):
    PROFILE_IMAGES = [
        ('img1', 'Image 1'),
        ('img2', 'Image 2'),
        ('img3', 'Image 3'),
        ('img4', 'Image 4'),
    ]
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    STORY_TYPES = [
        ('action', 'Action'),
        ('adventure', 'Adventure'),
        ('comedy', 'Comedy'),
        ('fantasy', 'Fantasy'),
        ('mystery', 'Mystery'),
        ('science fiction', 'Science Fiction'),
        ('fairy tale', 'Fairy Tale'),
        ('animal', 'Animal'),
        ('educational', 'Educational'),
        ('historical', 'Historical'),
        # Add more story types as needed
    ]
    #action , adventure , comedy ,fantasy, mystery, science fiction,fairy tale , animal, educational or historical

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profiles')
    name = models.CharField(max_length=255)
    profileimg = models.CharField(default='img0',max_length=10, choices=PROFILE_IMAGES)
    age = models.PositiveIntegerField()
    scores = models.TextField(default=json.dumps({
        story_type: 0 for story_type, _ in STORY_TYPES
    }))  # Field to store story scores

    def get_scores(self):
        return json.loads(self.scores)

    def set_scores(self, scores):
        self.scores = json.dumps(scores)

    def __str__(self):
        return (self.name)
    




class Story(models.Model):
    LENGTH_CHOICES = (
        (1, '1 minute'),
        (2, '2 minutes'),
        (5, '5 minutes'),
        (10, '10 minutes'),
    )
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('A','Any'),
    ]
    STORY_TYPES = [
    ('action', 'Action'),
    ('adventure', 'Adventure'),
    ('comedy', 'Comedy'),
    ('fantasy', 'Fantasy'),
    ('mystery', 'Mystery'),
    ('science_fiction', 'Science Fiction'),
    ('fairy_tale', 'Fairy Tale'),
    ('animal', 'Animal'),
    ('educational', 'Educational'),
    ('historical', 'Historical'),
    # Add more story types as needed
    ]

    title = models.CharField(max_length=100)
    content = models.TextField()
    age_range = models.IntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    story_type = models.CharField(max_length=20, choices=STORY_TYPES)
    picture = models.ForeignKey('StoryPictureRand', blank=True ,on_delete=models.CASCADE, null=True)
    length_minutes = models.PositiveIntegerField(choices=LENGTH_CHOICES, default=1)
    validated = models.BooleanField(default=False)
    audio_file = models.FileField(default=None,upload_to='audio_files', blank=True, null=True)
    


    def __str__(self):
        return self.title   
    
class StoryPictureRand(models.Model):
    STORY_TYPES = [
    ('action', 'Action'),
    ('adventure', 'Adventure'),
    ('comedy', 'Comedy'),
    ('fantasy', 'Fantasy'),
    ('mystery', 'Mystery'),
    ('science_fiction', 'Science Fiction'),
    ('fairy_tale', 'Fairy Tale'),
    ('animal', 'Animal'),
    ('educational', 'Educational'),
    ('historical', 'Historical'),
    # Add more story types as needed
    ]

    genre = models.CharField(max_length=20, choices=STORY_TYPES)
    picture = models.ImageField(upload_to='story_pictures', blank=True, null=True)

    def __str__(self):
        return f'{self.genre} Picture'