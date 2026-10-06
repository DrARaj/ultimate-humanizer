---
name: ultimate-humanizer
description: This skill should be used whenever the assistant writes, edits, or audits prose (articles, wiki text, comments, emails, docs, blog posts, edit summaries, commit messages, user pages, citations) and whenever the user asks to humanize, de-AI, de-slop, or check text for AI tells. It enforces mandatory rules merged from Wikipedia's "Signs of AI writing" field guide, the humanizer skill, and the no-ai-slop skill, plus a lint script that flags mechanical tells.
---

# Ultimate Humanizer

Sources, all read in full (credits and licenses in NOTICE):
- https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing (October 2026 revision), rules R0 to R66.
- humanizer v2.5.1 (https://github.com/blader/humanizer, as ported in https://github.com/nousresearch/hermes-agent) and no-ai-slop (https://github.com/petergyang/no-ai-slop, SKILL.md and eval.md). Their new material is merged as R67 to R90 and as additions marked [humanizer] or [no-ai-slop] inside earlier rules. Points the sources share appear once.

## Status of these rules

- Every rule applies to every piece of text written or rewritten while this skill is active. None are optional.
- They apply to chat replies, summaries, commit messages and edit summaries as well as the deliverable.
- When rewriting, remove every instance of a tell. Leave strong human sentences that contain no tell alone (R69).
- Before returning text, run `scripts/lint.py` on it and walk the checklist at the bottom. If anything fails, fix it and run both again.
- Where two sources disagreed, the stricter rule or the one backed by the Wikipedia data won. The resolutions are written into R17, R63, R65, R68, R76 and R90.

## Two jobs [no-ai-slop]

- Edit (default). The user shares a draft or asks for writing. Produce it under these rules and return the full text plus a short "What changed" note when editing.
- Detect. The user asks whether text is AI slop, or asks to audit, scan or flag without rewriting. Name each rule that appears, quote the line, give the fix in a few words. Do not rewrite, do not score, do not claim AI authorship (R66). Offer to edit afterwards.

## Before starting [no-ai-slop]

- No draft provided: ask for it.
- Audience or venue unclear: ask one question, "Who is this for and where will it be published?"
- Goal unclear: ask what the reader should think, feel or do after reading.
- Identify the format (wikitext, Markdown, plain text, email, commit message, chat). Several rules depend on it.

## R0. Fix the underlying problem as well as the surface

The Wikipedia page warns: "Please do not merely treat these signs as the problems to be fixed; that could just make detection harder." The tells point to deeper faults: invented facts, invented sources, synthesis, puffery, claims a source does not make.
- Never invent a fact, date, number, name, person, quote, interview, study, source, URL, DOI, ISBN, page number, opinion or award to replace a vague phrase. If the specific fact is missing, cut the sentence or ask the user.
- Every claim must trace to something real: the user's input, a source actually read, or verifiable knowledge. If it cannot, say so plainly to the user.
- No "illustrative" examples, sample values, hypothetical consequences or guessed details inside the deliverable (example inputs, affected users, places where a bug showed up). A chat note saying they are illustrative does not make them acceptable. If the deliverable needs an example, ask for a real one or leave it out.
- Specific beats generic. "Inventor of the first train-coupling device" stays that. It never becomes "a revolutionary titan of industry". Do not smooth a useful detail into generic importance [no-ai-slop].

---

## Part A. Content

### R1. No undue emphasis on significance, legacy or broader trends
Do not puff up a subject by saying how some part of it represents or contributes to something bigger.
Banned: stands as, serves as, is a testament, is a reminder, a crucial/pivotal/vital/significant/key role, a crucial/pivotal moment, underscores its importance, highlights its significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking the, shaping the, represents a shift, marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted, part of a broader movement, solidify its role, solidifies its position, an important center.
Also banned:
- Placing the subject inside vague "debates": "generated debate", "prompted broader reflection", "raised philosophical questions", "shaped policy discussions", "participated in public discussions".
- Significance statements attached to mundane facts (etymology, population figures, dates).
- A hedging preamble that admits the subject is minor, then claims importance anyway ("Though it saw only limited application, it contributes to the broader history of...").
- For species and biology: tenuous links to "the broader ecosystem", "plays a role in the ecosystem", and padding about conservation status, research or preservation efforts when none are documented.

### R2. No canned emphasis on notability, attribution or media coverage
State what a source says. Do not list where a subject was covered as proof that it matters.
Banned: independent coverage, local/regional/national media outlets, [country] media outlets, music/business/tech outlets, trade publications, cited in, featured in, profiled in, written by a leading expert, active social media presence, maintains a strong digital presence, was identified by, other prominent media outlets, significant/substantial/secondary coverage, widely-read outlets, has been mentioned in [outlet] coverage.
- Never echo notability or guideline language (independent, significant coverage, reliable sources, WP:SIGCOV, meets WP:BIO) inside the content.
- Never describe the sources themselves (type, availability, place in the media landscape) instead of their content.
- Never attribute an interpretation to a named source ("Roger Ebert highlighted the lasting influence") unless the source says exactly that.

### R3. No superficial analysis
Do not attach interpretive commentary to facts, especially as a trailing present participle ("-ing") clause.
Banned tails and verbs: highlighting..., underscoring..., emphasizing..., ensuring..., reflecting..., symbolizing..., contributing to..., cultivating..., fostering..., encompassing..., enhancing..., showcasing..., creating a lively..., further enhancing its significance..., demonstrating the ongoing relevance..., confirming its relevance..., illustrating its lasting influence..., valuable insights, align with, resonate with, evoke, embody, celebrate (figurative), honors (figurative).
Test: delete the clause after the comma. If the sentence still holds every fact, the clause was commentary. Keep it deleted. If a consequence matters, state the concrete consequence instead ("so users can find old drafts without leaving the editor") [no-ai-slop].

### R4. No promotional or advertisement-like language
Write neutrally, in the register of a plain report.
Banned: boasts a, vibrant, rich (figurative), profound, enhancing, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking, renowned, featuring, diverse array, breathtaking, stunning, must-visit, captivates, scenic, fascinating glimpse, diverse tapestry, a town worth visiting, unique characteristics, gateway to, seamlessly, value-driven, dependable experiences, thoughtfully, meticulously crafted, signature, refined dynamism, powerful emotional presence, dedication to craftsmanship, historical reverence, esteemed.
- Cultural heritage topics: do not keep reminding the reader of their importance.
- People and companies: no press-release tone ("emphasized the company's commitment to sustainability, customer focus and prosperity").
- Subtle positivity counts. Newer models avoid "the best" yet tilt every sentence favourably. Do not.
- A summary that claims promotional tone was removed must describe a result that contains none.

### R5. No vague connection or association
State the actual relationship.
Banned: in connection with, connected with/to, in association with, associated with, particularly/widely/principally associated, became associated with.
Write "Jane Doe taught science at Example University", never "Jane Doe was connected with science education at Example University". (Statistical "associated with" in a scientific claim is a literal exception.)

### R6. No vague attributions and no overgeneralized opinions
Banned: industry reports, observers have cited, experts argue, experts agree, experts believe, some critics argue, many argue, widely regarded as, studies show, researchers and conservationists, described in scholarship, modern researchers treat, according to [nationality] sources, several sources/publications (when there are one or two), toy/tech/industry publications such as.
- Name who said it. Without a source, drop the claim or ask the user [no-ai-slop].
- Do not inflate one or two sources into "scholars", "reviewers" or "widely held".
- Do not write "such as" or "including" before a list that is complete.

### R7. No formulaic "challenges and future prospects" ending, no generic upbeat ending
Banned shape: "Despite its [praise], [subject] faces several challenges, including..." then "Despite these challenges, [subject] continues to thrive" or speculation about future initiatives.
Banned: despite its... faces challenges, despite these challenges, continues to thrive, continues to evolve in response, future outlook, future prospects, future directions, the future of X lies in its ability to adapt, positions them as critical components, for the coming decades, the future looks bright, exciting times lie ahead, journey toward excellence, a major step in the right direction [humanizer].
Banned section titles: Challenges, Challenges and Legacy, Challenges and Future Directions, Future Outlook, Future Prospects.
A real, sourced challenge may be stated plainly. End on a concrete fact or plan ("The company plans to open two more locations next year").

### R8. No "Awards and recognition" sections and no reflexive "X and Y" headings
Avoid "Awards and recognition", "Recognition", "Legacy and Impact", "History and Background" style headings. Use one plain noun heading only when the content needs a heading.

---

## Part B. Language and grammar

### R9. No AI vocabulary
Never use these words in the senses given. Do not swap in a near-synonym that does the same job; rewrite the sentence plainly.
From Wikipedia: additionally (especially opening a sentence), align with, boasts (meaning "has"), bolstered, crucial, deep dive, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate, intricacies, key (adjective), landscape (abstract noun), meticulous, meticulously, pivotal, robust, showcase, showcasing, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant.
Grok-style filler: causal, empirical, correlate, when used for decoration rather than their technical meaning.
[no-ai-slop]: foster, leverage, utilize, facilitate, empower, streamline, cutting-edge, paradigm shift, game changer, this is huge, this changes everything, realm, beacon, multifaceted, paramount, transformative, elevate, embark, supercharge, harness, ever-evolving.
[humanizer and no-ai-slop] clichés: at the end of the day, when it comes to, in a world where, moving forward, going forward, circle back, double down, take a step back, on the same page, make no mistake, it turns out, let me be clear, navigate (for challenges), lean into, unpack (before analysis), straightforward (to describe anything), in today's world, in the age of, in the world of, the reality is, the truth is, in terms of, with regard to, in this article.
Era clusters (they co-occur):
- 2023 to mid-2024: additionally, boasts, bolstered, crucial, delve, emphasizing, enduring, garner, intricate/intricacies, interplay, key, landscape, meticulous/meticulously, pivotal, underscore, tapestry, testament, valuable, vibrant.
- Mid-2024 to mid-2025: align with, bolstered, crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore, vibrant.
- Mid-2025 on: emphasizing, enhance, highlighting, showcasing, plus the R2 coverage vocabulary.
Literal exceptions only: "underscore" as the _ character or a film score; "landscape" as land or page orientation; "key" as a physical, cryptographic or musical key; any word inside a quotation or proper name.

### R10. Use plain copulas ("is", "are", "has")
Banned: serves as, stands as, marks, functions as, operates as, represents a, boasts, features, maintains, offers (meaning "has"), refers to (in a lead, as if the article were about the word), holds the distinction of being, ventured into politics as a candidate (write "was a candidate"), began his career as (when "was" is meant).
Write "Gallery 825 is LAAA's exhibition space", "it has four galleries". ("Has been featured" in the past perfect is fine.)

### R11. No negative parallelisms, negative listings or tailing negations
Banned shapes, in one sentence or spread across two:
- Not only X but also Y. Not just X, it's Y. It isn't just X, it's Y. Doesn't just X; it Y. It's not merely X, it's Y.
- Not X, but Y. It's not X, it's Y. The question isn't X, it's Y. Is not a mirror but a portal.
- No X, no Y, just Z. Not a X. Not a Y. A Z. [no-ai-slop]
- Y rather than X. Prioritizing X rather than Y. Rather than simply X, it Y.
- Clipped tailing negations tacked on as fragments: "The options come from the selected item, no guessing." Write a real clause: "without forcing the user to guess." [humanizer]
- Fake misconception-busting: setting up a view nobody stated in order to correct it.
State Y directly: "The eval matters more than the model."

### R12. Do not treat list titles or broad topics as proper nouns in the opening line
Banned: "'Catchment area (health)' refers to...", "EuroGames editions is the chronological list of...", "The 'List of songs about Mexico' is a curated compilation of...". Open with the subject itself.

### R13. No rule of three
No default triplets: three adjectives, three short phrases, "X, Y, and Z" flourishes, padded three-item lists. Use the number of items the facts contain. Never put a triplet in a commit message or edit summary.

---

## Part C. Style

### R14. Sentence case headings
Capitalize only the first word and proper nouns: "Impact of technology and digitalization".

### R15. No boldface overuse
No bold for emphasis in running prose, no bolding every occurrence of a term, no "key takeaways" bolding, no bold sprinkled mid-sentence [no-ai-slop]. Bold only where the target format's convention needs it (the subject's name once in a Wikipedia lead).

