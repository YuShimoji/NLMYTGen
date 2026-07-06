# Episode 002 Review Layout Research

This packet evaluates the current compact review cockpit as a weak-pass prototype and benchmarks better layout patterns before another UI implementation.

## Current UI Failure Modes

- The top screen still assumes the reader understands project vocabulary and internal artifact names.
- The three choices are visible, but the page does not help a novice decide which one applies.
- Status rows and gate chips explain what the tool knows before the user understands the job.
- Source records are correctly secondary, but the first screen still feels like an audit cockpit.
- Tests currently reward structure counts more than user-task semantics.

## Research Basis

- NN/g dashboard guidance: Dashboards are useful when a single page supports quick action from at-a-glance information. Source: https://www.nngroup.com/articles/dashboards-preattentive/
- NN/g progressive disclosure: Advanced or rare detail belongs behind a secondary step so the primary choice stays learnable. Source: https://www.nngroup.com/articles/progressive-disclosure/
- NN/g cognitive-load form principles: Structure, transparency, clarity, and support reduce the mental effort of deciding what to do. Source: https://www.nngroup.com/articles/4-principles-reduce-cognitive-load/
- NN/g card component definition: Cards work when each card has one subject and can be scanned as a unit. Source: https://www.nngroup.com/articles/cards-component/
- GOV.UK task list component: Task lists are for multi-step services and should not be used merely to show answers. Source: https://design-system.service.gov.uk/components/task-list/
- GOV.UK complete multiple tasks pattern: A task list helps when users must understand tasks, order, and completion state. Source: https://design-system.service.gov.uk/patterns/complete-multiple-tasks/

## Reusable Design Principles

- Explain the job before artifact state: First screen should answer what this page is for, whether it fits the user's situation, and the next action.
- One decision path, not equal artifact panels: The layout should guide the user through the real input, YMM4 observation, or hold decision.
- Source records stay secondary: Show provenance after the user understands the decision, not before.
- Use durable user language: Prefer user task labels over internal enum-like labels in the primary surface.
- Layout should absorb more evidence without becoming an audit log: Add source records to a secondary evidence drawer, not to the first screen.
- Safety gates are visible but not the main task: Closed gates should reassure and constrain, not dominate the primary action.
- Tests should validate meaning, not exact layout counts: Future checks should assert task hierarchy, selected recommendation, source records secondary, dependency absence, and gate integrity.

## Pattern Benchmark Result

The guided decision flow wins because the work is not broad monitoring; it is one human decision that must be made safely by someone who may not know the project history.

Selected candidate: `candidate_b_guided_decision_flow`.

Primary wireframe file:

`production_pilots/yukkuri_newsroom_content_spine_002/review_layout_research/candidate_wireframes.html`
