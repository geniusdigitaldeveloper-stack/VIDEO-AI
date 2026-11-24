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
| **Perkataan kunci positif** (hook baik: nikmat, cinta, sayang, ingat, cari, muhasabah…) | **Hijau** `#4ADE80` |
| **Perkataan kunci negatif** (benda buruk: hilang, balasan, bukan, tak suka, rugi, dosa…) | **Merah** `#F87171` |
| **Perkataan/ayat Arab** | **Traditional Arabic** (regular, **bukan bold, bukan italic**), warna sama `#38BDF8` |

## Peraturan
1. Berlaku untuk setiap jenis video: Remotion, Hyperframes, ffmpeg/ASS, infografik dengan suara, apa sahaja, selagi ada teks ucapan user.
2. User bercakap campur BM + Inggeris. Semasa menjana subtitle, **tandakan setiap perkataan Inggeris** (termasuk perkataan pinjaman yang user sebut dalam Inggeris seperti *actually*) dan jadikan italic. Jangan italic-kan perkataan Melayu, nama jenama atau nama khas.
3. Kebolehbacaan: tambah outline gelap nipis (`#0B1020`, 4-6 px) atau bayang lembut supaya biru cerah jelas di atas video; kekal dalam safe zone (elak 220 px bawah, 150 px atas untuk UI TikTok).
4. **Bahasa Arab**: mana-mana perkataan/ayat Arab (doa, ayat, istilah) guna font **Traditional Arabic**, weight biasa (400), **tanpa bold dan tanpa italic**, warna biru air `#38BDF8` yang sama. Tulis dengan huruf Arab sebenar (jangan rumi) dan kekalkan harakat jika ada. Arah RTL.
5. 2-4 perkataan satu baris; susunan lain ikut `video-sound-and-captions`.
6. Font: guna Poppins (Google Fonts). Remotion: `@remotion/google-fonts/Poppins` dengan weight `600`, style `normal` dan `italic`. ffmpeg/ASS: pasang/letak fail Poppins-SemiBold dan Poppins-SemiBoldItalic, `Bold=0`.

## Animasi tetap (subtitle) — WAJIB
1. **Kotak kaca silver gaya iOS yang meluncur.** Hanya SATU kotak bagi setiap baris. Ia duduk di belakang perkataan yang **sedang disebut** sahaja, dan bila perkataan seterusnya disebut ia **meluncur lancar** (gerak + ubah lebar/tinggi) ke perkataan itu. Bukan semua perkataan berkotak serentak.
   - Rupa: kaca kelabu/silver lut sinar. `background: linear-gradient(180deg, rgba(236,240,246,.34), rgba(170,178,190,.22))`, `backdrop-filter: blur(14px) saturate(160%)`, border 1.5px `rgba(232,236,244,.78)`, radius ~22px, highlight dalam `inset 0 1.5px 0 rgba(255,255,255,.7)`, bayang `0 8px 20px rgba(0,0,0,.28)`. Padding ~14px kiri/kanan, ~4px atas/bawah perkataan.
   - Gerak: mula meluncur ~0.06 s sebelum perkataan disebut, tempoh ~0.34 s, easing lancar `power3.inOut` (rasa sistem iOS 60fps, tiada lompat). Kotak fade/scale masuk (0.85→1) pada perkataan pertama baris, fade keluar di hujung baris.
2. **Pop per perkataan (spring).** Setiap perkataan muncul tepat masa disebut: opacity 0→1, scale 0.6→1, naik 18 px→0, ~0.42 s, `back.out(2.4)` (Remotion `spring({damping: 12, stiffness: 180, mass: 0.6})`). Perkataan belum disebut kekal tempatnya (`opacity:0`) supaya baris tak melompat. Teks Arab = satu unit (satu kotak).
3. **Warna perkataan kunci:** perkataan hook yang baik = hijau `#4ADE80`, yang menunjukkan benda buruk = merah `#F87171`, selebihnya biru `#38BDF8`. Tandakan semasa jana subtitle (`"tone":"pos"` / `"tone":"neg"`). Guna dengan berhemat: perkataan kunci sahaja, bukan setiap perkataan.
4. Kedudukan: **bawah tengah**, betul-betul di tengah mendatar (x = 540 pada 1080), dalam safe zone (elak 220 px bawah, 150 px atas).
- **Hanya subtitle ucapan.** Teks grafik/infografik (keyword, kad, label, kaunter) TIDAK guna gaya, font atau warna subtitle ini; grafik guna font berbeza.

