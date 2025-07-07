


import pytest

wirecount = [
    6,8,12,16,20]
@pytest.mark.parametrize("wirecount", wirecount)
@pytest.mark.benchmark(group="pix_shader_loop")
def test_brute_iteration(benchmark, wirecount):
    from pybracelet.BData import BChunk, BData, NodeType
    bdata = BData(wireCount=wirecount)
    c = BChunk(bdata, column_index=0)
    c.set_input_wire_colors([0,1]* (wirecount//2))
    
    def run():
        nodetypes = c.enumerate_possible_nodetypes(only_count=False)
        for n in nodetypes:
            c.set_node_types(n)
            c.compute_output()

    benchmark(run)
    