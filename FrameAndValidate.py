#!/usr/bin/env python3
"""
CDIF Concept Scheme Profile JSON-LD Framing and Validation Script

Frames SKOS ConceptScheme documents according to the CDIF Concept Scheme profile
and validates them against the structured JSON Schema.

Usage:
    python FrameAndValidate.py <input-conceptscheme.jsonld> [--output framed.json] [--validate] [--schema schema.json] [--frame frame.jsonld]
"""

import json
import argparse
import sys
from pathlib import Path
from pyld import jsonld
import jsonschema
from jsonschema import Draft202012Validator

# Configure the requests-based document loader
jsonld.set_document_loader(jsonld.requests_document_loader())

SCRIPT_DIR = Path(__file__).parent

# Properties that should always be arrays per the CDIF Codelist schema
ARRAY_PROPERTIES = [
    'skos:hasTopConcept',
    'skos:altLabel',
    'skos:notation',
    'skos:narrower',
    'skos:broader',
    'skos:related',
    'skos:exactMatch',
    'skos:closeMatch',
    'skos:broadMatch',
    'skos:narrowMatch',
    'skos:relatedMatch',
    'skos:hiddenLabel',
    'skos:changeNote',
    'skos:editorialNote',
    'skos:historyNote',
    'skos:example',
    'skos:note',
    'skos:scopeNote',
    'schema:subjectOf',
    'dcterms:conformsTo',
]

# Term mappings: unprefixed -> prefixed (to match schema expectations)
TERM_MAPPINGS = {
    'conformsTo': 'dcterms:conformsTo',
}

# Output context for compaction
OUTPUT_CONTEXT = {
    "skos": "http://www.w3.org/2004/02/skos/core#",
    "dcterms": "http://purl.org/dc/terms/",
    "schema": "http://schema.org/",
    "xsd": "http://www.w3.org/2001/XMLSchema#",
}

# Frame without context - uses full IRIs
FRAME_TEMPLATE = {
    "@type": "http://www.w3.org/2004/02/skos/core#ConceptScheme",
    "@embed": "@always"
}


def remove_nulls_and_normalize(obj, parent_key=None):
    """
    Post-process the framed output to match schema expectations:
    1. Remove null values (framing adds null for missing optional properties)
    2. Rename unprefixed terms to prefixed versions
    3. Wrap single values in arrays where schema expects arrays
    4. Normalize @type to always be an array
    """
    if isinstance(obj, list):
        return [remove_nulls_and_normalize(item, parent_key) for item in obj if item is not None]

    if isinstance(obj, dict):
        result = {}

        for key, value in obj.items():
            # Skip null values
            if value is None:
                continue

            # Skip @context - pass through unchanged
            if key == '@context':
                result[key] = value
                continue

            # Rename key if needed
            new_key = TERM_MAPPINGS.get(key, key)

            # Process value recursively
            new_value = remove_nulls_and_normalize(value, parent_key=new_key)

            # Skip if value became None or empty after processing
            if new_value is None:
                continue

            # Normalize @type to array throughout the entire document
            if new_key == '@type' and isinstance(new_value, str):
                new_value = [new_value]

            # Wrap in array if schema expects array and value is not already an array
            if new_key in ARRAY_PROPERTIES and not isinstance(new_value, list):
                new_value = [new_value]

            result[new_key] = new_value

        return result

    return obj


