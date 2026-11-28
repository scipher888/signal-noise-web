import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e03-inkling-demo', 'artifact': 'episode', 'type': 'attribution', 'story': 'Unsloth demos', 'quote': 'On desktop hardware, Unsloth demonstrated a compact open model called Inkling 2 Mini driving Unreal Engine, Unity, and Blender'}


def check(ctx):
    return ctx.require('unslothai', r'Your local LLM can now take control of Unreal Engine, Unity .*Blender', r'Inkling 2 Mini GGUF and Unsloth successfully controlled those apps', r'(?:open.weight|open.source).*Inkling 2 Mini|Inkling 2 Mini.*(?:open.weight|open.source)', r'(?:demo|controlled).*(?:desktop hardware|desktop PC)', note='GGUF and local execution alone do not establish licensing or the demo machine.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
