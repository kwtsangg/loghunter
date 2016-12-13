#!/usr/bin/python                                                                                                                                                                                            
__file__       = "logtodo"
__author__     = "Ka Wa Tsang"
__copyright__  = "Copyright 2016"
__version__    = "1.0.1"
__email__      = "kwtsang@nikhef.nl"
__data__       = "2016 Dec 13"

"""
  Name:
       logtodo
  Author:
       Ka Wa TSANG
"""
Description=""" A program to output the todo list to the terminal.
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
LogDirPath="/home/kwtsang/OneDrive_CUHK/mle/loghunter"
RelSrcPath="src"

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
# Logtodo function
#=======================================================================================
def getToDoList(IntendDate):
  TEXDIRPATH = LogDirPath + "/data/log/" + IntendDate
  if os.path.isfile(TEXDIRPATH+"/log.tex"):
    # Initialization
    TEXOBJECT = open(TEXDIRPATH+"/log.tex", "r")
    ToDoList  = []
    ToDoListSectionString = r"\section{To do list}"
    ToDoListSectionCount  = 0
    BeginItemizeString    = r"\begin{itemize}"
    EndItemizeString      = r"\end{itemize}"
    BeginItemizeCount     = 0
    EndItemizeCount       = 0
    
    # Getting the ToDoList
    for line in TEXOBJECT:
      if line.replace('\n','') == ToDoListSectionString:
        ToDoListSectionCount = 1
      elif ToDoListSectionCount == 1:
        if line.replace(' ','').replace('\n','') == BeginItemizeString:
          BeginItemizeCount = BeginItemizeCount + 1
        elif line.replace(' ','').replace('\n','') == EndItemizeString:
          EndItemizeCount   = EndItemizeCount   + 1
        elif BeginItemizeCount == EndItemizeCount and BeginItemizeCount != 0:
          break
        else:
          ToDoList.append(line.replace('\n',''))

    # Return output
    return ToDoList
  else:
    printf("The tex of date %s doesnt exist." % IntendDate, "warning")
    printf("Returning empty ToDoList string ...", "warning")
    return []

#=======================================================================================
# Main
#=======================================================================================

def main():
  ToDoList = getToDoList(Date(args.date, dt=args.delta_days, dayofweek=0))
  for item in ToDoList:
    print item.replace('\item','')

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description=textwrap.dedent(Description), prog=__file__, formatter_class=argparse.RawTextHelpFormatter)
  parser.add_argument("-d ", "--date"      , default=datetime.today().strftime("%Y%m%d"), action="store", type=int, help="Date in YYYYMMDD format. (default: today)")
  parser.add_argument("-dt", "--delta-days", default=0                                  , action="store", type=int, help="Number of days before/after the --date. eg. -1 means yesterday.")
  parser.add_argument(       "--verbose"   , default=False, action="store_true", help="Print more messages.")
  parser.add_argument(       "--version"   ,                action="version", version='%(prog)s ' + __version__)
  args = parser.parse_args()

  main()
