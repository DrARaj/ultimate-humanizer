#!/usr/bin/env python3
"""Flag mechanical AI-writing tells defined in ultimate-humanizer/SKILL.md.

FAIL = banned outright, must be fixed. CHECK = context-dependent, judge it
against the named rule. Judgement rules (rhythm, voice, invented facts) are
not detectable here; the SKILL.md checklist covers those.

Usage: python -I lint.py FILE [FILE ...]   or   ... | python -I lint.py -
       python -I lint.py --selftest
Exit 1 when any FAIL is found.
"""
import re
import sys

FAIL_PHRASES = {
    "R1": ["stands as", "serves as", "is a testament", "a testament to", "is a reminder",
           "pivotal moment", "pivotal role", "crucial role", "vital role", "key role",
           "significant role", "underscores its", "highlights its importance",
           "highlights its significance", "reflects broader", "reflecting broader",
           "setting the stage for", "marks a shift", "marked a shift", "represents a shift",
           "key turning point", "evolving landscape", "focal point", "indelible mark",
           "deeply rooted", "part of a broader", "broader movement", "enduring legacy",
           "lasting legacy", "generated debate", "prompted broader reflection",
           "raising philosophical questions", "plays a role in the ecosystem",
           "solidify its role", "solidifies its position", "solidifying its"],
    "R2": ["independent coverage", "media outlets", "trade publications",
           "active social media presence", "digital presence", "leading expert",
           "widely-read", "prominent media", "significant coverage", "secondary coverage"],
    "R4": ["boasts", "vibrant", "nestled", "in the heart of", "groundbreaking", "renowned",
           "breathtaking", "stunning", "natural beauty", "diverse array", "commitment to",
           "must-visit", "captivates", "fascinating glimpse", "rich cultural heritage",
           "rich history", "seamlessly", "worth visiting", "exemplifies", "showcase",
           "showcases", "showcasing", "showcased"],
    "R6": ["industry reports", "observers have", "experts argue", "experts believe",
           "experts agree", "some critics argue", "many argue", "widely regarded",
           "studies show", "described in scholarship", "researchers and conservationists"],
    "R7": ["despite these challenges", "faces several challenges", "faces challenges",
           "continues to thrive", "future outlook", "future prospects",
           "the future looks bright", "exciting times lie ahead",
           "step in the right direction", "journey toward excellence"],
    "R8": ["awards and recognition"],
    "R9": ["additionally", "align with", "aligns with", "aligning with", "aligned with",
           "bolstered", "crucial", "deep dive", "delve", "delves", "delving", "emphasizing",
           "enduring", "enhance", "enhances", "enhancing", "enhanced", "foster", "fosters",
           "fostering", "garner", "garnered", "interplay", "intricate", "intricacies",
           "meticulous", "meticulously", "pivotal", "robust", "tapestry", "testament",
           "underscore", "underscores", "underscoring", "underscored", "valuable",
           "highlighting", "leverage", "leveraging", "utilize", "utilizes", "utilizing",
           "facilitate", "facilitates", "facilitating", "empower", "empowering",
           "streamline", "streamlined", "streamlining", "cutting-edge", "paradigm shift",
           "game changer", "game-changer", "this is huge", "this changes everything",
           "realm", "beacon", "multifaceted", "paramount", "transformative", "elevate",
           "elevates", "embark", "supercharge", "harness", "ever-evolving",
           "at the end of the day", "when it comes to", "in a world where",
           "moving forward", "going forward", "circle back", "double down",
           "take a step back", "on the same page", "make no mistake", "it turns out",
           "let me be clear", "lean into", "in today's world", "in the age of",
           "the reality is", "the truth is", "in this article", "straightforward"],
    "R22": ["i hope this helps", "of course!", "certainly!", "absolutely!",
            "you're absolutely right", "great question", "excellent point",
            "would you like me to", "is there anything else", "let me know if",
            "here is a", "here's a", "feel free to", "happy to help",
            "in this section, we will", "a wikipedia-style article"],
    "R23": ["not widely documented", "not widely available", "not extensively documented",
            "in the provided sources", "in the available sources", "in the search results",
            "based on available information", "maintains a low profile",
            "keeps personal details private", "should be treated as",
            "does not by itself establish", "while specific details"],
    "R41": ["this message finds you well", "i am writing to",
            "apologize for any inconvenience", "i have carefully reviewed",
            "dear wikipedia", "thank you for your understanding", "please point them out"],
    "R56": ["as of my last", "my last training", "my last knowledge"],
    "R57": ["important to note", "important to remember", "worth noting",
            "worth mentioning", "it is crucial to", "it's crucial to", "may vary"],
    "R58": ["in summary", "in conclusion", "to sum up", "in essence"],
    "R59": ["as an ai", "as a large language model", "as an ai language model"],
    "R74": ["matters more than it sounds", "the key point is", "as you can see",
            "this distinction matters"],
    "R75": ["here's the thing", "here's what i mean", "i'll be honest",
            "the uncomfortable truth", "most people skip", "most people get wrong",
            "nobody tells you", "everyone misses"],
    "R79": ["the real question is", "at its core", "what really matters",
            "the deeper issue", "the heart of the matter"],
    "R80": ["let's dive", "dive in", "let's explore", "let's break this down",
            "let's break it down", "here's what you need to know", "now let's look at",
            "without further ado"],
    "R82": ["what if i told you", "ever wondered", "think about it", "plot twist"],
    "R83": ["that's the whole thing"],
    "R88": ["and that's okay", "and that's fine", "there's nothing wrong with that",
            "no shame in", "you're not alone", "it's completely normal"],
}

