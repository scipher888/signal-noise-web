"""Writes one executable check file per claim. Claim list = Neon's extraction (claims_draft/) plus objection checks.
Bodies are hand-written deterministic code; re-run this file to regenerate the .py checks."""
from pathlib import Path
H = Path(__file__).resolve().parent
HDR = '''import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / 'lib'))
from auditlib import *  # noqa

CLAIM = %r


def check(ctx):
%s


if __name__ == '__main__':
    run_cli(CLAIM, check)
'''
C = []
def c(id, artifact, type, story, quote, body):
    C.append((id, dict(id=id, artifact=artifact, type=type, story=story, quote=quote), body))

# ======================= EPISODE =======================
E = 'episode'
c('e00-date', E, 'number', 'Intro', 'November 20th, 2026', '''    return ctx.ok(None, None, 'edition date matches audit date %s' % ctx.date) if ctx.date == '2026-11-20' else ctx.fail(None, None, 'date mismatch')''')
c('e01-journal-scope', E, 'number', 'Society', 'nearly a thousand AI scientists ran its own peer-reviewed journal', '''    # Who founded the journal? The abstract scopes it to agents in ONE laboratory.
    s = ctx.find('society', r'agents in one laborator\\w* also founded the Journal')
    sent = ctx.art_sentence(CLAIM['quote'])
    if s and not re.search(r'one lab', sent, re.I):
        return ctx.fail('society', s, 'artifact credits the whole ~1,000-agent society with running the journal; source says agents in one laboratory founded it')
    return ctx.ok('society', s)''')
c('e02-matched-1pct', E, 'comparison', 'Airbnb', 'matched frontier APIs at one percent of the cost', '''    return ctx.require('airbnb', r'matches frontier-level quality .*roughly 1% of the cost')''')
c('e03-astra-beat-humans', E, 'comparison', 'Blueprint', 'GPT-6.2 Astra beat humans at 3D spatial reasoning', '''    # Framed as a feed headline. Leaderboard: Astra 0.614 vs human 0.586 (human on 12 of 50 apartments).
    a = ctx.find('blueprint', r'GPT-6\\.2 Astra 0\\.614'); h = ctx.find('blueprint', r'Human\\* 0\\.586')
    g = ctx.find('gdb', r'exceeding human baseline')
    if a and h and g: return ctx.ok('blueprint', a + ' … ' + h, 'headline framing matches @gdb: "' + g + '"; caveat (12-apartment subset) is checked in o-e4')
    return ctx.need('blueprint', a, 'scores not found')''')
c('e04-headlines-miss', E, 'opinion', 'Intro', 'all three headlines miss the best part', '''    return ctx.need(None, None, 'opinion / framing; not checkable against sources')''')
c('e05-thesis', E, 'opinion', 'Intro', 'judging models by prose, prompts, or leaderboard headlines is breaking down', '''    s = ctx.find('society', r'Executable Review Finds What Text Can Miss')
    return ctx.need('society', s, 'opinion (episode thesis); nearest supporting source text quoted')''')
c('e06-real-signal', E, 'opinion', 'Intro', 'The real signal only shows up when you execute under real constraints', '''    s = ctx.find('society', r'need code-and-data scrutiny to test claims')
    return ctx.need('society', s, 'opinion; nearest supporting source text quoted')''')
