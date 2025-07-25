# Helper functions for BGE RO-Crate creation
from datetime import datetime
import os
import uuid
import requests

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


####################
# helper functions #
####################
def fetch_single_ena_record_by_accession(
    accession: str, result_type: str, accession_field: str = "accession"
) -> dict:
    """Fetch a single record from the ENA API.

    :param accession: accession of the record
    :param result_type: the ENA data set to search against.
        Options are listed in the first column here https://www.ebi.ac.uk/ena/portal/api/results?dataPortal=ena
    :param accession_field: the field which represents the accession in the chosen result_type (ENA data set). Default is "accession".
    :raises ValueError: multiple results found
    :raises ValueError: no results found
    :return: Dictionary (a JSON object) with the record's metadata
    """
    ena_api = "https://www.ebi.ac.uk/ena/portal/api"
    params = {
        "result": result_type,
        "query": f'{accession_field}="{accession}"',
        "fields": "all",
        "format": "json",
        "limit": 10,  # there should only be one, but this limit prevents malformed requests from hanging
    }
    r = requests.get(f"{ena_api}/search", params=params)
    r.raise_for_status()
    results_list = r.json()

    if len(results_list) == 1:
        return results_list[0]
    elif len(results_list) > 1:
        raise ValueError(
            f"Unexpectedly retrieved multiple results for accession {accession}: {[i["sample_accession"] for i in results_list]}"
        )
    else:  # len(results_list) is 0
        raise ValueError(f"No result found for accession {accession}.")


def get_accession_permalink(prefix, accession) -> str:
    return f"https://identifiers.org/{prefix}:{accession}"


def get_copo_rocrate_uri_from_accession(accession: str) -> str:
    copo_api = "https://copo-project.org/api"
    params = {
        "standard": "tol",
        "return_type": "json",
    }
    r = requests.get(f"{copo_api}/sample/biosampleAccession/{accession}", params=params)
    r.raise_for_status()
    results_list = r.json()["data"]

    if len(results_list) == 1:
        manifest_id = results_list[0]["manifest_id"]
        return f"{copo_api}/manifest/{manifest_id}?return_type=rocrate"
    elif len(results_list) > 1:
        raise ValueError(
            f"Unexpectedly retrieved multiple results for accession {accession}: {[i["copo_id"] for i in results_list]}"
        )
    else:  # len(results_list) is 0
        raise ValueError(f"No COPO record found for accession {accession}.")


def load_remote_crate(uri: str) -> dict:
    r = requests.get(uri)
    r.raise_for_status()
    dir = f"/tmp/{uuid.uuid4()}"
    with open(f"{dir}/ro-crate-metadata.json", "w") as f:
        f.write(r.text)
        crate = ROCrate(dir)
    return crate
