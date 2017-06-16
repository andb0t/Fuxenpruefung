
import sys
from tkinter import *

#user interface
dict_init={}
dict_init[0]='Erstelle neue Fuxenpruefung'
dict_init[1]='Zeige Fragenstatistik'
dict_init[2]='Zeige alle Fragen'

fox_png=r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\fox.png'
fox_ico=r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\fox.ico'
question_file=r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\Fragensammlung.txt'
answer_file='Fuxenloesung.txt'
test_file='Fuxenpruefung.txt'

class InitWindow:

    def __init__(self, master):

        self.master=master

        photo = PhotoImage(file=fox_png)
        photo=photo.subsample(5,5)
        self.w = Label(master, image=photo)
        self.w.photo = photo
        self.w.grid(row=0,columnspan=2)

        self.radio_var = IntVar()
        for key in dict_init.keys():
            Radiobutton(master, text=dict_init[key], variable=self.radio_var, value=key).grid(row=key+1,columnspan=2)

        # self.a_var = IntVar()
        # self.a_button = Checkbutton(master, text="Neue Fuxenpruefung", variable=self.a_var)
        # self.a_button.grid(row=1,columnspan=2)

        self.start_button = Button(master, text="Start", fg="green", command=master.quit)
        self.start_button.grid(row=len(dict_init)+1,column=0)

        self.quit_button = Button(master, text="Abbruch", fg="red", command=self.quit)
        self.quit_button.grid(row=len(dict_init)+1,column=1)

    def quit(self):
        sys.exit()

class InfoWindow:

    def __init__(self, master,header,lines):
        self.w = Message(master, text=header,width=200)
        self.w.grid(row=0,columnspan=3)

        row_count=1
        col_count=0
        widths=(200,50,50)
        stickys=(W,None,None)
        for line in lines:
            col_count = 0
            for item in line:
                mymsg=Message(master,text=line[col_count],width=widths[col_count])
                mymsg.grid(row=row_count,column=col_count,sticky=stickys[col_count])
                col_count += 1
            row_count += 1

        self.OK_button = Button(master, text="OK", command=master.quit)
        self.OK_button.grid(row=row_count,columnspan=3)

def sticky_gen(count):
    if count > 0:
        return W

class TextWindow:

    def __init__(self, master,header,lines):
        self.w = Message(master, text=header,width=400)
        self.w.grid(row=0,columnspan=len(lines[0]),sticky=None)

        row_count=1
        col_count=0
        widths=(5,60,60,15)
        for line in lines:
            col_count=0
            line=list(line)
            line.insert(0,str(row_count))
            for item in line:
                mytext = StringVar(value=item)
                myentry=Entry(master, textvariable=mytext, state='readonly',width=widths[col_count])
                myentry.grid(row=row_count,column=col_count, sticky=sticky_gen(col_count))
                col_count += 1
                col_start_str=''
            row_count += 1

        self.OK_button = Button(master, text="OK", command=master.quit)
        self.OK_button.grid(row=row_count,columnspan=len(lines[0]))

root = Tk()
root.iconbitmap(fox_ico)
root.title('Fux!')
app = InitWindow(root)
root.mainloop()
task_var=app.radio_var.get()
root.destroy() # optional; see description below

print('Gewaehlte Aufgabe:',dict_init[task_var])





#user defined parameters
number_D=2
number_M=2
number_E=3
number_F=1


#Read in data
qdict_D={}
qdict_M={}
qdict_E={}
qdict_F={}
with open(question_file) as data:
    for line in data:
        if line.startswith('#'): continue
        line = line.rstrip()
        try:
            difficulty, question, answer, category=line.split(":",3)
        except ValueError:
            continue
        if difficulty == 'D':
            qdict_D[len(qdict_D)]=question,answer,category
        elif difficulty == 'M':
            qdict_M[len(qdict_M)]=question,answer,category
        elif difficulty == 'E':
            qdict_E[len(qdict_E)]=question,answer,category
        elif difficulty == 'F':
            qdict_F[len(qdict_F)]=question,answer,category



if task_var == 0:

    import random
    keys_D =  list(qdict_D.keys())
    keys_M =  list(qdict_M.keys())
    keys_E =  list(qdict_E.keys())
    keys_F =  list(qdict_F.keys())

    random.shuffle(keys_D)
    random.shuffle(keys_M)
    random.shuffle(keys_E)
    random.shuffle(keys_F)

    QnA_D = [qdict_D[key][:2] for key in keys_D][:number_D]
    QnA_M = [qdict_M[key][:2] for key in keys_M][:number_M]
    QnA_E = [qdict_E[key][:2] for key in keys_E][:number_E]
    QnA_F = [qdict_F[key][:2] for key in keys_F][:number_F]

    myfile = open(test_file, 'w')
    print("Fuxenpruefung",file=myfile)
    count=0
    for question,answer in QnA_D:
        count += 1
        print('{}.'.format(count),question,file=myfile)
    for question,answer in QnA_M:
        count += 1
        print('{}.'.format(count),question,file=myfile)
    for question,answer in QnA_E:
        count += 1
        print('{}.'.format(count),question,file=myfile)
    for question,answer in QnA_F:
        count += 1
        print('{}.'.format(count),question,file=myfile)

elif task_var == 1:

    tot_n_questions= len(qdict_D)+ len(qdict_M)+ len(qdict_E)+ len(qdict_F)

    #create message
    header='Fragenstatistik'
    lines=[]
    lines.append(('Kategorie','Anzahl','Anteil'))
    lines.append(('Fragen "D": ',str(len(qdict_D)),'{:.2f}'.format(len(qdict_D)/tot_n_questions)))
    lines.append(('Fragen "M": ',str(len(qdict_M)),'{:.2f}'.format(len(qdict_M)/tot_n_questions)))
    lines.append(('Fragen "E": ',str(len(qdict_E)),'{:.2f}'.format(len(qdict_E)/tot_n_questions)))
    lines.append(('Fragen "F": ',str(len(qdict_F)),'{:.2f}'.format(len(qdict_F)/tot_n_questions)))

    #create the window
    root = Tk()
    root.iconbitmap(fox_ico)
    root.title('Fux!')
    app = InfoWindow(root,header,lines)
    root.mainloop()
    root.destroy() # optional; see description below


elif task_var == 2:

    header = 'Alle verfuegbaren Fragen und Antworten'
    lines=[]
    for item in qdict_D: lines.append(qdict_D[item])
    for item in qdict_M: lines.append(qdict_M[item])
    for item in qdict_E: lines.append(qdict_E[item])
    for item in qdict_F: lines.append(qdict_F[item])

    #create the window
    root = Tk()
    root.iconbitmap(fox_ico)
    root.title('Fux!')
    app = TextWindow(root,header,lines)
    root.mainloop()
    root.destroy() # optional; see description below
