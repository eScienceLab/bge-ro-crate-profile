# RO-Crate for Biodiversity Genomics

**Note:** This is a first draft currently in active development.

## RO-Crate Profile for Biodiversity Genomics Europe

A RO-Crate profile for biodiversity genomics is being developed as part of the [BGE project](https://biodiversitygenomics.eu).

Read the profile here: [BGE Profile](bge-profile.md).

There are two example RO-Crates which follow the profile: 

* Genome example: [HTML preview](example-bge-crate-genome/ro-crate-preview.html), [JSON-LD](example-bge-crate-genome/ro-crate-metadata.json).
* Barcode example: [HTML preview](example-bge-crate-barcode/ro-crate-preview.html), [JSON-LD](example-bge-crate-barcode/ro-crate-metadata.json).

## Example crate details

### Genome example 

The genome example is built using information about the following mosquito genome:

1. Culex laticinctus  
    SAMEA114402090, SAMEA114402091, SAMEA114402094, SAMEA114402071  
    ERX12519568, ERX12433627, ERX12405204, ERX12405205  
    GCA_964187845.1, GCA_964187835.1  
    https://github.com/ERGA-consortium/EARs/blob/main/Assembly_Reports/Culex_laticinctus/idCulLati1/idCulLati1_EAR.pdf  

Future examples may describe the following genomes:

1. Culex theileri  
    SAMEA114402095, SAMEA114402096, SAMEA114402099, SAMEA114402076  
    ERX13020690, ERX12671962, ERX12671963  
    GCA_964340515.1, GCA_964340705.1  
    https://github.com/ERGA-consortium/EARs/blob/main/Assembly_Reports/Culex_theileri/idCulThei1/idCulThei1_EAR.pdf  
  
1. Culex perexiguus  
    SAMEA114402089, SAMEA114402085, SAMEA114402086, SAMEA114402066  
    ERX12317846, ERX12326304, ERX12519566  
    GCA_964243045.1, GCA_964248615.1  
    https://github.com/ERGA-consortium/EARs/blob/main/Assembly_Reports/Culex_perexiguus/idCulPerx1/idCulPerx1_EAR.pdf  
 
1. Culex modestus  
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
Genome Assembly Review: Jèssica Gómez-Garrido (perexiguus & laticinctus), Fernando Cruz (modestus) & Tom Brown (theileri)  

When substantial changes are made to the code, the `example-bge-crate-genome/` folder should also be updated with the generated example crate and the HTML preview.

### Barcode example 

The barcode example is built using metadata retrieved from BOLD for the Process ID [MHMXN361-07](https://portal.boldsystems.org/record/MHMXN361-07). The script `make_crate_barcode.py` is used to generate the example.

Examples can also be made using BGE-related process IDs such as [BHNHM001-24](https://portal.boldsystems.org/record/BHNHM001-24) - the process ID can simply be swapped in the `make_crate_barcode.py` script. The reason for not using a BGE record is that these do not yet have GenBank Accessions, as these barcodes are not yet submitted to ENA, therefore related metadata cannot yet be fetched using the accession.

When substantial changes are made to the code, the `example-bge-crate-barcode/` folder should also be updated with the generated example crate and the HTML preview.

## For developers – scripts and examples

See [Developer Notes](developer_notes.md).
