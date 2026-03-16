import os

os.environ.setdefault("KIVY_WINDOW", "mock")
os.environ.setdefault("KIVY_GRAPHICS", "mock")
os.environ.setdefault("KIVY_AUDIO", "mock")
os.environ.setdefault("KIVY_TEXT", "mock")

import pytest

pytest.importorskip("kivy")

try:
    import tabletop.tabletop_view as tabletop_view
    from tabletop.tabletop_view import TabletopRoot
except BaseException as exc:  # pragma: no cover - test environment dependent
    pytest.skip(f"Kivy UI modules unavailable: {exc}", allow_module_level=True)

from tabletop.state.controller import TabletopController, TabletopState
from tabletop.state.phases import UXPhase


@pytest.fixture
def tabletop_root(monkeypatch, mocker):
    monkeypatch.setattr(tabletop_view, "resolve_background_texture", lambda: None)
    state = TabletopState(
        session_configured=True,
        session_finished=False,
        intro_active=True,
        first_player=1,
        second_player=2,
        phase=UXPhase.WAIT_BOTH_START,
        fixation_required=False,
    )
    controller = TabletopController(state)
    root = TabletopRoot(controller=controller, state=state)
    root._input_debouncer.allow = mocker.Mock(return_value=True)
    root._log_interaction_phase = mocker.Mock(return_value=True)
    root.update_user_displays = mocker.Mock()
    root.update_intro_overlay = mocker.Mock()
    return root


def test_continue_after_start_press_syncs_intro_active(tabletop_root):
    tabletop_root.intro_active = True
    tabletop_root.controller.state.intro_active = True

    tabletop_root.continue_after_start_press()

    assert tabletop_root.intro_active is False
    assert tabletop_root.controller.state.intro_active is False
    tabletop_root.update_intro_overlay.assert_called_once()


def test_goto_syncs_view_and_controller_phase(tabletop_root, mocker):
    tabletop_root.apply_phase = mocker.Mock()

    tabletop_root.goto(UXPhase.P2_INNER)

    assert tabletop_root.phase == UXPhase.P2_INNER
    assert tabletop_root.controller.state.phase == UXPhase.P2_INNER
    tabletop_root.apply_phase.assert_called_once()


def test_after_start_first_live_card_tap_reaches_controller_logic(tabletop_root, mocker, monkeypatch):
    widget = mocker.Mock()
    tabletop_root.card_widget_for_player = mocker.Mock(return_value=widget)
    monkeypatch.setattr(
        tabletop_view.Clock,
        "schedule_once",
        lambda callback, *_args, **_kwargs: callback(),
    )

    tabletop_root.continue_after_start_press()
    tabletop_root.tap_card(1, "inner")

    assert tabletop_root.intro_active is False
    assert tabletop_root.controller.state.phase == UXPhase.P2_INNER
    assert widget.flip.call_count == 1
