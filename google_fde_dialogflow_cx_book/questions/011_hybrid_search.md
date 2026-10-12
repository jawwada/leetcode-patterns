# Q011. Design hybrid keyword and vector search

## Scope and success

Retrieve enterprise evidence for questions containing both precise terminology and paraphrase. Assume product codes, policy names, and ordinary language. Success means relevant permitted evidence appears within a bounded candidate budget; answer quality is evaluated downstream separately.

## Architecture and request path

CX sends the question and collected context to a retrieval webhook. After authorization, the service runs lexical and embedding searches in parallel over compatible corpus generations. Each branch applies tenant and access filters. Combine ranked candidates using a method such as reciprocal-rank fusion, deduplicate by source/section, then rerank a bounded set.

Exact identifiers can use a deterministic lookup path. An order number should not compete with general semantic similarity. Preserve original wording alongside any rewritten query so diagnostics can explain retrieval changes.

## Data and contracts

Each candidate carries source ID, chunk ID, document version, branch rank, permitted metadata, and text. Avoid adding raw lexical and vector scores directly: their scales are not naturally comparable. The result contract includes evidence and retrieval diagnostics, not an unsupported truth-confidence number.

## Failure, security, and scale

Set independent branch deadlines. If one branch fails, return an evaluated degraded result or insufficient evidence. Do not remove filters during fallback. Bound candidate count and reranker context; cache embeddings and stable query results with authorization/version keys. Monitor index-version skew between branches.

## Trade-off and validation

Hybrid search adds latency and operational complexity but covers exact and semantic matching failures. Tune branch sizes and fusion on held-out queries. Measure recall at candidate cutoff, ranking quality, no-answer behavior, latency, and access leakage. Compare against each branch alone.

## Interview follow-up answered

**A query includes an exact policy code and a vague question.** Route the code through lexical or authoritative metadata lookup, restrict candidate sources to that policy when appropriate, then use semantic matching within its sections. Preserve version and country constraints; a similar policy with another effective date is not interchangeable.
