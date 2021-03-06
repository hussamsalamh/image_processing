import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
from studentInfo import studentInfo, Chapter

TYPE_ERROR = 'Please check the type of each chapter \n'
ID_LENGTH = 8


numQuestion = {'M': 20,
               'A': 20,
               'E': 22,
               'P': 0}

"""

still need to make the calculation of the students 
and take the excel to mapping the id number to each student
to pass the name and the id to make an object of the student



class studentInfo 

need to make the calculation of the student 
based in the mistake in each chapter 

the mathmaitical grade 

"""


def get_min_xy(img):
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


# type of chapter will be like that
"""


"""


class imageProcessing:
    def __init__(self, path, folder, typeChapter):
        self.typeChapter = typeChapter  # this gonna be string EAMP -> english arabic math unmarked
        # type of chapter the length must be 8 else raising exception

        self.studentsImagePaper = []
        self.teacherImage = path
        self.folder = folder
        self.correctAnswer = []
        self.studentAnswer = []
        self.studentsResult = []
        self.global_cache = dict()

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
        # print(f'Image is rotated by {t_deg} degrees')
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

    def process_image(self, img, des=True):
        if des:
            img = cv2.imread(img)
        if img.shape[0] > img.shape[1]:
            img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # gray = cv2.bilateralFilter(gray, 11, 17, 17)
        thresh: np.ndarray = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)[1]

        min_x, max_y = get_min_xy(thresh)
        img_cropped = thresh[:max_y - 13, min_x + 10:]

        y_bars, x_bars = self.list_bars(img_cropped)
        angle = self.calculate_angle(thresh, y_bars)

        img_rot = self.rotate_image(thresh, -angle)
        min_x, max_y = get_min_xy(img_rot)
        img_cropped = img_rot[:max_y - 5, min_x + 5:]
        # plt.imshow(img_cropped, cmap='gray')
        # plt.show()
        self.global_cache['x_off'] = min_x + 5
        self.global_cache['y_off'] = max_y + 5

        y_bars, x_bars = self.list_bars(img_cropped)
        return img_cropped, y_bars, x_bars

    # Still need to handle two answer in col

    '''
    This function return the index of the the answer in the sheet
    '''

    def get_ans(self, img, chapter_bars, question_bars, chapter, question):
        if chapter > 5:
            chapter -= 3
            question += 30
        ans = np.zeros((4,))
        for i in range(1, 5):
            y1, y2 = chapter_bars[5 * (chapter - 1) + i]
            x1, x2 = question_bars[question - 1]
            ans[i - 1] = np.sum(img[y1:y2, x1:x2])
        if np.all(ans > ans.max() / 2):
            return None
        return np.argmin(ans)

    def draw_ans(self, img, chapter_bars, question_bars, chapter, question, ans):
        t = self.global_cache['angle']
        x_off = self.global_cache['x_off']

        ellipse_size = (5, 8)
        if chapter > 5:
            chapter -= 3
            question += 30
        chap_bar = chapter_bars[5 * (chapter - 1) + ans + 1]
        ques_bar = question_bars[question - 1]
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

    def id(self, img, y_arr, x_axis, j):
        id_arr = np.zeros((10,))
        for i in range(10):
            y1, y2 = y_arr[j]
            x1, x2 = x_axis[39 + i]
            id_arr[i] = np.sum(img[y1:y2, x1:x2])
        if np.all(id_arr > id_arr.max() / 2):
            return None
        return 9 - np.argmin(id_arr)

    def getStudentId(self, img, y_axis, x_axis):
        diff = y_axis[1][0] - y_axis[0][1]
        h = y_axis[0][1] - y_axis[0][0]
        end = y_axis[0][1]
        start = y_axis[0][0]
        y_arr = []
        for i in range(ID_LENGTH):
            y_arr.append((start, end))
            end = start - diff
            start = end - h
        id_arr = []
        for j in range(ID_LENGTH):
            num = self.id(img,y_arr,x_axis,j)
            id_arr.insert(0,num)
        id_str = ''.join(str(num) for num in id_arr)
        return id_str

    def getCorrectAnswer(self):
        img, chapter_bars, question_bars = self.process_image(self.teacherImage)
        res = self.rotate_image(cv2.imread(self.teacherImage), -self.global_cache['angle'])
        for chapter in range(1, len(self.typeChapter) + 1):
            if self.typeChapter[chapter - 1] == Chapter.unmarked.value:
                continue
            arr = []
            for question in range(1, numQuestion[self.typeChapter[chapter - 1]] + 1):
                ans = self.get_ans(img, chapter_bars, question_bars, chapter, question)
                if ans is None:
                    arr.append(-1)
                else:
                    arr.append(ans)
                    # self.draw_ans(res, chapter_bars, question_bars, chapter, question, ans)
            self.correctAnswer.append(arr)
        # cv2.imwrite('detected.png', res)
        # plt.imshow(res, cmap='gray')
        # plt.show()

    def uploadImages(self):
        for filename in os.listdir(self.folder):
            img = cv2.imread(os.path.join(self.folder, filename))
            if img is not None:
                self.studentsImagePaper.append(img)

    def getStudentAnswer(self, image):
        img, chapter_bars, question_bars = self.process_image(image,False)
        res = self.rotate_image(cv2.imread(self.teacherImage), -self.global_cache['angle'])
        id = self.getStudentId(img, chapter_bars, question_bars)
        for chapter in range(1, len(self.typeChapter) + 1):
            if self.typeChapter[chapter - 1] == Chapter.unmarked.value:
                continue
            arr = []
            for question in range(1, numQuestion[self.typeChapter[chapter - 1]] + 1):
                ans = self.get_ans(img, chapter_bars, question_bars, chapter, question)
                if ans is None:
                    arr.append(-1)
                else:
                    self.draw_ans(res, chapter_bars, question_bars, chapter, question, ans)
                    arr.append(ans)
            self.studentAnswer.append(arr)
        return id



    def getStudentGrade(self, studentId):
        student = studentInfo(studentId, self.typeChapter)
        index = -1
        for chapter in range(len(self.typeChapter)):
            if self.typeChapter[chapter] == Chapter.unmarked.value:
                continue
            index += 1
            for question in range(numQuestion[self.typeChapter[chapter]]):
                try:
                    if self.studentAnswer[index][question] \
                            != self.correctAnswer[index][question]:
                        student.incrementMistake(chapter)
                except:
                    print(chapter, question)
        self.studentsResult.append(student)


    #TODO : need to install the library to make the file that contain the info
    # of students
    """
    need to think how to get the name of the students 
    without reading the file again 
    
    """

    def createExcel(self):

        for student in self.studentsResult:
            print(student.getId())
            print(student.getGrade())

    def doAction(self):
        self.getCorrectAnswer()
        self.uploadImages()
        for i in range(len(self.studentsImagePaper)):
            studentId = self.getStudentAnswer(self.studentsImagePaper[i])
            self.getStudentGrade(studentId)
        self.createExcel()


if __name__ == '__main__':
    pro = imageProcessing('/cs/usr/hussamsal/PycharmProjects/image/image.jpeg'
                          , '/cs/usr/hussamsal/PycharmProjects/image/output_Image',
                          'MEEMEPAP')
    pro.doAction()
