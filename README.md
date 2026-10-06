# Ultimate Humanizer

A Claude Code skill that stops AI writing tells from reaching your text. It turns every pattern in Wikipedia's "Signs of AI writing" field guide into a numbered rule, adds the extra patterns from the humanizer and no-ai-slop skills, and ships a lint script that catches the mechanical ones.

## What it does

- Writing and editing: prose, wiki text, docs, emails, comments, commit messages and edit summaries come out without the listed tells.
- Auditing: ask whether a piece reads as AI and you get findings with a rule number, the quoted line and a short fix. It does not score text or claim to know who wrote it.

The rules live in `SKILL.md`:

| Part | Rules | Covers |
|---|---|---|
| A | R1 to R8 | Content: inflated significance, coverage bragging, trailing "-ing" commentary, promotional tone, weasel attribution, formulaic endings |
| B | R9 to R13 | Language: overused vocabulary, avoided "is/has", negative parallelisms, triplets |
| C | R14 to R21 | Style: headings, bold, inline-header lists, em dashes, emoji, tables, curly quotes |
| D | R22 to R24 | Chatbot correspondence, source-availability hedges, placeholders |
| E, F | R25 to R40 | Markup and citations, including leaked ChatGPT, Gemini, Grok, DeepSeek and Perplexity artifacts |
| G, H | R41 to R47 | Discussion comments, edit summaries and commit messages |
| I, J | R48 to R62 | Voice, English variety, canned pages, older model habits |
| K, L | R63 to R66 | What human text looks like, what not to overcorrect, how to audit fairly |
| M | R67 to R90 | Voice matching, minimum edits, rhythm, rhetorical tricks, filler, hedging |

R0 sits above all of them: never invent a fact, source, person, example or opinion to replace a vague phrase.

## Install

```sh
git clone https://github.com/DrARaj/ultimate-humanizer ~/.claude/skills/ultimate-humanizer
```

Restart Claude Code. The skill shows up as `/ultimate-humanizer`.

## Use

- Type `/ultimate-humanizer` and paste a draft, or point it at a file.
- Ask "does this read as AI?" for an audit without a rewrite.
- Lint any text yourself:

```sh
python -I ~/.claude/skills/ultimate-humanizer/scripts/lint.py draft.md
python -I ~/.claude/skills/ultimate-humanizer/scripts/lint.py --selftest
```

FAIL lines are banned outright. CHECK lines depend on context and name the rule to judge them against. The script exits with 1 when any FAIL is present, so it can run in CI or a pre-commit hook. It needs Python 3 and nothing else.

## Make it always on

Claude Code decides on its own when to load a skill. In testing, a plain "write a commit message" request did not load it. To apply the rules to everything, add this line to `~/.claude/CLAUDE.md`:

```
Use the ultimate-humanizer skill for any prose, commit message or edit summary you write.
```

## How it was tested

- `quick_validate.py` from Anthropic's skill-creator: passes.
- `lint.py --selftest`: passes (12 rule families detected in a sloppy sample, no false FAIL on a clean one).
- A coverage script checked that 150 distinct patterns from the three sources each appear in `SKILL.md`. None were missing.
- skill-comply ran three commit-message scenarios (supportive, neutral, competing). It reported 0%, for two reasons: its classifier output failed to parse, and the outputs of these scenarios are plain text, which it cannot observe. The scenarios were then run directly and the messages linted. All three had zero FAIL. With the skill loaded, the competing prompt (which asked to "emphasize significance") produced a plain, factual message and asked for a real example instead of inventing one. Without the skill loaded, the same prompt invented example addresses, which led to the R0 rule against illustrative details.

## Limits

- The linter catches wording and formatting. Voice, rhythm, invented facts and citation accuracy need the checklist in `SKILL.md` and a human read.
- Style signs are evidence, not proof. Plenty of people write with bold text or curly quotes.

## Credits

Built on the Wikipedia guide "Signs of AI writing" by WikiProject AI Cleanup (CC BY-SA 4.0), [humanizer](https://github.com/blader/humanizer) by Siqi Chen and its [Hermes Agent port](https://github.com/nousresearch/hermes-agent), and [no-ai-slop](https://github.com/petergyang/no-ai-slop) by Peter Yang. See `NOTICE` for details.

## License

MIT, see `LICENSE`. Third-party material keeps its original license, listed in `NOTICE`.
