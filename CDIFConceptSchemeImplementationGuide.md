\---

title: CDIF Concept Scheme Profile Classes and Properties
date: 2026-09-26
---

# Purpose and scope

The **CDIF Concept Scheme profile** (`cdifConceptScheme`) describes a **SKOS concept scheme** — a controlled vocabulary of concepts used in CDIF metadata. A typical concept scheme is a community glossary or thesaurus that supplies shared definitions and terms: the concepts used to name variables, classify resources, or qualify measurements in other CDIF profiles.

**Related profile.** A *code list* is a concept scheme whose members are controlled values carrying machine notation codes (`skos:notation`). Code lists are published as the separate [profile-codelist](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist) profile. Use Concept Scheme for a general vocabulary of meanings; use Codelist when each concept is only required to carry a code and an English-language label.

This guide is organized by **class**: each class the profile defines gets a section, and every property the schema assigns to that class is documented under it. The authoritative source is `\\\_sources/profiles/cdifProfile/cdifConceptScheme/schema.yaml` in the CDIF [metadataBuildingBlocks](https://github.com/Cross-Domain-Interoperability-Framework/metadataBuildingBlocks) register.

# Table of contents

* [Namespaces](#namespaces)
* [Conformance](#conformance)
* [Classes](#classes)

  * [skos:ConceptScheme](#skosconceptscheme)
  * [skos:Concept (cdifConcept)](#skosconcept-cdifconcept)
  * [schema:Dataset (the catalog record)](#schemadataset-the-catalog-record)
* [Value types](#value-types)

  * [LanguageTaggedValue](#languagetaggedvalue)
  * [ConceptRef](#conceptref)
* [Bidirectional hierarchy](#bidirectional-hierarchy)
* [Array convention](#array-convention)
* [SKOS properties beyond this profile](#skos-properties-beyond-this-profile)
* [Validation](#validation)
* [Provenance of the artifacts](#provenance-of-the-artifacts)

# Namespaces

[^ Back to TOC](#table-of-contents)

```json
"@context": {
  "skos": "http://www.w3.org/2004/02/skos/core#",
  "schema": "http://schema.org/",
  "dcterms": "http://purl.org/dc/terms/",
  "dcat": "http://www.w3.org/ns/dcat#"
}
```

Note that `schema` binds to `http://schema.org/` — the `http` form, not `https`. The two are different IRIs and only the `http` form is recognized here.

# Conformance

[^ Back to TOC](#table-of-contents)

A conforming concept scheme is typed as a `skos:ConceptScheme` and declares conformance to the Concept Scheme profile identifier in its catalog record:

```json
{
  "@context": { "skos": "http://www.w3.org/2004/02/skos/core#" },
  "@id": "https://example.org/vocab/myscheme",
  "@type": \\\["skos:ConceptScheme"],
  "skos:prefLabel": {"@value": "My Vocabulary", "@language": "en"},
  "skos:definition": {"@value": "Shared terms for describing X.", "@language": "en"},
  "skos:hasTopConcept": \\\[ { "@id": "https://example.org/vocab/myscheme/top" } ],
  "schema:subjectOf": {
    "@type": \\\["schema:Dataset"],
    "schema:additionalType": \\\[{"@id": "dcat:CatalogRecord"}],
    "dcterms:conformsTo": \\\[{"@id": "https://w3id.org/cdif/conceptscheme/1.1"}]
  }
}
```

The scheme's four required properties are `@type`, `skos:prefLabel`, `skos:definition` and `skos:hasTopConcept`. Note that **`@id` is not among them** — the schema does not require the scheme to carry an IRI, although the SHACL shapes check that a scheme has an IRI identifier, so a scheme without `@id` passes JSON Schema and fails SHACL. Always supply it.

# Classes

[^ Back to TOC](#table-of-contents)

The profile defines two classes, plus the catalog record that carries the conformance claim.

|class|`@type` token|role|
|-|-|-|
|[skos:ConceptScheme](#skosconceptscheme)|`skos:ConceptScheme`|The vocabulary itself. The document root.|
|[cdifConcept](#skosconcept-cdifconcept)|`skos:Concept`|One concept in the vocabulary.|
|[schema:Dataset](#schemadataset-the-catalog-record)|`schema:Dataset` + `dcat:CatalogRecord`|The catalog record describing the scheme as CDIF metadata. The value of `schema:subjectOf`.|

Values that are structures rather than classes in their own right — `LanguageTaggedValue`, `ConceptRef` — are described under [Value types](#value-types).

## skos:ConceptScheme

[^ Back to TOC](#table-of-contents)

The root object representing the concept scheme.

|property|cardinality|content|
|-|-|-|
|`@type`|**Required**, repeatable|array of string containing `skos:ConceptScheme`|
|`skos:prefLabel`|**Required**|string, LanguageTaggedValue, or array of LanguageTaggedValue|
|`skos:definition`|**Required**|string, LanguageTaggedValue, or array|
|`skos:hasTopConcept`|**Required**, repeatable|array of `cdifConcept` or ConceptRef, at least one|
|`@context`|Optional|object|
|`@id`|Optional (but see [Conformance](#conformance))|string (URI)|
|`skos:altLabel`|Optional|string, LanguageTaggedValue, or array|
|`skos:notation`|Optional, repeatable|array of string|
|`skos:note`|Optional|string, LanguageTaggedValue, or array|
|`schema:version`|Optional|string or number|
|`schema:subjectOf`|Optional|schema:Dataset|

### @context

* **Cardinality:** Optional
* **Content:** object
* **Description:** JSON-LD context declaring the `skos` namespace prefix and any additional prefixes used in concept URIs. When present it must bind `skos` to `http://www.w3.org/2004/02/skos/core#`.

### @id

* **Cardinality:** Optional
* **Content:** string (URI)
* **Description:** URI identifier for this concept scheme. The JSON Schema does not require it, but the SHACL shapes check that a scheme has an IRI identifier, so a scheme without `@id` passes one layer and fails the other. Supply it.

### @type

* **Cardinality:** Required, Repeatable
* **Content:** array of string, at least one, containing `skos:ConceptScheme`
* **Description:** Types the scheme. Must contain `skos:ConceptScheme`.

### skos:prefLabel

* **Cardinality:** Required
* **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of [LanguageTaggedValue](#languagetaggedvalue)
* **Description:** Preferred lexical label for the concept scheme. Each language should appear at most once, enforced in SHACL by `sh:uniqueLang`. Alternate labels go on `skos:altLabel`. Note that the array form accepts **only** language-tagged values, not bare strings — mixing a plain string into an array of labels is not valid, although a single bare string on its own is.

### skos:definition

* **Cardinality:** Required
* **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of either
* **Description:** Formal explanation of the meaning or purpose of this concept scheme — what the vocabulary is for. Required on the scheme, unlike on an individual concept.

### skos:hasTopConcept

* **Cardinality:** Required, Repeatable
* **Content:** array of [cdifConcept](#skosconcept-cdifconcept) or [ConceptRef](#conceptref), at least one
* **Description:** The top-level concepts of the scheme — those with no `skos:broader` within it. The JSON-LD hierarchy is rooted here: all child concepts are reached by traversing `skos:narrower` from these top concepts. Items may be inline concept objects or `@id` references; a scheme built entirely from references carries no concept content of its own.

### skos:altLabel

* **Cardinality:** Optional
* **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of either
* **Description:** Alternative lexical labels for the scheme — acronyms, abbreviations, spelling variants.

### skos:notation

* **Cardinality:** Optional, Repeatable
* **Content:** array of string
* **Description:** Classification code for this concept within a scheme.

### skos:note

* **Cardinality:** Optional
* **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of either
* **Description:** General note about the concept scheme.

### schema:version

* **Cardinality:** Optional
* **Content:** string or number
* **Description:** Version identifier for the concept scheme. Accepts either a string (`"1.2.0"`) or a number (`1.2`); prefer the string form, since a numeric version cannot express a patch level.

### schema:subjectOf

* **Cardinality:** Optional
* **Content:** [schema:Dataset](#schemadataset-the-catalog-record)
* **Description:** used with schema:additionalType = dcat:CatalogRecord to specify properties of the metadata object, distinct from the resource it describes.

## skos:Concept (cdifConcept)

[^ Back to TOC](#table-of-contents)

One concept in the vocabulary: a `skos:Concept` constrained for CDIF concept-scheme use. Because JSON-LD is open-world, any other SKOS property may also be included — see [SKOS properties beyond this profile](#skos-properties-beyond-this-profile).

|property|cardinality|content|
|-|-|-|
|`@type`|**Required**, repeatable|array of string containing `skos:Concept`|
|`skos:prefLabel`|**Required**|string, LanguageTaggedValue, or array of LanguageTaggedValue|
|`@context`|Optional|object|
|`@id`|Optional|string (URI)|
|`skos:notation`|Optional|string|
|`skos:definition`|Optional|string, LanguageTaggedValue, or array|
|`skos:note`|Optional|string, LanguageTaggedValue, or array|
|`skos:inScheme`|Optional|object reference, or array of object reference|
|`skos:broader`|Optional, repeatable|array of ConceptRef or `cdifConcept`|
|`skos:narrower`|Optional, repeatable|array of ConceptRef or `cdifConcept`|

Only `@type` and `skos:prefLabel` are required. A concept may therefore be valid with no `@id`, no definition and no scheme membership — looser than the canonical `skosProperties/skosConcept` building block, which requires `skos:definition` and `skos:inScheme`. A concept that validates here will not necessarily validate against that block.

### @context

* **Cardinality:** Optional
* **Content:** object
* **Description:** JSON-LD context declaring the `skos` namespace prefix. Normally supplied once on the enclosing document rather than per concept.

### @id

* **Cardinality:** Optional
* **Content:** string (URI)
* **Description:** URI identifier for this concept. Not required by the schema, but a concept without one cannot be referenced by `skos:broader`, `skos:narrower` or `skos:hasTopConcept`, and cannot be cited from a data record. Supply it for any concept intended for reuse.

### @type

* **Cardinality:** Required, Repeatable
* **Content:** array of string, at least one, containing `skos:Concept`
* **Description:** Types the concept. Must contain `skos:Concept`.

### skos:prefLabel

* **Cardinality:** Required
* **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of [LanguageTaggedValue](#languagetaggedvalue)
* **Description:** Preferred lexical label for this concept. At most one per language, enforced in SHACL by `sh:uniqueLang`. Alternate labels go on `skos:altLabel`. As on the scheme, the array form accepts only language-tagged values.

### skos:notation

* **Cardinality:** Optional
* **Content:** string
* **Description:** Classification code for this concept within a scheme.

### skos:definition

* **Cardinality:** Optional
* **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of either
* **Description:** Formal explanation of the meaning of this concept. Optional in this profile, although a vocabulary whose purpose is to supply shared meanings should define every concept.

### skos:note

* **Cardinality:** Optional
* **Content:** string, [LanguageTaggedValue](#languagetaggedvalue), or array of either
* **Description:** General note about this concept — scope notes, editorial remarks, usage guidance.

### skos:inScheme

* **Cardinality:** Optional
* **Content:** [object reference](#conceptref), or array of object references
* **Description:** The concept scheme(s) this concept belongs to. Each value is a sealed `{"@id": "scheme-uri"}` reference. Accepts either a single reference or an array, unlike the Codelist profile, where `skos:inScheme` is always an array and is required.

### skos:broader

* **Cardinality:** Optional, Repeatable
* **Content:** array of [ConceptRef](#conceptref) or [cdifConcept](#skosconcept-cdifconcept)
* **Description:** Broader (parent) concepts in the hierarchy. Items are `@id` references or inline concept objects. Any concept that appears as a `skos:narrower` value should point back here — see [Bidirectional hierarchy](#bidirectional-hierarchy). Unlike the Codelist profile, this is not enforced by the JSON Schema.

### skos:narrower

* **Cardinality:** Optional, Repeatable
* **Content:** array of [ConceptRef](#conceptref) or [cdifConcept](#skosconcept-cdifconcept)
* **Description:** Narrower (child) concepts in the hierarchy. Items are `@id` references or inline concept objects; inline objects are how the JSON tree is built. See [Bidirectional hierarchy](#bidirectional-hierarchy).

## schema:Dataset (the catalog record)

[^ Back to TOC](#table-of-contents)

The value of [`schema:subjectOf`](#schemasubjectof): a catalog record describing the concept scheme as CDIF-conformant metadata. This is where profile conformance is declared, and it was undocumented in earlier revisions of this guide.

The record is typed `schema:Dataset` and marked as a catalog record through `schema:additionalType`. There is no class named `dcat:CatalogRecord` — `dcat:CatalogRecord` is an `schema:additionalType` value on the `Dataset` node that documents the metadata record itself.

|property|cardinality|content|
|-|-|-|
|`@type`|**Required**, repeatable|array of string containing `schema:Dataset`|
|`schema:additionalType`|**Required**, repeatable|array containing `{"@id": "dcat:CatalogRecord"}`|
|`dcterms:conformsTo`|**Required**, repeatable|array containing `{"@id": "https://w3id.org/cdif/conceptscheme/1.1"}`|
|`@id`|Optional|string|
|`schema:about`|Optional|object reference|

### schema:additionalType

* **Cardinality:** Required, Repeatable
* **Content:** array of string or object reference, at least one
* **Description:** schema.org property used to assign other type names or identifiers to extend the rdf @type for semantic purposes, without adding property requirements on the object from those types

### dcterms:conformsTo

* **Cardinality:** Required, Repeatable
* **Content:** array of object reference, at least one
* **Description:** Must contain `{"@id": "https://w3id.org/cdif/conceptscheme/1.1"}`. This is the record's claim to conform to this profile. Each item is a sealed `{@id}` reference; a bare string is not accepted.

### schema:about

* **Cardinality:** Optional
* **Content:** object reference
* **Description:** an object reference to the JSON object/graph node that a subjectOf.Dataset\[additionalProperty = dcat:CatalogRecord] describes

The record's `@type` is required and must contain `schema:Dataset`. Its `@id` is optional, and is distinct from the scheme's own `@id` — the record and the vocabulary it describes are different resources.

# Value types

[^ Back to TOC](#table-of-contents)

## LanguageTaggedValue

[^ Back to TOC](#table-of-contents)

An RDF literal with a language tag, serialized as a JSON-LD value object. Accepted on `skos:prefLabel`, `skos:altLabel`, `skos:definition` and `skos:note`, on both the scheme and its concepts.

```json
{"@value": "Sampled Feature Type vocabulary", "@language": "en"}
```

### @value

* **Cardinality:** Required
* **Content:** string
* **Description:** The text content of the literal.

### @language

* **Cardinality:** Optional
* **Content:** string
* **Description:** LanguageTaggedValue/properties/@language values specify the language of the element content using BCP 47 language tag (e.g. en, fr, de).

## ConceptRef

[^ Back to TOC](#table-of-contents)

A reference to a `skos:Concept` defined elsewhere, by URI. **Sealed**: `@id` is required and no other property is permitted. Used inside `skos:broader`, `skos:narrower`, `skos:inScheme` and `skos:hasTopConcept` as the alternative to an inline concept.

```json
{"@id": "https://w3id.org/isample/vocabulary/sampledfeature/anysampledfeature"}
```

# Bidirectional hierarchy

[^ Back to TOC](#table-of-contents)

CDIF guidelines require concept hierarchies to be expressed in both directions:

* **`skos:narrower`** is needed because the JSON-LD tree is rooted at `skos:hasTopConcept`. Without `skos:narrower`, child concepts cannot be reached by traversing the JSON document from the root.
* **`skos:broader`** is needed for upward navigation and for display trees in vocabulary browsers.

Any concept that appears as a value of `skos:narrower` **must** also declare `skos:broader` pointing back to its parent. Top concepts (those in `skos:hasTopConcept`) should **not** have `skos:broader` within the scheme.

Unlike the [Codelist profile](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist), this profile does **not** enforce the back-pointer in its JSON Schema: an inline `skos:narrower` concept that omits `skos:broader` validates here. Treat the rule as a convention this profile expects but does not check.

```json
{
  "@id": "sf:anysampledfeature",
  "@type": \\\["skos:Concept"],
  "skos:prefLabel": "Any sampled feature",
  "skos:definition": "Top concept",
  "skos:inScheme": {"@id": "sf:sampledfeaturevocabulary"},
  "skos:narrower": \\\[
    {
      "@id": "sf:earthmaterial",
      "@type": \\\["skos:Concept"],
      "skos:prefLabel": "Natural Solid Material",
      "skos:definition": "A naturally occurring solid material.",
      "skos:inScheme": {"@id": "sf:sampledfeaturevocabulary"},
      "skos:broader": \\\[{"@id": "sf:anysampledfeature"}]
    }
  ]
}
```

# Array convention

[^ Back to TOC](#table-of-contents)

Unlike other CDIF profiles, this profile does **not** require every repeatable property to be serialized as an array. This recognizes standard SKOS practice, which allows either a single value or an array for literal values. Both of these are valid:

```json
"skos:prefLabel": "Material"
```

```json
"skos:prefLabel": \\\[
  {"@value": "Material", "@language": "en"},
  {"@value": "Matériau", "@language": "fr"}
]
```

Which properties accept which form is set per property, and the [class tables](#classes) above are authoritative. `skos:notation` on the scheme, `skos:hasTopConcept`, `skos:broader` and `skos:narrower` are always arrays; the label and note properties accept a scalar or an array; `skos:inScheme` accepts either.

Consumers should test whether a value is a scalar or an array before iterating.

# SKOS properties beyond this profile

[^ Back to TOC](#table-of-contents)

JSON-LD validation here is open-world: properties the profile does not declare are permitted and are not rejected. The following appeared in earlier revisions of this guide but are **not** in this profile's schema — no cardinality or content rule applies to them, and neither the JSON Schema nor the SHACL shapes check them:

* `skos:topConceptOf` — the inverse of `skos:hasTopConcept`.
* `schema:creator` — author or maintainer of the vocabulary.
* `schema:identifier`, `schema:dateModified`, `schema:license`, `schema:conditionsOfAccess`, `schema:url` — CDIF core metadata properties. These **are** required or offered by the [Codelist profile](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist), which is the source of the confusion: earlier revisions of this guide documented the codelist's requirements as though they applied here. They do not. A concept scheme declares no licence, no modification date and no identifier beyond its `@id`.

Use them where they help. Do not rely on validation to check them, and do not treat their presence as a conformance requirement.

# Validation

[^ Back to TOC](#table-of-contents)

* **JSON Schema** — `cdifConceptSchemeStructuredSchema.json` (Draft 2020-12), generated from the source register. Validates the scheme's required properties (`@type`, `skos:prefLabel`, `skos:definition`, `skos:hasTopConcept`), each concept's required properties (`@type`, `skos:prefLabel`), and the catalog record's required properties when `schema:subjectOf` is present.
* **SHACL** — `conceptSchemeRules.shacl`, which targets `skos:ConceptScheme` and checks that a scheme has an IRI identifier, at least one `skos:prefLabel` (with `sh:uniqueLang`), and at least one `skos:hasTopConcept`.

```bash
python FrameAndValidate.py examples/exampleSkosConceptScheme.json --validate
```

`FrameAndValidate.py` frames the document with `cdifConceptScheme-frame.jsonld`, array-wraps the multi-valued SKOS properties, then validates against the JSON Schema. Validation is **open-world**: properties beyond the profile are permitted.

The two layers do not check the same things, and neither is a superset of the other. The clearest case is `@id` on the scheme: optional in JSON Schema, required by SHACL.

# Provenance of the artifacts

[^ Back to TOC](#table-of-contents)

Generated from the canonical [metadataBuildingBlocks](https://github.com/Cross-Domain-Interoperability-Framework/metadataBuildingBlocks) register:

* `cdifConceptSchemeStructuredSchema.json` ← `tools/resolve\\\_schema.py cdifConceptScheme`
* `conceptSchemeRules.shacl` ← byte-copy of `\\\_sources/skosProperties/skosConceptScheme/rules.shacl`

The profile schema (`\\\_sources/profiles/cdifProfile/cdifConceptScheme/schema.yaml`) is self-contained — it inlines the SKOS Concept and language-tagged-value definitions rather than referencing the `skosConceptScheme` building block — so the SHACL shapes are taken directly from the SKOS concept-scheme building block rather than produced by `validate\\\_shacl.py --emit-shapes`. Re-sync these artifacts whenever the source register changes.

