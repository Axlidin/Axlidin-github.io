from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(verbose_name="Ism", max_length=100)
    username = models.CharField(verbose_name="Telegram username", max_length=100, null=True)
    telegram_id = models.BigIntegerField(verbose_name='Telegram ID', unique=True, default=1)

    def __str__(self):
        return f"№{self.id} - {self.telegram_id} - {self.full_name}"

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    nomi = models.CharField(verbose_name="Mahsulot nomi", max_length=100)
    narhi = models.CharField(verbose_name="Mahsulot narhi", max_length=10)
    rasmi = models.CharField(verbose_name="Mahsulot rasmi", max_length=300)

    def __str__(self):
        return f"№{self.id}--{self.nomi}--{self.narhi}"