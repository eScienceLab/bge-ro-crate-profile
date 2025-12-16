# Create an RO-Crate following the in-development BGE profile
from datetime import datetime
import os
import uuid
import requests

from rocrate.model import ContextEntity, Entity, Person
from rocrate.rocrate import ROCrate
from rocrate_validator import services, models

from utils import (
    validate_crate,
    fetch_single_bold_record_by_id,
    fetch_single_ena_record_by_accession,
    load_remote_crate,
    get_accession_permalink,
    get_copo_rocrate_uri_from_accession,
)

#########
# setup #
#########

ENA_PREFIX = "ena.embl"  # identifiers.org prefix
BIOSAMPLES_PREFIX = "biosample"  # identifiers.org prefix


def add_species_metadata(
    crate: ROCrate, species_names: list[str], bold_taxid: str | None = None
) -> None:
    if not bold_taxid:
        raise ValueError("BOLD taxid must be specified")
    for name in species_names:
        # TODO: lookup species name in NCBI/BOLD to get id
        species = ContextEntity(
            crate,
            f"https://bench.boldsystems.org/index.php/TaxBrowser_TaxonPage?taxid={bold_taxid}",
            properties={
                "@type": "Taxon",
                "name": name,
                "scientificName": name,
            },
        )
        species.append_to(
            "taxonRank",
            f"https://bench.boldsystems.org/index.php/TaxBrowser_TaxonPage?taxid={bold_taxid}",
        )

    crate.add(species)
    crate.root_dataset.append_to("about", species)  # use this and/or taxonomicRange?
    crate.root_dataset.append_to(
        "taxonomicRange", species
    )  # what uri to use for taxonomy?
    crate.root_dataset.append_to("scientificName", species)  # is this necessary?


def add_authors_and_affiliations(crate: ROCrate) -> None:

    # authors and affiliations
    # institutions
    naturalis = crate.add(
        ContextEntity(
            crate,
            "https://ror.org/0566bfb96",
            properties={
                "@type": "Organization",
                "name": "Naturalis Biodiversity Center",
                "url": "https://www.naturalis.nl",
            },
        )
    )
    leiden = crate.add(
        ContextEntity(
            crate,
            "https://www.geonames.org/2751773",
            properties={"@type": "Place", "name": "Leiden, NL"},
        )
    )
    naturalis["location"] = leiden

    nhm = crate.add(
        ContextEntity(
            crate,
            "https://ror.org/039zvsn29",
            properties={
                "@type": "Organization",
                "name": "Natural History Museum",
                "url": "https://www.nhm.ac.uk",
            },
        )
    )
    london = crate.add(
        ContextEntity(
            crate,
            "https://www.geonames.org/2643743",
            properties={"@type": "Place", "name": "London, UK"},
        )
    )
    nhm["location"] = london


################
# sample stage #
################


def add_sample_stage(crate: ROCrate, sample_accessions: list[str]) -> list[Entity]:
    # Physical sample collection
    multiple = True if len(sample_accessions) > 1 else False
    if multiple:
        sample_collection = crate.add(
            ContextEntity(
                crate,
                "#sample-collection",
                properties={
                    "@type": "Collection",
                    "identifier": "TODO",  # need collection name and URL; TODO: automate
                    "hasPart": [],
                },
            )
        )
        crate.root_dataset.append_to("hasPart", sample_collection)

    for sample_accession in sample_accessions:
        sample_metadata = fetch_single_bold_record_by_id(
            id=sample_accession,  # query_field="ids:sampleid"
        )

        sample = crate.add(
            ContextEntity(
                crate,
                f"#{sample_accession}",  # TODO: permalinks for BOLD?
                properties={
                    "@type": "BioSample",
                    "conformsTo": {
                        "@id": "https://bioschemas.org/profiles/Sample/0.2-RELEASE-2018_11_10"
                    },
                    "name": f"Sample {sample_accession}",
                    "description": f"BOLD record for biosample accession {sample_accession}.",
                    "identifier": [
                        sample_accession,
                    ],
                },
            )
        )
        sample["locationOfOrigin"] = str(
            sample_metadata["coord"]
        )  # TODO Place entity? BOLD has country, region, coordinates
        sample["collector"] = sample_metadata[
            "collectors"
        ]  # TODO Person entity? Reqiuires ORCID - available in ENA browser but not ENA API?
        sample["custodian"] = (
            "TODO custodian"  # preservation authors? Sample coordinator not available in ENA API
        )
        sample["contributor"] = sample_metadata["identified_by"]  # TODO Person entity?
        sample["collectionMethod"] = sample_metadata[
            "sampling_protocol"
        ]  # TODO LabProtocol entity?
        sample["ethics"] = sample_metadata[
            "sampling_protocol"
        ]  # TODO LabProtocol entity?
        sample["dateCollected"] = sample_metadata["collection_date_start"]

        if multiple:
            sample_collection.append_to("hasPart", sample)

    return sample_collection["hasPart"] if multiple else [sample]


