from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import POKEMON_NAMES, NATURES
from core.lang import get_text
from utils.buttons import main_menu

ITEMS_PER_PAGE = 10

user_box_pages = {}

RARITY_ORDER = {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "legendary": 4}
RARITY_EMOJIS = {"common": "⚪", "uncommon": "🟢", "rare": "🔵", "epic": "🟣", "legendary": "🟡", "mythic": "🔴"}

POKEDEX_ORDER = {
    "Bulbasaur": 1, "Ivysaur": 2, "Venusaur": 3, "Charmander": 4, "Charmeleon": 5, "Charizard": 6,
    "Squirtle": 7, "Wartortle": 8, "Blastoise": 9, "Caterpie": 10, "Metapod": 11, "Butterfree": 12,
    "Weedle": 13, "Kakuna": 14, "Beedrill": 15, "Pidgey": 16, "Pidgeotto": 17, "Pidgeot": 18,
    "Rattata": 19, "Raticate": 20, "Spearow": 21, "Fearow": 22, "Ekans": 23, "Arbok": 24,
    "Pikachu": 25, "Raichu": 26, "Sandshrew": 27, "Sandslash": 28, "Nidoran♀": 29, "Nidorina": 30,
    "Nidoqueen": 31, "Nidoran♂": 32, "Nidorino": 33, "Nidoking": 34, "Clefairy": 35, "Clefable": 36,
    "Vulpix": 37, "Ninetales": 38, "Jigglypuff": 39, "Wigglytuff": 40, "Zubat": 41, "Golbat": 42,
    "Oddish": 43, "Gloom": 44, "Vileplume": 45, "Paras": 46, "Parasect": 47, "Venonat": 48,
    "Venomoth": 49, "Diglett": 50, "Dugtrio": 51, "Meowth": 52, "Persian": 53, "Psyduck": 54,
    "Golduck": 55, "Mankey": 56, "Primeape": 57, "Growlithe": 58, "Arcanine": 59, "Poliwag": 60,
    "Poliwhirl": 61, "Poliwrath": 62, "Abra": 63, "Kadabra": 64, "Alakazam": 65, "Machop": 66,
    "Machoke": 67, "Machamp": 68, "Bellsprout": 69, "Weepinbell": 70, "Victreebel": 71, "Tentacool": 72,
    "Tentacruel": 73, "Geodude": 74, "Graveler": 75, "Golem": 76, "Ponyta": 77, "Rapidash": 78,
    "Slowpoke": 79, "Slowbro": 80, "Magnemite": 81, "Magneton": 82, "Farfetch'd": 83, "Doduo": 84,
    "Dodrio": 85, "Seel": 86, "Dewgong": 87, "Grimer": 88, "Muk": 89, "Shellder": 90, "Cloyster": 91,
    "Gastly": 92, "Haunter": 93, "Gengar": 94, "Onix": 95, "Drowzee": 96, "Hypno": 97, "Krabby": 98,
    "Kingler": 99, "Voltorb": 100, "Electrode": 101, "Exeggcute": 102, "Exeggutor": 103, "Cubone": 104,
    "Marowak": 105, "Hitmonlee": 106, "Hitmonchan": 107, "Lickitung": 108, "Koffing": 109, "Weezing": 110,
    "Rhyhorn": 111, "Rhydon": 112, "Chansey": 113, "Tangela": 114, "Kangaskhan": 115, "Horsea": 116,
    "Seadra": 117, "Goldeen": 118, "Seaking": 119, "Staryu": 120, "Starmie": 121, "Mr. Mime": 122,
    "Scyther": 123, "Jynx": 124, "Electabuzz": 125, "Magmar": 126, "Pinsir": 127, "Tauros": 128,
    "Magikarp": 129, "Gyarados": 130, "Lapras": 131, "Ditto": 132, "Eevee": 133, "Vaporeon": 134,
    "Jolteon": 135, "Flareon": 136, "Porygon": 137, "Omanyte": 138, "Omastar": 139, "Kabuto": 140,
    "Kabutops": 141, "Aerodactyl": 142, "Snorlax": 143, "Articuno": 144, "Zapdos": 145, "Moltres": 146,
    "Dratini": 147, "Dragonair": 148, "Dragonite": 149, "Mewtwo": 150, "Mew": 151,
      "Chikorita": 152, "Bayleef": 153, "Meganium": 154,
    "Cyndaquil": 155, "Quilava": 156, "Typhlosion": 157,
    "Totodile": 158, "Croconaw": 159, "Feraligatr": 160,
    "Sentret": 161, "Furret": 162,
    "Hoothoot": 163, "Noctowl": 164,
    "Ledyba": 165, "Ledian": 166,
    "Spinarak": 167, "Ariados": 168,
    "Crobat": 169,
    "Chinchou": 170, "Lanturn": 171,
    "Pichu": 172,
    "Cleffa": 173,
    "Igglybuff": 174,
    "Togepi": 175, "Togetic": 176,
    "Natu": 177, "Xatu": 178,
    "Mareep": 179, "Flaaffy": 180, "Ampharos": 181,
    "Bellossom": 182,
    "Marill": 183, "Azumarill": 184,
    "Sudowoodo": 185,
    "Politoed": 186,
    "Hoppip": 187, "Skiploom": 188, "Jumpluff": 189,
    "Aipom": 190,
    "Sunkern": 191, "Sunflora": 192,
    "Yanma": 193,
    "Wooper": 194, "Quagsire": 195,
    "Espeon": 196, "Umbreon": 197,
    "Murkrow": 198,
    "Slowking": 199,
    "Misdreavus": 200,
    "Unown": 201,
    "Wobbuffet": 202,
    "Girafarig": 203,
    "Pineco": 204, "Forretress": 205,
    "Dunsparce": 206,
    "Gligar": 207,
    "Steelix": 208,
    "Snubbull": 209, "Granbull": 210,
    "Qwilfish": 211,
    "Scizor": 212,
    "Shuckle": 213,
    "Heracross": 214,
    "Sneasel": 215,
    "Teddiursa": 216, "Ursaring": 217,
    "Slugma": 218, "Magcargo": 219,
    "Swinub": 220, "Piloswine": 221,
    "Corsola": 222,
    "Remoraid": 223, "Octillery": 224,
    "Delibird": 225,
    "Mantine": 226,
    "Skarmory": 227,
    "Houndour": 228, "Houndoom": 229,
    "Kingdra": 230,
    "Phanpy": 231, "Donphan": 232,
    "Porygon2": 233,
    "Stantler": 234,
    "Smeargle": 235,
    "Tyrogue": 236,
    "Hitmontop": 237,
    "Smoochum": 238,
    "Elekid": 239,
    "Magby": 240,
    "Miltank": 241,
    "Blissey": 242,
    "Raikou": 243, "Entei": 244, "Suicune": 245,
    "Larvitar": 246, "Pupitar": 247, "Tyranitar": 248,
    "Lugia": 249, "Ho-Oh": 250, "Celebi": 251,
     "Treecko": 252, "Grovyle": 253, "Sceptile": 254,
    "Torchic": 255, "Combusken": 256, "Blaziken": 257,
    "Mudkip": 258, "Marshtomp": 259, "Swampert": 260,
    "Poochyena": 261, "Mightyena": 262,
    "Zigzagoon": 263, "Linoone": 264,
    "Wurmple": 265, "Silcoon": 266, "Beautifly": 267,
    "Cascoon": 268, "Dustox": 269,
    "Lotad": 270, "Lombre": 271, "Ludicolo": 272,
    "Seedot": 273, "Nuzleaf": 274, "Shiftry": 275,
    "Taillow": 276, "Swellow": 277,
    "Wingull": 278, "Pelipper": 279,
    "Ralts": 280, "Kirlia": 281, "Gardevoir": 282,
    "Surskit": 283, "Masquerain": 284,
    "Shroomish": 285, "Breloom": 286,
    "Slakoth": 287, "Vigoroth": 288, "Slaking": 289,
    "Nincada": 290, "Ninjask": 291, "Shedinja": 292,
    "Whismur": 293, "Loudred": 294, "Exploud": 295,
    "Makuhita": 296, "Hariyama": 297,
    "Azurill": 298,
    "Nosepass": 299,
    "Skitty": 300, "Delcatty": 301,
    "Sableye": 302,
    "Mawile": 303,
    "Aron": 304, "Lairon": 305, "Aggron": 306,
    "Meditite": 307, "Medicham": 308,
    "Electrike": 309, "Manectric": 310,
    "Plusle": 311, "Minun": 312,
    "Volbeat": 313, "Illumise": 314,
    "Roselia": 315,
    "Gulpin": 316, "Swalot": 317,
    "Carvanha": 318, "Sharpedo": 319,
    "Wailmer": 320, "Wailord": 321,
    "Numel": 322, "Camerupt": 323,
    "Torkoal": 324,
    "Spoink": 325, "Grumpig": 326,
    "Spinda": 327,
    "Trapinch": 328, "Vibrava": 329, "Flygon": 330,
    "Cacnea": 331, "Cacturne": 332,
    "Swablu": 333, "Altaria": 334,
    "Zangoose": 335,
    "Seviper": 336,
    "Lunatone": 337,
    "Solrock": 338,
    "Barboach": 339, "Whiscash": 340,
    "Corphish": 341, "Crawdaunt": 342,
    "Baltoy": 343, "Claydol": 344,
    "Lileep": 345, "Cradily": 346,
    "Anorith": 347, "Armaldo": 348,
    "Feebas": 349, "Milotic": 350,
    "Castform": 351,
    "Kecleon": 352,
    "Shuppet": 353, "Banette": 354,
    "Duskull": 355, "Dusclops": 356,
    "Tropius": 357,
    "Chimecho": 358,
    "Absol": 359,
    "Wynaut": 360,
    "Snorunt": 361, "Glalie": 362,
    "Spheal": 363, "Sealeo": 364, "Walrein": 365,
    "Clamperl": 366, "Huntail": 367, "Gorebyss": 368,
    "Relicanth": 369,
    "Luvdisc": 370,
    "Bagon": 371, "Shelgon": 372, "Salamence": 373,
    "Beldum": 374, "Metang": 375, "Metagross": 376,
    "Regirock": 377, "Regice": 378, "Registeel": 379,
    "Latias": 380, "Latios": 381,
    "Kyogre": 382, "Groudon": 383, "Rayquaza": 384,
    "Jirachi": 385, "Deoxys": 386,
    "Turtwig": 387, "Grotle": 388, "Torterra": 389,
    "Chimchar": 390, "Monferno": 391, "Infernape": 392,
    "Piplup": 393, "Prinplup": 394, "Empoleon": 395,
    "Starly": 396, "Staravia": 397, "Staraptor": 398,
    "Bidoof": 399, "Bibarel": 400,
    "Kricketot": 401, "Kricketune": 402,
    "Shinx": 403, "Luxio": 404, "Luxray": 405,
    "Budew": 406, "Roserade": 407,
    "Cranidos": 408, "Rampardos": 409,
    "Shieldon": 410, "Bastiodon": 411,
    "Burmy": 412, "Wormadam": 413, "Mothim": 414,
    # Wormadam formes (Sandy, Trash) n'ont pas de numéro, à gérer en interne si tu veux différencier
    "Combee": 415, "Vespiquen": 416,
    "Pachirisu": 417,
    "Buizel": 418, "Floatzel": 419,
    "Cherubi": 420, "Cherrim": 421,
    # Cherrim Sunshine forme, à gérer en interne
    "Shellos": 422, "Gastrodon": 423,
    # Shellos/Gastrodon West/East, à gérer en interne
    "Ambipom": 424,
    "Drifloon": 425, "Drifblim": 426,
    "Buneary": 427, "Lopunny": 428,
    "Mismagius": 429,
    "Honchkrow": 430,
    "Glameow": 431, "Purugly": 432,
    "Chingling": 433,
    "Stunky": 434, "Skuntank": 435,
    "Bronzor": 436, "Bronzong": 437,
    "Bonsly": 438,
    "Mime Jr.": 439,
    "Happiny": 440,
    "Chatot": 441,
    "Spiritomb": 442,
    "Gible": 443, "Gabite": 444, "Garchomp": 445,
    "Munchlax": 446,
    "Riolu": 447, "Lucario": 448,
    "Hippopotas": 449, "Hippowdon": 450,
    "Skorupi": 451, "Drapion": 452,
    "Croagunk": 453, "Toxicroak": 454,
    "Carnivine": 455,
    "Finneon": 456, "Lumineon": 457,
    "Mantyke": 458,
    "Snover": 459, "Abomasnow": 460,
    "Weavile": 461,
    "Magnezone": 462,
    "Lickilicky": 463,
    "Rhyperior": 464,
    "Tangrowth": 465,
    "Electivire": 466,
    "Magmortar": 467,
    "Togekiss": 468,
    "Yanmega": 469,
    "Leafeon": 470,
    "Glaceon": 471,
    "Gliscor": 472,
    "Mamoswine": 473,
    "Porygon-Z": 474,
    "Gallade": 475,
    "Probopass": 476,
    "Dusknoir": 477,
    "Froslass": 478,
    "Rotom": 479,
    # Rotom formes (Chaleur, Lavage, Froid, Hélice, Tonte) à gérer en interne (même numéro national)
    "Uxie": 480, "Mesprit": 481, "Azelf": 482,
    "Dialga": 483, "Palkia": 484, "Heatran": 485,
    "Regigigas": 486, "Giratina": 487,
    # "Giratina-Origin": 487,  # Même numéro, gère la forme en interne
    "Cresselia": 488,
    "Phione": 489, "Manaphy": 490,
    "Darkrai": 491,
    "Shaymin": 492,
    # "Shaymin-Sky": 492,  # Même numéro, à gérer en interne
    "Arceus": 493,
    # Arceus a aussi des formes (type), mais 1 seul numéro
    "Victini": 494,
    "Snivy": 495, "Servine": 496, "Serperior": 497,
    "Tepig": 498, "Pignite": 499, "Emboar": 500,
    "Oshawott": 501, "Dewott": 502, "Samurott": 503,
    "Patrat": 504, "Watchog": 505,
    "Lillipup": 506, "Herdier": 507, "Stoutland": 508,
    "Purrloin": 509, "Liepard": 510,
    "Pansage": 511, "Simisage": 512,
    "Pansear": 513, "Simisear": 514,
    "Panpour": 515, "Simipour": 516,
    "Munna": 517, "Musharna": 518,
    "Pidove": 519, "Tranquill": 520, "Unfezant": 521,
    "Blitzle": 522, "Zebstrika": 523,
    "Roggenrola": 524, "Boldore": 525, "Gigalith": 526,
    "Woobat": 527, "Swoobat": 528,
    "Drilbur": 529, "Excadrill": 530,
    "Audino": 531,
    "Timburr": 532, "Gurdurr": 533, "Conkeldurr": 534,
    "Tympole": 535, "Palpitoad": 536, "Seismitoad": 537,
    "Throh": 538, "Sawk": 539,
    "Sewaddle": 540, "Swadloon": 541, "Leavanny": 542,
    "Venipede": 543, "Whirlipede": 544, "Scolipede": 545,
    "Cottonee": 546, "Whimsicott": 547,
    "Petilil": 548, "Lilligant": 549,
    "Basculin": 550,
    # Basculin a des formes (Rouge/Bleu/Blanc), à gérer en interne
    "Sandile": 551, "Krokorok": 552, "Krookodile": 553,
    "Darumaka": 554, "Darmanitan": 555,
    # Darmanitan forme Zen, à gérer en interne
    "Maractus": 556,
    "Dwebble": 557, "Crustle": 558,
    "Scraggy": 559, "Scrafty": 560,
    "Sigilyph": 561,
    "Yamask": 562, "Cofagrigus": 563,
    "Tirtouga": 564, "Carracosta": 565,
    "Archen": 566, "Archeops": 567,
    "Trubbish": 568, "Garbodor": 569,
    "Zorua": 570, "Zoroark": 571,
    "Minccino": 572, "Cinccino": 573,
    "Gothita": 574, "Gothorita": 575, "Gothitelle": 576,
    "Solosis": 577, "Duosion": 578, "Reuniclus": 579,
    "Ducklett": 580, "Swanna": 581,
    "Vanillite": 582, "Vanillish": 583, "Vanilluxe": 584,
    "Deerling": 585, "Sawsbuck": 586,
    # Deerling/Sawsbuck saisons à gérer en interne
    "Emolga": 587,
    "Karrablast": 588, "Escavalier": 589,
    "Foongus": 590, "Amoonguss": 591,
    "Frillish": 592, "Jellicent": 593,
    "Alomomola": 594,
    "Joltik": 595, "Galvantula": 596,
    "Ferroseed": 597, "Ferrothorn": 598,
    "Klink": 599, "Klang": 600, "Klinklang": 601,
    "Tynamo": 602, "Eelektrik": 603, "Eelektross": 604,
    "Elgyem": 605, "Beheeyem": 606,
    "Litwick": 607, "Lampent": 608, "Chandelure": 609,
    "Axew": 610, "Fraxure": 611, "Haxorus": 612,
    "Cubchoo": 613, "Beartic": 614,
    "Cryogonal": 615,
    "Shelmet": 616, "Accelgor": 617,
    "Stunfisk": 618,
    "Mienfoo": 619, "Mienshao": 620,
    "Druddigon": 621,
    "Golett": 622, "Golurk": 623,
    "Pawniard": 624, "Bisharp": 625,
    "Bouffalant": 626,
    "Rufflet": 627, "Braviary": 628,
    "Vullaby": 629, "Mandibuzz": 630,
    "Heatmor": 631,
    "Durant": 632,
    "Deino": 633, "Zweilous": 634, "Hydreigon": 635,
    "Larvesta": 636, "Volcarona": 637,
    "Cobalion": 638, "Terrakion": 639, "Virizion": 640,
    "Tornadus": 641, "Thundurus": 642, "Reshiram": 643,
    "Zekrom": 644, "Landorus": 645,
    "Kyurem": 646,
    # Kyurem formes (White/Black), à gérer en interne
    "Keldeo": 647,
    # Keldeo forme Resolution à gérer en interne
    "Meloetta": 648,
    # Meloetta formes (Aria/Pirouette), à gérer en interne
    "Genesect": 649,
    # Genesect disques à gérer en interne
     "Chespin": 650, "Quilladin": 651, "Chesnaught": 652,
    "Fennekin": 653, "Braixen": 654, "Delphox": 655,
    "Froakie": 656, "Frogadier": 657, "Greninja": 658,
    "Bunnelby": 659, "Diggersby": 660,
    "Fletchling": 661, "Fletchinder": 662, "Talonflame": 663,
    "Scatterbug": 664, "Spewpa": 665, "Vivillon": 666,
    # Vivillon a plusieurs motifs, à gérer en interne
    "Litleo": 667, "Pyroar": 668,
    "Flabébé": 669, "Floette": 670, "Florges": 671,
    # Flabébé/Floette/Florges couleurs différentes à gérer en interne
    "Skiddo": 672, "Gogoat": 673,
    "Pancham": 674, "Pangoro": 675,
    "Furfrou": 676,
    # Furfrou formes de coupe à gérer en interne
    "Espurr": 677, "Meowstic": 678,
    # Meowstic formes mâle/femelle à gérer en interne
    "Honedge": 679, "Doublade": 680, "Aegislash": 681,
    # Aegislash formes offensive/défensive à gérer en interne
    "Spritzee": 682, "Aromatisse": 683,
    "Swirlix": 684, "Slurpuff": 685,
    "Inkay": 686, "Malamar": 687,
    "Binacle": 688, "Barbaracle": 689,
    "Skrelp": 690, "Dragalge": 691,
    "Clauncher": 692, "Clawitzer": 693,
    "Helioptile": 694, "Heliolisk": 695,
    "Tyrunt": 696, "Tyrantrum": 697,
    "Amaura": 698, "Aurorus": 699,
    "Sylveon": 700,
    "Hawlucha": 701,
    "Dedenne": 702,
    "Carbink": 703,
    "Goomy": 704, "Sliggoo": 705, "Goodra": 706,
    "Klefki": 707,
    "Phantump": 708, "Trevenant": 709,
    "Pumpkaboo": 710, "Gourgeist": 711,
    # Pumpkaboo/Gourgeist tailles différentes à gérer en interne
    "Bergmite": 712, "Avalugg": 713,
    "Noibat": 714, "Noivern": 715,
    "Xerneas": 716,
    "Yveltal": 717,
    "Zygarde": 718,
    # Zygarde a plusieurs formes (10%, 50%, Complète) à gérer en interne
    "Diancie": 719,
    # Diancie Méga à gérer en interne
    "Hoopa": 720,
    # Hoopa forme Déchaînée à gérer en interne
    "Volcanion": 721,
     "Rowlet": 722, "Dartrix": 723, "Decidueye": 724,
    "Litten": 725, "Torracat": 726, "Incineroar": 727,
    "Popplio": 728, "Brionne": 729, "Primarina": 730,
    "Pikipek": 731, "Trumbeak": 732, "Toucannon": 733,
    "Yungoos": 734, "Gumshoos": 735,
    "Grubbin": 736, "Charjabug": 737, "Vikavolt": 738,
    "Crabrawler": 739, "Crabominable": 740,
    "Oricorio": 741,  # Formes (Baile, Pom-Pom, Pa’u, Sensu) à gérer en interne
    "Cutiefly": 742, "Ribombee": 743,
    "Rockruff": 744, "Lycanroc": 745,  # Formes (Midday, Midnight, Dusk) à gérer en interne
    "Wishiwashi": 746,  # Formes (Solo, Banc) à gérer en interne
    "Mareanie": 747, "Toxapex": 748,
    "Mudbray": 749, "Mudsdale": 750,
    "Dewpider": 751, "Araquanid": 752,
    "Fomantis": 753, "Lurantis": 754,
    "Morelull": 755, "Shiinotic": 756,
    "Salandit": 757, "Salazzle": 758,
    "Stufful": 759, "Bewear": 760,
    "Bounsweet": 761, "Steenee": 762, "Tsareena": 763,
    "Comfey": 764,
    "Oranguru": 765,
    "Passimian": 766,
    "Wimpod": 767, "Golisopod": 768,
    "Sandygast": 769, "Palossand": 770,
    "Pyukumuku": 771,
    "Type: Null": 772, "Silvally": 773,
    "Minior": 774,  # Formes (Météore, Noyau de toutes couleurs) à gérer en interne
    "Komala": 775,
    "Turtonator": 776,
    "Togedemaru": 777,
    "Mimikyu": 778,  # Formes (Buste cassé) à gérer en interne
    "Bruxish": 779,
    "Drampa": 780,
    "Dhelmise": 781,
    "Jangmo-o": 782, "Hakamo-o": 783, "Kommo-o": 784,
    "Tapu Koko": 785, "Tapu Lele": 786, "Tapu Bulu": 787, "Tapu Fini": 788,
    "Cosmog": 789, "Cosmoem": 790, "Solgaleo": 791, "Lunala": 792,
    "Nihilego": 793, "Buzzwole": 794, "Pheromosa": 795,
    "Xurkitree": 796, "Celesteela": 797, "Kartana": 798, "Guzzlord": 799,
    "Necrozma": 800,  # Formes (Ailes de l’Aurore, Crinière du Couchant, Ultra) à gérer en interne
    "Magearna": 801,
    "Marshadow": 802,
    "Poipole": 803, "Naganadel": 804,
    "Stakataka": 805, "Blacephalon": 806,
    "Zeraora": 807,
    "Meltan": 808, "Melmetal": 809,
       "Grookey": 810, "Thwackey": 811, "Rillaboom": 812,
    "Scorbunny": 813, "Raboot": 814, "Cinderace": 815,
    "Sobble": 816, "Drizzile": 817, "Inteleon": 818,
    "Skwovet": 819, "Greedent": 820,
    "Rookidee": 821, "Corvisquire": 822, "Corviknight": 823,
    "Blipbug": 824, "Dottler": 825, "Orbeetle": 826,
    "Nickit": 827, "Thievul": 828,
    "Gossifleur": 829, "Eldegoss": 830,
    "Wooloo": 831, "Dubwool": 832,
    "Chewtle": 833, "Drednaw": 834,
    "Yamper": 835, "Boltund": 836,
    "Rolycoly": 837, "Carkol": 838, "Coalossal": 839,
    "Applin": 840, "Flapple": 841, "Appletun": 842,
    "Silicobra": 843, "Sandaconda": 844,
    "Cramorant": 845,
    "Arrokuda": 846, "Barraskewda": 847,
    "Toxel": 848, "Toxtricity": 849,
    # Toxtricity formes (Aiguë/Basse) à gérer en interne
    "Sizzlipede": 850, "Centiskorch": 851,
    "Clobbopus": 852, "Grapploct": 853,
    "Sinistea": 854, "Polteageist": 855,
    # Sinistea/Polteageist Authentic/Phony à gérer en interne
    "Hatenna": 856, "Hattrem": 857, "Hatterene": 858,
    "Impidimp": 859, "Morgrem": 860, "Grimmsnarl": 861,
    "Obstagoon": 862,
    "Perrserker": 863,
    "Cursola": 864,
    "Sirfetch’d": 865,
    "Mr. Rime": 866,
    "Runerigus": 867,
    "Milcery": 868, "Alcremie": 869,
    # Alcremie formes (différents goûts/couleurs) à gérer en interne
    "Falinks": 870,
    "Pincurchin": 871,
    "Snom": 872, "Frosmoth": 873,
    "Stonjourner": 874,
    "Eiscue": 875,
    # Eiscue formes (Tête de Glace, Tête Décongelée) à gérer en interne
    "Indeedee": 876,
    # Indeedee formes mâle/femelle à gérer en interne
    "Morpeko": 877,
    # Morpeko formes (Plein/Vide) à gérer en interne
    "Cufant": 878, "Copperajah": 879,
    "Dracozolt": 880, "Arctozolt": 881, "Dracovish": 882, "Arctovish": 883,
    "Duraludon": 884,
    "Dreepy": 885, "Drakloak": 886, "Dragapult": 887,
    "Zacian": 888,
    # Zacian formes (Hero/Crowned) à gérer en interne
    "Zamazenta": 889,
    # Zamazenta formes (Hero/Crowned) à gérer en interne
    "Eternatus": 890,
    "Kubfu": 891, "Urshifu": 892,
    # Urshifu formes (Poing Final/Poing Fluide) à gérer en interne
    "Zarude": 893,
    "Regieleki": 894, "Regidrago": 895,
    "Glastrier": 896, "Spectrier": 897, "Calyrex": 898,
    # Calyrex formes (Cavalier du Froid/Glacier) à gérer en interne
    # Pokémon Légendes : Arceus (Hisui)
    "Wyrdeer": 899,
    "Kleavor": 900,
    "Ursaluna": 901,
    "Basculegion": 902,
    "Sneasler": 903,
    "Overqwil": 904,
    "Enamorus": 905,
     "Sprigatito": 906, "Floragato": 907, "Meowscarada": 908,
    "Fuecoco": 909, "Crocalor": 910, "Skeledirge": 911,
    "Quaxly": 912, "Quaxwell": 913, "Quaquaval": 914,
    "Lechonk": 915, "Oinkologne": 916,
    # Oinkologne formes (Mâle, Femelle) à gérer en interne
    "Tarountula": 917, "Spidops": 918,
    "Nymble": 919, "Lokix": 920,
    "Pawmi": 921, "Pawmo": 922, "Pawmot": 923,
    "Tandemaus": 924, "Maushold": 925,
    # Maushold famille de 3 ou 4, à gérer en interne
    "Squawkabilly": 926,
    # Squawkabilly couleurs, à gérer en interne
    "Nacli": 927, "Naclstack": 928, "Garganacl": 929,
    "Charcadet": 930, "Armarouge": 931, "Ceruledge": 932,
    "Tadbulb": 933, "Bellibolt": 934,
    "Wattrel": 935, "Kilowattrel": 936,
    "Maschiff": 937, "Mabosstiff": 938,
    "Shroodle": 939, "Grafaiai": 940,
    "Bramblin": 941, "Brambleghast": 942,
    "Toedscool": 943, "Toedscruel": 944,
    "Klawf": 945,
    "Capsakid": 946, "Scovillain": 947,
    "Rellor": 948, "Rabsca": 949,
    "Flittle": 950, "Espathra": 951,
    "Tinkatink": 952, "Tinkatuff": 953, "Tinkaton": 954,
    "Wiglett": 955, "Wugtrio": 956,
    "Bombirdier": 957,
    "Finizen": 958, "Palafin": 959,
    # Palafin formes (Standard, Héros) à gérer en interne
    "Varoom": 960, "Revavroom": 961,
    "Cyclizar": 962,
    "Orthworm": 963,
    "Glimmet": 964, "Glimmora": 965,
    "Greavard": 966, "Houndstone": 967,
    "Flamigo": 968,
    "Cetoddle": 969, "Cetitan": 970,
    "Veluza": 971,
    "Dondozo": 972,
    "Tatsugiri": 973,
    # Tatsugiri formes (Étirement, Courbure, Goutte) à gérer en interne
    "Annihilape": 974,
    "Clodsire": 975,
    "Farigiraf": 976,
    "Dudunsparce": 977,
    # Dudunsparce famille de 2 ou 3 segments, à gérer en interne
    "Kingambit": 978,
    "Great Tusk": 979, "Scream Tail": 980, "Brute Bonnet": 981, "Flutter Mane": 982,
    "Slither Wing": 983, "Sandy Shocks": 984, "Iron Treads": 985, "Iron Bundle": 986,
    "Iron Hands": 987, "Iron Jugulis": 988, "Iron Moth": 989, "Iron Thorns": 990,
    "Frigibax": 991, "Arctibax": 992, "Baxcalibur": 993,
    "Gimmighoul": 994, "Gholdengo": 995,
    # Gimmighoul formes (Coffre, Errant) à gérer en interne
    "Wo-Chien": 996, "Chien-Pao": 997, "Ting-Lu": 998, "Chi-Yu": 999,
    "Roaring Moon": 1000, "Iron Valiant": 1001,
    "Koraidon": 1002, "Miraidon": 1003,
    "Walking Wake": 1004, "Iron Leaves": 1005,
    # DLC Trésor du Disque Indigo et Mask de Kitakami
    "Dipplin": 1006, "Poltchageist": 1007, "Sinistcha": 1008,
    "Okidogi": 1009, "Munkidori": 1010, "Fezandipiti": 1011, "Ogerpon": 1012,
    # Ogerpon masques, à gérer en interne
    "Archaludon": 1013, "Hydrapple": 1014, "Gouging Fire": 1015, "Raging Bolt": 1016,
    "Iron Boulder": 1017, "Iron Crown": 1018, "Terapagos": 1019,
    # Terapagos formes, à gérer en interne
    "Pecharunt": 1020,
    "Okidogi": 1021, "Munkidori": 1022, "Fezandipiti": 1023, "Ogerpon": 1024,
    "Poltchageist": 1025,
     "Unown-A": 201, "Unown-B": 201, "Unown-C": 201, "Unown-D": 201, "Unown-E": 201,
    "Unown-F": 201, "Unown-G": 201, "Unown-H": 201, "Unown-I": 201, "Unown-J": 201,
    "Unown-K": 201, "Unown-L": 201, "Unown-M": 201, "Unown-N": 201, "Unown-O": 201,
    "Unown-P": 201, "Unown-Q": 201, "Unown-R": 201, "Unown-S": 201, "Unown-T": 201,
    "Unown-U": 201, "Unown-V": 201, "Unown-W": 201, "Unown-X": 201, "Unown-Y": 201,
    "Unown-Z": 201, "Unown-!": 201, "Unown-?": 201,
    "Giratina-Origin": 487,
    "Shaymin-Sky": 492,
    "Basculin-Blue": 550,
    "Basculin-White": 550,
    "Darmanitan-Zen": 555,
    "Tornadus-Therian": 641,
    "Thundurus-Therian": 642,
    "Landorus-Therian": 645,
    "Kyurem-Black": 646,
    "Kyurem-White": 646,
    "Keldeo-Resolute": 647,
    "Meloetta-Pirouette": 648,
    "Greninja-Ash": 658,
    "Zygarde-10%": 718,
    "Zygarde-Complete": 718,
    "Hoopa-Unbound": 720,
    "Oricorio-Pom-Pom": 741,
    "Oricorio-Pa’u": 741,
    "Oricorio-Sensu": 741,
    "Lycanroc-Midnight": 745,
    "Lycanroc-Dusk": 745,
    "Wishiwashi-School": 746,
    "Minior-Meteor": 774,
    "Minior-Red": 774, "Minior-Blue": 774, "Minior-Green": 774,
    "Minior-Indigo": 774, "Minior-Orange": 774, "Minior-Violet": 774, "Minior-Yellow": 774,
    "Mimikyu-Busted": 778,
    "Necrozma-Dawn-Wings": 800,
    "Necrozma-Dusk-Mane": 800,
    "Necrozma-Ultra": 800,
    "Magearna-Original": 801,
    "Toxtricity-Low-Key": 849,
    "Polteageist-Antique": 855,
    "Sinistea-Antique": 854,
    "Indeedee-Female": 876,
    "Morpeko-Hangry": 877,
    "Zacian-Crowned": 888,
    "Zamazenta-Crowned": 889,
    "Urshifu-Rapid-Strike": 892,
    "Calyrex-Ice-Rider": 898,
    "Calyrex-Shadow-Rider": 898,
    "Dudunsparce-Three-Segment": 982,
    "Maushold-Family-of-Three": 925,
    "Palafin-Hero": 964,
    "Tatsugiri-Stretchy": 973,
    "Tatsugiri-Droopy": 973,
    "Tatsugiri-Curly": 973,
}

