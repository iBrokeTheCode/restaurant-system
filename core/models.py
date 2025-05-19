from django.db import models


class BusinessInfo(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, default='')
    opening_days = models.CharField(max_length=255)
    opening_hours = models.CharField(max_length=255)
    facebook_link = models.URLField(blank=True, default='')
    instagram_link = models.URLField(blank=True, default='')
    tiktok_link = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Business Info'
        verbose_name_plural = 'Business Info'

    def save(self, *args, **kwargs):
        if not self.pk and BusinessInfo.objects.exists():
            raise ValueError('Only one BusinessInfo instance allowed.')
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name
