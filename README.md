# Bookbinder & Antiquarian

Text cleanup.

`Bookbinder.py` is regex; `Antiquarian.py` is AI cleanup.

## How to

Because every project has different requirements, this needs to be manual every time.

1. Edit config files
1. Edit python scripts
1. Run scripts

## TODO

-   FIX: 1_PREPARE batch file ends up with a empty line at the end
-   fix check batch cost to work with the 0000 files
-   The model only responds with 4096 tokens at maximum. This means you have to do some preprocessing before sending.
    -   Add segmentation.
    -   Add batching.
    -   Add deferral to save on compute
