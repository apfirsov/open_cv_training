import cv2

from datetime import datetime
import random
from collections import deque


class PlateDetector:
    color = (0, 255, 0)
    scale_color = (255, 0, 0)
    thickness = 2
    scaleFactor = 1.05
    minNeighbors = 3

    def __init__(self, path_in, path_out, cascade_path):
        self.path_in = path_in
        self.path_out = path_out
        self.queue = deque(maxlen=64)
        self.start = None
        self.model = cv2.CascadeClassifier(cascade_path)
        self.meta_areas = [
            ((1060, 580), (1200, 670)),
        ]
        self.frames = 0
        self.hits = 0

    def detect_plate(self, frame):
        grey_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        grey_img = cv2.equalizeHist(grey_img)

        for up_left, bottom_right in self.meta_areas:
            cv2.rectangle(
                grey_img, up_left, bottom_right, (0, 0, 0), cv2.FILLED
            )

        results = self.model.detectMultiScale(
            grey_img, self.scaleFactor, self.minNeighbors
        )
        B, G, R = 0, 255, 0
        hit = 0
        for (x, y, w, h) in results:
            if x + w <= 740 and y >= 360: # Вынести в настройки detect_area
                cv2.rectangle(
                    frame, (x, y), (x + w, y + h), (B, G, R), self.thickness
                )
                # if len(results) == 1:
                hit = 1
                B, G, R = B + 70, G + 50, R + 25
                if B > 255: B = 0
                if G > 255: G = 0
                if R > 255: R = 0

        self.hits = self.hits + hit

        self.frames += 1
        self.update_chart()

    def update_chart(self):
        now = datetime.now()
        if self.start is None:
            self.start = now
            return

        delta_time = now - self.start

        if self.frames == 0:
            percent = 100
        else:
            percent = int(self.hits / self.frames * 100)

        # print(self.frames, self.hits, percent, delta_time.seconds)
        self.queue.append((delta_time.seconds, percent))

    def draw_chart(self, frame):
            scale_y = 170 # Динамический расчет области построения и шкалы
            #Рамка
            cv2.rectangle(
                frame, (0, 0), (320, 180), self.color, thickness=1
            )
            #Шкала
            cv2.line(
                frame, (0, scale_y), (319, scale_y), self.scale_color, thickness=1
            )
            point_one = None
            x = 0
            last_second = 0
            percent = 0
            for second, percent in self.queue:
                x += 5
                y = scale_y - percent
                point_two = (x, y)
                if point_one is not None:
                    # График
                    cv2.line(
                        frame, point_one, point_two,self.color,self.thickness
                    )

                    if last_second != second and second % 5 == 0:
                        # Шкала
                        cv2.line(
                            frame, (x, scale_y - 10), (x, scale_y), self.scale_color, thickness=1
                        )
                        cv2.putText(
                            frame, str(second), (x, scale_y), cv2.FONT_HERSHEY_PLAIN, 1, self.scale_color, 2
                        )
                        last_second = second

                point_one = point_two

            cv2.putText(
                frame, f'{percent}%', (290, 30), cv2.FONT_HERSHEY_PLAIN, 3,
                self.color, 1
            )

    def run(self):
        cap = cv2.VideoCapture(self.path_in)
        if not cap.isOpened():
            print("Cannot open")
            exit()

        print('start...', datetime.now())
        fourcc = cv2.VideoWriter_fourcc(*'XVID') #MP4
        out = cv2.VideoWriter(self.path_out, fourcc, 20.0, (1280,  720))

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                print("finish.", datetime.now())
                break

            self.detect_plate(frame)
            self.draw_chart(frame)
            out.write(frame)

        cap.release()
        out.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    path_in = 'videos/video_1.mp4'
    path_out = 'videos/output17.avi'
    cascade_path = 'haarcascade_russian_plate_number.xml'

    detector = PlateDetector(path_in, path_out, cascade_path)
    detector.run()