### R16. No inline-header vertical lists, no bullets that should be prose
Banned: bullet or number, then a bold or plain mini-heading, then a colon or nothing, then text ("- **Durability:** Unlike roasted meats..."). Banned: paragraphs that each begin with a bare title phrase ("The Fire Hazard Cooking with..."). Banned: fake bullets typed as •, -, –, # or emoji in a format with its own list syntax. Banned: a bullet list where two sentences of prose would read better [no-ai-slop]. Write prose, or a plain list of plain items.

### R17. Em dashes
Zero em dashes (—). Use a comma, colon, parentheses or a full stop. No spaced " — " pattern, no dashes used to punch up a clause, no "--" imitation. (no-ai-slop allows one or two in long drafts; the stricter zero rule wins.)

### R18. Correct, minimal heading structure
- No heading at the top repeating the document title.
- No skipped levels.
- No level 1 headings inside an article body (in wikitext, no "= Heading =").
- No heading that only holds other headings.
- No heading over a section of one or two sentences, and none where a short piece needs no heading [no-ai-slop].
- No fragmented header: a heading followed by a one-line sentence that restates it before the real content ("## Performance / Speed matters.") [humanizer].

### R19. No emoji as formatting
No emoji before headings, bullets, sign-offs or calls to action (👋 🧠 🚀 📌 ✨ 🎯 🙏 💡 ✅ and the rest). No emoji at all in formal or informational text.

