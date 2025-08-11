# Developer Notes

These notes are relevant to the GitHub repository for the profile: https://github.com/eScienceLab/bge-ro-crate-profile.

## Code

The `make_crate_genome.py` and `make_crate_barcode.py` scripts create example crates that represent the profile.

Currently the scripts are more defined than the profile text.

To run the scripts you must install the requirements listed in `requirements.txt`.

The scripts automatically run validation against the RO-Crate 1.1 specification when generating the RO-Crate. This should tell you if you did anything wrong according to the base spec (but does not mean that all entities are linked correctly). 

The scripts generate RO-Crates in the `bge-crate-genome` and `bge-crate-barcode` folders respectively. To generate a HTML preview of the crate (useful for checking things are linked as intended):
```
npm install ro-crate-html
rochtml bge-crate-genome/ro-crate-metadata.json
```

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
