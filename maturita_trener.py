import streamlit as st
import random
import re

# Kompletní databáze 20 literárních děl pro maturitu z českého jazyka
WORKS = [
    {
        "id": 1,
        "author": "Molière[cite: 5]",
        "title": "Lakomec[cite: 5]",
        "movement": "Klasicismus · 17. stol. · Francie[cite: 5]",
        "authorInfo": "Jean-Baptiste Poquelin (1622–1673) – dvorní dramaturg Ludvíka XIV. Kritizoval lakotu, pokrytectví, falešnou zbožnost. Psal komedie mravů. Kvůli satiře měl problémy s církví.[cite: 5]",
        "plot": "Harpagon, chorobně lakomý měšťan, nutí dceru Elišku provdat za bohatého Anselma a syna Kleanta do zásnub s bohatou vdovou. Sám chce si vzít Marianu – nevědomky Kleantovu lásku. Kleantův sluha Čipera ukradne zahrabanou truhličku se zlatem. Harpagon šílí a obviňuje všechny. Vše se rozřeší: Anselm je otec Valére i Mariany, zaplatí veškeré náklady, děti si vezmou koho chtějí.[cite: 5]",
        "excerpt": """HARPAGON (sám, v panice):
Zloději! Vrazi! Loupežníci! Spravedlnosti, spravedlivé nebe!
Jsem ztracen, jsem zavražděn! Podřízli mi krk, ukradli mi mé peníze!
Kdo to mohl být? Kam se poděl? Kde se skrývá?

(chytí sám sebe za ruku)

Ach, ty tam! Vydej mi mé peníze, nebo tě...!
Ach ne, vždyť já mluvím sám se sebou. Přišel jsem o rozum.
Ó mé milované peníze, mé zlatíčko, mého nejlepšího přítele mi ukradli!

Bez tebe je svět prázdný a tmavý. Všichni stůjte!
Kdo to viděl? Kdo to vzal?
(ukazuje na diváky)
Vy? – Nejste to vy? Nebo vy? – Nevím nic.
Svět zešílel a já s ním. Vraťte mi mé peníze, nebo se zblázdím![cite: 5]""",
        "context": "4. dějství, scéna 7 – Harpagon právě zjistil krádež truhličky. Vrcholný monolog = přechod od krizového bodu ke katarzi a rozuzlení.[cite: 5]"
    },
    {
        "id": 2,
        "author": "C. Goldoni[cite: 5]",
        "title": "Sluha dvou pánů[cite: 5]",
        "movement": "Osvícenství / Klasicismus · 18. stol. · Itálie[cite: 5]",
        "authorInfo": "Carlo Goldoni (1707–1793) – největší reformátor evropské komedie. Transformoval commedia dell'arte: zavedl plně vypsané dialogy místo improvizace, odstranil masky. Osvícenský důraz na rozum.[cite: 5]",
        "plot": "Sluha Truffaldino se naráz najme dvěma pánům (dvojí plat, dvojí jídlo). Jeden pán je Beatrice přestrojená za mrtvého bratra Federiga, druhý je Florindo (Beatricin milenec). Z Truffaldinovy dvojí služby, záměn dopisů a kufříků vzniká komický chaos. Vše se vyřeší: Beatrice s Florindem se najdou, Truffaldino dostane Smeraldinu.[cite: 5]",
        "excerpt": """TRUFFALDINO (sám, spokojeně):
Dva platy! Dva obědy! Dva pánové a já jeden!
To je teda paráda. Jeden o druhém neví – výborně!

(počítá na prstech)
Tohle je pan Florindo. Tamhle je pan Federigo – tedy slečna Beatrice.
Ale to já nevím. Pro mne jsou to dva pánové a dva platy.

(obává se)
Jen aby si náhodou nezačali povídat...
(radostně)
Ale zatím jsou spokojení. Oba! Jsem génius.
Největší sluha na světě![cite: 5]""",
        "context": "1. dějství – Truffaldino přijal druhou službu. Monolog spouštějící celou lavinu lží a nedorozumění.[cite: 5]"
    },
    {
        "id": 3,
        "author": "K. J. Erben[cite: 5]",
        "title": "Kytice[cite: 5]",
        "movement": "Národní obrození / Romantismus · 19. stol. · Čechy[cite: 5]",
        "authorInfo": "Karel Jaromír Erben (1811–1870) – archivář, historik, sběratel lidové slovesnosti. Český folklorní romantismus. Důraz na nevyhnutelnost osudu, přísné mravní principy.[cite: 5]",
        "plot": "Sbírka 13 balad: Polednice (matka v afektu přivolá Polednici, dítě udusí), Vodník (dívka neuposlechne matku, vodník zabije dítě), Svatební košile (mrtvý milenec si přijde pro dívku, zachrání ji modlitba), Záhořovo lože, Zlatý kolovrat, Věštkyně a další. Každá balada: porušení mravního řádu → nevyhnutelný trest.[cite: 5]",
        "excerpt": """Z balady Vodník:

Nevesely, truchlivy
jsou ty vodní kraje,
kde si v trávě pod leknínem
rybka s rybkou hraje.
Tu slunéčko nezahřívá,
větřík nezaveje:
chladno, ticho – jako v žalu
srdce bez naděje.

Zelená se hladina,
v hladině se nebe:
přes jezírko přeplouvá
zelený mužíček.
Zelený, zelený,
zelené šatičky;
sedí, šije, zpívá si,
čeká na ženičky.[cite: 5]""",
        "context": "Úvod balady Vodník – expozice. Navozuje temnou atmosféru podvodního světa ještě před příchodem hrdinky.[cite: 5]"
    },
    {
        "id": 4,
        "author": "K. H. Borovský[cite: 5]",
        "title": "Král Lávra[cite: 5]",
        "movement": "Realismus (počátky) · 19. stol. · Čechy[cite: 5]",
        "authorInfo": "Karel Havlíček Borovský (1821–1856) – zakladatel moderní české žurnalistiky a politické satiry. Nucené vyhnanství v Brixenu. Satirik absolutismu. Zemřel předčasně.[cite: 5]",
        "plot": "Irský král Lávra skrývá oslí uši, holiče po práci nechává popravovat. Holič Kukulín přežije díky slibu mlčení. Tajemství ho drtí – vyšeptá ho do vrby. Muzikant z větve vrby vyrobí basu, ta na plese vyzpívá pravdu. Lid krále nezavrhne.[cite: 5]",
        "excerpt": """Byltě jeden král,
irský mocnář Lávra,
posud o něm v Irčanech
divná pověst blábolí.

Byl to dobrý král,
jen tu chybu měl,
že ho holič po oholení
nikdy víc neviděl.

Jednou Kukulín,
chudý student mladý,
přišel ke králi
a dostal se k němu.

Král mu hladce hlavu
oholit si kázal –
Kukulín ho hladce
oholil a zhasil.

Ale neobjal ho
ruka krvavá:
„Ty mi budeš žít, jen
nesmíš mluvit na světa.“[cite: 5]""",
        "context": "Úvod a první střetnutí – expozice. Ironické představení krále a nastolení Kukulínova dilematu.[cite: 5]"
    },
    {
        "id": 5,
        "author": "R. L. Stevenson[cite: 5]",
        "title": "Dr. Jekyll a Mr. Hyde[cite: 5]",
        "movement": "Novoromantismus / Dekadence · konec 19. stol. · Anglie[cite: 5]",
        "authorInfo": "Robert Louis Stevenson (1850–1894) – skotský prozaik. Viktoriánská éra a její pokrytectví. Celoživotní fascinace morální dualitou. Zemřel na Samoe.[cite: 5]",
        "plot": "Lékař Jekyll vynalezne elixír, jímž se mění v Hyda – malého, ohavného muže bez morálky. Hyde páchá zločiny. Jekyll ztrácí kontrolu, Hyde přebírá i bez elixíru. Právník Utterson pátrá. Po Jekyllově/Hydově smrti nalezne zápisek s celou pravdou.[cite: 5]",
        "excerpt": """Celý ten večer jsem byl nevýslovně nešťastný.
Přemítal jsem a utrpení mé bylo velké.
Šel jsem do postele a usnul jsem hlubokým spánkem.

Ráno jsem se probudil s pocitem, který dávám do třídy „divný“.
Podíval jsem se na své ruce.

Byla to ruce Edwarda Hyda.

Tentokrát jsem se stal Hydem, aniž jsem vzal lektvar.
Bez varování. Bez přípravy.
A tehdy jsem pochopil, že konec se blíží.
Hyde přebírá.
A já ho nezastavím.[cite: 5]""",
        "context": "Vrchol Jekyllovy zpovědi – Hyde začíná převládat bez elixíru. Bod bez návratu. Přechod k tragickému závěru.[cite: 5]"
    },
    {
        "id": 6,
        "author": "A. de Saint-Exupéry[cite: 5]",
        "title": "Malý princ[cite: 5]",
        "movement": "Humanistická literatura · 20. stol. · Francie[cite: 5]",
        "authorInfo": "Antoine de Saint-Exupéry (1900–1944) – pilot, filosof. Dílo vzniklo v exilu v USA za 2. světové války. Zahynul při průzkumném letu.[cite: 5]",
        "plot": "Letec havaruje na Sahaře. Setká se s Malým princem z asteroidu B-612. Princ opustil svou Růži a cestoval od planety k planetě (Král, Domýšlivec, Pijan, Byznysmen, Lampář, Zeměpisec). Na Zemi ho Liška naučila: „Správně vidíme jen srdcem. Jsi zodpovědný za to, cos zkrotil.“ Princ se nechá uštknout hadem, aby se vrátil k Růži.[cite: 5]",
        "excerpt": """„Tady je mé tajemství,“ řekla liška. „Velice prosté:
správně vidíme jen srdcem.
Co je důležité, je očím neviditelné.“

„Co je důležité, je očím neviditelné,“
opakoval malý princ, aby si to zapamatoval.

„Čas, který jsi strávil se svou růží,
dělá tvou růži tak důležitou.“

„Čas, který jsem strávil se svou růží...“
opakoval malý princ, aby si to zapamatoval.

„Lidé na tuto pravdu zapomněli,“ řekla liška.
„Ale ty na ni nesmíš zapomenout.
Jsi navždy zodpovědný za to, cos zkrotil.
Jsi zodpovědný za svou růži.“[cite: 5]""",
        "context": "Kapitola 21 – Liška se loučí s princem. Nejdůležitější sdělení celého díla o zodpovědnosti a lásce.[cite: 5]"
    },
    {
        "id": 7,
        "author": "E. Hemingway[cite: 5]",
        "title": "Stařec a moře[cite: 5]",
        "movement": "Ztracená generace · 20. stol. · USA[cite: 5]",
        "authorInfo": "Ernest Hemingway (1899–1961) – laureát Nobelovy ceny (1954). Ztracená generace. Metoda ledovce. Válečný zpravodaj. Sebevražda 1961.[cite: 5]",
        "plot": "Kubánský rybář Santiago 84 dní nic nechytí. Vypluje sám daleko na moře. Přes dva dny bojuje s obrovským marlínem, zdolá ho, přiváže ke člunu. Na cestě zpět žraloci rybu sežerou. Vrátí se jen s kostrou – ale cítí se jako vítěz.[cite: 5]",
        "excerpt": """„Ale člověk není stvořen pro porážku,“ řekl.
„Člověka je možno zničit, ale ne porazit.“

Zamrzelo ho, že rybu zabil. Teď přijde zlá chvíle
a on nemá harpunu ani zbraň.
Ten dentuso žralok je krutý, zdatný, silný a inteligentní.
Ale já jsem byl taky inteligentní. Jen jsem neměl štěstí.

„Drž se, stará rybo,“ řekl tiše. „Drž se.“

Stáhl se do sebe, kousl do rtu a díval se do moře.
Věděl, co přijde.
Ale šel do toho. Jako vždy. Jako celý život.[cite: 5]""",
        "context": "Vrchol novely – Santiagovo ústřední životní krédo po zdolání ryby, těsně před příchodem žraloků.[cite: 5]"
    },
    {
        "id": 8,
        "author": "G. Orwell[cite: 5]",
        "title": "Farma zvířat[cite: 5]",
        "movement": "Světová literatura · 20. stol. · Anglie[cite: 5]",
        "authorInfo": "George Orwell, vl. Eric Arthur Blair (1903–1950) – novinář, esejista. Socialista rozčarovaný Stalinem. Bojoval ve španělské občanské válce. Zemřel na TBC.[cite: 5]",
        "plot": "Zvířata vyženou farmáře Jonese, vybudují Animalismus (7 přikázání). Prasata Napoleon (= Stalin) a Snowball (= Trockij) vedou farmu. Napoleon vyžene Snowballa pomocí psů. Boxer se udře k smrti, je prodán na jatka. Přikázání jsou přepisována. Konec: prasata chodí po dvou, jsou k nerozeznání od lidí.[cite: 5]",
        "excerpt": """Prasata vstala brzy ráno, ještě před začátkem pracovní doby,
a šla přečíst sedm přikázání na stěně stodoly.

Ale přikázání tam nebyla.
Byla tam jen jediná věta.

Zněla takto:

VŠECHNA ZVÍŘATA JSOU SI ROVNA,
ALE NĚKTERÁ JSOU SI ROVNĚJŠÍ.

Potom, co si to zvířata přečetla,
vracela se ke svým pracím.
Dveřmi farmářského domu viděla prasata.
Prasata chodila po dvou.
Prasata nesla bičíky.[cite: 5]""",
        "context": "Závěr novely – absolutní degenerace revolučních ideálů. Přikázání přepsána. Alegorie je dokonána.[cite: 5]"
    },
    {
        "id": 9,
        "author": "G. Orwell[cite: 5]",
        "title": "1984[cite: 5]",
        "movement": "Dystopická literatura · 20. stol. · Anglie[cite: 5]",
        "authorInfo": "Orwell dopsal 1984 umíraje na TBC (1948). Varování před totalitarismem – inspirace stalinismem i nacismem. Největší dystopie 20. stol.[cite: 5]",
        "plot": "Winston Smith pracuje na Ministerstvu pravdy – přepisuje historii. Tajně píše deník (ideozločin) a miluje Julii. Věří O'Brienovi – ten je agent Ideopolicie. Oba zatčeni. V Pokoji 101 Winston čelí svému největšímu strachu (krysy), zradí Julii. Na závěr miluje Velkého bratra.[cite: 5]",
        "excerpt": """Byl jasný, studený dubnový den a hodiny odbíjely třináctou.

Winston Smith, se zataženou bradou,
aby unikl zlému větru, vklouzl rychle
skleněnými dveřmi do paláce Vítězství.
Ale přesto mu vítr přinesl dovnitř závan prachu a písku.

Na stěně visela barevná plakáta –
příliš velká na to, aby se dala pověsit v bytě.
Zobrazovala obrovský obličej muže asi pětačtyřiceti let
s hustým černým knírem a přísně vyhlížejícíma očima.

Obličej sledoval Winstona z každého rohu.
VELKÝ BRATR TĚ SLEDUJE – hlásalo heslo pod ním.[cite: 5]""",
        "context": "Úvodní odstavce románu. 'Třináctá hodina' = pokřivená realita. Velký bratr = totalitní dozor etablován ihned.[cite: 5]"
    },
    {
        "id": 10,
        "author": "R. Bradbury[cite: 5]",
        "title": "451 stupňů Fahrenheita[cite: 5]",
        "movement": "Science Fiction · 20. stol. · USA[cite: 5]",
        "authorInfo": "Ray Bradbury (1920–2012) – mistr poetické SF. Varování před médii a pasivitou společnosti. Dílo vzniklo v době studené války a nástupu televize. 451 °F = teplota hoření papíru.[cite: 5]",
        "plot": "V budoucnosti jsou knihy zakázány, hasiči je pálí. Montag pracuje jako hasič. Sousedka Clarisse mu otevře oči. Začne tajně číst. Manželka Mildred ho udá. Montag zabije velitele Beattyho, uteče. Za městem se přidá ke 'knižním lidem' – ti si celé knihy pamatují nazpaměť.[cite: 5]",
        "excerpt": """Byla to zvláštní slast, vidět věci pohlcené plamenem,
vidět, jak černají a mění se.

Nyní, když svíral v rukou mosaznou proudnici
a vrhal ohromný proud jedovatého petroleje na svět,
cítil, jak se v něm probouzí rozum
a jak se mu kroutí ruce do divokého tance,
jakmile dům pohltila zář připomínající západ slunce,
jakmile ho obklopilo hřejivé červánkové jitro.

Montag byl hasičem č. 451.
A byl spokojený.
Zatím.[cite: 5]""",
        "context": "Úvod románu – Montagovo vstoupení do světa. Paradox: hasič zapaluje. Fáze PŘED jeho prozřením.[cite: 5]"
    },
    {
        "id": 11,
        "author": "R. Bradbury[cite: 5]",
        "title": "Marťanská kronika[cite: 5]",
        "movement": "Science Fiction · 20. stol. · USA[cite: 5]",
        "authorInfo": "Bradbury v Marťanské kronice kritizuje kolonialismus, rasismus a lidskou agresi. SF jako zrcadlo americké poválečné společnosti. Reaguje na strach z atomové války.[cite: 5]",
        "plot": "Série povídek o kolonizaci Marsu (1999–2026). Pozemšťané vyhubí Marťany nemocemi. Kolonizace, ničení kultury. Atomová válka na Zemi většinu kolonistů přinutí vrátit se. Zbylí se sami stávají novými Marťany.[cite: 5]",
        "excerpt": """Měli zlatohnědou pleť a žluté oči, jak mívají Marťané,
a hlas měli tichý a melodický jako déšť.

Kdysi dávno žili ve městech z křišťálu
a pili z pohárů průzračných jak vzduch
a zpívali písně starší než čas.

A pak přišli pozemšťané.
Přinesli plíce plné prachu
a hrdla hlasitá jak zvony.
Přinesli noviny, rádio, automobily.

Z planety tiché a harmonické
se stalo místo, kde bučí klaksony
a dusí výfuky.[cite: 5]""",
        "context": "Expozice – popis marťanské civilizace před příchodem lidí. Alegorie kolonialismu.[cite: 5]"
    },
    {
        "id": 12,
        "author": "Christiane F.[cite: 5]",
        "title": "My děti ze stanice ZOO[cite: 5]",
        "movement": "Dokumentární literatura · 20. stol. · Německo[cite: 5]",
        "authorInfo": "Christiane Vera Felscherinow (*1962 Berlín). Novináři Kai Hermann a Horst Rieck zpracovali magnetofonové záznamy 15leté těžké narkomanky. Autentická výpověď bez moralizování.[cite: 5]",
        "plot": "Christiane vyrůstá v sídlišti Gropiusstadt, alkoholik otec, nucený přesun. Diskotéka Sound, parta, experimenty s drogami. Heroin, závislost. Prostituce u stanice ZOO za peníze na drogu. Smrti kamarádek (Babsi, Stella). Opakované neúspěšné odvykání. Matka ji nakonec odveze na venkov.[cite: 5]",
        "excerpt": """Když mi bylo třináct, poprvé jsem si šlehla.
Vzala jsem si první háčko.

Myslela jsem, že to mám pod kontrolou.
Říkali jsme si, že jsme jiní než ti ubohci u stanice,
co se válejí ve vlastním zvratku.
My jsme cool.

Ale pak přišel první stupen. Druhý. Třetí.
A pak jsem stála u stanice ZOO.
A byla jsem jako oni.

Detlef mi řekl: „Teď jsi jedna z nás.“
Nevěděla jsem, jestli mám plakat, nebo se smát.[cite: 5]""",
        "context": "Retrospektivní začátek závislosti. Ztráta iluze kontroly. Přijetí identity narkomanky.[cite: 5]"
    },
    {
        "id": 13,
        "author": "S. King[cite: 5]",
        "title": "Carrie[cite: 5]",
        "movement": "Postmoderní literatura · 20. stol. · USA[cite: 5]",
        "authorInfo": "Stephen King (*1947) – mistr moderního hororu. Prvotina Carrie mu nastartovala kariéru. Zlo v díle nepramení z nadpřirozena, ale z lidské krutosti a šikany.[cite: 5]",
        "plot": "Carrie Whiteová je šikanována ve škole, doma ji tyranizuje fanaticky náboženská matka. Objeví telekinezi. Na maturitním plese ji spolužáci polévají prasečí krví. Carrie v šoku telekinezí zabíjí přítomné a město nechá vyhořet. Matka ji bodne nožem, Carrie ji zabije, sama umírá.[cite: 5]",
        "excerpt": """Ze tmy nad jevištěm se uvolnila vědra.

A pak na ni s ohlušujícím plesknutím dopadla krev.
Byla teplá a lepkavá, a rudá jako plameny.

Tommy stál vedle ní v šoku.
Korunka se mu sesunula z hlavy.

Z hlediště se ozval smích.
Pak další. A další.
Dunivý, bouřlivý smích.

Carrie stála na pódiu a cítila,
jak se v ní cosi mění.
Jako kdyby se otevřely dveře,
které dosud nikdo nikdy neotevřel.

Pak sklopila oči.
A smích ustal.[cite: 5]""",
        "context": "Klimax románu – maturitní ples. Bod zlomu od ponížení k telekinetické pomstě.[cite: 5]"
    },
    {
        "id": 14,
        "author": "F. Gellner[cite: 5]",
        "title": "Po nás ať přijde potopa[cite: 5]",
        "movement": "Anarchičtí buřiči · přelom 19./20. stol. · Čechy[cite: 5]",
        "authorInfo": "František Gellner (1881–1914) – básník, karikaturista, rebel. Anarchistický buřič. Žil bohémsky. Zmizel na haličské frontě 1914. Sbírka šokovala otevřenou sexualitou a vzdorem.[cite: 5]",
        "plot": "Sbírka 34 básní bez děje. Lyrický mluvčí (= autor) – cynický bohém v pražských putykách. Vzdor měšťácké morálce, posedlost opilstvím, volná láska, carpe diem. Pocit marnosti a existenciální prázdnoty.[cite: 5]",
        "excerpt": """Má milá rozmilá, neplakej!
Život už není jiný.
Dnes buďme ještě veselí
na naší cestě k smrti.
Pijme a milujme, pospíchej,
nežli nás osud zdrtí.

Za sto let, hezká a milá,
oba budeme prach.
Naše láska, naše milování
vyhnijou v červích pracech.

Tak proč se zdráháš a váháš?
Pospěšme si – hned teď!
Zítra se rána nedočkáme,
kdo ví co přijde v tmách.[cite: 5]""",
        "context": "Typický Gellnerův vitalismus: carpe diem jako vzdor. Forma šansonu / kupletu.[cite: 5]"
    },
    {
        "id": 15,
        "author": "K. Poláček[cite: 5]",
        "title": "Bylo nás pět[cite: 5]",
        "movement": "Meziválečná česká literatura · 20. stol. · Čechy[cite: 5]",
        "authorInfo": "Karel Poláček (1892–1945) – humorista, novinář, Pátečník (Čapek, Bass). Napsáno tajně 1943. Zahynul v koncentračním táboře. Vydáno posmrtně 1946.[cite: 5]",
        "plot": "Péťa Bajza a parta (Bejval, Zilvar, Čeněk, Éda) prožívají klukovská dobrodružství na maloměstě: války s Habrováky, vybírání vosího hnízda, školní peripetie, zásnuby s dívčí partou. Závěr: Péťa těžce onemocní spálou a v horečnatém snu cestuje do Indie.[cite: 5]",
        "excerpt": """My kluci, co spolu chodíme, zažijeme spoustu legrace.

Antonín Bejval tuhle vynalezl, že budeme vybírat vstupné
na to, jak budeme tlouct Zilvara z chudobince.

„A co z toho budeme mít?“ ptal se Čeněk Jirsák.

„No, peníze,“ vysvětloval Bejval velice rozumně.
„A Zilvar dostane od každého půlku.
Za to půjde do chudobince a bude tam tlučen.“

Zilvar poslouchal a tvářil se zcela klidně.
To proto, protože on je chudý.
Chudí lidé se nemohou rozčilovat.[cite: 5]""",
        "context": "Expozice – nastolení humoristického tónu. Naivní krutost jako zdroj humoru. Péťův dětský pohled.[cite: 5]"
    },
    {
        "id": 16,
        "author": "Z. Jirotka[cite: 5]",
        "title": "Saturnin[cite: 5]",
        "movement": "Česká literatura / Protektorát · 20. stol. · Čechy[cite: 5]",
        "authorInfo": "Zdeněk Jirotka (1911–2003). Protektorát 1942 – apolitická literatura prošla cenzurou. Vliv P. G. Wodehouse (Jeeves). Útěk od reality.[cite: 5]",
        "plot": "Gentleman (bezejmenný) zaměstná Saturnina – dokonalého, ale nepředvídatelného sluhu. Na chatě jsou odříznutí povodní s tetou Kateřinou. Saturnin řeší každou situaci po svém – s katastrofálně komickými výsledky, ale vždy vše dopadne dobře. Pomáhá pánovi získat slečnu Barboru.[cite: 5]",
        "excerpt": """Můj sluha Saturnin přešel k mému lůžku
s tváří naprosto klidnou a bezvýraznou, jako vždy.

„Promiňte, pane,“ řekl tichým a kultivovaným hlasem,
„teta Kateřina je v obývacím pokoji
a právě zahájila palbu příslovími.
Usoudil jsem, že je třeba přijmout přiměřená obranná opatření.“

„Přiměřená opatření?“ opakoval jsem nevěřícně.

„Právě jsem odstavil pianino do předsíně
a zablokoval dveře šatní skříní.“

Chvilku jsem hleděl ve dveřích.
Pak jsem se otočil a šel zpátky do postele.
Bylo to jediné rozumné řešení.[cite: 5]""",
        "context": "Typická Saturninova iniciativa – kultivovaný klid při absurdní akci = suchý anglický humor.[cite: 5]"
    },
    {
        "id": 17,
        "author": "B. Hrabal[cite: 5]",
        "title": "Ostře sledované vlaky[cite: 5]",
        "movement": "Poválečná česká literatura · 20. stol. · Čechy[cite: 5]",
        "authorInfo": "Bohumil Hrabal (1914–1997) – pábení, automatický text. Film Jiřího Menzla – Oscar 1968. Zemřel pádem z okna nemocnice.[cite: 5]",
        "plot": "Mladý výpravčí Miloš Hrma nastupuje na nádraží v Protektorátu. Trpí studem z intimního selhání (sebevražedný pokus). Výpravčí Hubička razítkoval telegrafistce záď – skandál. Miloš se zasvětí u partyzánky Viktorie Freie. Hrdinsky sabotuje německý zásobovací vlak – zahyne.[cite: 5]",
        "excerpt": """Stál jsem na peroně a koukal, jak odjíždí ten vlak.

Měl jsem na krku stříbrné frčky a cítil jsem se dospělý,
a přitom jsem věděl, že jsem selhal, že jsem k ničemu.

Vzpomínal jsem, jak pan výpravčí Hubička s klidem
razítkoval zadnici telegrafistky Zdeničky.
Razítko za razítkem.
Odzadu dopředu.
A ona stála a smála se.

A já jsem věděl, že takový nikdy nebudu.
A taky jsem věděl, že to jednou musím překonat.
Nějak. Anebo zahynout ve snaze.[cite: 5]""",
        "context": "Vnitřní zamyšlení Miloše po Hubičkově aféře. Kontrast banalita vs. hrdinství.[cite: 5]"
    },
    {
        "id": 18,
        "author": "V. Havel[cite: 5]",
        "title": "Audience[cite: 5]",
        "movement": "Samizdatová literatura · 20. stol. · Čechy[cite: 5]",
        "authorInfo": "Václav Havel (1936–2011) – Charta 77, první prezident ČR. Vaňkovské hry 1975 – šířeny samizdatem.[cite: 5]",
        "plot": "Disident Vaněk dře v pivovaru. Sládek mu nabídne kancelářskou práci pod podmínkou, že bude na sebe psát hlášení pro StB. Vaněk odmítne z principu. Sládek opilý celou nabídku opakuje stále dokola. Hra nemá rozuzlení – absurdní spirála bez konce.[cite: 5]",
        "excerpt": """SLÁDEK: Jste inteligent, to vím...
ale musíte mi pomoct.
Já nevím, co tam těm nahoře mám o vás pořád psát.
Kdybyste si to hlášení napsal sám...

VANĚK: Promiňte, ale to z principu nemohu udělat.

SLÁDEK: Vy jste mi taky člověk. Tohleto nechápete?
Já musím hlásit a vy mi nechcete pomoct.
(pauza, pije pivo)
Za mě jste tady, ne? Tak buďte rozumnej.

VANĚK: Promiňte.

SLÁDEK: (smutně) To jsou paradoxy, co?
(dlouhá pauza)
To jsou hrozné paradoxy.[cite: 5]""",
        "context": "Pointa hry – Sládek žádá Vaňka, aby psal sám na sebe udání. Spirálové opakování = absurdita systému.[cite: 5]"
    },
    {
        "id": 19,
        "author": "Svěrák & Smoljak[cite: 5]",
        "title": "Vyšetřování ztráty třídní knihy[cite: 5]",
        "movement": "Česká divadelní literatura · 20. stol. · Čechy[cite: 5]",
        "authorInfo": "Zdeněk Svěrák (*1936) a Ladislav Smoljak (1931–2010) – Divadlo Járy Cimrmana (1967). Mystifikace fiktivního génia jako krytí satirické kritiky komunismu.[cite: 5]",
        "plot": "1. část: Pseudovědecký seminář cimrmanologů o fiktivním géniovi Járovi Cimrmanovi. 2. část: Hra – ve škole zmizí třídní kniha. Ředitel, inspektor a zemský školní rada vedou absurdní vyšetřování prázdné třídy. Jednají nelogicky, byrokracie bez rozuzlení.[cite: 5]",
        "excerpt": """„Kdo z vás ukradl třídní knihu, ať se přihlásí.
Já počkám.“

(odmlka)

„Dobře. Vyhlásil jsem amnestii,
ale ta právě skončila.
Takže. Kdo z vás to udělal,
ať napíše své jméno na papírek
a dá mi to na stůl – anonymně.“

(rozhlíží se po prázdné třídě)

„Vidím, že nechcete spolupracovat.
V takovém případě budu nucen přistoupit
k jinému způsobu šetření.
Zavřeme třídu. Nikoho nepustíme domů.“

(ticho)

„Hm. Ale žáci... žáci odešli.“[cite: 5]""",
        "context": "Groteskní výslech prázdné třídy. Ředitel nezaregistroval odchod žáků – vrchol absurdní logiky.[cite: 5]"
    },
    {
        "id": 20,
        "author": "P. Šabach[cite: 5]",
        "title": "Hovno hoří[cite: 5]",
        "movement": "Současná česká literatura / Normalizace[cite: 5]",
        "authorInfo": "Petr Šabach (1951–2017) – autobiografická fikce. Normalizace v próze (Šabach, Viewegh). Scénář k Pelíškům (1999, Hřebejk/Jarchovský).[cite: 5]",
        "plot": "Série vzpomínkových povídek o dospívání za normalizace. Otcové jsou pasivně rezistentní (lodičky v lahvích). Synové vzdorují. Generační propast a absurdita komunistické každodennosti.[cite: 5]",
        "excerpt": """Když mi bylo patnáct,
myslel jsem, že fotr je ten největší debil na světě.

Zajímaly ho jenom lodičky v lahvi.
Hele.

Zato my jsme s klukama objevovali Ameriku.

Jednou přišel a povídá:
„Proč děláte ty strašný věci?“

A já mu řekl:
„Protože vy neděláte vůbec nic.“

Chvíli na mě koukal.
Pak se otočil a šel dál.
Nevím, jestli mě slyšel.
Nebo jestli to slyšet chtěl.[cite: 5]""",
        "context": "Generační střet – syn vs. otec. Pasivita dospělých vs. vzdor mládeže za normalizace.[cite: 5]"
    }
]

