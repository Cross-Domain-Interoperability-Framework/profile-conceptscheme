# CDIF Concept Scheme Profile — Implementation Guide

#. Purpose and scope

The **CDIF Concept Scheme profile ** (`cdifConceptScheme`) describes a **SKOS concept scheme** — a controlled vocabulary of concepts used in CDIF metadata. A typical concept scheme is a community glossary or thesaurus that supplies shared definitions and terms: the concepts used to name variables, classify resources, or qualify measurements in other CDIF profiles.

**Related profile.** A *code list* is a concept scheme whose members are controlled values carrying machine notation codes (`skos:notation`). Code lists are published as the separate [profile-codelist](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist) profile. Use Concept Scheme for a general vocabulary of meanings; use Codelist when each concept must carry a code.

# Table of contents

  - [2. Conformance](#2-conformance)
  - [3. Concepts](#3-concepts)
  - [4. Validation](#4-validation)
- [Model](#model)
  - [ConceptScheme](#conceptscheme)
  - [Data Types](#data-types)
  - [LanguageTaggedValue](#languagetaggedvalue)
  - [Object Reference](#object-reference)
  - [Optional Properties](#optional-properties)
  - [Optional Properties](#optional-properties)
  - [Required Properties](#required-properties)
- [Bidirectional Hierarchy](#bidirectional-hierarchy)
- [Array Convention](#array-convention)
  - [5. Provenance of the artifacts](#5-provenance-of-the-artifacts)

## 2. Conformance

A conforming concept scheme is typed as a `skos:ConceptScheme` and declares conformance to the Concept Scheme profile identifier:

```json
{
  "@context": { "skos": "http://www.w3.org/2004/02/skos/core#" },
  "@id": "https://example.org/vocab/myscheme",
  "@type": ["skos:ConceptScheme"],
  "skos:prefLabel": {"@value": "My Vocabulary", "@language": "en"},
  "skos:definition": {"@value": "...", "@language": "en"},
  "skos:hasTopConcept": [ { "@id": "https://example.org/vocab/myscheme/top" } ]
}
```

Required elements for the Concept Scheme:

- **`@id`** — the scheme's IRI;
- **`@type`** — must include `skos:ConceptScheme`;
- **`skos:prefLabel`** — preferred label (string or language-tagged value; at most one per language);
- **`skos:definition`** — what the scheme is for;
- **`skos:hasTopConcept`** — at least one top-level concept, defining the vocabulary's entry points.

## 3. Concepts

Top concepts (and their narrower concepts) are `skos:Concept` nodes, given inline or by `@id` reference. Each concept carries `skos:prefLabel` and   `skos:definition`. Optional properties include `skos:note`, `skos:inScheme`, and the hierarchy relations `skos:broader` / `skos:narrower` (themselves inline concepts or `@id` references). 

## 4. Validation

- **JSON Schema** — `cdifConceptSchemeStructuredSchema.json` (Draft 2020-12), generated from the source register.
- **SHACL** — `conceptSchemeRules.shacl`, which targets `skos:ConceptScheme` and checks that a scheme has an IRI identifier, at least one `skos:prefLabel` (with `sh:uniqueLang`), and at least one `skos:hasTopConcept`.

```bash
python FrameAndValidate.py examples/exampleSkosConceptScheme.json --validate
```

`FrameAndValidate.py` frames the document with `cdifConceptScheme-frame.jsonld`, array-wraps the multi-valued SKOS properties, then validates against the JSON Schema. Validation is **open-world**: properties beyond the profile are permitted.

# Model

## ConceptScheme

- The root object representing the concept scheme.

### @id

- **Cardinality:** Required
- **Content:** string.uri
- **Description:** Globally unique, resolvable URI for the concept scheme.

### @type

- **Cardinality:** Required
- **Content:** array
- **Description:** Must include `skos:ConceptScheme`.

### skos:prefLabel

- **Cardinality:** Required
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of [LanguageTaggedValue](#languagetaggedvalue)
- **Description:** Preferred human-readable label for the scheme. At most one per language.

### skos:hasTopConcept

- **Cardinality:** Required, Repeatable
- **Content:** array of [CdifConcept](#cdifconcept) or [object reference](#object-reference)
- **Description:** Top-level concepts that have no `skos:broader` within this scheme. The JSON-LD hierarchy is rooted here — all child concepts are reached by traversing `skos:narrower` from these top concepts.

### schema:identifier

- **Cardinality:** Required
- **Content:** string or [PropertyValue](#propertyvalue-for-schemaidentifier)
- **Description:** Primary identifier for the concept scheme. CDIF core metadata property; takes precedence over `dcterms:identifier`.

### schema:dateModified

- **Cardinality:** Required
- **Content:** string, ISO 8601
- **Description:** Date when the concept scheme was last modified. Takes precedence over `dcterms:modified`.

- **CHOICE — at least one of:**

### schema:license

- **Cardinality:** Required if no conditionsOfAccess
- **Content:** array of string or [object reference](#object-reference)
- **Description:** License for the concept scheme. Takes precedence over `dcterms:license`.

### schema:conditionsOfAccess

- **Cardinality:** Required if no license
- **Content:** array of string
- **Description:** Text statement of access conditions.

## Data Types

## LanguageTaggedValue

- An RDF literal with a language tag, serialized as a JSON-LD value object.

### @value

- **Cardinality:** Required
- **Content:** string
- **Description:** The text content.

### @language

- **Cardinality:** Required
- **Content:** string
- **Description:** BCP 47 language tag (e.g., `en`, `fr`, `de`, `sv`).
```json
{"@value": "Sampled Feature Type vocabulary", "@language": "en"}
```

## Object Reference

- A reference to another node by its `@id`, used for linking to concepts or schemes defined elsewhere in the graph or externally.
```json
{"@id": "https://w3id.org/isample/vocabulary/sampledfeature/anysampledfeature"}
```

### PropertyValue (for schema:identifier)

- When the identifier is not a simple resolvable URI, use `schema:PropertyValue`:

```json
{
  "@type": ["schema:PropertyValue"],
  "schema:propertyID": "https://registry.identifiers.org/registry/doi",
  "schema:value": "10.5683/SP2/TTJNIU",
  "schema:url": "https://doi.org/10.5683/SP2/TTJNIU"
}
```

## Optional Properties

### schema:url

- **Cardinality:** Optional
- **Content:** string.uri
- **Description:** Web location of a page describing the concept scheme. Default: `'missing'`.

### schema:creator

- **Cardinality:** Optional
- **Content:** Person, Organization, or @list
- **Description:** Author or maintainer of the vocabulary.

### skos:definition

- **Cardinality:** Optional
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array
- **Description:** Formal explanation of the meaning or purpose of the scheme.

### skos:altLabel

- **Cardinality:** Optional
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array
- **Description:** Alternative labels (acronyms, abbreviations, spelling variants).

### skos:note

- **Cardinality:** Optional
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array
- **Description:** General note about the scheme.

### cdifConcept

- SKOS Concept with CDIF concept scheme constraints. Represents a single term or category within a concept scheme.

## Optional Properties

### skos:inScheme

- **Cardinality:** Required
- **Content:** [object reference](#object-reference) or array of object references
- **Description:** The concept scheme(s) this concept belongs to. Each must be `{"@id": "scheme-uri"}`.

### skos:notation

- **Cardinality:** Optional, Repeatable
- **Content:** array of string
- **Description:** Classification codes. Should be unique within the scheme.

### skos:broader

- **Cardinality:** Required if concept appears in skos:narrower
- **Content:** array of object references
- **Description:** Broader (parent) concepts. Any concept that is the target of `skos:narrower` on another concept must declare `skos:broader` pointing back. See [Bidirectional hierarchy](#bidirectional-hierarchy) below. Each item is `{"@id": "parent-concept-uri"}`.

### skos:narrower

- **Cardinality:** Optional, Repeatable
- **Content:** array of [CdifConcept](#cdifconcept) or [object reference](#object-reference)
- **Description:** Narrower (child) concepts. If present, each inline child concept must have `skos:broader` pointing back to this concept. Items can be full inline concept objects (for building the JSON tree) or `{"@id": "child-uri"}` references.

### skos:altLabel

- **Cardinality:** Optional
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array
- **Description:** Alternative labels.

### skos:note

- **Cardinality:** Optional
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array
- **Description:** General note.

### skos:topConceptOf

- **Cardinality:** Optional
- **Content:** [object reference](#object-reference) or array
- **Description:** Scheme(s) for which this is a top concept.

## Required Properties

### @id

- **Cardinality:** Required
- **Content:** string.uri
- **Description:** Globally unique, resolvable URI for this concept.

### @type

- **Cardinality:** Required
- **Content:** array
- **Description:** Must include `skos:Concept`.

### skos:prefLabel

- **Cardinality:** Required
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of [LanguageTaggedValue](#languagetaggedvalue)
- **Description:** Preferred label. At most one per language (enforced by SHACL `sh:uniqueLang`).

### skos:definition

- **Cardinality:** Required
- **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array
- **Description:** Formal definition of this concept.

# Bidirectional Hierarchy

CDIF guidelines require concept hierarchies to be expressed in both directions:

- **`skos:narrower`** is needed because the JSON-LD tree is rooted at `skos:hasTopConcept`. Without `skos:narrower`, child concepts cannot be reached by traversing the JSON document from the root.

- **`skos:broader`** is needed for upward navigation and for display trees in vocabulary browsers.

Any concept that appears as a value of `skos:narrower` **must** also declare `skos:broader` pointing back to its parent. Top concepts (those in `skos:hasTopConcept`) should **not** have `skos:broader` within the scheme.

```json
{
  "@id": "sf:anysampledfeature",
  "@type": ["skos:Concept"],
  "skos:prefLabel": "Any sampled feature",
  "skos:definition": "Top concept",
  "skos:inScheme": {"@id": "sf:sampledfeaturevocabulary"},
  "skos:narrower": [
    {
      "@id": "sf:earthmaterial",
      "@type": ["skos:Concept"],
      "skos:prefLabel": "Natural Solid Material",
      "skos:definition": "A naturally occurring solid material.",
      "skos:inScheme": {"@id": "sf:sampledfeaturevocabulary"},
      "skos:broader": [{"@id": "sf:anysampledfeature"}]
    }
  ]
}
```

# Array Convention

Unlike other CDIF profiles, the skos profile does **not** require repeatable properties to always be serialized as arrays. This recognizes standard SKOS practice that allows either a single string or an array for literal values. For example, both of these are valid:

```json
"skos:prefLabel": "Material"
```

```json
"skos:prefLabel": [
  {"@value": "Material", "@language": "en"},
  {"@value": "Matériau", "@language": "fr"}
]
```

Consumers of CDIF concept scheme documents should test whether a value is a string or an array before iterating.

## 5. Provenance of the artifacts

Generated from the canonical [metadataBuildingBlocks](https://github.com/Cross-Domain-Interoperability-Framework/metadataBuildingBlocks) register:

- `cdifConceptSchemeStructuredSchema.json` ← `tools/resolve_schema.py cdifConceptScheme`
- `conceptSchemeRules.shacl` ← byte-copy of `_sources/skosProperties/skosConceptScheme/rules.shacl`

The profile schema (`_sources/profiles/cdifProfile/cdifConceptScheme/schema.yaml`) is self-contained — it inlines the SKOS Concept and language-tagged-value definitions rather than referencing the `skosConceptScheme` building block — so the SHACL shapes are taken directly from the SKOS concept-scheme building block rather than produced by `validate_shacl.py --emit-shapes`. Re-sync these artifacts whenever the source register changes.
