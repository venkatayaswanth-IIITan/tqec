import pytest

from tqec.gallery.move_rotation import move_rotation
from tqec.utils.enums import Basis


def test_move_rotation_open() -> None:
    g = move_rotation()
    assert g.num_ports == 2
    assert g.num_cubes == 5
    assert g.spacetime_volume == 3
    assert g.num_pipes == 4
    assert len(g.leaf_cubes) == 2
    assert {*g.ports.keys()} == {
        "In",
        "Out",
    }
    assert g.bounding_box_size() == (2, 2, 3)


@pytest.mark.parametrize("obs_basis", [Basis.X, Basis.Z])
def test_move_rotation_filled(obs_basis: Basis) -> None:
    g = move_rotation(obs_basis)
    assert g.num_ports == 0
    assert g.num_cubes == 5
    assert g.num_pipes == 4
    assert len(g.leaf_cubes) == 2
