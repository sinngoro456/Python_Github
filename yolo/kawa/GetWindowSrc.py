import ctypes
from ctypes.wintypes import HWND, DWORD, RECT
from ahk import AHK
import mss.tools
import cv2


def GetTitle(window_title):
    ahk = AHK()
    wins = list(ahk.windows())
    titles = [win.title for win in wins]
    for text in titles:
        if window_title in text:
            return text


def GetWindowRectFromName(TargetWindowTitle):
    TargetWindowHandle = ctypes.windll.user32.FindWindowW(0, TargetWindowTitle)
    Rectangle = ctypes.wintypes.RECT()
    ctypes.windll.user32.GetWindowRect(TargetWindowHandle, ctypes.pointer(Rectangle))
    return (Rectangle.left, Rectangle.top, Rectangle.right, Rectangle.bottom)


def SCT(bbox):
    with mss.mss() as sct:
        img = sct.grab(bbox)
    return img


def FaceDetection(img):
    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    face_rects = face_cascade.detectMultiScale(img)
    (face_x, face_y, w, h) = tuple(face_rects[0])
    track_window = (face_x, face_y, w, h)

    roi = img[face_y : face_y + h, face_x : face_x + w]
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
    cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
    term_crit = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    dst = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    rect, track_window = cv2.meanShift(dst, track_window, term_crit)

    return face_rects, track_window


folder_path = r"C:\Users\sinng\Pictures\Screenshots"
file_name = r"\src"


def main(window_title="YouTube"):

    TargetWindowTitle = GetTitle(window_title)

    n = 0
    while True:
        n = n + 1
        try:
            bbox = GetWindowRectFromName(TargetWindowTitle)

            output = folder_path + file_name + str(n) + r".png"
            img = SCT(bbox)
            mss.tools.to_png(img.rgb, img.size, output=output)
            print(output)
        except:
            continue


main()
