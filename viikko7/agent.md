Agentti päätyi toimivaan ratkaisuun. Varmistuin toimivuudesta agentin laatimilla testeillä ja kokeilemalla sovellusta itse. Olen ihan varma että ratkaisu toimii oikein. 

Jouduin ohjeistamaan agenttia melkeinpä jokaisen promptin jälkeen. Agentilla oli vaikeuksia ymmärtää miten poetry projekteja suoritetaan terminaalista, se yritti jatkuvasti ajaa komentoja ilman virtuaaliympäristöä ja asentaa riippuvuuksia pipillä. Agentti ei myöskään osannut asettaa poetrylle riippuvuuksia. 

Agentin testit ovat suhteellisen ok. Ne testaavat Tuomari, Tekoaly ja TekoalyParannettu luokkien palauttamia arvoja, sekä varsinaisen käytöliittymän toiminnallisuutta. Agentin tekemä koodi on ehkä hieman sekavaa, jouduin kyselemään esimerkiksi sid:n käytöstä, enkä rehellisesti ihan ymmärtänyt agentin vastauksen perusteella mistä on kyse. Agentti ei koskenut edellisessä tehtävässä tekemääni koodiin. 

Opin, että tietyissä tapauksissa agentin käyttö voi nopeuttaa huomattavasti joidenkin toimminallisuuksien lisäämsitä omiin projekteihin, mutta tämä edellyttää sen, että pohjakoodi on toteutettu siten, että sen päälle voi rakentaa uutta toiminnallisuutta mahdollisimman vähäisillä muutoksilla. On myös tärkeää käydä huolellisesti läpi agentin tuottama koodi ja valittava tarkkaan ne ominaisuudet, joiden toteuttamisen kehtaa ulkoistaa agentille. 
