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

    def __init__(self, questions):
        self.questions = questions
        self.id = Exam.count
        Exam.count+=1

    def randomize(self):
        random.shuffle(self.questions)

    def generate_pdf(self):
        pdf = PDF('P', 'mm', 'A4')
        pdf.add_font('ArialUni', '', 'fonts/arial-unicode-ms.ttf', uni=True)
        pdf.add_font('ArialUniBold', '', 'fonts/Arial-Unicode-Bold.ttf', uni=True)


        pdf.set_y(-15)
        pdf.set_font("ArialUni", size=10)
        pdf.add_page()
        pdf.cell(0, 3, txt="exam_{:03d}".format(self.id),
                 ln=1, align='L')
        pdf.set_font("ArialUniBold", size=14)
        pdf.cell(0, 4, txt="Οικονομικό Πανεπιστήμιο Αθηνών",
                 ln=1, align='C')

        pdf.image("data/aueb_logo.jpg", h=8, x=87)


        pdf.set_font("ArialUniBold", size=12)
        pdf.cell(0, 3, txt="Τμήμα Διοικητικής Επιστήμης και Τεχνολογίας",
                 ln=2, align='C')
        pdf.cell(0, 10, txt="Εισαγωγή στην Πληροφορική",
                 ln=1, align='C')

        pdf.set_font("ArialUni", size=11)
        pdf.cell(200, 4, txt="Όνομα: ﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒"
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
        pdf.multi_cell(190, 3.8, txt="Συμπληρώνετε όλες τις απαντήσεις σας στο φύλλο απαντήσεων, μαζί με τον αριθμό μητώου "
                                   "σας και τον αριθμό διαγωνίσματος, τον οποίο να βρείτε πάνω αριστερά σε αυτή τη σελίδα. "
                                   "Προσοχή: αν για παράδειγμα ο αριθμός διαγωνίσματος είναι ο exam_001, θα πρέπει να μαυρίσετε "
                                   "και τα δυο μηδενικά. Χρησιμοποιήστε σκούρο μπλέ η μαύρο στυλό, όχι μολύβι"
                                   "Κάθε ερώτηση έχει μία μόνο σωστή απάντηση. ΔΕΝ υπάρχει αρνητική βαθμολόγηση.",
                       align='L')

        for i in range(len(self.questions)):

            if self.questions[i].image is not None:
                pdf.multi_cell(190, 3, txt="\n"
                                           "Ερώτηση {}: {}\n\n".format(i+1,
                                                            self.questions[i].question),
                               align="L")

                pdf.image(self.questions[i].image, h=30, x=38)
                pdf.multi_cell(190, 3.8, txt="\n"
                                             "   (a) {}\n"
                                             "   (b) {}\n"
                                             "   (c) {}\n"
                                             "   (d) {}\n".format(i + 1,
                                                                    self.questions[i].answers[0],
                                                                    self.questions[i].answers[1],
                                                                    self.questions[i].answers[2],
                                                                    self.questions[i].answers[3]),
                               align="L")
            else:
                pdf.multi_cell(190, 3.8, txt="\n"
                                             "Ερώτηση {}: {}\n\n"
                                             "   (a) {}\n"
                                             "   (b) {}\n"
                                             "   (c) {}\n"
                                             "   (d) {}\n"
                               .format(i + 1,
                                        self.questions[i].question,
                                        self.questions[i].answers[0],
                                        self.questions[i].answers[1],
                                        self.questions[i].answers[2],
                                        self.questions[i].answers[3]),
                               align="L")
            try:
                if self.questions[i+1].image is None:
                    if pdf.get_y() > 245:
                        pdf.add_page()
                else:
                    if pdf.get_y() > 215:
                        pdf.add_page()
            except:
                pass
        pdf.output("exams/pdfs/{:03d}_exam.pdf".format(self.id))


    def export_answers_to_csv(self, filename=None):
        if filename is None:
            filename = "exams/answers/{:03d}_ans.csv".format(self.id)
        with open(filename, "w") as outfile:
            for question in self.questions:
                outfile.write("{} {}\n".format(question.id, question.correct))
