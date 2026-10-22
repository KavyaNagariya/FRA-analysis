# [ISSUE-009] Build Precision Industrial Master Layout Shell & Telemetry Header

- **ID**: ISSUE-009
- **Type**: `wayfinder:prototype` (HITL)
- **Status**: Closed
- **Assignee**: Antigravity
- **Blocked By**: None
- **Blocks**: ISSUE-010, ISSUE-012, ISSUE-013, ISSUE-014

---

## Question

How should the global navigation, system status telemetry header (active unit ID, IEEE compliance badge, system health indicator), and shared industrial responsive container grid be structured across all 4 views (Workbench, History, Standards, Landing)?

---

## Resolution

Successfully evaluated and resolved the master layout shell and global navigation architecture through an interactive HITL prototype (`/prototype/layout`) and codified the approved architecture into `app/templates/base.html`:

1. **Architecture Decision (Variant B Selected)**:
   - **Left Avionics Command Rail**: 68px (compact) to 224px (expanded) vertical navigation rail hosting instrument identity (`FRA-INSTRUMENT // V4.1`), pulsing CRT emerald status beacon (`SYS ONLINE`), view navigation (`WORKBENCH`, `FLEET RECORDS`, `STANDARDS KB`, `OVERVIEW`), and bottom hardware bus telemetry (`GPIB / ETHERNET OK`, `14ms latency`).
   - **Top Context Telemetry Strip**: 56px sticky header displaying asset hierarchy breadcrumb (`SUBSTATION-01 / TX-765KV-MAIN-01`), IEEE Std C57.149 / IEC 60076-18 compliance tag, real-time diagnostic status badge (`HEALTHY`, `WARNING`, or `DANGER` with correlation $R^2$), and rapid action button (`[+ INGEST CSV]`).
   - **1px Structural Grid Container**: Shared high-density responsive canvas with 1px slate structural borders (`#1e293b`), tactile inset bevels, custom slim scrollbars, and dual-typeface hierarchy (`Inter` + `JetBrains Mono`).

2. **Artifacts & Implementations**:
   - Master template: [`app/templates/base.html`](../app/templates/base.html) providing extensible blocks (`{% block content %}`, `{% block extra_head %}`, `{% block extra_scripts %}`).
   - Interactive prototype: [`app/templates/prototype_layout.html`](../app/templates/prototype_layout.html) with floating switcher at route `/prototype/layout` evaluating Variants A, B, and C across all 4 views.

3. **Downstream Unblocking**:
   - Fully unblocks [ISSUE-010](ISSUE-010-sfra-workbench-redesign.md), [ISSUE-012](ISSUE-012-history-fleet-records-redesign.md), [ISSUE-013](ISSUE-013-standards-and-knowledge-base-redesign.md), and [ISSUE-014](ISSUE-014-precision-industrial-landing-experience.md) to inherit directly from `base.html`.

