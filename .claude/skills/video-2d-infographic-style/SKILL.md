---
name: video-2d-infographic-style
description: Plan and build 2D infographic / explainer-style animated videos (flat vector, kinetic text, icon-driven scenes, voiceover-synced) using the user's own voice and script. Use when the user wants an infographic-style video, motion graphics, or AI-generated 2D explainer.
---

# 2D Infographic Video Style (Pekaya)

> STATUS: General 2D infographic toolbox + notes from the 10 reference TikToks (caption/metadata level).
> Frame-level visual review is still pending (TikTok blocks video download); see "Reference observations".

## Language rule (important)
- All on-screen text, captions, voiceover script and narration MUST be in **Bahasa Melayu** (Malaysia), matching the user's own voice.
- If a reference video is in Indonesian (e.g. `@galihry.id`) or English, copy only the *editing technique*, never the language. Convert wording to natural Malay (e.g. "bikin" -> "buat", "kaya gini" -> "macam ni"), not Indonesian.
- Use English only for fixed terms that Malay speakers normally keep (e.g. "AI", "motion graphic").

## Principles (read first)
- The style is a *toolbox*, not a template. Never clone a reference video shot-for-shot.
- Content comes from the user's own voice recording / script. Style serves the message.
- Pick techniques per scene: use what fits the sentence being spoken, skip what doesn't.

## Pipeline
1. **Script/voice**: take the user's transcript (or transcribe their voice). Split into beats of one idea each (3-8 s).
2. **Storyboard**: per beat -> one visual metaphor, key word(s) for on-screen text, transition in/out.
3. **Assets**: flat vector icons/illustrations (consistent stroke + palette), simple characters, charts, maps.
4. **Animate**: build in Remotion (preferred, code-driven; see `remotion:*` skills) or Canva/Figma motion.
5. **Sync**: align cuts and text pops to voice waveform / word timestamps (captions via Remotion captions).
6. **Polish**: sound design (subtle whooshes/pops, low music ducked under voice), export 9:16 1080x1920 for TikTok/Reels, 16:9 for YouTube.

## Technique toolbox (choose per scene)
| Need | Technique |
|---|---|
| Hook (0-3 s) | Big kinetic headline, bold number, or question; fast scale-in |
| Explain a concept | Icon + label pop-in, simple diagram drawing itself (stroke-dash reveal) |
| Compare | Split screen, before/after slider, side-by-side cards |
| Statistics | Animated counter, bar/line/donut chart growing from zero |
| Process/steps | Numbered nodes connected by a drawn line, one step per beat |
| Location/Geography | Flat map with zoom-to + pin drop |
| Emphasis | Highlight sweep, underline draw, shake/bounce, colour flash |
| Transitions | Wipe, slide-push, zoom-through, shape-morph; keep 1-2 types per video |
| Captions | Word-by-word highlight, large, safe-zone aware, high contrast |

## Visual rules
- Flat vector, limited palette (3-5 colours + 1 accent), generous whitespace, rounded shapes.
- One focal element per beat; max ~7 words on screen unless a list.
- Motion: ease-out entrances (~12-20 frames at 30 fps), slight overshoot for pops, stagger lists by 4-6 frames.
- Keep the same type system and icon style across the whole video.
- Use brand colours/logo of the project if defined (check repo README/brand files).

## Reference observations (from 10 TikTok references)

> Source: public caption, duration, hashtags and audio label of each post. The video frames themselves
> could NOT be downloaded (TikTok blocks it), so visual details below are what the creators state, not
> frame-by-frame review. Add frame-level notes when screen recordings are provided.

### What the references have in common
- Format: vertical 9:16 (576x1024 source), short 24-37 s (sweet spot ~25-30 s), one idea per video.
- Built with **Claude Code + Remotion** (code-driven video, no editing timeline / After Effects).
  `@galihry.id` (Indonesian, "Cara cepat bikin motion graphic") shows the same Claude + Remotion flow.
- Creator-stated ingredients: motion graphics, **kinetic typography** ("visuals that bring every word to life"),
  **seamless morphing transitions**, **animated numbers / counters**, **realistic 3D objects**, premium 3D motion
  design, **sound design / SFX**, hip-hop beat bed on some.
- Input is often a **raw voice/podcast clip** ("Same footage. Different level.") turned into an edited story:
  the speaker's words drive the visuals (Alex Hormozi, Joe Rogan, Iman Gadzhi-style talking clips).
- **Reference-driven styling**: "stop saying 'cinematic'; give one visual reference + one prompt" - show a
  reference image/video for the look instead of describing it in words.
- Before/after framing ("RAW FOOTAGE vs EDITED") is used as the hook/proof in several posts.
- Typical hook topics: advice lists ("3 ways to ..."), motivation lines, AI/tool opportunity statements.

### Per-post notes
| Ref | Creator | Len | Stated style |
|---|---|---|---|
| ZSgQatVT5 | galihry.id | 27s | Motion graphic via Claude + Remotion, quick workflow (Indonesian) |
| ZSg4y98Wu | brandlogistics | 25s | Full video from code: realistic 3D objects, motion graphics, sound design |
| ZSg4ybrN8 | brandlogistics | 29s | Raw vs edited: animated numbers, motion graphics, smooth transitions |
| ZSg4yq7Mo | brandlogistics | 27s | Motion graphics, transitions, 3D objects, animations, SFX |
| ZSg4yDTBM | brandlogistics | 24s | Motivational talking clip + edit (Rogan-style) |
| ZSg4y4EqH | brandlogistics | 28s | "3 ways to find a business idea": cinematic edit, Remotion, Hormozi clip |
| ZSg4yCP1J | brandlogistics | 37s | Podcast clip -> cinematic story: 3D motion design, morph transitions, kinetic type |
| ZSg4yUj4U | brandlogistics | 32s | Talking clip edit, AI-opportunity message (Iman Gadzhi-style) |
| ZSg4yHtyn | brandlogistics | 25s | Motion design from a few references + one prompt, hip-hop beat |
| ZSg4yGMpK | brandlogistics | 36s | Reference-based direction vs "cinematic" prompting, hip-hop beat |

### How to use these ideas (selectively, not as a template)
- Voice-first: transcribe the user's own recording (word timestamps), build every visual from what is said.
- Pick per beat: kinetic word (emotional line), counter/chart (a number), icon diagram (a process),
  3D/object shot (a concrete noun), morph transition (topic change), plain captioned shot (breathing room).
- Ask for / use a visual reference image for look & feel before generating scenes.
- Always add sound: subtle SFX on text pops/transitions, low beat ducked under voice.
- Keep 25-35 s unless content needs more; hook in the first 2 s.
- Don't force 3D or heavy effects when a clean flat infographic explains the point better.
