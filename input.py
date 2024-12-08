import cv2
from simple_facerec import SimpleFacerec
import requests

# API URL (Django'da qurilgan endpoint)
API_URL = "http://127.0.0.1:8000/api/attendense/"  # O'zingizning API endpointingiz

# Encode faces from a folder
sfr = SimpleFacerec()
sfr.load_encoding_images("images/images/")

# Load Camera
cap = cv2.VideoCapture(0)

counter = 0  # 'Unknown' ketma-ket nechta bo'lganini sanash uchun
prev_name = None  # Oldingi iteratsiyadagi ismni kuzatish uchun

while True:
    ret, frame = cap.read()

    # Detect Faces
    face_locations, face_names = sfr.detect_known_faces(frame)
    for face_loc, name in zip(face_locations, face_names):
        y1, x2, y2, x1 = face_loc[0], face_loc[1], face_loc[2], face_loc[3]
        name = name.replace("_", " ")

        # Begona bo'lsa, "Begona" deb yozadi
        if name == "Unknown":
            name = "Begona"
            counter = 0  # Hisoblagichni qayta boshlash
        else:
            if name == prev_name:
                counter += 1
                if counter == 7:  # Agar 7 marta aniqlansa
                    # API orqali POST request yuborish
                    print(name)
                    response = requests.post(API_URL, json={"user_name": name, "direction": "Keldi"})
                    print('7 marta ishlatildi')
                    if response.status_code == 201:
                        print(f"API orqali {name} ma'lumot yuborildi")
                    else:
                        print(f"API xatosi: {response.status_code}, {response.text}")
                    counter = 0  # Hisoblagichni qayta tiklash
            else:
                counter = 1  # Yangi ism aniqlansa, hisoblagichni qayta boshlash

        prev_name = name  # Oldingi ismni yangilash
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, name, (x1, y1 - 10), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2)

    cv2.imshow("Face Recognition", frame)

    key = cv2.waitKey(1)
    if key == 27:  # ESC tugmasi
        break

cap.release()
cv2.destroyAllWindows()
