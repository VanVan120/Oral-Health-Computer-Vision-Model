# History rewrite, 23 September 2026

On 23 September 2026 we rewrote the history of this repository to remove these files, which had
been committed during development and contained account details of test users of the
application:

- `database/oral_health.db`
- `database/database.db`
- `oral_health.db`  (the same file, before the 30 March 2026 restructure)
- `database.db`  (the same file, before the 30 March 2026 restructure)

The rewrite removed only these files. Every other file has the same content (the same
Git blob ID) as before. Every commit was kept, with its author, dates and message. Where
a commit message quoted an old commit ID, it now quotes the new one. Messages of annotated
tags were not changed, so they may still quote old IDs; the tables below map them. As with
any history rewrite, commit and tag signatures were removed.

(In this repository no commit or tag was signed, and no tag message quotes a commit ID,
so neither of those caveats costs anything here.)

A commit's ID depends on the whole history before it, so every commit descended from
`9038f35426b51c20ae808fbbe0d1f2b2ddaebaf1` (30 January 2026) has a new ID.
That commit is **not** the first commit in the repository: **44 of the 74 commits changed,
and the 30 commits before it kept their original IDs.**
Tags keep their names.

The analysis plan for the revision, `ANALYSIS_PLAN_R1.md`, has the same blob ID as before
the rewrite (`7cd38956dd1a6da70807063c0871746d117f5e03`), and its commit keeps its
original date of 21 September 2026.

The application creates the `database/` folder and its tables by itself on first start
(`core/database.py` calls `os.makedirs(..., exist_ok=True)`, and `create_db_and_tables()`
runs from the FastAPI startup hook), so no extra step is needed to run the app from any
commit or tag, before or after this note.

## Commit IDs cited in the paper and supplementary material

| Cited as | Now | Date | Commit subject |
|----------|-----|------|----------------|
| `12f3199` | `7ea8df283819e63b093a4de7d0e35ec42b768da5` | 2026-09-21 | Pre-register the revision R1 analysis plan |
| `5b815bb8e7f873f6e11771c55af12c3e7598d506` | `9504bf16e9bd063f52aec357599ae3c2c20a6c92` | 2026-08-13 | Ignore the remediation and leakage-audit specs |
| `f7e56f7` | `f7e56f79b619693979e7fb33cabc2cb2538ceb05 (unchanged)` | 2025-12-07 | Oral AI first commit |
| `122e026` | `122e02688bb99adfb31832169f30140fcb7c48b3 (unchanged)` | 2025-12-12 | Model B has been enhanced via evolution training |
| `48e1c4e` | `492b247320c575c454daf749616fe6112cf458f9` | 2026-02-05 | update the design for the analysis view for users |
| `5c2dc35` | `7c145fc424aca59215889a382379775d2cf6a8f7` | 2026-03-01 | evaluation for all model |
| `7210dea` | `fd32766ae41dfc9b8c8dc67fa2b4e8986800836a` | 2026-04-24 | latest changes |
| `0b21474` | `0b2546a31f633e1c429a0d7c38953942e92b7aea` | 2026-08-13 | Key display names on the model's class registry, not on index |
| `9ad5b13` | `268ed24d242dd0cfedcf28df803b69c1225dffe9` | 2026-08-13 | Move the JWT signing key and Roboflow key to environment variables |

Two of the nine predate the first removed file and are **unchanged**: `f7e56f7` and
`122e026`.

## Tags

| Tag | Before | After |
|-----|--------|-------|
| `v1.1-r1` | `3cad249fed9a7c44cb2db0183936970649bbe14c` | `bbab477e2d7a139c5204f886b4ae181fc0c153be` |
| `v1.1-r1b` | `c76379eed811f6240781dd19daa560198b5651e0` | `ea5d58596a69a9814fd85ed53dcaeee47cb71a24` |

Both tags are annotated and keep their names and messages; only the commit each points
to has a new ID.

## Other commit IDs quoted in this repository

Files written before the rewrite, such as the audit outputs under `audit/results/`,
quote the old IDs. They map as follows. Rows marked **unchanged** need no edit.