def format_iv(iv_dict):
    return " / ".join([f"{k}:{v}" for k, v in iv_dict.items()])

def build_box_keyboard(lang, page, max_page):
    buttons = []
    if page > 0:
        buttons.append(get_text("previous_page", lang))
    if page < max_page:
        buttons.append(get_text("next_page", lang))
    nav_buttons = [btn for btn in buttons]
    return ReplyKeyboardMarkup(
        [
            [get_text("button_sort_box", lang)],
            [get_text("button_sell_duplicates", lang)],
            nav_buttons if nav_buttons else [],
            [get_text("menu_back", lang)]
        ],
        resize_keyboard=True
    )

async def show_box(update: Update, context: ContextTypes.DEFAULT_TYPE, page=0):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    box = data.get("box", [])
    if not box:
        await update.message.reply_text(get_text("box_empty", lang), reply_markup=main_menu(lang))
        return

    max_page = (len(box) - 1) // ITEMS_PER_PAGE
    page = max(0, min(page, max_page))
    user_box_pages[user.id] = page

    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE

    message = f"\U0001F4E6 *BOX* (Page {page + 1}/{max_page + 1})\n\n"

    for pkm in box[start_index:end_index]:
        name = POKEMON_NAMES.get(pkm["name"].replace("shiny_", ""), {}).get(lang, pkm["name"].replace("shiny_", ""))
        shiny_icon = "✨ " if pkm.get("shiny") or pkm["name"].startswith("shiny_") else ""
        rarity = pkm.get("rarity", "common")
        rarity_emoji = RARITY_EMOJIS.get(rarity, "⚪")
        name = pkm["name"]
        base_name = name.replace("shiny_", "").split("-")[0]
        pokedex_number = POKEDEX_ORDER.get(base_name, "?")
        nature = NATURES.get(pkm["nature"], {}).get(lang, pkm["nature"])
        known_natures = pkm.get("known_natures", [])
        if known_natures:
            known_text = ", ".join(NATURES.get(n, {}).get(lang, n) for n in known_natures)
            nature += f" ({known_text})"
        ivs_formatted = format_iv(pkm["ivs"])
        quantity = pkm.get("quantity", 1)
        level = pkm.get("level", 1)
        ability = pkm.get("ability", "❓")
        ha = pkm.get("hidden_ability", "❓")
        known_abilities = pkm.get("known_abilities", [ability])
        if ability not in known_abilities:
            known_abilities.append(ability)

        abilities_line = "\n".join(
            [f"  - {'✅' if a == ability else '▫️'} {a}" for a in known_abilities]
        )

        message += (
            f"{rarity_emoji} *#{pokedex_number} {shiny_icon}{name}* _(x{quantity})_\n"
            f"🔢 Niveau : *{level}*\n"
            f"🌱 Nature : _{nature}_\n"
            f"🎯 Talents :\n{abilities_line}\n"
            f"👻 Caché : _{ha}_\n"
            f"📊 IVs : `{ivs_formatted}`\n"
            f"{'-'*30}\n"
        )

    await update.message.reply_text(message.strip(), reply_markup=build_box_keyboard(lang, page, max_page), parse_mode="Markdown")

