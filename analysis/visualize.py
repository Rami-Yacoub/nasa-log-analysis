#!/usr/bin/env python3
"""
Script de visualisation des resultats - Version Finale Optimisée
Compatible: Python 3.5+, Serveur sans ecran (Headless), Encodages mixtes
"""

import matplotlib
# Configuration du backend AVANT l'import de pyplot pour eviter l'erreur DISPLAY
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from collections import OrderedDict
import re
import os

# Configuration visuelle
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (15, 10)

def read_results(filename):
    """Lit un fichier de resultats MapReduce avec gestion d'erreurs d'encodage"""
    data = {}
    if not os.path.exists(filename):
        print("Avertissement: Fichier {} non trouve".format(filename))
        return {}
        
    try:
        # errors='ignore' permet de sauter les octets invalides (erreur 0x80)
        with open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) == 2:
                    key, value = parts
                    try:
                        data[key] = int(value)
                    except ValueError:
                        data[key] = value
    except Exception as e:
        print("Erreur lors de la lecture de {}: {}".format(filename, str(e)))
    return data

def plot_top_ips(input_file='output/job1_results.txt', top_n=10):
    """Graphique des Top IPs"""
    print("Generation du graphique Top IPs...")
    data = read_results(input_file)
    if not data: return
    
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    ips = [item[0] for item in sorted_data]
    counts = [item[1] for item in sorted_data]
    
    plt.figure(figsize=(12, 6))
    bars = plt.barh(range(len(ips)), counts, color='steelblue')
    plt.yticks(range(len(ips)), ips)
    plt.xlabel('Nombre de requetes')
    plt.title('Top {} des adresses IP les plus actives'.format(top_n), fontweight='bold')
    plt.gca().invert_yaxis()
    
    for i, count in enumerate(counts):
        plt.text(count + max(counts)*0.01, i, '{:,}'.format(count), va='center')
    
    plt.tight_layout()
    plt.savefig('output/viz_top_ips.png', dpi=300)
    print("Sauvegarde: output/viz_top_ips.png")
    plt.close()

