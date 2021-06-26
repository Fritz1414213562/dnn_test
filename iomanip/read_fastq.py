## read sequences from .fastq format file


def read_fastq(fastq_names):

	import sys
	import subprocess

	retval = dict()

	for fastq_name in fastq_names:
		with open(fastq_name, 'r') as ifs:
	
			row_num = int(subprocess.check_output(['wc', '-l', fastq_name]).decode().split(' ')[0])
			if row_num % 4 != 0:
				print("The file is broken. The row number should be multiple of 4.", file=sys.stderr)
				sys.exit()
	
			i_line = 0
			seq_id = ...
	
			for line in ifs:
	
				if i_line % 4 == 0:
					words = line.split()
					seq_id = words[0].lstrip('@')
	
				elif i_line % 4 == 1:
					seq = line.rstrip('\n')
					retval[seq_id] = seq
					seq_id = ...
	
				elif i_line % 4 == 2:
					if line != "+\n":
						print("The file is broken.", "The line", i_line + 1, "should be '+'", file=sys.stderr)
						sys.exit()
	
				else:
					pass
	
				i_line += 1

	return retval
