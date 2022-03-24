import configparser
import random
from exam import Exam
import question_parser
import time


def main():
    config = configparser.ConfigParser()
    config.read('config.txt')
    args = config["exam_generation"]
    exam_design_args = config["exam_design"]
    random.seed(int(args["SEED"]))
    VERBOSE = bool(args["VERBOSE"])
    GROUPS = bool(args["CATEGORIZE_QUESTIONS"])
    NUM_QUESTIONS = int(args["NUMBER_OF_QUESTIONS"])
    SAMPLE = bool(args["RANDOM_SAMPLING"])
    QUESTION_FILE = args["QUESTION_FILE"]
    NUM_EXAMS = int(args["NUMBER_OF_EXAMS"])
    SHUFFLE_QS = bool(args["SHUFFLE_QUESTIONS"])
    SHUFFLE_ANS = bool(args["SHUFFLE_OPTIONS"])
    EXAM_LENGTH = int(args["PAGES"])
    ANS = bool(args["GENERATE_ANSWERS"])

    questions, categories = question_parser.parse_question_file(QUESTION_FILE)

    if VERBOSE:
        for question in questions:
            print(question)
        print()
        print(f"Found {len(questions)} questions and {len(categories)} categories.")

    questions_grouped = dict()
    if GROUPS:
        for cat in categories:
            questions_grouped[cat] = []
        for question in questions:
            questions_grouped[question.category].append(question)
    else:
        questions_grouped["default"] = []
        for question in questions:
            questions_grouped["default"].append(question)

    questions_per_category = int(NUM_QUESTIONS / len(questions_grouped))
    if VERBOSE and GROUPS:
        print(f"Splitting category questions into equal segmants.\n"
              f"Questions per category: {questions_per_category}\n")

    for i in range(NUM_EXAMS):
        exam_qs = []

        for category in questions_grouped:
            # select random subset
            if SAMPLE:
                exam_qs.extend(sorted(random.sample(questions_grouped[category], questions_per_category), key=lambda x: x.id))
            else:
                exam_qs.extend(questions_grouped[category][:questions_per_category])

        ex = Exam(exam_qs, exam_design_args, EXAM_LENGTH)

        # optionally shuffle question answer order
        if SHUFFLE_ANS:
            for question in ex.questions:
                question.randomize()

        # optionally shuffle question order
        if SHUFFLE_QS:
            ex.randomize()

        start = time.time()
        ex.generate_pdf()
        ex.export_answers_to_csv()
        if ANS:
            ex.generate_pdf_answer_reference()
        end = time.time()

        if VERBOSE:
            print(f"Time to generate exam {ex.id}: {end-start}")


if __name__ == '__main__':
    main()
