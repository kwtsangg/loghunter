# This program is used to record the log.

# Place the program in where you want
# Modify the LogDirPath in each file (logcreate.sh, logview.sh)

# Add the following line to the .bashrc
export LogDirPath="/mnt/c/Users/kwtsang/Desktop/OneDrive_CUHK/mle/log"

alias logcreate="sh ${LogDirPath}/src_surface/logcreate.sh"
alias logview="source ${LogDirPath}/src_surface/logview.sh"
alias logcombine="pdftk $(ls -l ${LogDirPath}/data/log/ | grep ^d | awk '{print $9}' | sed "s:^:${LogDirPath}/data/log/:g" | sed "s:$:/log.pdf:g" | tr '\n' ' ') cat output ${LogDirPath}/data/log/logcombine.pdf"
alias logreport="evince ${LogDirPath}/data/log/logcombine.pdf"
alias loglistdir="find ${LogDirPath}/data/ -type d | sed "s:${LogDirPath}/data::""
alias loglistpdf="find ${LogDirPath}/data/ | sed "s:${LogDirPath}/data::" | grep .pdf | awk '{print $1}'"
alias logcd="cd ${LogDirPath}/data/"
alias logtodo="sh ${LogDirPath}/src_surface/logtodo.sh"

# Ka Wa
# 20161113
