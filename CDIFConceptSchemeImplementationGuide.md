# CDIF Concept Scheme Profile — Implementation Guide

## 1. Purpose and scope

The **CDIF Concept Scheme profile module** (`cdifConceptScheme`) describes a **SKOS concept scheme** — a controlled vocabulary of concepts used in CDIF metadata. A typical concept scheme is a community glossary or thesaurus that supplies shared definitions and terms: the concepts used to name variables, classify resources, or qualify measurements in other CDIF profiles.

This module is the register entry for concept schemes. It is built on `skosConceptScheme` and is reserved for concept-scheme-specific extensions and conformance rules.

**Related profile.** A *code list* is a concept scheme whose members are controlled values carrying machine notation codes (`skos:notation`). Code lists are published as the separate [profile-codelist](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist) profile. Use Concept Scheme for a general vocabulary of meanings; use Codelist when each concept must carry a code.

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

Required elements:

- **`@id`** — the scheme's IRI;
- **`@type`** — must include `skos:ConceptScheme`;
- **`skos:prefLabel`** — preferred label (string or language-tagged value; at most one per language);
- **`skos:definition`** — what the scheme is for;
- **`skos:hasTopConcept`** — at least one top-level concept, defining the vocabulary's entry points.

## 3. Concepts

Top concepts (and their narrower concepts) are `skos:Concept` nodes, given inline or by `@id` reference. Each concept carries `skos:prefLabel` and `skos:notation`, and may declare `skos:definition`, `skos:note`, `skos:inScheme`, and the hierarchy relations `skos:broader` / `skos:narrower` (themselves inline concepts or `@id` references). Mapping relations (`skos:exactMatch`, `skos:closeMatch`, `skos:broadMatch`, …) link concepts to terms in other vocabularies.

## 4. Validation

- **JSON Schema** — `cdifConceptSchemeStructuredSchema.json` (Draft 2020-12), generated from the source register.
- **SHACL** — `conceptSchemeRules.shacl`, which targets `skos:ConceptScheme` and checks that a scheme has an IRI identifier, at least one `skos:prefLabel` (with `sh:uniqueLang`), and at least one `skos:hasTopConcept`.

```bash
python FrameAndValidate.py examples/exampleSkosConceptScheme.json --validate
```

`FrameAndValidate.py` frames the document with `cdifConceptScheme-frame.jsonld`, array-wraps the multi-valued SKOS properties, then validates against the JSON Schema. Validation is **open-world**: properties beyond the profile are permitted.

## 5. Provenance of the artifacts

Generated from the canonical [metadataBuildingBlocks](https://github.com/Cross-Domain-Interoperability-Framework/metadataBuildingBlocks) register:

- `cdifConceptSchemeStructuredSchema.json` ← `tools/resolve_schema.py cdifConceptScheme`
- `conceptSchemeRules.shacl` ← byte-copy of `_sources/skosProperties/skosConceptScheme/rules.shacl`

The profile schema (`_sources/profiles/cdifProfile/cdifConceptScheme/schema.yaml`) is self-contained — it inlines the SKOS Concept and language-tagged-value definitions rather than referencing the `skosConceptScheme` building block — so the SHACL shapes are taken directly from the SKOS concept-scheme building block rather than produced by `validate_shacl.py --emit-shapes`. Re-sync these artifacts whenever the source register changes.