async def handle_box_navigation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = load_user(user.id).get("lang", "fr")
    current_page = user_box_pages.get(user.id, 0)
    text = update.message.text

    if text == get_text("previous_page", lang):
        await show_box(update, context, page=current_page - 1)
    elif text == get_text("next_page", lang):
        await show_box(update, context, page=current_page + 1)

async def handle_box_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_sort_choice(update, context)
async def sell_duplicates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    box = data.get("box", [])
    if not box:
        await update.message.reply_text(get_text("box_empty", lang), reply_markup=main_menu(lang))
        return

    locked_map = {pkm["name"]: pkm for pkm in box if pkm.get("locked")}
    new_box = []
    stacked_iv = 0
    stacked_ha = False
    stacked_nature = 0
    sold_count = 0
    total_units_sold = 0
    sale_summary = {}

    for pkm in box:
        name = pkm["name"]

        if pkm.get("shiny") or pkm["name"].startswith("shiny_"):
            new_box.append(pkm)
            continue

        if pkm.get("locked"):
            quantity = pkm.get("quantity", 1)
            if quantity > 1:
                rarity_value = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}
                reward = rarity_value.get(pkm.get("rarity", "common"), 100) * (quantity - 1)
                data["money"] += reward
                sold_count += reward
                total_units_sold += (quantity - 1)
                sale_summary[pkm["name"]] = sale_summary.get(pkm["name"], 0) + (quantity - 1)
                pkm["quantity"] = 1
            new_box.append(pkm)
            continue

        if name in locked_map:
            main = locked_map[name]
            for stat in pkm["ivs"]:
                if pkm["ivs"][stat] > main["ivs"].get(stat, 0):
                    main["ivs"][stat] = pkm["ivs"][stat]
                    stacked_iv += 1
            if pkm.get("ability") == pkm.get("hidden_ability") and main.get("ability") != main.get("hidden_ability"):
                main["ability"] = pkm["ability"]
                stacked_ha = True
            if pkm["nature"] not in main.get("known_natures", []):
                main.setdefault("known_natures", []).append(pkm["nature"])
                stacked_nature += 1
            qty = pkm.get("quantity", 1)
            rarity_value = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}
            reward = rarity_value.get(pkm.get("rarity", "common"), 100) * qty
            data["money"] += reward
            sold_count += reward
            total_units_sold += qty
            sale_summary[pkm["name"]] = sale_summary.get(pkm["name"], 0) + qty
        else:
            qty = pkm.get("quantity", 1)
            rarity_value = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}
            reward = rarity_value.get(pkm.get("rarity", "common"), 100) * qty
            data["money"] += reward
            sold_count += reward
            total_units_sold += qty
            sale_summary[pkm["name"]] = sale_summary.get(pkm["name"], 0) + qty

    data["box"] = new_box
    save_user(user.id, data)

    messages = []
    if sold_count > 0:
        messages.append(get_text("duplicates_sold", lang, money=sold_count))
    if stacked_iv > 0:
        messages.append(get_text("iv_stack_message", lang, count=stacked_iv))
    if stacked_ha:
        messages.append(get_text("hidden_ability_stack_message", lang))
    if stacked_nature > 0:
        messages.append(get_text("nature_stack_message", lang, count=stacked_nature))
    if not messages and total_units_sold == 0:
        messages.append(get_text("no_duplicates", lang))

    if sale_summary:
        messages.append("\n📦 Résumé des ventes :")
        for name, qty in sale_summary.items():
            unit_price = {"common": 100, "uncommon": 250, "rare": 500, "epic": 1000, "legendary": 3000}.get(
                next((p["rarity"] for p in box if p["name"] == name), "common"), 100
            )
            messages.append(f"- {name} x{qty} → +{unit_price * qty}💰")

    await update.message.reply_text("\n".join(messages), reply_markup=main_menu(lang))

