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

## Changelog — reviewRevision202606 (updates since branched from `main`)

This release-review branch has diverged from `main` with the following updates,
synced from the CDIF **metadataBuildingBlocks** source (see
`git log main..reviewRevision202606` for the full per-commit history):

- **Populated from metadataBuildingBlocks** — `*StructuredSchema.json`, merged SHACL,
  JSON-LD frame, examples, and the normative `FrameAndValidate.py` generated from the
  building-block source; `Examples/` renamed to `examples/`.
- **CDIF v1.1** — profile conformance URIs migrated `/1.0` → `/1.1`.
- **License** standardized on CC-BY-4.0.
- **`@id`-reference tightening** — bare `{@id}` reference slots sealed
  (`additionalProperties: false` + `required: ['@id']`); a canonical `objectReference`
  building block introduced as the strict node reference.
- **`prov:used` wrapper reconciliation** — the base `generatedBy.prov:used` accepts
  role-keyed wrappers (`schema:instrument` / `bios:computationalTool` / `prov:reagent`)
  alongside string / `{@id}` / inline `prov:Entity`; profiles pin a wrapper's shape via
  a constraint-only `if/then` (never a narrowed `anyOf`).
- **`skos:notation` → single string** at concept level (consistent with the codelist
  single-notation design).
- **`FrameAndValidate.py`** (normative, drift-checked against
  `Cross-Domain-Interoperability-Framework/validation`) — two-frame root-`@type`
  selection, context-aware `schema:about`, `--conformance` detection, `cdif:`-`@id`
  re-expansion, and (2026-08) reference-collapse on all document types + blank-node
  dedupe + agent `schema:identifier` unwrap, so `@embed:@always`-framed documents
  validate against the tightened schemas.
- **Examples** conformed to the tightened schemas throughout (PrimaryKey →
  `cdi:ComponentPosition`, reference slots → `{@id}`, CVE `hasIntendedDataType` →
  string, `skos:notation` → string, `schema:additionalType` URI → `{@id}`).


## Development branch

Active work for the 2026-06 review revision is on the `reviewRevision202606` branch. `main` reflects the prior release state. New changes should target the review branch; it is merged to main on release.


## License

This work is licensed under [Creative Commons Attribution 4.0 International (CC BY 4.0)](LICENSE).
