# AGENTS.md — AI Agent Guidance for CDIF Concept Scheme (profile module)

## Project context

This repository publishes the **CDIF Concept Scheme profile module** (`cdifConceptScheme`). It describes a SKOS concept scheme used as a controlled vocabulary in CDIF metadata. It is a thin module built on `skosConceptScheme`, reserved for concept-scheme-specific extensions. The sibling code-list profile (concepts with required `skos:notation`) lives in `profile-codelist`.

## Key files

- `CDIFConceptSchemeImplementationGuide.md` — module documentation
- `cdifConceptSchemeStructuredSchema.json` — JSON Schema (generated)
- `conceptSchemeRules.shacl` — SHACL shapes for `skos:ConceptScheme`
- `cdifConceptScheme-frame.jsonld` — JSON-LD frame used by `FrameAndValidate.py`
- `examples/` — validated JSON-LD examples
- `FrameAndValidate.py` — frame + JSON Schema validation

## Synced files (manual sync from metadataBuildingBlocks)

- `cdifConceptSchemeStructuredSchema.json` ← `python tools/resolve_schema.py cdifConceptScheme -o <file>`
- `conceptSchemeRules.shacl` ← byte-copy of `metadataBuildingBlocks/_sources/skosProperties/skosConceptScheme/rules.shacl`

> **Why the SHACL is a byte-copy, not an emit-shapes merge.** The profile schema (`cdifProfile/cdifConceptScheme/schema.yaml`) is self-contained — it inlines the Concept / LanguageTaggedValue definitions rather than `$ref`-ing `skosConceptScheme`. `validate_shacl.py --emit-shapes cdifConceptScheme` therefore follows no `$ref` to a building block with shapes and emits 0 triples. The applicable shapes are the SKOS `skos:ConceptScheme` shapes, copied directly. If the profile is later rewired to compose `skosConceptScheme` by `$ref`, switch to the standard emit-shapes sync.

Source profile dir: `metadataBuildingBlocks/_sources/profiles/cdifProfile/cdifConceptScheme/`.

## Conventions

- A concept scheme's root `@type` includes `skos:ConceptScheme`; the `@context` declares the `skos` prefix (`http://www.w3.org/2004/02/skos/core#`).
- Required: `@id` (IRI), `skos:prefLabel`, `skos:definition`, at least one `skos:hasTopConcept`.
- Never strip unknown properties — validation is open-world.

## Validation

```bash
python FrameAndValidate.py examples/<file>.json --validate
```
