# Q001. Design an enterprise RAG assistant with Dialogflow CX

## Scope and success

Support employees asking questions across internal policies and engineering documents. Assume multiple tenants, changing permissions, and frequent document updates. Success means a useful answer backed by accessible, current evidence. Establish freshness targets separately for ordinary edits and access revocation.

## Architecture and request path

An authenticated channel binds a CX session to an employee. CX collects ambiguous context through a flow or runs a bounded knowledge playbook. A retrieval service receives the question and trusted principal, searches a permission-filtered lexical/vector index, reranks candidates, and gives a model a limited evidence bundle. The answer includes source identifiers that the backend validates before presentation.

Ingestion independently reads approved sources, parses sections and tables, attaches ACLs and effective dates, embeds chunks, and publishes an index generation. Updates and deletions are idempotent jobs. CX keeps the conversational topic while source systems remain authoritative for access.

## Data and contracts

Documents carry tenant, source ID, version, ACL reference, language, and effective dates. Chunks retain parent IDs and citation offsets. Answer results contain status, text, citations, and evidence version. Distinguish insufficient evidence from denied access and infrastructure failure without disclosing restricted document existence.

## Failure, security, and scale

Use trusted access filters before retrieval and authoritative checks where indexed ACLs can lag. Cache by authorization context and index generation. Rate-limit expensive queries, bound context, and keep ingestion off the interactive path. On retrieval failure, offer a source-navigation or human path; model background knowledge must not silently replace missing enterprise evidence.

## Trade-off and validation

Managed data stores reduce ingestion work; custom retrieval provides control over ranking, permissions, and freshness. Evaluate both with held-out questions, denied-access cases, deletion tests, retrieval recall, groundedness, and cost per answered task.

## Interview follow-up answered

**What if access must disappear immediately?** Add a source-backed revocation/version check before evidence enters generation, invalidate affected caches, and fail closed if authorization cannot be established. Background index synchronization alone cannot satisfy immediate revocation.
