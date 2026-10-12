# Q022. Design structure-aware document chunking

## Scope and success

Create retrieval units from policies, manuals, and tables without losing critical relationships. Establish document types, languages, citation requirements, and model context limits. Success is retrieval of sufficient evidence with minimal irrelevant context, including exceptions and conditions.

## Architecture and request path

An ingestion parser produces a document tree: headings, paragraphs, lists, tables, and attachments. A chunker groups coherent sections under a token budget, carries heading context, and records links to parent and neighboring blocks. Serving may expand a relevant chunk to include its exception or table legend before generation.

CX supplies the customer's question and required context. Chunking remains an offline concern, with a versioned configuration so changes can be compared and rolled back.

## Data and contracts

Store document version, block IDs, chunk ID, text hash, character/page offsets, parent heading, overlap relationship, and parser/chunker version. Citations refer to stable source locations. Table chunks retain column labels and units; a number without its heading can be misleading.

## Failure, security, and scale

Reject or quarantine parsing failures rather than indexing incomplete text as authoritative. Bound memory for long documents and avoid arbitrary overlap that multiplies cost. Permissions inherit from source boundaries and cannot be weakened when adjacent text is combined. Deduplicate repeated boilerplate without removing meaningful policy differences.

## Trade-off and validation

Small chunks improve precision but can omit dependencies; large chunks preserve context but increase noise and tokens. Evaluate structure-aware and fixed-window baselines on answerable, exception-heavy, and no-answer queries. Measure evidence coverage, citation accuracy, index size, and final answer quality.

## Interview follow-up answered

**The answer depends on a footnote on another page.** Preserve document relationships during parsing and allow bounded evidence expansion using source links. Add a regression case requiring both passages. Increasing every chunk size is a blunt remedy that may worsen unrelated retrieval quality and serving cost.
