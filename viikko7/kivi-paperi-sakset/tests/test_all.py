import os
import sys
import pathlib

# ensure src is importable
ROOT = pathlib.Path(__file__).resolve().parent.parent
SRC = str(ROOT / "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from tuomari import Tuomari
from tekoaly import Tekoaly
from tekoaly_parannettu import TekoalyParannettu

from flask import url_for
import web


def test_tuomari_scoring():
    t = Tuomari()
    t.kirjaa_siirto('k', 's')  # eka wins
    t.kirjaa_siirto('p', 'k')  # eka wins
    t.kirjaa_siirto('s', 's')  # tie
    t.kirjaa_siirto('k', 'p')  # toka wins

    assert t.ekan_pisteet == 2
    assert t.tokan_pisteet == 1
    assert t.tasapelit == 1
    s = str(t)
    assert 'Pelitilanne' in s
    assert 'Tasapelit' in s


def test_tekoaly_cycle():
    a = Tekoaly()
    # According to implementation first call returns 'p', then 's', then 'k'
    assert a.anna_siirto() == 'p'
    assert a.anna_siirto() == 's'
    assert a.anna_siirto() == 'k'
    assert a.anna_siirto() == 'p'


def test_tekoaly_parannettu_basic():
    ta = TekoalyParannettu(3)
    # with empty or single memory, anna_siirto should return 'k'
    assert ta.anna_siirto() == 'k'
    ta.aseta_siirto('k')
    assert ta.anna_siirto() == 'k'


def test_flask_index_and_play():
    app = web.app
    client = app.test_client()

    # index page
    r = client.get('/')
    assert r.status_code == 200
    assert b'Kivi-paperi-sakset' in r.data

    # start a game vs AI (b)
    r = client.post('/start', data={'tyyppi': 'b'}, follow_redirects=False)
    assert r.status_code in (302, 303)
    location = r.headers.get('Location')
    assert location is not None
    assert '/play/' in location

    # play one round against AI
    r2 = client.post(location, data={'eka': 'k'}, follow_redirects=True)
    assert r2.status_code == 200
    assert b'Pelitilanne' in r2.data or b'Viimeisin siirto' in r2.data

    # start PvP
    r3 = client.post('/start', data={'tyyppi': 'a'}, follow_redirects=False)
    assert r3.status_code in (302, 303)
    loc2 = r3.headers.get('Location')
    # play PvP round
    r4 = client.post(loc2, data={'eka': 'k', 'toka': 'p'}, follow_redirects=True)
    assert r4.status_code == 200
    assert b'Historia' in r4.data
    assert b'k - p' in r4.data


def test_flask_play_until_winner_against_ai():
    app = web.app
    client = app.test_client()

    # start a game vs basic AI (b)
    r = client.post('/start', data={'tyyppi': 'b'}, follow_redirects=False)
    assert r.status_code in (302, 303)
    location = r.headers.get('Location')
    assert location and '/play/' in location

    # play until someone reaches 5 wins
    r_current = None
    for i in range(10):
        r_current = client.post(location, data={'eka': 'k'}, follow_redirects=True)
        assert r_current.status_code == 200
        if b'Peli on p' in r_current.data or b'Voittaja' in r_current.data:
            break

    assert r_current is not None
    assert b'Pelitilanne' in r_current.data


def test_flask_play_until_winner_pvp():
    app = web.app
    client = app.test_client()

    # start PvP
    r = client.post('/start', data={'tyyppi': 'a'}, follow_redirects=False)
    assert r.status_code in (302, 303)
    loc = r.headers.get('Location')

    # Play rounds where first player wins until first reaches 5
    for i in range(5):
        r2 = client.post(loc, data={'eka': 'k', 'toka': 's'}, follow_redirects=True)
        assert r2.status_code == 200

    # After five wins, the page should report game finished
    r_final = client.get(loc)
    # ensure winner marker is present
    assert b'Voittaja' in r_final.data
