import random

class ExamQuestion():

    count = 1

    def __init__(self, category, question, answers, correct, image=None):
        self.category = category
        self.question = question
        self.answers = answers
        self.correct = int(correct)
        self.id = str(ExamQuestion.count)
        self.image = image
        ExamQuestion.count += 1

    def __str__(self):
        string = "ID: {}\n" \
                 "{}\n".format(self.id, self.question)
        for i in range(len(self.answers)):
            string += "{}) {}".format(i+1, self.answers[i])
            if self.correct == i+1:
                print(self.correct)
                string += " <"
            string += "\n"
        return string

    def randomize(self, seed=None):
        if seed is not None:
            random.seed(seed)
        old_list = dict(enumerate(self.answers))
        old_correct = old_list.get(self.correct-1)
        random.shuffle(self.answers)
        for i in range(len(self.answers)):
            if self.answers[i] == old_correct:
                self.correct = i+1
