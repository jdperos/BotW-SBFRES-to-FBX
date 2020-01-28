import os
import subprocess
import shutil
import traceback
from customUtilities import CustomFileUtils, CommandLineUtils

def DecryptAndGroupBFRESbyActor():
	print("***Phase 3 (Jon): DecryptionAndGrouping***")

	# Get the initial working directory of this script.
	initialWD = os.getcwd()

	# Will vary based on other people's set ups.
	sbfresCompilation = os.path.join(initialWD, "Compilation\\")

	# Returns a boolean of whether this file should be added to the filename list.
	invalidFileEndings = [".Tex1.bfres", ".Tex2.bfres", "_Animation.bfres", "_L.bfres", "_L.Tex1.bfres", "_L.Tex2.bfres"]
	def isSupportingBFRES(sbfresInQuestion: str):
		for invalidEnd in invalidFileEndings:
			if sbfresInQuestion.endswith(invalidEnd):
				return True
		return False

	# Returns a boolean of whether this file begins a series of sbfres models, sharing the same textures
	startOfSeriesFileEnding = "-00.sbfres"
	def isStartOfSeries(sbfresInQuestion: str):
		if sbfresInQuestion.endswith(startOfSeriesFileEnding):
			return True
		return False

	# Extract the SBFRES to BFRES
	def extractSBFREStoRARC(sbfresPath: str):
		# Extract SBFRES with yaz0dec.
		CommandLineUtils.call(CommandLineUtils.quoted(os.path.join( initialWD, "Libraries", "szstools", "yaz0dec.exe")), [CommandLineUtils.quoted(os.path.join(sbfresCompilation, sbfresPath))])

		# Delete original SBFRES.
		os.remove(os.path.join(sbfresCompilation, sbfresPath))

		# Return the path of the resulting RARC.
		sbfresFolderPath = os.path.dirname(sbfresPath)
		for potentialRARC in os.listdir(sbfresCompilation):
			if potentialRARC.endswith(".rarc"):
				print("Extracting " + sbfresPath + " to rarc")
				return os.path.join(sbfresFolderPath, potentialRARC)

		print("yaz0dec.exe failed to extract a RARC for sbfres " + sbfresPath + " :(")
		return ""

	def renameRARCtoBFRES(rarcPath: str):
		if rarcPath.endswith(".rarc"):
			newFilename = rarcPath.replace(".sbfres 0.rarc", ".bfres")
			os.rename(os.path.join(sbfresCompilation,rarcPath), os.path.join(sbfresCompilation + newFilename))
		else:
			print("Invalid RARC file.")

	# Make all SBFRES into BFRES
	for sbfres in sorted(os.listdir(sbfresCompilation)):
		if sbfres.endswith(".sbfres"):
			renameRARCtoBFRES(extractSBFREStoRARC(sbfres))

	# Create a folder for every BFRES family
	for bfres in sorted(os.listdir(sbfresCompilation)):
		if not isSupportingBFRES(bfres):
			familyName = bfres.replace(".bfres","")
			os.makedirs(os.path.join(sbfresCompilation + familyName))
			for bfresToMove in sorted(os.listdir(sbfresCompilation)):
				if bfresToMove.startswith(familyName + "."):
					shutil.move(sbfresCompilation + bfresToMove, sbfresCompilation + familyName)
				if bfresToMove.startswith(familyName + "_Animation"):
					shutil.move(sbfresCompilation + bfresToMove, sbfresCompilation + familyName)

if __name__ == "__main__":
	extractModelAndTextureData()