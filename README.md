# Détecteur de brute-force SSH

Ce script Python simule un serveur SSH qui permet de détecter des attaques par force brute. Il écoute sur le port 22 (ou un autre) et loggue toutes les connexions entrantes. Si une adresse IP tente de se connecter plusieurs fois en peu de temps, une alerte est déclenchée.

## Fonctionnement

- Le script écoute sur le port 22 (par défaut)
- Il envoie une fausse bannière SSH pour paraître légitime
- Chaque tentative de connexion est enregistrée avec l’heure et l’adresse IP
- Si une adresse IP dépasse un certain nombre de tentatives en moins de 10 secondes, une alerte s’affiche

## Lancer le script

```bash
sudo python ssh_brute_detector.py
