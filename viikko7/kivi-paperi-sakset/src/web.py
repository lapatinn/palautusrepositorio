from flask import Flask, render_template, request, redirect, url_for
import uuid

from tuomari import Tuomari
from kps import KiviPaperiSakset

app = Flask(__name__)

# Simple in-memory session store for local development
SESSIONS = {}

class GameSession:
    def __init__(self, tyyppi):
        self.tyyppi = tyyppi
        self.tuomari = Tuomari()
        # luo_peli palauttaa aliluokan joka sisältää mahdollisen tekoälyn
        self.peli = KiviPaperiSakset.luo_peli(tyyppi)
        self.history = []
        self.finished = False
        self.winner = None

    def _check_finished(self):
        if self.tuomari.ekan_pisteet >= 3:
            self.finished = True
            self.winner = 'Ensimmäinen pelaaja'
        elif self.tuomari.tokan_pisteet >= 3:
            self.finished = True
            self.winner = 'Toinen pelaaja'

    def play_round(self, ekan_siirto, tokan_siirto=None):
        if self.finished:
            return None

        if self.tyyppi == "a":
            # Pelaaja vs pelaaja: molemmat siirrot annetaan
            self.tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            self.history.append((ekan_siirto, tokan_siirto))
            self._check_finished()
            return tokan_siirto
        else:
            # AI vastustaja: käytetään olemassaolevan peliluokan metodia
            tokan_siirto = self.peli._toisen_siirto(ekan_siirto)
            self.tuomari.kirjaa_siirto(ekan_siirto, tokan_siirto)
            self.history.append((ekan_siirto, tokan_siirto))
            self._check_finished()
            return tokan_siirto


@app.route("/", methods=["GET"]) 
def index():
    return render_template("index.html")


@app.route("/start", methods=["POST"]) 
def start():
    tyyppi = request.form.get("tyyppi")
    if tyyppi not in ("a", "b", "c"):
        return redirect(url_for("index"))

    sid = str(uuid.uuid4())
    SESSIONS[sid] = GameSession(tyyppi)
    return redirect(url_for("play", sid=sid))


@app.route("/play/<sid>", methods=["GET", "POST"]) 
def play(sid):
    session = SESSIONS.get(sid)
    if not session:
        return "Istuntoa ei löytynyt", 404

    last = None

    if request.method == "POST":
        # if game already finished, don't accept new moves
        if session.finished:
            # älä aseta messagea tässä — template näyttää voittajan finished/winner-arvoilla
            pass
        else:
            if session.tyyppi == "a":
                eka = request.form.get("eka")
                toka = request.form.get("toka")

                if not _onko_ok_siirto(eka) or not _onko_ok_siirto(toka):
                    # virheellinen siirto — älä näytä erillistä virheviestiä
                    last = None
                else:
                    session.play_round(eka, toka)
                    last = (eka, toka)
                    # ei aseteta messagea pelin päättymisestä täällä — template huolehtii siitä
            else:
                eka = request.form.get("eka")
                if not _onko_ok_siirto(eka):
                    # virheellinen siirto — älä näytä erillistä virheviestiä
                    last = None
                else:
                    toka = session.play_round(eka)
                    last = (eka, toka)
                    # ei aseteta messagea pelin päättymisestä täällä — template huolehtii siitä

    return render_template(
        "play.html",
        sid=sid,
        tyyppi=session.tyyppi,
        tuomari=str(session.tuomari),
        history=session.history,
        last=last,
        winner=session.winner,
        finished=session.finished,
    )


def _onko_ok_siirto(siirto):
    return siirto in ("k", "p", "s")


if __name__ == "__main__":
    # app.debug = True
    app.run(host="127.0.0.1", port=5000)