async def handle_sort_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    if get_text("button_sell_duplicates", lang).lower() in text:
        await sell_duplicates(update, context)
    elif get_text("button_sort_box", lang).lower() in text:
        keyboard = ReplyKeyboardMarkup([
            ["🔤 Nom", "🔺 Rareté"],
            ["📉 Niveau", "📦 Pokédex"],
            ["✨ Shiny", "💯 IV total"],
            [get_text("menu_back", lang)]
        ], resize_keyboard=True)
        await update.message.reply_text(get_text("choose_sorting", lang), reply_markup=keyboard)
    elif "nom" in text:
        data["box"].sort(key=lambda x: POKEMON_NAMES.get(x["name"], {}).get(lang, x["name"]).lower())
        save_user(user.id, data)
        await show_box(update, context)
    elif "rareté" in text:
        data["box"].sort(key=lambda x: RARITY_ORDER.get(x.get("rarity", "common"), 4), reverse=True)
        save_user(user.id, data)
        await show_box(update, context)
    elif "niveau" in text:
        data["box"].sort(key=lambda x: x.get("level", 1), reverse=True)
        save_user(user.id, data)
        await show_box(update, context)
    elif "pokédex" in text:
        data["box"].sort(key=lambda x: POKEDEX_ORDER.get(x.get("name"), 9999))
        save_user(user.id, data)
        await show_box(update, context)
    elif "shiny" in text:
        data["box"].sort(key=lambda x: not (x.get("shiny", False) or x["name"].startswith("shiny_")))
        save_user(user.id, data)
        await show_box(update, context)
    elif "iv" in text:
        data["box"].sort(key=lambda x: sum(x.get("ivs", {}).values()), reverse=True)
        save_user(user.id, data)
        await show_box(update, context)
    else:
        await show_box(update, context)

async def handle_box_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await handle_sort_choice(update, context)
