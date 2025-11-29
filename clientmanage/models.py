from django.db import models

# Create your models here.

class Client(models.Model):
    companyName = models.CharField(max_length=100)
    divisionName = models.CharField(max_length=100, blank=True, null=True)
    titleName = models.CharField(max_length=100, blank=True, null=True)
    sirName = models.CharField(max_length=100, blank=True, null=True)
    givenName = models.CharField(max_length=100, blank=True, null=True)
    postCode = models.CharField(max_length=20, blank=True, null=True)
    address1 = models.CharField(max_length=100, blank=True, null=True)
    address2 = models.CharField(max_length=100, blank=True, null=True)
    tel = models.CharField(max_length=100, blank=True, null=True)
    cell = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    email2 = models.EmailField(blank=True, null=True)
    note = models.CharField(max_length=200, blank=True, null=True)
    emailSend = models.BooleanField(default=False)
    emailSendStamp = models.DateTimeField(blank=True, null=True)
    eng = models.BooleanField(default=False)

    class Meta:
        ordering = ('companyName',)

    def __str__(self):
        return self.companyName