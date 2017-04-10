# Add the following line to the .bashrc

# loghunter
export LogSrcPath="/home/kwtsang/OneDrive_CUHK/mle/loghunter/src" 
export LogDataPath="/home/kwtsang/Dropbox/loghunter_data"
alias loghunter="python ${LogSrcPath}/loghunter.py"
alias logcombine="pdftk `ls -l ${LogDataPath}/log/ | grep ^d | awk '{print $9}' | sed "s:^:${LogDataPath}/log/:g" | sed "s:$:/log.pdf:g" | tr '\n' ' '` cat output ${LogDataPath}/log/logcombine.pdf"
alias logreport="okular ${LogDataPath}/log/logcombine.pdf"
alias logcd="cd ${LogDataPath}"
alias logtodo="sh ${LogSrcPath}/logtodo.sh"

# Ka Wa
# 20170410
