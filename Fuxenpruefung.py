
import sys
import random
from tkinter import *
from tkinter import filedialog


#user interface
dict_init={}
dict_init[0]='Erstelle neue Fuxenpruefung'
dict_init[1]='Zeige Fragenstatistik'
dict_init[2]='Zeige alle Fragen'

base_path=''
# base_path=r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\\'
fox_png=base_path+'fox.png'
fox_ico=base_path+'fox.ico'
answer_file='Fuxenloesung.txt'
test_file='Fuxenpruefung.txt'
question_file=''


categories=[
            [16,'Kleine Fragen','K'],
            [6,'Mittlere Fragen','M'],
            [4,'Grosse Fragen','G'],
            [1000,'Permanente Fragen','P'],
            [5,'Scherzfragen','S'],
            [0,'Archiv','A'],
            ]



class InitWindow:

    def __init__(self, master,radioinit=0):

        self.master=master

        photo = PhotoImage(file=fox_png)
        photo=photo.subsample(5,5)
        self.w = Label(master, image=photo)
        self.w.photo = photo
        self.w.grid(row=0,columnspan=2)
        self.input_dict={}

        col_idx=0
        row_count=3
        for default,lg_name,short_name in categories:
            if short_name == 'P' or short_name == 'A': continue
            Label(master,text=lg_name).grid(row=row_count-2,column=col_idx)
            self.string_val = StringVar()
            self.string_val.set(default)
            e=Entry(master, textvariable=self.string_val,width=5).grid(row=row_count-1,column=col_idx)
            self.input_dict[short_name]=self.string_val
            col_idx = (col_idx + 1) % 2
            if (col_idx == 0):
                row_count += 2

        self.radio_var = IntVar()
        for key in dict_init.keys():
            rad=Radiobutton(master, text=dict_init[key], variable=self.radio_var, value=key)
            rad.grid(row=row_count,columnspan=2)
            row_count += 1
        self.radio_var.set(radioinit)

        # self.a_var = IntVar()
        # self.a_button = Checkbutton(master, text="Neue Fuxenpruefung", variable=self.a_var)
        # self.a_button.grid(row=1,columnspan=2)

        self.start_button = Button(master, text="Start", fg="green", command=master.quit)
        self.start_button.grid(row=row_count,column=0)
        self.quit_button = Button(master, text="Schliessen", fg="red", command=self.exit)
        self.quit_button.grid(row=row_count,column=1)
        row_count+= 1

    def exit(self):
        sys.exit()

class InfoWindow:

    def __init__(self, master,lines):
        row_count=0
        col_count=0
        widths=(200,50,50)
        stickys=(W,None,None)
        for line in lines:
            if isinstance(line, str):
                Message(master, text=line,width=200).grid(row=row_count,columnspan=3)
            elif isinstance(line, tuple):
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
def mystrip(a):
    return a.strip()
def make_on_configure(canvas):
    def on_configure(event):
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        canvas.configure(scrollregion=canvas.bbox('all'))
    return on_configure
class TextWindow:

    def __init__(self, master,header,lines):

        self.label = Label(master, text=header)
        self.label.pack(side=TOP)
        self.OK_button = Button(master, text="OK", command=master.quit)
        self.OK_button.pack(side=TOP)

        # --- create canvas with scrollbar ---
        self.canvas = Canvas(master, width=1200, height=600)
        self.canvas.pack(side=LEFT)
        self.scrollbar = Scrollbar(master, command=self.canvas.yview)
        self.scrollbar.pack(side=LEFT, fill='y')
        self.canvas.configure(yscrollcommand = self.scrollbar.set)
        # update scrollregion after starting 'mainloop'
        # when all widgets are in canvas
        self.canvas.bind('<Configure>', make_on_configure(self.canvas))
        # --- put frame in canvas ---
        self.frame = Frame(self.canvas)
        self.canvas.create_window((0,0), window=self.frame, anchor='nw')
        # --- add widgets in frame ---
        line_count=0
        col_count=0
        widths=(5,110,60,10,5,5)
        for line in lines:
            col_count=0
            line=list(line)
            if line_count:
                line.insert(0,str(line_count))
            else:
                line.insert(0,'#')
            for item in line:
                mytext = StringVar(value=item)
                myentry=Entry(self.frame, textvariable=mytext, state='readonly',width=widths[col_count])
                # myentry.pack(side=LEFT)
                myentry.grid(row=line_count,column=col_count, sticky=sticky_gen(col_count))
                col_count += 1
            line_count += 1