c('e07-alphaxiv-study', E, 'attribution', 'Society', 'the alphaXiv study', '''    return ctx.require('society', r'alphaXivMITStanford', r'publisher=\\{alphaXiv\\}', note='alphaXiv-published, alphaXiv/MIT/Stanford authors')''')
c('e08-title', E, 'quote', 'Society', 'A Society of AI Scientists', '''    return ctx.require('society', r'^A Society of AI Scientists')''')
c('e09-twelve-weeks', E, 'number', 'Society', 'Over twelve weeks', '''    return ctx.require('society', r'twelve-week study')''')
c('e10-labs-agents', E, 'attribution', 'Society', 'thirty-five human labs, including Stanford, MIT, and ETH Zurich, deployed 936 autonomous agents onto a shared preprint server', '''    return ctx.require('society', r'936 autonomous agents across 35 human-operated laboratories .*shared preprint server', r'35 labs \\(across Stanford, MIT, ETH Zurich')''')
c('e11-936-papers', E, 'number', 'Society', 'published 936 papers with code and data', '''    return ctx.require('society', r'producing 936 papers alongside their code, data')''')
c('e12-9500', E, 'number', 'Society', 'exchanged 9,500 messages', '''    return ctx.require('society', r'exchanged 9,500 messages')''')
c('e13-retract-before', E, 'attribution', 'Society', 'retracted mistakes publicly before upload', '''    return ctx.support_or_contradict('society', r'publicly retract mistaken claims before publication', r'correction preceded upload', 'retraction timing')''')
c('e14-null-results', E, 'comparison', 'Society', 'published null results as often as positive ones', '''    # Claim: PUBLISHED nulls as often as positives. Source: CITED / ACKNOWLEDGED negatives as often.
    return ctx.support_or_contradict('society', r'publish\\w* (null|negative)[^.]{0,40}as often as positive',
        r'(cited|acknowledge) negative (results|findings) as often as positive',
        'source says negative results were cited/acknowledged as often as positive ones, not published as often')''')
c('e15-journal-founded', E, 'attribution', 'Society', 'founded the Journal of Agent Research', '''    s1 = ctx.find('society', r'agents founded the Journal of Agent Research'); s2 = ctx.find('society', r'agents in one laborator\\w* also founded')
    return ctx.need('society', (s1 or '') + ' … ' + (s2 or ''), 'paper says both "agents founded" and "agents in one laboratory founded"; subject "They" (all 936 agents) is ambiguous')''')
c('e16-rigor-llm-judges', E, 'comparison', 'Society', "blinded LLM judges did rate the agents' prose higher on experimental rigor than matched human preprints", '''    return ctx.require('society', r'Agent papers scored higher on experimental rigor, 9\\.02 versus 7\\.00', r'blinded LLM rubric ratings of prose', r'202 matched pairs')''')
c('e17-novelty', E, 'comparison', 'Society', 'humans won on novelty and significance', '''    return ctx.require('society', r'Human papers scored higher on novelty and significance')''')
c('e18-text-review-failed', E, 'opinion', 'Society', 'text-only peer review failed', '''    s = ctx.find('society', r'could not tell a disclosed weakness from a hidden one')
    return ctx.need('society', s, 'characterisation ("failed") is stronger than the source, which says text-only reviewers flagged 11 of 16 flawed drafts but could not tell disclosed from hidden weaknesses')''')
c('e19-11of16', E, 'number', 'Society', 'Text-only reviewers caught eleven of sixteen flawed drafts', '''    return ctx.require('society', r'Text-only reviewers flagged 11 of 16 flawed')''')
c('e20-10of16', E, 'number', 'Society', 'flagged ten of sixteen repaired versions where the limitation was already openly disclosed', '''    return ctx.require('society', r'10 of 16 repaired versions in which the limitation was already openly disclosed')''')
c('e21-answer-keys', E, 'attribution', 'Society', 'code inspections still caught scripts using answer keys and leaked targets', '''    return ctx.require('society', r'code inspections found submissions in which scripts or prompts used answer keys or leaked targets')''')
c('e22-guest-editor', E, 'attribution', 'Society', 'A guest editor turned referee objections into scripts and ran them on the uploaded data', '''    return ctx.require('society', r'guest editor then translated 276 objections .* into scripts that were run on the uploaded data')''')
c('e23-nearly-half', E, 'number', 'Society', 'overturning the headline conclusion in nearly half of major-objection cases', '''    s = ctx.find('society', r'major objections, the scripts overturned the headline conclusion in (\\d+) of (\\d+)')
    if not s: return ctx.need('society', None, 'figure not found')
    n, d = map(int, re.search(r'in (\\d+) of (\\d+)', s).groups())
    return ctx.ok('society', s, f'{n}/{d} = {n/d:.1%}; "nearly half" holds') if 0.40 <= n / d < 0.5 else ctx.fail('society', s, f'{n}/{d} = {n/d:.1%} is not "nearly half"')''')
