# Q020. Design regional recovery for a CX application

## Scope and success

Maintain agreed customer journeys during a regional failure. Define recovery time, tolerable data loss, data residency, supported channels, and behavior of active sessions. Separate read availability from mutation correctness.

## Architecture and request path

Prepare compatible CX agents/deployments, webhook services, identity access, search generations, and domain data in permitted regions. A routing layer or channel integration detects failure and sends eligible new conversations to the alternate deployment. Domain operation IDs and statuses remain discoverable under the selected database recovery model.

Do not assume live conversation state moves automatically. A resumption flow authenticates the customer and reconstructs safe context from durable tasks. Reconfirm expired or changed proposals. Keep telephony routing and support transfer in the recovery plan.

## Data and contracts

Maintain a release manifest per region, replication state, authoritative write-region policy, recovery epoch, and operation IDs. Search may use an older evaluated generation if freshness is disclosed and acceptable. Business mutations require a defined single-writer or globally coordinated strategy.

## Failure, security, and scale

Prevent two recovered regions independently executing the same operation. Use fencing or database coordination appropriate to the topology. Prevalidate quotas, secrets, key access, and customer-network paths. Failover must not move restricted data outside approved locations.

## Trade-off and validation

Active-active can improve latency and recovery but complicates writes and consistency. Active-passive is simpler with longer recovery. Choose from measured business requirements. Run failure drills covering routing, data lag, pending mutations, channel state, and failback, not only webhook health checks.

## Interview follow-up answered

**The primary comes back while the secondary is writing.** Keep the current recovery authority until reconciliation completes. Fence old writers, verify replication and operation states, and perform controlled failback. Automatic routing based only on endpoint health can create split-brain business actions.
