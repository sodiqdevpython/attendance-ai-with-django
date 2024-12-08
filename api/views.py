from django.shortcuts import render, get_object_or_404
from datetime import date
from django.views import View
from .models import User, Attendense, Late
from datetime import timedelta, time, datetime
from django.utils.timezone import now


#! API
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import AttendenseSerializer
#! /API


class DashboardView(View):
    def get(self, request):
        today = now().date()

        # Oxirgi 7 kun uchun statistik ma'lumotlarni olish
        last_7_days = [today - timedelta(days=i) for i in range(7)]
        daily_stats = [
            {
                "date": day,
                "in_count": Attendense.objects.filter(created__date=day, direction="Keldi").count(),
                "out_count": Attendense.objects.filter(created__date=day, direction="Ketdi").count(),
                "late_count": Late.objects.filter(created__date=day).count(),
            }
            for day in reversed(last_7_days)
        ]

        # Umumiy statistikalar
        total_users = User.objects.count()
        today_in_users = Attendense.objects.filter(created__date=today, direction="Keldi").count()
        today_out_users = Attendense.objects.filter(created__date=today, direction="Ketdi").count()
        late_users = Late.objects.filter(created__date=today).count()

        # Bugungi kun uchun jadval
        today_attendances = Attendense.objects.filter(created__date=today)
        daily_attendance_data = []
        for attendance in today_attendances.filter(direction="Keldi").select_related("user"):
            user = attendance.user
            departed = today_attendances.filter(user=user, direction="Ketdi").first()

            daily_attendance_data.append({
                "user": user,
                "arrived_time": attendance.created,
                "departed_time": departed.created if departed else None,
            })

        context = {
            "total_users": total_users,
            "today_in_users": today_in_users,
            "today_out_users": today_out_users,
            "late_users": late_users,
            "daily_stats": daily_stats,
            "daily_attendance_data": daily_attendance_data
        }

        return render(request, "dashboard.html", context)

class UsersView(View):
    def get(self, request):
        users = User.objects.all().order_by('name')
        context = {
            'users': users
        }
        return render(request, 'users-list.html', context)

class UserDetail(View):
    def get(self, request, id):
        user = get_object_or_404(User, id=id)
        attendense_records = Attendense.objects.filter(user=user)
        late_records = Late.objects.filter(user=user)
        context = {
            'user': user,
            'attendense_records': attendense_records,
            'late_records': late_records,
        }
        return render(request, 'user-detail.html', context)
    

class AttendenseCreateView(APIView):
    def post(self, request, *args, **kwargs):
        user_name = request.data.get("user_name")
        direction = request.data.get("direction")

        # Foydalanuvchi ism va familiyani ajratib olish
        try:
            first_name, last_name = user_name.split(" ", 1)
        except ValueError:
            return Response(
                {"error": "Foydalanuvchi ismi va familiyasini to'liq kiriting (Masalan, Vladimir Putin)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Foydalanuvchini ism va familiya bo'yicha topish
        user = get_object_or_404(User, name=first_name, last_name=last_name)

        # Bugungi sana
        today = datetime.now().date()

        # Tekshirish: Foydalanuvchi uchun bugungi kun uchun "Keldi" yoki "Ketdi" yozuvi mavjudmi
        if Attendense.objects.filter(user=user, created__date=today, direction=direction).exists():
            return Response(
                {"error": f"Foydalanuvchi uchun bugungi '{direction}' yozuvi allaqachon mavjud."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Hozirgi vaqtni olish
        current_time = datetime.now().time()
        late_time = time(9, 0)  # Ertalab 9:00 va undan keyingi vaqtni tekshirish uchun

        # Agar kirayotgan vaqt 9:00 yoki undan keyin bo'lsa, kechikish yozuvi yaratish
        if current_time >= late_time and direction == 'Keldi':
            Late.objects.create(user=user)

        # Yangi Attendense yozuvi yaratish
        data = {"user": user.id, "direction": direction}
        serializer = AttendenseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)