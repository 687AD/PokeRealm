from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from core.user_data import load_user, save_user
from core.translation_data import POKEMON_NAMES, NATURES
from core.lang import get_text
from utils.buttons import main_menu
from core.lang import get_ability_name

ITEMS_PER_PAGE = 10

user_box_pages = {}

RARITY_ORDER = {"common": 0, "uncommon": 1, "rare": 2, "epic": 3, "legendary": 4, "mythic" : 5}

POKEDEX_ORDER = {
    "Frillish-Male": 592,
    "Frillish-Female": 592,
    "Pikachu-Original-Cap": 25,
    "Bulbasaur": 1, "Ivysaur": 2, "Venusaur": 3, "Charmander": 4, "Charmeleon": 5, "Charizard": 6,
    "Squirtle": 7, "Squirtle-Sunglasses": 7, "Wartortle": 8, "Blastoise": 9, "Caterpie": 10, "Metapod": 11, "Butterfree": 12,
    "Weedle": 13, "Kakuna": 14, "Beedrill": 15, "Pidgey": 16, "Pidgeotto": 17, "Pidgeot": 18,
    "Rattata": 19, "Raticate": 20, "Spearow": 21, "Fearow": 22, "Ekans": 23, "Arbok": 24,
    "Pikachu": 25, "Raichu": 26, "Sandshrew": 27, "Sandslash": 28, "nidoran-m": 29, "Nidorina": 30,
    "Nidoqueen": 31, "nidoran-f": 32, "Nidorino": 33, "Nidoking": 34, "Clefairy": 35, "Clefable": 36,
    "Vulpix": 37, "Ninetales": 38, "Jigglypuff": 39, "Wigglytuff": 40, "Zubat": 41, "Golbat": 42,
    "Oddish": 43, "Gloom": 44, "Vileplume": 45, "Paras": 46, "Parasect": 47, "Venonat": 48,
    "Venomoth": 49, "Diglett": 50, "Dugtrio": 51, "Meowth": 52, "Persian": 53, "Psyduck": 54,
    "Golduck": 55, "Mankey": 56, "Primeape": 57, "Growlithe": 58, "Arcanine": 59, "Poliwag": 60,
    "Poliwhirl": 61, "Poliwrath": 62, "Abra": 63, "Kadabra": 64, "Alakazam": 65, "Machop": 66,
    "Machoke": 67, "Machamp": 68, "Bellsprout": 69, "Weepinbell": 70, "Victreebel": 71, "Tentacool": 72,
    "Tentacruel": 73, "Geodude": 74, "Graveler": 75, "Golem": 76, "Ponyta": 77, "Rapidash": 78,
    "Slowpoke": 79, "Slowbro": 80, "Magnemite": 81, "Magneton": 82, "Farfetch'd": 83, "Farfetch’d-Galarian":83, "Doduo": 84,
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
    "Castform-Sunny": 351,
    "Castform-Rainy": 351,
    "Castform-Snowy": 351,
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
    "Piplup": 393, "Prinplup": 394, "Empoleon": 395, "Piplup-Dawn-Hat": 393,
    "Starly": 396, "Staravia": 397, "Staraptor": 398,
    "Bidoof": 399, "Bibarel": 400,
    "Kricketot": 401, "Kricketune": 402,
    "Shinx": 403, "Luxio": 404, "Luxray": 405,
    "Budew": 406, "Roserade": 407,
    "Cranidos": 408, "Rampardos": 409,
    "Shieldon": 410, "Bastiodon": 411,
    "Mothim": 414,
    "Combee": 415, "Vespiquen": 416,
    "Pachirisu": 417,
    "Buizel": 418, "Floatzel": 419,
    "Cherubi": 420,
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
    "Rotom-Heat": 479,
    "Rotom-Wash": 479,
    "Rotom-Frost": 479,
    "Rotom-Fan": 479,
    "Rotom-Mow": 479,
    "Uxie": 480, "Mesprit": 481, "Azelf": 482,
    "Dialga": 483, "Palkia": 484, "Heatran": 485,
    "Regigigas": 486, "Giratina": 487,
    "Giratina-Origin": 487,
    "Cresselia": 488,
    "Phione": 489, "Manaphy": 490,
    "Darkrai": 491,
    "Shaymin": 492,
    "Shaymin-Sky": 492, 
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
    "Pidove": 519, "Tranquill": 520, "Unfezant-Male": 521,
    "Unfezant-Female": 521,
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
    "Sandile": 551, "Krokorok": 552, "Krookodile": 553,
    "Darumaka": 554,
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
    "Keldeo": 647,
    "Meloetta": 648,
    "Genesect": 649,
    "Genesect-Douse": 649,
    "Genesect-Shock": 649,
    "Genesect-Burn": 649,
    "Genesect-Chill": 649,
    "Chespin": 650, "Quilladin": 651, "Chesnaught": 652,
    "Fennekin": 653, "Braixen": 654, "Delphox": 655,
    "Froakie": 656, "Frogadier": 657, "Greninja": 658, "Greninja-Ash": 658,
    "Bunnelby": 659, "Diggersby": 660,
    "Fletchling": 661, "Fletchinder": 662, "Talonflame": 663,
    "Scatterbug": 664, "Spewpa": 665,
    "Vivillon-Meadow": 666, "Vivillon-Polar": 666, "Vivillon-Tundra": 666, "Vivillon-Garden": 666,
    "Vivillon-Sandstorm": 666, "Vivillon-Icy-Snow": 666, "Vivillon-Modern": 666, "Vivillon-Marine": 666,
    "Vivillon-Archipelago": 666, "Vivillon-High-Plains": 666, "Vivillon-Jungle": 666,
    "Vivillon-Fancy": 666, "Vivillon-Pokeball": 666, "Vivillon-Elegant": 666,
    "Vivillon-Monsoon": 666,
    "Vivillon-Ocean": 666,
    "Vivillon-River": 666,
    "Vivillon-Savanna": 666,
    "Vivillon-Sun": 666,
    "Vivillon-Typhoon": 666,
    "Litleo": 667, "Pyroar-Male": 668,
    "Pyroar-Female": 668,
    "Skiddo": 672, "Gogoat": 673,
    "Pancham": 674, "Pangoro": 675,
    "Espurr": 677,
    "Honedge": 679, "Doublade": 680,
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
    # Pumpkaboo/Gourgeist tailles différentes vraiment utile cette merde ?
    "Bergmite": 712, "Avalugg": 713,
    "Noibat": 714, "Noivern": 715,
    "Xerneas": 716,
    "Yveltal": 717,
    "Zygarde": 718,
    "Diancie": 719,
    "Hoopa": 720,
    "Volcanion": 721,
    "Rowlet": 722, "Dartrix": 723, "Decidueye": 724,
    "Litten": 725, "Torracat": 726, "Incineroar": 727,
    "Popplio": 728, "Brionne": 729, "Primarina": 730,
    "Pikipek": 731, "Trumbeak": 732, "Toucannon": 733,
    "Yungoos": 734, "Gumshoos": 735,
    "Grubbin": 736, "Charjabug": 737, "Vikavolt": 738,
    "Crabrawler": 739, "Crabominable": 740,
    "Cutiefly": 742, "Ribombee": 743,
    "Rockruff": 744,
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
    "Type: Null": 772, 
    "Komala": 775,
    "Turtonator": 776,
    "Togedemaru": 777,
    "Bruxish": 779,
    "Drampa": 780,
    "Dhelmise": 781,
    "Jangmo": 782, "Hakamo": 783, "Kommo": 784,
    "Tapu Koko": 785, "Tapu Lele": 786, "Tapu Bulu": 787, "Tapu Fini": 788,
    "Cosmog": 789, "Cosmoem": 790, "Solgaleo": 791, "Lunala": 792,
    "Nihilego": 793, "Buzzwole": 794, "Pheromosa": 795,
    "Xurkitree": 796, "Celesteela": 797, "Kartana": 798, "Guzzlord": 799,
    "Necrozma": 800, 
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
    "Toxel": 848,
    "Sizzlipede": 850, "Centiskorch": 851,
    "Clobbopus": 852, "Grapploct": 853,
    "Sinistea-Phony": 854,
    "Sinistea-Authentic": 854,
    "Polteageist-Phony": 855,
    "Polteageist-Authentic": 855,
    "Hatenna": 856, "Hattrem": 857, "Hatterene": 858,
    "Impidimp": 859, "Morgrem": 860, "Grimmsnarl": 861,
    "Obstagoon": 862,
    "Perrserker": 863,
    "Cursola": 864,
    "Sirfetch’d": 865,
    "Mr. Rime": 866,
    "Runerigus": 867,
    "Milcery": 868, "Alcremie": 869,
    # Alcremie formes goût couleur ultra chiant j'le fais si vraiment j'ai du temps a perdre
    "Falinks": 870,
    "Pincurchin": 871,
    "Snom": 872, "Frosmoth": 873,
    "Stonjourner": 874,
    "Cufant": 878, "Copperajah": 879,
    "Dracozolt": 880, "Arctozolt": 881, "Dracovish": 882, "Arctovish": 883,
    "Duraludon": 884,
    "Dreepy": 885, "Drakloak": 886, "Dragapult": 887,
    "Eternatus": 890,
    "Kubfu": 891,
    "Zarude": 893,
    "Regieleki": 894, "Regidrago": 895,
    "Glastrier": 896, "Spectrier": 897,
    "Wyrdeer": 899,
    "Kleavor": 900,
    "Ursaluna": 901,
    "Basculegion-Male": 902,
    "Basculegion-Female" : 902,
    "Sneasler-Female": 903,
    "Sneasler-Male": 903,
    "Overqwil": 904,
    "Enamorus": 905,
    "Sprigatito": 906, "Floragato": 907, "Meowscarada": 908,
    "Fuecoco": 909, "Crocalor": 910, "Skeledirge": 911,
    "Quaxly": 912, "Quaxwell": 913, "Quaquaval": 914,
    "Lechonk": 915,
    "Tarountula": 917, "Spidops": 918,
    "Nymble": 919, "Lokix": 920,
    "Pawmi": 921, "Pawmo": 922, "Pawmot": 923,
    "Tandemaus": 924, "Fidough": 926,
    "Dachsbun": 927,
    "Smoliv": 928,
    "Dolliv": 929,
    "Arboliva": 930,
    "Nacli": 932, "Naclstack": 933, "Garganacl": 934,
    "Charcadet": 935, "Armarouge": 936, "Ceruledge": 937,
    "Tadbulb": 938, "Bellibolt": 939,
    "Wattrel": 940, "Kilowattrel": 941,
    "Maschiff": 942, "Mabosstiff": 943,
    "Shroodle": 944, "Grafaiai": 945,
    "Bramblin": 946, "Brambleghast": 947,
    "Toedscool": 948, "Toedscruel": 949,
    "Klawf": 950,
    "Capsakid": 951, "Scovillain": 952,
    "Rellor": 953, "Rabsca": 954,
    "Flittle": 955, "Espathra": 956,
    "Tinkatink": 957, "Tinkatuff": 958, "Tinkaton": 959,
    "Wiglett": 960, "Wugtrio": 961,
    "Bombirdier": 962,
    "Finizen": 963, "Palafin": 964,
    "Varoom": 965, "Revavroom": 966,
    "Cyclizar": 967,
    "Orthworm": 968,
    "Glimmet": 969, "Glimmora": 970,
    "Greavard": 971, "Houndstone": 972,
    "Flamigo": 973,
    "Cetoddle": 974, "Cetitan": 975,
    "Veluza": 976,
    "Dondozo": 977, "Tatsugiri": 978,
    "Annihilape": 979,
    "Clodsire": 980,
    "Farigiraf": 981,
    "Dudunsparce": 982, "Dudunsparce-Three-Segment": 982,
    "Kingambit": 983,
    "Great Tusk": 984, "Scream Tail": 985, "Brute Bonnet": 986, "Flutter Mane": 987,
    "Slither Wing": 988, "Sandy Shocks": 989, "Iron Treads": 990, "Iron Bundle": 991,
    "Iron Hands": 992, "Iron Jugulis": 993, "Iron Moth": 994, "Iron Thorns": 995,
    "Frigibax": 996, "Arctibax": 997, "Baxcalibur": 998,
    "Gimmighoul": 999, "Gimmighoul-Roaming": 999, "Gholdengo": 1000,
    "Wo-Chien": 1001, "Chien-Pao": 1002, "Ting-Lu": 1003, "Chi-Yu": 1004,
    "Roaring Moon": 1005, "Iron Valiant": 1006,
    "Koraidon": 1007, "Miraidon": 1008,
    "Walking Wake": 1009, "Iron Leaves": 1010,
    "Poltchageist": 1011, "Sinistcha": 1012,
    "Okidogi": 1013, "Munkidori": 1014, "Fezandipiti": 1015, "Ogerpon": 1016,
    "Archaludon": 1017, "Hydrapple": 1018, "Gouging Fire": 1019, "Raging Bolt": 1020,
    "Iron Boulder": 1021, "Iron Crown": 1022,
    "Terapagos": 1023, "Terapagos-Terastal": 1023, "Terapagos-Stellar": 1023,
    "Pecharunt": 1024,
    "Unown-A": 201, "Unown-B": 201, "Unown-C": 201, "Unown-D": 201, "Unown-E": 201,
    "Unown-F": 201, "Unown-G": 201, "Unown-H": 201, "Unown-I": 201, "Unown-J": 201,
    "Unown-K": 201, "Unown-L": 201, "Unown-M": 201, "Unown-N": 201, "Unown-O": 201,
    "Unown-P": 201, "Unown-Q": 201, "Unown-R": 201, "Unown-S": 201, "Unown-T": 201,
    "Unown-U": 201, "Unown-V": 201, "Unown-W": 201, "Unown-X": 201, "Unown-Y": 201,
    "Unown-Z": 201, "Unown-!": 201, "Unown-?": 201,
    "Giratina-Origin": 487,
    "Shaymin-Sky": 492,
    "Basculin-Red-Striped" : 550,
    "Basculin-Blue-Striped": 550,
    "Basculin-White-Striped": 550,
    "Tornadus-Therian": 641,
    "Thundurus-Therian": 642,
    "Landorus-Therian": 645,
    "Kyurem-Black": 646,
    "Kyurem-White": 646,
    "Keldeo-Resolute": 647,
    "Meloetta-Pirouette": 648,
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
    "Sinistea-Antique": 854,
    "Calyrex-Ice-Rider": 898,
    "Calyrex-Shadow-Rider": 898,
    "Maushold-Family3": 925,
    "Calyrex": 898,
    "Floette-Eternal": 669,       
    "Oinkologne-Male": 916,
    "Oinkologne-Female": 916,
    "Tauros-Paldean-Combat": 128,
    "Tauros-Paldean-Blaze": 128,
    "Tauros-Paldean-Aqua": 128,
    "Enamorus-Therian": 905,
    "Deerling-Spring": 585,
    "Deerling-Summer": 585,
    "Deerling-Autumn": 585,
    "Deerling-Winter": 585,
    "Sawsbuck-Spring": 586,
    "Sawsbuck-Summer": 586,
    "Sawsbuck-Autumn": 586,
    "Sawsbuck-Winter": 586,
    "Tatsugiri-Curly": 978,
    "Tatsugiri-Droopy": 978,
    "Tatsugiri-Stretchy": 978,
    "Maushold-Family4": 925,
    "Squawkabilly-Green": 931,
    "Squawkabilly-Blue": 931,
    "Squawkabilly-Yellow": 931,
    "Squawkabilly-White": 931,
    "Furfrou": 676,
    "Furfrou-Heart": 676,
    "Furfrou-Star": 676,
    "Furfrou-Diamond": 676,
    "Furfrou-Debutante": 676,
    "Furfrou-Matron": 676,
    "Furfrou-Dandy": 676,
    "Furfrou-La-Reine": 676,
    "Furfrou-Kabuki": 676,
    "Furfrou-Pharaoh": 676,
    "Indeedee-Male": 876,
    "Indeedee-Female": 876,
    "Mimikyu-Disguised": 778,
    "Mimikyu-Busted": 778,
    "Wishiwashi-Solo": 746,
    "Wishiwashi-School": 746,
    "Aegislash-Shield": 681,
    "Aegislash-Blade": 681,
    "Darmanitan": 555,
    "Darmanitan-Galarian-Standard": 555,
    "Darmanitan-Galarian-Zen": 555,
    "Darmanitan-Zen": 555,
    "Shellos-East": 422,
    "Shellos-West": 422,
    "Gastrodon-East": 423,
    "Gastrodon-West": 423,
    "Wormadam-Plant": 413,
    "Wormadam-Sandy": 413,
    "Wormadam-Trash": 413,
    "Burmy-Plant": 412,
    "Burmy-Sandy": 412,
    "Burmy-Trash": 412,
    "Silvally-Normal": 773,
    "Silvally-Fire": 773,
    "Silvally-Water": 773,
    "Silvally-Electric": 773,
    "Silvally-Grass": 773,
    "Silvally-Ice": 773,
    "Silvally-Fighting": 773,
    "Silvally-Poison": 773,
    "Silvally-Ground": 773,
    "Silvally-Flying": 773,
    "Silvally-Psychic": 773,
    "Silvally-Bug": 773,
    "Silvally-Rock": 773,
    "Silvally-Ghost": 773,
    "Silvally-Dragon": 773,
    "Silvally-Dark": 773,
    "Silvally-Steel": 773,
    "Silvally-Fairy": 773,
    "Zarude": 893,
    "Zarude-Dada": 893,
    "Eternatus": 890,
    "Eternatus-Eternamax": 890,
    "Zacian": 888,
    "Zacian-Crowned": 888,
    "Zamazenta": 889,
    "Zamazenta-Crowned": 889,
    "Morpeko-Full-Belly": 877,
    "Morpeko-Hangry": 877,
    "Toxtricity-Amped": 849,
    "Toxtricity-Low-Key": 849,
    "Minior": 774,
    "Minior-Red-Core": 774,
    "Minior-Orange-Core": 774,
    "Minior-Yellow-Core": 774,
    "Minior-Green-Core": 774,
    "Minior-Blue-Core": 774,
    "Minior-Indigo-Core": 774,
    "Minior-Violet-Core": 774,
    "Minior-Core": 774,
    "Oricorio-Baile": 741,
    "Oricorio-Pom-Pom": 741,
    "Oricorio-Pa'u": 741,
    "Oricorio-Sensu": 741,
    "Arceus-Normal": 493,
    "Arceus-Fire": 493,
    "Arceus-Water": 493,
    "Arceus-Electric": 493,
    "Arceus-Grass": 493,
    "Arceus-Ice": 493,
    "Arceus-Fighting": 493,
    "Arceus-Poison": 493,
    "Arceus-Ground": 493,
    "Arceus-Flying": 493,
    "Arceus-Psychic": 493,
    "Arceus-Bug": 493,
    "Arceus-Rock": 493,
    "Arceus-Ghost": 493,
    "Arceus-Dragon": 493,
    "Arceus-Dark": 493,
    "Arceus-Steel": 493,
    "Arceus-Fairy": 493,
    "Flabebe-Red": 669,
    "Flabebe-Yellow": 669,
    "Flabebe-Orange": 669,
    "Flabebe-Blue": 669,
    "Flabebe-White": 669,
    "Floette-Red": 670,
    "Floette-Yellow": 670,
    "Floette-Orange": 670,
    "Floette-Blue": 670,
    "Floette-White": 670,
    "Florges-Red": 671,
    "Florges-Yellow": 671,
    "Florges-Orange": 671,
    "Florges-Blue": 671,
    "Florges-White": 671,
    "Meowstic-Male": 678, "Meowstic-Female": 678,
    "Cherrim-Overcast": 421, "Cherrim-Sunshine": 421,
    "Dudunsparce-Two-Segment": 982, "Dudunsparce-Three-Segment": 982,
    "Gimmighoul-Chest": 999, "Gimmighoul-Roaming": 999,
    "Ogerpon-Teal-Mask": 1017, "Ogerpon-Cornerstone-Mask": 1017,
    "Ogerpon-Wellspring-Mask": 1017, "Ogerpon-Hearthflame-Mask": 1017,
    "Palafin-Zero": 964, "Palafin-Hero": 964,
    "Urshifu-Single-Strike": 892, "Urshifu-Rapid-Strike": 892,
    "Eiscue-Ice": 875, "Eiscue-Noice": 875,
    "Rattata-Alolan": 19,
    "Raticate-Alolan": 20,
    "Raichu-Alolan": 26,
    "Sandshrew-Alolan": 27,
    "Sandslash-Alolan": 28,
    "Vulpix-Alolan": 37,
    "Ninetales-Alolan": 38,
    "Diglett-Alolan": 50,
    "Dugtrio-Alolan": 51,
    "Meowth-Alolan": 52,
    "Persian-Alolan": 53,
    "Geodude-Alolan": 74,
    "Graveler-Alolan": 75,
    "Golem-Alolan": 76,
    "Grimer-Alolan": 88,
    "Muk-Alolan": 89,
    "Exeggutor-Alolan": 103,
    "Marowak-Alolan": 105,
    "Meowth-Galarian": 52,
    "Ponyta-Galarian": 77,
    "Rapidash-Galarian": 78,
    "Farfetchd-Galarian": 83,
    "Weezing-Galarian": 110,
    "MrMime-Galarian": 122,
    "Articuno-Galarian": 144,
    "Zapdos-Galarian": 145,
    "Moltres-Galarian": 146,
    "Slowpoke-Galarian": 79,
    "Slowbro-Galarian": 80,
    "Slowking-Galarian": 199, 
    "Corsola-Galarian": 222,
    "Zigzagoon-Galarian": 263,
    "Linoone-Galarian": 264,
    "Darumaka-Galarian": 554,
    "Yamask-Galarian": 562,
    "Stunfisk-Galarian": 618,
    "Growlithe-Hisuian": 58,
    "Arcanine-Hisuian": 59,
    "Voltorb-Hisuian": 100,
    "Electrode-Hisuian": 101,
    "Typhlosion-Hisuian": 157,
    "Qwilfish-Hisuian": 211,
    "Sneasel-Hisuian": 215,
    "Zorua-Hisuian": 570,
    "Zoroark-Hisuian": 571,
    "Braviary-Hisuian": 628,
    "Samurott-Hisuian": 503,
    "Lilligant-Hisuian": 549,
    "Avalugg-Hisuian": 713,
    "Decidueye-Hisuian": 724,
    "Goodra-Hisuian": 706,
    "Sliggoo-Hisuian": 705,
    "Basculin-Hisuian": 550,
    "Dipplin" : 1011
    }

