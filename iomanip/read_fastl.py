## read sequences from .fastl format file


def read_fastl(fastl_name, output_kind = "all"):

	import sys
	import subprocess

	sequences = dict()
	labels = dict()

	with open(fastl_name, 'r') as ifs:
	
		row_num = int(subprocess.check_output(['wc', '-l', fastl_name]).decode().split(' ')[0])
		if row_num % 2 != 0:
			print("The file is broken. The row number should be multiple of 2.", file=sys.stderr)
			sys.exit()
	
		i_line = 0
		seq_id = ...
		label = ...
	
		for line in ifs:
	
			if i_line % 2 == 0:
				words = line.split()
				seq_id = words[0].lstrip('>')
				label = words[1].lstrip("label=")
	
			elif i_line % 2 == 1:
				seq = line.rstrip('\n')
				sequences[seq_id] = seq
				labels[seq_id] = label
				seq_id = ...
				label = ...
	
			else:
				pass
	
			i_line += 1
	
	if output_kind == "all":
		return sequences, labels
	elif output_kind == "sequence":
		return sequences
	elif output_kind == "label":
		return labels
	elif output_kind == None:
		return None
	else:
		print("Invalid argument: The argument, 'output_kind' should be 'all', 'sequence', 'label', or None.", file = sys.stderr)
		sys.exit()
