# Add the following line to the .bashrc

# loghunter
export LogDirPath="/home/kwtsang/OneDrive_CUHK/mle/loghunter"
export LogRelSrcPath="src"
 
alias loghunter="python ${LogDirPath}/${LogRelSrcPath}/loghunter.py"
alias logcombine="pdftk `ls -l ${LogDirPath}/data/log/ | grep ^d | awk '{print $9}' | sed "s:^:${LogDirPath}/data/log/:g" | sed "s:$:/log.pdf:g" | tr '\n' ' '` cat output ${LogDirPath}/data/log/logcombine.pdf"
alias logreport="okular ${LogDirPath}/data/log/logcombine.pdf"
alias logcd="cd ${LogDirPath}/data/"
alias logtodo="sh ${LogDirPath}/${LogRelSrcPath}/logtodo.sh"

# Ka Wa
# 20161127
