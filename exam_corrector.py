import csv
import pandas as pd

answer_sheets = pd.read_csv(r"C:\Users\gliar\Desktop\scan_results1.csv", delimiter=";")
print(answer_sheets)

am_cols = ["student_id.Question001", "student_id.Question002", "student_id.Question003", "student_id.Question004",
           "student_id.Question005", "student_id.Question006", "student_id.Question007"]

ans_cols = ["questions.Question008", "questions.Question009", "questions.Question0010", "questions.Question011", "questions.Question012", "questions.Question013",
                "questions.Question014", "questions.Question015", "questions.Question016", "questions.Question017", "questions.Question018", "questions.Question019",
                "questions.Question020", "questions.Question021", "questions.Question022", "questions.Question023", "questions.Question024", "questions.Question025",
                "questions.Question026", "questions.Question027", "questions.Question028", "questions.Question029", "questions.Question030", "questions.Question031"
                "questions.Question032", "questions.Question033", "questions.Question034", "questions.Question035", "questions.Question036", "questions.Question037"]

exam_no = ["exam_id.Question038", "exam_id.Question039", "exam_id.Question040"]

answer_sheets = answer_sheets.astype(str)

answer_sheets["AM"] = answer_sheets[am_cols[0]] + answer_sheets[am_cols[1]] + answer_sheets[am_cols[2]] + answer_sheets[am_cols[3]] + answer_sheets[am_cols[4]] + answer_sheets[am_cols[5]] +answer_sheets[am_cols[6]]
answer_sheets["exam_no"] = answer_sheets[exam_no[0]] + answer_sheets[exam_no[1]] + answer_sheets[exam_no[2]]
print(answer_sheets["AM"])

print(answer_sheets["exam_no"])