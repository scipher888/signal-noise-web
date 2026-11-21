import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e34-ties-qwen-3-8-27b-aa-index', 'artifact': 'episode', 'type': 'comparison', 'story': 'Inkling 2 Mini', 'quote': 'ties Qwen 3.8 27B on the Artificial Analysis Index'}


def check(ctx):
    s1 = ctx.find('thinking', r'AA Index')
    s2 = ctx.find('thinking', r'20\.1 \(Best reported score in this row\)')
    s3 = ctx.find('thinking', r'Qwen3\.8-27B')
    if s1 and s2 and s3:
        return ctx.ok('thinking', s2, 'Both Inkling 2 Mini and Qwen3.8-27B report 20.1 on AA Index (v5.0)')
    return ctx.need('thinking', s1 or s2, 'Check AA Index tie with Qwen3.8-27B')


if __name__ == '__main__':
    run_cli(CLAIM, check)