CHECK_PHRASES = {
    "R5": ["in connection with", "in association with", "associated with", "connected with"],
    "R9": ["highlight", "highlights", "highlighted", "key", "landscape", "causal",
           "empirical", "correlate", "navigate", "unpack", "in terms of", "with regard to",
           "in the world of"],
    "R10": ["functions as", "operates as", "holds the distinction", "ventured into",
            "refers to", "features", "offers"],
    "R43-R47": ["while preserving", "preserved", "retained", "for clarity",
                "for neutrality", "neutral tone", "encyclopedic tone", "reviewer feedback",
                "added sourced", "improved attribution", "in compliance with", "adheres to"],
    "R58": ["overall", "ultimately"],
    "R73": ["just", "literally", "honestly", "simply", "actually", "truly",
            "fundamentally", "inherently", "inevitably", "importantly", "crucially"],
    "R74": ["in other words"],
    "R76": ["in order to", "due to the fact that", "at this point in time",
            "in the event that", "has the ability to", "made a decision"],
    "R79": ["in reality"],
}

FAIL_REGEX = [
    ("R17", r"\u2014"),
    ("R21", r"[\u201c\u201d\u2018\u2019]"),
    ("R19", r"[\U0001F300-\U0001FAFF\u2600-\u27bf\u2b50\u2b06\u2194-\u21ff]\ufe0f?"),
    ("R31", r"contentReference|oaicite|oai_citation|attributableIndex|"
            r"turn\d+(?:search|image|news|file)\d+|\[cite:\s*\d|\((?:start|end)_span\)|"
            r"grok-card|grok_render_citation_card_json|\u3010\d+\u2020|"
            r"\[(?:attached_file|web):\d+\]|ppl-ai-file-upload|:::writing\{|\u21a9|"
            r"[\ue000-\uf8ff]"),
    ("R39", r"utm_[a-z]+=|referrer=grok\.com"),
    ("R24", r"\b20\d\d-(?:XX|xx)-(?:XX|xx)\b|\b\d{4}-\d\d-(?:XX|xx)\b|INSERT_[A-Z_]+|"
            r"PASTE_[A-Z_]+_HERE|SOURCE_PUBLISHER|\[Your Name\]|"
            r"\[[A-Z][^\]\n]{0,40}(?:Name|Topic|link|URL|Describe)[^\]\n]*\]|"
            r"\(Add your [^)]*here\)|Add if available"),
    ("R16", r"(?m)^\s*(?:[-*\u2022\u2013]|\d+\.)\s*(?:\*\*|''')[^*'\n]{1,60}?(?::(?:\*\*|''')|(?:\*\*|''')\s*:)"),
    ("R11", r"(?i)\bnot (?:only|just|merely)\b[^.!?\n]{0,80}(?:\bbut\b|[,;] it'?s\b)"),
    ("R3", r"(?i)[,\u2014]\s*(?:highlighting|underscoring|emphasizing|reflecting|symbolizing|"
           r"showcasing|fostering|ensuring|contributing to|cultivating|encompassing|"
           r"enhancing|demonstrating|illustrating|solidifying|marking)\b"),
]

