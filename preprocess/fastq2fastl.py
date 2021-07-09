
def main(label0_dirs, label1_dirs, output, paf_name, seed, seq_length_range, is_read_direct):


	if paf_name == None: 
		from iomanip import extract_seq, dump_fastl
		sequences, labels = extract_seq(label0_dirs, label1_dirs, seq_length_range)
		dump_fastl(sequences, labels, output, seed)
	elif not is_read_direct:
		from iomanip import extract_aligned_seq, dump_fastl, read_id_from_paf
		aligned_id_set = read_id_from_paf(paf_name)
		sequences, labels = extract_aligned_seq(label0_dirs, label1_dirs, aligned_id_set, seq_length_range)
		dump_fastl(sequences, labels, output, seed)
	else:
		from iomanip import extract_aligned_directed_seq, dump_fastl, read_id_and_direct_from_paf
		aligned_id_direct = read_id_and_direct_from_paf(paf_name)
		sequences, labels = extract_aligned_directed_seq(label0_dirs, label1_dirs, aligned_id_direct, seq_length_range)
		dump_fastl(sequences, labels, output, seed)



if __name__ == "__main__":

	import argparse
	import sys

	parser = argparse.ArgumentParser(description = "Preprocess fastq files and output as fastl")
	parser.add_argument("--label0_dir", help = "path to the directory that have .fastq files labeled '0'", nargs = '*', required = True)
	parser.add_argument("--label1_dir", help = "path to the directory that have .fastq files labeled '1'", nargs = '*', required = True)
	parser.add_argument("--output", help = "path to the output file (recommended: .fastl)", required = True)
	parser.add_argument("--align", help = "path to the alignment file (required: .paf)")
	parser.add_argument("--direct", help = "distinguish the direction of squiggle read", action="store_true")
	parser.add_argument("--sqrange", help = "the range of sequence length", nargs = 2, required = True)
	parser.add_argument("--seed", help = "random seed for data shuffling", default = None)
	args = parser.parse_args()

	label0_dirs = args.label0_dir
	label1_dirs = args.label1_dir
	output = args.output
	paf_name = args.align
	is_read_direct = args.direct
	seq_length_range = [int(args.sqrange[0]), int(args.sqrange[1])]
	if seq_length_range[0] >= seq_length_range[1]:
		print("The left value of sequence length range is not shorter than the right one", file = sys.stderr)
		sys.exit()
	if (paf_name == None) and (is_read_direct):
		print("The option '--direct' is dependent on that '--align'.", file = sys.stderr)
		sys.exit()
	
	seed = int(args.seed)

	main(label0_dirs, label1_dirs, output, paf_name, seed, seq_length_range, is_read_direct)
