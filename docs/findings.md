# Findings and unsuccessful approaches

## Geometry, skin and outfit slots

Actual clothing gloves and Gardbrace weapon cosmetics are separate BDO assets. Preserve this distinction during extraction, equipment registration, icons and conversion.

Do not decide which body parts are included by filename alone. Inferno's lower donor includes a FOOT-named section reaching from waist to knee. Treating the entire merged model as cloth assigned 667 of its 772 leg-section vertices to simulated guides. Restoring their original skeletal encoding restored visible legs without stopping skirt motion.

Native skin-colored geometry needs native UVs, skeleton weights and an appropriate character customization binding. A skin-colored armor texture will not automatically follow the player's skin setting. Exposed arms were user-confirmed to follow customization after the subsection binding repair.

Adding waist skin filled a missing-body gap but later made covered skin protrude through clothing. Hiding only covered waist triangles resolved the reported hip/stomach exposure; exposed arm binding was preserved. Rest-pose ray tests alone did not predict animated protrusion.

## Cloth correspondence

The native lower-body template used here had no authored guides. Physics came from generated guides, not from inheriting an existing lower-body simulation.

Per-vertex nearest-guide binding can pass index checks while triangles span independent guide components. One failed version had 2,522 such triangles. Bind coherent rendered islands and audit ownership across all LODs, not just index validity.

The original coherent moving reference had 57 disconnected guide components. Whole-island ownership eliminated crossing components; this did not guarantee correct physical contact or layering. Large rendered panels were sometimes 0.09–0.13 meters from their nearest guide samples. That distance is a rest approximation measure, not proof of runtime error.

## Visibility rules

Native clothing uses part cut/shrink relationships. Imported components can be unintentionally cut by Upperbody, Hand or Foot interactions. Item-owned tags allowed isolated exclusions while preserving unrelated native outfits. Do not globally disable native visibility rules.

## Physics versus contact

A guide-free skeletal comparison retained the intended lower shape but had no skirt gravity/contact. This separated rest geometry from the deformation path; it did not prove one exact solver cause.

A constrained guide-influence test (35% influence, rigid above Y=0.94, fade over 0.18 meters) produced no useful perceived movement. It was rejected as the working baseline.

The native Lower_Fabric profile uses Normal collision. A byte-identical item-owned native Cloak profile uses Ultra collision and additional native settings. User testing showed cloth movement returned, but initially legs disappeared and layers continued to overlap. Restoring the leg section's skeletal encoding fixed the reported leg loss and back glitch.

An earlier change from SkipSelfMeshCollidable=1 to 0 under Lower_Fabric did not resolve garment overlap. A later single-setting trial under the accepted native-contact baseline is untested and not part of the published result. The setting concerns provided/selected same-source mesh colliders; its name is not proof of triangle self-collision.

Native skeleton data contains pelvis, thigh and calf capsules. Definitions do not prove that a live garment selects them or that contacts occur. Both the inspected native cloak and imported lower PAC contain zero embedded PAC volumes; absence alone does not prove missing skeleton collision.

## Evidence boundaries

Independent parsing, tangent checks, preserved record comparisons and archive readback are offline evidence. User movement tests are runtime observations, bounded to the tested version and actions. A parser executed through REA is a controlled resource observation, not native engine decompilation. Old game-build addresses must not be reused without matching the executable.
