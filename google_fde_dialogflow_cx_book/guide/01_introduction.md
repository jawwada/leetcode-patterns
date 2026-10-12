# 1. Dialogflow CX: the conversational layer

## What this book covers

This guide is for preparing to discuss conversational AI as a Google Forward Deployed AI Engineer. It starts with Dialogflow CX, then develops two detailed designs: a drive-through voice ordering agent and Noctal's web/in-app conversational layer. Kalshi and Polymarket are covered as market-assistant integrations. The foundation material and 30 design answers already written are retained at the end. No additional design-question examples have been added.

The Noctal background supplied by you is: the conversational layer used CX flows, pages, intents, entities, and webhook fulfillment to FastAPI, above agentic workflows. The specific workflows supplied are media search, download/upload, job submission questions, progress tracking, result review, and user-approved follow-up questions. The architecture, names, contracts, transcripts, and operational targets below are proposed implementations for learning. They are not claims about Noctal's actual internals, customer results, or production metrics.

Vendor documentation was checked on October 12, 2026. API shapes, availability, and product names can change; links are included at the relevant concepts. All menu prices, market quotes, job IDs, and performance budgets in the examples are synthetic.

## The mental model

CX manages a conversation as a state machine. A user message is interpreted in the context of the active flow and page. The agent can extract values, ask for missing values, evaluate routes, send responses, and call a webhook. Your backend owns the durable business records and the actual work. A conversation can say "submitted" only after the system responsible for submission confirms the relevant state.

Think of three independent questions: **What did the user mean? Where are we in the conversation? What has the business system actually done?** An intent helps with the first, pages and routes help with the second, and your application services answer the third. Combining all three in one prompt makes it hard to inspect or recover the system.

Google's current Conversational Agents console brings flow and generative capabilities into a shared experience. This book uses the CX vocabulary because it matches your project description. [Console overview](https://docs.cloud.google.com/dialogflow/cx/docs/concept/console-conversational-agents).

## A vocabulary you can transfer to other systems

| CX concept | Meaning in CX | Closest familiar equivalent |
| --- | --- | --- |
| Agent | The configured conversational application | Assistant application or dialogue service |
| Flow | A conversational task area containing pages and handlers | Subworkflow, state-machine module, or dialogue graph |
| Page | A conversational state, possibly with a form | State/node or a step in a wizard |
| Intent | A recognized user purpose, learned from training phrases | Intent classifier output or semantic command label |
| Entity type | A category used to extract and normalize values | Slot type, enum, vocabulary, or extraction schema |
| Parameter | An extracted or assigned value | Typed variable, slot, or workflow input |
| Form | Page parameters to collect, including required values | Slot-filling form or input-validation step |
| Route | A handler selected by an intent and/or condition | Guarded transition or branch in a graph |
| Event handler | A handler for an event such as no input | Exception handler, event subscriber, or recovery branch |
| Fulfillment | Response generation and configured actions | Handler body or response/action callback |
| Webhook | CX's HTTP request to your service for fulfillment | Integration callback, RPC adapter, or tool backend |
| Playbook | Goal, instructions, examples, and tools for a generative task | Agent task recipe or instruction-driven subagent |
| Generator | A configured model call within fulfillment | Prompt template plus model invocation |
| Data store | A configured knowledge source for grounded answers | Retrieval index/knowledge connector |
| Session | Runtime dialogue context | Conversation context or ephemeral state object |
| Version / environment | Resources used to stage and release an agent | Deployment artifact and runtime environment |

These are comparisons of responsibility, not interoperability guarantees. A LangGraph node, a workflow-engine activity, and a CX page have different execution and persistence rules even when they solve a similar modeling problem.

## Why a webhook is only partly like MCP

Both can provide a bridge to external capabilities. A CX webhook is a configured fulfillment endpoint: CX sends a WebhookRequest, your service dispatches a known tag, and the service returns a WebhookResponse. The chosen page or route usually determines the call. It can retrieve a quote, validate a cart, or submit a media job.

MCP is a protocol for an AI host to interact with servers that expose capabilities such as tools, resources, and prompts. Discovery and tool invocation are part of that protocol. A FastAPI endpoint that accepts CX's JSON is not automatically an MCP server. The backend may separately implement an MCP client or expose the same business functions through an MCP server. [CX webhooks](https://docs.cloud.google.com/dialogflow/cx/docs/concept/webhook), [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture).

The useful analogy is: **the webhook handler and an MCP tool handler can call the same application service**. The wire format, caller, discovery mechanism, error model, and authorization context still differ. Share the business function, not a mistaken assumption that the protocols are identical.

## Why a playbook is only partly like a skill

A playbook expresses a goal, instructions, examples, and available tools that guide generative behavior. It can explore a task such as finding media or answering a menu question. A reusable agent skill packages task guidance and may include scripts and reference resources. Both encode procedural knowledge, but a skill package is not inherently a running conversational state machine, and a playbook does not automatically implement the Agent Skills file format. [CX playbooks](https://docs.cloud.google.com/dialogflow/cx/docs/concept/playbook), [Agent Skills overview](https://agentskills.io/home).

A practical design can pair a playbook for exploration with a flow for commitment. The playbook finds candidates and proposes a structured result. A flow asks for required inputs and confirms a versioned operation. The application service enforces whether that operation is allowed.

## A single turn, step by step

1. The channel captures text or speech. A web application normally sends text through a backend session service; a voice integration handles audio transport.
2. The application selects the correct CX session. For logged-in users, it binds that random session identifier to the authenticated principal on the server.
3. CX evaluates the utterance in the active conversational context. It can match an intent and extract parameter values using entity types.
4. A page form may prompt for missing values. A matching route can execute fulfillment and change page or flow.
5. If fulfillment invokes a webhook, FastAPI validates the request and dispatches the configured tag to an application service.
6. The service checks domain rules and authorization, reads or changes durable state, and returns a bounded result.
7. CX updates permitted conversational parameters and produces a response. The channel renders chat text, a card, or synthesized speech.

This sequence is a simplified teaching model. Exact handler evaluation depends on scope and configuration. Use CX's simulator and official handler rules to resolve ordering, especially when a flow-level route and a page-level route can both apply. [State handlers](https://docs.cloud.google.com/dialogflow/cx/docs/concept/handler).

## What "deterministic" means here

Flows explicitly define transitions, forms, and action boundaries. Intent recognition and speech transcription can still be uncertain. A route that commits a purchase is predictable only after the correct inputs and guards are satisfied. Therefore confidence handling, clarification, current backend validation, and explicit confirmation remain necessary.

Generative components expand the range of language and questions the application can handle. They introduce additional variability. Use them where flexible interpretation is valuable, and keep critical mutations behind narrow contracts. Neither an explicit graph nor a fluent model response is evidence that an external operation completed. [Generative and deterministic design](https://docs.cloud.google.com/dialogflow/cx/docs/generative-deterministic).

## How to read the cases

For each case, read the conversation first, then follow the concept map and request path. Finally, inspect what happens when a user corrects a value or a backend call times out. In an interview, that last part often reveals whether the architecture has a durable business model or only a successful demo transcript.
