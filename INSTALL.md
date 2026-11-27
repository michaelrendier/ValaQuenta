# Installing ValaQuenta

See the repository README. Use the `.venv`, never the system Python.

<!-- system-software:begin -->
## System software (not Python)

Programs this repository's own files call, found by scanning its source (`ValaQuenta/tools/repo_venv.py`). Install them with the system package manager; they are not pip packages.

| software | command | here | install |
|---|---|---|---|
| Blender (renders, headless `blender -b -P`) | `blender` | installed | `sudo apt install blender` |
| FFmpeg (audio/video) | `ffmpeg` | installed | `sudo apt install ffmpeg` |
| ImageMagick (`convert`, `montage`) | `convert` | installed | `sudo apt install imagemagick` |
| librsvg (`rsvg-convert`, SVG to PNG) | `rsvg-convert` | installed | `sudo apt install librsvg2-bin` |
| Firefox (headless screenshots, viewing the galleries) | `firefox` | installed | `sudo apt install firefox` |
| eSpeak (speech) | `espeak` | installed | `sudo apt install espeak` |
| SoX (audio) | `sox` | installed | `sudo apt install sox` |
| OpenSCAD (3D models) | `openscad` | installed | `sudo apt install openscad` |
| poppler-utils (PDF text and images) | `pdftotext` | installed | `sudo apt install poppler-utils` |
| TeX Live (papers) | `pdflatex` | installed | `sudo apt install texlive-latex-extra` |
| Pandoc | `pandoc` | installed | `sudo apt install pandoc` |
| a C compiler (gcc, make) for the C code | `gcc` | installed | `sudo apt install build-essential` |
| git | `git` | installed | `sudo apt install git` |
| curl | `curl` | installed | `sudo apt install curl` |
| Jupyter (installed in the .venv by pip; notebooks are executed with nbconvert) | `jupyter` | installed | pip (in the .venv) |
<!-- system-software:end -->
