__author__ = 'Bertrand'
from django.db import models
from mezzanine.blog.models import BlogPost
from image_cropping import ImageRatioField

# le modèle qui va nous permettre de gérer le contenu de notre home page
class GeneralPost(BlogPost):
    sub_title = models.CharField(max_length=150)
    image_post = models.ImageField(blank=True, upload_to='uploaded_images')
    cropping = ImageRatioField('image_post', '180x180')
