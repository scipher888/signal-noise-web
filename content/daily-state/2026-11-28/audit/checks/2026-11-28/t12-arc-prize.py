import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't12-arc-prize', 'artifact': 'takeaways', 'type': 'attribution', 'story': 'Benchmarks and builder reports', 'quote': 'ARC Prize verifying 100 percent on ARC-AGI-3'}


def check(ctx):
    return ctx.require('thezvi', r'ARC Prize: GPT-6\.2 Astra from @OpenAI on ARC-AGI \(Verified\)', r'ARC-AGI-3: 100\.0% \(SOTA\).*provider adapter')


if __name__ == '__main__':
    run_cli(CLAIM, check)
