import pytest

from tqec.gallery.steane_encoding import steane_encoding
from tqec.utils.enums import Basis


def test_steane_encoding_open() -> None:
    g = steane_encoding()
    assert g.num_ports == 7
    assert g.num_cubes == 19
    assert g.spacetime_volume == 12
    assert g.num_pipes == 20
    assert len(g.leaf_cubes) == 7
    assert g.bounding_box_size() == (4, 3, 4)


@pytest.mark.parametrize("obs_basis", (Basis.X, Basis.Z))
def test_steane_encoding_filled(obs_basis: Basis) -> None:
    g = steane_encoding(obs_basis)
    assert g.num_ports == 0
    assert g.num_cubes == 19
    assert g.num_pipes == 20
    assert len(g.leaf_cubes) == 7
