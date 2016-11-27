#!/bin/bash
#=======================================================================================
#  Name:
#       logcreate
#  Author:
#       Ka Wa TSANG
#  Description:
#       A program to create the log tex. (and cheatsheet tex, slide tex.)
#  History:
#       22-Sep-2016 First version.
#       23-Sep-2016 Arbitrary date of log can be added through -d.
#       25-Sep-2016 echo color added. Red for err and Green for msg.
#                   More checks are applyed on the date entered.
#       28-Sep-2016 Modified the log template. 
#                   Added vim +25 option.
#       30-Sep-2016 Added an error msg if compilation fails.
#       01-Oct-2016 Added a friendly option for -d/--date. eg. -d -7 means last week.
#                   Added Initialization.
#       07-Oct-2016 log.pdf is renamed to be log_old.pdf before compilation.
#                   If compilation fails, log_old.pdf -> log.pdf
#                   If compilation runs successfully, rm log_old.pdf
#       16-Oct-2016 New alias (logcombine, logreport) are added
#                   Tex report -> article
#       20-Oct-2016 Added physics package
#       05-Nov-2016 Typeflag (first version) is added.
#                   Typeflag = 0 represents log. (default)
#                            = 1 represents cheatsheet.
#                            = 2 represents slide.
#                   First version of logview.sh, used for view, cd, cp.
#       06-Nov-2016 Simple help is added.
#=======================================================================================
# Pre-Function
#=======================================================================================
  EchoMsg()
  {
    echo "log msg  ::  $1"
    #echo -e "\e[92m log msg  ::  $1 \e[0m"
  }
  EchoErr()
  {
    echo "log err  ::  $1"
    #echo -e "\e[41m log err  ::  $1 \e[0m"
  }
#=======================================================================================
# Pre-Main
#=======================================================================================
  EchoMsg "========================================================"

  #Initialization
  LogDirPath="/mnt/c/Users/kwtsang/Desktop/OneDrive_CUHK/mle/log"
  Date=$(date +%Y%m%d)
  Typeflag=0
  SlideType="weekly meeting"

  # Pass the argument into the script
  while [ $# -gt 0 ]
    do
      key="$1"

      case $key in
        -d|--date)
        Date="$2"
        EchoMsg "You entered '--date' to be '${Date}'."
        ;;
        -c|--cheatsheet)
        Typeflag=1
        EchoMsg "Typeflag is set to be ${Typeflag}. CheatSheet mode is turned on."
        ;;
        -s|--slide)
        Typeflag=2
        EchoMsg "Typeflag is set to be ${Typeflag}. Slide mode is turned on."
        SlideTitle="$2"
        EchoMsg "The slide title is set to be '${SlideTitle}'."
        ;;
        -st|--slidetype)
        SlideType="$2"
        EchoMsg "You entered '--slidetype' to be '${SlideType}'."
        ;;
        -h|--help)
        EchoMsg "Options available  :              Remarks               "
        EchoMsg "========================================================"
        EchoMsg "-d  | --date       : arg, today (Default)               "
        EchoMsg "                   :      (Use YYYYMMDD format!)        "
        EchoMsg "                   :      friendly option available     "  
        EchoMsg "                   :        eg. -6 means six days ago   "
        EchoMsg "-c  | --cheatsheet :                                    "
        EchoMsg "-s  | --slide      : arg, SlideTitle                    "
        EchoMsg "-st | --slidetype  : arg, weekly meeting (Default)      "
        EchoMsg "========================================================"
        exit 0
        ;;
        *)
          # unknown option
        ;;
      esac
    shift
  done
  
  # Check whether the date is an integer
  if [ ${Date} -ne 0 -o ${Date} -eq 0 2>/dev/null ]; then
    wait
  else
    EchoErr "The date is not an integer."
    exit 1
  fi
  
  # Choose the correct texdatapath according to Typeflag
  if [ ${Typeflag} -eq 0 ]; then
      # Clean up variables 
      WeekdayNo=0
      DayDiffFromToday=0
      TotalDayDiff=0
      SundayDate=0
    
      # Initialization
      FriendlyOptionRange=2000
      PhDStartDate=20160901
      
      # Friendly option of -d/--date
      if [ ${Date} -lt ${FriendlyOptionRange} -a ${Date} -gt $(( ${FriendlyOptionRange}*-1 )) ]; then
          Date=$(date -d "$(( -1*${Date} )) days ago" +%Y%m%d)
      fi
      
      EchoMsg "The date is set to be ${Date}."
      
      # Check whether the date is in the chosen range
      if [ ${Date} -lt ${PhDStartDate} ]; then
          EchoErr "The date is before your PhD started."
          exit 1
      elif [ ${Date} -gt $(date +%Y%m%d) ]; then
          EchoErr "The date is in the future."
          exit 1
      fi
      
      # Set up the log data path 
      WeekdayNo=$(date -d ${Date} +%w)
      DayDiffFromToday=$(( ($(date +%s) - $(date -d ${Date} +%s))/60/60/24 ))
      TotalDayDiff=$(( ${WeekdayNo}+${DayDiffFromToday} ))
      SundayDate=$(date -d "${TotalDayDiff} days ago" +%Y%m%d)
      
      # Check whether the date of Sunday is indeed on Sunday
      if [ $(date -d ${SundayDate} +%w) -ne 0 2>/dev/null ]; then
          EchoErr "Please make sure the date entered is a valid date with YYYYMMDD format."
          exit 1
      fi
      
      EchoMsg "The date of Sunday of that week is ${SundayDate}."
      
      # Create the log directory at that week
      TEXNAME=log
      TEXFILE=${TEXNAME}.tex
      TEXDIRPATH=${LogDirPath}/data/log/${SundayDate}/
  elif [ ${Typeflag} -eq 1 ]; then
      TEXNAME=cheatsheet
      TEXFILE=${TEXNAME}.tex
      TEXDIRPATH=${LogDirPath}/data/cheatsheet/
  elif [ ${Typeflag} -eq 2 ]; then
      SlideTitle_wo_space=$(echo ${SlideTitle} | sed "s/ /_/g")
      SlideType_wo_space=$(echo ${SlideType} | sed "s/ /_/g")
      TEXNAME=${Date}_${SlideTitle_wo_space} 
      TEXFILE=${TEXNAME}.tex
      TEXDIRPATH=${LogDirPath}/data/slide/${SlideType_wo_space}/${TEXNAME}
  else
      EchoErr "Selected Typeflag doesnt exist."
      exit 1
  fi
    
  mkdir -p ${TEXDIRPATH}
  cd ${TEXDIRPATH}
