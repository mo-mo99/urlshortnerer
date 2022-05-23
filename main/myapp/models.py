from django.db import models

class Url(models.Model):
    text = models.CharField(max_length=1000, blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text