CITE_PATTERN = re.compile(r"\[cite:\s*\d+\]")


def clean_text(value: str) -> str:
    return CITE_PATTERN.sub("", value).strip()


def movement_key(movement: str) -> str:
    return movement.split("·")[0].strip()


ACHIEVEMENTS = [
    ("První bod", "Získej první body.", lambda s: s["score"] >= 10),
    ("Sběratel bodů", "Nasbírej 100 bodů.", lambda s: s["score"] >= 100),
    ("Rozjetá série", "Udrž sérii 3 správných odpovědí.", lambda s: s["best_streak"] >= 3),
    ("Maturitní mašina", "Udrž sérii 5 správných odpovědí.", lambda s: s["best_streak"] >= 5),
    ("Tréninkový dříč", "Odpověz alespoň 10 otázek.", lambda s: s["total_answered"] >= 10),
]


def init_game_state() -> None:
    defaults = {
        "score": 0,
        "xp": 0,
        "streak": 0,
        "best_streak": 0,
        "total_answered": 0,
        "correct_answers": 0,
        "unlocked_achievements": [],
        "last_unlocks": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def player_level(xp: int) -> int:
    return xp // 100 + 1


def points_to_next_level(xp: int) -> int:
    return 100 - (xp % 100)


def unlock_new_achievements() -> list[str]:
    unlocked = []
    current = set(st.session_state["unlocked_achievements"])
    snapshot = {
        "score": st.session_state["score"],
        "best_streak": st.session_state["best_streak"],
        "total_answered": st.session_state["total_answered"],
    }
    for name, _, condition in ACHIEVEMENTS:
        if name not in current and condition(snapshot):
            current.add(name)
            unlocked.append(name)
    st.session_state["unlocked_achievements"] = sorted(current)
    st.session_state["last_unlocks"] = unlocked
    return unlocked


def reward_result(correct: bool, base_points: int = 20, base_xp: int = 25) -> list[str]:
    st.session_state["total_answered"] += 1
    if correct:
        st.session_state["correct_answers"] += 1
        st.session_state["streak"] += 1
        streak_bonus = min(st.session_state["streak"] * 2, 20)
        st.session_state["score"] += base_points + streak_bonus
        st.session_state["xp"] += base_xp + streak_bonus
    else:
        st.session_state["streak"] = 0
        st.session_state["score"] = max(0, st.session_state["score"] - 5)
        st.session_state["xp"] += 5

    st.session_state["best_streak"] = max(
        st.session_state["best_streak"], st.session_state["streak"]
    )
    return unlock_new_achievements()


AUTHOR_DATABASE = {
    "Molière": {
        "bio": "Francouzský dramatik klasicismu, mistr komedie mravů. Vystavěl satirické postavy posedlé jednou vášní (lakota, pokrytectví, snobství).",
        "other_works": ["Tartuffe", "Zdravý nemocný", "Měšťák šlechticem"],
    },
    "C. Goldoni": {
        "bio": "Italský reformátor komedie. Nahradil improvizaci přesně napsaným dialogem a psychologičtější kresbou postav.",
        "other_works": ["Poprask na laguně", "Mirandolina", "Lhář"],
    },
    "K. J. Erben": {
        "bio": "Sbíral lidovou slovesnost a přetavil ji do balad s důrazem na osudovost, vinu a trest.",
        "other_works": ["Prostonárodní české písně a říkadla", "Písně národní v Čechách", "Pohádky"],
    },
    "K. H. Borovský": {
        "bio": "Novinář a satirik kritizující absolutismus i církevní moc. Pracoval s ironií, alegorií a politickou nadsázkou.",
        "other_works": ["Tyrolské elegie", "Křest svatého Vladimíra", "Epištoly kutnohorské"],
    },
    "R. L. Stevenson": {
        "bio": "Skotský prozaik, který spojoval dobrodružný příběh s psychologickou a morální problematikou.",
        "other_works": ["Ostrov pokladů", "Černý šíp", "Unesen"],
    },
    "A. de Saint-Exupéry": {
        "bio": "Pilot a humanistický autor propojující filosofické otázky s poetickým vyprávěním.",
        "other_works": ["Noční let", "Země lidí", "Válečný pilot"],
    },
    "E. Hemingway": {
        "bio": "Zástupce ztracené generace; úsporný styl, silné podtexty a hrdinové testovaní tlakem situace.",
        "other_works": ["Sbohem, armádo", "Komu zvoní hrana", "Fiesta"],
    },
    "G. Orwell": {
        "bio": "Anglický prozaik a esejista, který demaskoval mechanismy totality, propagandy a manipulace jazykem.",
        "other_works": ["Hold Katalánsku", "Nad vodou a pod vodou v Paříži a Londýně", "Barmské dny"],
    },
    "R. Bradbury": {
        "bio": "Americký autor poetické science fiction; varoval před kulturní pasivitou, cenzurou a technologickým odcizením.",
        "other_works": ["Pampeliškové víno", "Kaleidoskop", "Ikarův pád"],
    },
    "Christiane F.": {
        "bio": "Autobiograficky založená výpověď o drogové závislosti dospívajících v západním Berlíně.",
        "other_works": ["Christiane F. – Můj druhý život"],
    },
    "S. King": {
        "bio": "Americký prozaik, který kombinuje horor s psychologickým realismem a kritikou sociálního násilí.",
        "other_works": ["Osvícení", "To", "Misery"],
    },
    "F. Gellner": {
        "bio": "Básník anarchistických buřičů; civilní lyrika, ironie, vzdor a motiv pomíjivosti.",
        "other_works": ["Radosti života", "Nové verše", "Cesty do hor"],
    },
    "K. Poláček": {
        "bio": "Humorista a fejetonista s mimořádným citem pro jazyk postav a atmosféru maloměsta.",
        "other_works": ["Muži v offsidu", "Hostinec U kamenného stolu", "Okresní město"],
    },
    "Z. Jirotka": {
        "bio": "Autor jemného situačního humoru a inteligentní jazykové komiky inspirované anglickou tradicí.",
        "other_works": ["Muž se psem", "Saturnin se vrací", "Pravidla společenského chování"],
    },
    "B. Hrabal": {
        "bio": "Klíčový český prozaik 2. poloviny 20. století; poetika pábení a směs tragiky s groteskou.",
        "other_works": ["Obsluhoval jsem anglického krále", "Postřižiny", "Příliš hlučná samota"],
    },
    "V. Havel": {
        "bio": "Dramatik absurdního divadla a disident. Sleduje jazykovou manipulaci moci a rozpad osobní odpovědnosti.",
        "other_works": ["Vernisáž", "Zahradní slavnost", "Odcházení"],
    },
    "Svěrák & Smoljak": {
        "bio": "Autorská dvojice Divadla Járy Cimrmana; pracuje s mystifikací, parodií vědeckého diskurzu a absurditou byrokracie.",
        "other_works": ["Akt", "Dobytí severního pólu", "Hospoda Na mýtince"],
    },
    "P. Šabach": {
        "bio": "Prozaik zachycující normalizaci skrze civilní humor, rodinné vztahy a generační střety.",
        "other_works": ["Babičky", "Občanský průkaz", "Šakalí léta"],
    },
}


MOVEMENT_DATABASE = {
    "Klasicismus": "Důraz na rozum, řád, typizované postavy a společenskou satiru. Časté jsou žánrově čisté komedie a tragédie.",
    "Osvícenství / Klasicismus": "Víra v rozum, výchovná funkce literatury a kritika neřestí prostřednictvím komediální situace.",
    "Národní obrození / Romantismus": "Obnova národní kultury, zájem o folklor, historická témata a osudové konflikty.",
    "Realismus (počátky)": "Směřování k věcnosti, kritice společenských poměrů a satirickému odhalování moci.",
    "Novoromantismus / Dekadence": "Krize identity, fascinace temnými stránkami osobnosti, střet civilizované masky a pudovosti.",
    "Humanistická literatura": "Etické otázky, mezilidské vztahy, odpovědnost a smysl života vyjádřené srozumitelnou symbolikou.",
    "Ztracená generace": "Válečná zkušenost, deziluze, osamělý hrdina a úsporný styl s důrazem na podtext.",
    "Světová literatura": "Široce sdílená témata 20. století: moc, propaganda, ideologie, rozklad hodnot.",
    "Dystopická literatura": "Model totalitní budoucnosti, sledování, kontrola jazyka a likvidace individuality.",
    "Science Fiction": "Fikční budoucnost jako nástroj kritiky současnosti, techniky, médií a společenských mechanismů.",
    "Dokumentární literatura": "Autentické svědectví, civilní jazyk, důraz na sociální realitu bez idealizace.",
    "Postmoderní literatura": "Míchání žánrů, práce s popkulturními motivy a otevřená kompozice.",
    "Anarchičtí buřiči": "Programový vzdor vůči měšťácké morálce, bohémský životní styl, ironie a provokace.",
    "Meziválečná česká literatura": "Kombinace humoru a kritického pohledu na společnost, jazyková stylizace vypravěče.",
    "Česká literatura / Protektorát": "Únik k humoru a civilnímu příběhu jako protiúzkostná reakce na okupaci.",
    "Poválečná česká literatura": "Prolnutí všednosti a historického traumatu, tragikomika a vyprávění z periferie.",
    "Samizdatová literatura": "Neoficiální oběh textů, absurdní dramatika a střet jednotlivce s institucí moci.",
    "Česká divadelní literatura": "Autorská mystifikace, parodie odborného jazyka a satira byrokratického systému.",
    "Současná česká literatura / Normalizace": "Paměť pozdního socialismu, rodinné perspektivy a ironická civilnost.",
}


ENRICHED_WORKS = []
for work in WORKS:
    author_clean = clean_text(work["author"])
    movement_clean = clean_text(work["movement"])
    cleaned = {
        **work,
        "authorClean": author_clean,
        "titleClean": clean_text(work["title"]),
        "movementClean": movement_clean,
        "movementKey": movement_key(movement_clean),
        "authorInfoClean": clean_text(work["authorInfo"]),
        "plotClean": clean_text(work["plot"]),
        "excerptClean": clean_text(work["excerpt"]),
        "contextClean": clean_text(work["context"]),
    }
    ENRICHED_WORKS.append(cleaned)

AUTHOR_LIST = sorted({w["authorClean"] for w in ENRICHED_WORKS})
MOVEMENT_LIST = sorted({w["movementKey"] for w in ENRICHED_WORKS})

st.set_page_config(page_title="Maturitní trenér", layout="wide")
st.sidebar.title("📚 Navigace")
mode = st.sidebar.radio(
    "Zvolte režim aplikace:",
    ["Databáze děl", "Profily autorů", "Interaktivní trénink"],
)

if mode == "Databáze děl":
    st.header("📖 Databáze literárních děl k maturitě")
    query = st.text_input("Hledat podle názvu, autora, děje nebo kontextu")
    selected_authors = st.multiselect("Filtr autora", AUTHOR_LIST)
    selected_movements = st.multiselect("Filtr literárního směru", MOVEMENT_LIST)

    filtered_works = []
    for work in ENRICHED_WORKS:
        if selected_authors and work["authorClean"] not in selected_authors:
            continue
        if selected_movements and work["movementKey"] not in selected_movements:
            continue
        haystack = " ".join(
            [work["titleClean"], work["authorClean"], work["plotClean"], work["contextClean"]]
        ).lower()
        if query and query.lower() not in haystack:
            continue
        filtered_works.append(work)

    col1, col2 = st.columns(2)
    col1.metric("Počet děl v databázi", len(ENRICHED_WORKS))
    col2.metric("Počet děl po filtraci", len(filtered_works))

    if not filtered_works:
        st.warning("Žádné dílo neodpovídá zadaným filtrům.")
    else:
        labels = [f"{w['id']}. {w['titleClean']} — {w['authorClean']}" for w in filtered_works]
        selected_label = st.selectbox("Vyber dílo", labels)
        selected_work = next(
            w for w in filtered_works if selected_label.startswith(f"{w['id']}.")
        )

        st.subheader(selected_work["titleClean"])
        st.write(
            f"**Autor:** {selected_work['authorClean']}  \n"
            f"**Literární směr:** {selected_work['movementClean']}"
        )

        tab_plot, tab_excerpt, tab_author, tab_movement = st.tabs(
            ["Děj díla", "Úryvek + kontext", "Autor", "Směr"]
        )

        with tab_plot:
            st.markdown("### Podrobný děj")
            st.write(selected_work["plotClean"])
            with st.expander("Rychlý tahák k zasazení úryvku"):
                st.success(selected_work["contextClean"])

        with tab_excerpt:
            st.markdown("### Dlouhý úryvek")
            st.info(selected_work["excerptClean"])
            st.markdown("### Jak úryvek zasadit do děje")
            st.write(selected_work["contextClean"])

        with tab_author:
            author_detail = AUTHOR_DATABASE.get(
                selected_work["authorClean"],
                {"bio": selected_work["authorInfoClean"], "other_works": []},
            )
            st.markdown("### Profil autora")
            st.write(author_detail["bio"])
            st.markdown("### Další díla autora")
            if author_detail["other_works"]:
                for item in author_detail["other_works"]:
                    st.write(f"- {item}")
            else:
                st.write("Další díla zatím nejsou doplněna.")

        with tab_movement:
            st.markdown("### Kontext literárního směru")
            st.write(
                MOVEMENT_DATABASE.get(
                    selected_work["movementKey"],
                    "Kontext směru zatím není doplněn.",
                )
            )

elif mode == "Profily autorů":
    st.header("🧑‍🏫 Profily autorů a jejich díla")
    selected_author = st.selectbox("Vyber autora", AUTHOR_LIST)
    works_by_author = [w for w in ENRICHED_WORKS if w["authorClean"] == selected_author]
    author_detail = AUTHOR_DATABASE.get(
        selected_author, {"bio": works_by_author[0]["authorInfoClean"], "other_works": []}
    )

    st.markdown("### Bio a význam")
    st.write(author_detail["bio"])
    st.markdown("### Díla v této databázi")
    for work in works_by_author:
        st.write(f"- {work['titleClean']} ({work['movementClean']})")
    st.markdown("### Další důležitá díla")
    if author_detail["other_works"]:
        for item in author_detail["other_works"]:
            st.write(f"- {item}")
    else:
        st.write("Další díla zatím nejsou doplněna.")

else:
    st.header("🎯 Interaktivní trénink k maturitě")
    init_game_state()

    level = player_level(st.session_state["xp"])
    accuracy = (
        st.session_state["correct_answers"] / st.session_state["total_answered"]
        if st.session_state["total_answered"]
        else 0.0
    )

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Skóre", st.session_state["score"])
    m2.metric("Level", level)
    m3.metric("Série", st.session_state["streak"])
    m4.metric("Úspěšnost", f"{accuracy * 100:.0f}%")

    st.progress((st.session_state["xp"] % 100) / 100)
    st.caption(f"Do dalšího levelu zbývá {points_to_next_level(st.session_state['xp'])} XP.")

    if st.session_state["total_answered"] >= 5 and accuracy >= 0.6:
        st.success("🔥 Denní challenge splněna: 5+ odpovědí a alespoň 60 % úspěšnost.")

    with st.expander("🏅 Úspěchy"):
        if st.session_state["unlocked_achievements"]:
            for name, description, _ in ACHIEVEMENTS:
                if name in st.session_state["unlocked_achievements"]:
                    st.write(f"✅ **{name}** — {description}")
        else:
            st.write("Zatím žádné odemčené úspěchy.")

    quiz_mode = st.radio(
        "Typ tréninku",
        ["Poznej dílo podle úryvku", "Zasaď úryvek do děje", "Poznej autora podle díla"],
    )

    if "current_q" not in st.session_state:
        st.session_state.current_q = random.choice(ENRICHED_WORKS)

    current = st.session_state.current_q
    st.info(current["excerptClean"])

    if quiz_mode == "Poznej dílo podle úryvku":
        options = [current["titleClean"]]
        while len(options) < min(4, len(ENRICHED_WORKS)):
            candidate = random.choice(ENRICHED_WORKS)["titleClean"]
            if candidate not in options:
                options.append(candidate)
        random.shuffle(options)

        guess = st.radio("Ze kterého díla je úryvek?", options)
        if st.button("Zkontrolovat odpověď", key="check_work"):
            if guess == current["titleClean"]:
                unlocks = reward_result(True)
                st.success("✅ Správně.")
            else:
                unlocks = reward_result(False)
                st.error(f"❌ Správně je: {current['titleClean']}.")
            st.write(f"**Kontext:** {current['contextClean']}")
            if unlocks:
                st.balloons()
                st.info("Odemčené úspěchy: " + ", ".join(unlocks))

    elif quiz_mode == "Zasaď úryvek do děje":
        st.write("Napiš stručně, co se děje před/po úryvku a proč je důležitý.")
        _ = st.text_area("Tvá odpověď")
        if st.button("Porovnat s databází", key="check_context"):
            st.session_state["total_answered"] += 1
            st.session_state["score"] += 8
            st.session_state["xp"] += 12
            unlocks = unlock_new_achievements()
            st.success(f"Referenční kontext: {current['contextClean']}")
            st.write(f"Rozšířený děj: {current['plotClean']}")
            st.info("✅ Aktivní trénink odměněn: +8 bodů, +12 XP.")
            if unlocks:
                st.balloons()
                st.info("Odemčené úspěchy: " + ", ".join(unlocks))

    else:
        options = [current["authorClean"]]
        while len(options) < min(4, len(AUTHOR_LIST)):
            candidate = random.choice(AUTHOR_LIST)
            if candidate not in options:
                options.append(candidate)
        random.shuffle(options)

        guess = st.radio(
            f"Kdo je autorem díla '{current['titleClean']}'?",
            options,
        )
        if st.button("Zkontrolovat autora", key="check_author"):
            if guess == current["authorClean"]:
                unlocks = reward_result(True, base_points=15, base_xp=20)
                st.success("✅ Správně.")
            else:
                unlocks = reward_result(False, base_points=15, base_xp=20)
                st.error(f"❌ Správně je: {current['authorClean']}.")
            if unlocks:
                st.balloons()
                st.info("Odemčené úspěchy: " + ", ".join(unlocks))

    if st.button("Načíst další otázku"):
        st.session_state.current_q = random.choice(ENRICHED_WORKS)
        st.rerun()

    if st.button("Resetovat progres"):
        for key in [
            "score",
            "xp",
            "streak",
            "best_streak",
            "total_answered",
            "correct_answers",
            "unlocked_achievements",
            "last_unlocks",
        ]:
            del st.session_state[key]
        st.session_state.current_q = random.choice(ENRICHED_WORKS)
        st.rerun()