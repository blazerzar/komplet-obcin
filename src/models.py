import genanki

OBCINA_MODEL_ID = 1872843919

obcina_model = genanki.Model(
    OBCINA_MODEL_ID,
    'Občina',
    fields=[
        {'name': 'Ime'},
        {'name': 'Zemljevid'},
        {'name': 'ZemljevidPrazen'},
    ],
    templates=[
        {
            'name': 'Zemljevid → ime',
            'qfmt': 'Katera občina je to?{{Zemljevid}}',
            'afmt': '{{FrontSide}}<hr id=answer><b>{{Ime}}</b>',
        },
        {
            'name': 'Ime → zemljevid',
            'qfmt': 'Kje je občina <b>{{Ime}}</b>?{{ZemljevidPrazen}}',
            'afmt': 'Kje je občina <b>{{Ime}}</b>?{{Zemljevid}}',
        },
    ],
    css='.card{font-family:sans-serif;text-align:center;font-size:20px}'
    'img{display:block;margin:1em auto 0;max-width:100%;max-height:60vh}',
)
