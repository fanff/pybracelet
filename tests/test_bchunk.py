


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


def test_enumerate_possible_nodetypes():
    bdata = BData(wireCount=6)
    bdata.setNodeColor(0,0, 1)
    bdata.setNodeColor(0,1, 3)
    bdata.setNodeColor(0,2, 5)


    asso = bdata.wire_assortment()
    assert bdata.validate_assortment(asso)

    c = BChunk(bdata, column_index=0)
    c.set_input_wire_colors([1, 2, 3, 4, 5, 6])
    
    nodetypes = c.enumerate_possible_nodetypes()
    
    assert c.enumerate_possible_nodetypes(only_count=True) == 64  # 3 nodes with 4 types each
    alls = list(nodetypes)  # Force evaluation of the generator 
    assert len(alls) == 64  # 3 nodes with 4 types each (4^3 = 64) 


    valid_nt = []
    invalid_nt = []
    for nt in alls:
        c.set_node_types(nt)
        c.compute_output()
        if c.colors == [1, 3, 5] :
            valid_nt.append(nt)
        else:
            invalid_nt.append(nt)
    assert len(valid_nt) == 8
    assert len(invalid_nt) == 56

def test_enumerate_possible_nodetypes():
    bdata = BData(wireCount=6)
    bdata.setNodeColor(0,0, 1)
    bdata.setNodeColor(0,1, 3)
    bdata.setNodeColor(0,2, 5)


    asso = bdata.wire_assortment()
    assert bdata.validate_assortment(asso)

    c = BChunk(bdata, column_index=0)
    input_deck = list(c.enumerate_possible_input_wire_colors(asso))
    
    input_wire_colors, node_types = input_deck[0]
    assert len(input_wire_colors) == 6
    assert len(node_types) == 3   

    assert len(input_deck) == 64
        