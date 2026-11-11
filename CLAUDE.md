# Project guidance

This repo carries the shared Pekaya skill set in `.claude/skills/` (index: `.claude/skills/INDEX.md`):
18 prompt skills (research, summary, ideas, strategy, marketing, content, social, YouTube script, email,
code, debug, website, presentation, learning plan, automation, personas, competitors, custom workflow)
plus video skills (`video-2d-infographic-style`, `video-storyboard`, `shot-list`, `short-form-video-script`, `voiceover-script`, `video-thumbnail-title`, `video-content-calendar`) with templates in `.claude/templates/video/`.
Extra BM video skills: `video-script-bm`, `video-hook-library`, `video-remotion-builder`, `video-sound-and-captions`, with Remotion components in `templates/video/remotion/`.

Video tools have **no default**: auto-pick per task between **Higgsfield MCP** (`.mcp.json`, guide `docs/higgsfield-mcp.md`; AI images, video, voice, upscale, ads), **Hyperframes**, **Remotion** and Canva/Figma, combining them as needed. Use `video-auto-pipeline`; always confirm Higgsfield credit cost before generating.

- Use the matching skill whenever the user's request fits; adapt it to context rather than copying it rigidly.
- Reply in the user's language (Bahasa Melayu / English).
- When creating a NEW repo, run `.claude/scripts/sync-skills.sh <new-repo-path>` to copy these skills into it.

Also included: 52 marketing skills from marketingskills (start with `product-marketing`; upstream `marketing-plan` is `marketing-plan-corey`) and `free-llm-apis`. Sources: `.claude/skills/SOURCES.md`.

Also included: Anthropic cloud skills (`docs`, `docx`, `pdf`, `pptx`, `xlsx`, `google-workspace`, `import-memory`, `morning`, `setup-writing-style`, `skill-creator`, `session-start-hook`).

## New repos (important)
Every NEW repo must get these skills: run `.claude/scripts/sync-skills.sh <new-repo-path>` right after creating/cloning it (it only adds missing skills, never overwrites) and commit the result. For an existing repo with a different skill set, run it again to top up.

## Gaya subtitle tetap (semua video)
Setiap video yang ada suara user bercakap (Hyperframes, Remotion, infografik, ffmpeg, apa-apa): subtitle ucapan = **Poppins SemiBold (600)**, warna **biru air cerah `#38BDF8`**, dan **perkataan Inggeris (contoh *actually*) dalam italic**. Ini hanya untuk subtitle ucapan, bukan font infografik. Butiran: skill `video-subtitle-style`, komponen `templates/video/remotion/Subtitle.tsx`.
