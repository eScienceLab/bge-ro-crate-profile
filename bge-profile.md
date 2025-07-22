# Biodiversity Genomics RO-Crate Profile

## UNDER CONSTRUCTION

This is a first draft currently in active development. Everything is subject to change.

## Overview

The aim of this profile is to provide a full description of the provenance of biodiversity genomics data. This means capturing and connecting the different steps of biodiversity genomics research, including:

* source collection
* sample collection from a source
* source/sample preservation and biobanking
* extraction of genomic material
* genomic data processing
* genomic sequencing
* genome assembly
* genome annotations and further analysis

These steps represent a mixture of physical and computational processes. They can be broadly grouped into three main stages:
* Sample collection and preservation - the steps that get you from the field to the preserved sample
* Wet lab and sequencing - the steps that get you from a sample to raw genetic sequence data
* Computational analysis - that steps that get you from the raw genetic data to an assembled genome, a reference barcode, or some other "final product"

At each stage, accession numbers, authors, affiliations, and additional metadata are collected. The stages are connected through these accession numbers, and the steps within them are connected as "actions" which represent the processes and workflows used.

This profile takes heavy inspiration from the [Process Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/) profile, specifically in how processes are connected to inputs, outputs, and tools through the use of `CreateAction`. As Process Run Crate is intended only for describing computational processes, we aim to generalize its approach to work in additional contexts. The [Provenance of entities](https://www.researchobject.org/ro-crate/specification/1.2/provenance.html)page of the RO-Crate specification is also relevant here.

## Notes before reading

Note the distinction between Bioschemas LabProtocol (a sequence of tasks and operations executed to perform experimental research) and LabProcess (the specific application of a LabProtocol to some input (biological material or data) to produce some output (biological material or data)). This is analogous to the prospective and retrospective provenance ideas presented in [Workflow Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/workflow_run_crate/).

This spreadsheet [RO-Crate Bioschema mapping](https://docs.google.com/spreadsheets/d/1l33cmZC7SYsbD2JhxZ-XmW5MrwW7bdiBg3tQONWUc1w/edit?gid=1705586496#gid=1705586496) is the original reference for which metadata should be mapped to which terms in RO-Crate and particularly Bioschemas. Where information is omitted here in this draft, it may be present in that spreadsheet (though eventually all of the spreadsheet information should be in this profile).

The [ISA (Investigation, Study, Assay) metadata framework](https://isa-specs.readthedocs.io/en/latest/index.html) and [ISA RO-Crate profile](https://github.com/nfdi4plants/isa-ro-crate-profile/blob/release/profile/isa_ro_crate.md) may map onto this draft profile cleanly (with the root dataset as the Investigation and the stages as Studies). That profile is already supported by some existing platforms and projects (e.g. FAIRDOM-SEEK, FAIR Data Station, ARC framework). A future version of this profile may incorporate or inherit requirements from the ISA profile in order to improve interoperability.

The [Common Provenance Model](https://www.nature.com/articles/s41597-022-01537-6) (CPM) and the [CPM RO-Crate profile](https://by-covid.github.io/cpm-ro-crate/0.2/) also offer a path to more detailed, distributed provenance metadata. Incorporating CPM would better support the step-by-step construction of the provenance chain _during_ the research pipeline, rather than at the end of it. For now, this profile focuses mainly on the publication use case, where all provenance information is collected from disparate database sources once the analysis is complete and ready to publish. A future version of this profile may incorporate or inherit requirements from the CPM profile.

## Core Metadata

The crate should have all metadata in this section.

### Root Data Entity

The root data entity should include the following properties:

* `hasPart`: must include the data objects included within the crate.
* `mentions`: must include all the processes described (i.e. all the `CreateAction`s)
* `about`: links to a Taxon entity for the species being described (same as `taxonomicRange`)
* `taxonomicRange`: links to a Taxon entity for the species being described (same as `about`)
* `identifier`: should include a BioProject identifier if one exists for the project
* `mainEntity`: must reference the following three types of entities ():
    * One or more `BioSample`s representing the sample(s)
    * One or more `File`s or `Dataset`s representing the raw genetic data
    * One or more `File`s or `Dataset`s representing the primary output(s) of the analysis
    * Exception: If the crate is only representing a sample and not any further analysis, it only needs to have the `BioSample` entity from the sample stage. If the crate is intended to include wet lab processes but not computational analyses, it only needs entities from the first two stages.
* `funder`: should reference an `Organization` representing the project that funded the work. See [Funding and grants](https://www.researchobject.org/ro-crate/specification/1.2/contextual-entities.html#funding-and-grants) from the core RO-Crate spec.

## Species/taxon

A species should be represented using the Bioschemas Taxon type (https://bioschemas.org/Taxon). Its properties `name`, `scientificName` and `taxonRank` should be present.

## Stages

At all stages, there may be multiple samples or data entities - these can be grouped together using an entity of type `Collection` with `hasPart` linking to the individual entities. A `Collection` may be used in any `object` or `result` property on a `CreateAction` instead of an individual entity, provided that the entities in its `hasPart` are of the expected type for that process.

Most processes and objects are optional as not all this data may be collected or machine-retrievable in all cases. Where there are gaps, placeholder entities can be used - these should have an `@id` with a local identifier* and a `name` and `description` explaining what the placeholder is representing. 

*local identifiers should start with `#` and include a UUID to ensure uniqueness. The UUID is useful to avoid duplicate entities when many RO-Crates are combined into a [knowledge graph](https://en.wikipedia.org/wiki/Knowledge_graph).

## Stage: Sample Collection and Preservation

### Process: Collection

Optional - may be sufficient to include `collectionMethod` on the description of the collected specimen.

### Object: Collected specimen

A physical specimen should be represented using the Bioschemas BioSample type (https://bioschemas.org/BioSample).

Properties of that entity should include:
* `identifier`: URI or accession of the sample in a database (BioSamples, COPO, etc)
* `collector`: person who collected the sample
* `maintainer`: person who preserved the sample ?
* `contributor`: person who identified the sample
* `locationOfOrigin`: where the sample was collected
* `collectionMethod` and `ethics`: Details/locations of permits and/or ethical/legal documentation/compliance

### Process: Biobanking

Should be represented using an entity of type `CreateAction` and `LabProcess` (https://bioschemas.org/LabProcess) with properties:
* `instrument`: any relevant lab protocol used (link to a `LabProtocol`)
* `object`: the collected specimen
* `result`: the biobanked specimen
* `agent`: the person who carried out the process

### Object: Biobanked specimen

A biobanked specimen should be represented using the Bioschemas BioSample type (https://bioschemas.org/BioSample).

## Stage: Wet lab and sequencing

### Process: Genomic material extraction

Should be represented using an entity of type `CreateAction` and `LabProcess` (https://bioschemas.org/LabProcess) with properties:
* `instrument`: the genomic material extraction protocol used (link to a `LabProtocol`)
* `object`: the biobanked specimen
* `result`: the genomic material sample
* `agent`: the person who carried out the process

### Object: Genomic material extraction protocol

Should be represented using the Bioschemas LabProtocol type (https://bioschemas.org/LabProtocol).

Ideally has `author`s and `name`.

### Object: Genomic material sample

Should be represented using the Bioschemas BioSample type (https://bioschemas.org/BioSample).

### Process: Genome sequencing

Should be represented using an entity of type `CreateAction` with properties:
* `instrument`: the computational workflow or software application used (link to a `ComputationalWorkflow` and/or `SoftwareApplication`, see Process/Workflow Run Crate)
* `object`: the genomic material sample
* `result`: the genome sequencing data
* `agent`: the person who initiated the workflow

### Object: Genome sequencing data

Represent using `File`/`Dataset` now?

## Stage: Computational Analysis

### Process: Genome assembly

Should be represented using an entity of type `CreateAction` with properties:
* `instrument`: the computational workflow or software application used (link to a `ComputationalWorkflow` and/or `SoftwareApplication`, see Process/Workflow Run Crate)
* `object`: the genome sequencing data
* `result`: the assembled genome
* `agent`: the person who initiated the workflow

### Object: Assembled genome

Represent using `File`/`Dataset` now?

### Process: Genome annotation/other additional processes

Should be represented using an entity of type `CreateAction` with properties:
* `instrument`: the computational workflow or software application used (link to a `ComputationalWorkflow` and/or `SoftwareApplication`, see Process/Workflow Run Crate)
* `object`: the genome sequencing data or the assembled genome
* `result`: the annotation or other outputs
* `agent`: the person who initiated the workflow

### Object: Annotation

Represent using `File`/`Dataset` now?
