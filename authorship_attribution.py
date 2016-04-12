from model import *
import glob
import nltk

def generateModelAuthors(rootDirectory, order):
	numberOfAuthors = len(glob.glob(rootDirectory))
	modelsOfEachAuthor = {}
	for i in glob.glob(rootDirectory):
		modelsOfEachAuthor[i] = None

	for i in glob.glob(rootDirectory):
		all_files = glob.glob(i+"/*")
		



generateModelAuthors("./testDirectory/*", 2)
