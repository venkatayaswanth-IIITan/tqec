import pytest

from tqec.gallery.cz import cz
from tqec.utils.exceptions import TQECError
from tqec.utils.position import Position3D


def test_cz_open() -> None:
    g = cz()
    assert g.num_ports == 4
    assert g.num_cubes == 6
    assert g.spacetime_volume == 2
    assert g.num_pipes == 5
    assert len(g.leaf_cubes) == 4
    assert {*g.ports.keys()} == {
        "In_1",
        "Out_1",
        "In_2",
        "Out_2",
    }
    assert g.bounding_box_size() == (2, 3, 3)


def test_cz_resolve_ports() -> None:
    port_positions = (
        Position3D(0, 0, 0),
        Position3D(1, -1, 1),
        Position3D(0, 0, 2),
        Position3D(1, 1, 1),
    )
    g = cz("XI -> XZ")
    assert [str(g[pos].kind) for pos in port_positions] == ["XZX", "XZZ", "XZX", "XZZ"]

    g = cz(["XI -> XZ", "IZ -> IZ"])
    assert [str(g[pos].kind) for pos in port_positions] == ["XZX", "XZZ", "XZX", "XZZ"]

    g = cz(["ZX -> IX"])
    assert [str(g[pos].kind) for pos in port_positions] == ["XZZ", "XXZ", "XZZ", "XXZ"]

    g = cz(["ZZ -> ZZ"])
    assert [str(g[pos].kind) for pos in port_positions] == ["XZZ", "XZZ", "XZZ", "XZZ"]

    with pytest.raises(
        TQECError,
        match=r"Y basis initialization/measurements are not supported yet.",
    ):
        cz("YI -> XZ")

    with pytest.raises(TQECError, match=r"X_ -> XX is not a valid flow for the CZ gate."):
        cz("XI -> XX")

    with pytest.raises(TQECError, match=r"Port 0 fails to support both X and Z observable."):
        cz(["XI -> XZ", "ZI -> ZI"])


def test_cz_ports_filling() -> None:
    g = cz()
    filled_graphs = g.fill_ports_for_minimal_simulation()
    assert len(filled_graphs) == 2
    assert filled_graphs[0].graph == cz(["XI -> XZ", "IZ -> IZ"])
    assert filled_graphs[1].graph == cz(["ZI -> ZI", "IX -> ZX"])
