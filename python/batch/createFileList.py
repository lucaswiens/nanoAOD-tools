#!/usr/bin/env python2
"""
author:	Lucas Wiens
mail:	lucas.wiens@desy.de
"""

import sys, os
import argparse
import subprocess
import shutil

def createFileAndModuleList(sampleFileName):
	fileList, moduleList = [], []
	sampleFile = open(sampleFileName, "r")
	for sample in sampleFile:
		sample = sample.strip()
		if not (sample.startswith("#") or sample in ["", "\n", "\r\n"]):
			fileList.append(createFileList(sample))
			moduleList.append(createModuleList(sample))
	sampleFile.close()
	return fileList, moduleList

#"root://cms-xrd-global.cern.ch"
def createFileList(sample):
	#CMD = "dasgoclient -query=\"file dataset=" + str(sample) + "\""
	return subprocess.check_output("dasgoclient -query=\"file dataset=" + str(sample) + "\"", shell=True).split()

def createModuleList(sample):
	isMC = False
	isSIG = False
	isUSER = False
	era = "unknown"
	module = "unknown"
	if "RunIISummer16" in str(sample) or "Run2016" in str(sample): era = 2016
	elif "RunIIFall17" in str(sample) or "Run2017" in str(sample): era = 2017
	if "/NANOAODSIM" in sample:
		isMC = True
	if "/SMS-T1tttt" in sample:
		isSIG = True
	if "//SMS-T1tttt" in sample:
		isSIG = True
		isMC = True
		era = 2016
	if isMC and not isSIG:
		module = "susy_1l_FiltersMC,jecUncert,susy1lepTOPMC,susy_1l_gen"#,xsec,genpartsusymod
		if era == 2016:
			module +=",jetmetUncertainties16,puWeight_2016,btagSF_csvv2_2016,btagSF_cmva_2016,countHistogramAll_2016,susy_1l_Trigg2016,susy1lepMC"
		if era == 2017:
			# Temporarly use the jetmet uncertainty for 2016
			module +=",jetmetUncertainties16,puWeight_2017,btagSF_csvv2_2017,btagSF_deep_2017,countHistogramAll_2017,susy_1l_Trigg2017,susy1lepMC17"
		if "TTJets" in str(sample) and era == 2016: module +=",susy_1l_nISR16,susy1lepTT_syst"
		if "TTJets" in str(sample) and era == 2017: module +=",susy_1l_nISR17,susy1lepTT_syst"
		if "WJets"  in str(sample): module +=",susy1lepWJets_syst"
	elif isMC and isSIG:
		module = "susy_1l_FiltersMC,jecUncert,puWeight,susy1lepTOPMC,susy_1l_gen,susy1lepSIG_syst"#,xsec,genpartsusymod
			# Temporarly use the jetmet uncertainty for 2016
		if era == 2016: module +=",jetmetUncertainties16,puWeight_2016,btagSF_csvv2_2016,btagSF_cmva_2016,susy_1l_Sig16,countHistogramAll_2016,susy1lepSIG"
		if era == 2017: module +=",jetmetUncertainties16,puWeight_2017,btagSF_csvv2_2017,btagSF_deep_2017,susy_1l_Sig17,countHistogramAll_2017,susy1lepSIG17"
	else:
		if era == 2016:
			module = "susy1lepdata,susy_1l_Trigg2016,susy_1l_FiltersData,susy1lepTOPData -J $CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/JSONS/Cert_271036-284044_13TeV_23Sep2016ReReco_Collisions16_JSON.txt"
		elif era == 2017:
			module = "susy1lepdata17,susy_1l_Trigg2017,susy_1l_FiltersData,susy1lepTOPData -J $CMSSW_BASE/src/PhysicsTools/NanoAODTools/data/JSONS/Cert_294927-306462_13TeV_PromptReco_Collisions17_JSON.txt"
	return module

	X509_USER_PROXY
def getOSVariable(Var):
	try:
		variable = os.environ[Var]
	except KeyError:
		print "Please set the environment variable " + Var
		sys.exit(1)
	return variable



