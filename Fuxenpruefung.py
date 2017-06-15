#defaultdict

print("Fuxenpruefung!")

number_D=2
number_M=2
number_E=3
number_F=1
question_file=r'C:\Users\Andreas Maier\Dropbox\Projects\Python\Fuxenpruefung\Fragensammlung.txt'
answer_file='Fuxenloesung.txt'
test_file='Fuxenpruefung.txt'

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
        if difficulty == 'S':
            qdict_D[len(qdict_D)]=question,answer,category
        elif difficulty == 'M':
            qdict_M[len(qdict_M)]=question,answer,category
        elif difficulty == 'L':
            qdict_E[len(qdict_E)]=question,answer,category
        elif difficulty == 'F':
            qdict_F[len(qdict_F)]=question,answer,category

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
