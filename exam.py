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

    num_to_latin = {1: 'I  ', 2: 'II ', 3: 'III', 4: 'IV',
                     5: 'V ', 6: 'VI', 7: 'VII', 8: 'IX',
                     9: 'X ', 10: 'IX', 11:'XI', 12:'XII'}


    def __init__(self, questions, config, pages=None):
        self.questions = questions
        self.id = Exam.count
        self.pages = pages
        self.logo_file_path = str(config["LOGO_FILE_PATH"])
        self.institution = str(config["INSTITUTION"])
        self.department = str(config["DEPARTMENT"])
        self.course = str(config["COURSE"])
        self.field_1 = str(config["FIELD_1"])
        self.field_2 = str(config["FIELD_2"])
        self.field_3 = str(config["FIELD_3"])
        self.instruction_heading = str(config["INSTRUCTION_HEADING"])
        self.instructions = str(config["INSTRUCTIONS"])
        self.duration = str(config["DURATION_INSTRUCTION"])
        self.question_text = str(config["QUESTION_TEXT"])
        self.numbering = str(config["NUMBERING"])
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

        pdf.image(self.logo_file_path, h=11, x=87)
        pdf.set_font("ArialUniBold", size=14)
        pdf.cell(0, 4, txt=self.institution,
                 ln=1, align='C')
        pdf.set_font("ArialUniBold", size=12)
        pdf.cell(0, 4, txt=self.department,
                 ln=2, align='C')
        pdf.cell(0, 10, txt=self.course,
                 ln=1, align='C')

        pdf.set_font("ArialUni", size=11)
        pdf.cell(200, 3.6, txt=f"{self.field_1} ﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒"
                             "﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒    "
                              f"{self.field_2} ﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒"
                             "﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒     "
                             f"{self.field_3} ﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒"
                             "﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒﹒    ",
                 ln=1, align='L')

        pdf.set_font("ArialUniBold", size=10)
        pdf.cell(190, 10, txt=self.instruction_heading,
                 ln=1, align='L')

        pdf.set_font("ArialUni", size=10)
        pdf.multi_cell(190, 3.6, txt=self.instructions,
                       align='L')
        pdf.ln(2)
        pdf.multi_cell(190, 3.6, txt=self.duration,
                       align='L')

        for i in range(len(self.questions)):
            pdf.multi_cell(190, 3.6, txt=f"\n {self.question_text} {i + 1}: {self.questions[i].question}",
                           align="L")
            if self.questions[i].image is not None:
                more_space = self.length_exceeds_limit(i)
                ybefore = pdf.get_y()
                pdf.multi_cell(effective_page_width / 2 - 10, 3.6, f"{self.create_question_text(i)}", align="L")
                pdf.set_xy(effective_page_width / 2 + pdf.l_margin, ybefore)
                pdf.image(self.questions[i].image, (effective_page_width / 2), h=25)
                pdf.ln(0.5 + 5 * more_space)
            else:
                pdf.multi_cell(190, 3.6, txt=f"{self.create_question_text(i)}", align="L")
            try:
                if self.questions[i+1].image is None:
                    if pdf.get_y() > 252:
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
                pdf.cell(190, 10, txt="Blank Page",
                         ln=2, align='C')

        pdf.output("exams/pdfs/{:03d}_exam.pdf".format(self.id))


    def generate_pdf_answer_reference(self):
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

        pdf.set_font("ArialUniBold", size=14)
        pdf.cell(0, 4, txt="Answer Reference",
                 ln=1, align='C')
        pdf.set_font("ArialUni", size=10)


        for i in range(len(self.questions)):
            pdf.multi_cell(190, 3.6, txt=f"\n {self.question_text} {i + 1}: {self.questions[i].question}",
                           align="L")
            if self.questions[i].image is not None:
                more_space = self.length_exceeds_limit(i)
                ybefore = pdf.get_y()
                pdf.multi_cell(effective_page_width / 2 - 10, 3.6,
                               f"{self.create_question_text_with_ans(i,self.questions[i].correct)}", align="L")
                pdf.set_xy(effective_page_width / 2 + pdf.l_margin, ybefore)
                pdf.image(self.questions[i].image, (effective_page_width / 2), h=24)
                pdf.ln(0.5 + 5 * more_space)
            else:
                pdf.multi_cell(190, 3.6, txt=f"{self.create_question_text_with_ans(i,self.questions[i].correct)}", align="L")
            try:
                if self.questions[i+1].image is None:
                    if pdf.get_y() > 252:
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
                pdf.cell(190, 10, txt="Blank Page",
                         ln=2, align='C')

        pdf.output("exams/ans_pdf/{:03d}_exam_ans.pdf".format(self.id))


    def create_question_text(self, index):
        txt = "\n"
        for i in range(len(self.questions[index].answers)):
             txt = txt + f"  ({self.convert_numbering(i + 1)}) {self.questions[index].answers[i]}\n"
        return txt[:-1]

    def create_question_text_with_ans(self, index, correct):
        txt = "\n"
        for i in range(len(self.questions[index].answers)):
            if i == correct - 1:
                txt = txt + f" ✓({self.convert_numbering(i + 1)}) {self.questions[index].answers[i]}\n"
            else:
                txt = txt + f"    ({self.convert_numbering(i + 1)}) {self.questions[index].answers[i]}\n"
        return txt[:-1]


    def length_exceeds_limit(self, index):
        if len(self.create_question_text(index)) > 200:
            return 1
        else:
            return 0


    def convert_numbering(self, num):
        if self.numbering == "Alphanumeric":
            return self.num_to_letter[num]
        elif self.numbering == "Latin":
            return self.num_to_latin[num]
        elif self.numbering == "Numeric":
            pass


    def export_answers_to_csv(self, filename=None):
        if filename is None:
            filename = "exams/answers/{:03d}_ans.csv".format(self.id)
        with open(filename, "w") as outfile:
            for question in self.questions:
                outfile.write("{} {}\n".format(question.id, question.correct))
