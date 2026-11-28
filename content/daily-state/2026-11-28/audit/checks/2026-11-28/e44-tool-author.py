import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e44-tool-author', 'artifact': 'episode', 'type': 'attribution', 'story': 'GGUF defenses', 'quote': 'Root0ne released an open-source scanner and sanitizer called gguf-radar'}


def check(ctx):
    return ctx.require('gguf', r'Root0ne\s*/\s*gguf-radar', r'open-source tool gguf-radar detects these templates and hidden bytes.*rebuilds a clean GGUF file')


if __name__ == '__main__':
    run_cli(CLAIM, check)
