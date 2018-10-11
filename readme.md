# bed2hgvs

## Description

A small program for annotating a bed file with HGVSc information.

When viewing a bed file containing regions it is useful to be able to understand a genomic interval in the context of a transcript.

For example the genomic coordinates below are not particually informative to a human:

17	7573921	7573994

The program uses Mutalyzer to annotate this bed file with information about specific transcripts. The final output will then be something like:

17	7573921	7573994	TP53:c.1100+5_c.1033

This makes it easier to understand and shows that the region spans TP53 between c.1033 and c.1100+5.

Within AWGL the tool is used to annotate a bed file of regions within a sequencing assay that fall below a certain coverage i.e. coverage gaps.

## Installation

The repository can be collected though the following command:

`git clone https://github.com/josephhalstead/bed2hgvs.git`

The program is written in Python3 and the requirements can be found in the envs/main.yaml file.

It is reccomended that the tool is installed within a Conda environment.

Install Miniconda from https://conda.io/miniconda.html

A virtual environment called bed2hgvs can then be created using the following command:

`conda env create -f envs/main.yaml `

`source activate bed2hgvs`

## Configure and Run

There are two configuration files to edit:

1) configs/local.yaml

2) transcript\_gene_map.csv

The main config file (example given by configs/local.yaml) should be edited and the preferred_transcript_map,  mutalyser_url. and mutalyzer_build variables set.

The transcript_gene_map.csv should also be edited so that it contains the transcript that should be used for each gene. Note that if a transcript is not set in this file no annotation will be provided for this line in the bed file.

To run the program use the following command:

`python bed2hgvs.py --config_location config/local.yaml --input tests/test_data/pass.bed --output pass.hgvs.bed `

## Test

To run tests:

`python tests.py `

## Limitations

Only works within a transcript - e.g. will annotate with error if the region spans multiple transcripts.

Uses remote Mutalyzer - we should really use local installation