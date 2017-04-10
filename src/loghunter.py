#!/usr/bin/python
__file__       = "loghunter"
__author__     = "Ka Wa Tsang"
__copyright__  = "Copyright 2016"
__version__    = "1.1.3"
__email__      = "kwtsang@nikhef.nl"

"""
  Name:
       loghunter
  Author:
       Ka Wa TSANG
"""
Description="""
       A program to 1) create tex                 (log, slide, research)
                    2) view pdf, djvu             (log, slide, research, cheatsheet, paper, presentation, book)
                    3) copy files to folder       (log, slide, research, cheatsheet, paper, presentation, book)
                    4) change directory to folder (log, slide, research, cheatsheet, paper, presentation. book) 

       Default 1) type is log 
               2) mode is create

       Example Usage 1) loghunter             To create the log of this week
                     2) loghunter -v          To view the log pdf of this week
                     3) loghunter -v -dt -7   To view the log pdf of last week
                     4) loghunter -ls -v      To view the pdf by entering the corresponding index
       """
"""
  History:
       22-Sep-2016 First version. Namely logcreate.
       23-Sep-2016 Arbitrary date of log can be added through -d.
       25-Sep-2016 echo color added. Red for err and Green for msg.
                   More checks are applyed on the date entered.
       28-Sep-2016 Modified the log template. 
                   Added vim +25 option.
       30-Sep-2016 Added an error msg if compilation fails.
       01-Oct-2016 Added a friendly option for -d/--date. eg. -d -7 means last week.
                   Added Initialization.
       07-Oct-2016 log.pdf is renamed to be log_old.pdf before compilation.
                   If compilation fails, log_old.pdf -> log.pdf
                   If compilation runs successfully, rm log_old.pdf
       16-Oct-2016 New alias (logcombine, logreport) are added
                   Tex report -> article
       20-Oct-2016 Added physics package
       05-Nov-2016 Typeflag (first version) is added.
                   Typeflag = 0 represents log. (default)
                            = 1 represents cheatsheet.
                            = 2 represents slide.
                   First version of logview.sh, used for view, cd, cp.
       06-Nov-2016 Simple help is added.
       24-Nov-2016 Transform the shell script to python script.
                   Rename the program to be "loghunter" !!
                   Change Description.
                   version tag = 1.0.1
       01-Dec-2016 Added one more directory layer to "paper" type for the classification of layer.
                   If the tex didnt be modified, wont start compilation.
       08-Dec-2016 Added a handy --list option.
                   Modified the argparse shorthand.
                   version tag = 1.1.1
                   Minor fix to the printf statement
                   version tag = 1.1.2
                   Included extension apart from ".pdf"
                   Completed --copy mode
                   Added types (presentation, book and other)
                   version tag = 1.1.3
       21-Jan-2017 Added research type
"""

#=======================================================================================
# Module/package import
#=======================================================================================

import os
import sys
import subprocess
import argparse
import textwrap
from datetime import datetime, timedelta

#=======================================================================================
# User Input before using this scirpt !!
#=======================================================================================

# Global Variable
LogDirPath="/home/kwtsang/Dropbox/loghunter_data"
LogSrcPath="/home/kwtsang/OneDrive_CUHK/mle/loghunter/src"
PDFReader="okular"
TexEditor="vim"
TexEditorOptions="+26"

TexCleanFileFormat=[ "log", "aux", "out", "nav", "snm", "toc", "dvi" ]

#=======================================================================================
# General Function
#=======================================================================================
def printf(string, printtype="message", askforinput=False):
  """
    To print out the message of different types.
    Optional: "askforinput", if true, the function will return the input by user.
  """
  if askforinput == False:
    print "log %7s :: %s" % ( printtype, string )
  elif askforinput == True:
    return raw_input( "log %7s :: %s" % ( printtype, string ) )
  else:
    printf("Unknown option for askforinput in the printf function ! Exiting ...", "error")
    sys.exit()