c('e24-101', E, 'number', 'Society', '101-step citation chain', '''    return ctx.require('society', r'longest citation chain reached 101 steps')''')
c('e25-random-null', E, 'comparison', 'Society', 'statistically indistinguishable from randomly citing recent papers', '''    s = ctx.find('society', r'recency-matched random citation null averaged [\\d.]+ steps \\(P = ([\\d.]+)\\)')
    if not s: return ctx.need('society', None, 'null comparison not found')
    p = float(re.search(r'P = ([\\d.]+)', s).group(1))
    return ctx.ok('society', s, f'P = {p} > 0.05') if p > 0.05 else ctx.fail('society', s, f'P = {p} is significant')''')
c('e26-theater', E, 'opinion', 'Society', 'Without an execution path, AI science risks becoming very polite, rigorous-sounding theater', '''    s = ctx.find('society', r'Evidence Needs an Execution Path')
    return ctx.need('society', s, 'opinion; echoes the paper section title quoted')''')
c('e27-gemma-promoting', E, 'attribution', 'Airbnb', "Google's Gemma account is promoting Airbnb's new benchmark", '''    return ctx.require('gemma', r'@googlegemma: Love seeing what happens when open weights meet great engineering')''')
c('e28-e2b-rtx', E, 'qualifier', 'Airbnb', 'a fine-tuned Gemma 4 E2B model on a single NVIDIA RTX Pro 6000 GPU', '''    return ctx.require('gemma', r'Gemma 4 E2B .*single @NVIDIA RTX Pro 6000 GPU')''')
c('e29-matched-sol-sonnet', E, 'comparison', 'Airbnb', 'matched GPT-6.1 Sol and Claude Sonnet 5.5 on a real-time policy classifier', '''    # Source never gives an F1 for Sol or Sonnet; it says "on par with the best proprietary models".
    named = ctx.find('airbnb', r'(Sol|Sonnet 5\\.5)[^.]*\\b(F1|0\\.9\\d)')
    if named: return ctx.ok('airbnb', named)
    s = ctx.find('airbnb', r'on par with the best proprietary models')
    return ctx.need('airbnb', s, 'source does not show Sol or Sonnet 5.5 are the best proprietary models on F1; names come from the latency/cost passages')''')
c('e30-0902', E, 'number', 'Airbnb', 'Quality hit 0.902 max F1', '''    return ctx.require('gemma', r'0\\.563 to 0\\.902 max F1')''')
c('e31-latency-drop', E, 'number', 'Airbnb', 'median latency dropped from roughly 900 milliseconds to 35', '''    # "dropped from 900 to 35" implies one system got faster; sources compare two different models.
    return ctx.support_or_contradict('gemma', r'(drop|fell|reduc|cut)\\w*[^.]{0,40}900', r'35ms median latency \\(85ms p99\\) vs\\. ~900ms for frontier models',
        'not a drop: 35 ms is the fine-tuned Gemma, ~900 ms is the frontier models')''')
c('e32-1pct', E, 'number', 'Airbnb', 'costs fell to about one percent at high volume', '''    return ctx.require('gemma', r'~1% of frontier API spend at high volume', note='relative cost vs frontier APIs; "fell" is loose but the figure matches')''')
c('e33-0563', E, 'number', 'Airbnb', 'Out of the box, that two-billion-parameter model scored a weak 0.563', '''    return ctx.require('airbnb', r'2 billion effective parameters', r'lifts its F1 from 0\\.563')''')
c('e34-2700', E, 'number', 'Airbnb', "even a 2,700-word prompt couldn't close the gap", '''    return ctx.require('airbnb', r"2,700 word prompt couldn't|detailed prompt improves classification quality but doesn't close the gap")''')
c('e35-hundreds-thousands', E, 'number', 'Airbnb', 'fine-tuning on hundreds of thousands of labeled production examples', '''    return ctx.require('airbnb', r'hundreds of thousands of domain-specific examples')''')
c('e36-rpm', E, 'qualifier', 'Airbnb', 'only beats APIs above fifteen to thirty requests per minute', '''    return ctx.require('airbnb', r'below roughly 15 to 30 RPM, Claude Sonnet 5\\.5 and GPT-6\\.1 Sol are cheaper')''')
c('e37-true-false', E, 'qualifier', 'Airbnb', 'Frontier models return a slow, fixed true-or-false verdict', '''    s = ctx.find('airbnb', r'each model returns a verdict rather than a score, it gives a single, fixed precision-recall point')
    m = ctx.find('airbnb', r'most proprietary models return only a True or False verdict')
    if s: return ctx.ok('airbnb', s + ' … ' + (m or ''), 'said of proprietary generative models; elsewhere "most proprietary models"')
    return ctx.need('airbnb', m, 'only the "most proprietary models" wording found')''')
