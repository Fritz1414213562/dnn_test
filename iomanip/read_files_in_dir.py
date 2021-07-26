
__all__ = ["filesindir", "filesindirs"]

def filesindir(dirpath, suffix):

	import os

	files = os.listdir(dirpath)
	retval = [dirpath + "/" + file for file in files if file.endswith(suffix)]

	return retval


def filesindirs(dirs, suffix):

	import sys

	retval = list()
	cand_dirs = ...

	if isinstance(dirs, str):
		cand_dirs = [dirs]
	elif isinstance(dirs, list):
		cand_dirs = dirs
	else:
		print("Error: Internal Error, The type of file directories should be list or str", file = sys.stderr)
		sys.exit()

	for dir in cand_dirs:
		retval[len(retval):len(retval)] = filesindir(dir, suffix)
	

	return retval
