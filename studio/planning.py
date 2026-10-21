"""Rad-e Hoor production planning pipeline — fine-grained phases."""

from __future__ import annotations

import uuid
from pathlib import Path

from studio.config import Settings, ensure_project_dirs, get_settings
from studio.models import (
    PlanDeliverable,
    PlanStatus,
    ProductionPlan,
    StoryAnalysis,
    utc_now,
)


def _d(
    id: str,
    title: str,
    layer: str,
    acceptance: str,
    role: str,
    depends_on: list[str] | None = None,
) -> PlanDeliverable:
    return PlanDeliverable(
        id=id,
        title=title,
        layer=layer,
        acceptance=acceptance,
        depends_on=depends_on or [],
        agent_role=role,
    )


def build_production_plan(
    analysis: StoryAnalysis | None = None,
    settings: Settings | None = None,
) -> ProductionPlan:
    """Build a precise, dependency-ordered production plan for Rad-e Hoor."""
    settings = settings or get_settings()
    plan_id = f"plan-{uuid.uuid4().hex[:10]}"

    deliverables: list[PlanDeliverable] = [
        # ── P0 Studio (already largely done; keep as explicit gate) ──
        _d(
            "P0-STUDIO-MVP",
            "Studio MVP verified (CLI/API/UI/SQLite/tests green)",
            "P0",
            "pytest green; align/status/approve path works; SQLite file store only",
            "Technical Director",
        ),
        # ── P1 Hearing proof (C0) — start implementation HERE ──
        _d(
            "P1-00-SCAFFOLD",
            "Create game/c0-web scaffold (static web app + local serve script)",
            "P1",
            "Folder game/c0-web with index.html runnable via a documented local server command",
            "Gameplay Engineer",
            ["P0-STUDIO-MVP"],
        ),
        _d(
            "P1-01-TELEMETRY",
            "Shared timed event log + CSV export + session id",
            "P1",
            "Events: sound_played, choice, discovery(+cause), reach_action; downloadable CSV",
            "QA / Playtest Lead",
            ["P1-00-SCAFFOLD"],
        ),
        _d(
            "P1-02-T1-SCENE",
            "Playtest 1 scene: corridor + multiple directional sources (Web Audio HRTF)",
            "P1",
            "~5 min playable corridor; player can point/select 'live now' source; headphones path works",
            "Audio Director",
            ["P1-01-TELEMETRY"],
        ),
        _d(
            "P1-03-T1-BALANCE",
            "Playtest 1 balancing: L/R/F/B equal; half trials echo louder; shuffled order",
            "P1",
            "Config enforces equal direction counts; 50% louder-echo; order randomized per session",
            "Game Designer",
            ["P1-02-T1-SCENE"],
        ),
        _d(
            "P1-04-T1-PROBE",
            "Playtest 1 failure-probe UX: hide cause until after question; reveal button",
            "P1",
            "Fail reason hidden until post-fail prompt answered; reveal control available to facilitator",
            "QA / Playtest Lead",
            ["P1-03-T1-BALANCE"],
        ),
        _d(
            "P1-05-T3-WINDOW",
            "Playtest 3: black screen, reach-toward-sound, exact 10s window [T,E)",
            "P1",
            "5 min build; cold/warm reach feedback without requiring mic; window timing documented",
            "Gameplay Engineer",
            ["P1-01-TELEMETRY"],
        ),
        _d(
            "P1-06-T3-MIC-OPT",
            "Playtest 3 optional local mic level (Bang equivalent only; no raw audio stored)",
            "P1",
            "Mic off by default; if enabled, only local level used; no upload/save of raw PCM",
            "Audio Director",
            ["P1-05-T3-WINDOW"],
        ),
        _d(
            "P1-07-PILOT",
            "Pilot 2–3 strangers/non-close-friends; fix instrumentation bugs only",
            "P1",
            "Pilot notes + patched build; no new systems added; protocol friction logged",
            "QA / Playtest Lead",
            ["P1-04-T1-PROBE", "P1-06-T3-MIC-OPT"],
        ),
        _d(
            "P1-08-ENGINE-SHORTLIST",
            "Engine shortlist memo (Unity vs Godot vs other) — NOT a lock",
            "P1",
            "English ADR draft comparing audio latency, input, PC export; recommendation pending P1-13",
            "Technical Director",
            ["P1-07-PILOT"],
        ),
        _d(
            "P1-09-T2-STEALTH",
            "Playtest 2 night stealth gray-box (Unity or shortlisted engine): shelter, throw rock, tarantulas",
            "P1",
            "10 min build; hearing radii prototype; CPU + audio latency logged on target PC",
            "Gameplay Engineer",
            ["P1-08-ENGINE-SHORTLIST"],
        ),
        _d(
            "P1-10-T4-LEDGE-OPT",
            "Optional Playtest 4 ledge path (outside Go/No-Go)",
            "P1",
            "5 min optional; difficulty tuning only; does not block Go/No-Go",
            "Game Designer",
            ["P1-09-T2-STEALTH"],
        ),
        _d(
            "P1-11-PROTOCOL",
            "Playtest protocol pack: consent, script, questionnaire 1–5, facilitator notes template",
            "P1",
            "English+Persian facilitator pack under projects/rade-hoor/artifacts/playtest-protocol/",
            "QA / Playtest Lead",
            ["P1-07-PILOT"],
        ),
        _d(
            "P1-12-N12",
            "Run N=12 playtest (half gamepad / half MK; ≥50% no prior project knowledge)",
            "P1",
            "12 CSV sessions + questionnaires + same-day facilitator notes stored as evidence",
            "QA / Playtest Lead",
            ["P1-09-T2-STEALTH", "P1-11-PROTOCOL", "P1-04-T1-PROBE", "P1-06-T3-MIC-OPT"],
        ),
        _d(
            "P1-13-GONOGO",
            "Go/No-Go decision report (counts not only %); human gate",
            "P1",
            "reports/c0-go-nogo.md with n/N; pass-all→P2; one fail→2-week redesign; 2+ fails→concept review",
            "Studio Manager",
            ["P1-12-N12"],
        ),
        # ── P2 Vertical slice (C1) ──
        _d(
            "P2-00-ENGINE-ADR",
            "Lock main engine via signed ADR (human gate)",
            "P2",
            "decisions/ADR-main-engine.md approved; repo game/main bootstrapped",
            "Technical Director",
            ["P1-13-GONOGO"],
        ),
        _d(
            "P2-01-HEARING-CORE",
            "Port hearing unit table + Bang attribution into main project",
            "P2",
            "Automated tests or debug overlay prove radius vs Bang independence for key rows",
            "Gameplay Engineer",
            ["P2-00-ENGINE-ADR"],
        ),
        _d(
            "P2-02-SHELTER",
            "Vehicle cabin shelter: contact blocked, sound not erased; breath ≠ Bang",
            "P2",
            "Acceptance scene matching Validation cabin tests; evidence video/log",
            "Gameplay Engineer",
            ["P2-01-HEARING-CORE"],
        ),
        _d(
            "P2-03-PLATE",
            "Plate defense (Art SE-02): plate blocks contact; quiet path remains valid",
            "P2",
            "Player can fail loudly or succeed quietly; no forced combat",
            "Gameplay Engineer",
            ["P2-02-SHELTER"],
        ),
        _d(
            "P2-04-STRAP",
            "Strap rescue (Art SE-05): hazard/goal/anchor co-visible; read-pause not hidden punish",
            "P2",
            "Camera framing checklist pass; timing fair under pause/read",
            "Gameplay Engineer",
            ["P2-03-PLATE"],
        ),
        _d(
            "P2-05-SILENCE-THREE",
            "Three silence endings gray-box: Circle / Escape / Ledge(Anchor)",
            "P2",
            "All three reachable; no echoes outside E01–E07; Rules §7 timing respected in slice",
            "Game Designer",
            ["P2-04-STRAP"],
        ),
        _d(
            "P2-06-A11Y",
            "Slice accessibility: essential info without headphones/mic; captions; reduced motion",
            "P2",
            "Checklist from Art §2.2 / Rules §6 completed with evidence",
            "Audio Director",
            ["P2-05-SILENCE-THREE"],
        ),
        _d(
            "P2-07-SLICE-REPORT",
            "Vertical slice acceptance report (human gate before mass content)",
            "P2",
            "reports/c1-vertical-slice.md cites Rules §§3&7 and SE-02/05/06",
            "Independent Reviewer",
            ["P2-06-A11Y"],
        ),
        # ── P3 Campaign blockout (C2) ──
        _d(
            "P3-00-SPINE",
            "Canyon blockout spine SE→NW with readable corners for sound occlusion",
            "P3",
            "Gray mesh playable drive/walk path; no claim of surveyed real elevation",
            "Technical Director",
            ["P2-07-SLICE-REPORT"],
        ),
        _d(
            "P3-01-CHAPTER-SHELLS",
            "Eleven chapter gray shells with design-minute budgets as soft caps",
            "P3",
            "Chapter markers 0–10 loadable; budgets visible in debug; not final pacing",
            "Game Designer",
            ["P3-00-SPINE"],
        ),
        _d(
            "P3-02-VEHICLE-TOOLS",
            "Vehicle 7 + electric winch + hand puller placement/sound costs",
            "P3",
            "Matches Rules §4.1.1 carry locations; winch Bang 30m documented in-game debug",
            "Gameplay Engineer",
            ["P3-00-SPINE"],
        ),
        _d(
            "P3-03-COMPANIONS-CH9",
            "Chapter 9 dual-path companions without illegal teleport",
            "P3",
            "Sara/Bahram/Dara routing test pass; no spawn/despawn exploits",
            "AI Companion Engineer",
            ["P3-01-CHAPTER-SHELLS", "P3-02-VEHICLE-TOOLS"],
        ),
        _d(
            "P3-04-ECHO-WIRE",
            "Wire only approved echoes E01–E07 to sources",
            "P3",
            "Echo table audit; no unsourced lines",
            "Narrative Lead",
            ["P3-01-CHAPTER-SHELLS"],
        ),
        # ── P4 Content & presentation (C3) ──
        _d(
            "P4-00-CHAR-SHEETS",
            "Character concept sheets from Character Bible (Daniel/Sara/Bahram/Dara/tarantulas)",
            "P4",
            "Sheets in artifacts/art/character-sheets/; Sara unveiled; no religious symbols",
            "Art Director",
            ["P2-07-SLICE-REPORT"],
        ),
        _d(
            "P4-01-ENV-KEY",
            "Key environment concepts for garage, canyon, caravanserai, Hoor heart",
            "P4",
            "Art bible–aligned concepts; everyday Iranian life not exotic-ruin only",
            "Art Director",
            ["P3-00-SPINE"],
        ),
        _d(
            "P4-02-DIALOGUE",
            "Implement screenplay dialogue/tapes for playable chapters in slice→blockout order",
            "P4",
            "FA playable; EN adaptation path started; speaker spoiler rules for echoes held",
            "Narrative Lead",
            ["P3-04-ECHO-WIRE"],
        ),
        _d(
            "P4-03-AUDIO-BANK",
            "SFX bank + music briefs after hearing rhythm locked",
            "P4",
            "artifacts/audio/ with naming; live vs echo visual language respected",
            "Audio Director",
            ["P2-07-SLICE-REPORT"],
        ),
        _d(
            "P4-04-INTEGRATION",
            "Integrate art/audio/dialogue into blockout; content complete for vertical path",
            "P4",
            "Playable integrated build; Independent Review checklist green",
            "Project Manager",
            ["P4-00-CHAR-SHEETS", "P4-01-ENV-KEY", "P4-02-DIALOGUE", "P4-03-AUDIO-BANK", "P3-03-COMPANIONS-CH9"],
        ),
        # ── P5 Ship (C4) ──
        _d(
            "P5-00-PERF",
            "Performance pass on target PC; measure print-style cost",
            "P5",
            "Perf report with hardware specs; reduced-motion mode verified",
            "Technical Director",
            ["P4-04-INTEGRATION"],
        ),
        _d(
            "P5-01-STEAM",
            "Steam packaging path + store page draft assets",
            "P5",
            "Build pipeline documented; no fake sales numbers",
            "Technical Director",
            ["P5-00-PERF"],
        ),
        _d(
            "P5-02-I18N",
            "Complete English adaptation + final FA polish",
            "P5",
            "Localization checklist done; costume/language consistency for Sara held",
            "Localization",
            ["P4-02-DIALOGUE"],
        ),
        _d(
            "P5-03-RELEASE-GATE",
            "Human release gate: public build / marketing",
            "P5",
            "Signed decision in decisions/; playtest evidence attached",
            "Studio Manager",
            ["P5-01-STEAM", "P5-02-I18N"],
        ),
    ]

    summary = (
        "Fine-grained Rad-e Hoor plan: P0 studio gate → P1 hearing playtests "
        "(start at game/c0-web) → P2 vertical slice after Go/No-Go → P3 campaign "
        "blockout → P4 content/art/audio → P5 ship. No mass final art before P2 gate. "
        "No main-engine lock before P1-13."
    )
    if analysis is not None:
        summary += f" Analysis cites {len(analysis.source_paths)} source paths."

    return ProductionPlan(
        id=plan_id,
        project_id=settings.project_id,
        status=PlanStatus.DRAFT,
        summary=summary,
        phases=[
            "P0 — Studio MVP gate",
            "P1 — Hearing proof (Web T1/T3 → pilot → engine shortlist → T2 → N=12 → Go/No-Go)",
            "P2 — Vertical slice (engine ADR → hearing port → shelter/plate/strap/three silences → a11y)",
            "P3 — Campaign blockout (spine, chapter shells, vehicle tools, Ch9 companions, E01–E07)",
            "P4 — Content & presentation (sheets, env, dialogue, audio bank, integrate)",
            "P5 — Ship (perf, Steam, i18n, release gate)",
        ],
        deliverables=deliverables,
        risks=[
            "Teachability of loop + Bang + radii (primary P1 risk)",
            "Web Audio HRTF variance across headphones/OS",
            "Audio latency when moving T2 into engine",
            "Chapter 9 companion dual-path complexity",
            "Bahram 20-year resources still OPEN — must not block P1–P2",
            "Scope creep into 11 chapters before P1 Go/No-Go",
            "Early engine lock before hearing evidence",
            "Mass art before slice acceptance wastes budget",
        ],
        human_gates=[
            "Re-approve this fine-grained production plan",
            "P1-13 Go/No-Go",
            "P2-00 main engine ADR",
            "P2-07 vertical slice acceptance before mass content",
            "P5-03 public release",
            "Any change to loop / Bang / endings / E01–E07 pack",
            "API spend over configured cap; destructive ops",
        ],
    )


