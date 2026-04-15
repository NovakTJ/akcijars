// =============================================
//  AkcijaRS – Mock Data & Shared Helpers
// =============================================

const AKCIJE = [
  { id:1, naziv:"Čišćenje Ade Ciganlije", opis:"Pridružite nam se u akciji čišćenja i uređenja obale Ade Ciganlije. Zajedno možemo napraviti razliku za naš grad i buduće generacije! Ponesite rukavice i dobro raspoloženje – sve ostalo obezbeđujemo mi.", organizator:"Zeleni Beograd", datum:"2026-05-15", vreme:"09:00", lokacija:"Ada Ciganlija, Beograd", kategorija:"Ekologija", maxVolontera:50, prihvacenih:28, kontaktEmail:"info@zelenibeograd.rs", kontaktTelefon:"+381 11 123 4567", status:"otvorena", sponzori:["EkoFarma d.o.o.","GreenTech RS"], createdAt:"2026-04-10", lat:44.7916, lng:20.4260 },
  { id:2, naziv:"Pomoć starim licima u Zemunu", opis:"Volonteri će pomagati starim i iznemoglim licima u nabavci namirnica, lekova i uslugama u domaćinstvu na teritoriji Zemuna. Svaki sat vašeg vremena znači ogroman doprinos.", organizator:"Srce za Zemun", datum:"2026-05-20", vreme:"10:00", lokacija:"Zemun, Beograd", kategorija:"Socijalna pomoć", maxVolontera:20, prihvacenih:15, kontaktEmail:"kontakt@srcezazemun.rs", kontaktTelefon:"+381 65 987 6543", status:"otvorena", sponzori:[], createdAt:"2026-04-08", lat:44.8414, lng:20.4114 },
  { id:3, naziv:"Sadnja drveća u Zvezdara šumi", opis:"Zajedno sadimo 500 novih stabala u Zvezdara šumi. Doprinesimo zelenilu i čistom vazduhu Beograda. Organizovani autobusi polaze sa više lokacija u gradu.", organizator:"Zeleni Beograd", datum:"2026-05-28", vreme:"08:00", lokacija:"Zvezdara šuma, Beograd", kategorija:"Ekologija", maxVolontera:80, prihvacenih:40, kontaktEmail:"sadnja@zelenibeograd.rs", kontaktTelefon:"+381 11 123 4567", status:"otvorena", sponzori:["NatureSeed","BioRast d.o.o."], createdAt:"2026-04-05", lat:44.7892, lng:20.5101 },
  { id:4, naziv:"Zidna slika u Savamali", opis:"Kreiramo veliku zidnu sliku sa temom solidarnosti i zajednice u centru Savamale. Tražimo kreativne ljude svih uzrasta koji žele da ostave trag u gradu.", organizator:"Art za Sve", datum:"2026-06-05", vreme:"11:00", lokacija:"Savamala, Beograd", kategorija:"Umetnost i kultura", maxVolontera:15, prihvacenih:15, kontaktEmail:"hello@artzasve.rs", kontaktTelefon:"+381 63 555 1234", status:"popunjena", sponzori:["PaintCo Serbia"], createdAt:"2026-04-01", lat:44.8090, lng:20.4542 },
  { id:5, naziv:"Edukacija dece u Surčinu", opis:"Volonteri predaju matematiku, srpski i engleski jezik deci osnovnoškolskog uzrasta u Surčinu. Nije potrebno pedagoško iskustvo – samo entuzijazam i strpljenje.", organizator:"Znanje za Sve", datum:"2026-06-10", vreme:"14:00", lokacija:"Surčin, Beograd", kategorija:"Obrazovanje", maxVolontera:10, prihvacenih:6, kontaktEmail:"info@znanjezasve.rs", kontaktTelefon:"+381 69 111 2222", status:"otvorena", sponzori:[], createdAt:"2026-04-12", lat:44.8019, lng:20.2844 },
  { id:6, naziv:"Bazar hrane za potrebite", opis:"Organizujemo bazar na kome se skupljaju prehrambeni paketi za porodice u potrebi. Pomozite nam da paketujemo i distribuiramo hranu na Trgu Republike.", organizator:"Hrana za Sve", datum:"2026-06-15", vreme:"09:00", lokacija:"Trg Republike, Beograd", kategorija:"Humanitarne akcije", maxVolontera:35, prihvacenih:20, kontaktEmail:"bazar@hranazasve.rs", kontaktTelefon:"+381 11 456 7890", status:"otvorena", sponzori:["Mercator Srbija","Delhaize Serbia"], createdAt:"2026-04-11", lat:44.8176, lng:20.4583 },
  { id:7, naziv:"Trčanje za zdravlje Novog Sada", opis:"Humanitarna trka za prikupljanje sredstava za Dečju bolnicu u Novom Sadu. Svi prikupljeni prihodi idu direktno bolnici.", organizator:"Sport za Dobro", datum:"2026-06-20", vreme:"09:00", lokacija:"Novi Sad, Vojvodina", kategorija:"Sport i rekreacija", maxVolontera:200, prihvacenih:87, kontaktEmail:"info@sportzadobro.rs", kontaktTelefon:"+381 21 555 6789", status:"otvorena", sponzori:["Sportmaster","Aqua Viva"], createdAt:"2026-04-09", lat:45.2671, lng:19.8335 },
  { id:8, naziv:"Renoviranje doma za nezbrinutu decu", opis:"Renoviramo prostorije Doma za nezbrinutu decu 'Moša Pijade'. Tražimo volontere sa osnovnim znanjem molovanja, keramičarstva ili opštih radova.", organizator:"Ruke za Decu", datum:"2026-07-01", vreme:"08:00", lokacija:"Beograd, Voždovac", kategorija:"Socijalna pomoć", maxVolontera:25, prihvacenih:12, kontaktEmail:"info@rukezadecu.rs", kontaktTelefon:"+381 11 789 0123", status:"otvorena", sponzori:["Bauhaus Srbija"], createdAt:"2026-04-13", lat:44.7704, lng:20.4821 }
];

