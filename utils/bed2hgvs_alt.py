import yaml
import hgvs.parser
import hgvs.dataproviders.uta
import hgvs.assemblymapper
from pyfaidx import Fasta
import csv

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


def get_base_at_position(chr, position, fasta_obj):
	"""
	Returns the base at a given position in a fasta. Needed to get the reference base.
	"""
	return fasta_obj[chr][position]

def create_genomic_variant(chromosome, position, config, base_at_pos):
	"""
	take a genomic variant in the format

	"""

	hp = hgvs.parser.Parser()

	contig = config['contigs'][chromosome]

	hgvs_g = '{contig}:g.{position}{base_at_pos}>{base_at_pos}'.format(contig=contig,
	 position=position,
	 base_at_pos=base_at_pos)

	var_g = hp.parse_hgvs_variant(hgvs_g)

	return var_g


def parse_transcript_gene_map(config):

	pass





def main():

	test = ['17', 7577013, 7572928]

	config = parse_config('config/local.yaml')

	ref = Fasta(config['reference_genome'])

	start_base = get_base_at_position(test[0], test[1], ref)
	end_base = get_base_at_position(test[0], test[2], ref)

	start_var_g =  create_genomic_variant(test[0], test[1]+1, config, start_base)
	end_var_g =  create_genomic_variant(test[0], test[2], config, start_base)

	print (start_var_g)
	print (end_var_g)

	hdp = hgvs.dataproviders.uta.connect(db_url=u'postgresql://anonymous:anonymous@uta.biocommons.org/uta_dev/uta_20160908')

	am = hgvs.assemblymapper.AssemblyMapper(hdp,
		assembly_name='GRCh37')

	start_transcripts = am.relevant_transcripts(start_var_g)
	end_transcripts = am.relevant_transcripts(end_var_g)

	print(start_transcripts)
	print(end_transcripts)

	start_var_c = am.g_to_c(start_var_g, 'NM_000546.5')
	end_var_c = am.g_to_c(end_var_g, 'NM_000546.5')

	print(start_var_c)
	print(end_var_c)



main()














