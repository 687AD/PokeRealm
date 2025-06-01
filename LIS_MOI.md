🇬🇧 Ce projet est aussi disponible en anglais : [README.md](./README.md)

# 🧬 PokeRealm - Bot Pokémon Telegram

PokeRealm est un bot Telegram ultra-complet inspiré de PokéMeow, offrant une **expérience stratégique fidèle et enrichie** de l'univers Pokémon. Il inclut **tous les Pokémon de toutes les générations**, des **systèmes de capture, de combat PvP, d'inventaire, de boutique, d'EV/IV**, et bien plus.

---

## 📦 Fonctionnalités principales

- 🎯 Apparitions aléatoires de Pokémon (shiny, IV, nature, talents normaux/cachés)
- 📥 Inventaire complet avec objets catégorisés (Pokéballs, boosts, soins, etc.)
- 📘 Boîte Pokémon avec fusion automatique des doublons (IV, talent, nature)
- 🧠 Moteur de combat stratégique : effets de statut, priorités, types, STAB, etc.
- 💰 Économie complète avec Pokédollars, boutique, objets
- 🧗 Tour Pokémon à difficulté croissante
- ⚔️ PvP contre d'autres joueurs (en cours)
- 🔁 Récompenses journalières et système de connexion
- 🌐 Multilingue : 🇫🇷 Français et 🇬🇧 Anglais
- 🧬 Système complet de stats, EV/IV, talents et fusion intelligente

---

## 🎲 Chances de capture

| **Rareté**    | **Pokéball** | **Superball** | **Hyperball** |
| ------------- | ------------ | ------------- | ------------- |
| Commun        | 80%          | 90%           | 100%          |
| Peu commun    | 60%          | 75%           | 90%           |
| Rare          | 40%          | 60%           | 80%           |
| Épique        | 25%          | 45%           | 65%           |
| Légendaire    | 10%          | 25%           | 40%           |
| Mythique      | 5%           | 15%           | 30%           |

> 🎯 **Masterball** : capture garantie à 100%

---

## ✨ Probabilités spéciales

- ⭐ Chance de shiny : **1 / 4096**  
- 🧬 Talent caché : **5%**  
- ✨ **Charme Chroma** : +5% de chance de shiny

---

## 📚 Exemples de commandes

- `/start` – Lance ton aventure
- `/roulette` – Rencontre un Pokémon sauvage
- `/box` – Affiche ta collection de Pokémon
- `/shop` – Accède à la boutique
- `/daily` – Récupère ta récompense quotidienne
- `/nature <nom> <nature>` – Change la nature active d’un Pokémon
- `/stats <nom>` – Affiche les stats, IVs, natures et talents

---

## ✅ À faire

- [x] Tous les Pokémon de toutes les générations
- [x] Boutique et objets fonctionnels
- [x] Roulette avec raretés et shiny
- [x] Fusion automatique des IV, talents, nature
- [x] Support multilingue
- [x] Gestion des talents normaux et cachés
- [x] UI Telegram avec boutons
- [x] Tri de la box et vente des doublons
- [ ] Système de PvP avec création d'équipe
- [ ] Tour avec boss à chaque étage
- [ ] Récompenses de quêtes et objectifs

---

## 🗂️ Arborescence du projet

```
PokeRealm/
├── core/              # Logique (combat, données Pokémon, etc.)
├── handlers/          # Commandes Telegram
├── data/              # Pokémon, attaques, talents
├── translations/      # Fichiers multilingues
├── utils/             # Fonctions auxiliaires
├── main.py            # Lancement du bot
└── requirements.txt   # Dépendances Python
```

---

## 📜 Licence

Projet sous licence MIT – libre à modifier, partager et utiliser.

---

## 👤 Développeur principal

- **@ad_687**

---

## 📬 Contact

Pour toute suggestion ou retour : [@ad_687 sur Telegram](https://t.me/ad_687)

---

*Dernière mise à jour : 31/05/2025*