def frame_codelist_document(doc_path, frame_path=None):
    """Frame a CDIF Codelist JSON-LD document using three-step approach"""
    print(f"Loading document: {doc_path}")
    with open(doc_path, 'r', encoding='utf-8') as f:
        doc = json.load(f)

    # Load custom frame if provided, otherwise use minimal frame template
    if frame_path:
        print(f"Loading frame: {frame_path}")
        with open(frame_path, 'r', encoding='utf-8') as f:
            frame = json.load(f)
    else:
        frame = FRAME_TEMPLATE

    # Merge contexts bidirectionally so both expansion and compaction work
    # with all prefixes from either source.
    if frame_path and isinstance(frame, dict) and '@context' in frame:
        doc_ctx = doc.get('@context', {})
        if isinstance(doc_ctx, dict):
            frame_ctx = frame['@context']
            for k, v in frame_ctx.items():
                if isinstance(v, str) and k not in doc_ctx:
                    doc_ctx[k] = v
            doc['@context'] = doc_ctx
            for k, v in doc_ctx.items():
                if isinstance(v, str) and k not in frame_ctx:
                    frame_ctx[k] = v

    # Step 1: Expand the document (resolves all prefixes to full IRIs)
    print("Expanding document...")
    expanded = jsonld.expand(doc)

    # Step 2: Frame the document
    print("Framing document...")
    framed = jsonld.frame(expanded, frame)

    # Step 3: Compact with our desired output context (if using template frame)
    if not frame_path:
        print("Compacting with output context...")
        framed = jsonld.compact(framed, OUTPUT_CONTEXT)

    # Step 4: Extract main ConceptScheme from @graph if present
    result = framed
    if '@graph' in framed and isinstance(framed['@graph'], list):
        scheme = None
        for item in framed['@graph']:
            item_type = item.get('@type', [])
            if isinstance(item_type, str):
                item_type = [item_type]
            if 'skos:ConceptScheme' in item_type:
                scheme = item
                break
        if scheme:
            result = {'@context': framed.get('@context'), **scheme}

    # Step 5: Post-process to remove nulls, normalize terms and array properties
    print("Post-processing output...")
    result = remove_nulls_and_normalize(result)

    return result


def validate_against_schema(framed, schema_path):
    """Validate framed document against JSON Schema"""
    print(f"Loading schema: {schema_path}")
    with open(schema_path, 'r', encoding='utf-8') as f:
        schema = json.load(f)

    # Use Draft 2020-12 validator
    validator = Draft202012Validator(schema)
    errors = list(validator.iter_errors(framed))

    return {
        'valid': len(errors) == 0,
        'errors': errors
    }


def main():
    parser = argparse.ArgumentParser(
        description='CDIF Concept Scheme Profile JSON-LD Framing and Validation Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Frame a SKOS concept scheme and print output
  python FrameAndValidate.py my-conceptscheme.jsonld

  # Frame with custom frame and save output
  python FrameAndValidate.py my-conceptscheme.jsonld --frame cdifConceptScheme-frame.jsonld -o framed.json

  # Validate against the CDIF Concept Scheme Profile schema
  python FrameAndValidate.py my-conceptscheme.jsonld -v --schema cdifConceptSchemeStructuredSchema.json

  # Full workflow: frame and validate
  python FrameAndValidate.py my-conceptscheme.jsonld --frame cdifConceptScheme-frame.jsonld -o framed.json -v --schema cdifConceptSchemeStructuredSchema.json
"""
    )
    parser.add_argument('input', help='Input JSON-LD file to process')
    parser.add_argument('-o', '--output', help='Write framed output to file')
    parser.add_argument('-v', '--validate', action='store_true', help='Validate against JSON Schema')
    parser.add_argument('--schema', default=str(SCRIPT_DIR / 'cdifConceptSchemeStructuredSchema.json'),
                        help='Path to JSON Schema (default: cdifConceptSchemeStructuredSchema.json)')
    parser.add_argument('--frame', default=str(SCRIPT_DIR / 'cdifConceptScheme-frame.jsonld'),
                        help='Path to JSON-LD frame (default: cdifConceptScheme-frame.jsonld)')

    args = parser.parse_args()

    try:
        framed = frame_codelist_document(args.input, args.frame)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(framed, f, indent=2)
            print(f"Framed output written to: {args.output}")
        elif not args.validate:
            print("\nFramed output:")
            print(json.dumps(framed, indent=2))

        if args.validate:
            print("\nValidating against schema...")
            result = validate_against_schema(framed, args.schema)

            if result['valid']:
                print("Validation PASSED")
            else:
                print("Validation FAILED")
                print("\nErrors:")
                for error in result['errors']:
                    path = '/'.join(str(p) for p in error.absolute_path) if error.absolute_path else '/'
                    print(f"  - /{path}: {error.message}")
                sys.exit(1)

        print("\nDone!")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
