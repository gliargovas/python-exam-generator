import argparse
import random
from exam import Exam
import question_parser
import time


def main(args):
    random.seed(args.seed)
    VERBOSE = args.verbose
    GROUPS = args.categories
    NUM_QUESTIONS = args.no_questions
    NUM_ANSWERS = args.no_options
    QUESTION_FILE = args.question_file
    NUM_EXAMS = args.no_exams
    SHUFFLE_QS = args.shuffle_questions
    SHUFFLE_ANS = args.shuffle_options
    EXAM_LENGTH = args.no_pages

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
            exam_qs.extend(random.sample(questions_grouped[category], questions_per_category))

        ex = Exam(exam_qs, EXAM_LENGTH)

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
        end = time.time()

        if VERBOSE:
            print(f"Time to generate exam {ex.id}: {end-start}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Python multiple choise exam generator')
    parser.add_argument('question_file', type=str,
                        help='the path of the question file')
    parser.add_argument('--no_exams', type=int, default=1,
                        help='number of the generated exams')
    parser.add_argument('--no_options', type=int, default=4,
                        help='the number of the possible options to select')
    parser.add_argument('--no_questions', type=int, default=30,
                        help='number of questions in the exam')
    parser.add_argument('--seed', type=int, default=0,
                        help='the seed for the exam generation')
    parser.add_argument('-v', "--verbose", action="store_true", default=False,
                        help='the seed for the exam generation')
    parser.add_argument('-s', '--shuffle_questions', action="store_true", default=False,
                        help='display questions in random order, other than the input order')
    parser.add_argument('-S', '--shuffle_options', action="store_true", default=False,
                        help='display question options in random order, other than the input order')
    parser.add_argument('-c', '--categories', action="store_true",
                        help='the number of question types in an exam, if 0, no categorization is made')
    parser.add_argument('--no_pages', type=int, default=None,
                        help='the page length of the exam, could help have similar exam format. '
                             'If 0, variable length instead')
    args = parser.parse_args()
    main(args)
