import cv2
import mediapipe as mp
import math
import time
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import pythoncom


# MediaPipe el tespiti için gerekli sınıfı yaratma
mp_hands = mp.solutions.hands.Hands(static_image_mode=False, max_num_hands=1, min_detection_confidence=0.5)

# Anlık Görüntü almak için kaynak belirt.
cap = cv2.VideoCapture(0)

# Başlangıç uzaklığı belirle
initial_distance = None

# Ses kontrolü için gerekli değişkenler
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, pythoncom.CLSCTX_ALL, None)
volume = interface.QueryInterface(IAudioEndpointVolume)

# FPS değerini hesaplamak için başlangıç zamanını al
start_time = time.time()
frame_count = 0

while True:
    # Kameradan bir frame al
    ret, frame = cap.read()

    # MediaPipe'e girdi olarak vermek üzere frame'i BGR2RGB formatına dönüştürme
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Frame'i MediaPipe'e göndererek el tespiti yapma
    results = mp_hands.process(rgb_frame)

    # El tespiti sonuçlarını alıp noktaları ve çizgileri çizme
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Noktaları çizme
            for i in range(21):
                landmark = hand_landmarks.landmark[i]
                x = int(landmark.x * frame.shape[1])
                y = int(landmark.y * frame.shape[0])
                cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

            # Başparmak ile işaret parmağı arasına çizgi çizme
            thumb_tip = hand_landmarks.landmark[4]
            index_finger_tip = hand_landmarks.landmark[8]
            x0 = int(thumb_tip.x * frame.shape[1])
            y0 = int(thumb_tip.y * frame.shape[0])
            x1 = int(index_finger_tip.x * frame.shape[1])
            y1 = int(index_finger_tip.y * frame.shape[0])
            cv2.line(frame, (x0, y0), (x1, y1), (255, 0, 0), 2)

            # Başparmak ile işaret parmağı arasındaki uzaklığı hesaplama
            distance = math.dist([x0, y0], [x1, y1])

            if initial_distance is None:
                initial_distance = distance

            # İşaret parmağının başparmağa göre açılma yüzdesini hesaplama
            percentage = min(max(int((distance / initial_distance) * 100), 0), 100)

            # Ses seviyesini ayarla
            volume_range = volume.GetVolumeRange()  # Ses seviyesi aralığını al
            min_volume = volume_range[0]
            max_volume = volume_range[1]  # maksimum ses seviyesi

            # Yeni ses seviyesini hesapla
            new_volume = min_volume + (max_volume - min_volume) * (percentage / 100)
            volume.SetMasterVolumeLevel(new_volume, None)

            # İlerleme çubuğunu çizme
            bar_width = 20
            bar_max_height = frame.shape[0] - 40  # Çubuğun dolacağı maksimum yükseklik (üstten 20 piksel boşluk bırakıyoruz)
            bar_height = int(bar_max_height * (percentage / 100))
            bar_x = 10
            bar_y = frame.shape[0] - 40 - bar_height  # Çubuğun yukarıdan başlayacağı yükseklik

            # Dolacak alana dair dikdörtgeni çizme
            cv2.rectangle(frame, (bar_x, frame.shape[0] - 40), (bar_x + bar_width, frame.shape[0] - 40 - bar_max_height), (255, 255, 255), 2)

            # İlerleme çubuğunun dolu kısmını çizme
            cv2.rectangle(frame, (bar_x, bar_y + bar_height), (bar_x + bar_width, bar_y), (0, 0, 255), -1)

            # Yüzdelik değeri ekrana yazdırma
            cv2.putText(frame, f"Volume: {percentage}%", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # FPS değerini hesapla
    frame_count += 1
    elapsed_time = time.time() - start_time
    fps = frame_count / elapsed_time

    # FPS değerini ekrana yazdırma
    cv2.putText(frame, f"FPS: {int(fps)}", (50, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

    # Frame'i görüntüle
    cv2.imshow('Video', frame)

    # Çıkış için 'q' tuşuna basıldığını kontrol eder
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Kaynakları serbest bırak
cap.release()
cv2.destroyAllWindows()
