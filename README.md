# 🧬 PokeRealm - Bot Pokémon Telegram

PokeRealm est un bot Telegram ultra-complet inspiré de PokéMeow, offrant une **expérience stratégique fidèle et enrichie** de l'univers Pokémon. Il inclut **tous les Pokémon de toutes les générations**, des **systèmes de capture, de combat PvP, d'inventaire, de boutique, d'EV/IV**, et bien plus.

---

## 📦 Fonctionnalités principales

- 🎯 **Système de capture aléatoire** (shiny, IVs, nature, talents, etc.)
- 💰 **Économie complète** avec pokédollars, boutique, objets spéciaux et boosters
- 🧃 **Objets utilisables** pendant ou hors combat
- 📥 **Inventaire** catégorisé (Pokéballs, soins, boosts, objets tenus, etc.)
- 📘 **Box Pokémon** avec fusion automatique des doublons (IV, talent, nature)
- 🧠 **IA stratégique** avec calcul de type, faiblesse, priorité, statut, STAB, OHKO, etc.
- 🧗 **Tour Pokémon** avec étages à difficulté croissante
- ⚔️ **PvP** contre d'autres dresseurs en temps réel
- 🔄 **Commandes journalières** avec récompenses
- 🌐 **Multilingue** : 🇫🇷 Français et 🇬🇧 Anglais
- 📊 **Système complet de stats, EV/IV, talents normaux & cachés**
- 🔄 **Roulette de capture** optimisée avec une économie équilibrée

---

## 🎲 Chances de capture

| **Rareté**    | **Pokéball** | **Superball** | **Hyperball** |
| ------------- | ------------ | ------------- | ------------- |
| Commun        | 80%          | 90%           | 100%          |
| Uncommon      | 60%          | 75%           | 90%           |
| Rare          | 40%          | 60%           | 80%           |
| Épique (Epic) | 25%          | 45%           | 65%           |
| Légendaire    | 10%          | 25%           | 40%           |
| Mythique      | 5%           | 15%           | 30%           |

🔮 La **Masterball** offre un taux de capture de 100% pour tous les Pokémon.

---

## ✨ Autres probabilités importantes

- 🌟 Chance d'obtenir un Pokémon shiny : **1 / 4096**
- 🧬 Chance qu’un Pokémon ait son talent caché : **5%**
- 🧠 Bonus Chroma : +1% de chance de shiny par unité (stackable jusqu'à 10%)

---

## 🚀 Installation

```bash
git clone https://github.com/AD-nocap/PokeRealm.git
cd PokeRealm
pip install -r requirements.txt
python main.py
```

> Ajoute ton token Telegram dans `main.py` ou via une variable d’environnement.

---

## 📚 Exemples de commandes

- `/start` – Démarre ton aventure
- `/roulette` – Fais apparaître un Pokémon sauvage
- `/box` – Affiche tes Pokémon capturés
- `/shop` – Accès à la boutique
- `/daily` – Obtiens ta récompense journalière
- `/nature <nom> <nature>` – Change la nature active de ton Pokémon
- `/stats <nom>` – Affiche les stats et les IVs du Pokémon

---

## ✅ TODO

- [x] Ajout de tous les Pokémon de chaque génération
- [x] Gestion complète des objets et boutique
- [x] Système de roulette avec raretés et shiny
- [x] Stack automatique des IVs, talents et natures
- [x] Langue FR/EN
- [x] Gestion des talents cachés et actifs
- [x] Système de commandes Telegram avec boutons
- [x] Box triable avec fonctions de vente
- [ ] Combats PvP avec builds d’équipe
- [ ] Système de tour avec boss par étage
- [ ] Récompenses d’objectifs et quêtes

---

## 📁 Structure du projet

```
PokeRealm/
├── core/              # Logique interne (capture, combat, stats)
├── handlers/          # Commandes Telegram
├── data/              # Pokémon, attaques, talents, etc.
├── translations/      # Support multilingue
├── utils/             # Fonctions auxiliaires
├── main.py            # Lancement du bot
└── requirements.txt   # Dépendances
```

---

## 📜 Licence

Projet sous licence MIT – libre à modifier, distribuer et utiliser.

---

## ❤️ Contributeur principal

- **@ad_687** (Développeur principal)

---

## 📬 Contact

Pour toute question ou suggestion, contacte : [@ad_687](https://t.me/ad_687)

---

*Dernière mise à jour : 31/05/2025*
