from .models import Code,Story
from .utils import generate_audio,generate_picture
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver



#this signal will be sent when a user is created to create a code for the user
@receiver(post_save, sender=User)
def post_save_create_code(sender, instance, created, **kwargs):
    if created:
        Code.objects.create(user=instance)

#these are the signals that will be sent when a story is created and saved to generate the audio and assign a random picture to a story
#⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇⬇⬇⬇⬇⬇⬇⬇⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️⬇️

@receiver(post_save, sender=Story)
def generate_audio_for_story(sender, instance, created, **kwargs):
    if not instance.audio_file and created:
        # Generate audio for the new story
        generate_audio(instance)

@receiver(post_save, sender=Story)
def generate_picture_for_story(sender, instance, created, **kwargs):
    if not instance.picture :
        print("Generating picture for story")
        # Generate picture for the new story
        generate_picture(instance)