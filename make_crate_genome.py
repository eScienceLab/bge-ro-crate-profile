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


def add_species_metadata(crate: ROCrate, species_names: list[str]) -> None:

    for name in species_names:
        # TODO: lookup species name in NCBI/BOLD to get id
        species = ContextEntity(
            crate,
            "https://www.ncbi.nlm.nih.gov/taxonomy/1464561",
            properties={
                "@type": "Taxon",
                "name": name,
                "scientificName": name,
                "taxonRank": [  # which to include?
                    "https://bench.boldsystems.org/index.php/TaxBrowser_TaxonPage?taxid=304734",
                    "https://www.ncbi.nlm.nih.gov/taxonomy/1464561",
                    "https://www.wikidata.org/wiki/Q13855218",
                ],
            },
        )

        crate.add(species)
        crate.root_dataset.append_to(
            "about", species
        )  # use this and/or taxonomicRange?
        crate.root_dataset.append_to(
            "taxonomicRange", species
        )  # what uri to use for taxonomy?
        crate.root_dataset.append_to("scientificName", species)  # is this necessary?


def add_authors_and_affiliations(crate: ROCrate) -> None:

    # authors and affiliations
    # institutions
    wsi = crate.add(
        ContextEntity(
            crate,
            "https://ror.org/05cy4wa09",
            properties={
                "@type": "Organization",
                "name": "Wellcome Sanger Institute",
                "url": "https://www.sanger.ac.uk",
            },
        )
    )
    cambridge = crate.add(
        ContextEntity(
            crate,
            "https://www.geonames.org/2653941",
            properties={"@type": "Place", "name": "Cambridge, UK"},
        )
    )
    wsi["location"] = cambridge


################
# sample stage #
################


def add_sample_stage(crate: ROCrate, sample_accessions: list[str]) -> list[Entity]:
    # Physical sample collection
    sample_collection = crate.add(
        ContextEntity(
            crate,
            "#sample-collection",
            properties={
                "@type": "Collection",
                "identifier": "EBD_I-002382",  # need collection name and URL; TODO: automate
                "hasPart": [],
            },
        )
    )
    crate.root_dataset.append_to("hasPart", sample_collection)

    for sample_accession in sample_accessions:
        sample_metadata = fetch_single_ena_record_by_accession(
            accession=sample_accession, result_type="sample"
        )

        # reference the copo crate which has all the provenance for the sample
        # try:
        #     copo_rocrate_uri = get_copo_rocrate_uri_from_accession(sample_accession)
        # except ValueError:
        #     copo_rocrate_uri = ""

        # fetch and load the crate
        # copo_rocrate = load_remote_crate(copo_rocrate_uri)

        identifiers_org_ena_uri = get_accession_permalink(ENA_PREFIX, sample_accession)
        identifiers_org_biosamples_uri = get_accession_permalink(
            BIOSAMPLES_PREFIX, sample_accession
        )

        if False:  # TODO if copo_rocrate_uri:
            sample = crate.add(
                ContextEntity(
                    crate,
                    copo_rocrate_uri,
                    properties={
                        "@type": ["Dataset", "BioSample"],
                        "conformsTo": [
                            {"@id": "https://w3id.org/ro/crate"},
                        ],
                        "name": f"Sample {sample_accession}",
                        "description": f"COPO manifest for biosample accession {sample_accession}. Resolves to a detached RO-Crate.",
                        "identifier": [
                            sample_accession,
                            identifiers_org_ena_uri,
                            identifiers_org_biosamples_uri,
                        ],
                        "sdDatePublished": str(datetime.now()),
                    },
                )
            )
        else:
            sample = crate.add(
                ContextEntity(
                    crate,
                    identifiers_org_ena_uri,
                    properties={
                        "@type": "BioSample",
                        "conformsTo": {
                            "@id": "https://bioschemas.org/profiles/Sample/0.2-RELEASE-2018_11_10"
                        },
                        "name": f"Sample {sample_accession}",
                        "description": f"ENA record for biosample accession {sample_accession}.",
                        "identifier": [
                            sample_accession,
                            sample_metadata["sample_description"],  # a UUID from ENA
                            identifiers_org_ena_uri,
                            identifiers_org_biosamples_uri,
                        ],
                    },
                )
            )
            sample["locationOfOrigin"] = sample_metadata[
                "location"
            ]  # TODO Place entity?
            sample["collector"] = sample_metadata[
                "collected_by"
            ]  # TODO Person entity? Reqiuires ORCID - available in ENA browser but not ENA API?
            sample["custodian"] = (
                "TODO custodian"  # preservation authors? Sample coordinator not available in ENA API
            )
            sample["contributor"] = sample_metadata[
                "identified_by"
            ]  # TODO Person entity?
            # sample["collectionMethod"] = (
            #     sentinel_trap  # term does not yet exist? # TODO how to track in ENA? Biosamples has this but ENA doesn't
            # )
            sample["ethics"] = {
                "@id": "https://www.boe.es/eli/es-an/l/2003/10/28/8"
            }  # term does not yet exist?

        if related_samples := sample_metadata["related_sample_accession"]:
            if not isinstance(related_samples, list):
                related_samples = [related_samples]
            for id in related_samples:
                accession, relation = id.split(":")
                if relation == "same_as":
                    sample["sameAs"] = {
                        "@id": get_accession_permalink(ENA_PREFIX, accession)
                    }

        sample_collection.append_to("hasPart", sample)

    return sample_collection["hasPart"]


