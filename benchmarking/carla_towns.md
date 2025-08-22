
## MAP SUMMARY

Table summarizing the physical area and approximate file size ranges for CARLA’s stock maps, including both “classic” towns and newer Large Maps

| Map Name       | Approximate Area (km²)       | Approximate File Size on Disk\*             |
| -------------- | ---------------------------- | ------------------------------------------- |
| Town01         | \~0.5 km²                    | \~200–400 MB (small demo town)              |
| Town02         | \~0.5 km²                    | \~200–400 MB                                |
| Town03         | \~1 km²                      | \~300–600 MB (more complex layout)          |
| Town04         | \~1 km²                      | \~300–600 MB                                |
| Town05         | \~2 km²                      | \~500 MB – 1 GB (bridges, textures)         |
| Town07 (rural) | \~2 km²                      | \~500 MB – 1 GB                             |
| Town10HD       | \~2–4 km² (visually richest) | \~1–2 GB (high-detail textures/meshes)      |
| **Town12**     | **10×10 km = 100 km²**       | **\~several GB–tens of GB** (Large Map)\*\* |
| **Town13**     | **10×10 km = 100 km²**       | **Likely similar to Town12**                |


## USAGE
* Small-scale testing or multi-ego vehicle runs 
Town01–Town05 or Town07 are most efficient (under ~2 km²).
* Visualization-heavy runs or urban complexity
Town10HD is visually rich but large (~2–4 km²).
* City-scale simulations
Town12 or Town13 (100 km²) exist but require hardware capable of handling GB-scale maps and streaming, and careful resource planning (GPU memory, asset loading, tick performance).