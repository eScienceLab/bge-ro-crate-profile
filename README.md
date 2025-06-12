# Biodiversity Genomics RO-Crate Profile

## UNDER CONSTRUCTION

This is a first draft currently in active development. Everything is subject to change.

## Profile draft

See [BGE Profile](bge-profile.md), currently under construction.

Additional ideas contained in this [working document for BGE profile](https://docs.google.com/document/d/1c_F5Bcuu7ZUED3F_Z0yDVBwlCqrzMMynh-KOCZq4kbQ/edit?tab=t.0) and other documents linked from there.

## Code

The `make_crate.py` script creates an example crate that represents the profile.

Currently the script is more defined than the profile text.

To run the `make_crate.py` script you must install the requirements listed in `requirements.txt`.

The script automatically runs validation against the RO-Crate 1.1 specification when generating the RO-Crate. This should tell you if you did anything wrong according to the base spec (but does not mean that all entities are linked correctly). 

The script generates an RO-Crate in the `bge-crate` folder. To generate a HTML preview of the crate (useful for checking things are linked as intended):
```
npm install ro-crate-html
rochtml bge-crate/ro-crate-metadata.json
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
