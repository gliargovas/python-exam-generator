# python-exam-generator
A dynamic multiple choise exam generator using python

## Installation and running

### Prerequisites

* Python 3
* PyFPDF: `pip install fpdf`

At first clone the repo (or download release):

    git clone https://github.com/gliargovas/python-exam-generator.git
    
### Question file
    
The structure of your exam is specified by a question file that contains the different
questions of the exam.

The questions csv file is comma (`,`) delimited.

Also, use double quotation marks when specifying text.

The general format of the exam is the following:

| Category  |  Question | Option 1 | Option 2 | ... | Option n | Correct option | Image path |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| Countries  |  "Which country is NOT located in Europe?" | Malta | Greenland | ... | United Kingdom | 2 |  |
| Countries  |  "Which country is NOT located in North America?" | Germany | United States | ... | United Kingdom | 1 |  |
| Flags  |  "Which country's flag is this?" | Greece | Greenland | ... | Germany | 2 | images/greek-flag.png |
| ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... | ... |

