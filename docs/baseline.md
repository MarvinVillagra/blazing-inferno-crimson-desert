# Accepted Inferno baseline

These values describe one tested transplant. They are not universal settings for all outfits or game versions.

| Area | Accepted behavior / recipe |
| --- | --- |
| Gloves | Use the actual outfit hand geometry as clothing. Gardbrace weapon cosmetics are separate; do not substitute a two-handed weapon for gloves. |
| Skin customization | Native skin subsection alias `CD_Nude_Sub` within `CD_Upperbody`; include `CD_Upperbody@CD_Nude_Sub` in skinColor binding. Exposed skin retains native UVs and weights. |
| Covered waist | Hide 782 central waist skin triangles in each of four stored LODs. The locally tested selection was Y between 0.95 and 1.215 meters, absolute X below 0.26 meters. Preserve exposed skin and armor records. Confirm coordinates on another model before selecting faces. |
| Lower mesh | 7,862 visible vertices / 9,592 triangles per stored LOD. Preserve original UVs, faces, normals and four detail levels. |
| Guides | 724 guide vertices / 909 guide triangles; 328 fixed, 396 moving. Whole rendered islands use coherent guide components. |
| Leg participation | Original lower donor starts with a FOOT-named section containing 772 vertices / 1,098 triangles. Restore its original skeletal record lanes; remove 667 erroneous cloth bindings per LOD. This section's name alone was misleading: verify geometry before classifying it. |
| Skirt participation | 5,477 rendered vertices retain guide influence per each of four LODs after leg repair. |
| Physics profile | Item-owned copy of native `Cloak` profile, with native `Ultra` collision, `IsCloak=1`, and other settings retained together. Do not globally replace native profiles. |
| Layering | Not fully resolved. Native profile still has `SkipSelfMeshCollidable=1`; changing that setting is not proof that cloth triangles self-collide. |

Local acceptance record: the user confirmed hips/stomach covered, then legs visible again while skirt movement remains; a follow-up reports no remaining back glitch. Other animation extremes, additional outfits and future game updates require separate testing.

Archive readback establishes installed bytes and mount priority. It does not establish the runtime contact list, active solver flags, or every animation outcome.