const CLANCI = [
  { id:1, naslov:"Uspešno završena akcija čišćenja Topčiderskog parka", sadrzaj:"Prošle subote, više od 200 volontera iz celog Beograda se okupilo u Topčiderskom parku kako bi zajedno očistili ovo omiljeno izletište Beograđana. Akcija je trajala od 9 do 14 časova, a prikupljeno je čak 2 tone smeća.\n\nOrganizatori iz udruženja Zeleni Beograd su istakli da je ovo bila jedna od njihovih najuspešnijih akcija do sada. Sponzori su obezbedili opremu za čišćenje, rukavice i osveženje za sve volontere. Mnogi učesnici su se odmah prijavili za sledeću akciju, što govori o entuzijazmu zajednice.\n\nPlanirane su još dve slične akcije u maju – u Košutnjaku i na Avali. Prijave su već otvorene na platformi AkcijaRS.", organizator:"Zeleni Beograd", datumObjave:"2026-04-08", lokacija:"Topčiderski park", kategorija:"Ekologija", komentari:[{autor:"Maja P.",tekst:"Odlična akcija, jedva čekam sledeću!",datum:"2026-04-09"},{autor:"Stefan M.",tekst:"Bilo je sjajno, preporučujem svima da se prijave.",datum:"2026-04-09"}], createdAt:"2026-04-08" },
  { id:2, naziv:"Deca iz Surčina dobila zimsku gardarobu zahvaljujući volonterima", naslov:"Deca iz Surčina dobila zimsku gardarobu zahvaljujući volonterima", sadrzaj:"Udruženje Srce za Decu je uspešno sprovelo akciju prikupljanja i distribucije zimske garderobe za decu iz socijalno ugroženih porodica u Surčinu. Zahvaljujući 45 volontera i donatorima, obezbeđeno je više od 300 komada garderobe.\n\nAkcija je trajala tri dana i obuhvatila je 85 porodica. Pored garderobe, deca su dobila i školski pribor i knjige. Organizatori planiraju nastavak u proleće sa školskim priborom.", organizator:"Srce za Decu", datumObjave:"2026-04-05", lokacija:"Surčin, Beograd", kategorija:"Socijalna pomoć", komentari:[{autor:"Ana K.",tekst:"Predivna inicijativa, svaka čast!",datum:"2026-04-06"}], createdAt:"2026-04-05" },
  { id:3, naslov:"Predstoji velika akcija sadnje u Zvezdara šumi", sadrzaj:"U narednim nedeljama, udruženje Zeleni Beograd planira veliku akciju sadnje drveća u Zvezdara šumi. Cilj je posaditi 500 novih stabala i doprineti obnovi šumskog pojasa koji je stradao u požarima.\n\nPrijave su otvorene! Sva potrebna oprema biće obezbeđena. Akcija je planirana za 28. maj.", organizator:"Zeleni Beograd", datumObjave:"2026-04-12", lokacija:"Zvezdara šuma", kategorija:"Ekologija", komentari:[], createdAt:"2026-04-12" },
  { id:4, naslov:"AkcijaRS prešla 10.000 registrovanih volontera", sadrzaj:"Platforma AkcijaRS je obeležila veliki jubilej — dostigla smo 10.000 registrovanih volontera! Od osnivanja, organizovano je više od 500 akcija u kojima je učestvovalo hiljade građana Srbije.\n\nUkupan broj volonterskih sati premašuje 150.000, što je ekvivalentno više od 17 godina rada punog radnog vremena. Ovaj uspeh je dokaz da civilno društvo u Srbiji živi i raste!", organizator:"Tim AkcijaRS", datumObjave:"2026-04-14", lokacija:"Srbija", kategorija:"Vesti", komentari:[{autor:"Luka J.",tekst:"Bravo, nastavite ovako!",datum:"2026-04-14"},{autor:"Milica D.",tekst:"Ponosna što sam deo ove zajednice.",datum:"2026-04-14"}], createdAt:"2026-04-14" }
];

