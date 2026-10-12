# Q016. Design prompt-injection defenses

## Scope and success

Protect an agent that reads documents and uses enterprise tools. Threats include instructions hidden in sources, user attempts to change tenant or role, and tool output encouraging unauthorized actions. Define approved capabilities and the data each task requires.

## Architecture and request path

CX routes into bounded tasks. The retrieval service returns permitted evidence with provenance. The model receives clear task instructions and separated data, but its proposed tool call goes through a policy-enforcing gateway. Backend services verify principal, arguments, action class, and current resource state. Consequential actions require a valid proposal and confirmation flow.

Use fixed tool endpoints and destination allowlists. A retrieved URL or document instruction cannot create a new network capability. Reduce context and output fields so compromised content has less opportunity to influence unrelated work.

## Data and contracts

Record tool proposal, policy decision, evidence sources, operation, and safe security category. Tools accept typed identifiers rather than arbitrary shell, SQL, or URLs where possible. Mark retrieved content as evidence; never treat a statement that it came from an administrator as authenticated authority.

## Failure, security, and scale

Fail closed on authorization ambiguity. Keep secrets outside model context. Apply egress restrictions, read-only identities, resource budgets, and independent output checks. Content detection can add defense but will have false positives and misses. Limit agent loops and cross-tool data movement.

## Trade-off and validation

Broader tools improve flexibility while widening the attack surface. Narrow domain tools are easier to secure and evaluate. Test malicious documents, encoded instructions, fake system messages, forged tool outputs, cross-tenant requests, and attempts to exfiltrate via citations or destinations.

## Interview follow-up answered

**Can a better prompt solve injection?** It can improve behavior, but it cannot enforce backend identity or network access. Keep model proposals subordinate to executable policy. Measure prompt defenses as one layer while relying on authorization and capability boundaries for critical protection.