def format_iv(iv_dict):
    return " / ".join([f"{k}:{v}" for k, v in iv_dict.items()])

POKEBALL_EMOJIS = {
    "pokeball": "🔴",
    "superball": "🔵",
    "hyperball": "🟡",
    "masterball": "🟣"
}
RARITY_EMOJIS = {
    "common": "⚪",
    "uncommon": "🟢",
    "rare": "🔵",
    "epic": "🟣",
    "legendary": "🟡",
    "mythic": "🔴"
}
SORT_OPTIONS = [
    ("pokédex", "📚 Pokédex"),
    ("name", "🔤 Nom"),
    ("rarity", "⭐ Rareté"),
    ("level", "🔢 Niveau"),
    ("shiny", "✨ Shiny"),
    ("iv", "📊 IV")
]

def build_sort_keyboard(lang):
    return ReplyKeyboardMarkup(
        [
            [opt[1]] for opt in SORT_OPTIONS
        ] + [[get_text("menu_back", lang)]],
        resize_keyboard=True
    )

def get_pokedex_order(pkm_name):
    base = pkm_name.replace("shiny_", "")
    return POKEDEX_ORDER.get(base, 0)

def build_sort_keyboard(lang):
    return ReplyKeyboardMarkup(
        [[opt[1]] for opt in SORT_OPTIONS] + [[get_text("menu_back", lang)]],
        resize_keyboard=True
    )

