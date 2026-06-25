# Federation API

Status: canonical doctrine draft

## Purpose

The Federation API describes how trust seeds, applications, repositories, manifests, AI stewards, maps, missions, and economy records should communicate.

This document is a design foundation, not a final implementation specification.

## Core Principle

The API should expose the Federation pattern without centralizing unnecessary private data.

Local-first operation comes before remote synchronization.

## Primary Resources

- Trust: a sovereign local instance of the Federation pattern.
- Identity: local, trust-level, public, and agent identity information.
- Tree: seed, roots, trunk, branches, leaves, fruit, and new seeds.
- Mission: a scoped request for useful contribution.
- Contribution: a record of completed work or stewardship.
- Repository: a Git or Forge repository connected to a trust or project.
- Atlas Node: a map-visible trust, project, business, event, mission, or community.
- Governance Proposal: a proposed decision, amendment, or review item.
- Economy Record: a value-flow, listing, bounty, grant, or service record.
- AI Steward Context: the permitted local context available to an AI assistant.

## Design Rules

1. Prefer local-first operation.
2. Require explicit permission before synchronization.
3. Separate public, shared, private, and agent-local data.
4. Pair Markdown-readable documents with machine-readable manifests.
5. Make important writes auditable where practical.
6. Attribute agent actions.
7. Require human confirmation for sensitive actions.
8. Carry maturity labels on claims and projects.
9. Carry compliance status on regulated economic activity.
10. Preserve export, portability, and forkability.

## Manifest-First Implementation

The first implementation layer should use JSON manifests beside Markdown documents.

Examples:

- `federation.manifest.json`
- `trust.manifest.json`
- `tree.manifest.json`
- `agent.policy.json`
- `mission.manifest.json`
- `atlas.node.json`
- `economy.record.json`

## Safety Rule

The API must not make it easy to accidentally publish private trust data.

The safest default is local private data with explicit opt-in federation.

## Design Goal

A future developer should be able to generate an application, AI agent, local workspace, or repository workflow from the same trust seed documents and manifests.
