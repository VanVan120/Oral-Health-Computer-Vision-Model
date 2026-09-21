# Dataset lineage (spec Phase 5.4) — PARTIAL, blocked

## Route availability

- `https://universe.roboflow.com/...` returns **HTTP 403** to non-browser clients
  (Cloudflare). Fetched 2026-09-21. So the Universe page route is unavailable
  from this session.
- `https://api.roboflow.com/...` requires `ROBOFLOW_API_KEY`, which is unset.
  So the API route is unavailable too.
- Therefore the fork/source question is **NOT RESOLVED**. What follows is
  search-index evidence only, and is labelled as such.

## Reference 8 — `tesisdientes/oral-diseases-5ctay-rqpxs`

Source: web search index of the Universe page (not the page itself), 2026-09-21.
Labelled INFERRED-FROM-SEARCH-INDEX, not verified against the project API.

- classes (4): calculos, caries, gingivitis, ulcera
- images: ~4.2k
- licence: CC BY 4.0

This is consistent with the manuscript revision note that reference 8 has four
classes and 4,162 images, whereas the project actually used
(`segp-fcn6m/oral-diseases-5ctay-h9oye`) has six classes and 10,000 images.
So reference 8 as printed does not describe the dataset used.

## Structural clue about the fork (NOT CONFIRMED)

Roboflow slugs carry a stable stem plus a per-project random suffix:

- ours       `oral-diseases-5ctay` + `-h9oye`
- reference 8 `oral-diseases-5ctay` + `-rqpxs`
- ours       `oral-cancer-1mnve`  + `-n5yij`
- reference 9 `oral-cancer-1mnve`  (no suffix)

The shared stems are consistent with ours being forks of those two projects,
which would make reference 8 and reference 9 the right *lineage* citations but
the wrong *dataset* citations. This is a naming-pattern inference only. It must
be confirmed against the project metadata (the `forkedFrom` / source field) once
the API key is available, before anything is written into the manuscript.

## Still required for 5.4

- class list, image counts, licence for both `segp-fcn6m` projects (API);
- fork/source field for both (API);
- preprocessing and augmentation settings from `README.roboflow.txt` in each
  download (needs the dataset download, hence the key).