def Date(date, dt=0, dayofweek=None, dateformat="%Y%m%d"):
  """
    To obtain the date of the weekday of the input date.
    eg. Date( today, dayofweek=6 ) returns the date of the coming Saturday.
    Optional: "dt", eg dt = -1, the date passed will be one day earlier of the input date.
  """
  d = datetime.strptime(str(date),"%Y%m%d") + timedelta(days=dt)
  if dayofweek!=None:
    if isinstance( dayofweek, int ):
      if d.isoweekday() == 7:
        isoweekday = 0;
      else:
        isoweekday = d.isoweekday()
      d = ( d - timedelta(days=isoweekday+dayofweek) )
    else:
      printf("Unknown value for dayofweek in the Date function !", "warning")
      printf("Ignoring the dayofweek option in the Date function ...", "warning")
  return d.strftime(dateformat)

def List(path, ext=[".pdf", ".djvu"], savepath=False):
  """
    To obtain the absolute path of all files under "path" with "extension"
    Optional: "savepath", if true, return [AbsPath,Name,Ext] of the target file, if any
  """
  ArrayAbsPath = []
  # To obtain all files (with absolute path under "path") and store in ArrayFullPath
  for dirPath, dirName, fileName in os.walk(path):
    for iter_fileName in fileName:
      if os.path.splitext(iter_fileName)[1] in ext:
        ArrayAbsPath.append([dirPath,os.path.splitext(iter_fileName)[0],os.path.splitext(iter_fileName)[1]])
  # If ArrayAbsPath not empty:
  if ArrayAbsPath:
    for iter_AbsPath, iter_Name, iter_Ext in ArrayAbsPath:
      print "%3i) %s/%s%s" % (ArrayAbsPath.index([iter_AbsPath,iter_Name,iter_Ext])+1,iter_AbsPath,iter_Name,iter_Ext)
    if savepath==True:
      while 1:
        try:
          IndexToSave = printf("Please enter the file index to select: ", askforinput=True)
          if IndexToSave == "":
            continue
          else:
            IndexToSave = int(IndexToSave)
            if isinstance(IndexToSave, int):
              if IndexToSave > 0 and IndexToSave < len(ArrayAbsPath)+1:
                return ArrayAbsPath[IndexToSave-1]
              else:
                printf("The file index is out of range. Try again ..." ,"warning")
        except KeyboardInterrupt:
          print ""
          printf("User terminates the loghunter. Good Bye!")
          sys.exit()
        except: 
          printf("Unknown file index. Exiting ...", "error")
          sys.exit()
    elif savepath!=False:
      printf("Unknown value for savepath in the List function !", "warning")
      printf("Ignoring the savepath option in the List function ...", "warning")
  # If empty:
  else:
    printf("No file with extension (%s) is found in the path of %s" % (ext,path))
    if savepath==True:
      printf("Expected return value from the List function is missing. Exiting ...", "error")
      sys.exit()
    elif savepath!=False:
      printf("Unknown value for savepath in the List function !", "warning")
      printf("Ignoring the savepath option in the List function ...", "warning")

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is one of "yes" or "no".
    """
    valid = {"yes":"yes",   "y":"yes",  "ye":"yes",
             "no":"no",     "n":"no"}
    if default == None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while 1:
        choice = printf(question + prompt, askforinput=True).lower()
        if default is not None and choice == '':
            return default
        elif choice in valid.keys():
            return valid[choice]
        else:
            printf("Please respond with 'yes' or 'no' (or 'y' or 'n').", "warning")

#=======================================================================================
# Template Function
#=======================================================================================
def print_log_tex():
  TEXOBJECT = open (TEXTEXPATH,"w+")
  TEXOBJECT.write('%s\n' % (r"\documentclass[a4paper,12pt]{article}" ))
  TEXOBJECT.write('%s\n' % (r"\usepackage{geometry}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{graphicx}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{amsmath}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{hyperref}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{physics}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{url}"))
  TEXOBJECT.write('%s\n' % (r"\geometry{"))
  TEXOBJECT.write('%s\n' % (r" a4paper,"))
  TEXOBJECT.write('%s\n' % (r" total={170mm,257mm},"))
  TEXOBJECT.write('%s\n' % (r" left=20mm,"))
  TEXOBJECT.write('%s\n' % (r" top=20mm,"))
  TEXOBJECT.write('%s\n' % (r"}"))
  TEXOBJECT.write('%s\n' % (r""))
  
  TEXOBJECT.write('%s\n' % (r"%Title page"))
  TEXOBJECT.write('%s\n' % (r"\title{Work log}"))
  TEXOBJECT.write('%s\n' % (r"\author{" + __author__ +  "}"))
  TEXOBJECT.write('%s\n' % (r"\date{" + Date(args.date, dt=args.delta_days, dayofweek=0, dateformat="%Y-%m-%d") + "}"))
  TEXOBJECT.write('%s\n' % (r""))
 
  TEXOBJECT.write('%s\n' % (r"\begin{document}" ))
  TEXOBJECT.write('%s\n' % (r"\maketitle"))
  TEXOBJECT.write('%s\n' % (r""))
  
  TEXOBJECT.write('%s\n' % (r"%Contents"))

  TEXOBJECT.write('%s\n' % (r"\section{Summary}"))
  TEXOBJECT.write('%s\n' % (r"\begin{itemize}"))
  TEXOBJECT.write('%s\n' % (r"  \item "))
  TEXOBJECT.write('%s\n' % (r"\end{itemize}"))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r"\section{To do list}"))
  TEXOBJECT.write('%s\n' % (r"\begin{itemize}"))
  TEXOBJECT.write('%s\n' % (r"  \item [ ] H:"))
  TEXOBJECT.write('%s\n' % (r"  \item [ ] M:"))
  TEXOBJECT.write('%s\n' % (r"  \item [ ] L:"))
  TEXOBJECT.write('%s\n' % (r"\end{itemize}"))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r""))
  TEXOBJECT.write('%s\n' % (r"\end{document}"))
  TEXOBJECT.close()

def print_slide_tex():
  TEXOBJECT = open (TEXTEXPATH,"w+")
  TEXOBJECT.write('%s\n' % (r"\documentclass{beamer}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage[utf8]{inputenc}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{graphicx}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{physics}"))
  TEXOBJECT.write('%s\n' % (r"\usetheme{Madrid}"))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r"\title[TitleShortHand]{" + args.title + "}"))
  TEXOBJECT.write('%s\n' % (r"\subtitle{Subtitle}"))
  TEXOBJECT.write('%s\n' % (r"\author{" + __author__ +  "}"))
  TEXOBJECT.write('%s\n' % (r"\institute[Nikhef]{National Institute for Subatomic Physics (Nikhef)}"))
  TEXOBJECT.write('%s\n' % (r"\date[" + Date(args.date, dt=args.delta_days, dateformat="%Y %b %d") + "]{" + args.subtype.replace ("_", " ") + ", " + Date(args.date, dt=args.delta_days, dateformat="%Y %b %d" + "}")))
  TEXOBJECT.write('%s\n' % (r"\titlegraphic{\includegraphics[width=3cm, keepaspectratio]{Nikhef-400x177.png}}"))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r"\begin{document}"))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r"\section{Title Page}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r"\begin{frame}"))
  TEXOBJECT.write('%s\n' % (r"\titlepage"))
  TEXOBJECT.write('%s\n' % (r"\end{frame}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r"\section{Contents}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r"\begin{frame}"))
  TEXOBJECT.write('%s\n' % (r"\frametitle{Table of Contents}"))
  TEXOBJECT.write('%s\n' % (r"\begin{enumerate}"))
  TEXOBJECT.write('%s\n' % (r"  \item "))
  TEXOBJECT.write('%s\n' % (r"\end{enumerate}"))
  TEXOBJECT.write('%s\n' % (r"\end{frame}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r"\section{Motivation}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r"\begin{frame}"))
  TEXOBJECT.write('%s\n' % (r"\frametitle{Motivation}"))
  TEXOBJECT.write('%s\n' % (r""))
  TEXOBJECT.write('%s\n' % (r"\end{frame}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r""))

  TEXOBJECT.write('%s\n' % (r"\section{Backup}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r"\begin{frame}"))
  TEXOBJECT.write('%s\n' % (r"\frametitle{Backup}"))
  TEXOBJECT.write('%s\n' % (r"Thank you!"))
  TEXOBJECT.write('%s\n' % (r"\Huge{\centerline{The End}}"))
  TEXOBJECT.write('%s\n' % (r"\end{frame}"))
  TEXOBJECT.write('%s\n' % (r"%==================================="))
  TEXOBJECT.write('%s\n' % (r""))
  TEXOBJECT.write('%s\n' % (r""))
  TEXOBJECT.write('%s\n' % (r"\end{document}"))

def print_research_tex():
  TEXOBJECT = open (TEXTEXPATH,"w+")
  TEXOBJECT.write('%s\n' % (r"\documentclass[a4paper,12pt]{article}" ))
  TEXOBJECT.write('%s\n' % (r"\usepackage{geometry}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{graphicx}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{amsmath}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{hyperref}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{physics}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{longtable}"))
  TEXOBJECT.write('%s\n' % (r"\usepackage{url}"))
  TEXOBJECT.write('%s\n' % (r"\geometry{"))
  TEXOBJECT.write('%s\n' % (r" a4paper,"))
  TEXOBJECT.write('%s\n' % (r" total={170mm,257mm},"))
  TEXOBJECT.write('%s\n' % (r" left=20mm,"))
  TEXOBJECT.write('%s\n' % (r" top=20mm,"))
  TEXOBJECT.write('%s\n' % (r"}"))
  TEXOBJECT.write('%s\n' % (r""))
  
  TEXOBJECT.write('%s\n' % (r"%Title page"))
  TEXOBJECT.write('%s\n' % (r"\title{Research Progress - " + args.subtype + "}"))
  TEXOBJECT.write('%s\n' % (r"\author{" + __author__ +  "}"))
  TEXOBJECT.write('%s\n' % (r"\date{\today}"))
  TEXOBJECT.write('%s\n' % (r""))
 
  TEXOBJECT.write('%s\n' % (r"\begin{document}" ))
  TEXOBJECT.write('%s\n' % (r"\maketitle"))
  TEXOBJECT.write('%s\n' % (r""))
  
  TEXOBJECT.write('%s\n' % (r"%Contents"))

  TEXOBJECT.write('%s\n' % (r""))
  TEXOBJECT.write('%s\n' % (r""))
  TEXOBJECT.write('%s\n' % (r"\end{document}"))
  TEXOBJECT.close()

#=======================================================================================
# Preliminary
#=======================================================================================

parser = argparse.ArgumentParser(description=textwrap.dedent(Description), prog=__file__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-d ", "--date"      , default=datetime.today().strftime("%Y%m%d"), action="store", type=int, help="Date in YYYYMMDD format. (default: today)")
parser.add_argument("-dt", "--delta-days", default=0                                  , action="store", type=int, help="Number of days before/after the --date. eg. -1 means yesterday.")
parser.add_argument("-st", "--subtype"   ,                                              action="store", help="For further classification in each type.")
parser.add_argument("-tt", "--title"                                                  , action="store")

parser.add_argument("-lg", "--log"          , default=False, action="store_true", help="Type: log. (Default)")
parser.add_argument("-sl", "--slide"        , default=False, action="store_true", help="Type: slide. Please include --date, --subtype and --title.")
parser.add_argument("-ch", "--cheatsheet"   , default=False, action="store_true", help="Type: cheatsheet.")
parser.add_argument("-pp", "--paper"        , default=False, action="store_true", help="Type: paper.")
parser.add_argument("-pt", "--presentation" , default=False, action="store_true", help="Type: past presentation by others.")
parser.add_argument("-bk", "--book"         , default=False, action="store_true", help="Type: book.")
parser.add_argument("-rs", "--research"     , default=False, action="store_true", help="Type: research. Please include --subtype.")
parser.add_argument(       "--other"        , default=False, action="store_true", help="Type: other.")

parser.add_argument("-cr", "--create"    , default=False, action="store_true", help="Mode: create the tex. (Default)")
parser.add_argument("-v ", "--view"      , default=False, action="store_true", help="Mode: view the pdf.")
parser.add_argument("-cp", "--copy"                     , action="store"     , help="Mode: copy files to folder.")
parser.add_argument("-cd", "--changedir" , default=False, action="store_true", help="Mode: change directory to folder.")

parser.add_argument("-ls", "--list" , default=False, action="store_true", help="List/Select contents. (Very handy!)")

parser.add_argument(       "--verbose"   , default=False, action="store_true", help="Print more messages.")
parser.add_argument(       "--version"   ,                action="version", version='%(prog)s ' + __version__)
args = parser.parse_args()

# Initialize the modeflag and typeflag
if args.copy:
  copyflag = True
else:
  copyflag = False
modeflag = { "create":args.create, "view":args.view, "copy":copyflag, "changedir":args.changedir }
typeflag = { "log":args.log, "slide":args.slide, "cheatsheet":args.cheatsheet, "paper":args.paper, "presentation":args.presentation, "book":args.book, "research":args.research, "other":args.other }

# if --list only (ie. without modeflag) and exit
if args.list and sum(modeflag.values())==0:
  for typekey,typevalue in typeflag.iteritems():
    if typevalue == True or sum(typeflag.values())==0:
      printf("List of %s:" % typekey)
      List(LogDirPath + "/" + typekey)
      print ""
  sys.exit()

# Set default mode to be "create" and ensure there is only one mode
if sum(modeflag.values()) == 0:
  modeflag["create"] = True
elif sum(modeflag.values()) > 1:
  printf("Modeflag is %s." % modeflag, "error")
  printf("More than one modeflag! Exiting ...", "error")
  sys.exit()

# if --list with modeflag enabled
if args.list:
  _TEXEXTENSION = [".pdf", ".djvu"]
  if modeflag["create"] == True:
    _TEXEXTENSION = [".tex"]

  if sum(typeflag.values()) == 0:
    TEXDIRPATH, TEXNAME, TEXEXTENSION = List(LogDirPath, ext=_TEXEXTENSION, savepath=True)
  elif sum(typeflag.values()) == 1:
    for typekey,typevalue in typeflag.iteritems():
      if typevalue == True:
        printf("List of %s:" % typekey)
        TEXDIRPATH, TEXNAME, TEXEXTENSION = List(LogDirPath + "/" + typekey, ext=_TEXEXTENSION, savepath=True)
  else:
    printf("Typeflag is %s." % typeflag, "error")
    printf("More than one typeflag! Exiting ...", "error")
    sys.exit()

  if args.verbose:
    printf("TEXDIRPATH is set to be %s ." % TEXDIRPATH, "verbose")
    printf("TEXNAME is set to be %s ." % TEXNAME, "verbose")
    printf("TEXEXTENSION is set to be %s ." % TEXEXTENSION, "verbose")

# Set default type to be "log" and ensure there is only one type
if sum(typeflag.values()) == 0:
  typeflag["log"] = True
elif sum(typeflag.values()) > 1:
  printf("Typeflag is %s." % typeflag, "error")
  printf("More than one typeflag! Exiting ...", "error")
  sys.exit()

# if --list disabled (Default)
if not args.list:
  # Check arguments
  # Check the validity of date
  args.date=Date(args.date)
  # Check whether --title or --subtype are missing
  for typekey, typevalue in typeflag.iteritems():
    for modekey, modevalue in modeflag.iteritems():
      if typekey in ["slide", "paper", "presentation", "book"] and typevalue == True:
        if modekey in ["create", "view"] and modevalue == True:
          if args.title == None or args.subtype == None:
            printf("Type %s in mode %s requires both --title and --subtype. Exiting ..." % (typekey, modekey), "error")
            sys.exit()
        if modekey in ["copy", "changedir"] and modevalue == True:
          if args.subtype == None:
            printf("Type %s in mode %s requires --subtype. Exiting ..." % (typekey, modekey), "error")
            sys.exit()
          if args.title == None:
            args.title = "Arbitrary"
            printf("args.title is set to be Arbitrary because it will not be used.", "verbose") if args.verbose == True else None
      if typekey in ["cheatsheet", "other"] and typevalue == True:
        if modekey in ["create", "view"] and modevalue == True:
          if args.title == None:
            printf("Type %s in mode %s requires --title. Exiting ..." % (typekey, modekey), "error")
            sys.exit()
        if modekey in ["copy", "changedir"] and modevalue == True:
          if args.title == None:
            args.title = "Arbitrary"
            printf("args.title is set to be Arbitrary because it will not be used.", "verbose") if args.verbose == True else None
      if typekey in ["research"] and typevalue == True:
        if modekey in ["create", "view", "copy", "changedir"] and modevalue == True:
          if args.subtype == None:
            printf("Type %s in mode %s requires --subtype. Exiting ..." % (typekey, modekey), "error")
            sys.exit()

# verbose
if args.verbose:
  for value in args.__dict__:
    printf("%12s = %s" % ("--" + value, args.__dict__[value]), "verbose")

#=======================================================================================
# Main
#=======================================================================================
# If TEXNAME, TEXDIRPATH didnt be set, then set it.
if not args.list:
  printf("Defining TEXNAME and TEXDIRPATH ...", "verbose") if args.verbose == True else None
  if typeflag["log"]:
    printf("Typeflag is log.","verbose") if args.verbose else None
    TEXNAME    = "log"
    TEXDIRPATH = LogDirPath + "/log/" + Date(args.date, dt=args.delta_days, dayofweek=0)
  elif typeflag["slide"]:
    printf("Typeflag is slide.","verbose") if args.verbose else None
    TEXNAME    = Date(args.date) + "_" + args.title.replace(" ","_")
    TEXDIRPATH = LogDirPath + "/slide/" + args.subtype.replace (" ", "_") + "/" + TEXNAME
  elif typeflag["cheatsheet"]:
    printf("Typeflag is cheatsheet.","verbose") if args.verbose else None
    TEXNAME    = args.title.replace(" ","_")
    TEXDIRPATH = LogDirPath + "/cheatsheet"
  elif typeflag["paper"]:
    printf("Typeflag is paper.","verbose") if args.verbose else None
    TEXNAME    = args.title.replace(" ","_")
    TEXDIRPATH = LogDirPath + "/paper/" + args.subtype.replace (" ", "_")
  elif typeflag["presentation"]:
    printf("Typeflag is presentation.","verbose") if args.verbose else None
    TEXNAME    = args.title.replace(" ","_")
    TEXDIRPATH = LogDirPath + "/presentation/" + args.subtype.replace (" ", "_")
  elif typeflag["book"]:
    printf("Typeflag is book.","verbose") if args.verbose else None
    TEXNAME    = args.title.replace(" ","_")
    TEXDIRPATH = LogDirPath + "/book/" + args.subtype.replace (" ", "_")
  elif typeflag["research"]:
    printf("Typeflag is research.","verbose") if args.verbose else None
    TEXNAME    = args.subtype
    TEXDIRPATH = LogDirPath + "/research/" + args.subtype
  elif typeflag["other"]:
    printf("Typeflag is other.","verbose") if args.verbose else None
    TEXNAME    = args.title.replace(" ","_")
    TEXDIRPATH = LogDirPath + "/other"
  else:
    printf("Typeflag is undefined! Exiting ...", "error")
    sys.exit()
  # Assumption: It is always ".pdf".
  printf("Assumption: TEXEXTENSION is .pdf", "verbose") if args.verbose else None
  TEXEXTENSION = ".pdf"
  if not os.path.isdir(TEXDIRPATH):
    printf("The target directory (%s) doesnt exist." % TEXDIRPATH)
    if query_yes_no("Do you really want to create it?" , default="no")=="yes":
      subprocess.check_call("mkdir -p %s" % TEXDIRPATH, stdout=subprocess.PIPE, shell=True)
    else:
      printf("You dont want to create the target directory. Exiting ...")
      sys.exit()

TEXTEXPATH = TEXDIRPATH + "/" + TEXNAME + ".tex"
TEXEXTPATH = TEXDIRPATH + "/" + TEXNAME + TEXEXTENSION
printf("The tex directory path is %s" % TEXDIRPATH, "verbose") if args.verbose else None

# Modeflag
if modeflag["create"]:
  if typeflag["log"] == True or typeflag["slide"] == True or typeflag["research"] == True:
    # Create the tex file if it doesnt exist
    if os.path.isfile(TEXTEXPATH):
      printf("The %s exists." % (TEXNAME + ".tex"))
    else:
      printf("The %s doesnt exist. Creating ..." % (TEXNAME + ".tex"))
      if typeflag["log"]:
        print_log_tex()
      elif typeflag["slide"]:
        print_slide_tex()
        subprocess.check_call("cp " + LogSrcPath + "/Nikhef-400x177.png " + TEXDIRPATH, stdout=subprocess.PIPE, shell=True)
      elif typeflag["research"]:
        print_research_tex()
      printf("The %s is created." % (TEXNAME + ".tex"), "verbose") if args.verbose else None

    time_update_before = os.path.getmtime(TEXTEXPATH)
    printf("The time of last modification before editing is %s." % datetime.fromtimestamp(time_update_before).strftime('%Y-%m-%d %H:%M:%S'), "verbose") if args.verbose else None
   
    printf("Editing %s ..." % (TEXNAME + ".tex"))
    os.system(TexEditor + " " + TEXTEXPATH + " " + TexEditorOptions)

    time_update_after = os.path.getmtime(TEXTEXPATH)
    printf("The time of last modification after editing is %s." % datetime.fromtimestamp(time_update_after).strftime('%Y-%m-%d %H:%M:%S'), "verbose") if args.verbose else None

    if (time_update_after > time_update_before):
      printf("The file get updated after editing!", "verbose") if args.verbose else None
      printf("Compiling %s ..." % (TEXNAME + ".tex"))
      os.chdir(TEXDIRPATH)
      subprocess.check_call("pdflatex -halt-on-error %s" % (TEXTEXPATH), stdout=subprocess.PIPE, shell=True)
      subprocess.check_call("pdflatex -halt-on-error %s" % (TEXTEXPATH), stdout=subprocess.PIPE, shell=True)
      printf("Compilation Done!")
    
      printf("Removing redundant files ...")
      for fileformat in TexCleanFileFormat:
        item = TEXDIRPATH + "/" + TEXNAME + "." + fileformat
        if os.path.isfile(item):
          printf("Deleting %s ..." % item, "verbose") if args.verbose else None
          subprocess.check_call("rm " + item, stdout=subprocess.PIPE, shell=True)
      printf("Removal Done!")
    else:
      printf("The tex file didnt be modified. Wont start compilation.")
  else:
    printf("Typeflag is not defined for create mode.", "error")
    sys.exit()

elif modeflag["view"]:
  if os.path.isfile(TEXEXTPATH):
    subprocess.check_call(PDFReader + " " + TEXEXTPATH, stdout=subprocess.PIPE, shell=True)
  else:
    printf("The %s doesnt exist." % TEXEXTPATH, "error")
    if query_yes_no("Do you want to list all pdf in the data directory?") == "yes":
      List(LogDirPath)
    sys.exit()

elif modeflag["copy"]:
  if os.path.exists(args.copy) and os.path.isdir(TEXDIRPATH):
    printf("cp -t %s %s" % (TEXDIRPATH, args.copy)) if args.verbose else None
    subprocess.check_call("cp -r -t %s %s" % (TEXDIRPATH, args.copy), stdout=subprocess.PIPE, shell=True)
    printf(args.copy + " is copied to " + TEXDIRPATH + " successfully.")
  else:
    printf("The path provided (%s) in copy mode or the target directory (%s) dont exist! Exiting ..." % (args.copy, TEXDIRPATH), "error")
    sys.exit()

elif modeflag["changedir"]:
  printf("Type the following command.")
  printf("cd %s" % TEXDIRPATH)

else:
  printf("Modeflag is undefined! Exiting ...","error")
  sys.exit()