#=======================================================================================
# Functions
#=======================================================================================
logtex_print_template()
{
    printf '%s\n' "\documentclass[a4paper,12pt]{article}" 
    printf '%s\n' "\usepackage{geometry}"
    printf '%s\n' "\usepackage{graphicx}"
    printf '%s\n' "\usepackage{amsmath}"
    printf '%s\n' "\usepackage{hyperref}"
    printf '%s\n' "\usepackage{physics}"
    printf '%s\n' "\usepackage{url}"
    printf '%s\n' "\geometry{"
    printf '%s\n' " a4paper,"
    printf '%s\n' " total={170mm,257mm},"
    printf '%s\n' " left=20mm,"
    printf '%s\n' " top=20mm,"
    printf '%s\n' "}"
    printf '%s\n' ""
    
    printf '%s\n' "%Title page"
    printf '%s\n' "\title{Work log}"
    printf '%s\n' "\author{Ka Wa TSANG}"
    printf '%s\n' "\date{$(date -d ${SundayDate} +%Y-%m-%d)}"
    printf '%s\n' ""
    
    printf '%s\n' "\begin{document}" 
    printf '%s\n' "\maketitle"
    printf '%s\n' ""
    
    printf '%s\n' "%Contents"

    printf '%s\n' "\section{Summary}"
    printf '%s\n' "\begin{itemize}"
    printf '%s\n' "\item "
    printf '%s\n' "\end{itemize}"
    printf '%s\n' ""

    printf '%s\n' "\section{To do list}"
    printf '%s\n' "\begin{itemize}"
    printf '%s\n' "  \item [ ] H:"
    printf '%s\n' "  \item [ ] M:"
    printf '%s\n' "  \item [ ] L:"
    printf '%s\n' "\end{itemize}"
    printf '%s\n' ""

    printf '%s\n' "\section{Question}"
    printf '%s\n' "\begin{itemize}"
    printf '%s\n' "  \item "
    printf '%s\n' "\end{itemize}"
    printf '%s\n' ""

    printf '%s\n' "" 
    printf '%s\n' "\end{document}"    
} >> $TEXFILE

cheatsheettex_print_template()
{
    printf '%s\n' "\documentclass[a4paper,12pt]{article}" 
    printf '%s\n' "\usepackage{geometry}"
    printf '%s\n' "\usepackage{graphicx}"
    printf '%s\n' "\usepackage{amsmath}"
    printf '%s\n' "\usepackage{hyperref}"
    printf '%s\n' "\usepackage{physics}"
    printf '%s\n' "\usepackage{url}"
    printf '%s\n' "\geometry{"
    printf '%s\n' " a4paper,"
    printf '%s\n' " total={170mm,257mm},"
    printf '%s\n' " left=20mm,"
    printf '%s\n' " top=20mm,"
    printf '%s\n' "}"
    printf '%s\n' ""
    
    printf '%s\n' "%Title page"
    printf '%s\n' "\title{Cheat sheet}"
    printf '%s\n' "\author{Ka Wa TSANG}"
    printf '%s\n' "\date{$(date +%Y-%m-%d)}"
    printf '%s\n' ""

    printf '%s\n' "\begin{document}"    
    printf '%s\n' "\maketitle"
    printf '%s\n' ""
    
    printf '%s\n' "%Contents"

    printf '%s\n' "\section{}"
    printf '%s\n' "" 
    printf '%s\n' "" 

    printf '%s\n' "" 
    printf '%s\n' "\end{document}"
} >> $TEXFILE

