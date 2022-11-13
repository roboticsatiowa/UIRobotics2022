import cv2


class VideoFeed:

    def __init__(self):
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            raise IOError("Cannot open webcam")

    def get_frame(self):
        ret, frame = self.cap.read()
        frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
        return frame


def start_display():
    feed = VideoFeed()
    while 1:
        cv2.imshow('Video feed', feed.get_frame())

        c = cv2.waitKey(1)
        if c == 27:
            break

    feed.cap.release()
    feed.cap.destroyAllWindows()


if __name__ == '__main__':
    start_display()
