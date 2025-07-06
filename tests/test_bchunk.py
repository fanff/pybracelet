


from pybracelet.BData import BChunk, BData, NodeType


def test_wire_index():
    bdata = BData(wireCount=8)
    c = BChunk(bdata, column_index=0)
    
    assert c.wire_count() == 8
    
    assert c.input_wire_indice_for_node(0) == (0,1)
    assert c.input_wire_indice_for_node(1) == (2,3)
    assert c.input_wire_indice_for_node(2) == (4,5)
    assert c.input_wire_indice_for_node(3) == (6,7)


   
    c = BChunk(bdata, column_index=1)
    assert c.input_wire_indice_for_node(0) == (1,2)
    assert c.input_wire_indice_for_node(1) == (3,4)
    assert c.input_wire_indice_for_node(2) == (5,6)

def test_compute_output():
    bdata = BData(wireCount=6)
    c = BChunk(bdata, column_index=0)
    assert c.wire_count == 6
    c.set_input_wire_colors([1, 2, 3, 4, 5, 6])
    c.set_node_types([NodeType.RR, NodeType.RR, NodeType.RR])

    c.compute_output()
    assert c.output_wire_colors == [2, 1, 4, 3, 6, 5]
    assert c.colors == [1,3,5] 