slidetex_print_template()
{
  printf '%s\n' "\documentclass{beamer}"
  printf '%s\n' "\usepackage[utf8]{inputenc}"
  printf '%s\n' "\usepackage{graphicx}"
  printf '%s\n' "\usepackage{physics}"
  printf '%s\n' "\usetheme{Madrid}"
  printf '%s\n' ""
  
  printf '%s\n' "\title[TitleShortHand]{${SlideTitle}}"
  printf '%s\n' "\subtitle{Subtitle}"
  printf '%s\n' "\author{Ka Wa TSANG}"
  printf '%s\n' "\institute[Nikhef]{National Institute for Subatomic Physics (Nikhef)}"
  printf '%s\n' "\date[$(date -d "${Date}" +%Y-%b-%d)]{${SlideType}, $(date -d "${Date}" +%Y-%b-%d)}"
  printf '%s\n' "\titlegraphic{\includegraphics[width=3cm, keepaspectratio]{imgs/Nikhef-400x177.png}}"
  printf '%s\n' ""
  
  printf '%s\n' "\begin{document}"
  printf '%s\n' ""
  
  printf '%s\n' "\section{Title Page}"
  printf '%s\n' "%==================================="
  printf '%s\n' "\begin{frame}"
  printf '%s\n' "\titlepage"
  printf '%s\n' "\end{frame}"
  printf '%s\n' "%==================================="
  printf '%s\n' ""
  
  printf '%s\n' "\section{Contents}"
  printf '%s\n' "%==================================="
  printf '%s\n' "\begin{frame}"
  printf '%s\n' "\frametitle{Table of Contents}"
  printf '%s\n' "\begin{enumerate}"
  printf '%s\n' "  \item "
  printf '%s\n' "\end{enumerate}"
  printf '%s\n' "\end{frame}"
  printf '%s\n' "%==================================="
  printf '%s\n' "" 
  
  printf '%s\n' "\section{Motivation}"
  printf '%s\n' "%==================================="
  printf '%s\n' "\begin{frame}"
  printf '%s\n' "\frametitle{Motivation}"  
  printf '%s\n' ""
  printf '%s\n' "\end{frame}" 
  printf '%s\n' "%==================================="
  printf '%s\n' ""   

  printf '%s\n' "\section{Backup}"  
  printf '%s\n' "%==================================="
  printf '%s\n' "\begin{frame}"
  printf '%s\n' "\frametitle{Backup}"
  printf '%s\n' "Thank you!"
  printf '%s\n' "\Huge{\centerline{The End}}"
  printf '%s\n' "\end{frame}"
  printf '%s\n' "%==================================="
  printf '%s\n' ""
  printf '%s\n' ""
  printf '%s\n' "\end{document}"
} >> $TEXFILE

create_tex()
{
  # create the tex file if it doesnt exist
  if [ ! -f "${TEXFILE}" ] ; then
      EchoMsg "The ${TEXFILE} doesnt exist. Creating ..."
      touch "${TEXFILE}"
      
      # print the appropriate template
      if [ ${Typeflag} -eq 0 ]; then
          logtex_print_template
      elif [ ${Typeflag} -eq 1 ]; then
          cheatsheettex_print_template
      elif [ ${Typeflag} -eq 2 ]; then
          slidetex_print_template
          cp -r ${LogDirPath}/src_surface/imgs/ .
      else
          EchoErr "Selected Typeflag doesnt exist."
          exit 1
      fi
  else
      EchoMsg "The ${TEXFILE} exists."
  fi
}
#=======================================================================================
# Main
#=======================================================================================
  create_tex

  EchoMsg "Editing the log tex ..."
  vim ${TEXFILE} +26
  
  if [ -f "${TEXNAME}.pdf" ] ; then
      mv ${TEXNAME}.pdf ${TEXNAME}_old.pdf
  fi
  
  EchoMsg "Compiling the log tex ..."
  pdflatex -interaction batchmode -halt-on-error ${TEXFILE}
  pdflatex -interaction batchmode -halt-on-error ${TEXFILE}

  if [ ! -f "${TEXNAME}.pdf" ] ; then
      EchoErr "Compilation error occurs. Check the ${TEXFILE} again."
      if [ -f "${TEXNAME}_old.pdf" ] ; then
          mv ${TEXNAME}_old.pdf ${TEXNAME}.pdf
      fi
  else
      EchoMsg "Compiling Done!"
      if [ -f "${TEXNAME}_old.pdf" ] ; then
          rm ${TEXNAME}_old.pdf
      fi
  fi
  
  EchoMsg "Removing redundant files ..."
  rm -f ${TEXNAME}.log ${TEXNAME}.aux ${TEXNAME}.out ${TEXNAME}.nav ${TEXNAME}.snm ${TEXNAME}.toc ${TEXNAME}.dvi

  cd -
  EchoMsg "========================================================"
#=======================================================================================
# End
#=======================================================================================