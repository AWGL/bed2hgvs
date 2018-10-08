import unittest
from bed2hgvs import *
import csv


class ProcessBedFileTest(unittest.TestCase):


	def test_pass_bed(self):
		"""
		Test the TP53 bed file see if we get the right output

		"""


		correct_data = ['TP53:c.*5_c.1181', 'TP53:c.1100+5_c.1033', 'TP53:c.919+5_c.919+2',
			'TP53:c.782+5_c.773', 'TP53:c.730_c.673-5', 'TP53:c.205_c.180', 'TP53:c.99_c.97-5',
			'TP53:c.96+5_c.75-5', 'TP53:c.74+5_c.65']

		config = parse_config('configs/test_pass.yaml')

		process_bed_file('test_data/pass.bed', config, 'test_data/pass_output.bed')

		with open('test_data/pass_output.bed', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')

			i = 0

			for row in spamreader:

				self.assertEqual(row[3], correct_data[i])

				i = i + 1

	
	def test_fail_bed_different_transcripts(self):
		"""
		This should raise an error as we have different transcripts for the start and end.

		"""

		config = parse_config('configs/test_fail.yaml')

		self.assertRaises(RuntimeError, process_bed_file, 'test_data/error_different_transcripts.bed', config, 'test_data/error_different_transcripts.bed')


	def test_fail_unknown_transcripts(self):
		"""
		We haven't put a transcript in the gene_transcript_map for this position.

		"""

		config = parse_config('configs/test_fail.yaml')

		correct_data = ['ERROR', 'TP53:c.919+5_c.919+2']

		process_bed_file('test_data/error_unknown_transcripts.bed', config, 'test_data/error_unknown_transcripts_output.bed')

		with open('test_data/error_unknown_transcripts_output.bed', 'r') as csvfile:

			spamreader = csv.reader(csvfile, delimiter='\t')

			i = 0

			for row in spamreader:

				self.assertEqual(row[3], correct_data[i])

				i = i + 1


if __name__ == '__main__':
    unittest.main()