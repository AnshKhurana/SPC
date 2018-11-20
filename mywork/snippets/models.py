from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
class Snippet(models.Model):
    owner=models.ForeignKey('auth.User',\
                            related_name='snippets',\
                            on_delete=models.CASCADE)
    # highlighted=models.TextField()
    stext=models.CharField(max_length=50)
    scom=models.CharField(max_length=50)
    class Meta:
        ordering=('stext',)




# Create your models here.
