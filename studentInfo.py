import enum

NUM_QUESTION_MATH = 40
NUM_QUESTION_ARABIC = 40
NUM_QUESTION_ENGLISH = 44


class Chapter(enum.Enum):
    math = 'M'
    arabic = 'A'
    english = 'E'
    unmarked = 'P'


# still need to do the calculation
class studentInfo:

    def __init__(self, id, typeChapter, name=''):
        self.name = name
        self.id = id
        self.mistake = {Chapter.math: 0, Chapter.arabic: 0, Chapter.english: 0}
        # chapter number and how many mistake on it
        self.typeChapter = typeChapter

    def incrementMistake(self, chapterNumber):
        self.mistake[chapterNumber] += 1

    def getGrade(self):
        math = (NUM_QUESTION_MATH - self.mistake[Chapter.math] )* 3
        ar = NUM_QUESTION_ARABIC - self.mistake[Chapter.arabic]
        en = NUM_QUESTION_ENGLISH - self.mistake[Chapter.english]

        grade = int((math * 3 + ar + en) / 5)
        return grade

    def getId(self):
        return self.id