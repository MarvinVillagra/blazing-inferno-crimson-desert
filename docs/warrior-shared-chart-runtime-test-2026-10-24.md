# Warrior shared-chart runtime test — 2026-10-24

## Result

The reversible 0201 shared-chart test was installed for a user runtime check and then rolled back after the game was closed. The user reported that **every sword used the shared motion**. The VFX and SFX remained the Crimson Desert base effects and sounds; no BDO effect or sound was observed. The user asked to remove the custom movesets, VFX, and SFX, so the test overlay was removed and the original mount restored. Manual Save 2 was left untouched.

This confirms that replacing a shared sword chart changes the whole chart family. It does not provide an isolated BDO weapon route. It also does not verify BDO VFX/SFX bindings. Do not reinstall this shared-chart package as a custom-item implementation.

## Interpretation

- The chart replacement is visible in game, but its scope is global to swords using that chart.
- BDO-derived motion can be observed through this shared route; it cannot be attributed only to the custom BDO item.
- BDO VFX/SFX were not bound. Keep native effects and audio until a compatible event route and per-action timing are proven.
- The result does not establish that block, dodge, hit timing, or every attack chain behaved correctly; these were not confirmed in the user's report.

## Current state and next gate

The test overlay is rolled back. Keep the native mount and save intact. The next implementation must prove a separate chart/action route that activates only for the custom BDO weapon while an ordinary sword remains native. Then bind and test effects and sounds per action. Treat any future shared-chart experiment as a scoped diagnostic only, with an explicit global-family impact recorded before installation.