CHECK_REGEX = [
    ("R11", r"(?i)\b(?:it'?s|this is|that'?s|isn'?t|is not)\b[^.!?\n]{0,50}[,;:] (?:it'?s|but)\b"),
    ("R11", r"(?i)\brather than\b"),
    ("R17", r"\w ?-- ?\w"),
    ("R15/R26", r"\*\*[^*\n]+\*\*"),
    ("R29", r"(?m)^\s*(?:-{3,}|\*{3,}|_{3,})\s*$"),
    ("R77", r"(?i)\b(?:could|might|may)\s+(?:potentially|possibly)\b"),
    ("R78", r"(?i)\bfrom [^,.;\n]{2,40} to [^,.;\n]{2,40}, from\b"),
    ("R87", r"(?m)(?:^|[.!?]\s+)(?:So|Look|Interestingly|Importantly|Notably|Crucially|"
            r"Essentially|Ultimately|Additionally),"),
    ("R14", r"(?m)^(?:#{1,6}|={1,6})\s*(?:[A-Z][\w'-]*\s+){2,}[A-Z][\w'-]*\s*=*\s*$"),
]


def _compile(table):
    out = []
    for rule, phrases in table.items():
        for p in phrases:
            out.append((rule, p, re.compile(r"(?<![\w-])" + re.escape(p) + r"(?![\w-])", re.I)))
    return out


FAIL_P, CHECK_P = _compile(FAIL_PHRASES), _compile(CHECK_PHRASES)
FAIL_R = [(r, re.compile(x)) for r, x in FAIL_REGEX]
CHECK_R = [(r, re.compile(x)) for r, x in CHECK_REGEX]


def lint(text):
    """Return sorted (line, col, level, rule, match) tuples."""
    hits = set()
    starts = [0] + [m.end() for m in re.finditer("\n", text)]

    def pos(i):
        lo, hi = 0, len(starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if starts[mid] <= i:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1, i - starts[lo] + 1

    for level, items in (("FAIL", FAIL_P), ("CHECK", CHECK_P)):
        for rule, _p, rx in items:
            for m in rx.finditer(text):
                hits.add((*pos(m.start()), level, rule, m.group(0)))
    for level, items in (("FAIL", FAIL_R), ("CHECK", CHECK_R)):
        for rule, rx in items:
            for m in rx.finditer(text):
                hits.add((*pos(m.start()), level, rule, m.group(0).strip()[:60]))
    return sorted(hits)


def selftest():
    slop = ("Nestled in the heart of the valley, the town stands as a testament to resilience\u2014"
            "highlighting its vibrant culture. It's not just a town, it's a feeling. "
            "Additionally, we delve into its rich history. I hope this helps!\n"
            "- **Key Point:** Something [cite: 3] utm_source=chatgpt.com 2025-XX-XX \U0001F680\n"
            "In conclusion, the future looks bright.")
    found = {r for _l, _c, lvl, r, _m in lint(slop) if lvl == "FAIL"}
    for rule in ("R1", "R3", "R4", "R9", "R16", "R17", "R19", "R22", "R24", "R31", "R39", "R58"):
        assert rule in found, f"selftest: {rule} not detected"
    clean = ("The Statistical Institute of Catalonia was established in 1989. "
             "It publishes regional statistics and has about 90 staff.")
    bad = [h for h in lint(clean) if h[2] == "FAIL"]
    assert not bad, f"selftest: false FAIL on clean text: {bad}"
    print("selftest ok")


def main(argv):
    if argv[1:] == ["--selftest"]:
        selftest()
        return 0
    if len(argv) < 2:
        print(__doc__)
        return 2
    sys.stdout.reconfigure(encoding="utf-8")
    fails = 0
    for path in argv[1:]:
        text = sys.stdin.read() if path == "-" else open(path, encoding="utf-8").read()
        for line, col, level, rule, match in lint(text):
            fails += level == "FAIL"
            print(f"{path}:{line}:{col}  {level:5}  {rule:8} {match!r}")
    print(f"{fails} FAIL")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
