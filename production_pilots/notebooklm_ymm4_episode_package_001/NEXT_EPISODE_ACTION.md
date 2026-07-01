# Next Episode Action

The next action is one concrete production step:

Use one real, user-approved NotebookLM transcript as input and regenerate this
package for that episode, then manually confirm YMM4 CSV import.

## Do Next

1. Put the real transcript in a new episode-specific input file.
2. Create or update the speaker map.
3. Run `validate`, `build-csv`, `build-cue-packet`, and, if useful,
   `build-diagram-packet`.
4. Open YMM4 manually and import the CSV.
5. Record the import result and concrete fixes needed.

## After That

If the import is acceptable, proceed to render proof, thumbnail direction,
title/description refinement, and upload approval. Do not add OAuth, automatic
posting, or status-producer work until multiple posting candidates have passed
manual production review.