#################
# wet lab stage #
#################


def add_sequencing_stage(crate: ROCrate, sequencing_accessions: list[str]) -> Entity:

    # ideally this protocol would be an RO-Crate itself so we could include just minimal metadata here
    protocol_sequencing = crate.add(
        ContextEntity(
            crate,
            f"#sequencing-protocol-{uuid.uuid4()}",
            properties={
                "@type": "LabProtocol",
                "name": f"Sequencing protocol",
                "description": "Sequencing protocol [placeholder]",
            },
        )
    )

    # Sequenced data collection
    multiple = True if len(sequencing_accessions) > 1 else False
    if multiple:
        sequencing_collection = crate.add(
            ContextEntity(
                crate,
                "#sequencing-collection",
                properties={
                    "@type": "Collection",
                    "hasPart": [],
                },
            )
        )
        crate.root_dataset.append_to("hasPart", sequencing_collection)

    for sequencing_accession in sequencing_accessions:

        # Sequenced data collection
        sequencing_main_entity = crate.add(
            ContextEntity(
                crate,
                f"#{sequencing_accession}-sequencing",  # TODO: BOLD permalinks?
                properties={
                    "@type": "Dataset",
                    "name": f"Sequencing stage {sequencing_accession}",
                    "description": f"Sequencing stage for {sequencing_accession}. Contains sequenced data and a description of the process used to create it.",
                    "hasPart": [],
                },
            )
        )

        sequencing_metadata = fetch_single_bold_record_by_id(
            sequencing_accession,
        )
        sample_accession = sequencing_metadata["sampleid"]
        sample_entity = crate.get(f"#{sample_accession}")
        if not sample_entity:
            raise ValueError(
                f"Sequencing {sequencing_accession} is based on sample f{sample_accession}, but no entity f{sample_id} exists in the RO-Crate. Please ensure all samples are added to the RO-Crate before adding sequencing."
            )

        # action connects protocol and output
        # Sequencing
        sequenced_data = []
        sequenced_data.append(
            crate.add_file(
                source=f"ftp://placeholder-data-download-link",
                validate_url=False,
                properties={
                    "name": f"Sequencing data for {sequencing_accession}",
                    # TODO automate description better
                    "description": f'example: PacBio sequencing of sample {sample_accession}, performed as part of process {sequencing_metadata["processid"]} for study accession XYZ.',
                    "sdDatePublished": str(datetime.now()),
                    "contentSize": 0,
                    "encodingFormat": "TODO",
                },
            )
        )

        sequencing_process = crate.add_action(
            instrument=protocol_sequencing,
            identifier=f"#sequencing-process-{uuid.uuid4()}",
            object=sample_entity,
            result=sequenced_data,
            properties={
                "@type": "LabProcess",  # is this in roc?
                "agent": "TODO wet lab contributors",
                "name": f"Genome sequencing process ({sequencing_accession})",
            },
        )
        sequencing_process["executesLabProtocol"] = protocol_sequencing
        sequencing_process["provider"] = sequencing_metadata["sequence_run_site"]
        sequencing_process["endDate"] = sequencing_metadata["sequence_upload_date"]
        sequencing_main_entity.append_to("mentions", sequencing_process)
        sequencing_main_entity.append_to("hasPart", sequenced_data)

        # sequencing_collection.append_to("hasPart", sequenced_data)
        if multiple:
            sequencing_collection.append_to("hasPart", sequencing_main_entity)

    return sequencing_collection["hasPart"] if multiple else [sequencing_main_entity]


##################
# analysis stage #
##################


