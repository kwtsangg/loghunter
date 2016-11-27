#=======================================================================================
#  Name:
#       logtodo
#  Author:
#       Ka Wa TSANG
#  Description:
#       A program to view the "To do list" in log.tex
#  History:
#       13-Nov-2016 First version.
#=======================================================================================

# Initialization
LogDirPath="/home/kwtsang/OneDrive_CUHK/mle/loghunter"

# Main
SundayDate=$(date +%Y%m%d -d "$(( $(date +%w) )) days ago")
echo "======================================================================"
echo "To do lists:"
echo "Not yet done:"
cat $LogDirPath/data/log/${SundayDate}/log.tex | sed -n 's:.*item\ \[\ \]\ H\:\(.*\)\.*:\1:p' | sed "s/^/\[\ \]\ H:/g"
echo " --- "
cat $LogDirPath/data/log/${SundayDate}/log.tex | sed -n 's:.*item\ \[\ \]\ M\:\(.*\)\.*:\1:p' | sed "s/^/\[\ \]\ M:/g"
echo " --- "
cat $LogDirPath/data/log/${SundayDate}/log.tex | sed -n 's:.*item\ \[\ \]\ L\:\(.*\)\.*:\1:p' | sed "s/^/\[\ \]\ L:/g"
echo ""
echo "Finished:"
cat $LogDirPath/data/log/${SundayDate}/log.tex | sed -n 's:.*item\ \[V\]\ H\:\(.*\)\.*:\1:p' | sed "s/^/\[\V\]\ H:/g"
echo " --- "
cat $LogDirPath/data/log/${SundayDate}/log.tex | sed -n 's:.*item\ \[V\]\ M\:\(.*\)\.*:\1:p' | sed "s/^/\[\V\]\ M:/g"
echo " --- "
cat $LogDirPath/data/log/${SundayDate}/log.tex | sed -n 's:.*item\ \[V\]\ L\:\(.*\)\.*:\1:p' | sed "s/^/\[\V\]\ L:/g"
echo "======================================================================"
