# Setup Global Streamer — tutorial (HyperFrames, 16:9 1080p)

Edit screen recording "DOWNLOAD & SETUP GLOBAL STREAMER APPS" (BM).

- `index.html` — komposisi (dijana oleh `scripts/build.py`, jangan edit terus; ubah skrip kemudian jana semula)
- `scripts/build.py` — EDL (buang pause / 2x), bina `assets/base.mp4`, sintesis muzik + SFX, jana `index.html`
- `transcript.json` — transkrip whisper large-v3 (masa per perkataan, masa sumber)
- `silences.json` — senyap dikesan (ffmpeg silencedetect) untuk potongan pause
- `edl.json` — keputusan potongan + masa step (rujukan)

Fail media besar (`assets/base.mp4`, `assets/music.wav`, `renders/`) tidak di-commit. Bina semula:

```bash
python3 scripts/build.py /path/ke/SETUP-GLOBAL-STREAMER.mp4   # video sumber asal
npm run check
npx hyperframes preview            # studio pratonton
npx hyperframes render -q draft -o renders/preview-draft.mp4   # draf
npx hyperframes render -q delivery --video-frame-format png -o renders/final.mp4   # final (hanya selepas diluluskan)
```

Tukar teks hook, step, kedudukan ring dan zoom: `HOOK_TEXT`, `STEPS`, `ZOOMS` dalam `scripts/build.py`, kemudian
`python3 scripts/build.py --html-only`.
