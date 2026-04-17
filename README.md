# Elpako Problema

Autorius: Tadas Sasnauskas <tadas@yoyo.lt>

Aprašas: [REPORT.md](report/REPORT.md)

# "Proof of concept" demonstracinė piktavalė sistema

Komponentai:
  - Serveryje veikianti programa "forwarder" su mini svetaine.
    Žiūr: `src/elpako_issue/forwarder`
  - Programišiaus kompiuteryje veikianti programa "signer", apsimetanti
    Elpako. Šaukiniai persiunčiami į "forwarder".
    Žiūr: `src/elpako_issue/signer`
  - Programišiaus naršyklės konsolėje, esant https://api.elpako.lt prisijungimo
    puslapyje, reikalingas Javascript fragmentas laukiantis vartotojo prisijungimo:
    ```javascript
    fetch('https://127.0.0.1:38888/wait_for_the_visitor').then(function(response) {
      if (response.status == 200) { startAuthentication(); }
    });
    ```

Demonstracijos įrašas bus paskelbtas atskirai.
