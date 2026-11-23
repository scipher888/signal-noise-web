import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e47-lingsante-training-recipe', 'artifact': 'episode', 'type': 'qualifier', 'story': 'Ant Group LingSante-3.1-flash', 'quote': 'through medical-mixed training, task-specific reinforcement learning, multi-step tool workflows, and multi-teacher on-policy distillation'}


def check(ctx):
    s1 = ctx.find('lingsante', r'medical-mixed pretraining')
    s2 = ctx.find('lingsante', r'task-specific reinforcement learning')
    s3 = ctx.find('lingsante', r'multi-teacher on-policy distillation')
    s_tool = ctx.find('lingsante', r'multi-step tool workflows|tool workflows')
    found = [s for s in (s1, s2, s3, s_tool) if s]
    if s1 and s2 and s3 and s_tool:
        return ctx.ok('lingsante', ' … '.join(found))
    if s1 and s2 and s3:
        return ctx.need(
            'lingsante',
            ' … '.join(found),
            'Model card supports medical-mixed pretraining, task-specific reinforcement learning, and multi-teacher on-policy distillation, but does not list "multi-step tool workflows" as a training method (tool use appears as a post-training target; "multi-stage workflows" is a capability)',
        )
    return ctx.need('lingsante', found[0] if found else None, 'Could not match the stated training recipe')


if __name__ == '__main__':
    run_cli(CLAIM, check)
