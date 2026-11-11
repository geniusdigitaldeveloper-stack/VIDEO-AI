---
name: video-subtitle-style
description: WAJIB untuk SEMUA video yang user edit/cipta (Hyperframes, Remotion, infografik, ffmpeg, apa-apa). Tetapan tetap gaya subtitle (teks yang user cakap): Poppins SemiBold, biru air cerah, perkataan Inggeris italic, teks Arab Traditional Arabic (tak bold, tak italic).
---

# Gaya subtitle tetap (jangan tukar kecuali user minta)

Terpakai pada **subtitle/kapsyen ucapan user sahaja**. Font infografik, tajuk dan grafik lain **bukan** bawah skill ini; ia ada gaya sendiri.

| Perkara | Tetapan |
|---|---|
| Font | **Poppins SemiBold** (weight 600). Bukan Bold (700). |
| Warna teks | **Biru air cerah** `#38BDF8` (sky/water blue) |
| Perkataan Inggeris | **Italic** (Poppins SemiBold Italic), contoh *actually*, *literally*, *basically*, *so* |
| Perkataan Melayu | Poppins SemiBold biasa (tegak) |
| **Perkataan/ayat Arab** | **Traditional Arabic** (regular, **bukan bold, bukan italic**), warna sama `#38BDF8` |

## Peraturan
1. Berlaku untuk setiap jenis video: Remotion, Hyperframes, ffmpeg/ASS, infografik dengan suara, apa sahaja, selagi ada teks ucapan user.
2. User bercakap campur BM + Inggeris. Semasa menjana subtitle, **tandakan setiap perkataan Inggeris** (termasuk perkataan pinjaman yang user sebut dalam Inggeris seperti *actually*) dan jadikan italic. Jangan italic-kan perkataan Melayu, nama jenama atau nama khas.
3. Kebolehbacaan: tambah outline gelap nipis (`#0B1020`, 4-6 px) atau bayang lembut supaya biru cerah jelas di atas video; kekal dalam safe zone (elak 220 px bawah, 150 px atas untuk UI TikTok).
4. **Bahasa Arab**: mana-mana perkataan/ayat Arab (doa, ayat, istilah) guna font **Traditional Arabic**, weight biasa (400), **tanpa bold dan tanpa italic**, warna biru air `#38BDF8` yang sama. Tulis dengan huruf Arab sebenar (jangan rumi) dan kekalkan harakat jika ada. Arah RTL.
5. 2-4 perkataan satu baris; susunan lain ikut `video-sound-and-captions`.
6. Font: guna Poppins (Google Fonts). Remotion: `@remotion/google-fonts/Poppins` dengan weight `600`, style `normal` dan `italic`. ffmpeg/ASS: pasang/letak fail Poppins-SemiBold dan Poppins-SemiBoldItalic, `Bold=0`.

## Remotion
Guna komponen `templates/video/remotion/Subtitle.tsx` dan pemalar `subtitle` dalam `theme.ts`. Format perkataan:
```json
[{"text":"saya","start":0.0,"end":0.3},{"text":"actually","start":0.3,"end":0.8,"en":true}]
```
`en: true` = italic Inggeris. Teks Arab dikesan automatik (julat Unicode Arab) atau tanda `"ar":true`; ia guna Traditional Arabic, tegak, weight biasa.

**Nota font Arab:** Traditional Arabic ialah font Microsoft (Windows/Office), bukan Google Font, jadi ia tiada pada mesin render Linux/cloud. Untuk render tepat, render pada mesin yang ada font itu (Windows/Office) atau pasang fail Traditional Arabic pada mesin render (sistem fon). Kalau tiada, Subtitle.tsx jatuh ke **Amiri** (Google Font, rupa naskh tradisional yang hampir sama) dan aku mesti bagitahu user fallback digunakan. Atau dalam teks biasa: `saya *actually* suka`.

## ASS (ffmpeg)
`Style: Sub,Poppins SemiBold,64,&H00F8BD38,&H00F8BD38,&H00201B0B,&H64000000,0,0,0,0,100,100,0,0,1,5,1,2,60,60,260,1`
Perkataan Inggeris: bungkus dengan `{\i1}actually{\i0}`.
Arab: `Style: Arab,Traditional Arabic,72,&H00F8BD38,&H00F8BD38,&H00201B0B,&H64000000,0,0,0,0,100,100,0,0,1,5,1,2,60,60,260,1` (Bold=0, Italic=0). (Warna ASS ialah BGR: `#38BDF8` = `&H00F8BD38`.)