task_var=0
while True:

    useGUI = True
    quest_numbers={}
    if useGUI:
        mainroot = Tk()
        mainroot.iconbitmap(fox_ico)
        mainroot.title('Fux!')

        FILEOPENOPTIONS = dict(initialdir='.',defaultextension='.txt', filetypes=[('Text files','*.txt')])
        if not question_file: question_file=filedialog.askopenfilename(parent=mainroot,**FILEOPENOPTIONS)

        mainapp = InitWindow(mainroot,task_var)
        mainroot.mainloop()
        task_var=mainapp.radio_var.get()
        idx=0
        for default,lg_name,short_name in categories:
            try:
                quest_numbers[short_name]=int((mainapp.input_dict)[short_name].get())
            except KeyError:
                quest_numbers[short_name]=default
            categories[idx][0]=quest_numbers[short_name]
            idx += 1
        mainroot.destroy()
    else:
        question_file=base_path+'Fragensammlung.txt'
        task_var=0
        for default,lg_name,short_name in categories:
            quest_numbers[short_name]=default



    print('Gewaehlte Aufgabe:',dict_init[task_var])
    if not question_file:
        root = Tk()
        root.iconbitmap(fox_ico)
        root.title('Fehler!')
        lines = []
        lines.append('Keine Fragensammlung ausgewaehlt! Nochmal!')
        app = InfoWindow(root,lines)
        root.mainloop()
        root.destroy()
        continue



    #Read in data
    qdicts={}
    for key in quest_numbers.keys():
        qdicts[key]= {}
    qdicts_all={}

    quest_counter=0
    with open(question_file) as data:
        for line in data:
            line = line.rstrip()
            if line.startswith('#') or not len(line): continue
            splitlist=[]
            try:
                splitlist=line.split("#",4)
            except ValueError:
                continue
            splitlist=[x for x in map(mystrip,splitlist)]
            difficulty, question, answer, category, vspace=splitlist
            qdicts[difficulty][len(qdicts[difficulty])]=question,answer,category,vspace
            qdicts_all[quest_counter]=question,answer,category,difficulty,vspace
            quest_counter += 1







    if task_var == 0:
        ran_qdicts={}
        for qdict_str in qdicts:
            qdict=qdicts[qdict_str]
            keys = list(qdict.keys())
            random.shuffle(keys)
            ran_QnA = [(qdict[key][:2]+(qdict[key][3],)) for key in keys][:quest_numbers[qdict_str]]
            ran_qdicts[qdict_str]=ran_QnA

        with open(test_file, 'w') as myfile:
            print("Fuxenpruefung\n",file=myfile)
            count=0
            for default,lg_name,short_name in categories:
                for question,answer,vspace in ran_qdicts[short_name]:
                    count += 1
                    questionlines=question.split("\\\\")
                    print('{}.'.format(count),questionlines[0],file=myfile)
                    for item in questionlines[1:]:
                        print('\to '+item,file=myfile)
                    print('\n'*int(vspace),file=myfile)

    elif task_var == 1:
        from collections import Counter
        tot_n_questions = len(qdicts_all)
        #create message
        lines=[]
        lines.append('Fragenpool nach Schwierigkeit')
        lines.append(('Kategorie','Anzahl','Anteil'))
        for default,lg_name,short_name in categories:
            lines.append((lg_name+': ',str(len(qdicts[short_name])),'{:.2f}'.format(len(qdicts[short_name])/tot_n_questions)))

        lines.append('Fragenpool nach Thema')
        lines.append(('Kategorie','Anzahl','Anteil'))
        count_dict=Counter([x[2] for x in qdicts_all.values()])
        keys=list(count_dict.keys())
        keys.sort()
        for key in keys:
            lines.append((key+': ',str(count_dict[key]),'{:.2f}'.format(count_dict[key]/tot_n_questions)))

        root = Tk()
        root.iconbitmap(fox_ico)
        root.title('Fux!')
        app = InfoWindow(root,lines)
        root.mainloop()
        root.destroy()


    elif task_var == 2:

        header = 'Alle verfuegbaren Fragen und Antworten'
        lines=[]
        lines.append(('Frage','Antwort','Kateg.','Schw.','Platz'))
        for key in qdicts_all: lines.append((qdicts_all[key][0],qdicts_all[key][1],qdicts_all[key][2],qdicts_all[key][3],qdicts_all[key][4]))

        root = Tk()
        root.iconbitmap(fox_ico)
        root.title('Fux!')
        app = TextWindow(root,header,lines)
        root.mainloop()
        root.destroy()

    if not useGUI: break
