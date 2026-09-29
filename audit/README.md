# Audit records

`removed/<receiver>-from-<donor>.json` holds the rows that audits cut from the tables, keyed by receiver word: the class the row had, the donor word, and the reason. They are the permanent record: a rebuild subtracts them, so a cut row cannot come back.

Two kinds of reason:

- **Reading audit** (683 rows: 353 Armenian, 325 Russian, 5 French). Written by hand, for example `native "thing"; not banda "gang"`. Armenian and Russian receiver words are short and common, and some of them start like an unrelated Latin word. The romanization gate cannot see that, because it compares letters, not meaning. Rules used: keep a pair only when the two words are a borrowing of, or share a borrowing with, each other in meaning; drop translations however close the letters; drop donor words that are not real words; keep proper names only when both sides are the same name.
- **Model meaning check** (4,028 rows, reason starts "model pass"). Claude Sonnet 5 judged every row for same source word and same meaning. Roughly nine in ten of a random sample of its cuts were correct.

The records cover only the rows that are also in the published frequency-list vocabulary, so counts here are lower than in the private build (4,711 of 5,814).
