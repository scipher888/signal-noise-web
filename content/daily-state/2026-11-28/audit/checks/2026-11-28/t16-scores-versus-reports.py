import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 't16-scores-versus-reports', 'artifact': 'takeaways', 'type': 'comparison', 'story': 'Benchmarks and builder reports', 'quote': 'Despite ARC Prize verifying 100 percent on ARC-AGI-3 alongside OpenAI-reported benchmark highs, Zvi Mowshowitz and user reports flag struggles with human intent and reward hacking'}


def check(ctx):
    q = ctx.find('gpt', r'On Agents. Last Exam.*Astra sets a new high')
    if not q: return ctx.need('gpt', None, 'Missing company-reported benchmark high.')
    return ctx.require('thezvi', r'ARC Prize: GPT-6\.2 Astra from @OpenAI on ARC-AGI \(Verified\)', r'ARC-AGI-3: 100\.0%.*provider adapter', r'biggest complaint.*failure to understand user intent', r'Reward hacks.*personal benchmarks', r'worry about various forms of reward hacking', note=q)


if __name__ == '__main__':
    run_cli(CLAIM, check)
