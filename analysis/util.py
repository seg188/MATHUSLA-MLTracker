import os
import numpy as np

def GetFilesInDir(base_dir, postfix=".root"):
	if not (os.path.isdir(base_dir)):
		print("bad directory")
		return []
	files = []
	for file in os.listdir(base_dir):
		if file.endswith(postfix):
			files.append(base_dir + "/" + file)
	return files

def sigfigs(number, n):
	order = int(np.log10(number))
	if order > 0:
		return round(number, n)
	else:
		return round(number, int(-1*order) + n)




