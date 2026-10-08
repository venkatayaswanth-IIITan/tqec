import pytest

from tqec.gallery.cnot import cnot
from tqec.utils.enums import Basis


def test_cnot_open() -> None:
    g = cnot()
    assert g.num_ports == 4
    assert g.num_cubes == 10
    assert g.spacetime_volume == 6
    assert g.num_pipes == 9
    assert len(g.leaf_cubes) == 4
    assert {*g.ports.keys()} == {
        "In_Control",
        "Out_Control",
        "In_Target",
        "Out_Target",
    }
    assert g.bounding_box_size() == (2, 2, 4)


@pytest.mark.parametrize("obs_basis", [Basis.X, Basis.Z])
def test_cnot_filled(obs_basis: Basis) -> None:
    g = cnot(obs_basis)
    assert g.num_ports == 0
    assert g.num_cubes == 10
    assert g.num_pipes == 9
    assert len(g.leaf_cubes) == 4


def test_compose_two_cnots() -> None:
    g1 = cnot()
    g2 = cnot()
    g_composed = g1.compose(g2, "Out_Control", "In_Control")
    assert g_composed.num_cubes == 18
    assert g_composed.num_ports == 4
