# heicToJpg

Converts HEIC/HEIF photos (e.g. from an iPhone) to JPG. It applies rotation and keeps the EXIF metadata (date taken, GPS, camera) and the color profile.

## Setup

```sh
git clone https://github.com/Merkaban/heicToJpg.git
cd heicToJpg
python -m venv .venv          # use python3 if python isn't available (3.9+)
```

Activate the venv:

- macOS/Linux: `source .venv/bin/activate`
- Windows (PowerShell): `.venv\Scripts\Activate.ps1`

Then install the dependencies:

```sh
pip install -r requirements.txt
```

## Usage

```sh
python heic_to_jpg.py photo.heic                 # single file
python heic_to_jpg.py ~/Pictures/iphone          # every .heic in a folder
python heic_to_jpg.py ~/Pictures -r              # include subfolders
python heic_to_jpg.py ~/Pictures -o ~/converted  # write JPGs to another folder
python heic_to_jpg.py ~/Pictures -q 85 --delete  # lower quality, remove originals
```

By default, JPGs are saved next to the originals and existing JPGs are skipped.

## Options

| Option | Description |
|---|---|
| `-r`, `--recursive` | Include subfolders |
| `-o`, `--output DIR` | Write JPGs to `DIR`, keeping the folder structure (default: next to the originals) |
| `-q`, `--quality N` | JPEG quality 1–95 (default 92) |
| `--overwrite` | Replace existing JPGs instead of skipping them |
| `--delete` | Delete each HEIC file after it converts successfully |
