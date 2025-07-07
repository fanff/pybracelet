

from pybracelet.BData import Assortment, BData


def test_make_valid_input():
    wire_count=6
    bdata = BData(wireCount=wire_count)
    bdata.setNodeColor(0,0, 1)
    bdata.setNodeColor(0,1, 3)
    bdata.setNodeColor(0,2, 5)


    asso:Assortment = bdata.wire_assortment()
    assert bdata.validate_assortment(asso)

    valid_input_gen = asso.generate_valid_inputs(max_wire_count=wire_count)

    valid_inputs = list(valid_input_gen)
    assert len(valid_inputs) == 120