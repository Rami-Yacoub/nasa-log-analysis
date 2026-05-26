#!/bin/bash

echo "==================================="
echo "Upload du dataset vers HDFS"
echo "==================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

# Vérifier si le fichier existe
if [ ! -f "datasets/access.log" ]; then
    echo -e "${RED}❌ Erreur: datasets/access.log n'existe pas${NC}"
    echo "Téléchargez le dataset depuis Kaggle:"
    echo "https://www.kaggle.com/datasets/adchatakora/nasa-http-access-logs"
    exit 1
fi

# Créer le répertoire dans HDFS
echo -e "${BLUE}Création du répertoire /user/hadoop/nasa-logs dans HDFS...${NC}"
hdfs dfs -mkdir -p /user/hadoop/nasa-logs/input

# Supprimer l'ancien fichier s'il existe
echo -e "${BLUE}Nettoyage des anciennes données...${NC}"
hdfs dfs -rm -f /user/hadoop/nasa-logs/input/access.log 2>/dev/null

# Upload du fichier
echo -e "${BLUE}Upload de access.log vers HDFS...${NC}"
hdfs dfs -put datasets/access.log /user/hadoop/nasa-logs/input/

# Vérification
echo -e "${BLUE}Vérification...${NC}"
hdfs dfs -ls /user/hadoop/nasa-logs/input/

FILE_SIZE=$(hdfs dfs -du -h /user/hadoop/nasa-logs/input/access.log | awk '{print $1" "$2}')
echo -e "${GREEN}✓ Upload réussi! Taille: ${FILE_SIZE}${NC}"

echo -e "\n${GREEN}==================================="
echo "Upload terminé avec succès!"
echo "===================================${NC}"