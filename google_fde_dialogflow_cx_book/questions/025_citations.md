# Q025. Design answer citations and source verification

## Scope and success

Show customers evidence for material claims while keeping sources accessible and current. Define citation granularity and channel presentation. Success means the cited passage supports the claim and the user may open the source; a plausible-looking link is insufficient.

## Architecture and request path

The retrieval service assigns evidence IDs to approved passages. Generation returns an answer with references to those IDs. A validator checks references exist in the supplied evidence, verifies access and source version, and assesses support for material claims. CX renders short source labels in chat and concise attribution in voice.

Use stable source links or an authorized document viewer rather than exposing private storage URLs. Citation validation should fail or qualify unsupported portions of an answer, with an appropriate recovery path.

## Data and contracts

Evidence records contain document/version, chunk, offsets or page, title, access context, and canonical URI. Generated output contains claim segments and evidence IDs. The renderer maps verified IDs to user-visible links; the model does not invent destination URLs.

## Failure, security, and scale

A revoked document must not remain accessible through cached citation text. Recheck sensitive source access and handle deleted or moved documents. Limit evidence length and validator work. Store sufficient lineage for audits without retaining every unrestricted source payload indefinitely.

## Trade-off and validation

Fine-grained claim citations are more useful but require structured generation and validation. Document-level links are simpler but can conceal unsupported claims. Evaluate citation precision, support coverage, accessible-link rate, and user usefulness, including answers with multiple sources and contradictions.

## Interview follow-up answered

**The citation is real but does not support the sentence.** Existence validation has passed while attribution validation failed. Remove or regenerate that claim from sufficient evidence, or state the uncertainty. Checking that an ID belongs to the evidence bundle is necessary but does not prove entailment.
