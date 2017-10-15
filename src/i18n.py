import files


CURRENT_LANGUAGE = 'ger'


class dictionary:
    def __init__():
        pass
    score = {'ger': 'Punkte',
             'bay': 'Punkte',
             }
    rank = {'ger': 'Platz',
            'bay': 'Bloz',
            }
    time = {'ger': 'Datum',
            'bay': 'Datum',
            }
    username = {'ger': 'Name',
                'bay': 'Nom',
                }


def lang():
    return CURRENT_LANGUAGE


def translate(word):
    try:
        return getattr(dictionary, word.lower())[lang()]
    except KeyError:
        return word


def lang_button_image():
    return files.resource_path('', 'images\\' + lang() + '_' + switch_language(False) + '.png')


def switch_language(doSwitch=True):
    global CURRENT_LANGUAGE
    if CURRENT_LANGUAGE == 'ger':
        if doSwitch:
            CURRENT_LANGUAGE = 'eng'
        return 'eng'
    elif CURRENT_LANGUAGE == 'eng':
        if doSwitch:
            CURRENT_LANGUAGE = 'bay'
        return 'bay'
    elif CURRENT_LANGUAGE == 'bay':
        if doSwitch:
            CURRENT_LANGUAGE = 'ger'
        return 'ger'


longNames = {'ger': ['Kleine Frage', 'Mittlere Frage', 'Große Frage', 'Permanente Frage',
                     'Scherzfrage', 'Archiv'],
             'eng': ['Small question', 'Medium question', 'Hard question', 'Permanent question',
                     'Joke question', 'Archive'],
             'bay': ['Gloane Frog', 'Normale Frog', 'Gscheide Frog', 'Dauerfrog',
                     'Schmarrnfrog', 'Oide Frogn'],
             }
shortNames = {'ger': ['S', 'M', 'H', 'P', 'J', 'A'],
              'eng': ['S', 'M', 'H', 'P', 'J', 'A'],
              'bay': ['S', 'M', 'H', 'P', 'J', 'A'],
              }
startButtonText = {'ger': ['Start', 'Schließen'],
                   'eng': ['Go!', 'Close'],
                   'bay': ["Af geht's!", 'A Rua is!'],
                   }
linkLabelText = {'ger': 'AGV Webseite',
                 'eng': 'AGV website',
                 'bay': "Webseitn",
                 }
errorTitle = {'ger': 'Bierjunge!',
              'eng': 'Error!',
              'bay': 'Foisch!',
              }
errorText = {'ger': ['Keine Fragensammlung ausgewaehlt! Nochmal!', 'Falsches Passwort! Nochmal!',
                     'Fehler in Fragensammlung: '],
             'eng': ['No question file selected. Retry!', 'Bad password. Retry!', 'Error in question file: '],
             'bay': ['Koa Frognkatalog gfunna. Nomoi!', 'Posswoat foisch. Nomoi!', 'Foische Form im Frognkatalog: '],
             }
dictInit = {'ger': ['Erstelle neue Fuxenprüfung', 'Zeige Fragenstatistik', 'Zeige alle Fragen', 'Interaktives Quiz',
                    'Fuxensnake'],
            'eng': ['Compile new exam', 'Show question statistics', 'Show all questions', 'Interactive quiz',
                    'Fox Snake'],
            'bay': ['Gib ma a neie Pruefung', "Zeig ma d'Statistik", "Zeig olle Frogn her", 'Machma a Quiz',
                    'Fuxnspui'],
            }
examTitle = {'ger': ['Fuxenprüfung', 'Fuxenlösung'],
             'eng': ['Exam', 'Solution'],
             'bay': ["Afgobntext fia'd Fuxn", 'Loesung fian FM'],
             }
statisticsHeader = {'ger': ['Fragenpool nach Schwierigkeit', 'Fragenpool nach Thema'],
                    'eng': ['Question pool by difficulty', 'Question pool by topic'],
                    'bay': ["Frognkatalog noch wia schwar s'is", 'Frognkatalog noch Thema'],
                    }
statisticsColHeader = {'ger': ['Kategorie', 'Anzahl', 'Anteil'],
                       'eng': ['Category', 'Number', 'Fraction'],
                       'bay': ['Kategorie', 'Zohl', 'Brozent'],
                       }
allquestionsHeader = {'ger': 'Alle verfügbaren Fragen und Antworten',
                      'eng': 'All available questions and answers',
                      'bay': "Olle Frogn und Antwortn di wo's gibt",
                      }
allquestionsColHeader = {'ger': ['Frage', 'Antwort', 'Kateg.', 'Schw.', 'Platz'],
                         'eng': ['Question', 'Answer', 'Categ.', 'Diff.', 'Space'],
                         'bay': ['Frog', 'Antwort', 'Kateg.', 'Schw.', 'Ploz'],
                         }
appHeader = {'ger': 'Fuxenprüfungsgenerator',
             'eng': 'Exam generator',
             'bay': "Afgobnautomat fia'd Fuxn",
             }