## Hyperframes
Setiap baris: `<span class="subtxt"><i class="gbox"></i><span class="w pos" data-t="START">nikmat</span> ...</span>`; `.subtxt{position:relative;isolation:isolate}`, `.w{display:inline-block}`, `.gbox{position:absolute;z-index:-1}` + gaya kaca di atas (letak `filter`/drop-shadow pada `.w`, bukan pada `.subtxt`, supaya backdrop-filter berfungsi).
```js
const geo=w=>({x:w.offsetLeft-14,y:w.offsetTop-4,width:w.offsetWidth+28,height:w.offsetHeight+8});
ws.forEach((w,k)=>{const t=Math.max(lineStart,+w.dataset.t);
  tl.fromTo(w,{opacity:0,scale:0.6,y:18},{opacity:1,scale:1,y:0,duration:0.42,ease:"back.out(2.4)"},t);
  if(k===0){tl.set(box,{x:()=>geo(w).x,y:()=>geo(w).y,width:()=>geo(w).width,height:()=>geo(w).height},t);
    tl.fromTo(box,{opacity:0,scale:0.85},{opacity:1,scale:1,duration:0.3,ease:"power3.out"},t);}
  else tl.to(box,{x:()=>geo(w).x,y:()=>geo(w).y,width:()=>geo(w).width,height:()=>geo(w).height,duration:0.34,ease:"power3.inOut"},t-0.06);});
tl.to(box,{opacity:0,duration:0.15},lineEnd-0.15);
```
(Nilai fungsi `()=>` diukur semasa render, selepas font dimuat.)

## Remotion
Guna komponen `templates/video/remotion/Subtitle.tsx` dan pemalar `subtitle` dalam `theme.ts`. Format perkataan:
```json
[{"text":"saya","start":0.0,"end":0.3},{"text":"actually","start":0.3,"end":0.8,"en":true},{"text":"nikmat","start":0.8,"end":1.2,"tone":"pos"}]
```
`en: true` = italic Inggeris. `tone: "pos"` = hijau, `tone: "neg"` = merah. Komponen sudah ada kotak kaca yang meluncur. Teks Arab dikesan automatik (julat Unicode Arab) atau tanda `"ar":true`; ia guna Traditional Arabic, tegak, weight biasa.

**Nota font Arab:** Traditional Arabic ialah font Microsoft (Windows/Office), bukan Google Font, jadi ia tiada pada mesin render Linux/cloud. Untuk render tepat, render pada mesin yang ada font itu (Windows/Office) atau pasang fail Traditional Arabic pada mesin render (sistem fon). Kalau tiada, Subtitle.tsx jatuh ke **Amiri** (Google Font, rupa naskh tradisional yang hampir sama) dan aku mesti bagitahu user fallback digunakan. Atau dalam teks biasa: `saya *actually* suka`.

## ASS (ffmpeg)
`Style: Sub,Poppins SemiBold,64,&H00F8BD38,&H00F8BD38,&H00201B0B,&H64000000,0,0,0,0,100,100,0,0,1,5,1,2,60,60,260,1`
Perkataan Inggeris: bungkus dengan `{\i1}actually{\i0}`.
Arab: `Style: Arab,Traditional Arabic,72,&H00F8BD38,&H00F8BD38,&H00201B0B,&H64000000,0,0,0,0,100,100,0,0,1,5,1,2,60,60,260,1` (Bold=0, Italic=0). (Warna ASS ialah BGR: `#38BDF8` = `&H00F8BD38`.)
