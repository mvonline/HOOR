# Native 3D PC prototype — build evidence

Date: 2026-10-21

## Source implementation

Main game project: `game/RadEHoor/`, Unity 6000.3.7f1, Windows x64.
Procedural 3D canyon, first-person CharacterController, real camera/lighting,
physical static collision, three visible creatures, intact vehicle shelter,
throwable distraction and limited transmitter. A separate darkness mode models
the ten-second interaction. Broadband test sounds use world-space AudioSources;
the listener turns with the player camera. All four directions are retained.

Editor tools create the demo scene and build Windows. `NativeGame.cmd` opens
the native executable when built, otherwise the Unity project. Browser samples
are retained as research, not the PC deliverable.

## Verified so far

- The actual C# rules compile with the Windows .NET Framework compiler.
- **40 native C# assertions pass**, covering hearing/Bang separation, radius
  boundaries, last-source targeting, quiet/stone movement, search/return,
  shelter audibility/protection, contact, transmitter orbit/tail, quiet route,
  lack of visual acquisition, and exact window boundaries/release behavior.
- The launch/build/test PowerShell files and Unity package manifest parse.
- The official Unity CLI was downloaded and SHA-256 verified. The pinned
  editor's official release checksum is checked by the resumable downloader.

## Remaining gates

Unity 6000.3.7f1 is installed locally and registered with Hub. The official
installer's checksum and publisher signature were verified. Unity CLI
1.0.0-beta.14 is current, and Pipeline 0.9.0-exp.1 is installed in the project.
The first Editor import found an invalid `com.unity.modules.inputlegacy`
dependency; that entry was removed. Import is currently blocked by the
Editor's Unity Package Manager Error dialog, which needs Retry in its window.
Unity import,
Unity-facing API compilation, Windows player build, native smoke execution,
rendered screenshot inspection and headphone listening are **not yet verified**.
No executable should be advertised as delivered before those build gates.
The licensing client is not yet available and account activation may require
the user to complete Unity's own sign-in and license interface.

`Tools/Smoke-PC.ps1` is prepared to launch a built native player, verify its
scene/mode setup and request a fresh rendered screenshot. Its existence is not
evidence that it has passed.

## Scope and sources

Rules trace to the proposal's hearing/shelter sections 3.3–3.4 and window/input
sections 2.2/6.2. No story sources are changed. Layout, speeds, reusable throws,
impact timing and throwable classification are prototype assumptions. Native
Unity positional audio does not bundle a custom HRTF spatializer. Final art,
driving, gamepad controls, translated campaign text, player studies, performance
certification and a Go/No-Go decision remain open.

Official engine reference: [Unity 6000.3.7f1 release](https://unity.com/releases/editor/whats-new/6000.3.7f1).
Build reference: [Build a player from the command line](https://docs.unity3d.com/6000.3/Documentation/Manual/build-command-line.html).
