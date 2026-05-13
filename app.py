import gradio as gr

from app.app import CSS, demo


if __name__ == "__main__":
    demo.launch(
        server_name="0.0.0.0",
        css=CSS,
        theme=gr.themes.Soft(primary_hue="teal", neutral_hue="slate"),
    )
