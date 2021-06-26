
__all__ = ["filesindir", "filesindirs"]

def filesindir(dirpath, suffix):

	import os

	files = os.listdir(dirpath)
	retval = [dirpath + "/" + file for file in files if file.endswith(suffix)]

	return retval


def filesindirs(dirs, suffix):

	retval = list()

	for dir in dirs:
		retval[len(retval):len(retval)] = filesindir(dir, suffix)
	

	return retval
