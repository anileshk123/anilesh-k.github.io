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

    def media_image(self):
        #host_id = socket.gethostbyname(socket.gethostname())
        ret = ''
        for media_file in self.media.all()[:1]:
            ret = media_file.file.url
        return ret

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

class Order(models.Model):
    qr_code = models.ForeignKey('QRCode', on_delete=models.CASCADE, null=False, blank=False, related_name='orders')
    total_quantity = models.IntegerField(default=1)
    total = models.FloatField(blank=True, null=True)
    suggestion = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, default="Pending")
    is_active = models.BooleanField(default=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(null=True, blank=True)

class OrderDetails(models.Model):
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_master')
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, null=False, blank=False, related_name='orders_menu')
    quantity = models.IntegerField(default=1)
    unit_price = models.FloatField(blank=True, null=True)
    total = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=10, default="Pending")
    is_active = models.BooleanField(default=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    date_confirmed = models.DateTimeField(null=True,blank=True)


class Cart(models.Model):
    qr_code = models.ForeignKey('QRCode', on_delete=models.CASCADE, related_name='cart_qrcode')
    menu_item = models.ForeignKey('MenuItem', on_delete=models.CASCADE, related_name='cart_menu')
    quantity = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now_add=True)