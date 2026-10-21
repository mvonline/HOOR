## New Requirement: Story-Driven Planning and Autonomous Project Management

### 1. Game Story as the Source of Truth

The game story and related design documents will be placed in the `gameStory/` directory at the repository root.

The system must treat this directory as the primary source of truth for the game's narrative, world, characters, mechanics, objectives, and constraints.

The system must not assume that the game is always an exploration or puzzle game. The architecture, tools, agents, and production phases must be selected based on the actual story and game requirements.

Support multiple files and formats where practical, including Markdown, text, JSON, images, and other documented formats. Preserve the original files and track which source documents support each important decision.

### 2. Story Analysis Agent

Before planning production, the AI Studio Manager must initiate a story-analysis workflow.

The workflow should:

1. Discover and index files in `gameStory/`.
2. Extract the game's core concept, genre, target platform, gameplay loop, mechanics, characters, environments, narrative structure, visual direction, audio needs, and technical requirements.
3. Identify missing information, contradictions, technical risks, and assumptions.
4. Separate explicit requirements from AI-generated suggestions.
5. Produce a structured analysis document with links or references to the source files.
6. Ask the human for clarification or approval when a missing decision could significantly affect scope, cost, architecture, or the player experience.

The AI must not silently invent important story details or treat its own assumptions as approved requirements.

### 3. Dynamic Production Planning

After story analysis, the AI Studio Manager must create a production plan tailored to the actual game.

The plan should identify:

- Production phases and their dependencies.
- Features and deliverables for each phase.
- Required Agent roles and responsibilities.
- Required tools, engines, frameworks, and external services.
- Asset requirements, including 2D/3D models, textures, animations, audio, and UI.
- Implementation and testing strategies.
- Estimated effort, resource usage, and AI/API costs where measurable.
- Risks, milestones, acceptance criteria, and human approval gates.

The system must explain why each major tool or technology is selected. It should compare viable alternatives when a decision has significant cost or long-term impact.

Do not force every game through the same fixed production pipeline. Reuse common workflow templates where appropriate, but allow the AI Studio Manager to add, remove, reorder, or split phases according to the game's needs.

### 4. AI Project Manager

The AI Project Manager is the central coordinator responsible for executing the approved production plan.

It must:

1. Convert the approved plan into small, actionable tasks.
2. Build a dependency graph and identify tasks that can run in parallel.
3. Select suitable Agents and registered tools for each task.
4. Assign clear inputs, outputs, constraints, and acceptance criteria.
5. Execute tasks through the orchestration system.
6. Validate outputs using tests, tool results, and independent review.
7. Retry recoverable failures within configured limits.
8. Replan when a task fails, a tool becomes unavailable, or new requirements emerge.
9. Request human approval before major scope changes, costly actions, destructive operations, or public releases.
10. Maintain a persistent record of progress, decisions, costs, blockers, and generated artifacts.
11. Resume unfinished work after a restart without unnecessarily repeating completed tasks.

The Project Manager must report actual progress based on persisted task states and verified outputs. It must never claim that an asset, build, test, or feature is complete without evidence.

### 5. Planning and Approval Workflow

Implement the following workflow:

`Story Discovery → Story Analysis → Requirements and Risk Review → Proposed Production Plan → Human Approval → Task Breakdown → Production → Automated Validation → Independent Review → Integration → Milestone Approval`

Not every task needs human approval. Routine, reversible, low-risk tasks should proceed autonomously within the approved plan.

If the story changes, detect potentially affected requirements, tasks, assets, and milestones. Propose a plan update and request approval when the impact is significant.

### 6. Required Artifacts

Create a dedicated project workspace for generated planning documents and production outputs. Keep generated files separate from the original `gameStory/` inputs.

Suggested structure:

- `gameStory/` — original story and design inputs.
- `projects/<project-id>/analysis/` — story analysis, requirements, assumptions, and risks.
- `projects/<project-id>/planning/` — production phases, dependency graphs, milestones, and estimates.
- `projects/<project-id>/decisions/` — architecture decisions and human approvals.
- `projects/<project-id>/reports/` — progress, test, review, and release reports.
- `projects/<project-id>/artifacts/` — references to generated assets and other deliverables.

The exact structure can be adapted to the existing repository, but original story files must never be overwritten by generated documents.

### 7. First Implementation Milestone

Start by implementing a real, end-to-end story-driven planning workflow:

1. Read the repository and inspect `gameStory/`.
2. Build a story ingestion and analysis pipeline.
3. Generate a structured story analysis with source references and clearly marked assumptions.
4. Generate a proposed production plan with phases, dependencies, tools, Agent roles, risks, and acceptance criteria.
5. Persist the plan and expose its status through the API.
6. Add a human approval step before production execution.
7. Once approved, create executable tasks and allow the Project Manager to coordinate them.
8. Add automated tests covering story ingestion, planning, approval, task creation, failure recovery, and story updates.

If `gameStory/` is empty or missing, report that clearly and provide a way to add the story. Do not fabricate a game story to make the workflow appear successful.

Implement real functionality incrementally. Do not create placeholder Agents that claim to have completed work they did not perform.
