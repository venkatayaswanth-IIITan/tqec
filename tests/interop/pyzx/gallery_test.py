import pytest
import pyzx as zx

from tqec.gallery.cnot import cnot
from tqec.gallery.cz import cz
from tqec.gallery.move_rotation import move_rotation
from tqec.gallery.three_cnots import three_cnots


@pytest.mark.parametrize(
    "graph_fn, inputs, outputs, qasm",
    [
        (
            cnot,
            (0, 6),
            (3, 9),
            """
            qreg q[2];
            cx q[0], q[1];
            """,
        ),
        (
            cz,
            (0, 3),
            (2, 5),
            """
            qreg q[2];
            cz q[0], q[1];
            """,
        ),
        (
            move_rotation,
            (0,),
            (4,),
            """
            qreg q[1];
            """,
        ),
        (
            three_cnots,
            (1, 4, 8),
            (0, 7, 11),
            """
            qreg q[3];
            cx q[0], q[1];
            cx q[1], q[2];
            cx q[0], q[2];
            """,
        ),
    ],
)
def test_gallery_open_zx(
    graph_fn,
    inputs: tuple[int, ...],
    outputs: tuple[int, ...],
    qasm: str,
) -> None:
    graph = graph_fn().to_zx_graph().g
    graph.set_inputs(inputs)
    graph.set_outputs(outputs)

    circuit = zx.qasm(qasm)

    assert zx.compare_tensors(circuit, graph)