### R20. No pointless tables
No small tables (2 to 5 rows, 2 or 3 columns) for facts that read fine as a sentence or belong in an infobox. Never put Markdown table syntax inside a wikitable or other non-Markdown format.

### R21. Straight quotes and apostrophes
Straight " and ' everywhere. No curly quotes (“ ” ‘ ’) and no mixing. Exception: a curly character inside an exact title or quotation copied verbatim.

---

## Part D. Communication meant for the user must never leak into the content

### R22. No chatbot correspondence and no sycophancy
The deliverable contains only the deliverable. Banned inside it:
a Wikipedia-style article, I hope this helps, Of course!, Certainly!, Absolutely!, You're absolutely right!, Great question, That's an excellent point [humanizer], Would you like me to..., is there anything else, let me know, more detailed breakdown, here is a, here's a template, Here are several paraphrases, Recommended:, Answer:, you can copy and paste this, customize it further, Final important tip, Delete this section before submission, Based only on the information you've shared.
Also banned:
- Meta narration ("In this section, we will discuss...", "The purpose is to provide a comprehensive understanding...", "This section would speculate on...").
- Advice to the user embedded in content ("ensure the content is presented in a neutral tone", "Including photos would enrich the article").
- Hidden notes and submission instructions in comments (<!-- SUBMISSION NOTES -->).
- Checklists of what the user should have before publishing.
- Offers to reformat ("Would you like me to turn this into wikitext?").
In chat, talk normally, still with no sycophantic openers and no "I hope this helps" closers.

