import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e50-arc-verifier', 'artifact': 'episode', 'type': 'attribution', 'story': 'Astra benchmarks', 'quote': 'ARC Prize verified it as the first model to score 100 percent on ARC-AGI-3'}


def check(ctx):
    return ctx.require('thezvi', r'ARC Prize: GPT-6\.2 Astra from @OpenAI on ARC-AGI \(Verified\)', r'GPT-6\.2 Astra is the first model to achieve a 100% score on ARC-AGI-3', r'ARC-AGI-3: 100\.0%.*provider adapter', note='Verified result uses the provider adapter, not the standard harness.')


if __name__ == '__main__':
    run_cli(CLAIM, check)
