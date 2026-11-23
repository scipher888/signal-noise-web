import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = {'id': 'e33-cot-rl-tool-use-perplexity', 'artifact': 'episode', 'type': 'qualifier', 'story': 'OpenAI Perplexity', 'quote': 'Chain-of-thought reasoning, reinforcement learning, and tool use do not lower base-model perplexity'}


def check(ctx):
    s_cot = ctx.find('openai', r'chain-of-thought reasoning does not reduce perplexity')
    s_rl = ctx.find('openai', r'reinforcement learning.{0,80}does not (?:reduce|lower) (?:base-model )?perplexity|does not (?:reduce|lower) (?:base-model )?perplexity.{0,80}reinforcement learning')
    s_tool = ctx.find('openai', r'tool use.{0,80}does not (?:reduce|lower) (?:base-model )?perplexity|does not (?:reduce|lower) (?:base-model )?perplexity.{0,80}tool use')
    s_outside = ctx.find('openai', r'Not accounting for advances outside of pretraining')
    found = [s for s in (s_cot, s_rl, s_tool) if s]
    if s_cot and s_rl and s_tool:
        return ctx.ok('openai', ' … '.join(found))
    if s_cot or s_outside:
        return ctx.need(
            'openai',
            ' … '.join([s for s in (s_cot, s_outside) if s]),
            'Source says chain-of-thought reasoning does not reduce perplexity and that the metric does not account for advances outside of pretraining, but it does not explicitly say reinforcement learning and tool use do not lower base-model perplexity',
        )
    return ctx.need('openai', None, 'Could not confirm that CoT, RL, and tool use do not lower base-model perplexity')


if __name__ == '__main__':
    run_cli(CLAIM, check)
