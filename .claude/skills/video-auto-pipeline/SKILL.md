---
name: video-auto-pipeline
description: Pipeline video gabungan TANPA tool default. Claude auto-pilih tool terbaik untuk setiap langkah/beat - Higgsfield MCP (imej, video AI, suara, muzik, upscale, buang latar, reframe, virality), Hyperframes (komposisi HTML), Remotion (komposisi React, templat di templates/video/remotion), Canva/Figma (grafik statik). Guna bila user mahu hasilkan video atau aset video, atau sebut Higgsfield, Hyperframes atau Remotion.
---

# Video auto pipeline (tiada default)

Tiada tool default. Untuk setiap langkah, pilih tool yang paling sesuai ikut jadual di bawah, dan nyatakan pilihan + sebab ringkas kepada user. Jika user sebut tool tertentu, guna tool itu.

## Jadual auto-pilih

| Keperluan | Pilih | Sebab |
|---|---|---|
| Visual realistik / sinematik, B-roll, watak, produk dalam babak | **Higgsfield** `generate_image` / `generate_video` (`models_explore` action `recommend` untuk pilih model) | Footage yang tak boleh dirakam |
| Voiceover / muzik / SFX AI | **Higgsfield** `generate_audio` (atau suara user sendiri) | |
| Kemas aset: besarkan resolusi, buang latar, tukar nisbah | **Higgsfield** `upscale_*`, `remove_background`, `reframe` | |
| Iklan produk / UGC / poster pantas | **Higgsfield** Marketing/Ads Studio | Aliran iklan siap |
| Teks kinetik, kapsyen, infografik, motion graphic, templat berulang | **Hyperframes** atau **Remotion** | Teks tepat & boleh diulang; AI tak boleh render teks |
| - projek HTML/CSS, edit pantas, tiada React | Hyperframes | |
| - guna templat sedia ada `templates/video/remotion/` atau `beats.json` | Remotion (`video-remotion-builder`) | |
| Grafik statik / thumbnail | Higgsfield `generate_image` (visual) + Canva/Figma (teks & layout) | |
| Semak potensi viral sebelum post | Higgsfield `virality_predictor` | |

Video biasa = gabungan: aset AI dari Higgsfield dimasukkan sebagai clip/`<Video>`/`<Img>` ke dalam komposisi Hyperframes atau Remotion, kemudian render.

## Langkah

1. **Skrip & storyboard** - `video-script-bm` / `short-form-video-script`, `video-hook-library`, `video-storyboard`. Tandakan setiap beat dengan tool yang dipilih ikut jadual.
2. **Aset AI (Higgsfield)** - prompt visual dalam EN, nisbah 9:16 / 16:9, tempoh. Banyak aset: `*_batch` -> `jobs_wait` -> satu `show_generation_by_ids`. Simpan fail dalam `assets/` dan rekod prompt + job id dalam `assets/SOURCES.md`.
3. **Komposisi** - Hyperframes (`npx hyperframes init` / `preview` / `render -o out/video.mp4`) atau Remotion (`npx remotion studio` / `render`). Subtitle ucapan WAJIB ikut `video-subtitle-style` (Poppins SemiBold, biru air cerah, Inggeris italic); kapsyen & SFX ikut `video-sound-and-captions`. Hook bergerak dalam 0.5 s pertama.
4. **Semak & render** - pratonton, semak sync suara, render. Pilihan: `virality_predictor`.

## Kredit Higgsfield
Setiap penjanaan guna kredit. Semak `balance`, beri anggaran kos, dan dapatkan persetujuan user sebelum jana. Jika kredit tak cukup: guna placeholder dalam komposisi, render draf, dan senaraikan aset yang masih perlu dijana.
