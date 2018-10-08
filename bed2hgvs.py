import yaml
from suds.client import Client
import csv
import argparse

def parse_config(config_location):
	"""
	Parse the YAML config file.
	"""

	with open(config_location, 'r') as stream:

		try:
			return yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)
			raise


def get_hgvsc_from_hgvsg(hgvs_g, wsdl_o, config):
	"""
	Use the mutalyser API to convert hgvsg to hgvsc.

	Input:

	hgvsg: A string of the hgvsg

	wsdl_o: The wscl client service for mutalyser

	config: The config dictionary

	Output:

	A responce with the hgvsc for the transcripts the hgvsg falls within.

	"""

	build = config['mutalyzer_build']

	response = wsdl_o.numberConversion(build=build, variant=hgvs_g)

	return response


def create_transcript_dict(response):
	"""
	The mutalyser API returns a list of HGVSc nomanclature for different transcripts \
	that the variant falls in. This function creates a dictionary with each transcript \
	as a key and the HGVSc for the transcript as the value.

	Input:

	response: The response object from the mutalyser API

	Output:

	transcript_dict: A transcript dictionary e.g {NM_000546.4: NM_000546.4:c.919+2T>T}

	"""

	transcript_dict = {}

	for hgvsc in response['string']:

		transcript_dict[hgvsc.split(':')[0]] = hgvsc

	return transcript_dict

def parse_transcript_gene_map(config):
	"""
	Parse the transcript gene map CSV file into a dictionary.

	Input:

	config: The config dictionary createad from the YAML config file. This contains \
	the location of the transcript gene map CSV.


	Output:

	transcript_gene_dict: A dictionary containing the information from the \
	transcript gene map. Transcript is key and gene is value.
	
	"""

	transcript_gene_dict = {}

	with open(config['preferred_transcript_map'], 'r') as csvfile:

		spamreader = csv.reader(csvfile, delimiter=',')

		for row in spamreader:

			transcript_gene_dict[row[0]] = row[1]

	return transcript_gene_dict


def process_bed_line(chr, start, end, wsdl_o, transcript_map, config):
	"""
	Function that processes each line of a bed file and returns the appropiate annotation.

	Input:

	chr: the chromosome e.g 1 or chr1
	start: the start position from the bed file.
	end: the end position from the bed file.
	wsdl_o: the wsdl_o object from the suds library.
	transcript_map: the transcript_gene map returned by parse_transcript_gene_map()

	Output:

	annotation: The annotation to add to the bed file.

	"""

	# Account for chromosomes in different format.
	if chr[0:3] != 'chr':

		chr = 'chr' + chr

	# Put into HGVSg format from bed file. Mutalyser doesn't care what the base value is \
	# so we just use A>A.
	variant_start = '{chr}:g.{start}A>A'.format(chr=chr, start=int(start)+1)
	variant_end = '{chr}:g.{end}A>A'.format(chr=chr, end=int(end))

	# Get the HGVSc annotation from mutalyser API.
	response_start = get_hgvsc_from_hgvsg(variant_start, wsdl_o, config)
	response_end = get_hgvsc_from_hgvsg(variant_end, wsdl_o, config)

	# Process the response into a dictionary using create_transcript_dict()
	start_variant_transcripts = create_transcript_dict(dict(response_start))
	end_variant_transcripts = create_transcript_dict(dict(response_end))

	variant_transcripts = [start_variant_transcripts, end_variant_transcripts]

	hgvsc_dict = {}

	# Loop through both the start_variant_transcripts and end_variant_transcripts objects \
	# and create a hgvsc_dict with the information in
	for i, variant_transcript in enumerate(variant_transcripts):

		found_transcript = False

		for key in variant_transcript:


			# if the user has added this as the preferred transcript
			if key in transcript_map:

				print(key,variant_transcript[key])

				hgvsc_dict[i] = [key,variant_transcript[key]]

				found_transcript = True
			
				break

		if found_transcript == False:

			hgvsc_dict[i] = [None, None]

	if hgvsc_dict[0][0] != hgvsc_dict[1][0]:

		print ('Transcript mismatch between bed start and end. Gaps are not allowed to span multiple transcripts - please investigate.')
		raise

	if hgvsc_dict[0][0] == None or hgvsc_dict[1][0] == None:

		print('No transcript could be determined for this line in the BED file - try adding the transcript to the preferred_transcript_map file.')
		return 'ERROR'



	gene_name = wsdl_o.getGeneName(build=config['mutalyzer_build'], accno=hgvsc_dict[0][0])

	annotation  = '{gene_name}:{start}_{end}'.format(
		gene_name=gene_name,
		start = hgvsc_dict[0][1].split(':')[-1][:-3],
		end = hgvsc_dict[1][1].split(':')[-1][:-3]
		)

	return annotation



def process_bed_file(bed_file_location, config_dict, output_location):
	"""
	Loop through a BED file and process each line with process_bed_line()

	"""

	transcript_map = parse_transcript_gene_map(config_dict)

	URL = config_dict['mutalyser_url']

	client = Client(URL, cache=None)
	wsdl_o = client.service

	bed_list = []

	with open(bed_file_location, 'r') as csvfile:

		spamreader = csv.reader(csvfile, delimiter='\t')

		for row in spamreader:

			hgvs_description = process_bed_line(row[0], row[1], row[2],wsdl_o, transcript_map, config_dict )

			bed_list.append([row[0], row[1], row[2], hgvs_description])


	with open(output_location, 'w') as csvfile:

		spamwriter = csv.writer(csvfile, delimiter='\t')

		for row in bed_list:

			spamwriter.writerow(row)


def main():

	parser = argparse.ArgumentParser(description='Annotate a BED file with the HGSVc of the location.')
	parser.add_argument('--config_location', type=str, nargs=1,
					help='The location of the YAML config.')
	parser.add_argument('--input', type=str, nargs=1,
					help='The input location of the original BED file.')
	parser.add_argument('--output', type=str, nargs=1,
					help='The output location to put the annotated BED file')

	args = parser.parse_args()

	bed_file = args.input[0]

	config = parse_config(args.config_location[0])

	process_bed_file(bed_file, config, args.output[0])

if __name__ == '__main__':

	main()