const KATEGORIJE = ["Ekologija","Socijalna pomoć","Obrazovanje","Zdravlje","Humanitarne akcije","Umetnost i kultura","Sport i rekreacija","Ostalo"];

// ── Haversine distance (km) ───────────────────
function haversine(lat1, lng1, lat2, lng2) {
  const R = 6371;
  const dLat = (lat2 - lat1) * Math.PI / 180;
  const dLng = (lng2 - lng1) * Math.PI / 180;
  const a = Math.sin(dLat/2)**2 + Math.cos(lat1*Math.PI/180) * Math.cos(lat2*Math.PI/180) * Math.sin(dLng/2)**2;
  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a));
}

// ── Mock locations for autocomplete ──────────
const LOKACIJE_AUTOCOMPLETE = [
  { naziv:"Beograd, Centar",      lat:44.8176, lng:20.4569 },
  { naziv:"Beograd, Zemun",       lat:44.8414, lng:20.4114 },
  { naziv:"Beograd, Voždovac",    lat:44.7704, lng:20.4821 },
  { naziv:"Beograd, Zvezdara",    lat:44.7892, lng:20.5101 },
  { naziv:"Beograd, Novi Beograd",lat:44.8008, lng:20.4159 },
  { naziv:"Beograd, Surčin",      lat:44.8019, lng:20.2844 },
  { naziv:"Beograd, Ada Ciganlija",lat:44.7916, lng:20.4260 },
  { naziv:"Novi Sad",             lat:45.2671, lng:19.8335 },
  { naziv:"Niš",                  lat:43.3209, lng:21.8954 },
  { naziv:"Kragujevac",           lat:44.0165, lng:20.9268 },
  { naziv:"Subotica",             lat:46.1000, lng:19.6667 },
  { naziv:"Zrenjanin",            lat:45.3833, lng:20.3833 },
  { naziv:"Pančevo",              lat:44.8708, lng:20.6406 },
  { naziv:"Čačak",                lat:43.8914, lng:20.3497 },
  { naziv:"Kraljevo",             lat:43.7231, lng:20.6893 },
  { naziv:"Novi Pazar",           lat:43.1367, lng:20.5122 },
  { naziv:"Smederevo",            lat:44.6639, lng:20.9278 },
  { naziv:"Valjevo",              lat:44.2667, lng:19.8833 },
  { naziv:"Vranje",               lat:42.5500, lng:21.9000 },
  { naziv:"Šabac",                lat:44.7539, lng:19.6942 },
];

