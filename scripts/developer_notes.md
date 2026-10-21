# Developer Notes

These notes are relevant to the GitHub repository for the profile: https://github.com/eScienceLab/bge-ro-crate-profile.

## Code

To run the scripts you must install the requirements listed in `requirements.txt`.

The scripts use [`roc-validator`](https://github.com/crs4/rocrate-validator) to automatically run validation against the specification when generating RO-Crates. This should tell you if you did anything wrong according to the base spec (but does not mean that everything is definitely correct - e.g. it is possible to link things incorrectly and still pass validation).

### Examples

The `make_crate_genome.py` and `make_crate_barcode.py` scripts create example crates that represent the profile.

Currently the scripts are not in sync with the profile text - as of v0.2 the scripts have been advanced further than the profile text.

The scripts generate RO-Crates in the `bge-crate-genome` and `bge-crate-barcode` folders respectively. To generate a HTML preview of the crate (useful for checking things are linked as intended):
```
npm install ro-crate-html
rochtml bge-crate-genome/ro-crate-metadata.json
```

### Profile Crate

The `make_profile_crate.py` script builds a Profile Crate (an RO-Crate that represents the profile itself) using the [ROCratePCC](https://github.com/nfdi4plants/ROCratePCC) package. The resulting crate should be suitable for submission to the [RO-Crate Profile Portal](https://profiles.ro-crate.org/en/). 

If there are changes to the `context.json` or the URIs for the profile/examples, the script should be updated accordingly. When releasing a new profile version, ensure all the metadata in the script (authors etc) is up to date.

## Where to find useful metadata and identifiers

* People: https://orcid.org/
* Organizations: https://ror.org/
* Places: https://www.geonames.org/v3/
* Taxonomy: https://www.ncbi.nlm.nih.gov/taxonomy
* BioProjects: https://www.ncbi.nlm.nih.gov/search/ (though at time of writing, search results may give 500 errors)
* Protocols: https://protocols.io/
* Samples (example accession SAMEA114402090):
    * https://www.ebi.ac.uk/ena/browser/ (preferred)
    * https://www.ebi.ac.uk/biosamples/
* Sequencing experiments (example accession ERX12519568):
    * https://www.ebi.ac.uk/ena/browser/ (preferred)
    * https://www.ncbi.nlm.nih.gov/sra
* Assembled genome (example accession GCA_964187845.1):
    * https://www.ebi.ac.uk/ena/browser/ (preferred)
    * https://www.ncbi.nlm.nih.gov/datasets/genome/
