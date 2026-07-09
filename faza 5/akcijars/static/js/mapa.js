// ── Google Maps integracija (FZ 4.3.1) ─────────────────────────────────────
//
// `window.initMape` je callback koji Google Maps JS API pozove kad se učita
// (vidi templates/_maps_script.html). Na osnovu toga šta postoji na stranici
// granamo ponašanje:
//   • #akcija-mapa      → prikaz markera na detalju akcije (data-lat/lng).
//   • #lokacija-input   → Places Autocomplete pri kreiranju akcije; puni
//                         skrivena polja geo_sirina/geo_duzina.
//   • #lok-input        → Places Autocomplete + „Moja lokacija" na listi akcija;
//                         puni skrivena polja lat/lng za pretragu po radijusu.
//
// Bez inline JS-a u template-ima; svi podaci se prenose preko data-* atributa.

(function () {
  'use strict';

  // Centriramo autocomplete i podrazumevani pogled na Srbiju.
  var CENTAR_RS = { lat: 44.0165, lng: 21.0059 };

  function inicijalizujDetaljMapu() {
    var el = document.getElementById('akcija-mapa');
    if (!el) return;

    var lat = parseFloat(el.dataset.lat);
    var lng = parseFloat(el.dataset.lng);
    if (isNaN(lat) || isNaN(lng)) return;

    var pozicija = { lat: lat, lng: lng };
    var mapa = new google.maps.Map(el, {
      center: pozicija,
      zoom: 14,
      mapTypeControl: false,
      streetViewControl: false,
    });
    new google.maps.Marker({
      position: pozicija,
      map: mapa,
      title: el.dataset.naziv || '',
    });
  }

  // Vezuje Places Autocomplete na tekstualno polje i, po izboru mesta, upisuje
  // koordinate u zadata skrivena polja (po id-u). Ograničeno na Srbiju.
  function veziAutocomplete(input, latInput, lngInput) {
    if (!input || !google.maps.places) return null;

    var autocomplete = new google.maps.places.Autocomplete(input, {
      componentRestrictions: { country: 'rs' },
      fields: ['geometry', 'name', 'formatted_address'],
    });

    autocomplete.addListener('place_changed', function () {
      var place = autocomplete.getPlace();
      if (place && place.geometry && place.geometry.location) {
        if (latInput) latInput.value = place.geometry.location.lat();
        if (lngInput) lngInput.value = place.geometry.location.lng();
      }
    });

    // Ako korisnik ručno izmeni tekst bez izbora predloga, koordinate više ne
    // odgovaraju unosu → brišemo ih (akcija/pretraga bez koordinata je validna).
    input.addEventListener('input', function () {
      if (latInput) latInput.value = '';
      if (lngInput) lngInput.value = '';
    });

    return autocomplete;
  }

  function inicijalizujFormuAkcije() {
    var input = document.getElementById('id_lokacija');
    if (!input) return;
    veziAutocomplete(
      input,
      document.getElementById('id_geo_sirina'),
      document.getElementById('id_geo_duzina')
    );
  }

  function inicijalizujPretraguPoLokaciji() {
    var input = document.getElementById('lok-input');
    if (!input) return;

    var latInput = document.getElementById('lok-lat');
    var lngInput = document.getElementById('lok-lng');
    veziAutocomplete(input, latInput, lngInput);

    // „Moja lokacija" — koristi browser Geolocation API i pokreće pretragu.
    var dugme = document.getElementById('moja-lokacija');
    if (dugme && navigator.geolocation) {
      dugme.addEventListener('click', function () {
        dugme.disabled = true;
        navigator.geolocation.getCurrentPosition(
          function (pos) {
            if (latInput) latInput.value = pos.coords.latitude;
            if (lngInput) lngInput.value = pos.coords.longitude;
            if (input) input.value = 'Moja lokacija';
            dugme.disabled = false;
            // Pokreni AJAX filtriranje iz akcije.js (submit forme).
            var forma = document.getElementById('filter-form');
            if (forma) {
              forma.dispatchEvent(new Event('submit', { cancelable: true }));
            }
          },
          function () {
            dugme.disabled = false;
            alert('Nije moguće očitati vašu lokaciju.');
          }
        );
      });
    }
  }

  window.initMape = function () {
    inicijalizujDetaljMapu();
    inicijalizujFormuAkcije();
    inicijalizujPretraguPoLokaciji();
  };
})();