c('e38-logprobs', E, 'attribution', 'Airbnb', 'Extracting logprobs from a fine-tuned model gives Airbnb a continuous score they can threshold', '''    return ctx.require('airbnb', r'By extracting logprobs, we.re able to produce a score for thresholding')''')
c('e39-dial', E, 'opinion', 'Airbnb', "You can't prompt your way to an operational dial", '''    s = ctx.find('airbnb', r'Scores let you choose your tradeoff .* without rewriting the prompt')
    return ctx.need('airbnb', s, 'opinion; paraphrases the quoted source line')''')
c('e40-andon', E, 'attribution', 'Blueprint', "Andon Labs' Blueprint-Bench 2", '''    return ctx.require('blueprint', r'author=\\{Andon Labs\\}')''')
c('e41-twenty-photos', E, 'number', 'Blueprint', 'agents turn roughly twenty apartment photos into 2D floor plans', '''    return ctx.require('blueprint', r'~20 interior photos', r'2D floor plans')''')
c('e42-brockman', E, 'attribution', 'Blueprint', "OpenAI's Greg Brockman highlighted that GPT-6.2 Astra ranked first at 0.614", '''    g = ctx.find('gdb', r'GPT-6\\.2 Astra exceeding human baseline'); a = ctx.find('blueprint', r'1 GPT-6\\.2 Astra 0\\.614')
    if g and a: return ctx.ok('gdb', g + ' … leaderboard: ' + a, 'Brockman highlighted the human-baseline result; the 0.614 figure is from the leaderboard, not his post')
    return ctx.need('gdb', g, 'post or score not found')''')
c('e43-0586', E, 'comparison', 'Blueprint', 'edging past the human baseline of 0.586', '''    return ctx.require('blueprint', r'Human\\* 0\\.586')''')
c('e44-12of50', E, 'qualifier', 'Blueprint', 'human baseline was tested on just twelve apartments out of fifty', '''    return ctx.require('blueprint', r'Human baseline tested on subset of 12 apartments only', r'processes 50 apartments')''')
c('e45-carbon-tie', E, 'comparison', 'Blueprint', 'Gemini 4 Carbon tied it', '''    return ctx.require('blueprint', r'T2 Gemini 4 Carbon 0\\.586 T2 Human\\* 0\\.586')''')
c('e46-neon-absent', E, 'qualifier', 'Blueprint', "Google's newly released Gemini 4 Neon isn't even on the board yet", '''    if not ctx.absent('blueprint', r'Neon'): return ctx.fail('blueprint', ctx.find('blueprint', r'Neon'), 'Neon is on the leaderboard')
    r = ctx.find('andon', r'Google released the best model in the world, Gemini 4 Neon')
    return ctx.ok('andon', r, 'no "Neon" anywhere in the leaderboard page; "newly released" comes from a reply in the @andonlabs thread') if r else ctx.need('andon', None, 'release not sourced')''')
c('e47-robotics-zero', E, 'number', 'Blueprint', 'Gemini Robotics-ER 1.6, a model built specifically for embodied spatial reasoning, scored zero', '''    return ctx.require('blueprint', r'Gemini Robotics-ER 1\\.6 0\\.000\\*\\*', r'designed for spatial and embodied reasoning')''')
c('e48-random', E, 'comparison', 'Blueprint', 'at or below random chance', '''    return ctx.require('blueprint', r'\\*\\*Score at or below the random baseline')''')
c('e49-notepad-trend', E, 'number', 'Blueprint', 'general frontier models given a persistent notepad to carry lessons across apartments are climbing steadily at four-hundredths of a point per month', '''    # Is +0.04/month a notepad effect? Source: a trend line over SOTA models by release date.
    return ctx.support_or_contradict('blueprint', r'notepad[^.]{0,120}0\\.04|0\\.04[^.]{0,120}notepad',
        r'SOTA frontier models are labeled and a trend line is fitted .* \\+0\\.04/month',
        '+0.04/month is the trend of SOTA scores against model release date, not models improving via the notepad')''')