def build_box_keyboard(lang, page, max_page):
    nav = []
    if page > 0:
        nav.append(get_text("previous_page", lang))
    if page < max_page:
        nav.append(get_text("next_page", lang))
    kb = [
        [get_text("button_sort_box", lang)],
        [get_text("button_sell_duplicates", lang)]
    ]
    if nav:
        kb.append(nav)
    kb.append([get_text("menu_back", lang)])
    return ReplyKeyboardMarkup(kb, resize_keyboard=True)

def format_pokemon_display(pkm, lang, box=None):
    name_key = pkm["name"].replace("shiny_", "")
    name = POKEMON_NAMES.get(name_key, {}).get(lang, name_key)
    shiny = "✨ " if pkm.get("shiny") is True else ""
    ball = POKEBALL_EMOJIS.get(pkm.get("caught_with"), "🎯")
    pokedex_id = pkm.get("pokedex_id") or get_pokedex_order(name_key)
    rarity = RARITY_EMOJIS.get(pkm.get("rarity", "common"), "❓")
    rarity_text = get_text(pkm.get("rarity", "common"), lang)
    level = pkm.get("level", 1)
    level_label = get_text("level_label", lang)

    # Gestion du nombre (quantité ou doublons physiques)
    if "quantity" in pkm:
        count = pkm["quantity"]
    elif box is not None:
        count = sum(1 for x in box if x["name"].replace("shiny_", "") == name_key)
    else:
        count = 1
    count_display = f" (x{count})" if count > 1 else ""

    # Natures
    selected_nature = pkm.get("selected_nature", pkm.get("nature"))
    natures_list = pkm.get("known_natures", []) or []
    natures_unique = []
    if selected_nature:
        natures_unique.append(selected_nature)
    natures_unique += [n for n in natures_list if n != selected_nature]
    natures_display = [
        f"✅ {NATURES.get(nat, {}).get(lang, nat)}" if nat == selected_nature else NATURES.get(nat, {}).get(lang, nat)
        for nat in natures_unique
    ]
    nature_line = f"{get_text('nature_label', lang)} : {', '.join(natures_display)}" if natures_display else ""

    # Talents
    ability = pkm.get("ability")
    abilities_list = pkm.get("known_abilities", []) or []
    abilities_unique = []
    if ability:
        abilities_unique.append(ability)
    abilities_unique += [ab for ab in abilities_list if ab != ability]
    abilities_display = [
        f"✅ {get_ability_name(ab, lang)}" if ab == ability else get_ability_name(ab, lang)
        for ab in abilities_unique
    ]
    ability_line = f"{get_text('abilities_label', lang)} : {', '.join(abilities_display)}" if abilities_display else ""

    # --- Talent caché (pareil ici pour hidden)
    hidden = pkm.get("hidden_ability")
    known_hidden = pkm.get("known_hidden_abilities", [])

    if hidden and hidden in known_hidden:
        hidden_line = f"{get_text('hidden_ability_label', lang)} : ✅ {get_ability_name(hidden, lang)}"
    elif hidden:
        hidden_line = f"{get_text('hidden_ability_label', lang)} : ❓"
    else:
        hidden_line = f"{get_text('hidden_ability_label', lang)} : {get_text('none', lang)}"

    # IVs
    ivs = pkm.get("ivs", {})
    iv_line = f"{get_text('ivs_label', lang)} : " + " / ".join(f"{k.upper()}:{v}" for k, v in ivs.items())

    rarity_line = f"{rarity} {get_text('rarity_label', lang)} {rarity_text}"

    lines = [
        f"{ball} #{pokedex_id} {name}{count_display} {shiny}\n",
        rarity_line,
        f"{level_label} : {level}",
        nature_line,
        ability_line,
        hidden_line,
        iv_line,
        "──────────────────"
    ]
    return "\n".join([l for l in lines if l.strip()])

