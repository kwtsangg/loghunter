# Add the following line to the .bashrc
export LogDirPath="/home/kwtsang/OneDrive_CUHK/mle/loghunter"
 
alias loghunter="python ${LogDirPath}/src_medion_linux/loghunter.py"
alias logcombine="pdftk $(ls -l ${LogDirPath}/data/log/ | grep ^d | awk '{print $9}' | sed "s:^:${LogDirPath}/data/log/:g" | sed "s:$:/log.pdf:g" | tr '\n' ' ') cat output ${LogDirPath}/data/log/logcombine.pdf"
alias logreport="okular ${LogDirPath}/data/log/logcombine.pdf"
alias logcd="cd ${LogDirPath}/data/"
alias logtodo="sh ${LogDirPath}/src_medion_linux/logtodo.sh"

# Ka Wa
# 20161125
