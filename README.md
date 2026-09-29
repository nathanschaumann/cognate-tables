# Cognate tables

Word pairs that look like the same word across six languages: English, Spanish, Portuguese, French, Russian and Armenian. **111,711 rows** in 25 directional tables covering 15 language pairs, as CSV and Markdown. They were built for a language-learning app that estimates how new a word is to someone who already knows its cognate (`nación` is not new if you know `nation`).

## What counts as a cognate here

A cognate is a **spelling fact**: two words that look like the same word once both are written in the Latin alphabet (Russian and Armenian are compared after romanization), and that mean the same thing.

- `transparent`: read without effort, like `casa`/`casa` or `nación`/`nação`.
- `altered`: recognizably the same word after a sound or spelling shift, like `escuchar`/`escutar` or `hijo`/`filho`.

Not cognates, and left out: translations that share no letters (`pecho`/`грудь`), false friends (`embarazada`/`embaraçada`), shared ancestors that no longer look alike (`padre`/`հայր`), and native words that merely start like a foreign one (`լավ` "good" is not "lava").

## Files and columns

- `csv/<a>-<b>.csv` and `markdown/<a>-<b>.md`: one pair per file, both directions where both exist.
- Columns: `receiver_lang`, `receiver_word`, `donor_lang`, `donor_word`, `class`. Words are lowercase lemmas (verbs as infinitives, nouns and adjectives masculine singular).
- Direction matters. `es` receiving from `fr` lists Spanish words with the French word each one matches. English is a donor only, so `en-es.csv` holds Spanish words matched to English.
- `audit/removed/`: every row cut by the audits (words, class, reason). `audit/README.md` explains them.
- `scripts/check_tables.py` validates the files and prints the counts; `scripts/build_markdown.py` regenerates the Markdown from the CSVs.

## Rows per pair

| pair | rows | pair | rows |
|---|---|---|---|
| en-es | 9,415 | es-ru | 3,359 + 3,337 |
| en-fr | 9,549 | fr-hy | 1,859 + 1,622 |
| en-hy | 1,921 | fr-pt | 6,328 + 6,142 |
| en-pt | 8,574 | fr-ru | 3,066 + 2,753 |
| en-ru | 2,261 | hy-pt | 1,576 + 1,662 |
| es-fr | 7,374 + 9,591 | hy-ru | 1,667 + 1,585 |
| es-hy | 1,941 + 2,123 | pt-ru | 2,182 + 2,071 |
| es-pt | 9,623 + 10,130 | | |

Two numbers mean the two directions, in the order the pair is named (`es-fr`: Spanish receiving, then French receiving).

## How they were built

1. **Word lists.** Top 200,000 word forms of [wordfreq](https://github.com/rspeer/wordfreq) 3.1.1 (`large` list) for English, Spanish, Portuguese, French and Russian. wordfreq has no Armenian, so Armenian uses a Leipzig Corpora Collection frequency list (news 2020, web 2015, Wikipedia 2021). Forms were lemmatized with [simplemma](https://github.com/adbar/simplemma) plus a few project fixes.
2. **Model pass.** Claude Haiku 4.5 got batches of 120 lemmas from one language and named each lemma's cognate in every other language, with the definition above and worked mistakes to avoid. Both sides of each pair were asked and merged (disagreement becomes `altered`; a false-friend verdict from either side drops the pair). English was asked from the English side only, plus a pass from the Armenian side for English loanwords.
3. **Mechanical gate.** Both words are romanized and must share at least half their letters.
4. **Reading audit of Armenian and Russian.** Every credited Armenian pair, and the Russian pairs for the 3,000 most-met words, were read row by row without sampling; 683 rows were cut, mostly native words matched to unrelated look-alikes. A few French rows were cut the same way.
5. **Model meaning check.** Claude Sonnet 5 re-judged every row for same source word and same meaning, in two passes (2026-09-13, 2026-09-23), which cut about 4,000 more.
6. **Publication filter.** Rows were dropped when either word is not in the public frequency lists above, or is a private name. That removed 8,239 of 119,950 rows.

The build script is not included: it needs private services (a lemmatizer bundled with the app, API access and the app's own data). These tables are a frozen snapshot of 2026-09-29.

## Limitations

- Classification is by a language model, so errors remain. A random read before the model check put the wrong-row rate near 4 percent; a read of the model's cuts found about nine in ten right, so some real cognates were lost.
- One donor word per receiver word per direction; alternates are missing.
- Coverage follows the frequency lists, not a dictionary. Lemma forms can look odd, especially in Armenian and for French elisions.
- Spelling only: a pair judged `transparent` may sound quite different.

## Licenses and sources

The tables and audit records are licensed **CC BY-SA 4.0** (`LICENSE-DATA.md`) because they derive from wordfreq data, which is CC BY-SA 4.0 (wordfreq code is Apache-2.0; it combines Wikipedia, subtitles, news, books and web text, credited in its README). The Armenian list comes from the Leipzig Corpora Collection (Goldhahn, Eckart and Quasthoff 2012), used under its CC BY terms. simplemma is MIT. Scripts: MIT (`LICENSE`).
