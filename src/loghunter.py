#!/usr/bin/python
__file__       = "loghunter"
__author__     = "Ka Wa Tsang"
__copyright__  = "Copyright 2016"
__version__    = "1.0.1"
__email__      = "kwtsang@nikhef.nl"

"""
  Name:
       loghunter
  Author:
       Ka Wa TSANG
"""
Description="""
       A program to 1) create tex                 (log, slide)
                    2) view pdf                   (log, slide, cheatsheet, paper)
                    3) copy files to folder       (log, slide, cheatsheet, paper)
                    4) change directory to folder (log, slide, cheatsheet, paper) 

       Default 1) type is log 
               2) mode is create

       Example Usage 1) loghunter             To create the log of this week
                     2) loghunter -v          To view the log pdf of this week
                     3) loghunter -v -dt -7   To view the log pdf of last week
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

LogDirPath="/home/kwtsang/OneDrive_CUHK/mle/loghunter"
RelSrcPath="src"
PDFReader="okular"
TexEditor="vim"
TexEditorOptions="+26"

# Global Variable
TexCleanFileFormat=[ "log", "aux", "out", "nav", "snm", "toc", "dvi" ]

#=======================================================================================
# General Function
#=======================================================================================
def printf(str, type="msg"):
  print "log %s :: %s" % ( type, str )

def Date(date, dt=0, dayofweek=None, dateformat="%Y%m%d"):
  # To obtain the date of the weekday of the input date.
  d = datetime.strptime(str(date),"%Y%m%d") + timedelta(days=dt)
  if isinstance( dayofweek, int ):
    if d.isoweekday() == 7:
      isoweekday = 0;
    else:
      isoweekday = d.isoweekday()
    d = ( d - timedelta(days=isoweekday+dayofweek) )
  return d.strftime(dateformat)

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

  TEXOBJECT.write('%s\n' % (r"\section{Question}"))
  TEXOBJECT.write('%s\n' % (r"\begin{itemize}"))
  TEXOBJECT.write('%s\n' % (r"  \item "))
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
  TEXOBJECT.write('%s\n' % (r"\date[" + Date(args.date, dt=args.delta_days, dateformat="%Y %b %d") + "]{" + args.slidetype.replace ("_", " ") + ", " + Date(args.date, dt=args.delta_days, dateformat="%Y %b %d" + "}")))
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


#=======================================================================================
# Preliminary
#=======================================================================================

parser = argparse.ArgumentParser(description=textwrap.dedent(Description), prog=__file__, formatter_class=argparse.RawTextHelpFormatter)
parser.add_argument("-d" , "--date"      , default=datetime.today().strftime("%Y%m%d"), action="store", type=int, help="Date in YYYYMMDD format. (default: today)")
parser.add_argument("-dt", "--delta-days", default=0                                  , action="store", type=int, help="Number of days before/after the --date. eg. -1 means yesterday.")

parser.add_argument("-s" , "--slide"     , default=False                              , action="store_true", help="Type: slide. Please include --date, --slidetype and --title.")
parser.add_argument("-st", "--slidetype" , default="group meeting", choices=["group meeting","conference","CBC meeting"], action="store", help="Classification of the slide.")
parser.add_argument("-t" , "--title"                                                  , action="store")
parser.add_argument("-c" , "--cheatsheet", default=False                              , action="store_true", help="Type: cheatsheet. Please include --title.")
parser.add_argument("-p" , "--paper"     , default=False                              , action="store_true", help="Type: paper. Please include --title.")

parser.add_argument("-v ", "--view"      , default=False                              , action="store_true", help="Mode: view the pdf.")
parser.add_argument("-cp", "--copy"                                                   , action="store"     , help="Mode: copy files to folder.")
parser.add_argument("-cd", "--changedir" , default=False                              , action="store_true", help="Mode: change directory to folder.")
parser.add_argument("-l" , "--list"      , const="all", nargs='?', choices=["all","log","slide","cheatsheet","paper"], action="store", help="List pdf contents (default: all) and exit.")

parser.add_argument(       "--verbose"   , default=False                              , action="store_true", help="Print more messages.")
parser.add_argument(       "--version"   ,                                              action="version", version='%(prog)s ' + __version__)
args = parser.parse_args()

# --list first
if args.list:
  subprocess.check_call("ls %s/data/log/*/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True) if args.list=="all" or args.list=="log" else None
  subprocess.check_call("ls %s/data/slide/*/*/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True) if args.list=="all" or args.list=="slide" else None
  subprocess.check_call("ls %s/data/cheatsheet/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True) if args.list=="all" or args.list=="cheatsheet" else None
  subprocess.check_call("ls %s/data/paper/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True) if args.list=="all" or args.list=="paper" else None
  sys.exit()

# Check arguments
args.date=Date(args.date)

# Set default type to be "log"
typeflag = { "log":False, "slide":args.slide, "cheatsheet":args.cheatsheet, "paper":args.paper }
if sum(typeflag.values()) == 0:
  typeflag["log"] = True
elif sum(typeflag.values()) > 1:
  printf("Typeflag is %s" % typeflag, "err")
  printf("More than one type", "err")
  sys.exit()

for key, value in typeflag.iteritems():
  if key != "log" and value == True  and args.title == None:
    printf("Type %s requires --title" % key, "err")
    sys.exit()

# Set default mode to be "create"
if args.copy:
  copyflag = True
else:
  copyflag = False
modeflag = { "create":False, "view":args.view, "copy":copyflag, "changedir":args.changedir }
if sum(modeflag.values()) == 0:
  modeflag["create"] = True
elif sum(modeflag.values()) > 1:
  printf("Modeflag is %s" % modeflag, "err")
  printf("More than one mode.", "err")
  sys.exit()


if args.verbose:
  for value in args.__dict__:
    printf("--%s = %s" % (value, args.__dict__[value]), "verbose")


#=======================================================================================
# Main
#=======================================================================================
# Setup TexName, TexPdfPath etc.
if typeflag["log"]:
  printf("Tex type is log","verbose") if args.verbose else None
  TEXNAME    = "log"
  TEXDIRPATH = LogDirPath + "/data/log/" + Date(args.date, dt=args.delta_days, dayofweek=0)
elif typeflag["slide"]:
  printf("Tex type is slide","verbose") if args.verbose else None
  TEXNAME    = Date(args.date) + "_" + args.title.replace(" ","_")
  TEXDIRPATH = LogDirPath + "/data/slide/" + args.slidetype.replace (" ", "_") + "/" + TEXNAME
elif typeflag["cheatsheet"]:
  printf("Tex type is cheatsheet","verbose") if args.verbose else None
  TEXNAME    = args.title.replace(" ","_")
  TEXDIRPATH = LogDirPath + "/data/cheatsheet"
  subprocess.check_call("mkdir -p %s" % TEXDIRPATH, stdout=subprocess.PIPE, shell=True)
elif typeflag["paper"]:
  printf("Tex type is paper","verbose") if args.verbose else None
  TEXNAME    = args.title.replace(" ","_")
  TEXDIRPATH = LogDirPath + "/data/paper"
  subprocess.check_call("mkdir -p %s" % TEXDIRPATH, stdout=subprocess.PIPE, shell=True)
else:
  printf("Typeflag is undefined", "err")
  sys.exit()

TEXFILE    = TEXNAME + ".tex"
TEXTEXPATH = TEXDIRPATH + "/" + TEXFILE
TEXPDFPATH = TEXDIRPATH + "/" + TEXNAME + ".pdf"
printf("The tex directory path is %s" % TEXDIRPATH, "verbose") if args.verbose else None

# Modeflag
if modeflag["create"]:
  if typeflag["log"] == True or typeflag["slide"] == True:
    # Create the tex file if it doesnt exist
    if os.path.isfile(TEXTEXPATH):
      printf("The %s exists" % TEXFILE)
    else:
      printf("The %s doesnt exist. Creating ..." % TEXFILE)
      subprocess.check_call("mkdir -p %s" % TEXDIRPATH, stdout=subprocess.PIPE, shell=True)
      if typeflag["log"]:
        print_log_tex()
      elif typeflag["slide"]:
        print_slide_tex()
        subprocess.check_call("cp " + LogDirPath + "/" + RelSrcPath + "/Nikhef-400x177.png " + TEXDIRPATH, stdout=subprocess.PIPE, shell=True)
      printf("The %s is created" % TEXFILE, "verbose") if args.verbose else None
   
    printf("Editing %s ..." % TEXFILE)
    os.system(TexEditor + " " + TEXTEXPATH + " " + TexEditorOptions)
  
    printf("Compiling %s ..." % TEXFILE)
    os.chdir(TEXDIRPATH)
    subprocess.check_call("pdflatex -halt-on-error %s" % (TEXTEXPATH), stdout=subprocess.PIPE, shell=True)
    subprocess.check_call("pdflatex -halt-on-error %s" % (TEXTEXPATH), stdout=subprocess.PIPE, shell=True)
    printf("Compilation Done!")
  
    printf("Removing redundant files ...")
    for fileformat in TexCleanFileFormat:
      item = TEXDIRPATH + "/" + TEXNAME + "." + fileformat
      if os.path.isfile(item):
        printf("Deleting %s" % item, "verbose") if args.verbose else None
        subprocess.check_call("rm " + item, stdout=subprocess.PIPE, shell=True)
    printf("Removal Done!")
  else:
    printf("Typeflag is not defined for create mode", "err")
    sys.exit()

elif modeflag["view"]:
  if os.path.isfile(TEXPDFPATH):
    subprocess.check_call(PDFReader + " " + TEXPDFPATH, stdout=subprocess.PIPE, shell=True)
  else:
    printf("The %s.pdf doesnt exist." % TEXNAME, "err")
    printf("All pdf in the folder will be listed")
    print ""
    subprocess.check_call("ls %s/data/log/*/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True) 
    subprocess.check_call("ls %s/data/slide/*/*/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True)
    subprocess.check_call("ls %s/data/cheatsheet/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True)
    subprocess.check_call("ls %s/data/paper/*.pdf | awk '{print $1}' | sed 's/^/%s /g'" % (LogDirPath, PDFReader), shell=True)
    sys.exit()

elif modeflag["copy"]:
  printf("cp -t %s %s" % (TEXDIRPATH, args.copy)) if args.verbose else None
  subprocess.check_call("cp -r -t %s %s" % (TEXDIRPATH, args.copy), stdout=subprocess.PIPE, shell=True)
  printf(args.copy + " is copied to " + TEXDIRPATH + " successfully")

elif modeflag["changedir"]:
  printf("Type the following command")
  print "cd %s" % TEXDIRPATH

else:
  printf("Modeflag is undefined","err")
  sys.exit()

