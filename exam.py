from fpdf import FPDF
import random


class PDF(FPDF):
    def footer(self):
        # Go to 1.5 cm from bottom
        self.set_y(-15)
        # Select Arial italic 8
        self.set_font('Arial', "", 9)
        # Print centered page number
        self.cell(0, 10, '%s' % self.page_no(), 0, 0, 'R')


class Exam():

    count = 1

    num_to_letter = {1: 'A', 2: 'B', 3: 'C', 4: 'D',
                     5: 'E', 6: 'F', 7: 'G', 8: 'H',
                     9: 'I', 10: 'J', 11:'K', 12:'L'}


    def __init__(self, questions, pages=None):
        self.questions = questions
        self.id = Exam.count
        self.pages = pages
        Exam.count += 1


    def randomize(self):
        random.shuffle(self.questions)


    def generate_pdf(self):
        # init pdf and configure fonts
        pdf = PDF('P', 'mm', 'A4')
        pdf.add_font('ArialUni', '', 'fonts/arial-unicode-ms.ttf', uni=True)
        pdf.add_font('ArialUniBold', '', 'fonts/Arial-Unicode-Bold.ttf', uni=True)

        effective_page_width = pdf.w - 2 * pdf.l_margin

        pdf.set_y(-15)
        pdf.set_font("ArialUni", size=10)
        pdf.add_page()
        pdf.cell(0, 3, txt="exam_{:03d}".format(self.id),
                 ln=1, align='L')

        pdf.image("data/aueb_logo.jpg", h=11, x=87)
        pdf.set_font("ArialUniBold", size=14)
        pdf.cell(0, 4, txt="Οικονομικό Πανεπιστήμιο Αθηνών",
                 ln=1, align='C')
        pdf.set_font("ArialUniBold", size=12)
        pdf.cell(0, 4, txt="Τμήμα Διοικητικής Επιστήμης και Τεχνολογίας",
                 ln=2, align='C')
        pdf.cell(0, 10, txt="Εισαγωγή στην Πληροφορική",
                 ln=1, align='C')

        pdf.set_font("ArialUni", size=11)
        pdf.cell(200, 3.6, txt="Όνομα: ﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒"
                             "﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒    "
                              "Επώνυμο: ﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒"
                             "﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒     "
                             "Αρ. Μητρώου: ﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒"
                             "﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒    ",
                 ln=1, align='L')

        pdf.set_font("ArialUniBold", size=10)
        pdf.cell(190, 10, txt="Οδηγίες:",
                 ln=1, align='L')

        pdf.set_font("ArialUni", size=10)
        pdf.multi_cell(190, 3.6, txt="Συμπληρώνετε όλες τις απαντήσεις σας στο φύλλο απαντήσεων, μαζί με τον αριθμό μητώου "
                                   "σας και τον αριθμό διαγωνίσματος, τον οποίο να βρείτε πάνω αριστερά σε αυτή τη σελίδα. "
                                   "Προσοχή: αν για παράδειγμα ο αριθμός διαγωνίσματος είναι ο exam_001, θα πρέπει να μαυρίσετε "
                                   "και τα δυο μηδενικά. Χρησιμοποιήστε σκούρο μπλέ η μαύρο στυλό, όχι μολύβι. "
                                   "Κάθε ερώτηση έχει μία μόνο σωστή απάντηση. ΔΕΝ υπάρχει αρνητική βαθμολόγηση.",
                       align='L')

        for i in range(len(self.questions)):
            pdf.multi_cell(190, 3.6, txt="\nΕρώτηση {}: {}".format(i + 1, self.questions[i].question),
                           align="L")
            if self.questions[i].image is not None:
                more_space = self.length_exceeds_limit(i)
                ybefore = pdf.get_y()
                pdf.multi_cell(effective_page_width / 2 - 10, 3.6, f"{self.create_question_text(i)}", align="L")
                pdf.set_xy(effective_page_width / 2 + pdf.l_margin, ybefore)
                pdf.image(self.questions[i].image, (effective_page_width / 2) - 4, h=28)
                pdf.ln(0.5 + 5 * more_space)
            else:
                pdf.multi_cell(190, 3.6, txt=f"{self.create_question_text(i)}", align="L")
            try:
                if self.questions[i+1].image is None:
                    if pdf.get_y() > 245:
                        pdf.add_page()
                else:
                    if pdf.get_y() > 235:
                        pdf.add_page()
            except:
                pass

        if self.pages is not None and self.pages >= pdf.page_no():
            for i in range(self.pages - pdf.page_no()):
                pdf.add_page()
                pdf.set_font("ArialUni", size=18)
                pdf.set_y(140)
                pdf.cell(190, 10, txt="ΚΕΝΗ  ΣΕΛΙΔΑ",
                         ln=2, align='C')

        pdf.output("exams/pdfs/{:03d}_exam.pdf".format(self.id))


    def create_question_text(self, index):
        txt = "\n"
        for i in range(len(self.questions[index].answers)):
             txt = txt + f"  ({self.num_to_letter[i+1]}) {self.questions[index].answers[i]}\n"
        return txt[:-1]


    def length_exceeds_limit(self, index):
        if len(self.create_question_text(index)) > 200:
            return 1
        else:
            return 0


    def export_answers_to_csv(self, filename=None):
        if filename is None:
            filename = "exams/answers/{:03d}_ans.csv".format(self.id)
        with open(filename, "w") as outfile:
            for question in self.questions:
                outfile.write("{} {}\n".format(question.id, question.correct))
