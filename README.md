<div align="center">

# 🐔 Komplet Občin

**Anki deck for learning all 212 Slovene municipalities**

[![Latest release](https://img.shields.io/github/v/release/blazerzar/komplet-obcin?label=deck)](https://github.com/blazerzar/komplet-obcin/releases/latest)
[![Release workflow](https://github.com/blazerzar/komplet-obcin/actions/workflows/release.yml/badge.svg)](https://github.com/blazerzar/komplet-obcin/actions/workflows/release.yml)
[![License](https://img.shields.io/github/license/blazerzar/komplet-obcin)](LICENSE)

<img
  src="https://www.gov.si/assets/ministrstva/MNZJU/MJU/Lokalna-samouprava/Zemljevid-obcin-Slovenije-v2__FitMaxWzIwMDAsMjAwMCwiZDVmMTM2ZjdhZSJd.jpg"
  alt="Map of Slovene municipalities"
  width="600"
/>

<sub>Map: [Občine v številkah](https://www.gov.si/teme/obcine-v-stevilkah/)</sub>

</div>

## About

The deck contains one note per municipality, split into subdecks by
statistical region (`Občine::<regija>`). Each note produces two cards:

- **Zemljevid → ime**: the map with the municipality highlighted; name it.
- **Ime → zemljevid**: the municipality's name; find it on a blank map.

Download the latest `obcine.apkg` from
[Releases](https://github.com/blazerzar/komplet-obcin/releases) and import it
into Anki. A CSV list of municipalities with their regions (`obcine.csv`) is
published alongside it.

## Setup

The project uses [mise](https://mise.jdx.dev/) for tools and
[uv](https://docs.astral.sh/uv/) for Python dependencies.

```sh
mise install
mise run setup  # uv sync + install git hooks
```

Lint with `mise run lint` and auto-fix with `mise run fix`.

## Building

```sh
uv run python src/main.py
```

This downloads the data, renders a map for each municipality and writes the
outputs to `build/`:

- `build/obcine.apkg` – the Anki deck with all images,
- `build/obcine.csv` – municipality names and regions.

Pushing a `v*` tag runs the release workflow, which builds the deck and attaches
both files to a GitHub release.

## Data

Municipality and region boundaries are downloaded from the
[GeoHub](https://geohub.gov.si/) spatial units service
(`TEMELJNE_VSEBINE/GH_Prostorske_enote`, layers for statistical regions and
municipalities) of the Surveying and Mapping Authority of the Republic of
Slovenia. Geometries are projected to the Slovene D96/TM coordinate system
(EPSG:3794), and each municipality is assigned to the region containing its
representative point.
