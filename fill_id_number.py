import cv2
import matplotlib.pyplot as plt
import numpy as np


class fillID:
    def __init__(self,students):
        self.global_cache = dict()
        self.studentsPath = students



    def get_min_xy(self, img):
        min_x, max_y = 0, 0
        for x in range(img.shape[1]):
            if np.any(img[:, x] == 0):
                min_x = x
                break
        for y in range(img.shape[0] - 1, 0, -1):
            if np.any(img[y, :] == 0):
                max_y = y
                break
        return min_x, max_y

    def list_bars(self, img):
        black = False
        y_idx = []
        for y in range(img.shape[0]):
            if img[y, 0] == 0 and not black:
                y_idx.append(y)
                black = True
            elif img[y, 0] > 0 and black:
                y_idx.append(y - 1)
                black = False

        yy_idx = []
        for i in range(0, len(y_idx), 2):
            yy_idx.append((y_idx[i], y_idx[i + 1]))

        x_idx = []
        black = False
        for x in range(img.shape[1]):
            if img[-1, x] == 0 and not black:
                x_idx.append(x)
                black = True
            elif img[-1, x] > 0 and black:
                x_idx.append(x - 1)
                black = False

        xx_idx = []
        for i in range(0, len(x_idx), 2):
            xx_idx.append((x_idx[i], x_idx[i + 1]))
        return yy_idx, xx_idx

    def calculate_angle(self, img, x_bars):
        # to calculate the angle
        bar_1 = x_bars[0]
        bar_2 = x_bars[~0]
        y_offset = abs(bar_1[0] - bar_2[1])

        y1 = int((bar_1[0] + bar_1[1]) / 2)
        x1 = 0
        for x1 in range(img.shape[1]):
            if img[y1, x1] == 0:
                break
        y2 = int((bar_2[0] + bar_2[1]) / 2)
        x2 = 0
        for x2 in range(img.shape[1]):
            if img[y2, x2] == 0:
                break
        t = np.arctan(abs(x1 - x2) / y_offset)
        t_deg = np.degrees(t)
        self.global_cache['angle'] = t_deg
        print(f'Image is rotated by {t_deg} degrees')
        return t_deg

    def rotate_image(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        if image.ndim == 3:
            fill = (255, 255, 255)
        else:
            fill = 255
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=fill)
        return result

    def process_image(self, file):
        img = cv2.imread(file)
        if img.shape[0] > img.shape[1]:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.bilateralFilter(gray, 11, 17, 17)
        thresh: np.ndarray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

        min_x, max_y = self.get_min_xy(thresh)
        img_cropped = thresh[:max_y - 13, min_x + 10:]

        y_bars, x_bars = self.list_bars(img_cropped)
        angle = self.calculate_angle(thresh, y_bars)

        img_rot = self.rotate_image(thresh, -angle)
        min_x, max_y = self.get_min_xy(img_rot)
        img_cropped = img_rot[:max_y - 5, min_x + 5:]
        plt.imshow(img_cropped, cmap='gray')
        plt.show()
        self.global_cache['x_off'] = min_x + 5
        self.global_cache['y_off'] = max_y + 5

        y_bars, x_bars = self.list_bars(img_cropped)
        return img_cropped, y_bars, x_bars

    # def get_ans(sself,img, chapter_bars, question_bars, chapter, question):
    #     if chapter > 5:
    #         chapter -= 3
    #         question += 30
    #     ans = np.zeros((4,))
    #     for i in range(1, 5):
    #         y1, y2 = chapter_bars[5 * (chapter - 1) + i]
    #         x1, x2 = question_bars[question - 1]
    #         ans[i - 1] = np.sum(img[y1:y2, x1:x2])
    #     if np.all(ans > ans.max() / 2):
    #         return None
    #     return np.argmin(ans)
    #

    def fill_id(self, img, id_bars, question_bars, id_number):
        t = self.global_cache['angle']
        x_off = self.global_cache['x_off']
        ellipse_size = (5, 8)
        for i in range(len(id_number)):
            chap_bar = id_bars[i]
            ques_bar = question_bars[40 - (id_number[i] - '0')]
            center = (int(sum(ques_bar) / 2), int(sum(chap_bar) / 2),)
        # center = rotate_point(center[0] + 3, center[1] +4, t)
        # center = center[0] - 3, center[1] - 4
            center = center[0] + x_off, center[1]
            cv2.ellipse(img, center, ellipse_size, 0, 0, 360, (0, 255, 0), -1)

    def rotate_point(self, x, y, t):
        t = np.radians(t)
        xx = x * np.cos(t) - y * np.sin(t)
        yy = x * np.sin(t) + y * np.cos(t)
        return int(xx), int(yy)

    def findIDPos(self, y_axis):
        diff = y_axis[1][0] - y_axis[0][1]
        h = y_axis[0][1] - y_axis[0][0]
        end = y_axis[0][1]
        start = y_axis[0][0]
        y_arr = []
        for i in range(9):
            y_arr.append((start, end))
            end = start - diff
            start = end - h
        return y_arr

    def doAction(self, path, id_number):
        img, chapter_bars, question_bars = self.process_image(path)
        res = self.rotate_image(cv2.imread(path), -self.global_cache['angle'])
        y_arr = self.findIDPos(chapter_bars)
        self.fill_id(img, y_arr, question_bars,id_number)
        cv2.imwrite('detected.png', res)
        plt.imshow(res, cmap='gray')
        plt.show()

if __name__ == '__main__':
    a = fillID("")
    a.doAction('image.jpeg','208179804')

