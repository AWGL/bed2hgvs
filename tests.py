import unittest
from bed2hgvs import *
import csv


class ProcessBedFileTest(unittest.TestCase):


	def test_pass_bed(self):
		"""
		Test the TP53 bed file see if we get the right output

		"""


		correct_data = ['TP53(NM_000546.4):c.1181_*5', 'TP53(NM_000546.4):c.1033_1100+5', 'TP53(NM_000546.4):c.919+2_919+5',
			'TP53(NM_000546.4):c.773_782+5', 'TP53(NM_000546.4):c.673-5_730', 'TP53(NM_000546.4):c.180_205', 'TP53(NM_000546.4):c.97-5_99',
			'TP53(NM_000546.4):c.75-5_96+5', 'TP53(NM_000546.4):c.65_74+5']

		config = parse_config('configs/test_pass.yaml')

		process_bed_file('test_data/pass.bed', config, 'test_data/pass_output.bed', 'configs/test_pass_transcript_gene_map.csv')

		with open('test_data/pass_output.bed', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')

			next(spamreader, None)

			i = 0

			for row in spamreader:

				self.assertEqual(row[3], correct_data[i])

				i = i + 1

	
	def test_fail_bed_different_transcripts(self):
		"""
		This should raise an error as we have different transcripts for the start and end.

		"""

		correct_data = ['ERROR1']

		config = parse_config('configs/test_pass.yaml')

		process_bed_file('test_data/error_different_transcripts.bed', config, 'test_data/error_different_transcripts_output.bed', 'configs/test_pass_transcript_gene_map.csv')

		with open('test_data/error_different_transcripts_output.bed', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')

			next(spamreader, None)

			i = 0

			for row in spamreader:

				self.assertEqual(row[3], correct_data[i])

				i = i + 1



	def test_fail_unknown_transcripts(self):
		"""
		We haven't put a transcript in the gene_transcript_map for this position.

		"""

		config = parse_config('configs/test_fail.yaml')

		correct_data = ['ERROR2', 'TP53(NM_000546.4):c.919+2_919+5']

		process_bed_file('test_data/error_unknown_transcripts.bed', config, 'test_data/error_unknown_transcripts_output.bed','configs/test_fail_transcript_gene_map.csv' )

		with open('test_data/error_unknown_transcripts_output.bed', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')

			next(spamreader, None)

			i = 0

			for row in spamreader:

				self.assertEqual(row[3], correct_data[i])

				i = i + 1


	def test_gene_on_forward_strand(self):
		"""
		Test program works on genes on the forward strand.

		"""

		correct_data = ['EGFR(NM_005228.3):c.-175_-161', 'EGFR(NM_005228.3):c.31_80']

		config = parse_config('configs/test_pass.yaml')

		process_bed_file('test_data/forward_test.bed', config, 'test_data/forward_test_output.bed', 'configs/test_pass_transcript_gene_map.csv')

		with open('test_data/forward_test_output.bed', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')

			next(spamreader, None)

			i = 0

			for row in spamreader:

				self.assertEqual(row[3], correct_data[i])

				i = i + 1

if __name__ == '__main__':
    unittest.main()