c('e50-twelve-humans', E, 'qualifier', 'Blueprint', 'whether a leaderboard edges past twelve humans', '''    return ctx.support_or_contradict('blueprint', r'(12|twelve) (humans|people|participants)', r'Human baseline tested on subset of 12 apartments',
        'the 12 is apartments in the human-baseline subset, not twelve humans')''')

# ======================= SHORT =======================
S = 'short'
c('s00-thesis', S, 'opinion', 'Intro', 'judging models by prose, prompts, or leaderboards is breaking down', '''    s = ctx.find('society', r'Executable Review Finds What Text Can Miss')
    return ctx.need('society', s, 'opinion (short thesis); nearest supporting source text quoted')''')
c('s01-alphaxiv-watched', S, 'attribution', 'Society', 'alphaXiv watched 936 AI agents run their own preprint server', '''    return ctx.require('society', r'Today we.re launching a preprint server built specifically for AI agents', r'nearly 1,000 agents from 35 labs .* on this server', note='alphaXiv launched the server and co-led the study (alphaXiv/MIT/Stanford)')''')
c('s02-journal-scope', S, 'attribution', 'Society', 'publish 936 papers, and launch a peer-reviewed journal', '''    s = ctx.find('society', r'agents in one laborator\\w* also founded the Journal')
    sent = ctx.art_sentence(CLAIM['quote'])
    if s and not re.search(r'one lab', sent, re.I):
        return ctx.fail('society', s, 'credits all 936 agents with launching the journal; source says agents in one laboratory founded it')
    return ctx.ok('society', s)''')
c('s03-936-papers', S, 'number', 'Society', '936 papers', '''    return ctx.require('society', r'producing 936 papers')''')
c('s04-card-journal', S, 'number', 'Society', '936 agents built a journal', '''    s = ctx.find('society', r'agents in one laborator\\w* also founded the Journal')
    return ctx.fail('society', s, 'on-screen card credits all 936 agents with the journal; source scopes it to one laboratory') if s else ctx.need('society', None, 'scope sentence not found')''')
c('s05-honest-caveat', S, 'attribution', 'Society', "text-only peer review couldn't tell an honest caveat from a hidden flaw", '''    return ctx.require('society', r'could not tell a disclosed weakness from a hidden one')''')
c('s06-overturned', S, 'qualifier', 'Society', 'Only running scripts on the uploaded data overturned nearly half of major objections', '''    # What was overturned: the objections, or the papers' headline conclusions?
    return ctx.support_or_contradict('society', r'overturned[^.]{0,30}objections', r'scripts overturned the headline conclusion in 77 of 156 cases',
        'inverted: the scripts overturned the papers\\' headline conclusions in 49.4% of major-objection cases, not the objections themselves')''')
c('s07-494', S, 'number', 'Society', '49.4%', '''    return ctx.require('society', r'77 of 156 cases \\(49\\.4%\\)')''')
c('s08-airbnb-2b', S, 'attribution', 'Airbnb', 'Airbnb fine-tuned a tiny 2-billion-parameter Gemma model', '''    return ctx.require('airbnb', r'fine-tuned classifier with 2 billion effective parameters', r'Fine-tuning Gemma4-E2B')''')
c('s09-matched-35ms-1pct', S, 'comparison', 'Airbnb', 'matched frontier APIs in 35 milliseconds at one percent of the cost', '''    return ctx.require('gemma', r'matching top frontier APIs', r'35ms median latency', r'~1% of frontier API spend')''')
c('s10-2700', S, 'comparison', 'Airbnb', "Even a 2,700-word prompt couldn't close the gap", '''    return ctx.require('airbnb', r"2,700 word prompt couldn't")''')
c('s11-examples-thresholds', S, 'number', 'Airbnb', 'Hundreds of thousands of real examples', '''    return ctx.require('airbnb', r'hundreds of thousands of in-domain examples did what', r'Scores let you choose your tradeoff')''')
c('s12-card-mega', S, 'comparison', 'Airbnb', 'Fine-tuning beat mega-prompts', '''    return ctx.require('airbnb', r"Hundreds of thousands of in-domain examples did what a 2,700 word prompt couldn't")''')
c('s13-astra-edged', S, 'comparison', 'Blueprint', 'GPT-6.2 Astra edged a human baseline tested on just twelve apartments', '''    return ctx.require('blueprint', r'1 GPT-6\\.2 Astra 0\\.614', r'Human\\* 0\\.586', r'Human baseline tested on subset of 12 apartments')''')
c('s14-robotics-zero', S, 'attribution', 'Blueprint', 'a dedicated robotics model scored zero', '''    return ctx.require('blueprint', r'Gemini Robotics-ER 1\\.6 0\\.000\\*\\*')''')
c('s15-easy-to-fake', S, 'opinion', 'Close', 'Polished prose and top-line scores are easy to fake', '''    s = ctx.find('society', r'a convincing paper could still describe a flawed experiment')
    return ctx.need('society', s, 'opinion stated as fact; sources show prose can mislead reviewers, not that scores are "easy to fake"')''')
