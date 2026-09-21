# Analysis Notebook Style

These notebooks (`*/python/task*.ipynb`) are for lab analysis, not production code. The goal is
that every number and every plot can be verified by reading the notebook top to bottom — not
that the code is short, fast, or reusable. When in doubt, prefer the more explicit, more
repetitive version.

## No helper functions, except the fit model itself

Don't wrap a mask + `curve_fit` call in a function "for reuse" — write it inline, once per
dataset, even if two datasets need nearly identical code. The only functions that belong in
these notebooks are the physical models passed into `curve_fit` (e.g. `lasing_branch`,
`log_spontaneous_emission`) — those exist because they *are* the physics, not because they
save lines.

```python
# avoid
def fit_carrier_temperature(df, window, E_g=None):
    ...
fit_led = fit_carrier_temperature(df_led, WINDOW_LED)
fit_sub = fit_carrier_temperature(df_sub, WINDOW_SUB, E_g=fit_led["E_g"])

# prefer
mask_led = df_led["lambda_nm"].between(*WINDOW_LED) & (df_led["S_E"] > 0)
E_led = df_led.loc[mask_led, "E_eV"].to_numpy()
ln_S_led = np.log(df_led.loc[mask_led, "S_E"].to_numpy())
(E_g_led, T_c_led, ln_A_led), cov_led = curve_fit(log_spontaneous_emission, E_led, ln_S_led, ...)
```

## Explicit, named variables per dataset — not generic loops

Don't collect results into a `list[dict]` and loop over it to plot. Give each dataset its own
suffix (`_led`, `_sub`, ...) and write the two or three plot calls out by hand. A reader should
be able to point at `T_c_sub` and know exactly which fit it came from, without dereferencing a
dict key or stepping through a loop body.

## New columns go on the DataFrame, not into a loose Series

If a quantity is derived per-row from an existing DataFrame, assign it back as a column
(`df["S_E"] = ...`) instead of keeping it in a separate `pd.Series` variable. It stays attached
to its row context and shows up in `df.head()` for a free sanity check.

## Separate "prepare" cells from "plot" cells

A cell that builds the arrays a plot needs (fit curves, flattened flanks, unit conversions)
should contain no `plt`/`ax` calls. The following cell should contain only matplotlib calls on
already-computed, plainly named variables — no masking or fitting logic hidden inside a
plotting loop.

## Split "enrich data" into columns vs. fit parameters

When a section both adds columns to a DataFrame and fits something, split it into two
subsections/cells: one that only adds columns, one that only computes fit parameters. Each
cell should do one kind of thing.

## Comments say why, not what

A short inline comment or a markdown cell right above the code should explain the physics or
statistics reasoning (why fit in energy and not wavelength, why `E_g` is held fixed for the
second fit, why the log is fit instead of the raw signal) — not restate what the following
line of code obviously does.

## Typing preferred if it improves readability

Type annotations should be used unless the typing makes the code harder to read.