#################
# wet lab stage #
#################


def add_sequencing_stage(crate: ROCrate, sequencing_accessions: list[str]) -> Entity:

    # ideally this protocol would be an RO-Crate itself so we could include just minimal metadata here
    protocol_wet_lab = crate.add(
        ContextEntity(
            crate,
            "https://dx.doi.org/10.17504/protocols.io.8epv5xxy6g1b/v1",
            properties={
                "@type": "LabProtocol",
                "name": "Sanger Tree of Life Wet Laboratory Protocol Collection  V.1",
            },
        )
    )

    protocol_sequencing = crate.add(
        ContextEntity(
            crate,
            f"#sequencing-protocol-{uuid.uuid4()}",
            properties={
                "@type": "LabProtocol",
                "name": f"Sequencing protocol",
                "description": "Sequencing protocol described in (paper link - https://docs.google.com/document/d/199jTDzWqWLShYXEvS08YbqMkUz_HyNlmT2cRf5879nU/edit?tab=t.0)",
            },
        )
    )

    # Sequenced data collection
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
                get_accession_permalink(ENA_PREFIX, sequencing_accession),
                properties={
                    "@type": "Dataset",
                    "name": f"Sequencing stage {sequencing_accession}",
                    "hasPart": [],
                },
            )
        )
        # crate.root_dataset.append_to("hasPart", sequencing_main_entity)

        sequencing_metadata = fetch_single_ena_record_by_accession(
            sequencing_accession,
            "read_experiment",
            accession_field="experiment_accession",
        )

        processed_dna = crate.add(
            ContextEntity(
                crate,
                f"#processed-dna-rna-{uuid.uuid4()}",
                properties={
                    "@type": "BioSample",
                    "name": f"Processed DNA/RNA ({sequencing_accession})",
                    "description": "This entity represents the processed DNA/RNA from the genomic extraction process",
                },
            )
        )
        sequencing_main_entity.append_to("hasPart", processed_dna)

        sample_accession = sequencing_metadata["sample_accession"]
        sample_id = get_accession_permalink(ENA_PREFIX, sample_accession)
        sample_entity = crate.get(sample_id)
        if not sample_entity:
            raise ValueError(
                f"Sequencing {sequencing_accession} is based on sample f{sample_accession}, but no entity f{sample_id} exists in the RO-Crate. Please ensure all samples are added to the RO-Crate before adding sequencing."
            )

        # action connects protocol and output
        wet_lab_process = crate.add_action(
            instrument=protocol_wet_lab,
            identifier=f"#wet-lab-process-{uuid.uuid4()}",
            object=sample_entity,  # sample or biobank? assume sample...
            result=processed_dna,
            properties={
                "@type": "LabProcess",  # is this in roc?
                "agent": "TODO wet lab contributors",
                "name": f"DNA/RNA extraction process ({sequencing_accession})",
            },
        )
        wet_lab_process["executesLabProtocol"] = protocol_wet_lab
        wet_lab_process["location"] = crate.get(
            "https://www.geonames.org/2653941"
        )  # TODO: set these...
        wet_lab_process["provider"] = crate.get(
            "https://ror.org/05cy4wa09"
        )  # provisional term in schema.org
        sequencing_main_entity.append_to("mentions", wet_lab_process)

        # Sequencing

        download_uris = sequencing_metadata["fastq_ftp"].split(";")
        download_sizes = sequencing_metadata["fastq_bytes"].split(";")
        sequenced_data = []

        for uri, size in zip(download_uris, download_sizes):
            sequenced_data.append(
                crate.add_file(
                    source=f"ftp://{uri}",
                    validate_url=True,
                    properties={
                        "name": f'{sequencing_metadata["experiment_title"]}: {os.path.basename(uri)}',
                        # TODO automate description better
                        "description": "example: PacBio sequencing of library ERGA_PI14589222, constructed from sample accession SAMEA114402090 for study accession PRJEB75413.",
                        "sdDatePublished": str(datetime.now()),
                        "contentSize": size,
                        "encodingFormat": "TODO file type for FASTA",
                    },
                )
            )

        sequencing_process = crate.add_action(
            instrument=protocol_sequencing,
            identifier=f"#sequencing-process-{uuid.uuid4()}",
            object=processed_dna,
            result=sequenced_data,
            properties={
                "@type": "LabProcess",  # is this in roc?
                "agent": "TODO wet lab contributors",
                "name": f"Genome sequencing process ({sequencing_accession})",
            },
        )
        sequencing_process["executesLabProtocol"] = protocol_sequencing
        sequencing_process["location"] = crate.get("https://www.geonames.org/2653941")
        sequencing_process["provider"] = crate.get(
            "https://ror.org/05cy4wa09"
        )  # provisional term in schema.org
        sequencing_main_entity.append_to("mentions", sequencing_process)
        sequencing_main_entity.append_to("hasPart", sequenced_data)

        # sequencing_collection.append_to("hasPart", sequenced_data)
        sequencing_collection.append_to("hasPart", sequencing_main_entity)

    return sequencing_collection["hasPart"]


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
        try:
            genome_assembly_metadata = fetch_single_ena_record_by_accession(
                analysis_accession, "assembly", "assembly_accession"
            )
        except ValueError:
            genome_assembly_metadata = fetch_single_ena_record_by_accession(
                analysis_accession, "assembly", "assembly_set_accession"
            )

        # fetch experiment accessions to connect to sequencing stage
        # but the assembly metadata only has the runs
        run_accessions = genome_assembly_metadata["run_accession"].split(";")
        experiment_entities = []
        for run in run_accessions:
            experiment_metadata = fetch_single_ena_record_by_accession(
                run, "read_experiment", accession_field="run_accession"
            )
            experiment_accession = experiment_metadata["experiment_accession"]
            experiment_id = get_accession_permalink(ENA_PREFIX, experiment_accession)
            experiment_entity = crate.get(experiment_id)
            if not experiment_entity:
                raise ValueError(
                    f"Analysis {analysis_accession} is based on sequencing f{experiment_accession}, but no entity f{experiment_id} exists in the RO-Crate. Please ensure all sequencing is added to the RO-Crate before adding analyses."
                )
            experiment_entities.append(experiment_entity)

        # ENA specific - get data files
        wgs_set_accession = genome_assembly_metadata["wgs_set"]
        wgs_set_metadata = fetch_single_ena_record_by_accession(
            wgs_set_accession, "wgs_set", "wgs_set"
        )

        download_uris = wgs_set_metadata["set_fasta_ftp"].split(";")

        genome_assembly_data = []

        for uri in download_uris:
            genome_assembly_data.append(
                crate.add_file(
                    source=f"ftp://{uri}",
                    validate_url=True,
                    properties={
                        "name": f'{wgs_set_metadata["description"]}',
                        "sdDatePublished": str(datetime.now()),
                        "encodingFormat": "TODO file type for FASTA",
                        "identifier": get_accession_permalink(
                            ENA_PREFIX, wgs_set_accession
                        ),
                    },
                )
            )

        genome_assembly = crate.add_dataset(
            # source=get_accession_permalink(ENA_PREFIX, analysis_accession), # TODO identifiers.org doesn't work with the underscore?
            source=f"https://www.ebi.ac.uk/ena/browser/view/{analysis_accession}",
            validate_url=True,
            properties={
                "name": f'{genome_assembly_metadata["assembly_title"]}',
                "description": genome_assembly_metadata["description_comment"],
                "sdDatePublished": str(datetime.now()),
            },
        )
        genome_assembly.append_to("hasPart", genome_assembly_data)

        genome_assembly.append_to(
            "hasPart", workflow_assembly
        )  # TODO: could also be mainEntity? in WROC style?

        assembly_process = crate.add_action(
            instrument=workflow_assembly,
            identifier=f"#assembly-process-{uuid.uuid4()}",
            object=experiment_entities,
            result=genome_assembly,
            properties={
                "@type": "CreateAction",  # is this in roc?
                "agent": "TODO assembly contributors",
                "name": f"Genome assembly process ({analysis_accession})",
            },
        )
        genome_assembly.append_to("mentions", assembly_process)

        analysis_collection.append_to("hasPart", genome_assembly)

    return analysis_collection["hasPart"]


