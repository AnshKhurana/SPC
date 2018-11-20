from django.db import models

# Create your models here.


class FileRecord(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=200, blank=True, default='')
    file_data = models.TextField(editable=True, default=b'')
    md5sum = models.CharField(max_length=40, default='')
    file_type = models.CharField(max_length=200, default='')
    owner = models.ForeignKey('auth.User', related_name='files', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):

        super(FileRecord, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)
        unique_together = ('owner', 'file_name',)