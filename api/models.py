from django.db import models
from utils.choise import AttendType
from datetime import datetime
from django.core.validators import FileExtensionValidator

class WorkTypes(models.Model):
    number = models.FloatField()

    def __str__(self):
        return self.number
    
    class Meta:
        verbose_name = "Shtat birligi"
        verbose_name_plural = "Shtat birliglari"

class Position(models.Model):
    name = models.CharField(max_length=64, unique=True, help_text="Lavozim")

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Lavozim"
        verbose_name_plural = "Lavozimlar"

class User(models.Model):
    name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    image = models.ImageField(
        null=True,
        upload_to='images/',
        validators=[FileExtensionValidator(allowed_extensions=["png", "jpg"], message="Faqat png yoki jpg rasm yuklashingiz mumkin")]
    )
    position = models.ForeignKey(Position, on_delete=models.CASCADE)  # Lavozimi
    table_number = models.IntegerField(unique=True, null=True)  # Tabel raqami
    work_type = models.FloatField(null=True)  # Shtat birligi (stavka)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.last_name}"
    
    class Meta:
        verbose_name = "Xodim"
        verbose_name_plural = "Xodimlar"

class WorkDay(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='work_days')
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    hours_worked = models.FloatField()

    def save(self, *args, **kwargs):
        start = datetime.combine(self.date, self.start_time)
        end = datetime.combine(self.date, self.end_time)
        self.hours_worked = (end - start).total_seconds() / 3600
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user} - {self.date} - {self.hours_worked} soat"



class Attendense(models.Model):
    direction = models.CharField(max_length=5, choices=AttendType.choices, default=AttendType.In)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = "Davomat"
        verbose_name_plural = "Davomatlar"


class Late(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.user)
    
    class Meta:
        verbose_name = "Kechikish"
        verbose_name_plural = "Kechikishlar"