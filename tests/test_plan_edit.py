from studio import service
from studio.db import StudioStore
from studio.models import PlanStatus
from studio.service import bootstrap_alignment


def test_save_plan_edits_resets_approved_to_draft(settings):
    bootstrap_alignment(settings)
    store = StudioStore(settings)
    plan = store.latest_plan()
    assert plan is not None
    service.submit_latest(store)
    service.approve_latest(note="ok", store=store)
    plan = store.get_plan(plan.id)
    assert plan is not None
    assert plan.status == PlanStatus.APPROVED

    result = service.save_plan_edits(
        plan,
        summary="Edited summary",
        phases=["P0 only"],
        risks=["r1"],
        human_gates=["g1"],
        deliverables=[
            {
                "id": "P0-STUDIO-MVP",
                "layer": "P0",
                "title": "Studio gate",
                "agent_role": "Technical Director",
                "depends_on": "",
                "acceptance": "pytest green",
            }
        ],
        store=store,
    )
    assert result["status"] == "draft"
    reloaded = store.get_plan(plan.id)
    assert reloaded is not None
    assert reloaded.status == PlanStatus.DRAFT
    assert reloaded.summary == "Edited summary"
    assert len(reloaded.deliverables) == 1