c('s16-real-signal', S, 'opinion', 'Close', 'The real signal only appears when you execute under real constraints', '''    s = ctx.find('society', r'need code-and-data scrutiny to test claims')
    return ctx.need('society', s, 'opinion; nearest supporting source text quoted')''')
c('s17-credit', S, 'attribution', 'Close', 'Sources: alphaXiv, Airbnb and Andon Labs.', '''    return ctx.ok(None, None, 'credit names the three primary-source outlets in index.json')''')

# ======================= OBJECTIONS (dropped caveats) =======================
def obj(id, artifact, story, src_pat, art_pat, what):
    c(id, artifact, 'objection', story, None, f'''    # Objection: {what}
    s = ctx.find('framing', r{src_pat!r})
    if not s: return ctx.ok(None, None, 'no such caveat in the scan framing for this story')
    if ctx.art_has(r{art_pat!r}): return ctx.ok('framing', s, 'caveat present in artifact')
    return ctx.fail('framing', s, 'artifact never states this caveat ({what})')''')
SOC_CAV = r"not (yet )?(been )?peer[- ]reviewed|not yet reviewed|unreviewed|preliminary|exploratory|hasn'?t been (peer[- ])?reviewed|early,? author[- ]reported"
AIR_CAV = r"company[- ]reported|airbnb (says|reports|reported|claims)|according to airbnb|airbnb's own (data|benchmark|test)|its own (held-out )?data|(one|single) (production )?(task|classifier)"
for art in (E, S):
    p = art[0]
    obj(f'o{p}1-society-preliminary', art, 'Society', r'not yet peer reviewed', SOC_CAV, 'Society paper is an exploratory preprint, not yet peer reviewed or replicated')
    obj(f'o{p}2-airbnb-company-reported', art, 'Airbnb', r'Company-reported benchmark on Airbnb.s own held-out data for one production task', AIR_CAV, 'Airbnb result is company-reported, on its own data, for one task')
    obj(f'o{p}3-blueprint-subset', art, 'Blueprint', r'human baseline covers only 12 of the 50 apartments', r'(12|twelve) apartments', 'human baseline covers only 12 of 50 apartments')
    obj(f'o{p}4-blueprint-operator', art, 'Blueprint', r'Benchmark operator.s own leaderboard', r"andon labs'? blueprint|andon labs|on blueprint-bench", 'leaderboard is run by the benchmark operator (named as source)')
c('oe5-rigor-llm-judges', E, 'objection', 'Society', None, '''    # Objection: if the rigor score is cited, it must be framed as LLM ratings of prose, not human peer review.
    s = ctx.find('society', r'blinded LLM rubric ratings of prose, not expert human peer review')
    if not ctx.art_has(r'rigor'): return ctx.ok(None, None, 'rigor score not cited')
    return ctx.ok('society', s, 'framed as LLM judges') if ctx.art_has(r'LLM judges|language model judges') else ctx.fail('society', s, 'rigor score cited without LLM-judge caveat')''')
c('oe6-interested-parties', E, 'objection', 'Airbnb/Blueprint', None, '''    # Objection: promoters with a stake (Google's Gemma account, OpenAI's president) must be identified as such.
    g = ctx.art_has(r"Google's Gemma account"); b = ctx.art_has(r"OpenAI's Greg Brockman")
    s = ctx.find('framing', r'Company-reported')
    return ctx.ok(None, None, 'both promoters identified with their company') if g and b else ctx.fail(None, None, f'gemma identified={g}, brockman identified={b}')''')

for id, meta, body in C:
    (H / f'{id}.py').write_text(HDR % (meta, body))
print(len(C), 'checks written')
