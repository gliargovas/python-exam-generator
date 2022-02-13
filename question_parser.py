import csv
from exam_question import ExamQuestion


def parse_question_file(input_file):
    questions = []
    found_categories = set()
    with open(input_file, newline='', encoding="UTF-8") as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            try:
                if row[-1] != "":
                    questions.append(ExamQuestion(str(row[0]), row[1], row[2:-2], row[-2], row[-1]))
                else:
                    questions.append(ExamQuestion(str(row[0]), row[1], row[2:-2], row[-2]))
                found_categories.add(row[0])
            except:
                print(f"An error occured while parsing line: {row}")
    return questions, found_categories
