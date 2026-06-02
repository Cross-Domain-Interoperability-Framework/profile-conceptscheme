# CDIF Concept Scheme (profile module)

This repository holds the published artifacts for the **CDIF Concept Scheme profile module** — the `cdifConceptScheme` building block from the [metadataBuildingBlocks](https://github.com/Cross-Domain-Interoperability-Framework/metadataBuildingBlocks) source register.

> **Scope.** `cdifConceptScheme` describes a SKOS concept scheme used as a controlled vocabulary in CDIF metadata — a community glossary or code system that supplies definitions and terms (for example, the concepts used to name variables) for use in other CDIF profiles. It is a thin module built on `skosConceptScheme`, reserved for concept-scheme-specific extensions and conformance rules. For controlled-value *code lists* (concepts with required `skos:notation` codes), see the related [profile-codelist](https://github.com/Cross-Domain-Interoperability-Framework/profile-codelist) repository.

## Specification

- **[CDIFConceptSchemeImplementationGuide.md](CDIFConceptSchemeImplementationGuide.md)** — Documentation for the Concept Scheme profile module.
- **[cdifConceptSchemeStructuredSchema.json](cdifConceptSchemeStructuredSchema.json)** — JSON Schema (Draft 2020-12), generated from the source register with `tools/resolve_schema.py`.
- **[conceptSchemeRules.shacl](conceptSchemeRules.shacl)** — SHACL shapes for `skos:ConceptScheme` instances.

## Conformance

A conforming concept scheme is a `skos:ConceptScheme` and declares conformance to:

- `https://w3id.org/cdif/conceptscheme/1.1`

Required elements: a scheme IRI (`@id`), `skos:prefLabel`, `skos:definition`, and at least one `skos:hasTopConcept`.

## Examples

```bash
python FrameAndValidate.py examples/exampleSkosConceptScheme.json --validate
```

`FrameAndValidate.py` frames the document against `cdifConceptScheme-frame.jsonld`, array-wraps the multi-valued SKOS properties (`skos:hasTopConcept`, `skos:altLabel`, `skos:narrower`, `skos:broader`, the match and note properties, etc.), then validates against the JSON Schema. Validation is open-world: unknown properties pass.

## Synced from metadataBuildingBlocks

Generated artifacts; re-sync manually when the source register changes:

| file | source |
|---|---|
| `cdifConceptSchemeStructuredSchema.json` | `python tools/resolve_schema.py cdifConceptScheme -o cdifConceptSchemeStructuredSchema.json` |
| `conceptSchemeRules.shacl` | byte-copy of `_sources/skosProperties/skosConceptScheme/rules.shacl` (the profile schema is a self-contained SKOS wrapper, so `validate_shacl.py --emit-shapes` finds no `$ref`-linked rules to merge) |

Source profile: `_sources/profiles/cdifProfile/cdifConceptScheme/`.

## Development branch

Active work for the 2026-06 review revision is on the `reviewRevision202606` branch. `main` reflects the prior release state. New changes should target the review branch; it is merged to main on release.


## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