function formatDate(str) {
  if (!str) return '';
  const d = new Date(str);
  return d.toLocaleDateString('sr-Latn-RS', {day:'numeric', month:'long', year:'numeric'});
}

function formatDateShort(str) {
  if (!str) return '';
  const d = new Date(str);
  return d.toLocaleDateString('sr-Latn-RS', {day:'numeric', month:'short'});
}

function getStatusBadge(status) {
  const map = {
    otvorena: '<span class="badge badge-green"><i class="bi bi-check-circle-fill"></i> Otvorena</span>',
    popunjena: '<span class="badge badge-warning"><i class="bi bi-people-fill"></i> Popunjena</span>',
    otkazana: '<span class="badge badge-error"><i class="bi bi-x-circle-fill"></i> Otkazana</span>',
    zavrsena: '<span class="badge badge-gray"><i class="bi bi-flag-fill"></i> Završena</span>',
  };
  return map[status] || '';
}

function getKategorijaBadge(kat) {
  return `<span class="badge badge-teal">${getCategoryEmoji(kat)} ${kat}</span>`;
}

function getCategoryGradient(kat) {
  const g = {
    'Ekologija':'linear-gradient(135deg,#c8f0d8,#a8e4c0)',
    'Socijalna pomoć':'linear-gradient(135deg,#c8dff0,#a8cce4)',
    'Obrazovanje':'linear-gradient(135deg,#f0ebc8,#e4d8a8)',
    'Zdravlje':'linear-gradient(135deg,#f0c8c8,#e4a8a8)',
    'Humanitarne akcije':'linear-gradient(135deg,#f0c8e8,#e4a8d4)',
    'Umetnost i kultura':'linear-gradient(135deg,#e4c8f0,#d4a8e4)',
    'Sport i rekreacija':'linear-gradient(135deg,#c8ecf0,#a8d8e4)',
    'Vesti':'linear-gradient(135deg,#f0e4c8,#e4d0a8)',
  };
  return g[kat] || 'linear-gradient(135deg,var(--teal-light),var(--green-light))';
}

function getCategoryEmoji(kat) {
  const e = {
    'Ekologija':'🌿','Socijalna pomoć':'🤝','Obrazovanje':'📚',
    'Zdravlje':'❤️','Humanitarne akcije':'🍽️','Umetnost i kultura':'🎨',
    'Sport i rekreacija':'⚽','Vesti':'📰',
  };
  return e[kat] || '✨';
}

function progressWidth(prihvacenih, max) {
  return Math.min(100, Math.round((prihvacenih / max) * 100));
}

// ── Auth simulation ───────────────────────────

const AUTH = {
  isLoggedIn: () => !!localStorage.getItem('akcijars_user'),
  getUser:    () => JSON.parse(localStorage.getItem('akcijars_user') || 'null'),
  login:  (u)    => localStorage.setItem('akcijars_user', JSON.stringify(u)),
  logout:        () => localStorage.removeItem('akcijars_user'),
};

function getDashboardLink(uloga) {
  return { volonter:'volonter-panel.html', organizator:'organizator-panel.html', sponzor:'sponzor-panel.html', admin:'admin-panel.html' }[uloga] || '#';
}

function updateNavbar() {
  const el = document.getElementById('nav-auth');
  const mob = document.getElementById('nav-mobile-auth');
  if (!el) return;

  let authHtml;
  if (AUTH.isLoggedIn()) {
    const u = AUTH.getUser();
    authHtml = `
      <span style="font-size:.85rem;color:var(--text-secondary);font-weight:500;display:flex;align-items:center;gap:5px;">
        <i class="bi bi-person-circle" style="color:var(--teal);"></i> ${u.ime}
      </span>
      <a href="${getDashboardLink(u.uloga)}" class="btn btn-secondary btn-sm">Moj nalog</a>
      <button onclick="AUTH.logout();location.href='index.html';" class="btn btn-ghost btn-sm">Odjavi se</button>`;
  } else {
    authHtml = `
      <a href="prijava.html" class="btn btn-ghost btn-sm">Prijavi se</a>
      <a href="registracija.html" class="btn btn-primary btn-sm">Registruj se</a>`;
  }

  el.innerHTML = authHtml;
  if (mob) mob.innerHTML = authHtml;
}

