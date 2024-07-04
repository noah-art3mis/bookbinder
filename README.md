# Bookbinder & Antiquarian

Text cleanup.

`Bookbinder.py` is regex; `Antiquarian.py` is AI cleanup.

## TODO

-   The model only responds with 4096 tokens at maximum. This means you have to do some preprocessing before sending.
    -   Add segmentation.
    -   Add batching.
    -   Add deferral to save on compute
