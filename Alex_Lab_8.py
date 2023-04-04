from PIL import Image
import cv2
import time

im = Image.open('variant-8.jpg')
width, height = im.size

im_crop = im.crop(((width - 400) // 2, (height - 400) // 2 + 1, (width + 400) // 2, (height + 400) // 2))
im_crop.show()

fl = Image.open('fly64.png')
fl = fl.resize((24, 24))
fl.save('fly24.png')

img = cv2.imread('fly24.png')

img_height, img_width, _ = img.shape

def video_processing():
    cap = cv2.VideoCapture(0)
    down_points = (640, 480)
    i = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, down_points, interpolation=cv2.INTER_LINEAR)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        ret, thresh = cv2.threshold(gray, 60, 120, cv2.THRESH_BINARY_INV)
        contours, hierarchy = cv2.findContours(thresh,
                                               cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            a = x + (w // 2)
            b = y + (h // 2)
            cv2.line(frame, (a, b + (h // 2)), (a, y), (0, 255, 255), 5)
            cv2.line(frame, (x, b), (a + (w // 2), b), (0, 255, 255), 5)

        if b - img_height // 2 > 32 and a - img_width // 2 > 32:
            frame[b - img_height // 2:b + img_height // 2, a - img_width // 2:a + img_width // 2] = img

        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        time.sleep(0.1)
        i += 1
    cap.release()


if __name__ == '__main__':
    # image_processing()
    video_processing()

cv2.waitKey(0)
cv2.destroyAllWindows()