def render_plan_markdown(plan: ProductionPlan) -> str:
    lines = [
        f"# Production Plan — {plan.project_id}",
        "",
        f"Plan ID: `{plan.id}`",
        f"Status: **{plan.status.value}**",
        f"Updated (UTC): {plan.updated_at.isoformat()}",
        "",
        "## Summary",
        plan.summary,
        "",
        "## How to start implementation (after approve)",
        "",
        "1. Approve this plan in CLI/UI.",
        "2. Mark `P0-STUDIO-MVP` done with pytest evidence (already mostly true).",
        "3. **First code to write:** `P1-00-SCAFFOLD` → `game/c0-web/` playable corridor harness.",
        "4. Do **not** start character models, music, or full campaign until P1-13 + P2 gates.",
        "",
        "## Phases",
    ]
    for phase in plan.phases:
        lines.append(f"- {phase}")

    # Group deliverables by layer for readability
    layers: dict[str, list] = {}
    for item in plan.deliverables:
        layers.setdefault(item.layer, []).append(item)

    lines.extend(["", "## Deliverables (by phase)"])
    for layer in sorted(layers.keys()):
        lines.append(f"\n### Phase {layer}\n")
        for item in layers[layer]:
            deps = ", ".join(item.depends_on) if item.depends_on else "—"
            lines.extend(
                [
                    f"#### `{item.id}` — {item.title}",
                    f"- Role: {item.agent_role}",
                    f"- Depends on: {deps}",
                    f"- Acceptance: {item.acceptance}",
                    "",
                ]
            )

    lines.extend(["## Risks"])
    for risk in plan.risks:
        lines.append(f"- {risk}")
    lines.extend(["", "## Human gates"])
    for gate in plan.human_gates:
        lines.append(f"- {gate}")
    if plan.approval_note:
        lines.extend(
            [
                "",
                "## Approval",
                f"- Note: {plan.approval_note}",
                f"- At: {plan.approved_at.isoformat() if plan.approved_at else 'n/a'}",
            ]
        )
    lines.append("")
    return "\n".join(lines)


def write_plan(
    plan: ProductionPlan,
    settings: Settings | None = None,
) -> Path:
    settings = ensure_project_dirs(settings)
    plan.updated_at = utc_now()
    path = settings.planning_dir / "production-plan.md"
    path.write_text(render_plan_markdown(plan), encoding="utf-8")
    plan.markdown_path = str(path.relative_to(settings.repo_root))
    json_path = settings.planning_dir / "production-plan.json"
    json_path.write_text(plan.model_dump_json(indent=2), encoding="utf-8")
    return path
