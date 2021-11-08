#!/bin/bash

touch .env
echo "Génération du fichier d'environement : "
read -p "Port API: " API_PORT
read -p "Port de l'application web: " APP_PORT
read -p "Chemin vers les sources de l'application web: " APP_SOURCES

echo "API_PORT="$API_PORT"
APP_PORT="$APP_PORT"
APP_SOURCES="$APP_SOURCES > .env
echo "Génération terminée" 
