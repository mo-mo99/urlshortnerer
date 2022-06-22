from django.db import models

class Url(models.Model):
    origin_url = models.CharField(max_length=1000, blank=False, null=False)
    salt = models.BinaryField(blank=False, null=False)
    hash_salted_url = models.BinaryField(blank=False, null=False)
    visited = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.origin_url