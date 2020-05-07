#!/bin/bash
#
TGT_URL='https://api.github.com/repos/code4nara/covid19/deployments'
#TGT_URL='https://api.github.com/repos/yasushiIS/covid19/deployments'
TGT_REF="development"  # master
TGT_ENV="development"  # production
BATCH_FLAG=0
DRYRUN_FLAG=0

####
#   Start Massege / Usage
####
usage_exit() {
    echo 
    echo "  Execute Github Action Scrpit" 1>&2
    echo "  Usage: $0 [-b] [-e environment]" 1>&2
    echo "    -b               Execute batch mode, no confirmation." 1>&2
    echo "    -u url           GitHub URL, default is ${TGT_URL} ." 1>&2
    echo "    -r reffer        Set Deploy Reffer, default is ${TGT_ERF} ." 1>&2
    echo "    -e Environment   Set Deploy Environment, default is ${TGT_ENV} ." 1>&2
    exit 1
}

####
#   Yes/no check
####
YN_CHECK()
{
    while true; do
        read -p '  Continue? [Y/n] ' Answer
        case $Answer in
            '' | [Yy]* )
                break;
                ;;
            [Nn]* )
                echo "  CANCELed."
                exit;
                ;;
            * )
                echo Please answer YES or NO.
        esac
    done
}

####
#   Main
####
#   GitHub Token
if [ "${GITHUB_TOKEN}" = "" ] ; then
    echo '=---------------------------------------------------------------------=' 
    echo '  GITHUB_TOKEN not Found' 
    echo '    Set your Github token to environment variable "GITHUB_TOKEN"' 
    echo '=---------------------------------------------------------------------=' 
    usage_exit
fi

#   Option Check
while getopts "hbdu:r:e:" OPT
do
    case $OPT in
	h) usage_exit ;;
	b) BATCH_FLAG=1 ;;
	d) DRYRUN_FLAG=1 ;;
	u) TGT_URL=$OPTARG ;;
	e) TGT_ENV=$OPTARG ;;
	r) TGT_REF=$OPTARG ;;
    esac
done

#   Option Check
if [ ${BATCH_FLAG} == 0 ] ; then
    echo "  TGT_URL: ${TGT_URL}  TGT_Reffer: ${TGT_REF}  TGT_Environment: ${TGT_ENV}"
    YN_CHECK
    echo
fi

JSON='{"ref":"'${TGT_REF}'", "environment":"'${TGT_ENV}'", "auto_merge":false}'

CMD="curl -X POST -H \"Authorization: token ${GITHUB_TOKEN}\" -H \"Content-Type: application/json\" ${TGT_URL} --data '${JSON}'"

if [ ${DRYRUN_FLAG} == 1 ] ; then
    # RRYRUN for debug
    echo "  mode DRYRUN" 
    echo "  cmd:  "${CMD}
else
    # Exec Command
    eval "${CMD}"
fi

####
#   End Massege
####
echo
echo "  Finished"
