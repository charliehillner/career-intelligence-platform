# Adzuna Source Analysis

## Purpose

This document describes the exploratory analysis of the Adzuna API as
the first real-world data source of the Career Intelligence Platform.

The purpose of the analysis is to identify the structure, availability,
and limitations of the source data before implementing the
normalisation pipeline.

## Exploratory Sample

An initial search for `Biostatistician` in Germany returned eight job
postings.

The sample is used for source exploration only and should not be
interpreted as evidence that the observed availability rates generalise
to the complete Adzuna dataset.

## Field Availability

| Field               | Availability |
| ------------------- | -----------: |
| id                  |          8/8 |
| title               |          8/8 |
| description         |          8/8 |
| created             |          8/8 |
| company             |          8/8 |
| location            |          8/8 |
| category            |          8/8 |
| salary_is_predicted |          8/8 |
| contract_time       |          2/8 |
| latitude            |          1/8 |
| longitude           |          1/8 |

No explicit salary minimum or maximum was present in the exploratory
sample.

## Description Limitation

All eight returned descriptions had a length of exactly 500 characters.

The Adzuna search response therefore provides only a limited description
snippet rather than the complete job description in this sample.

This represents an important limitation for skill extraction. A skill
that is not observed in the available description cannot automatically
be interpreted as not being required by the job.

The platform must distinguish between:

- evidence that a skill is required,
- evidence that a skill is not required,
- absence of information in the available source data.

## Category

The `category` object was structurally present for all eight jobs but was
classified as `Unknown` for six of them.

Adzuna categories are therefore not mapped directly to the canonical
job-profile concept in MVP 1C.

The original category may be retained as source information.

## Location

Location information was consistently available and included both a
display name and a hierarchical `area` representation.

Example:

`Deutschland -> Hessen -> Frankfurt am Main`

The structured Adzuna location is preferred over locations inferred from
the description text.

## Duplicate and Multi-Location Postings

The exploratory sample contained two postings with the same job title
and company but different Adzuna IDs and location representations.

The Adzuna job ID is therefore treated as a source-posting identifier
and not necessarily as an identifier for a semantically unique vacancy.

Deduplication across source postings is outside the scope of the initial
MVP 1C pipeline.

## Mapping to the Canonical Model

| Canonical Concept    | Adzuna Source          | Strategy                               |
| -------------------- | ---------------------- | -------------------------------------- |
| Source Job ID        | `id`                   | Direct mapping                         |
| Job Title            | `title`                | Direct mapping                         |
| Publication Date     | `created`              | Timestamp transformation               |
| Company              | `company.display_name` | Normalisation                          |
| Location             | `location`             | Structured transformation              |
| Job Profile          | Not reliably available | Not directly mapped                    |
| Required Skill       | `description`          | Information extraction                 |
| Required Proficiency | `description`          | Information extraction when observable |
| Required Experience  | `description`          | Information extraction when observable |

## Conclusion

The Adzuna API provides a stable core of structured job metadata that
can be mapped to the canonical analytical model with relatively little
transformation.

The main challenge for MVP 1C is not job ingestion itself but the
construction of canonical skill requirements from limited,
semi-structured description text.

The normalisation pipeline must therefore avoid interpreting missing
source information as evidence that a requirement does not exist.
