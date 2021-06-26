
__all__ = ["extract_seq", "extract_aligned_seq"]


def extract_seq(label0_dirs, label1_dirs, seq_length_range):

	from iomanip import read_fastq, filesindirs


	fastq_suffix = ".fastq"
	label0_names = filesindirs(label0_dirs, fastq_suffix)
	label1_names = filesindirs(label1_dirs, fastq_suffix)

	label0_seq = read_fastq(label0_names)
	label0_keys = label0_seq.keys()
	label1_seq = read_fastq(label1_names)
	label1_keys = label1_seq.keys()

	sequences = dict()
	labels = dict()

	_label_seq(sequences, labels, label0_seq, 0, label0_keys, seq_length_range)
	_label_seq(sequences, labels, label1_seq, 1, label1_keys, seq_length_range)
	
	return sequences, labels



def extract_aligned_seq(label0_dirs, label1_dirs, aligned_id_set, seq_length_range):


	from iomanip import read_fastq, filesindirs


	fastq_suffix = ".fastq"
	label0_names = filesindirs(label0_dirs, fastq_suffix)
	label1_names = filesindirs(label1_dirs, fastq_suffix)

	label0_seq = read_fastq(label0_names)
	label0_keys = list(aligned_id_set & set(label0_seq.keys()))
	label1_seq = read_fastq(label1_names)
	label1_keys = list(aligned_id_set & set(label1_seq.keys()))

	sequences = dict()
	labels = dict()

	_label_seq(sequences, labels, label0_seq, 0, label0_keys, seq_length_range)
	_label_seq(sequences, labels, label1_seq, 1, label1_keys, seq_length_range)
	
	return sequences, labels


def _label_seq(out_sequences, out_labels, in_sequences, in_label, in_keys, seq_length_range):

	for key in in_keys:
		if (seq_length_range[0] < len(in_sequences[key])) or (len(in_sequences[key]) <= seq_length_range[1]):
			out_sequences[key] = in_sequences[key]
			out_labels[key] = in_label
