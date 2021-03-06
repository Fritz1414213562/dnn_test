def read_id_from_paf(paf_name):

	retval = set()

	with open(paf_name, 'r') as ifs:
		for line in ifs:
			words = line.split('\t')
			retval.add(words[0])
	

	return retval


def read_id_and_direct_from_paf(paf_name):

	retval = dict()

	with open(paf_name, 'r') as ifs:
		for line in ifs:
			words = line.split('\t')
			retval[words[0]] = words[4]
	
	return retval
