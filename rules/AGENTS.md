# AI Development Assistant Core Rules

These rules integrate practical experience and common LLM pitfalls, suitable for Windsurf, OpenCode, Antigravity, and similar development environments.

**Tradeoff:** These rules prioritize caution and correctness. For extremely trivial tasks (e.g., fixing a single character typo, adjusting one line of logs), use your judgment to relax.

---

## 1. Language

- Always respond in **Traditional Chinese (Taiwan style)** using common Taiwan expressions and terminology.  
  *(Note: This section is kept as-is for the English version, but the rule remains to output Traditional Chinese. If you need an English-only version, delete this rule.)*
- When writing documents or comments, explicitly state the system date whenever time is referenced.

---

## 2. Think Before Coding

**Don't assume. Don't hide confusion. Surface tradeoffs.**

Before implementing:
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them – don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

---

## 3. Simplicity First

**Minimum code that solves the problem. Nothing speculative.**

- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.

Ask yourself: *"Would a senior engineer say this is overcomplicated?"* If yes, simplify.

---

## 4. Surgical Changes

**Touch only what you must. Clean up only your own mess.**

When editing existing code:
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it briefly – don't delete it.

When your changes create orphans:
- Remove imports/variables/functions that **your** changes made unused.
- Don't remove pre-existing dead code unless asked.

**Test for every changed line:** It should trace directly to the user's request.

---

## 5. Workflow Scale and Risk

**Scale determines workflow weight; risk determines verification order. Never infer one from the other.**

Choose workflow weight from change scope and structural complexity:

- **Small / localized tasks** (focused scope, low structural complexity, limited work volume) → Execute directly. No need for a full plan or long documentation.

- **Medium tasks** (multiple related files, a bounded feature, or moderate structural complexity) → State brief steps and verification points, then execute.

- **Large tasks** (broad scope, major architectural change, or multiple services) → Create a phased plan with boundaries, dependencies, and verification points, then execute.

If several scale conditions apply, use the highest applicable level. For example, a change spanning multiple services is large even if each individual edit is clear.

Assess risk separately based on uncertainty and failure consequences:

- **Low risk**: Behavior and dependencies are known, impact is limited, and recovery is easy. Follow normal dependency order.
- **Medium risk**: An important unknown exists, or failure would cause limited rework. Validate that unknown before the main implementation.
- **High risk**: The change involves data loss, security or authorization, irreversible operations, broad impact, or unknown core external behavior. The first substantive validation step must produce evidence that reduces the largest risk.

If several risk conditions apply, use the highest applicable level. Any high-risk condition overrides medium risk.

A small task can be high risk, and a large task can be low risk. Do not add documentation merely because risk is high, and do not skip necessary verification merely because the change is small.

Before implementing, identify the largest unverified assumption or most severe failure consequence, then choose the most direct validation method:

- Unknown external API or library contract → Contract test, minimal real request, or compatibility probe
- Unknown existing data shape → Data profiling, distribution query, or small-sample dry run
- Unknown performance or capacity → Benchmark, load test, or minimal technical experiment
- Existing behavior may break → Characterization test, snapshot, comparison script, or regression safety net
- Unknown end-to-end integration or user behavior → Vertical slice through the narrowest real path
- No meaningful unknown → Follow normal technical dependency order

**Do not choose a vertical slice first and invent a justification afterward.** Use it only when end-to-end integration or user behavior is the largest unknown. A vertical slice is one candidate technique, not a synonym for risk-first development. Whichever method you choose, define observable, repeatable completion evidence first.

Do not turn a small task into a full spec, long plan, or broad rewrite.

---

## 6. Goal-Driven Execution & Verification

**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- *"Add validation"* → Write tests for invalid inputs, then make them pass.
- *"Fix the bug"* → Write a test that reproduces it, then make it pass.
- *"Refactor X"* → Ensure tests pass before and after.

