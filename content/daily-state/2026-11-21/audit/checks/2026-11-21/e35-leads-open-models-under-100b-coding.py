import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e35-leads-open-models-under-100b-coding', 'artifact': 'episode', 'type': 'comparison', 'story': 'Inkling 2 Mini', 'quote': 'leads open models under a hundred billion parameters on agentic coding benchmarks like DeepSWE and SWE-bench Pro'}


def check(ctx):
    return ctx.require('thinking', r'leads every open-weights model with less than 100B total parameters.*DeepSWE', r'agentic coding benchmarks such as DeepSWE v1\.1 and SWE-bench Pro v2')


if __name__ == '__main__':
    run_cli(CLAIM, check)
