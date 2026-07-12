import os
import base64
import requests


def save_graph_visuals(app, output_dir: str = "outputs") -> None:
    os.makedirs(output_dir, exist_ok=True)
    compiled_graph = app.get_graph()

    mermaid_text = compiled_graph.draw_mermaid()
    with open(f"{output_dir}/graph.mmd", "w", encoding="utf-8") as f:
        f.write(mermaid_text)

    try:
        png_bytes = compiled_graph.draw_mermaid_png()
        with open(f"{output_dir}/graph.png", "wb") as f:
            f.write(png_bytes)
        print(f"[visualize] Saved {output_dir}/graph.png")
    except Exception as e:
        print(f"[visualize] PNG export failed (needs internet access): {e}")

    try:
        encoded = base64.urlsafe_b64encode(mermaid_text.encode("utf8")).decode("ascii")
        svg_resp = requests.get(f"https://mermaid.ink/svg/{encoded}", timeout=15)
        svg_resp.raise_for_status()
        with open(f"{output_dir}/graph.svg", "wb") as f:
            f.write(svg_resp.content)
        print(f"[visualize] Saved {output_dir}/graph.svg")
    except Exception as e:
        print(f"[visualize] SVG export failed (needs internet access): {e}")
        print(f"[visualize] Fallback: paste {output_dir}/graph.mmd into https://mermaid.live")
