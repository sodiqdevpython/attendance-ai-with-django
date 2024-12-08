from django.db.models import TextChoices

class AttendType(TextChoices):
    In = "Keldi", "Keldi"
    Out = "Ketdi", "Ketdi"