if __name__=="__main__":
	parser = argparse.ArgumentParser(description="Runs a NAF batch system for nanoAOD", formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument("-i", "--input-file", required=True, help="Path to the file containing a list of samples.")
	parser.add_argument("-o", "--output", help="Path to the output directory", default = subprocess.check_output("date +\"%Y_%m_%d\"", shell=True).replace("\n", ""))

	args = parser.parse_args()

	cmsswBase = getOSVariable("CMSSW_BASE")
	workarea = "%s/src" % cmsswBase
	executable = "%s/src/PhysicsTools/NanoAODTools/batch"% cmsswBase
	#X509 = "%s/src/PhysicsTools/NanoAODTools/batch/x509up_u29118"% cmsswBase #CHANGE THIS ONCE X509 is obtained
	X509 = getOSVariable("X509_USER_PROXY")

	condTEMP = "./templates/submit.condor"
	wrapTEMP = "./templates/wrapnanoPost.sh"
	SkimTEMP = "./templates/Skim_tree.py"

	# fileList, moduleList = createFileAndModuleList(args.input_file)
	# print(fileList)
	# print(moduleList)

	if  os.path.exists(args.output):
		keepDirectory = raw_input("Output directory already exists: " + str(args.output) + " Do you want to remove it [y/n]: ")
		if ( "y" in keepDirectory or "Y" in keepDirectory or "Yes" in keepDirectory):
			shutil.rmtree(str(args.output))
			os.makedirs(str(args.output))
			os.makedirs(str(args.output) + "/Samples")
			os.makedirs(str(args.output) + "/Condor")
			os.makedirs(str(args.output) + "/Wrapper")
			os.makedirs(str(args.output) + "/Logs")
			os.makedirs(str(args.output) + "/Tree")
		elif ( "N" in keepDirectory or  "n" in keepDirectory or  "No" in keepDirectory ): print str(args.output) , "will be ovewritten by the job output -- take care"
		else:
			raise ValueError( "invalid input, answer with \"Yes\" or \"No\"")
	else:
		os.makedirs(str(args.output))
		os.makedirs(str(args.output) + "/Samples")
		os.makedirs(str(args.output) + "/Condor")
		os.makedirs(str(args.output) + "/Wrapper")
		os.makedirs(str(args.output) + "/Logs")

	sampleFile = open(args.input_file, "r")
	for sample in sampleFile:
		sample = sample.strip()
		if not (sample.startswith("#") or sample in ["", "\n", "\r\n"]):
			fileList = createFileList(sample)
			moduleList = createModuleList(sample)
			sampleName = sample.replace("/", "_")[1:]

			file = open(args.output + "/Samples/" + sampleName + ".txt", "w+")
			for filename in fileList:
				file.write("root://cms-xrd-global.cern.ch" + str(filename) + "\n")
			file.close()

			i = 1
			logDirectory = args.output + "/Logs"
			os.system("cp " + SkimTEMP + " " + args.output)
			for filename in fileList:
				os.system("cp " + condTEMP + " " + args.output + "/Condor/" + sampleName + str(i) + ".submit")
				submitFileContent = open(args.output + "/Condor/" + sampleName + str(i) + ".submit").read()
				submitFileContent = submitFileContent.replace("@EXECUTABLE", args.output + "/Wrapper/" + sampleName + str(i))
				submitFileContent = submitFileContent.replace("@LOGS", logDirectory)
				submitFileContent = submitFileContent.replace("@X509", X509)
				submitFileContent = submitFileContent.replace("@TIME", "60*60*48")

				submitFile = open(args.output + "/Condor/" + sampleName + str(i) + ".submit", "w")
				submitFile.write(submitFileContent)
				submitFile.close()

				skimTreeInput = filename.split("/")[-1].replace(".root", "_Skim.root")

				os.system("cp " + wrapTEMP + " " + args.output + "/Wrapper/" + sampleName + str(i))
				wrapperFileContent = open(args.output + "/Wrapper/" + sampleName + str(i)).read()
				wrapperFileContent = wrapperFileContent.replace("@WORKDIR", workarea)
				wrapperFileContent = wrapperFileContent.replace("@EXEDIR", executable)
				wrapperFileContent = wrapperFileContent.replace("@MODULES", moduleList)
				wrapperFileContent = wrapperFileContent.replace("@OUTPUT", args.output)
				wrapperFileContent = wrapperFileContent.replace("@INPUTFILE", filename)
				wrapperFileContent = wrapperFileContent.replace("@X509", X509)
				wrapperFileContent = wrapperFileContent.replace("@STEP1", skimTreeInput)
				wrapperFileContent = wrapperFileContent.replace("@TRIM", "Tree/" + skimTreeInput.replace("_Skim.root", "_Trim.root"))

				wrapperFile = open(args.output + "/Wrapper/" + sampleName + str(i), "w")
				wrapperFile.write(wrapperFileContent)
				wrapperFile.close()
				file = open(args.output + "/submitAllViaHTC", "a")
				file.write("condor_submit -name s02 " + args.output + "/Condor/" + sampleName + str(i) + ".submit\n")
				file.close()
				i +=1
	os.system("chmod +744 " + args.output + "/submitAllViaHTC")
	print "submitAllViaHTC created in " + args.output + " to submit all jobs"
	sampleFile.close()