function toggleMobileMenu() {
  const drawer = document.getElementById('nav-mobile-drawer');
  const btn    = document.getElementById('nav-hamburger');
  if (!drawer) return;
  const isOpen = drawer.classList.toggle('open');
  btn.classList.toggle('open', isOpen);
  // refresh mobile auth content on open
  if (isOpen) updateNavbar();
}

// Close mobile drawer on outside click
document.addEventListener('click', e => {
  const drawer = document.getElementById('nav-mobile-drawer');
  const btn    = document.getElementById('nav-hamburger');
  if (!drawer || !drawer.classList.contains('open')) return;
  if (!drawer.contains(e.target) && !btn.contains(e.target)) {
    drawer.classList.remove('open');
    btn.classList.remove('open');
  }
});

// ── Navbar scroll effect ──────────────────────
document.addEventListener('DOMContentLoaded', () => {
  const nb = document.getElementById('navbar');
  if (nb) {
    window.addEventListener('scroll', () => nb.classList.toggle('scrolled', scrollY > 20));
  }
  updateNavbar();
});

// ── Shared navbar HTML ────────────────────────
function renderNavbar(activePage) {
  const pages = [
    {href:'index.html',  label:'Početna', key:'home'},
    {href:'akcije.html', label:'Akcije',  key:'akcije'},
    {href:'clanci.html', label:'Članci',  key:'clanci'},
  ];
  const linksHtml = pages.map(p =>
    `<a href="${p.href}" class="nav-link${activePage===p.key?' active':''}">${p.label}</a>`
  ).join('');

  return `
  <nav class="navbar" id="navbar">
    <div class="container">
      <div class="nav-inner">
        <a href="index.html" class="nav-logo">
          <img src="logo.png" alt="AkcijaRS logo" style="height:46px;width:auto;object-fit:contain;">
        </a>
        <div class="nav-links">${linksHtml}</div>
        <div class="nav-auth" id="nav-auth"></div>
        <!-- Hamburger -->
        <button class="nav-hamburger" id="nav-hamburger" onclick="toggleMobileMenu()" aria-label="Meni">
          <span></span><span></span><span></span>
        </button>
      </div>
    </div>
  </nav>
  <!-- Mobile drawer -->
  <div class="nav-mobile-drawer" id="nav-mobile-drawer">
    <div class="nav-mobile-links">
      ${pages.map(p=>`<a href="${p.href}" class="${activePage===p.key?'active':''}">${p.label}</a>`).join('')}
    </div>
    <div class="nav-mobile-auth" id="nav-mobile-auth"></div>
  </div>`;
}

function renderFooter() {
  return `
  <footer>
    <div class="container">
      <div class="footer-inner">
        <div class="footer-brand">
          <div class="nav-logo">
            <img src="logo.png" alt="AkcijaRS logo" style="height:36px;width:auto;object-fit:contain;filter:brightness(0) invert(1);opacity:.85;">
          </div>
          <p>Jedinstvena platforma za volonterske akcije u Srbiji. Zajedno gradimo bolju zajednicu.</p>
        </div>
        <div class="footer-col">
          <h4>Navigacija</h4>
          <ul>
            <li><a href="index.html">Početna</a></li>
            <li><a href="akcije.html">Akcije</a></li>
            <li><a href="clanci.html">Članci</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Nalog</h4>
          <ul>
            <li><a href="prijava.html">Prijava</a></li>
            <li><a href="registracija.html">Registracija</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <span>© 2026 AkcijaRS – Tim VolonTech</span>
        <span>ETF Beograd · SI3PSI</span>
      </div>
    </div>
  </footer>`;
}
