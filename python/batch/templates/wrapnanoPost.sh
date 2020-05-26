#!/bin/bash
source /etc/profile
# TODO: these could be filled in from a template
#CMSSW_RELEASE_BASE="/cvmfs/cms.cern.ch/slc6_amd64_gcc630/cms/cmssw/CMSSW_9_4_4"

source /cvmfs/cms.cern.ch/cmsset_default.sh
workdir=@WORKDIR
melalibdir=${CMSSW_BASE}/lib/slc6_amd64_gcc630/
exedir=`echo @EXEDIR`
export LD_LIBRARY_PATH=${melalibdir}:$LD_LIBRARY_PATH
cd ${workdir}
eval `scramv1 runtime -sh`
cd ${exedir}
#export LD_LIBRARY_PATH=$PWD/lib:$LD_LIBRARY_PATH
export X509_USER_PROXY=@X509
voms-proxy-info -all
nano_postproc.py -I tthAnalysis.NanoAODTools.postprocessing.tthModules @MODULES @OUTPUT @INPUTFILE -b $CMSSW_BASE/src/tthAnalysis/NanoAODTools/data/keep_or_drop.txt
python @OUTPUT/Skim_tree.py --infile @OUTPUT/@STEP1 --outfile @OUTPUT/@TRIM
rm -rf @OUTPUT/@STEP1

#nano_postproc.py -s 2 @OUTPUT @OUTPUT/@STEP1 -c "HT1 > 350 && ST1 > 150"
#rm -rf @OUTPUT/@STEP1
