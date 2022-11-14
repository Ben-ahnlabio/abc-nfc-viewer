import pathlib
import tempfile


from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM


def svg_text_to_png(svg_text: str, output_path: pathlib.Path) -> pathlib.Path:
    with tempfile.TemporaryDirectory() as dir:
        svg_filepath = pathlib.Path(dir) / "tmp.svg"
        with svg_filepath.open("w") as f:
            f.write(svg_text)

        drawing = svg2rlg(svg_filepath)
        target = output_path / "img.png"

        renderPM.drawToFile(drawing, target, dpi=72 * 20, fmt="PNG")
        return target
