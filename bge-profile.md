# Biodiversity Genomics RO-Crate Profile

## UNDER CONSTRUCTION

This is a first draft currently in active development. Everything is subject to change.

## Overview

The aim of this profile is to provide a full description of the provenance of biodiversity genomics data. This means capturing and connecting the different stages of biodiversity genomics research, including:
* sample collection
* sample preservation and biobanking
* extraction of genomic material
* genomic data processing
* genomic sequencing
* genome assembly
* genome annotations and further analysis

These stages represent a mixture of physical processes, lab protocols, and computational workflows.

At each stage, accession numbers, authors, affiliations, and additional metadata are collected. The stages are connected through "actions" which represent the processes and workflows used.

This profile takes heavy inspiration from the [Process Run Crate](https://www.researchobject.org/workflow-run-crate/profiles/process_run_crate/) profile, specifically in how processes are connected to inputs, outputs, and tools through the use of `CreateAction`. As Process Run Crate is intended only for describing computational processes, we aim to generalize its approach to work in additional contexts. The [Provenance of entities](https://www.researchobject.org/ro-crate/specification/1.2/provenance.html)page of the RO-Crate specification is also relevant here.