async def show_box(update: Update, context: ContextTypes.DEFAULT_TYPE, page=0):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    box = data.get("box", [])
    if not box:
        await update.message.reply_text(get_text("box_empty", lang), reply_markup=main_menu(lang))
        return

    # Tri
    sort_type = context.user_data.get("box_sort", "pokédex")
    if sort_type == "name":
        box = sorted(box, key=lambda p: POKEMON_NAMES.get(p["name"].replace("shiny_", ""), {}).get(lang, p["name"]))
    elif sort_type == "rarity":
        box = sorted(box, key=lambda p: RARITY_ORDER.get(p.get("rarity", "common"), 0), reverse=True)
    elif sort_type == "level":
        box = sorted(box, key=lambda p: p.get("level", 1), reverse=True)
    elif sort_type == "shiny":
        box = sorted(box, key=lambda p: not p.get("shiny", False))
    elif sort_type == "iv":
        box = sorted(box, key=lambda p: sum(p.get("ivs", {}).values()), reverse=True)
    else:
        box = sorted(box, key=lambda p: get_pokedex_order(p["name"].replace("shiny_", "")))

    max_page = (len(box) - 1) // ITEMS_PER_PAGE
    page = max(0, min(page, max_page))
    user_box_pages[user.id] = page
    context.user_data["box_page"] = page

    start_index = page * ITEMS_PER_PAGE
    end_index = start_index + ITEMS_PER_PAGE
    message = f"📦 BOX — {get_text('box_page', lang, current=page + 1, total=max_page + 1)}\n\n"
    for pkm in box[start_index:end_index]:
        message += format_pokemon_display(pkm, lang, box=box) + "\n"
    await update.message.reply_text(message.strip(), reply_markup=build_box_keyboard(lang, page, max_page), parse_mode=None)

