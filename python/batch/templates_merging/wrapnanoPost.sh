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
@COMMAND


