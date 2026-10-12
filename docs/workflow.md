# Porting workflow

1. Identify the exact class/outfit asset and distinguish hand clothing from weapon cosmetics. Inspect every source subsection and account for included leg pieces.
2. Keep source assets local. Record hashes and provenance so a later game update does not silently change inputs.
3. Select target clothing templates with understood skeleton palettes, material aliases, equipment slots and prefab behavior.
4. Convert geometry and weights. Preserve all stored LODs; check face indices, finite values, UVs, normals and tangent frames. Compare a rest-pose render with the original outfit.
5. Bind exposed native skin subsections to character skin customization. Hide covered body faces locally when appropriate; do not globally shrink or hide the character.
6. Build low-resolution cloth guides with intentional pins and coherent island ownership. Exclude rigid leg armor and body-following sections from simulation. Retain original skeletal encoding as a repair/reference source.
7. Audit prefab cutting and shrink relationships before blaming collision for disappearing geometry.
8. Assign an item-owned physics profile and catalog entry. Start from a coherent native profile, retain the original, and isolate each subsequent experiment.
9. Build reversible archive overlays. Check payload readback, mount priority and model catalog hashes. Save/close the game before installation and keep a rollback package.
10. Verify appearance and movement separately: standing front/back, walking, turns, bends and dodges. Record both successful and failed results. Do not equate movement with body or layer contact.

This repository provides repair utilities and a case study; extraction, general retargeting, equipment registration, texture conversion and archive installation still require the appropriate local tools. It does not yet reproduce every step through one automated command.