async def handle_sort_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    lang = load_user(user.id).get("lang", "fr")
    text = update.message.text.strip().lower()

    # Utilise le texte exact des boutons pour la navigation
    next_btn = get_text("next_page", lang).lower()
    prev_btn = get_text("previous_page", lang).lower()

    # Page suivante
    if text == next_btn or "suivant" in text or "next" in text or "▶" in text or "page suivante" in text:
        context.user_data["awaiting_sort_choice"] = False
        context.user_data["box_page"] = context.user_data.get("box_page", 0) + 1
        await show_box(update, context, page=context.user_data["box_page"])
        return
    # Page précédente
    if text == prev_btn or "précéd" in text or "prev" in text or "🔼" in text or "previous" in text or "page précédente" in text:
        context.user_data["awaiting_sort_choice"] = False
        context.user_data["box_page"] = max(context.user_data.get("box_page", 0) - 1, 0)
        await show_box(update, context, page=context.user_data["box_page"])
        return
    # Retour menu principal
    if any(x in text for x in ["retour", "back", "⬅"]):
        context.user_data.clear()
        await update.message.reply_text("⬅️ Retour au menu principal.", reply_markup=main_menu(lang))
        return

    # Critère de tri
    if context.user_data.get("awaiting_sort_choice"):
        for opt_key, opt_label in SORT_OPTIONS:
            if opt_label.lower() in text or opt_key in text:
                context.user_data["box_sort"] = opt_key
                context.user_data["awaiting_sort_choice"] = False
                await show_box(update, context)
                return
        await update.message.reply_text(get_text("invalid_sort_choice", lang), reply_markup=build_sort_keyboard(lang))
        return

    context.user_data["awaiting_sort_choice"] = True
    await update.message.reply_text(get_text("choose_sort_box", lang), reply_markup=build_sort_keyboard(lang))

