from django.db import models

import qrcode
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.conf import settings
# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

class MenuItem(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    price = models.FloatField(blank=True, null=True)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, null=False, blank=False,
                                 related_name='menu_items')
    is_active = models.BooleanField(default=True)
    media = models.ManyToManyField('Media', related_name='item_media')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

FILE_CHOICES = (
    ("Image", "Image"),
    ("Video", "Video"),
)

class Media(models.Model):
    type = models.CharField(max_length=10, choices=FILE_CHOICES, null=False, blank=False)
    file = models.FileField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    
class QRCode(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    qr_code_id = models.CharField(max_length=16, blank=True)
    qr_code = models.ImageField(null=False, blank=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def generate_qrcode(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=12,
            border=0,
        )
        code = settings.QR_CODE_URL + "/" + self.qr_code_id
        qr.add_data(code)
        qr.make(fit=True)
        img = qr.make_image()

        buffer = io.BytesIO()
        img.save(buffer)
        filename = 'qr_code-%s.png' % (self.id)
        filebuffer = InMemoryUploadedFile(
            buffer, None, filename, 'image/png', buffer.getbuffer().nbytes, None)
        self.qr_code.save(filename, filebuffer)