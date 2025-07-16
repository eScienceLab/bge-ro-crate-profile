# Biodiversity Genomics RO-Crate Profile

## UNDER CONSTRUCTION

This is a first draft currently in active development. Everything is subject to change.

## Profile draft

See [BGE Profile](bge-profile.md), currently under construction.

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

## Example crate

The example is built using information about the following mosquito genomes:

1. Culex laticinctus  
    SAMEA114402090, SAMEA114402091, SAMEA114402094, SAMEA114402071  
    ERX12519568, ERX12433627, ERX12405204, ERX12405205  
    GCA_964187845.1, GCA_964187835.1  
    https://github.com/ERGA-consortium/EARs/blob/main/Assembly_Reports/Culex_laticinctus/idCulLati1/idCulLati1_EAR.pdf  

2. Culex theileri  
    SAMEA114402095, SAMEA114402096, SAMEA114402099, SAMEA114402076  
    ERX13020690, ERX12671962, ERX12671963  
    GCA_964340515.1, GCA_964340705.1  
    https://github.com/ERGA-consortium/EARs/blob/main/Assembly_Reports/Culex_theileri/idCulThei1/idCulThei1_EAR.pdf  
  
3. Culex perexiguus  
    SAMEA114402089, SAMEA114402085, SAMEA114402086, SAMEA114402066  
    ERX12317846, ERX12326304, ERX12519566  
    GCA_964243045.1, GCA_964248615.1  
    https://github.com/ERGA-consortium/EARs/blob/main/Assembly_Reports/Culex_perexiguus/idCulPerx1/idCulPerx1_EAR.pdf  
  
4. Culex modestus  
    SAMEA114402100, SAMEA114402102, SAMEA114402103, SAMEA114402081  
    ERX12326303, ERX12317845, ERX12519565  
    GCA_964213205.1, GCA_964213185.1  
    https://github.com/ERGA-consortium/EARs/blob/main/Assembly_Reports/Culex_modestus/idCulMode1/idCulMode1_EAR.pdf  

Project Coordination: Maria Jose Ruiz Lopez
Sample Collection: Maria Jose Ruiz Lopez, Sonia Cebrián-Camisón, Sergio Magallanes, Josué Martínez-de la Puente, Jordi Figuerola
Species Identification: Jordi Figuerola, Sonia Cebrián-Camisón
Sample Preservation: Sonia Cebrián-Camisón
Metadata Provision: Maria Jose Ruiz Lopez
DNA Extraction & Sequencing: Caroline Howard, Wellcome Sanger Institute Tree of Life Management, Samples and Laboratory team
Genome Assembly: Shane McCarthy, Kerstin Howe, Mark Blaxter, Wellcome Sanger Institute Tree of Life Core Informatics team

(Genome Assembly Review: Jèssica Gómez-Garrido (perexiguus & laticinctus), Fernando Cruz (modestus) & Tom Brown (theileri)

When substantial changes are made to the code, the `example-bge-crate-genome/` folder should also be updated with the generated example crate and the HTML preview.

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