def main():
    species_names = [
        "Culex laticinctus",
        # "Culex modestus",
        # "Culex perexiguus",
        # "Culex theileri",
    ]

    sample_accessions = [
        "SAMEA114402090",
        "SAMEA114402091",
        "SAMEA114402094",
        "SAMEA114402071",
    ]
    # sample from specimen SAMEA114402071
    sequencing_experiment_accessions = [
        "ERX12519568",  # linked to another sample? SAMEA114402094
        "ERX12433627",
        "ERX12405204",
        "ERX12405205",
    ]
    genome_assembly_accessions = [
        "GCA_964187845.1",  # cross-refs SAMEA114402071
        "GCA_964187835.1",
    ]

    crate = ROCrate()
    output_dir = "bge-crate-genome/"

    ##################
    # core metadata  #
    ##################

    name = species_names[0]

    crate.name = f"Genome of {name}"
    crate.description = f"Genome of {name} created by ERGA-BGE"
    crate.license = "TODO license"

    add_species_metadata(crate=crate, species_names=species_names)

    crate.root_dataset["identifier"] = [
        get_accession_permalink(ENA_PREFIX, "PRJEB75414"),
        "https://www.ncbi.nlm.nih.gov/bioproject/1109235",
    ]  # BioProject identifiers

    add_authors_and_affiliations(crate=crate)

    samples = add_sample_stage(crate=crate, sample_accessions=sample_accessions)

    sequenced_data = add_sequencing_stage(
        crate=crate, sequencing_accessions=sequencing_experiment_accessions
    )

    assemblies = add_analysis_stage(
        crate=crate,
        analysis_accessions=genome_assembly_accessions,
    )

    #################
    # write & check #
    #################
    crate.root_dataset["hasPart"] = [*samples, *sequenced_data, *assemblies]
    # the assembled genomes are the focus of the crate
    crate.root_dataset["mainEntity"] = assemblies

    # Writing the RO-Crate metadata:
    crate.write(output_dir)

    validate_crate(output_dir)


if __name__ == "__main__":
    main()
