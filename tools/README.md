# Offline repair utilities

These tools require decoded PAC 3/9 files and compatible CDMW parsers. No game assets are bundled. Set `PYTHONPATH` to a CDMW checkout containing the `cdmw` package. Inspect inputs and keep originals; output creation is exclusive and refuses an existing destination.

```bash
python3 tools/pac_repairs.py inspect /path/to/decoded.pac
```

Hide only covered skin faces using an exact subsection name from `inspect`. The following bounds are the tested Inferno example, not a universal body mask:

```bash
python3 tools/pac_repairs.py hide-skin /path/to/torso.pac /path/to/torso-hidden.pac \
  --submesh EXACT_SKIN_SUBSECTION --y-min 0.95 --y-max 1.215 --half-width 0.26
```

This collapses selected triangles to zero area while keeping their indices allocated. Vertex records, exposed-skin customization binding, weights and other sections remain unchanged. Replacing a whole body subsection is intentionally avoided.

Restore original skeletal encoding for a verified rigid section inside a merged mesh:

```bash
python3 tools/pac_repairs.py restore-skeletal /path/to/moving-lower.pac /path/to/repaired-lower.pac \
  --reference /path/to/original-guide-free-lower.pac \
  --submesh EXACT_LOWER_SUBSECTION --first 0 --count 772
```

The 772-vertex range is specific to this Inferno conversion. Verify source subsection ordering and geometry before using it on any other model. The reference must have identical topology, UVs and skeleton palette, and ordinary skeletal encoding in the selected range.

Use `--expected-sha256 HASH` **before** the command for optional input identity checking. Output JSON reports hashes and edit counts. Install resulting resources with your own reversible archive tooling after closing the game; these utilities do not install automatically.

Offline validation used the local decoded Inferno inputs: the portable helpers reproduce the accepted waist-hiding and leg-section outputs byte-for-byte. This does not provide a generalized extraction/retargeting pipeline or prove collision in an arbitrary game build.
