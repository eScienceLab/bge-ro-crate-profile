from rocratepcc import *

# List all types which are used in this profile
types = [
    UsedType(iri="https://schema.org/CreativeWork", name="CreativeWork"),
    UsedType(iri="http://www.w3.org/ns/dx/prof/Profile", name="Profile"),
    UsedType(iri="https://bioschemas.org/terms/BioSample", name="BioSample"),
    UsedType(iri="https://bioschemas.org/terms/Taxon", name="Taxon"),
    UsedType(iri="https://bioschemas.org/LabProcess", name="LabProcess"),
    UsedType(iri="https://bioschemas.org/LabProtocol", name="LabProtocol"),
    UsedType(iri="https://bioschemas.org/terms/scientificName", name="scientificName"),
    UsedType(iri="https://bioschemas.org/terms/taxonRank", name="taxonRank"),
    UsedType(iri="https://bioschemas.org/terms/collector", name="collector"),
    UsedType(iri="https://bioschemas.org/terms/maintainer", name="maintainer"),
    UsedType(iri="https://bioschemas.org/terms/custodian", name="custodian"),
    UsedType(
        iri="https://bioschemas.org/terms/locationOfOrigin", name="locationOfOrigin"
    ),
    UsedType(
        iri="https://bioschemas.org/terms/collectionMethod", name="collectionMethod"
    ),
    UsedType(iri="https://bioschemas.org/terms/ethics", name="ethics"),
    UsedType(iri="https://bioschemas.org/terms/submitter", name="submitter"),
    UsedType(iri="https://bioschemas.org/terms/dateCollected", name="dateCollected"),
    UsedType(
        iri="https://bioschemas.org/terms/executesLabProtocol",
        name="executesLabProtocol",
    ),
]

# List all authors of this profile
authors = [
    Author(orcid="0000-0002-0035-6475", name="Eli Chadwick"),
    Author(orcid="0000-0002-2036-8350", name="Nick Juty"),
    Author(orcid="0000-0003-2569-0768", name="Joana Pauperio"),
    Author(orcid="0000-0001-8293-4816", name="Tom Brown"),
    Author(orcid="0000-0001-9254-7318", name="Rutger Vos"),
]

keywords = [
    "biodiversity",
    "genomics",
    "lab process",
    "life sciences",
    "bioinformatics",
]

# Version of the profile (semver if possible)
version = "0.2-DRAFT"
version_tag = "0.2"  # github tag

# Identifier of the root data entity of the profile, if url not applicable then use "./"
id = f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/bge-profile"  # TODO w3id

# Name of the profile
name = "Biodiversity Genomics RO-Crate Profile"

# Description of the profile
description = "The aim of this profile is to provide a full description of the provenance of biodiversity genomics data. This means capturing and connecting the different steps of biodiversity genomics research, from sample collection and preservation through to genome assembly, annotation, and further analysis."

# License by which the profile is published
license = License(iri="https://spdx.org/licenses/Apache-2.0", name="Apache License 2.0")

# List of the textual resources we use as specifications for this profile
specifications = [
    TextualResource(
        name="Biodiversity Genomics RO-Crate Profile description (Markdown)",
        file_path=f"https://github.com/eScienceLab/bge-ro-crate-profile/tree/{version_tag}/{version}/bge-profile.md",
        encoding_format="text/markdown",
    ),
    TextualResource(
        name="Biodiversity Genomics RO-Crate Profile description (HTML)",
        file_path=f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/bge-profile.html",
        encoding_format="text/html",
    ),
]

examples = [
    TextualResource(
        name="Genome example - Culex laticinctus (RO-Crate JSON-LD)",
        # description="Example genome assembly provenance for Culex laticinctus. For demo purposes only; may not represent the true provenance of this genome.",
        file_path=f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/example-bge-crate-genome/ro-crate-metadata.json",
        encoding_format="application/ld+json",
    ),
    TextualResource(
        name="Genome example - Culex laticinctus (RO-Crate HTML preview)",
        # description="Example genome assembly provenance for Culex laticinctus. For demo purposes only; may not represent the true provenance of this genome.",
        file_path=f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/example-bge-crate-genome/ro-crate-preview.html",
        encoding_format="text/html",
    ),
    TextualResource(
        name="Barcode example - BOLD Process ID MHMXN361-07 (RO-Crate JSON-LD)",
        # description="Example barcode provenance built using metadata retrieved from BOLD for the Process ID MHMXN361-07. For demo purposes only; may not represent the true provenance of this genome.",
        file_path=f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/example-bge-crate-barcode/ro-crate-metadata.json",
        encoding_format="application/ld+json",
    ),
    TextualResource(
        name="Barcode example - BOLD Process ID MHMXN361-07 (RO-Crate HTML preview)",
        # description="Example barcode provenance built using metadata retrieved from BOLD for the Process ID MHMXN361-07. For demo purposes only; may not represent the true provenance of this genome.",
        file_path=f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/example-bge-crate-barcode/ro-crate-preview.html",
        encoding_format="text/html",
    ),
]

# List of all the resource descriptors. Here, only the specification is given. Other possible types
resourceDescriptors = [
    Specification(specifications),
    Example(examples),
    # Guidance()
    # Constraint()
]

# The root data entity of the profile
rootEntity = RootDataEntity(
    id=id,
    name=name,
    description=description,
    license=license,
    used_types=types,
    resource_descriptors=resourceDescriptors,
    authors=authors,
    keywords=keywords,
)

# Profile entity
profile = Profile(rootEntity, license=license)

# Convert the profile to a JSON-LD string
string = profile.ToROCrateJsonString(spaces=2)

# override the base RO-Crate version
# the profile crate itself is valid under 1.2 but needs 1.3 for `isProfileOf`,
# so just change it throughout to be consistent
# can be removed when https://github.com/nfdi4plants/ROCratePCC/issues/4 is complete
string = string.replace(
    "https://w3id.org/ro/crate/1.2", "https://w3id.org/ro/crate/1.3"
)

# fix the base RO-Crate conformsTo reference
# can be removed when https://github.com/nfdi4plants/ROCratePCC/issues/2 is complete
string = string.replace(
    '"conformsTo": "https://w3id.org/ro/crate/1.3"',
    '"conformsTo": {"@id": "https://w3id.org/ro/crate/1.3"}',
)

metadata_file_path = f"../{version}/ro-crate-metadata.json"

# Write the string to a file "ro-crate-metadata.json"
with open(metadata_file_path, "w", encoding="utf-8") as f:
    f.write(string)
