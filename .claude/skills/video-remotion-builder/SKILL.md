---
name: video-remotion-builder
description: Bina video infografik/motion graphic dalam Remotion menggunakan komponen templat di templates/video/remotion dan beats.json. Guna bila storyboard sudah siap dan user mahu video dijana.
---

# Bina dengan Remotion

Rujuk juga skill `remotion:*` (create, captions, render, studio).

1. Salin `templates/video/remotion/` ke projek Remotion (atau `npx create-video@latest`).
2. Letak suara user di `public/voice.mp3`; jana kapsyen perkataan (remotion-captions) -> `public/captions.json`.
3. Isi `beats.json`: setiap beat ada `type` (kinetic | counter | steps | comparison), `from`/`duration` dalam saat dan `props`.
4. `Main.tsx` membaca `beats.json` dan memaparkan komponen ikut `type`; tambah komponen baru jika perlu.
5. Format: 1080x1920, 30 fps. Hook mesti bergerak dalam 15 frame pertama.
6. Semua teks dalam Bahasa Melayu. Palet dan fon ikut `theme.ts`; guna warna jenama projek jika ada.
7. Pratonton (`npx remotion studio`), semak sync suara, kemudian render (`npx remotion render Main out/video.mp4`).

Templat ialah titik mula, bukan had: ubah, gabung atau buang ikut keperluan video.
