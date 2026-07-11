// Autor: Novak Stijepic 0124/2023
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
    if (!input || !google.maps.places || !google.maps.places.Autocomplete) return null;

    // Legacy Places Autocomplete nije dostupan novim Google nalozima (od 1.3.2025).
    // Ako padne, vraćamo null — ostatak (mapa, ručni unos) i dalje radi.
    var autocomplete;
    try {
      autocomplete = new google.maps.places.Autocomplete(input, {
        componentRestrictions: { country: 'rs' },
        fields: ['geometry', 'name', 'formatted_address'],
      });
    } catch (e) {
      return null;
    }

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

    var latInput = document.getElementById('id_geo_sirina');
    var lngInput = document.getElementById('id_geo_duzina');
    var mapEl = document.getElementById('lokacija-mapa');

    // Bez kontejnera za mapu (npr. ključ nije postavljen) — samo autocomplete.
    if (!mapEl || !google.maps.places) {
      veziAutocomplete(input, latInput, lngInput);
      return;
    }

    // Već inicijalizovano (ponovni poziv posle promene taba) — samo osveži
    // veličinu (mapa u sakrivenom div-u se iscrta sivo dok se ne prikaže) i
    // recentriraj na marker.
    if (mapEl._picker) {
      var p = mapEl._picker;
      google.maps.event.trigger(p.mapa, 'resize');
      p.mapa.setCenter(p.marker.getVisible() ? p.marker.getPosition() : CENTAR_RS);
      return;
    }

    var pocetna = CENTAR_RS;
    var imaKoord = false;
    var lat0 = parseFloat(mapEl.dataset.lat);
    var lng0 = parseFloat(mapEl.dataset.lng);
    if (!isNaN(lat0) && !isNaN(lng0)) {
      pocetna = { lat: lat0, lng: lng0 };
      imaKoord = true;
    }

    var mapa = new google.maps.Map(mapEl, {
      center: pocetna,
      zoom: imaKoord ? 14 : 7,
      mapTypeControl: false,
      streetViewControl: false,
    });
    var marker = new google.maps.Marker({
      map: mapa,
      draggable: true,
      position: pocetna,
      visible: imaKoord,
    });
    var geocoder = new google.maps.Geocoder();

    // Pamtimo poslednji „potvrđeni" tekst (iz predloga ili geokodiranja) da bismo
    // razlikovali stvarnu izmenu od izbora — koordinate brišemo samo ako se tekst
    // zaista promeni (ranije su se brisale na svaki pritisak tastera).
    input.dataset.lastText = imaKoord ? input.value : '';

    function postaviLokaciju(pos, azurirajTekst) {
      marker.setPosition(pos);
      marker.setVisible(true);
      mapa.panTo(pos);
      if (mapa.getZoom() < 13) mapa.setZoom(14);
      if (latInput) latInput.value = pos.lat;
      if (lngInput) lngInput.value = pos.lng;
      if (azurirajTekst) {
        // Klik/prevlačenje: dopuni čitljiv naziv (reverse geocoding), pa označi
        // dobijeni tekst kao potvrđen.
        geocoder.geocode({ location: pos }, function (rezultati, status) {
          if (status === 'OK' && rezultati[0]) {
            input.value = rezultati[0].formatted_address;
          }
          input.dataset.lastText = input.value;
        });
      } else {
        input.dataset.lastText = input.value;
      }
    }

    // Legacy Places Autocomplete nije dostupan novim Google nalozima (od 1.3.2025).
    // Ako padne, mapa + klik/prevlačenje markera i dalje rade (SSU 5).
    try {
      var autocomplete = new google.maps.places.Autocomplete(input, {
        componentRestrictions: { country: 'rs' },
        fields: ['geometry', 'name', 'formatted_address'],
      });
      autocomplete.addListener('place_changed', function () {
        var place = autocomplete.getPlace();
        if (place && place.geometry && place.geometry.location) {
          postaviLokaciju(
            { lat: place.geometry.location.lat(), lng: place.geometry.location.lng() },
            false
          );
        }
      });
    } catch (e) { /* autocomplete nedostupan — nastavljamo bez njega */ }

    // Izbor lokacije klikom na mapu ili prevlačenjem markera (SSU 5 — biranje
    // lokacije preko Google Maps prozorčića).
    mapa.addListener('click', function (e) {
      postaviLokaciju({ lat: e.latLng.lat(), lng: e.latLng.lng() }, true);
    });
    marker.addListener('dragend', function (e) {
      postaviLokaciju({ lat: e.latLng.lat(), lng: e.latLng.lng() }, true);
    });

    // Ručna izmena teksta bez izbora predloga → koordinate više ne odgovaraju
    // unosu; brišemo ih samo ako se tekst STVARNO razlikuje od potvrđenog.
    input.addEventListener('input', function () {
      if (input.value === input.dataset.lastText) return;
      if (latInput) latInput.value = '';
      if (lngInput) lngInput.value = '';
      marker.setVisible(false);
    });

    mapEl._picker = { mapa: mapa, marker: marker };
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

  // Ponovna inicijalizacija picker mape kada se forma za izmenu prikaže (promena
  // taba) ili zameni novim fragmentom posle AJAX čuvanja (SSU 10). Bezbedno je
  // pozvati i pre nego što se Google Maps učita.
  window.reinicijalizujMapuFormu = function () {
    if (typeof google === 'undefined' || !google.maps) return;
    inicijalizujFormuAkcije();
  };
})();
