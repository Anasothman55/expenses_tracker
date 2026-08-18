# app/emails/renderer.py
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pathlib import Path

_env = Environment(
  loader=FileSystemLoader(Path(__file__).parent / "templates"),
  autoescape=select_autoescape(["html"]),
)

def render_template(template_name: str, context: dict) -> str:
  return _env.get_template(template_name).render(**context)