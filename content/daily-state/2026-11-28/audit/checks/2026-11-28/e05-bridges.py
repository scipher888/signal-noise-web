import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e05-bridges', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Unsloth demos', 'quote': 'new built-in MCP bridges in Unsloth Desktop and Studio for Godot, Figma, and Roblox Studio'}


def check(ctx):
    return ctx.support_or_contradict('unsloth', r'built.in MCP bridges in Unsloth Desktop and Studio for Godot, Figma and Roblox Studio', r'search Godot MCP Native, then download and install it', 'Built-in connection choices are not three bridges supplied by Unsloth; Godot needs a separate plugin.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