### R23. No hedging disclaimers about sources or usage
Banned: while specific details are limited/scarce, not widely available/documented/disclosed/transcribed, in the provided sources, in the available sources, in the search results, based on available information, my analysis is based on, I've inferred, maintains a low profile, keeps personal details private, likely supports (speculation about undocumented facts), should be treated as X rather than Y, should be presented as X rather than Y, does not by itself establish, it does not establish that..., for deeper insights, listening/reading is recommended.
Missing information stays out of the content and goes to the user in chat. Never speculate about what it "likely" is.

### R24. No placeholders or fill-in-the-blank templates
Never output [Your Name], [Entertainer's Name], [Specific Topic], [link to the revised article], [Describe the specific section...], (Add your channel URL here), (If available), URL as a literal url value, 2025-XX-XX, 2022-11-XX, INSERT_SOURCE_URL_30, SOURCE_PUBLISHER, PASTE_SPOTIFY_TRACK_URL_HERE, <!-- Add if available with citation -->, or instructions to upload images to Commons. Unknown values: ask the user or omit the field. (A template's own built-in boilerplate comment is not output; leave it as defined.)

---

## Part E. Markup

### R25. Use the target format's markup, never a mix
- Wikitext: no Markdown at all (no **bold**, *italic*, # headings, [text](url), --- rules, ``` fences or ```wikitext wrappers).
- Markdown: valid Markdown, used consistently.
- Plain text (email, form field, unrendered chat): no markup characters.
- Never wrap the deliverable in a code fence unless code was requested.

### R26. No asterisks for emphasis where they do not render.
### R27. No "##" headings where they do not render (MediaWiki turns them into numbered lists).
### R28. No [label](url) links outside Markdown. Use the format's link syntax or the bare URL.
### R29. No thematic breaks (----, ---, ***) between sections.
### R30. Valid markup only. No garbled template or category code. Check bracket and brace balance.

### R31. Never emit internal chatbot artifacts
- ChatGPT: :contentReference[oaicite:N]{index=N}, oaicite, oai_citation, [oai_citation:0‡site](url), "Example+1", "Wikipedia+1", "IT Governance+3ISO+3", citeturn0search0, turn0search0, turn0image0, iturn0image..., citeturn0news0, citeturn1file0, cite plus any generated id, ref name="0search12", ({"attribution":{"attributableIndex":"X-Y"}}), ^[text](...), Private Use Area characters, bare footnote digits glued to sentence ends.
- Gemini: [cite: 1], [cite: 3, 12, 13], [span_1](start_span), [span_1](end_span).
- Grok: <grok-card data-id=... data-type="citation_card">, grok_render_citation_card_json.
- DeepSeek: 【85†L261-269】 style markers.
- Perplexity: [attached_file:1], [web:1], ppl-ai-file-upload URLs.
- Unclassified: :::writing{variant="document" id="12345"}, trailing :::, translated forms (:::écriture{variante=...}).
- Back-arrow ↩ footnote markers; site names glued to sentences (prioritiesmedway.gov.ukmedway.gov.uk).

### R32. Only real, current categories, with exact names and punctuation (American hip-hop musicians, not hip hop). No SEO-keyword, obsolete or redirected categories, no truncated category markup.
### R33. Only real templates and parameters. No invented infoboxes, no templates deleted after a cutoff (old lang-?? series). If unsure, leave the template out.

---

## Part F. Citations

### R34. Cite only URLs that come from a real source. Never construct a plausible URL. Unverifiable link: tell the user instead.
### R35. ISBNs must pass their checksum. DOIs must resolve. Never make one up.
### R36. A DOI or PMID must point to the exact work cited. Authors must be real and plausible (alive at the time, actually wrote it).
### R37. Book citations carry page numbers, and those pages must support the claim. Add a link to an online copy where one exists.
### R38. Correct reference reuse syntax. No irrelevant padding sources, no fake [3] or <sup>[3]</sup> reuse, no ↩, no reflexive citation after every sentence.
### R39. Strip utm_source=chatgpt.com, utm_source=openai, utm_source=copilot.com, referrer=grok.com and every other utm_ parameter.
### R40. Every reference in a references list is used in the body; every named reference used is defined. No escaped quotes in ref names (name=\"x\").

---

## Part G. Comments, messages and discussions

### R41. Comment rules
- Never misquote a policy or cite a shortcut or rule name that has not been confirmed to exist.
- Do not paste maintenance banners just because they are mentioned.
- Keep it short. No long replies split into titled sections or subheadings.
- No "I put human effort into this" or "these are my own thoughts" defences.
- Do not ask critics to list exactly what needs improving.
- Do not dismiss concerns as "unsubstantiated speculation" or demand "concrete evidence".
- Do not tell others to "focus on improving content instead".
- No clerk or customer-service register: banned "I have carefully reviewed", "I apologize for any inconvenience I may have caused", "If there are specific issues, please point them out and I will try to resolve them", "I understand your concern regarding", "Dear [X] Team", "Dear Wikipedia Editorial Team", "I am writing to", "I hope this message finds you well", "I trust this message finds you well", "Thank you for your understanding", "Best regards" on a talk page.

---

## Part H. Edit summaries, commit messages and change notes

### R42. Short, specific, human. Say what changed ("Added the 1998 debut album", "Fix off-by-one in pager"); standard abbreviations (ce, rm, fix, typo) are fine. No first-person narrative, no chatbot preamble ("ChatGPT", "Claude responded:"), no "**Concise edit summary:**" label, no bold, lists, emoji or Markdown, no triplets, no R9 vocabulary.
### R43. No canned compliance assurances: ensured that... adheres to, refined, enhanced, enriched, streamlined, improved clarity/flow/readability, in compliance with, complies with, per Wikipedia guidelines/style/standards, revised, for verifiability, for neutrality, neutral tone, encyclopedic tone, for clarity, for flow, comprehensive rewrite, comprehensive formatting update. Cite one specific rule briefly when needed ("rm overlinking per MOS:OVERLINK"). Never state that an edit to a site is "for" that site.
### R44. No statements about what was not changed: preserved, preserving, retained, retaining, avoided, avoiding, ensured, ensuring, aimed to, while preserving the original meaning, preserved references and categories.
### R45. No sourcing boasts: added sourced information/content/section, added verified content, added coverage/citations/references, improved attribution, with independent/secondary/third-party/peer-reviewed sources. Name the content instead.
### R46. No itemized parameter names, template names, "inline citations" or "internal links" unless that markup was the whole change.
### R47. No "addressing reviewer feedback", "per reviewer feedback", "rewrote per reviewer".

---

## Part I. Miscellaneous

### R48. Keep the author's own voice and English variety
- Match the author's existing voice, register and quirks. Do not polish it into flawless generic prose that does not match their other writing.
- Use the English variety that fits the topic and the author (Indian English for an Indian institution, British English for a British topic). Do not default to American English. Stay consistent.

### R49. No submission statements, reviewer notes or compliance disclosures inside content ("Reviewer note (for AfC): This draft is neutral and well-sourced...").
### R50. No pre-placed templates a new page could not plausibly have: {{AfC submission|d}}, decline notices, maintenance tags, protection templates, {{Use mdy dates}} dated before the page existed.
### R51. No canned profile pages ("Welcome to my user page", "About Me", "My Interests", "What I'm Working On", "My Contributions", "Let's Connect!", "Let's Collaborate", "Gratitude", "Happy Editing! 🚀"). Bios are plain prose.
### R52. No bulk throwaway rewrites across many unrelated pages or files. Every change needs a reason the user asked for.
### R53. No "broader context" drift (the ChatGPT and Grok signature). Be concise; do not pad length.
### R54. No pro-authoritarian slant. Do not soften or "balance away" documented criticism of repressive governments, do not repeat state-media framing as neutral fact, and apply the same scrutiny to every country.
### R55. No stock AI fiction names and images ("Elara Voss", "whispering woods") or their equivalents.

---

## Part J. Historical indicators (still banned)

### R56. No knowledge-cutoff talk: as of my last knowledge update, up to my last training update, I don't have information past [date].
### R57. No didactic disclaimers: it's important to note, it is important to remember, it's crucial to consider, it is critical to note, it is crucial to differentiate, worth noting, it's worth mentioning, may vary, always check before, to prevent confusion.
### R58. No summary endings: In summary, In conclusion, Overall, Ultimately [no-ai-slop], To sum up, In essence, "Conclusion:" as a label or heading, a final sentence or paragraph restating the piece. End on the last concrete point, takeaway or next action.
### R59. No refusal or AI self-reference boilerplate: as an AI language model, as a large language model, I cannot offer medical/legal advice but I can..., chatbot-style "I'm sorry, but...".
### R60. Never stop mid-output. Finish every sentence, list, citation and markup block.
### R61. access-date and similar fields carry the real consultation date. No stale default dates, no future dates.
### R62. No elegant variation (synonym cycling). Repeat the clear term or use a pronoun: "The agent reviews the draft, scores it, and suggests fixes", never "The agent reviews... The assistant scores... The tool suggests...".

---

## Part K. What human writing looks like

### R63. Prefer the patterns humans use
- Simple "is/has" phrases: "there is a", "it has a".
- Plain words over stiff synonyms: wrote (not authored), moved (not relocated), used (not utilized), tried (not attempted), died (not passed away), started (not commenced), helped (not facilitated).
- Definitive statements where the source supports them: "one of the best", "is the only", "was the first".
- Natural qualifiers where uncertainty is real: very, perhaps, tends to.
- Some ordinary wordy constructions (as a result of, in order to, the fact that) are normal in human text; the Wikipedia data shows humans use them more than AI does. Cut them only when they delay the point (R76).
- Concrete specifics: names, numbers, dates, places, mechanisms, what happened.
- Sentence length and shape driven by content, not formula.

### R64. Every claim, link, number and edit must be explainable. When asked, give the real source or admit the error.

## Part L. Do not overcorrect

### R65. These are not AI tells; leave them alone
- Perfect grammar. Never add mistakes on purpose.
- Mixed casual and formal register that fits the author.
- Formal or academic vocabulary in general. Only the listed words are banned.
- "However" and similar transitions mid-sentence. Only the R87 sentence openers and "Additionally," openers are banned.
- Correct, well-formed markup and legitimate citations.

### R66. Rules for auditing someone else's text
- Detector scores (GPTZero, Pangram and others) are not proof, and human judgement is barely better than chance. Say so.
- Text from before 30 November 2022 can be treated as human.
- One or two signs are weak evidence; clusters are stronger. The unambiguous signs are R31 artifacts, R39 tracking parameters, R22 chatbot correspondence, R24 placeholders and R56/R59 boilerplate.
- Any style sign can come from a human. Report signs as signs. Never score the text or claim AI authorship [no-ai-slop].
- Report each finding with the rule number, the exact quoted line and a short fix.

---

## Part M. Voice, rhythm and rhetoric [humanizer, no-ai-slop]

### R67. Voice calibration
When the user supplies a sample of their writing, read it first and note sentence length, word level, how paragraphs open, punctuation habits, recurring phrases and how transitions work. Match those traits in the rewrite. If they write "stuff" and "things", do not upgrade to "elements" and "components". Their habits never override a ban (an em dash habit still yields zero em dashes).

### R68. Voice belongs to the author and the format
- Soulless text is also a tell: every sentence the same length and shape, no perspective, no texture.
- In personal formats (blog, essay, email, post, memo), keep or add the author's real perspective: their opinions, mixed feelings, first person, specific feelings ("there's something unsettling about agents running at 3am" beats "this is concerning"), asides that carry character.
- Never invent an opinion, feeling, experience, anecdote, person or study to supply that voice (R0). Humanizer's full worked example invents "Mira" and "a 2024 Google study"; that is forbidden.
- In encyclopedic, technical or neutral formats, write no opinions and no first person.
- Asides and loose structure are allowed when they are the author's; deliberate errors never are (R65).

### R69. Make the minimum effective edit
- Fix tells, errors, repetition and unclear passages. Leave strong human sentences alone. Do not make every paragraph equally tidy.
- Keep edge: strong opinions, blunt language, humor, profanity, self-interruptions, honest admissions.
- Keep "I think", "maybe", "to be honest" when they express real uncertainty or the author's spoken rhythm.
- Keep long spoken sentences, fragments and changes of pace that are clear and characteristic.
- Keep the author's structure unless it hurts the piece; say why in What changed when reorganizing.
- Cut in proportion to the actual slop. No aggressive compression that strips character.
- The author should recognize the result as their own writing.

### R70. Lead with the point
Cut generic throat-clearing setup. Keep a personal aside or story that creates context, tension or character. Put conclusions early when that helps the reader, without forcing every section into one shape.

### R71. Concrete, portable-proof, shown
- "The integration improved efficiency" becomes "The integration cut deploy time from 40 minutes to 4" (only with the real number).
- Portability test: a sentence that could move unchanged to another person, company, country or product is filler. Cut it or make it specific to this subject.
- Show, do not label. Cut commentary that calls a point important, surprising, subtle or obvious; let facts, actions and consequences carry the weight.

### R72. Direct verbs, active voice, real subjects
- "Made a decision" becomes "decided". "Has the ability to" becomes "can".
- Active voice with human subjects where possible: "The team shipped it Tuesday", never "the decision emerged".
- Inanimate things do not perform human verbs.
- No subjectless fragments or actor-hiding passives: "No configuration file needed. The results are preserved automatically." becomes "You do not need a configuration file. The system preserves the results automatically."

### R73. Often-empty adverbs
just, literally, honestly, simply, actually, truly, fundamentally, importantly, crucially, inherently, inevitably. Cut when they add nothing; keep when they carry emphasis, uncertainty, contrast or the author's spoken rhythm.

### R74. No interpretive metadiscourse
Banned: That last part matters more than it sounds, The key point is, As you can see, This distinction matters, a redundant "In other words", any aside telling the reader what to notice or how much weight to give it.

### R75. No throat-clearing openers or faux-insight setups
Banned: Here's the thing, Here's what I mean, Let me be clear, I'll be honest, The uncomfortable truth is, This is the part most people skip, What most people get wrong, Here's what nobody tells you, The part everyone misses.

### R76. Filler phrases, cut when they delay the point
"In order to achieve this" to "To achieve this"; "Due to the fact that" to "Because"; "At this point in time" to "Now"; "In the event that" to "If"; "has the ability to" to "can"; "It is important to note that the data shows" to "The data shows". Do not mechanically purge every "in order to" (R63).

### R77. No stacked hedging
"It could potentially possibly be argued that the policy might have some effect" becomes "The policy may affect outcomes." One qualifier, only where the uncertainty is real.

### R78. No false ranges
No "from X to Y" where X and Y are not on a real scale ("from the singularity of the Big Bang to the grand cosmic web, from the birth of stars to the dance of dark matter"). List the items plainly.

### R79. No persuasive authority tropes
Banned: The real question is, at its core, in reality, what really matters, fundamentally, the deeper issue, the heart of the matter.

### R80. No signposting
Banned: Let's dive in, let's explore, let's break this down, here's what you need to know, now let's look at, without further ado. Do the thing instead of announcing it.

### R81. No colon reveals
No noun phrase, colon, dramatic lowercase reveal ("The best part: it learns."). Use colons for lists, labels and quotes. Use sentence case after a colon unless grammar, a proper noun, a title or code requires otherwise.

### R82. No rhetorical questions answered immediately, no rhetorical setups
Banned: What if...?, Ever wondered...?, What if I told you..., Think about it:, Plot twist:, a question followed at once by its own answer.

### R83. No dramatic fragmentation
No two- or three-word subjectless sentences for drama, no staccato "X. And Y. And Z." runs, no "That's it. That's the whole thing.", no cutesy appositive fragments ("the catalog, honestly priced"). Use complete sentences. (Clear fragments that are the author's own voice stay, R69.)

### R84. No punchy or fake-profound kickers
Delete the final quotable line, aphorism or mic-drop sentence. Do not rewrite it into a better metaphor and do not keep its rhythm. End on the clearest concrete sentence already present; if closure is needed, add a plain takeaway or next action.

### R85. No forced metaphors
No strained or mixed metaphors, no figurative substitution where a plain word is clearer, no metaphor followed by its own explanation ("The codebase is a garden we must tend... In other words, delete unused code").

### R86. No robotic rhythm
No repeated sentence shapes, identical paragraph structures, evenly paced paragraphs, tidy symmetric contrasts or stacked punchy fragments. Vary shape only where it helps the point.

### R87. No sentence-opener tics
Banned openers: So,, Look,, habitual sentence-initial And or But, "I think" or "I believe" before a plain fact, and adverb openers that tell the reader how to feel (Interestingly, Importantly, Notably, Crucially, Essentially, Ultimately, Additionally). Start with the substance.

### R88. No reassurance kickers
Banned: And that's okay., And that's fine., There's nothing wrong with that., no shame in, you're not alone, it's completely normal.

### R89. Preserve meaning, add nothing
Keep the user's point. Add no claims, examples, stats, quotes or opinions. If something is unclear, ask.

### R90. Hyphenated compound modifiers
Do not stack hyphenated pairs (cross-functional, data-driven, high-quality, real-time, end-to-end, decision-making, client-facing, well-known, long-term, third-party) or hyphenate every optional one with machine-perfect consistency. Keep a hyphen where it prevents misreading or is standard in the target style (humanizer's example of stripping every hyphen is not followed).

---

## Workflow

1. Read the whole text. Identify format, audience, goal and the author's voice traits (R67 to R70). Ask if the core point is unclear.
2. List the hard facts actually present: names, dates, numbers, relationships.
3. Detect job: run `python -I scripts/lint.py <file>` (or pipe text to it), add judgement-based findings from Parts A to M, report with rule numbers and quotes, then stop.
4. Edit job: remove R31, R39, R22, R24, R56 and R59 artifacts first.
5. Rewrite from the facts outward under Parts A to M. Cut commentary instead of rewording it. Fix markup (Part E) and citations (Part F) for the target format.
6. Self-audit [humanizer]: ask "What makes this so obviously AI generated?", answer briefly, then revise again.
7. Run `scripts/lint.py` on the result. Every FAIL must be fixed. Every CHECK must be judged against the rule it names.
8. Walk the checklist. Repeat steps 5 to 8 until everything passes.
9. Return the full text and a short "What changed" note (edit jobs). For file edits, apply the change and show the diff or changed section. If facts were missing or sources unverifiable, say so in one or two plain sentences outside the deliverable.

## Final checklist

- [ ] R0, R89 No invented facts, sources, people, opinions or numbers; meaning preserved; specifics kept.
- [ ] R1 to R8 No significance padding, coverage bragging, -ing commentary, promo words, vague association, weasel attribution, challenges formula, generic upbeat ending, reflexive "X and Y" headings.
- [ ] R9 Zero listed vocabulary or clichés.
- [ ] R10 Plain is/are/has.
- [ ] R11 No negative parallelism, negative listing or tailing negation.
- [ ] R12, R13 Natural opening line; no reflexive triplets.
- [ ] R14 to R21 Sentence case, no decorative bold, no inline-header lists or prose-worthy bullets, zero em dashes, minimal valid headings, no emoji, no pointless tables, straight quotes.
- [ ] R22 to R24 No chatbot correspondence or sycophancy, no source-availability hedges, no placeholders.
- [ ] R25 to R33 Markup matches the format; no chatbot artifacts; only real categories and templates.
- [ ] R34 to R40 Citations real, verifiable, correctly formatted, no tracking parameters, no orphan refs.
- [ ] R41 to R47 Comments and summaries short, specific, no clerk tone, no compliance or "preserved" talk.
- [ ] R48 to R55 Author voice and English variety kept; no reviewer notes, pre-placed templates, canned profiles, bulk edits, context drift, authoritarian slant or stock fiction tells.
- [ ] R56 to R62 No cutoff talk, didactic notes, summary endings, refusals, truncation, stale dates, synonym cycling.
- [ ] R63 to R65 Plain human patterns; every choice explainable; no overcorrection.
- [ ] R67 to R70 Voice matched; voice only from the author; minimum effective edit; point first.
- [ ] R71 to R88 Concrete and specific; direct active verbs; no empty adverbs, metadiscourse, throat-clearing, filler that delays, stacked hedges, false ranges, authority tropes, signposting, colon reveals, rhetorical questions, dramatic fragments, kickers, forced metaphors, robotic rhythm, opener tics or reassurance kickers.
- [ ] R90 No stacked hyphenated pairs.
- [ ] `scripts/lint.py` reports zero FAIL; every CHECK judged.
- [ ] Output is the full text plus "What changed" (edit) or a findings list with rule, quote and fix (detect, R66).