def plot_http_codes(input_file='output/job2_results.txt'):
    """Graphique de distribution des codes HTTP"""
    print("Generation du graphique Codes HTTP...")
    data = read_results(input_file)
    if not data: return
    
    code_descriptions = {
        '200': '200 OK', '304': '304 Not Modif', '302': '302 Found',
        '404': '404 Not Found', '500': '500 Error', '403': '403 Forbidden'
    }
    
    labels = [code_descriptions.get(k, k) for k in data.keys()]
    values = list(data.values())
    
    plt.figure(figsize=(10, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, shadow=True)
    plt.title('Distribution des codes de statut HTTP', fontweight='bold')
    plt.axis('equal')
    plt.savefig('output/viz_http_codes.png', dpi=300)
    print("Sauvegarde: output/viz_http_codes.png")
    plt.close()

def plot_top_pages(input_file='output/job3_results.txt', top_n=15):
    """Graphique des pages les plus visitees"""
    print("Generation du graphique Top Pages...")
    data = read_results(input_file)
    if not data: return
    
    sorted_data = sorted(data.items(), key=lambda x: x[1], reverse=True)[:top_n]
    pages = [item[0][:50] + '...' if len(item[0]) > 50 else item[0] for item in sorted_data]
    counts = [item[1] for item in sorted_data]
    
    plt.figure(figsize=(12, 8))
    plt.barh(range(len(pages)), counts, color='#16a085')
    plt.yticks(range(len(pages)), pages)
    plt.title('Top {} des ressources les plus demandees'.format(top_n), fontweight='bold')
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('output/viz_top_pages.png', dpi=300)
    print("Sauvegarde: output/viz_top_pages.png")
    plt.close()

def plot_traffic_by_hour(input_file='output/job4_results.txt'):
    """Graphique du trafic par heure - Version compatible anciennes libs"""
    print("Generation du graphique Trafic par heure...")
    data = read_results(input_file)
    if not data: return
    
    # Tri robuste des heures
    try:
        hours_sorted = sorted(data.items(), key=lambda x: int(''.join(filter(str.isdigit, x[0]))))
    except:
        hours_sorted = sorted(data.items())

    hours_labels = [item[0] for item in hours_sorted]
    counts = [item[1] for item in hours_sorted]
    
    # ASTUCE : On utilise des positions numeriques (0, 1, 2...) pour l'axe X
    x_positions = range(len(hours_labels))
    
    plt.figure(figsize=(14, 6))
    
    # On trace en utilisant les positions numeriques
    plt.plot(x_positions, counts, marker='o', linewidth=2, color='#e74c3c')
    plt.fill_between(x_positions, counts, alpha=0.2, color='#e74c3c')
    
    # On remplace les chiffres (0, 1...) par les vrais noms ('00h', '01h'...)
    plt.xticks(x_positions, hours_labels, rotation=45)
    
    plt.title('Distribution du trafic par heure', fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('output/viz_traffic_by_hour.png', dpi=300)
    print("Sauvegarde: output/viz_traffic_by_hour.png")
    plt.close()

def plot_traffic_by_day(input_file='output/job5_results.txt'):
    """Graphique du trafic par jour"""
    print("Generation du graphique Trafic par jour...")
    data = read_results(input_file)
    if not data: return
    
    # Tri par date (clef)
    dates_sorted = sorted(data.items())
    dates = [item[0] for item in dates_sorted]
    counts = [item[1] for item in dates_sorted]
    
    plt.figure(figsize=(16, 6))
    plt.bar(range(len(dates)), counts, color='#3498db')
    step = max(1, len(dates) // 15)
    plt.xticks(range(0, len(dates), step), [dates[i] for i in range(0, len(dates), step)], rotation=45)
    plt.title('Evolution quotidienne du trafic', fontweight='bold')
    plt.tight_layout()
    plt.savefig('output/viz_traffic_by_day.png', dpi=300)
    print("Sauvegarde: output/viz_traffic_by_day.png")
    plt.close()

def plot_bandwidth(input_file='output/job6_results.txt'):
    """Graphique de la bande passante"""
    print("Generation du graphique Bande passante...")
    data = read_results(input_file)
    if not data: return
    
    dates_sorted = sorted(data.items())
    dates = [item[0] for item in dates_sorted]
    # Conversion en MB
    bandwidth_mb = [v / (1024 * 1024) for v in data.values()]
    
    plt.figure(figsize=(16, 6))
    plt.plot(range(len(dates)), bandwidth_mb, color='#9b59b6', marker='s')
    plt.title('Consommation de bande passante (MB)', fontweight='bold')
    plt.tight_layout()
    plt.savefig('output/viz_bandwidth.png', dpi=300)
    print("Sauvegarde: output/viz_bandwidth.png")
    plt.close()

def generate_summary_report():
    """Affiche un resume texte propre dans la console"""
    print("\n" + "="*60)
    print("             RESUME DE L'ANALYSE NASA")
    print("="*60)
    
    files = [
        ("Top IP", "output/job1_results.txt"),
        ("Code HTTP", "output/job2_results.txt"),
        ("Page Top", "output/job3_results.txt")
    ]

    for label, path in files:
        res = read_results(path)
        if res:
            top = max(res.items(), key=lambda x: x[1])
            print("{:<15} : {} ({} fois)".format(label, top[0], top[1]))
    print("="*60)

def main():
    # Creation du dossier output s'il n'existe pas
    if not os.path.exists('output'):
        os.makedirs('output')

    print("--- Debut du traitement des visualisations ---")
    
    plot_top_ips()
    plot_http_codes()
    plot_top_pages()
    plot_traffic_by_hour()
    plot_traffic_by_day()
    plot_bandwidth()
    
    print("\n[SUCCESS] Toutes les images ont ete creees dans le dossier 'output/'")
    generate_summary_report()

if __name__ == "__main__":
    main()