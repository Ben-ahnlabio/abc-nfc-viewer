import pathlib

from anv import lib


def test_text_encode_base64():
    text = '<svg xmlns="http://www.w3.org/2000/svg" version="1.2" viewBox="0 0 24 24"><rect x="9" y="1" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="1" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="1" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="8" y="2" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="9" y="2" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="10" y="2" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="2" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="2" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="2" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="14" y="2" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="8" y="3" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="9" y="3" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="10" y="3" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="3" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="3" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="3" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="14" y="3" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="8" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="9" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="10" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="14" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="15" y="4" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="8" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="9" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="10" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="14" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="15" y="5" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="8" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="16" y="6" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#8b532cff"/><rect x="10" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="7" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#8b532cff"/><rect x="9" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="8" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="9" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="10" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#562600ff"/><rect x="10" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#562600ff"/><rect x="11" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#562600ff"/><rect x="15" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#562600ff"/><rect x="16" y="11" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="5" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="7" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="10" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#723709ff"/><rect x="11" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="15" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#723709ff"/><rect x="16" y="12" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="5" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="7" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="13" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="5" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="14" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="14" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="15" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="16" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="17" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="13" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="14" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="18" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="12" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="13" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="14" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="16" y="19" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="11" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#a66e2cff"/><rect x="12" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#a66e2cff"/><rect x="13" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#a66e2cff"/><rect x="14" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="15" y="20" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#a66e2cff"/><rect x="12" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#a66e2cff"/><rect x="13" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#a66e2cff"/><rect x="14" y="21" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="11" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#a66e2cff"/><rect x="13" y="22" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="6" y="23" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="7" y="23" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="8" y="23" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="9" y="23" width="1" height="1" shape-rendering="crispEdges" fill="#713f1dff"/><rect x="10" y="23" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/><rect x="12" y="23" width="1" height="1" shape-rendering="crispEdges" fill="#000000ff"/></svg>'

    png_filepath = lib.svg_text_to_png(text, pathlib.Path(__file__).parent)
    assert png_filepath.exists()
