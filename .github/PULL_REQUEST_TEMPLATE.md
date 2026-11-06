## What

<!-- One paragraph. Which stage / layer does this touch? -->

## Why

<!-- What breaks or is missing today? Link the issue if there is one. -->

## How

<!-- Key decision, and what you deliberately did not change. -->

## Checks

- [ ] `make check` passes
- [ ] `make test` passes
- [ ] New arithmetic or a new error path has an assertion
- [ ] No secrets, real exports, buyer data or supplier quotes
- [ ] Platform numbers stay in `markets/<market>.json` (no `null` replaced by a guess)
- [ ] Buyer-facing text is in the target market language; numbers trace to `spec_table`
