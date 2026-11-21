# 0.6.1-dev / runtime scanned-rock collision fix

User screenshot exposed repeated `CollisionMeshData couldn't be created ... non-accessible` errors in 0.6.0-dev. Reading the actual player log identified CampScannedRock adding a MeshCollider to the imported RockFace01 default mesh. Its ModelImporter had isReadable disabled, so runtime collision cooking could not access the mesh data in a player.

Enabled Read/Write on that model's importer. Rendering and collider geometry are retained. The camp environment regression now requires readable scanned collision data and raycasts a nondegenerate triangle on each matching scanned-rock collider to verify an actual cooked surface. Check-Player.ps1 now explicitly rejects CollisionMeshData and non-accessible errors, in addition to its existing exception/shader failure markers.

Correction to the 0.6.0 report: the six suites returned their PASS markers, but their error scan did not include this Unity collision-cooking error. Old player logs did contain the error; therefore that release was not error-free. The new check closes this specific gap.

Built isolated Windows 0.6.1-dev. All six fresh executable suites passed: prologue, Chapter 1, camp, spine, epilogue and intro. The camp collision surface probe passed, and the updated checker found no collision accessibility errors in those fresh logs. No continuous manual playtest is claimed. This fixes the demonstrated camp imported-mesh failure; it does not finish the remaining blockout art or gameplay production work.

Music remains unchanged. No Suno downloads or credits were used. Prior versions were not overwritten or stopped. Portable ZIP packaging validates required files, CRC and SHA-256.
