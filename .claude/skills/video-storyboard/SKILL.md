---
name: video-storyboard
description: Turn a video script or voiceover into a beat-by-beat storyboard (visual, on-screen text, transition, duration per scene). Use when the user wants a storyboard, scene plan or visual breakdown for a video (BM/EN).
---

# Video Storyboard

## Base prompt
> Turn this script into a scene-by-scene storyboard: for each beat give duration, visual, on-screen text, voiceover line, transition and sound cue. Script: [script]

## How to apply
- Split the script into beats of one idea each (3-8 s). Output as a table using `templates/video/storyboard.md`.
- One visual metaphor per beat; keep 1-2 transition types per video.
- Specify the aspect ratio (9:16 short-form, 16:9 YouTube) and keep text inside safe zones.
- Reply in the user's language (Bahasa Melayu or English). Finish with a concrete next step (assets list or build in Remotion/Canva).
- For Remotion builds, also save the storyboard as `beats.json` (see `templates/video/remotion/beats.example.json`) and continue with `video-remotion-builder`.
