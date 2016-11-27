#!/bin/bash
#=======================================================================================
#  Name:
#       logview
#  Author:
#       Ka Wa TSANG
#  Description:
#       A program to view the log. (and cd, cp)
#  History:
#       05-Nov-2016 First version.
#                   Added new alias (loglist) for slidemode mostly.
#                   Typeflag = 0 represents log. (default)
#                            = 1 represents cheatsheet.
#                            = 2 represents slide.
#                   Modeflag = 0 represents view. (default)
#                            = 1 represents cd.
#                            = 2 represents cp.
#       06-Nov-2016 Simple help is added.
#=======================================================================================
# Pre-Function
#=======================================================================================
  EchoMsg()
  {
    echo "logview msg  ::  $1"
    #echo -e "\e[92m logview msg  ::  $1 \e[0m"
  }
  EchoErr()
  {
    echo "logview err  ::  $1"
    #echo -e "\e[41m logview err  ::  $1 \e[0m"
  }
#=======================================================================================
# Pre-Main
#=======================================================================================
  #Initialization
  PDFviewer=evince
  LogDirPath="/mnt/c/Users/kwtsang/Desktop/OneDrive_CUHK/mle/log"
  Date=$(date +%Y%m%d)
  Typeflag=0
  Modeflag=0
  unset FileToBeCopied
  unset SlideTitle
  SlideType="weekly meeting"
  HelpMode=0
  
  # Pass the argument into the script
  while [ $# -gt 0 ]
    do
      key="$1"

      case $key in
        -d|--date)
        Date="$2"
        ;;
        -c|--cheatsheet)
        Typeflag=1
        ;;
        -s|--slide)
        Typeflag=2
        SlideTitle="$2"
        ;;
        -st|--slidetype)
        SlideType="$2"
        ;;
        -cd)
        Modeflag=1
        ;;
        -cp|--copy)
        Modeflag=2
        FileToBeCopied="$2"
        ;;
        -h|--help)
        HelpMode=1
        EchoMsg "========================================================"
        EchoMsg "Options available  :              Remarks               "
        EchoMsg "========================================================"
        EchoMsg "-d  | --date       : arg, today (Default)               " 
        EchoMsg "                   :      (Use YYYYMMDD format!)        "
        EchoMsg "                   : arg, -7  means lastweek            "
        EchoMsg "                   : arg, -14 means lastlastweek        " 
        EchoMsg "                   : arg, -21 means lastlastlastweek    "        
        EchoMsg "-c  | --cheatsheet :                                    "
        EchoMsg "-s  | --slide      : arg, SlideTitle                    "
        EchoMsg "-st | --slidetype  : arg, weekly meeting (Default)      "
        EchoMsg "-cd                :      for entering the DIR          "
        EchoMsg "-cp | --copy       : arg, for copying files to the DIR  "
        EchoMsg "========================================================"
        ;;
        *)
          # unknown option
        ;;
      esac
    shift
  done
  if [ ${HelpMode} -eq 0 ]; then
    # Check whether the date is an integer
    if [ ${Date} -ne 0 -o ${Date} -eq 0 2>/dev/null ]; then
      wait
    else
      EchoErr "The date is not an integer."
      EchoMsg "The value entered in --date is ignored."
      EchoMsg "The date is set to be today."
      Date=$(date +%Y%m%d)
    fi
#=======================================================================================
# Main
#=======================================================================================  
    # Default value
    TargetPDFName="log.pdf"
    TargetDirPath="${LogDirPath}/data/log/$(date +"%Y%m%d" -d "$(( $(date +%w) )) days ago")"
    
    # Set appropriate TargetDirPath and TargetPDFName
    if [ ${Typeflag} -eq 0 ]; then   
      if [ ${Date} -eq -7   ]; then
        TargetDirPath="${LogDirPath}/data/log/$(date +"%Y%m%d" -d "$(( $(date +%w) + 7 )) days ago")"
      elif [ ${Date} -eq -14 ]; then
        TargetDirPath="${LogDirPath}/data/log/$(date +"%Y%m%d" -d "$(( $(date +%w) + 14 )) days ago")"
      elif [ ${Date} -eq -21 ]; then
        TargetDirPath="${LogDirPath}/data/log/$(date +"%Y%m%d" -d "$(( $(date +%w) + 21 )) days ago")"
      fi
    elif [ ${Typeflag} -eq 1 ]; then
      TargetPDFName="cheatsheet.pdf"
      TargetDirPath="${LogDirPath}/data/cheatsheet"
    elif [ ${Typeflag} -eq 2 ]; then
      SlideTitle_wo_space=$(echo ${SlideTitle} | sed "s/ /_/g")
      SlideType_wo_space=$(echo ${SlideType} | sed "s/ /_/g")
      TargetPDFName="${Date}_${SlideTitle_wo_space}.pdf"
      TargetDirPath="${LogDirPath}/data/slide/${SlideType_wo_space}/${Date}_${SlideTitle_wo_space}"
    fi
   
    # Execute the corresponding mode
 
    if [ ${Modeflag} -eq 0 ]; then
      ${PDFviewer} ${TargetDirPath}/${TargetPDFName}
    elif [ ${Modeflag} -eq 1 ]; then
      cd ${TargetDirPath}
    elif [ ${Modeflag} -eq 2 ]; then
      cp -t ${TargetDirPath} -r ${FileToBeCopied}
      EchoMsg "${FileToBeCopied} is copied to ${TargetDirPath}."
    fi
  fi
#=======================================================================================
# End
#=======================================================================================