passwordText = {'ger': ['Passwort', 'Datei ist verschlüsselt! Bitte Passwort eingeben:'],
                'eng': ['Password', 'File is encryoted! Please enter password:'],
                'bay': ['Posswoat', "Abgsperrt! Schlisse eigebn bitt'schen:"],
                }
examFile = {'ger': ['fuxenpruefung.txt', 'fuxenloesung.txt'],
            'eng': ['exam.txt', 'solution.txt'],
            'bay': ['fuxenpruefung.txt', 'fuxenloesung.txt'],
            }

quizTitle = {'ger': 'Fuxenquiz',
             'eng': 'Interactive quiz',
             'bay': "Quiz",
             }
yesNo = {'ger': ['Klar!', 'Nein'],
         'eng': ['Yes!', 'No'],
         'bay': ['No halle', 'Na'],
         }
quizButton = {'ger': ['Weiss ich', 'Keine Ahnung', 'Überspringen', 'Abbruch'],
              'eng': ['I know it', "I don't know", 'Skip', 'Cancel'],
              'bay': ['Woass I', 'Woas I ned', 'Andere Frog', 'Etz reichts!'],
              }
quizHeader = {'ger': ['Testergebnis', 'Interpretation'],
              'eng': ['Test result', 'Interpretation'],
              'bay': ["Zeignis", 'Wos hoast des etz'],
              }
quizInterpretation = {'ger': ['Durchgefallen', 'Knapp bestanden', 'Befriedigend', 'Gut gemacht', 'Perfekt'],
                      'eng': ['Insufficient', 'Barely passed', 'Sufficient', 'Well done', 'Perfect'],
                      'bay': ['A totaler Depp', 'Do homma scho bessane ghabt', 'Ned schlecht',
                              'Sauber, du woast echt vui', 'Du host gspickt'],
                      }
quizCorrect = {'ger': 'der Antworten wurden richtig beantwortet',
               'eng': 'of the questions were answered correctly',
               'bay': 'hom gstimmt',
               }
answerCorrect = {'ger': ['Richtig', 'Falsch', 'Übersprungen'],
                 'eng': ['Correct', 'Wrong', 'Skipped'],
                 'bay': ['Hod gstimmt', 'Foisch', 'Übersprunga'],
                 }
snakeWelcome = {'ger': 'Fuxensnake',
                'eng': 'Fox Snake',
                'bay': 'Fuxnspui',
                }
snakeInstruction = {'ger': ['Zum Start Enter oder Pfeiltaste drücken!',
                            'Es gibt einen Punkt pro Bier pro gefangenen Fux',
                            'Bier macht dich schnell und verwegen.',
                            'Aber Achtung, zu viel Bier behindert deine Arbeit!'],
                    'eng': ['Press return or arrow key to start!',
                            'You are awarded one point per Beer per caught Fox',
                            'Beer makes you tough and performant.',
                            'Buet take care, too much of it complicates your mission!'],
                    'bay': ['Druck af Enter oda an Pfeil zum Spuin!',
                            'Fia jeds Bier gibts bei am Fux an Punkt',
                            'A poa Bier san guad fiad Konzentration.',
                            'Aber Obacht, zvui Bier is a nix!'],
                    }
snakeScore = {'ger': 'Punktestand',
              'eng': 'Score',
              'bay': 'Punkte',
              }
gameOver = {'ger': ['Spiel vorbei', 'Escape Taste für Abbruch', 'Enter Taste für Neustart'],
            'eng': ['Game over', '<esc> to continue', '<return> for restart'],
            'bay': ["Aus is'", 'Druck af Escape wannst gnua host!', 'Nomoi mit da Enter Tastn'],
            }
snakeUserNameRequest = {'ger': ['Name eingeben', 'zum Ändern klicken', 'Name', 'Zeichen maximal'],
                        'eng': ['Enter your name', 'click to change', 'Name', 'characters maximum'],
                        'bay': ['Wia hoastn?', 'Do drucka fia ondan Nom', 'Nom', 'Buchstobn, koana drüba!'],
                        }
snakeHighScore = {'ger': ['Punktestand wird geladen', 'Persönlicher Highscore', 'Globaler Highscore'],
                  'eng': ['Loading highscore', 'Personal highscore', 'Global highscore'],
                  'bay': ['Heiskor werd glon', 'Dei Heiskor', 'Heiskor vo olle'],
                  }
snakeWebErr = {'ger': ['Keine Daten verfügbar', 'Webserver nicht erreichbar\nÜberprüfe deine Internetverbindung.',
                       'Kein Name gesetzt'],
               'eng': ['No data available', 'Webserver not reachable!\nPlease check your internet connection.',
                       'No user name set'],
               'bay': ['Koane Datn do', 'Webserver antwoat ned\nBist überhabts verbunna?.',
                       'Koa Nom ned eigem'],
               }
