import os
from zlib import crc32

import genanki
import geopandas
import matplotlib.pyplot as plt
import shapely

from models import obcina_model

BASE_URL = (
    'https://geohub.gov.si/ags/rest/services/TEMELJNE_VSEBINE/'
    'GH_Prostorske_enote/MapServer'
)
REGIJE, OBCINE = 1520, 1530
NAME_COL = 'NAZIV'
SLOVENE_COORDINATE_SYSTEM = 3794

BUILD_DIR = 'build'


def main():
    if not os.path.exists(BUILD_DIR):
        os.mkdir(BUILD_DIR)

    regije = layer(REGIJE)
    obcine = layer(OBCINE)
    print(f'Loaded {len(regije)} regions')
    print(f'Loaded {len(obcine)} municipalities')

    obcine['regija'] = compute_municipality_regions(obcine, regije)

    create_municipalities_deck(obcine, os.path.join(BUILD_DIR, 'obcine.apkg'))


def layer(layer_id):
    """Download layer as GeoDataFrame in Slovene coordinate system (D96/TM)."""
    url = (
        f'{BASE_URL}/{layer_id}/query?where=1%3D1&outFields=*'
        f'&returnGeometry=true&outSR=4326&f=geojson'
    )
    gdf = geopandas.read_file(url)
    gdf = gdf.to_crs(SLOVENE_COORDINATE_SYSTEM)
    gdf = gdf[['NAZIV', 'geometry']]
    return gdf


def compute_municipality_regions(obcine, regije):
    """Compute and return a region for each municipality."""
    points = geopandas.GeoDataFrame(
        obcine[NAME_COL], geometry=obcine.representative_point(), crs=obcine.crs
    )
    points = geopandas.sjoin(
        points,
        regije[[NAME_COL, 'geometry']].rename(columns={NAME_COL: 'regija'}),
        predicate='within',
        how='left',
    ).drop(columns='index_right')
    return points['regija']


def municipalities_plot(obcine, file_name, marked=None):
    """Create a plot of all municipalities and mark one if provided."""
    C = dict(land='#FAF3EB', inner='#E3D5C6', border='#8A7866', hi='#A6D5F7')

    slovenija = obcine.dissolve()
    slovenija['geometry'] = shapely.polygons(slovenija.geometry.exterior)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.set_axis_off()

    slovenija.plot(ax=ax, color=C['land'])
    obcine.plot(ax=ax, color='none', edgecolor=C['inner'], linewidth=0.5)
    if marked is not None:
        obcine.loc[[marked]].plot(
            ax=ax, color=C['hi'], edgecolor=C['border'], linewidth=0.6
        )
    slovenija.plot(ax=ax, color='none', edgecolor=C['border'], linewidth=1.0)

    file_path = os.path.join(BUILD_DIR, file_name)
    fig.savefig(file_path, dpi=250, bbox_inches='tight')
    plt.close(fig)
    return file_path


def create_municipalities_deck(obcine, out_file):
    """Create the final municipalities deck with subdecks for each region."""
    decks = [
        genanki.Deck(
            crc32('Občine'.encode()),
            'Občine',
            description='Slovenske občine po regijah',
        ),
    ]
    media_files = [municipalities_plot(obcine, 'obcine_blank.png')]

    for regija, o in obcine.groupby('regija'):
        deck = genanki.Deck(crc32(regija.encode('utf-8')), f'Občine::{regija}')
        decks.append(deck)

        for i, obcina in o.iterrows():
            name = obcina[NAME_COL]
            img = f'obcina_{name}.png'
            media_files.append(municipalities_plot(obcine, img, i))

            deck.add_note(
                genanki.Note(
                    obcina_model,
                    fields=[
                        name,
                        f'<img src="{img}">',
                        '<img src="obcine_blank.png">',
                    ],
                    guid=genanki.guid_for('obcine', name),
                )
            )

        print(f'Completed {regija}')

    package = genanki.Package(decks)
    package.media_files = media_files
    package.write_to_file(out_file)


if __name__ == '__main__':
    main()
