import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e02-two-announcements', 'artifact': 'episode', 'type': 'number', 'story': 'Creative software', 'quote': 'This week, two separate announcements showed AI stepping straight out of the chat box and taking direct control of creative software'}


def check(ctx):
    a = ctx.find('unslothai', r'local LLM can now take control of Unreal Engine, Unity .*Blender')
    b = ctx.find('gpt', r'animated the results in Blender')
    return ctx.need('unslothai', a, 'Check both publication dates and distinguish direct control from generated code. OpenAI example: ' + str(b))


if __name__ == '__main__':
    run_cli(CLAIM, check)
