# Cortana

[![Build Status](https://travis-ci.org/ValHook/Cortana.svg?branch=master)](https://travis-ci.org/ValHook/Cortana.svg?branch=master)

A useful bot to organize Destiny 2 raids in a Discord server.

### Usage
TODO: Translate to English.
```
Guide d'utilisation:
Cortana gère et génère les affiches d'un planning d'activités Destiny.
Elle connaît les noms et les niveaux d'expérience des joueurs de la FE11 et des clans alliés.
Ce guide détaille les commandes pour utiliser Cortana.
Dans toutes les commandes détaillées ci-dessous il faut savoir que: 

-[nom activité] doit être remplacé par un vrai nom, style calus, fleche, fleau, jds, couronne, etc...
Plusieurs formats sont supportés (e.g. leviathan, jardin du salut, couronne du malheur, flèche prestige, flèche d'étoiles prestige marchent aussi). Les fautes d'orthographe sont aussi gérées dans la limite du raisonnable. (e.g. kalus, fleo, devorer, etc... sont aussi supportés).

- (date) indique une date optionnelle. Plusieurs formats de date sont gérés (e.g. mercredi, 17/08, dimanche 21h, demain 22h30, 20/8 20h30, etc...)
La date est utile pour 2 cas de figures:
1) Afficher la date sur les affiches.
2) Différencier deux activités du même type dans une commande.
La date peut généralement être ignorée dans une commande qui modifie les détails d'une activité qui est la seule de son type dans le planning.

- [date] indique une date obligatoire. Par exemple pour la commande de modification d'une date d'activité.

- [gamer_tags] indique une liste de gamer tags (au minimum 1 gamer tag).
Cortana est capable de comprendre et corriger les gamer tags même si ils sont mal ortographiés. (e.g. cosa, croptus, darklight, franstuck, hartok etc...)


Liste des commandes: 

!cortana [nom activité] (date) [gamer_tag1, ...] => Créé/modifie une escouade pour/d'une activité. Précédez un gamer tag par '-' pour signaler que le joueur doit être retiré et non ajouté.

!cortana backup [nom activité] (date) [gamer_tag1, ...] => Pareil que la commande du dessus mais pour gérer les remplaçants.

!cortana date [nom activité] (ancienne date) [nouvelle date] => Ajoute ou modifie une date à une activité.

!cortana milestone [nom activité] (date) => Précise une save ou un statut pour l'activité concernée. (e.g. !cortana milestone jds save au boss, !cortana milestone leviathan prestige reporté).!cortana finish [nom activité] (date) => Marque l'activité comme terminée.

!cortana info [nom activité] (date) => Affiche les détails de l'activité dans un format texte.

!cortana clear [nom activité] (date) => Supprime l'activité du planning.

!cortana images => Génère les affiches pour toutes les activités du planning.

!cortana help => Affiche le guide d'utilisation.

!cortana infoall => Affiche tout le planning dans un format texte.

!cortana clearpast => Supprime toutes les activités des semaines précédentes.

!cortana clearall => Supprime toutes les activités.

!cortana sync => Synchronise la liste des joueurs et leurs stats.
Utile quand des nouveaux membres rejoignent le clan.
Utile pour que Cortana soit au courant des changements de niveaux d'expérience des joueurs.
Attention toutefois, les changements de niveaux d'expérience ne sont pas directement reflétés dans les affiches. Ils seront appliqués à partir des prochaines commandes (nouvelle création d'activité ou mise à jour d'escouade).

!cortana lastsync => Affiche la dernière date de synchronisation.

!cortana credits => Affiche les noms de mes créateurs.
```

### Build

You must have the following dependencies installed:
1. python3
2. bazel

Set your bungie API key and discord token in an environment variable:
```sh
export CORTANA_BUNGIE_API_KEY=...
export CORTANA_DISCORD_TOKEN=...
```

### Run
```sh
bazel run //bot
```

### Tests
Run all the workspace tests:
```sh
./check_tests.sh
```

Run linter checks (Only bazel and python files, no support for protos yet):
```sh
./check_lint.sh
```

Attempt fixing some of the lint mistakes (Only Bazel files, no support for python or protos yet):
```sh
./perform_lint.sh
```

