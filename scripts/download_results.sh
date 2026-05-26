#!/bin/bash

echo "========================================="
echo "Téléchargement des résultats depuis HDFS"
echo "========================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variables
OUTPUT_BASE="/user/hadoop/nasa-logs/output"
LOCAL_OUTPUT="output"

# Créer le dossier local
mkdir -p ${LOCAL_OUTPUT}

echo -e "${BLUE}Téléchargement des résultats...${NC}\n"

# Fonction pour télécharger les résultats d'un job
download_job() {
    local job_number=$1
    local job_name=$2
    
    echo -e "${BLUE}Job ${job_number}: ${job_name}${NC}"
    
    if hdfs dfs -test -e ${OUTPUT_BASE}/job${job_number}; then
        hdfs dfs -getmerge ${OUTPUT_BASE}/job${job_number}/part-* ${LOCAL_OUTPUT}/job${job_number}_results.txt 2>/dev/null
        
        if [ $? -eq 0 ]; then
            SIZE=$(ls -lh ${LOCAL_OUTPUT}/job${job_number}_results.txt | awk '{print $5}')
            echo -e "${GREEN}✓ Téléchargé (${SIZE})${NC}"
        else
            echo -e "${RED}✗ Erreur lors du téléchargement${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ Output non trouvé dans HDFS${NC}"
    fi
}

# Télécharger tous les jobs
download_job 1 "Top IPs"
download_job 2 "Codes HTTP"
download_job 3 "Top Pages"
download_job 4 "Trafic par heure"
download_job 5 "Navigateurs"
download_job 6 "Bande passante"

echo -e "\n${GREEN}========================================="
echo "✓ Téléchargement terminé!"
echo "=========================================${NC}"

# Afficher les statistiques
echo -e "\n${BLUE}Fichiers téléchargés:${NC}"
ls -lh ${LOCAL_OUTPUT}/

echo -e "\n${BLUE}Aperçu des résultats:${NC}"
for i in {1..6}; do
    if [ -f "${LOCAL_OUTPUT}/job${i}_results.txt" ]; then
        echo -e "\n${YELLOW}=== Job ${i} (5 premières lignes) ===${NC}"
        head -5 ${LOCAL_OUTPUT}/job${i}_results.txt
    fi
done

echo -e "\n${BLUE}Pour générer les visualisations, exécutez:${NC}"
echo -e "${YELLOW}python3 analysis/visualize.py${NC}"