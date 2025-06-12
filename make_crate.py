# Create an RO-Crate following the in-development BGE profile
import sys
import uuid
from datetime import datetime

from rocrate.model import ContextEntity, Person
from rocrate.rocrate import ROCrate
from rocrate_validator import services, models


#####################
#  crate validation #
#####################
def validate_crate(crate_uri):
    # Create an instance of `ValidationSettings` class to configure the validation
    settings = services.ValidationSettings(
        # Set the path to the RO-Crate root directory
        rocrate_uri=crate_uri,
        # Set the identifier of the RO-Crate profile to use for validation.
        # If not set, the system will attempt to automatically determine the appropriate validation profile.
        profile_identifier="ro-crate-1.1",
        # Set the requirement level for the validation
        requirement_severity=models.Severity.REQUIRED,
        # requirement_severity=models.Severity.RECOMMENDED, # use for best practices!
    )

    # Call the validation service with the settings
    result = services.validate(settings)

    # Check if the validation was successful
    if not result.has_issues():
        print("RO-Crate is valid!")
    else:
        print("RO-Crate is invalid!")
        # Explore the issues
        for issue in result.get_issues():
            # Every issue object has a reference to the check that failed, the severity of the issue, and a message describing the issue.
            print(
                f'Detected issue of severity {issue.severity.name} with check "{issue.check.identifier}": {issue.message}'
            )


##################
# crate creation #
##################

species_names = [
    "Culex laticinctus",
    "Culex modestus",
    "Culex perexiguus",
    "Culex theileri",
]

name = species_names[0]
output_dir = "bge-crate/"

crate = ROCrate()

crate.name = f"Genome of {name}"
crate.description = f"Genome of {name} created by ERGA-BGE"
crate.license = "TODO license"

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
crate.root_dataset["about"] = species  # use this and/or taxonomicRange?
crate.root_dataset["taxonomicRange"] = species  # what uri to use for taxonomy?
crate.root_dataset["scientificName"] = name  # is this necessary?
crate.root_dataset["identifier"] = [
    "PRJEB75414",
    "https://www.ncbi.nlm.nih.gov/bioproject/1109235",
]  # BioProject identifiers

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


# Physical sample collection
sample_collection = crate.add(
    ContextEntity(
        crate,
        "#sample-collection",
        properties={
            "@type": "Collection",  # TODO check this
            "identifier": "EBD_I-002382",  # need collection name and URL
            "hasPart": [],
        },
    )
)
# TODO add the other 3 samples
sample = crate.add(
    ContextEntity(
        crate,
        "https://www.ebi.ac.uk/biosamples/samples/SAMEA114402090",
        properties={
            "@type": "BioSample",
            "conformsTo": {
                "@id": "https://bioschemas.org/profiles/Sample/0.2-RELEASE-2018_11_10"
            },
            "url": "https://www.ebi.ac.uk/biosamples/samples/SAMEA114402090",
            "identifier": [
                "https://www.ebi.ac.uk/biosamples/samples/SAMEA114402090",
                "idCulLati1",
            ],
        },
    )
)
sentinel_trap = crate.add(
    ContextEntity(
        crate,
        "https://eu.biogents.com/bg-sentinel/",
        properties={
            "@type": "IndividualProduct",
            "identifier": "https://eu.biogents.com/bg-sentinel/",
            "name": "BG-Sentinel trap",
            "description": "The BG-Sentinel (a.k.a. the BG trap or BGS trap) is a mosquito trap.",
        },
    )
)

sample["locationOfOrigin"] = "TODO place entity"
sample["collector"] = "TODO collectors"  # sampling authors
sample["custodian"] = "TODO custodian"  # preservation authors
sample["contributor"] = "TODO contributors"  # identification authors
sample["collectionMethod"] = sentinel_trap  # term does not yet exist?
sample["ethics"] = {
    "@id": "https://www.boe.es/eli/es-an/l/2003/10/28/8"
}  # term does not yet exist?

# TODO add other samples here
sample_collection["hasPart"].append(sample)

# Biobanking
# TODO creators, maintainers, and such"
biobank_collection = crate.add(
    ContextEntity(
        crate,
        "#biobank-collection",
        properties={
            "@type": "Collection",  # TODO check this
            "identifier": "EBD_I-002381",  # need collection name and URL
            "hasPart": [],  # are there parts of this?
        },
    )
)

# Genomic material extraction / wet lab

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

processed_dna = crate.add(
    ContextEntity(
        crate,
        f"#processed-dna-rna-{uuid.uuid4()}",
        properties={
            "@type": "BioSample",
            "name": "Processed DNA/RNA",
            "description": "This entity represents the processed DNA/RNA from the genomic extraction process",
        },
    )
)

# action connects protocol and output
wet_lab_process = crate.add_action(
    instrument=protocol_wet_lab,
    identifier=f"#wet-lab-process-{uuid.uuid4()}",
    object=sample_collection,  # sample or biobank? assume sample...
    result=processed_dna,
    properties={
        "@type": "LabProcess",  # is this in roc?
        "agent": "TODO wet lab contributors",
        "name": "DNA/RNA processing",
    },
)
wet_lab_process["executesLabProtocol"] = protocol_wet_lab
wet_lab_process["location"] = cambridge
wet_lab_process["provider"] = wsi  # provisional term in schema.org

# Sequencing

protocol_sequencing = crate.add(
    ContextEntity(
        crate,
        f"#sequencing-protocol-{uuid.uuid4()}",
        properties={
            "@type": "LabProtocol",
            "name": "Sequencing protocol",
            "description": "Sequencing protocol described in (TODO paper link - https://docs.google.com/document/d/199jTDzWqWLShYXEvS08YbqMkUz_HyNlmT2cRf5879nU/edit?tab=t.0)",
        },
    )
)

# TODO one of these for each sample?
sequenced_data = crate.add_file(
    source="https://sra-downloadb.be-md.ncbi.nlm.nih.gov/sos4/sra-pub-run-30/ERR013/13033/ERR13033463/ERR13033463.1",
    validate_url=True,
    properties={
        "name": "Revio sequencing",
        "description": "PacBio sequencing of library ERGA_PI14589222, constructed from sample accession SAMEA114402090 for study accession PRJEB75413.",
        "identifier": "https://www.ncbi.nlm.nih.gov/sra/ERX12405204",
    },
)

# TODO one of these for each sample?
sequencing_process = crate.add_action(
    instrument=protocol_sequencing,
    identifier=f"#sequencing-process-{uuid.uuid4()}",
    object=processed_dna,
    result=sequenced_data,
    properties={
        "@type": "LabProcess",  # is this in roc?
        "agent": "TODO wet lab contributors",
        "name": "Genome sequencing",
    },
)
sequencing_process["executesLabProtocol"] = protocol_sequencing
wet_lab_process["location"] = cambridge
wet_lab_process["provider"] = wsi  # provisional term in schema.org

# Writing the RO-Crate metadata:
crate.write(output_dir)

validate_crate(output_dir)


# if __name__ == "__main__":
#     create_ro_crate(
#         input_file=sys.argv[1], workflow_file=sys.argv[2], output_dir=sys.argv[3]
#     )