def add_analysis_stage(crate: ROCrate, analysis_accessions: str) -> Entity:

    workflow_assembly = crate.add_workflow(
        dest_path=f"#assembly-workflow-{uuid.uuid4()}",
        properties={
            "name": f"Assembly workflow (placeholder)",
            "description": "A placeholder for a workflow that could exist on WorkflowHub (etc) or be directly contained within the crate",
            "sdDatePublished": str(datetime.now()),
        },
    )

    multiple = True if len(analysis_accessions) > 1 else False
    if multiple:
        analysis_collection = crate.add(
            ContextEntity(
                crate,
                "#analysis-collection",
                properties={
                    "@type": "Collection",
                    "hasPart": [],
                },
            )
        )
        crate.root_dataset.append_to("hasPart", analysis_collection)

    for analysis_accession in analysis_accessions:
        # try main accession first, then set accession, as they are similar but different...
        genome_assembly_metadata = {}
        genome_assembly_metadata = fetch_single_bold_record_by_id(analysis_accession)

        genome_assembly_data = []

        accession = genome_assembly_metadata["insdc_acs"]
        id = (
            get_accession_permalink(ENA_PREFIX, accession)
            if accession
            else f"#{analysis_accession}-barcode"
        )
        genome_assembly_item = crate.add(
            ContextEntity(
                crate,
                id,
                properties={
                    "@type": "BioChemEntity",
                    "name": f"Barcode data from process {analysis_accession}",
                    "sdDatePublished": str(datetime.now()),
                    "hasRepresentation": genome_assembly_metadata["nuc"],
                },
            )
        )
        tax_id = genome_assembly_metadata["taxid"]
        tax_range = (
            f"https://bench.boldsystems.org/index.php/TaxBrowser_TaxonPage?taxid={tax_id}",
        )
        genome_assembly_item["taxonomicRange"] = crate.get(
            f"https://bench.boldsystems.org/index.php/TaxBrowser_TaxonPage?taxid={tax_range}"
        )
        genome_assembly_data.append(genome_assembly_item)

        record_id = genome_assembly_metadata["record_id"]
        genome_assembly = crate.add(
            ContextEntity(
                crate,
                f"#{record_id}",
                properties={
                    "name": f"Barcode assembly {record_id}",
                    "description": f"Barcode assembly stage for {record_id}. Contains the workflow used, the workflow execution details, and the output data.",
                    "sdDatePublished": str(datetime.now()),
                    "@type": "Dataset",
                },
            )
        )
        genome_assembly.append_to("hasPart", genome_assembly_data)

        genome_assembly.append_to(
            "hasPart", workflow_assembly
        )  # TODO: could also be mainEntity? in WROC style?

        assembly_process = crate.add_action(
            instrument=workflow_assembly,
            identifier=f"#{analysis_accession}-assembly",
            object=crate.get(f"#{analysis_accession}-sequencing")["hasPart"],
            result=genome_assembly_data,
            properties={
                "@type": "CreateAction",  # is this in roc?
                "agent": "TODO assembly contributors",
                "name": f"Barcode assembly process ({analysis_accession})",
            },
        )
        genome_assembly.append_to("mentions", assembly_process)

        if multiple:
            analysis_collection.append_to("hasPart", genome_assembly)

    return analysis_collection["hasPart"] if multiple else [genome_assembly]


def main():

    target_bold_process_id = "MHMXN361-07"

    # TODO - multiple?
    bold_metadata = fetch_single_bold_record_by_id(target_bold_process_id)
    print(bold_metadata)
    species_names = [bold_metadata["species"]]

    sample_accessions = [bold_metadata["sampleid"]]
    # sample from specimen SAMEA114402071
    sequencing_experiment_accessions = [bold_metadata["processid"]]
    genome_assembly_accessions = [bold_metadata["processid"]]

    bold_process_id = bold_metadata["processid"]
    bold_sample_id = bold_metadata["sampleid"]
    bold_record_id = bold_metadata["record_id"]

    crate = ROCrate()
    output_dir = "bge-crate-barcode/"

    ##################
    # core metadata  #
    ##################

    name = species_names[0]

    crate.name = f"Barcode of {name}"
    crate.description = f"Barcode of {name}"
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

    add_species_metadata(
        crate=crate, species_names=species_names, bold_taxid=bold_metadata["taxid"]
    )

    crate.root_dataset["identifier"] = [
        "TODO project identifiers for barcoding"
    ]  # BioProject identifiers

    ##########################################################

    add_authors_and_affiliations(crate=crate)

    samples = add_sample_stage(crate=crate, sample_accessions=sample_accessions)

    sequenced_data = add_sequencing_stage(
        crate=crate, sequencing_accessions=sequencing_experiment_accessions
    )

    assemblies = add_analysis_stage(
        crate=crate,
        analysis_accessions=genome_assembly_accessions,
    )

    # TODO: add_validation_stage
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
    # this is VALIDATION - confirming that a particular run/sample/whatever matches what's in BOLD
    # so maybe not all the detailed metadata is needed for the validation bit
    # do we actually have two different things here
    # the "source of truth" - the barcode in BOLD - these are the reference points - list in "mentions"?
    # BOLD references are essentially another type of input, conceptually, but hmm
    # the validation of additional samples - the workflow executions and analysis in these example files

    # what would a ROC export from BOLD look like?

    #################
    # write & check #
    #################
    crate.root_dataset["hasPart"] = [*samples, *sequenced_data, *assemblies]
    # the final barcode is the focus of the crate
    crate.root_dataset["mainEntity"] = assemblies

    # Writing the RO-Crate metadata:
    crate.write(output_dir)

    validate_crate(output_dir)


if __name__ == "__main__":
    main()
