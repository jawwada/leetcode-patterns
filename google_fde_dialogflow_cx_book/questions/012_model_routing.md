# Q012. Design model routing by task, cost, and latency

## Scope and success

Choose among approved model configurations for classification, summarization, retrieval-grounded answers, and complex reasoning. Establish per-task quality floors, latency budgets, residency constraints, and spend limits. The goal is the lowest practical cost while maintaining task-specific correctness.

## Architecture and request path

CX handles conversational routes; the backend classifies the requested generation task using trusted operation metadata. A router applies tenant policy, capability requirements, context size, deadline, quota, and current health. It invokes an eligible model configuration and validates the result before returning it.

Use measured task difficulty or a bounded classifier where useful, but avoid circularly spending more on routing than the task. Define a tested escalation path from a cheaper model to a stronger one when a detectable result requirement fails.

## Data and contracts

The registry records model/configuration ID, supported tasks, regions, context constraints, evaluated datasets, quality results, latency, and cost estimates. Each inference trace records selected configuration and routing reason. Policy versions are part of the release manifest.

## Failure, security, and scale

Fallback models must preserve security and residency requirements. Timeout and quota errors consume part of the same overall deadline. Do not retry every failure across every model. Apply per-tenant budgets and admission control. A stronger model cannot override failed business authorization.

## Trade-off and validation

Static task routing is easier to understand; dynamic routing can adapt to load but complicates reproducibility. Start static and add dynamic decisions based on demonstrated benefit. Compare task success, severe error rate, p95 latency, and cost per successful task across cohorts.

## Interview follow-up answered

**The inexpensive model becomes worse after an update.** Detect the cohort regression, pin or switch to an evaluated configuration, and rerun the affected dataset. Roll back router policy together with model configuration. Production monitoring must distinguish model changes from retrieval or customer-data changes.
