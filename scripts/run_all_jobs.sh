#!/bin/bash

echo "========================================="
echo "Exécution de tous les jobs MapReduce"
echo "========================================="

# Couleurs
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Variables
INPUT_PATH="/user/hadoop/nasa-logs/input/access.log"
OUTPUT_BASE="/user/hadoop/nasa-logs/output"

# ========================================
# CORRECTION : Trouver le BON JAR
# ========================================
# Exclure les JARs sources et tests
STREAMING_JAR=$(find /usr/local/hadoop -name "hadoop-streaming*.jar" 2>/dev/null | grep -v "sources" | grep -v "test" | head -1)

# Si non trouvé, essayer $HADOOP_HOME
if [ -z "$STREAMING_JAR" ]; then
    STREAMING_JAR=$(find $HADOOP_HOME -name "hadoop-streaming*.jar" 2>/dev/null | grep -v "sources" | grep -v "test" | head -1)
fi

# Si toujours pas trouvé, essayer /opt/hadoop
if [ -z "$STREAMING_JAR" ]; then
    STREAMING_JAR=$(find /opt/hadoop -name "hadoop-streaming*.jar" 2>/dev/null | grep -v "sources" | grep -v "test" | head -1)
fi

# En dernier recours, chemin par défaut
if [ -z "$STREAMING_JAR" ]; then
    STREAMING_JAR="/usr/local/hadoop/share/hadoop/tools/lib/hadoop-streaming-2.7.2.jar"
fi

# Vérifier que le JAR existe
if [ ! -f "$STREAMING_JAR" ]; then
    echo -e "${RED}❌ Erreur: JAR Hadoop Streaming introuvable${NC}"
    echo ""
    echo "Recherche manuelle des JARs disponibles :"
    find /usr/local/hadoop -name "*streaming*.jar" 2>/dev/null
    find $HADOOP_HOME -name "*streaming*.jar" 2>/dev/null
    find /opt/hadoop -name "*streaming*.jar" 2>/dev/null
    exit 1
fi

# Vérifier que ce n'est pas un JAR sources/test
if echo "$STREAMING_JAR" | grep -q "sources\|test"; then
    echo -e "${RED}❌ Erreur: Le JAR trouvé est un JAR sources/test${NC}"
    echo "JAR actuel : $STREAMING_JAR"
    echo ""
    echo "Recherche du bon JAR :"
    find /usr/local/hadoop -name "hadoop-streaming*.jar" | grep -v "sources" | grep -v "test"
    exit 1
fi

echo -e "${GREEN}✓ JAR Hadoop Streaming trouvé: ${STREAMING_JAR}${NC}"

# Fonction pour exécuter un job
run_job() {
    local job_name=$1
    local job_number=$2
    local job_dir=$3
    local mapper_path="src/${job_dir}/mapper.py"
    local reducer_path="src/${job_dir}/reducer.py"
    
    echo -e "\n${BLUE}=========================================${NC}"
    echo -e "${BLUE}Job ${job_number}: ${job_name}${NC}"
    echo -e "${BLUE}=========================================${NC}"
    
    # Vérifier que les fichiers existent
    if [ ! -f "${mapper_path}" ]; then
        echo -e "${RED}❌ Erreur: ${mapper_path} n'existe pas${NC}"
        return 1
    fi
    
    if [ ! -f "${reducer_path}" ]; then
        echo -e "${RED}❌ Erreur: ${reducer_path} n'existe pas${NC}"
        return 1
    fi
    
    # Supprimer l'ancien output
    echo -e "${YELLOW}Nettoyage de l'ancien output...${NC}"
    hdfs dfs -rm -r -f ${OUTPUT_BASE}/job${job_number} 2>/dev/null
    
    # Rendre les scripts exécutables
    chmod +x ${mapper_path}
    chmod +x ${reducer_path}
    
    # Exécuter le job
    echo -e "${BLUE}Lancement du job MapReduce...${NC}"
    hadoop jar ${STREAMING_JAR} \
        -files ${mapper_path},${reducer_path} \
        -mapper "python3 mapper.py" \
        -reducer "python3 reducer.py" \
        -input ${INPUT_PATH} \
        -output ${OUTPUT_BASE}/job${job_number}
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Job ${job_number} terminé avec succès!${NC}"
        
        # Afficher un aperçu des résultats
        echo -e "${BLUE}Aperçu des résultats (10 premières lignes):${NC}"
        hdfs dfs -cat ${OUTPUT_BASE}/job${job_number}/part-00000 2>/dev/null | head -10
    else
        echo -e "${RED}✗ Erreur lors de l'exécution du job ${job_number}${NC}"
        echo -e "${YELLOW}Vérifiez les logs YARN pour plus de détails${NC}"
        return 1
    fi
}

# Vérifier que le fichier d'entrée existe
echo -e "${BLUE}Vérification du fichier d'entrée...${NC}"
if ! hdfs dfs -test -e ${INPUT_PATH}; then
    echo -e "${RED}❌ Erreur: Le fichier ${INPUT_PATH} n'existe pas dans HDFS${NC}"
    echo "Exécutez d'abord: ./scripts/upload_data.sh"
    exit 1
fi

echo -e "${GREEN}✓ Fichier d'entrée trouvé${NC}"
hdfs dfs -du -h ${INPUT_PATH}

# Vérifier que tous les scripts Python existent
echo -e "\n${BLUE}Vérification des scripts Python...${NC}"
MISSING=0
for job in "Job1_TopIPs" "Job2_HTTPCodes" "Job3_TopPages" "Job4_TrafficByHour" "Job5_Browsers" "Job6_BandwidthByDay"; do
    if [ ! -f "src/${job}/mapper.py" ] || [ ! -f "src/${job}/reducer.py" ]; then
        echo -e "${RED}✗ Scripts manquants dans src/${job}/${NC}"
        MISSING=1
    else
        echo -e "${GREEN}✓ src/${job}/ OK${NC}"
    fi
done

if [ $MISSING -eq 1 ]; then
    echo -e "${RED}❌ Des scripts Python sont manquants. Vérifiez votre structure.${NC}"
    exit 1
fi

# Exécuter tous les jobs
echo -e "\n${BLUE}=========================================${NC}"
echo -e "${BLUE}Démarrage de l'exécution des 6 jobs...${NC}"
echo -e "${BLUE}=========================================${NC}"

run_job "Top IPs les plus actives" 1 "Job1_TopIPs"

run_job "Distribution des codes HTTP" 2 "Job2_HTTPCodes"

run_job "Pages les plus visitées" 3 "Job3_TopPages"

run_job "Trafic par heure de la journée" 4 "Job4_TrafficByHour"

run_job "Navigateurs les plus utilisés" 5 "Job5_Browsers"

run_job "Bande passante par jour" 6 "Job6_BandwidthByDay"

echo -e "\n${GREEN}========================================="
echo "✓ Tous les jobs sont terminés!"
echo "=========================================${NC}"

# Afficher la liste des outputs
echo -e "\n${BLUE}Liste des outputs dans HDFS:${NC}"
hdfs dfs -ls ${OUTPUT_BASE}/

# Statistiques
echo -e "\n${BLUE}Taille des outputs:${NC}"
hdfs dfs -du -h ${OUTPUT_BASE}/

echo -e "\n${BLUE}Pour télécharger les résultats, exécutez:${NC}"
echo -e "${YELLOW}./scripts/download_results.sh${NC}"