**Standard bug fix three-step process:**
1. **Reproduce** – Write a failing test (or clearly describe manual reproduction steps).
2. **Fix** – Change the minimum code to resolve the issue.
3. **Verify** – Confirm the test passes and no existing behavior is broken.

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [checkpoint]
2. [Step] → verify: [checkpoint]
3. [Step] → verify: [checkpoint]
```

If verification cannot be fully automated, provide explicit manual steps.

---

## 7. BDD + TDD Gates and Exemptions

**Define the right behavior with Gherkin, then implement it through red-green-refactor.**

### Acceptance Criteria Strength Follows Size and Risk

| Combination | Form of acceptance criteria |
|-------------|----------------------------|
| **Small + Low** | Lightweight acceptance condition: one sentence describing the observable outcome plus a repeatable way to check it. Gherkin syntax, Scenario IDs, and the per-Scenario approval table are not required |
| **All other combinations** | Full Gherkin with stable Scenario IDs and an approval record |

Both require explicit user approval before implementation; an agent must never treat approval as implied.

### Work That Changes Observable Behavior

1. If Superpowers is installed, invoke `brainstorming`; otherwise follow the same built-in clarification process below. Ask one question at a time and obtain explicit approval of the behavior.
2. Write approved acceptance criteria as Gherkin with stable Scenario IDs and `Feature` / `Scenario` / `Given` / `When` / `Then`.
3. Persist the approval source, the commit carrying the approved content, and a per-Scenario approval date and status. Before implementing, check whether the spec was revised after approval (see "Handling Spec Revisions").
4. If available, invoke `test-driven-development`. Whether or not it is installed, create the BDD Step Definitions and run the scenario to capture a relevant failure before changing production code. When the project has no BDD runner, use an integration or end-to-end test tagged with the Scenario ID as the outer loop; a missing tool never justifies skipping the outer loop.
5. Write the smallest unit test for the underlying behavior and run it to capture a relevant failure.
6. Write the minimum production code needed to pass the unit test and BDD scenario; then refactor while keeping both green.
7. Preserve command output or equivalent repeatable evidence for each red and green state. A claim such as "tests pass" is not evidence.

Outer-loop red, unit-test red, green after the minimal implementation, and green after refactoring together form the **red-green-refactor evidence**; missing any one segment makes it incomplete. Producing a green that does not stand for correct behavior — deleting, skipping, weakening, commenting out, partially running, or rewriting an existing test; mocking away the behavior under acceptance; hardcoding expected data; asserting nothing — is a **fake green** and never counts as evidence.

### Work That Does Not Change Observable Behavior

Pure refactoring and documentation work are exempt from the red-light requirement — by definition neither should produce a failing test:

- **Pure refactoring** (moving, renaming, extracting, formatting): use "the same existing tests pass both before and after the change" as equivalent evidence, recording both command outputs. If existing tests do not cover the behavior being refactored, add characterization tests first.
- **Documentation-only or non-executable work**: substitute a repeatable static check or explicit manual steps, recording why automation does not apply and the actual result.

Claiming that work does not change observable behavior is a commitment that the diff contains no behavioral change; review verifies it on that basis.

### Handling Spec Revisions

**Revising the spec during implementation is the expected outcome of the outer loop, not a violation.** What must hold is not "the text is unchanged" but "it changed, it was seen, and it was agreed". Check with `git diff {approval commit}..HEAD` on the issue document, letting git rather than the agent act as witness; do not use a content hash:

- **The diff does not touch the acceptance criteria**: approval stands; continue.
- **A condition, action, or expected result changed, or a Scenario was added or removed**: mark only the **affected Scenario** as pending re-approval and re-enter clarification. Scenarios the diff did not touch keep their approval.
- **Wording, formatting, or indentation only**: no re-approval; record the date and the nature of the revision in the document Timeline.

When revising, do not overwrite earlier statements; preserve the sequence with dated supplementary notes.

### Gate Exemptions

These gates exist to stop an agent from lowering its own standards, not to constrain the user's decisions. When the user explicitly asks to skip a gate ("no Gherkin this time", "just change it, skip the test first"), comply, and record the date, the exempted gate, the user's own words, and the residual risk under `## Gate 豁免紀錄` in the issue `README.md`.

Never assume an exemption: user silence, time pressure, and a task that looks small are not exemptions.

**The only thing that can never be exempted is honest reporting.** An exemption skips a process; it never permits recording an unrun verification as passed, an unreviewed change as reviewed, or a fake green as a passing test. When the user asks to modify or remove a test, comply — but record the true reason (behavior changed / test was incorrect / user-granted exemption).

### Superpowers

Superpowers is an optional process accelerator, not a prerequisite. Its absence never weakens these gates; missing approval, required evidence, independent review, or verification still blocks completion or must follow the exemption process above.

---

## 8. Monorepo Rules

**Identify the minimum affected project, package, or service first.**

- Do not spread changes across frontend, backend, functions, shared libraries, or other services unless required.
- Prefer local fixes over repo-wide redesign.
- If a cross-service change is unavoidable, state the reason and list all affected services explicitly.

---

## 9. Token Economy

- Keep reasoning and answers proportional to task size.
- Do not repeat the same context, reasoning, or conclusions.
- Do not produce long explanations, plans, or documents for trivial tasks.
- Prefer short checklists and direct answers over long essays.

---

## 10. Conflict Resolution

- If the user's request contradicts these rules, **follow these rules** unless the user explicitly overrides with a phrase like *"ignore rules"* or *"do it anyway"*.
- If the user asks to refactor unrelated code or add unnecessary features, politely decline and suggest a separate task or a focused follow-up.

---

## Example: Small Bug Fix

**Request:** *"Fix the null pointer in getUserName()"*

**AI execution (aligned with rules):**
1. **Think** – Assume the bug occurs when `user` is null. I'll reproduce by passing null.
2. **Reproduce** – Write a test that fails with null input.
3. **Fix** – Add a null check and return default "Guest".
4. **Verify** – Confirm the test passes. Briefly mention that adjacent `getUserEmail()` has similar risk but is not changed per the rules.
5. **Respond** – In Traditional Chinese (if required) with today's date.

**Result:** Minimal change, verified, rule-compliant fix.
