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
            f'Unexpectedly retrieved multiple ENA records for accession {accession}: {[i["sample_accession"] for i in results_list]}'
        )
    else:  # len(results_list) is 0
        raise ValueError(f"No ENA record found for accession {accession}.")


def fetch_single_bold_record_by_id(id: str, query_field: str | None = None) -> dict:
    """Fetch a single record from the BOLD API.

    :param id: id of the record
    :param result_type: BOLD tokens to narrow the query, e.g. "ids:processid" narrows the search to just BOLD process IDs.
        By default, this function will use the BOLD API to narrow the query automatically.
        See the BOLD API docs: https://portal.boldsystems.org/api/docs#/query/query_records_api_query_get
    :raises ValueError: multiple results found
    :raises ValueError: no results found
    :return: Dictionary (a JSON object) with the record's metadata
    """
    BOLD_API = "https://portal.boldsystems.org/api"

    # build query terms
    if query_field:
        query_str = f"{query_field}:{id}"
    else:
        r = requests.get(f"{BOLD_API}/query/parse", params={"query": {id}})
        r.raise_for_status()
        query_str = r.json()["terms"]

    # preprocessing - resolves wildcards to specific terms
    r = requests.get(f"{BOLD_API}/query/preprocessor", params={"query": {query_str}})
    r.raise_for_status()
    try:
        query_str = r.json()["successful_terms"][0]["matched"]
    except KeyError:
        raise ValueError(
            f"BOLD query could not be built for id {id} (query preprocessing failed with {query_str})."
        )

    if ";" in query_str:
        print(f"Warning: multiple query strings identified: {query_str}")
        query_str = query_str.split(";")[0]
        print(f"Selecting first query from list: {query_str}")

    # query records - returns an ID which can be used to fetch data
    r = requests.get(f"{BOLD_API}/query", params={"query": query_str})
    r.raise_for_status()
    bold_query_id = r.json()["query_id"]

    # fetch the record
    r = requests.get(f"{BOLD_API}/documents/{bold_query_id}")
    r.raise_for_status()
    results_list = r.json()["data"]

    if len(results_list) == 1:
        return results_list[0]
    elif len(results_list) > 1:
        raise ValueError(
            f'Unexpectedly retrieved multiple BOLD records for id {id}: {[i["processid"] for i in results_list]}'
        )
    else:  # len(results_list) is 0
        raise ValueError(f"No BOLD record found for id {id}.")


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
            f'Unexpectedly retrieved multiple results for accession {accession}: {[i["copo_id"] for i in results_list]}'
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
