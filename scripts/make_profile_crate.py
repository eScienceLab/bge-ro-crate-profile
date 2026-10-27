from rocratepcc import *
from utils import validate_crate
import json


def load_types_from_context_file(context_file: str) -> list[UsedType]:
    with open(context_file, "r") as f:
        c = json.load(f)
        context = c.get("@context", None)
        if not context:
            raise ValueError('no "@context" found in input file')
        return [UsedType(iri=iri, name=key) for key, iri in context.items()]


# Version of the profile (semver if possible)
version = "0.2"
version_tag = "0.2"  # github tag

profile_dir = f"../{version}/"

# List all types which are used in this profile
types = [
    UsedType(iri="https://schema.org/CreativeWork", name="CreativeWork"),
    UsedType(iri="http://www.w3.org/ns/dx/prof/Profile", name="Profile"),
    *load_types_from_context_file(f"{profile_dir}/context.json"),
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

# Identifier of the root data entity of the profile, if url not applicable then use "./"
id = f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/bge-profile"  # TODO w3id

# Name of the profile
name = "Biodiversity Genomics RO-Crate Profile"

# Description of the profile
description = "The aim of this profile is to provide a full description of the provenance of biodiversity genomics data. This means capturing and connecting the different steps of biodiversity genomics research, from sample collection and preservation through to genome assembly, annotation, and further analysis."

# License by which the profile is published
license_rde = License(
    iri="https://spdx.org/licenses/Apache-2.0", name="Apache License 2.0"
)
license_metadata = License(
    iri="https://spdx.org/licenses/CC0-1.0", name="Creative Commons Zero v1.0 Universal"
)

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
    TextualResource(
        name="Biodiversity Genomics RO-Crate Profile Context (JSON-LD)",
        file_path=f"https://esciencelab.org.uk/bge-ro-crate-profile/{version}/context.json",
        encoding_format="application/ld+json",
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
    license=license_rde,
    used_types=types,
    resource_descriptors=resourceDescriptors,
    authors=authors,
    keywords=keywords,
    version=version,
)

# Profile entity
profile = Profile(rootEntity, license=license_metadata)

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

# Write the string to a file "ro-crate-metadata.json"
with open(f"{profile_dir}/ro-crate-metadata.json", "w", encoding="utf-8") as f:
    f.write(string)

print("RO-Crate generated. Validating...")

validate_crate(profile_dir)