async def sell_duplicates(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")
    box = data.get("box", [])

    sold = 0
    money_gained = 0

    def get_rarity_price(rarity):
        prices = {
            "common": 50,
            "uncommon": 150,
            "rare": 400,
            "epic": 1200,
            "legendary": 10000,
            "mythic": 50000
        }
        return prices.get(rarity, 100)

    rarity_counter = {
        "common": 0,
        "uncommon": 0,
        "rare": 0,
        "epic": 0,
        "legendary": 0,
        "mythic": 0
    }

    for pkm in box:
        if pkm.get("shiny"):
            continue
        qty = pkm.get("quantity", 1)
        if qty > 1:
            to_sell = qty - 1
            sold += to_sell
            rarity = pkm.get("rarity", "common")
            gain = get_rarity_price(rarity) * to_sell
            money_gained += gain
            rarity_counter[rarity] += to_sell
            pkm["quantity"] = 1

    data["money"] = data.get("money", 0) + money_gained
    save_user(user.id, data)

    if sold:
        lines = []
        for rarity, count in rarity_counter.items():
            if count > 0:
                rarity_label = get_text(rarity, lang)
                lines.append(get_text("rarity_sold_summary", lang, qty=count, rarity=rarity_label))
        msg = get_text("duplicates_sold_simple", lang, money=money_gained) + "\n\n" + "\n".join(lines)
    else:
        msg = get_text("no_duplicates", lang)

    await update.message.reply_text(msg, reply_markup=main_menu(lang))

async def handle_box_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = update.effective_user
    data = load_user(user.id)
    lang = data.get("lang", "fr")

    if query.data == "box_next":
        context.user_data["box_page"] = context.user_data.get("box_page", 0) + 1
    elif query.data == "box_prev":
        context.user_data["box_page"] = max(context.user_data.get("box_page", 0) - 1, 0)
    elif query.data == "main_menu":
        context.user_data["box_page"] = 0
        await query.message.delete()
        await query.message.reply_text(get_text("choose", lang), reply_markup=main_menu(lang))
        return

    await query.message.delete()
    await show_box(update, context, page=context.user_data.get("box_page", 0))