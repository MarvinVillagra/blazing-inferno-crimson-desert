# Blazing Inferno — Crimson Desert

Reusable notes and offline repair tools from porting Black Desert Online's Striker Blazing Inferno outfit into Crimson Desert.

This is an experimental porting toolkit and case study. It is not a ready-to-install outfit download or a complete automated converter. Obtain your own source assets and target templates locally. Game archives, extracted meshes/textures, saves, executable dumps, and third-party tools are not included.

Screenshot publication is pending browser upload support.

## Current result

User testing confirms actual clothing gloves and forearm armor, exposed arm skin following character skin-color changes, improved arm clearance, covered hip/stomach skin, visible legs, moving skirt panels, and no remaining reported back glitch. Dye and metallic armor rendering have progressed, but material behavior still needs broader verification.

**Remaining limitation:** overlapping skirt layers can pass through each other. Motion is confirmed; complete garment-to-garment collision is not. The latest screenshot is a still image and does not establish animation or contact behavior.

The accepted baseline combines covered-waist skin hiding, a local copy of the target game's native cloak physics profile, and original skeletal encoding for the lower outfit's leg section. An additional same-garment collision switch test is staged locally but is **not installed or accepted**, and is excluded from this baseline.

## Start here

- [Porting workflow](docs/workflow.md)
- [Findings and failed experiments](docs/findings.md)
- [Offline tools](tools/README.md)
- [Current baseline recipe](docs/baseline.md)

The Python tools use the `cdmw` format parsers from [CDMW-Full](https://github.com/Ratty123/CDMW-Full). That project is a separate dependency with its own licensing. Place a compatible checkout's package root on `PYTHONPATH`; these tools refuse unsupported or mismatched inputs rather than guessing a binary layout. Python 3.12 was used for the local checks.

## Scope

Tools operate on explicitly supplied, decoded PAC files and write new files. They do not log into BDO, connect game accounts, modify saves, patch a live process, or install into a running game. Local asset work does not justify guarantees about account safety or undetectability.

No author affiliation with Pearl Abyss is implied. Game names and asset ownership remain with their respective owners. Original code and documentation here use the MIT license; that license does not grant rights to game assets or dependencies.
