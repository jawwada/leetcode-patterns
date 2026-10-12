# Q027. Design multimodal document retrieval

## Scope and success

Search manuals containing text, screenshots, scanned tables, and recorded demonstrations. Clarify supported media, languages, accessibility, and citation needs. Success is retrieval and explanation of evidence with correct page, image, or timestamp context.

## Architecture and request path

Ingestion stores original media, extracts OCR/transcripts where appropriate, and creates modality-specific or compatible embeddings. A metadata layer connects text, figures, captions, tables, and video segments. CX gathers the customer's issue; retrieval searches relevant modalities and returns a bounded evidence bundle to an appropriate model.

Keep direct links to original pages or timestamps. The conversational answer describes the evidence and offers accessible alternatives rather than assuming a voice customer can inspect an image immediately.

## Data and contracts

Artifacts carry media type, source/version, page or time range, language, permission, parser model, and extraction quality. Segment IDs connect derived text to originals. Results disclose whether a claim comes from OCR, transcript, or direct visual interpretation where that distinction matters.

## Failure, security, and scale

Quarantine unsupported or malformed media. Low-quality OCR can corrupt amounts or warning labels, so route critical ambiguity to confirmation or human review. Bound video processing and model context. All derived artifacts inherit source access and deletion requirements; thumbnails are sensitive too.

## Trade-off and validation

Text extraction is cheap and searchable but loses visual relationships. Direct multimodal inference preserves context at greater cost. Combine modalities only when evaluated need justifies it. Measure evidence recall, numeric accuracy, temporal localization, citation fidelity, and latency.

## Interview follow-up answered

**A diagram's arrows carry the essential meaning.** Retrieve the figure and surrounding legend for visual processing rather than relying solely on OCR. Preserve the exact version and cite the page. Add a test where extracted text alone would produce the wrong relationship or instruction.
