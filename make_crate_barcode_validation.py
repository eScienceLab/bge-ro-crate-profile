# Create an RO-Crate following the in-development BGE profile
from datetime import datetime
import os
import uuid
import requests
import pandas as pd

from rocrate.model import ContextEntity, Person
from rocrate.rocrate import ROCrate
from rocrate_validator import services, models

from utils import validate_crate, fetch_single_ena_record_by_accession


##################
# crate creation #
##################

# example data files - taken from https://github.com/bge-barcoding/bge-skimming-analytics/
target_fasta = "example-data/BGE00146_MGE-BGE_r1_1.3_1.5_s50_100.fasta"
target_tsv = "example-data/BGE00146_MGE-BGE_r1_1.3_1.5_s50_100.fasta.tsv"

df = pd.read_table(target_tsv)

species_names = df["species"].unique()
print(species_names)

name = species_names[0]
output_dir = "bge-crate-barcode-validation/"

crate = ROCrate()

crate.name = f"Barcode of {name}"
crate.description = f"Barcode of {name} created by iBOL and BGE"
license = crate.add(
        ContextEntity(
            crate,
            "https://spdx.org/licenses/CC0-1.0",
            properties={
                "@type": "CreativeWork",
                "name": "Creative Commons Zero v1.0 Universal",
                "url": "https://creativecommons.org/publicdomain/zero/1.0/legalcode",
            },
        )
    )
    crate.license = license

# TODO get this info from API
species = ContextEntity(
    crate,
    "https://www.ncbi.nlm.nih.gov/taxonomy/1464561",  # WRONG ID
    properties={
        "@type": "Taxon",
        "name": name,
        "scientificName": name,
        "taxonRank": [  # which to include?
            "https://bench.boldsystems.org/index.php/TaxBrowser_TaxonPage?taxid=304734",  # WRONG ID
            "https://www.ncbi.nlm.nih.gov/taxonomy/1464561",  # WRONG ID
            "https://www.wikidata.org/wiki/Q13855218",  # WRONG ID
        ],
    },
)

crate.add(species)
crate.root_dataset["about"] = species  # use this and/or taxonomicRange?
crate.root_dataset["taxonomicRange"] = species  # what uri to use for taxonomy?
crate.root_dataset["scientificName"] = name  # is this necessary?
crate.root_dataset["identifier"] = [
    "TODO project identifiers for barcoding"
]  # BioProject identifiers

fasta_format = crate.add(
    ContextEntity(
        crate,
        "https://blast.ncbi.nlm.nih.gov/doc/blast-topics/#fasta",
        properties={"name": "FASTA file format", "@type": ["WebPage", "Standard"]},
    )
)

# barcoding skimming outputs
barcodes_file = crate.add_file(
    source=target_fasta,
    properties={
        "name": "Barcodes in FASTA format",
        "description": "description of barcodes and what run they came from",
        "sdDatePublished": str(datetime.now()),
        "contentSize": os.stat(target_fasta).st_size,
        "encodingFormat": "text/x-fasta",
    },
)
barcodes_file.append_to("encodingFormat", fasta_format)

# barcoding skimming outputs
barcodes_tsv_file = crate.add_file(
    source=target_tsv,
    properties={
        "name": "Barcode process details in TSV format",
        "description": "A TSV containing details of each barcode validation run with different parameters",
        "sdDatePublished": str(datetime.now()),
        "contentSize": os.stat(target_tsv).st_size,
        "encodingFormat": "text/tab-separated-values",
    },
)


df["bold_process_id"] = df.sequence_id.apply(lambda x: x.split("_")[0])

barcode_validator = crate.add(
    ContextEntity(
        crate,
        "https://github.com/naturalis/barcode_validator",
        properties={
            "name": "DNA Barcode Validator",
            "description": "A Python-based toolkit for validating DNA barcode sequences through structural and taxonomic validation.",
            "version": "TODO",  # TODO
        },
    )
)

for bold_process_id in df["bold_process_id"].unique():
    # entity representing BOLD record - or a process?
    # BOLD Process IDs are unique codes automatically generated for each new record added to a project.
    #   They serve to connect specimen information, such as taxonomy, collection data and images,
    #   to the DNA barcode sequence for that specimen.
    # BOLD Process IDs consist of a standard format including the project code and sequential numbers,
    # followed by the year the record was added to the database. For example, the first record uploaded
    # to project PROJ in 2012 would be assigned BOLD Process ID PROJ001-12 . This format ensures BOLD
    # Process IDs are always unique in the system, as well as identifying the year the record was uploaded
    # and the original project it was uploaded to.

    # a CreateAction
    # object: specimen id
    # result: the barcode sequence(s) on BOLD

    crate.add_action(
        instrument=barcode_validator,
        identifier=f"#{bold_process_id}",
        object="TODO specimen id",  # is this actually the barcodes file?
        result=[barcodes_file, barcodes_tsv_file],
        properties={"name": f"Validation for BOLD process ID {bold_process_id}"},
    )

    # context entity - the barcode(s)
    # are these the FASTA file? or are these represented by BINs

    pass

# the whole file represents a workflow run
# instrument: https://github.com/bge-barcoding/barcode_validator (I think)
# object: the fasta file
# result: the tsv file
# agent: unknown - is this captured?

# this is VALIDATION - confirming that a particular run/sample/whatever matches what's in BOLD
# so maybe not all the detailed metadata is needed for the validation bit
# do we actually have two different things here
# the "source of truth" - the barcode in BOLD - these are the reference points - list in "mentions"?
# BOLD references are essentially another type of input, conceptually, but hmm
# the validation of additional samples - the workflow executions and analysis in these example files

# what would a ROC export from BOLD look like?


print(df.loc[df["species"] == name])

# Writing the RO-Crate metadata:
crate.write(output_dir)

validate_crate(output_dir)


# if __name__ == "__main__":
#     create_ro_crate(
#         input_file=sys.argv[1], workflow_file=sys.argv[2], output_dir=sys.argv[3]
#     )