| Old | New | Quoted in |
|-----|-----|-----------|
| `f7e56f79b619693979e7fb33cabc2cb2538ceb05` | *unchanged* | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `3f9583ab4438a3748f3d22f19ef5b747a1b70f9f` | *unchanged* | `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `b2f2ba469eb21e6e2fe7e4ea0f3ef7bd616f37ba` | *unchanged* | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `17b99c8e8daadfa5bc3a6fc0b2d45db3554af4c2` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `89cc020480291011f2e8bd04da6e6ca644f88449` | *unchanged* | `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `c78787b8bca6046e28b6230276a73aafe191ecdf` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `32a00ce9fd3b78d3d78b97003f1f47310be4bf9f` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `7c8a2d123414b365df5f0dc3e805b12d05672810` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `3bf90328a443d122261b9f8322ae8be2dfacdd9d` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `8e93e5b9ad0f7b8cf5134e41465583d3b7f82429` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `a0352b2fcc6accf2635e124e2f352a1fe8c2a55d` | *unchanged* | `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `7930619bf1fd2f589bffe2764bad16e651ff5d33` | *unchanged* | `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `48a5282062744c973b4ab5fec71282d650955e53` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `337cdd36a466ebc0244c78416d9cd3317a601767` | *unchanged* | `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `e56c539515e6d3b0a7af2dcc29c50a358627cc53` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `492fd05bd5939a8970b052a488a6d40199bf25a1` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `1c283fe58a11350a9ec9983db3c92f7f9801f61c` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `e845ccec01bb9b01896d77f5a2230fdc3b6561e3` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `b6d1718b4fb8cac176bd8628fd1ec39e8169baa7` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `0dc7cdd652bec502d786bc98aa49d76ba3839189` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `5686e9b05927b1dbd3cbaa43160ba8a038b90122` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `c7c4ff01bf2966a25263187fa3efb9087a6769cd` | *unchanged* | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `1295ee6dea93aae0c42da5cfee9d737e397a6b53` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `2103d29d31add46c8c4aef674cc3f72415185fd0` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `595e696485f4e6e259e9ac5676c42d5f3b6c4d3b` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `570553314dd9dc750fed7de4f3d3633b066d2789` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `0a89bb7bee0cb87145af87926c07278af07d7411` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `9ca7b6c33ce701d9332f4cb5f71df8477166c703` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `122e02688bb99adfb31832169f30140fcb7c48b3` | *unchanged* | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `8877066df63d15d725806884102b8024f52efd29` | *unchanged* | `audit/results/S16_chronology_all_commits.txt` |
| `9038f35426b51c20ae808fbbe0d1f2b2ddaebaf1` | `d37bcaf462d6750c33a870b507b17466b79701d4` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `dc96dd9737c1baab26676b3f318b380dd40878b4` | `d0de5bd73fea9707c62f7cd7c18150b9d8298f46` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `5c9f92fda6fa168dbef7a8060a75780359a63886` | `94f9f392b3a109633e7f21776f3bbec50833a029` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `2588cff7603da24a3f94e9db5800cef81868c60a` | `441c1ced69379c35831262cd509222b2e3ac89fc` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `211ba28312686f2129eb836858798c06d2aed9fa` | `36e04d032830712426af61aecd7ed9016edfeb46` | `audit/results/S16_chronology_all_commits.txt` |
| `d0f4ecf5a43fd5abbd522a07592a59d5f9b1e6e8` | `773a8f85aaa4298d43e09be4d3b04d2f562cc57f` | `audit/results/S16_chronology_all_commits.txt` |
| `48e1c4eced191b3d183720b549abe4d807202d37` | `492b247320c575c454daf749616fe6112cf458f9` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `2c67474c5aeba4d419647b616d86f046d2dbcd43` | `e959b2eff73a73c2b5707a6ecc6f049f242b4757` | `audit/results/S16_chronology_all_commits.txt` |
| `6998cf71f2596afd542a4dbfb23b9faa2b3a70bc` | `9b09cb41cec9f1b164881a5d4c1a00cd8cecb985` | `audit/results/S16_chronology_all_commits.txt` |
| `5b5a3e3fe1f885bef4ffa48c3d26c13b5b3e17a6` | `79e1049a18883692004701900147a8e5e83308df` | `audit/results/S16_chronology_all_commits.txt` |
| `a2ffd090e23232542ba2aee2d1c3d7c1d9f125d9` | `a6c9e59464e5c6fae5dc50768a59304cf899ff28` | `audit/results/S16_chronology_all_commits.txt` |
| `0c9afcf010c752beca660ff7998e2547835b2245` | `14213887068cfea9b10126579758bf9a41f329b9` | `audit/results/S16_chronology_all_commits.txt` |
| `376437e22879ca6bcd0f43ce3b2834d3871295a3` | `73cb8156f17930fc7856b0a815d788e17226bc90` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `86930015d2b699071f95ee13d2fac5fffa2e6c23` | `c77a0a8907b897d09a06d5b43e224d3a93a25aa3` | `audit/results/S16_chronology_all_commits.txt` |
| `5c2dc3588c0374ddee4011a2bc708c42dd5668f8` | `7c145fc424aca59215889a382379775d2cf6a8f7` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `57df00d16b9c2de73004167a974f014360236f47` | `7e7b14d7405e8e2f3eb157e61907fe62427927b4` | `audit/results/S16_chronology_all_commits.txt` |
| `015d8cd67efeff2e7ea9f80e719404f077e7c367` | `3b68f491bb175e8bbeec3819e33ccb44657435fe` | `audit/results/S16_chronology_all_commits.txt` |
| `3920c0820cdb61452156d838d8ab5f0a4fd99593` | `d0607c0468de5be01ddf5cbd30398d15d697f76e` | `audit/results/S16_chronology_all_commits.txt` |
| `275e4489eff2779c50f9c660dcb21d8f47b2f181` | `5e7fc3fd0dfa7eb0a744e58c7b8ed9e75714a087` | `audit/results/S16_chronology_all_commits.txt` |
| `09e37adf948a7d56878f67a2c316f8ab658bf75f` | `c4130207a851213fa4300986bc67c6e42d7b6f2e` | `audit/results/S16_chronology_all_commits.txt` |
| `f5c69a6a4edfcb70d1efa9cba5190611352df724` | `230101cdc0e9b364aa7509ce4920542d63429f23` | `audit/results/S16_chronology_all_commits.txt` |
| `065dbd44ea4b740121e7dcbd989038f76669a02f` | `652a63ab56f0c10199dfc91f0a815c21ac693a29` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `0a9faf894ff14585737856ec3f4a48c8389ac51a` | `f7afc459084dbaaae95e707207642749b2ecebe4` | `audit/results/S16_chronology_all_commits.txt` |
| `7210dea81144dee4ec214776165790d308e43e17` | `fd32766ae41dfc9b8c8dc67fa2b4e8986800836a` | `ANALYSIS_PLAN_R1.md`, `audit/README.md`, `audit/results/S13_request_path_and_mapping.md` and 5 more |
| `0b21474f1fcec2d1957c2a4bf8e9f0a627e65fb9` | `0b2546a31f633e1c429a0d7c38953942e92b7aea` | `audit/results/S13_request_path_and_mapping.md`, `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` and 2 more |
| `46fddfbbf71dc03026c8597928858eb2d3ff315f` | `00010782fae1068d86d6bf865dd04764bd312326` | `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `9ad5b13b24f698da7569789d97bd28e3fbd080a2` | `268ed24d242dd0cfedcf28df803b69c1225dffe9` | `audit/results/S16_chronology_all_commits.txt` |
| `2eccc76099b6ac672415bf3c92d3cf2215806042` | `2c07981c265fb42e78fa24eb8ad142495aacd8ee` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` |
| `5b815bb8e7f873f6e11771c55af12c3e7598d506` | `9504bf16e9bd063f52aec357599ae3c2c20a6c92` | `audit/results/PROGRESS.md`, `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` and 1 more |
| `12f3199e0669565b35fe663e3b9bc6fe993cc3a7` | `7ea8df283819e63b093a4de7d0e35ec42b768da5` | `audit/results/PROGRESS.md`, `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt` and 1 more |
| `aa758e6b13e7fb805404fec72f2668be8be4c662` | `f973de76aeef6a940026560affce970d8c94e48c` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `723980862fea1ba70a10ff916f8d4abdd868aba1` | `e42685be2ff0d3eee49a8894ca41650de681fba9` | `audit/results/S15_weight_history_and_warm_start.md`, `audit/results/S16_chronology_all_commits.txt`, `audit/results/SUMMARY_R1.md` |
| `f68e14ff02629e836ca3c323dad68a7ed202ead3` | `b8f506400aa608be4a23223d6f38eff462f538bb` | `audit/results/SUMMARY_R1.md` |
| `47d1f9a6bdb1de38fa47bc1c6d9af63bcf751b14` | `5096fcc00f2b84f05fbb3abeeb741e8586151daf` | `audit/results/SUMMARY_R1.md` |
| `e8fdd915b412a01430a29abb0dacd56c4ad42285` | `d26fbeb78adab6dad094b3ec6adee6e7dd275b6a` | `audit/results/SUMMARY_R1.md` |
| `5eb022dfa15006faf7ec66e13cabbb644a9a1d41` | `3d8e60568f620c8533cec62e4b6f07f66864cddd` | `audit/results/SUMMARY_R1.md` |
| `a4ad95b650829562df863720cdda3d72bdc3023d` | `c45b63e8747fc29f23ea088df51b513c93299a31` | `audit/results/SUMMARY_R1.md` |
| `0cc21200b9713d8d414b77fbfc248740c2a94c46` | `ca0019c0211415be8efa5b45e5a671bcbc47f716` | `audit/results/SUMMARY_R1.md` |
| `2c5731a48ba2c6c8a5db9d131ebb1718cad60e28` | `721ab7e2d4b6328e2e5e4b737a1113656f70395c` | `audit/results/SUMMARY_R1.md` |
| `d52b1b24bcd06c7794d75b1808cd0af56ba0cc63` | `f006e1171a1922b2fb66ba1ca26710ec56ceff13` | `audit/results/SUMMARY_R1.md` |
| `abb3e293c3588cd1e97b46a856c6973b8573217b` | `5fd09c10d09914103b3a045ab830b4f969212d2b` | `audit/results/SUMMARY_R1.md` |
| `3cad249fed9a7c44cb2db0183936970649bbe14c` | `bbab477e2d7a139c5204f886b4ae181fc0c153be` | `audit/results/SUMMARY_R1.md` |
| `81f8b8f4204ab797c0a1e1ce0894f163d4d042df` | `d96e00070b7fde89e4a262c2e62d76212f2e31f1` | `audit/results/SUMMARY_R1.md` |

73 commit IDs are quoted in the tree; **43 changed** and
30 are unchanged.

