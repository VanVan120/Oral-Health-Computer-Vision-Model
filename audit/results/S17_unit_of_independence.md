# Unit of independence (spec Phase 5.5) — answered from the files

The question is what identifiers actually exist, so the manuscript can state the
correct unit of statistical independence. Answers are YES / NO / PARTIAL with
the evidence, and each PARTIAL says what would upgrade it.

The image datasets are not on this machine, so these answers come from the
repository, the notebooks, the application's database schema, and the published
supplementary material in `audit/results/reference/`. Where an answer depends on
the images themselves, that is stated.

---

## 1. Do patient IDs exist? — **NO**

No patient identifier attaches to any dataset image.

- Roboflow export filenames carry a class-and-index stem plus a content hash —
  e.g. `calculus-1160-_jpg.rf.e4bf320a31bb09ba6e1dac644f42ad40.jpg`,
  `OSCC_400x_105_jpg.rf.6c2a7c021cc03afa80b47172faf95eca.jpg`
  (`audit/results/reference/S1_aligned_duplicate_pairs.csv:2`,
  `S5_histopathology_leaked_validation.csv:2`). Neither encodes a subject.
- The application's schema (`core/models.py`) defines exactly four tables:
  `User`, `Appointment`, `DailyHabitLog`, `GenAIFeedback`. **None stores an
  image, an inference result, a specimen, or a study.**

One thing must be said explicitly to avoid a false negative on a grep: a
`patient_id` column *does* exist, at `core/models.py:16`,
`patient_id: int = Field(foreign_key="user.id")`. It is the appointment-booking
foreign key to a registered application user. It never touches a dataset image
and plays no part in any reported metric. It is not a patient identifier for the
evaluation data.

**Consequence:** no analysis in this manuscript can be clustered by patient, and
no patient-level quantity is estimable. That is a property of the data, not a
choice, and it cannot be repaired after the fact.

## 2. Do source-photograph IDs exist? — **YES**

This is the one identifier that genuinely exists, and the audit already relies
on it.

Roboflow encodes the pre-augmentation identity as the filename stem before
`.rf.`. The executable definition is in this repository:

    audit/scripts/near_duplicates.py
    def source_of(name: str) -> str:
        """Roboflow encodes the pre-augmentation identity before '.rf.'."""
        return name.split(".rf.")[0] if ".rf." in name else name

It is materialised as a column in three of the published supplementary files:

- `S1_aligned_duplicate_pairs.csv` — `test_source`, `train_source`
- `S2_orientation_duplicate_pairs.csv` — `test_source`, `train_source`
- `S5_histopathology_leaked_validation.csv` — `source_prefix`

and the published `S0_README.txt` states the convention outright: *"source" =
filename before ".rf.", i.e. the pre-augmentation identity*.

**Consequence:** the source photograph is the available unit of independence,
and it is the one the resampling should respect. Two images sharing a stem are
not independent observations.

**The limit of this identifier, which must be stated with it:** it identifies
only *augmented copies of one file*. It cannot identify the same lesion
photographed twice, in two sessions or from two angles — those would be two
distinct source stems and would leak identically. The published `S0_README.txt`
says the same thing under KNOWN LIMITS, and calls all its counts lower bounds.
So "source photograph" is a *lower-bound* unit of independence, not a guaranteed
one.

## 3. Is there any episode or visit information? — **NO**

Nothing in the datasets, the notebooks or the schema records a visit, an
episode, a date of capture, or a session. `Appointment` records application
bookings between registered users and has no link to any image.

## 4. Is there any record of upstream augmentation? — **YES**, with counts

`S5_histopathology_leaked_validation.csv` records, per validation image, how
many copies of its source exist in the pooled corpus (`total_copies_in_pool`)
and how many of those are in training (`sibling_copies_in_train`), and lists the
sibling filenames explicitly. Over its 96 rows:

| copies of the source in the pool | rows |
|---|---|
| 3 | 66 |
| 2 | 30 |

Those 96 images span **81 distinct sources**, and all 96 have
`roboflow_origin_split == train`.

So upstream augmentation is not merely inferable — it is recorded, with
multiplicities. The pattern is that one source photograph was expanded into two
or three dataset images.

**Consequence, and it is the substantive one for Model A:** Roboflow split
*before* augmenting, so no source spans Roboflow's own partitions. The leakage
is created by the notebook, which pools Roboflow's three partitions into one
flat set (474 + 44 + 26 = 544) and re-splits with
`random_split(..., generator=torch.Generator().manual_seed(42))` into 435/109.
That re-split cuts straight through the augmentation groups: **96 of 109
validation images (88.1%) have a sibling in training**. The 13 that do not are
the subset spec 4.1(6) asks to report separately.

---

## Summary

| question | answer | strength of evidence |
|---|---|---|
| patient IDs | **NO** | schema and filenames, conclusive |
| source-photograph IDs | **YES** | column in three published files, plus code |
| episode / visit | **NO** | schema and filenames, conclusive |
| upstream augmentation | **YES** | recorded with per-source multiplicities |

What this implies for the revision: the analyses can and should cluster on the
source photograph, which the duplicate graph already does. They cannot cluster
on patient, and the manuscript should say so plainly rather than leaving the
unit of independence implicit. Because the source stem catches only augmented
copies of one file, every contamination count derived from it is a lower bound.

**Not verifiable without the images:** whether any *additional* structure exists
inside the datasets themselves — EXIF capture timestamps, camera identifiers, or
a metadata sidecar in the Roboflow export. Downloading the two datasets would
settle it, and would also let the `.rf.` stems be enumerated over the full
10,544 images rather than over the 1,098 that appear in the published CSVs.
