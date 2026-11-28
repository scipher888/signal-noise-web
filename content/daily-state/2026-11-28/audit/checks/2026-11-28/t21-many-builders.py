import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't21-many-builders', 'artifact': 'takeaways', 'type': 'qualifier', 'story': 'Benchmarks and builder reports', 'quote': 'many builders'}


def check(ctx):
    q = ctx.find('thezvi', r'My process of .*spend your ChatGPT usage on Sol')
    if q and ctx.absent('thezvi', r'many (?:builders|practitioners).*?(?:supervis|default to Sol)'): return ctx.fail('thezvi', q, 'A personal workflow is not evidence of prevalence.')
    return ctx.require('thezvi', r'many (?:builders|practitioners).*?(?:supervis|default to Sol)')


if __name__ == '__main__':
    run_cli(CLAIM, check)
