# 📐 Diagrammes UML - Guide de Visualisation

## 📂 Fichiers Disponibles

```
backend/docs/uml/
├── use-case-diagram.puml        # Diagramme de Cas d'Utilisation
├── class-diagram.puml           # Diagramme de Classes (Modèle de Données)
├── component-diagram.puml       # Diagramme de Composants
├── sequence-application.puml    # Séquence: Candidature à une Mission
└── sequence-validation-hours.puml  # Séquence: Validation des Heures
```

## 🖼️ Visualisation des Diagrammes

### Méthode 1: PlantUML Online (Rapide)

1. **Ouvrir**: https://www.plantuml.com/plantuml/uml/
2. **Copier-coller** le contenu d'un fichier `.puml`
3. **Cliquer** sur "Submit" pour générer le diagramme
4. **Télécharger** en PNG, SVG ou PDF

### Méthode 2: Extension VS Code (Recommandé)

1. **Installer l'extension**: PlantUML (jebbs.plantuml)
2. **Installer Java** (requis): https://www.java.com/download/
3. **Ouvrir** un fichier `.puml`
4. **Aperçu**: `Alt + D` ou `Ctrl + Shift + P` → "PlantUML: Preview Current Diagram"
5. **Exporter**: `Ctrl + Shift + P` → "PlantUML: Export Current Diagram"

### Méthode 3: PlantUML Local (Avancé)

```bash
# Installer PlantUML
pip install plantuml

# Générer un diagramme en PNG
python -m plantuml backend/docs/uml/use-case-diagram.puml

# Générer tous les diagrammes
python -m plantuml backend/docs/uml/*.puml

# Résultat: fichiers PNG dans le même dossier
```

## 📊 Description des Diagrammes

### 1️⃣ Diagramme de Cas d'Utilisation

**Fichier**: `use-case-diagram.puml`

**Contenu**:
- **3 acteurs principaux** : Bénévole, Organisation, Administrateur
- **35 cas d'utilisation** couvrant toutes les fonctionnalités
- **Relations include/extend** : Dépendances entre cas d'utilisation
- **Notes** : Règles métier critiques

**À utiliser pour**:
- Présentation globale du système
- Compréhension des rôles et permissions
- Documentation fonctionnelle

---

### 2️⃣ Diagramme de Classes (Modèle de Données)

**Fichier**: `class-diagram.puml`

**Contenu**:
- **11 classes principales** : User, Volunteer, Organization, Mission, etc.
- **Attributs** avec types SQL
- **Méthodes** principales
- **Relations** avec cardinalités (1-1, 1-N, N-N)
- **Notes** : Règles de calcul de badge, validation compétences

**À utiliser pour**:
- Conception de la base de données
- Documentation technique
- Diagramme ER remplacé par diagramme de classes OOP

---

### 3️⃣ Diagramme de Composants

**Fichier**: `component-diagram.puml`

**Contenu**:
- **Frontend React** : Redux, Router, i18n
- **Backend Django** : API, Business Logic, Data Layer
- **PostgreSQL** : Tables, Index, Contraintes
- **Infrastructure** : Docker, CI/CD, Déploiement
- **Services externes** : Email, Stockage

**À utiliser pour**:
- Architecture technique globale
- Compréhension des flux de données
- Documentation DevOps

---

### 4️⃣ Diagramme de Séquence: Candidature à une Mission

**Fichier**: `sequence-application.puml`

**Scénario**: Un bénévole postule à une mission avec vérification des compétences

**Étapes**:
1. Authentification JWT
2. Vérification capacité mission (places disponibles)
3. Vérification candidature unique
4. **Vérification compétences requises validées** (règle métier critique)
5. Création de la candidature avec statut PENDING
6. Notification à l'organisation

**À utiliser pour**:
- Comprendre la logique de candidature
- Valider les règles métier
- Documentation des endpoints API

---

### 5️⃣ Diagramme de Séquence: Validation des Heures

**Fichier**: `sequence-validation-hours.puml`

**Scénario**: Organisation valide les heures d'un bénévole → Mise à jour badge automatique

**Étapes**:
1. Authentification Organisation
2. Vérification propriété mission
3. Vérification date fin mission
4. **Transaction ACID** (atomique)
5. Mise à jour participation (heures validées)
6. **Calcul automatique du nouveau badge** (BRONZE → SILVER)
7. Mise à jour statistiques bénévole
8. Notification au bénévole

**À utiliser pour**:
- Comprendre la logique de validation heures
- Valider le système de badges automatique
- Documentation des transactions BDD

---

## 🎯 Conformité Cahier des Charges

### Livrables UML Requis (Section 5)

| Livrable | Fichier | Statut |
|----------|---------|--------|
| ✅ Diagramme de Cas d'Utilisation | use-case-diagram.puml | Complet |
| ✅ Diagramme de Classes (Modèle de Données) | class-diagram.puml | Complet |
| ✅ Diagramme de Composants | component-diagram.puml | Complet |
| ✅ 2 Diagrammes de Séquence | sequence-*.puml | Complet |

**Total**: 5 diagrammes UML professionnels ✅

---

## 📝 Génération pour Rapport PDF

### Script de Génération Automatique

```bash
# backend/docs/generate_diagrams.sh

#!/bin/bash
echo "Génération des diagrammes UML..."

# Installer PlantUML si nécessaire
pip install plantuml

# Générer tous les diagrammes en PNG haute résolution
for file in backend/docs/uml/*.puml; do
    echo "Génération de $file..."
    python -m plantuml -tpng -Sbackground=white "$file"
done

echo "✓ Tous les diagrammes générés dans backend/docs/uml/"
echo "Fichiers PNG prêts pour inclusion dans le rapport"
```

### Pour Rapport LaTeX

```latex
% Dans votre rapport.tex

\section{Diagramme de Cas d'Utilisation}
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{backend/docs/uml/use-case-diagram.png}
\caption{Diagramme de Cas d'Utilisation - DZ-Volunteer}
\end{figure}

\section{Diagramme de Classes}
\begin{figure}[H]
\centering
\includegraphics[width=\textwidth]{backend/docs/uml/class-diagram.png}
\caption{Diagramme de Classes (Modèle de Données)}
\end{figure}
```

### Pour Rapport Word

1. Générer les PNG avec le script ci-dessus
2. Insérer → Image → Sélectionner le fichier PNG
3. Ajouter une légende (clic droit → Insérer une légende)

---

## 🔍 Vérification Qualité

### Checklist Diagrammes

- [x] **Use Case** : Tous les acteurs et cas d'utilisation principaux
- [x] **Classes** : Attributs, méthodes, relations, cardinalités
- [x] **Composants** : Architecture complète Frontend/Backend/BDD
- [x] **Séquences** : Scénarios critiques avec règles métier
- [x] **Lisibilité** : Notes explicatives, couleurs, organisation claire
- [x] **Conformité UML** : Notation standard respectée

---

## 📞 Support

Pour toute question sur les diagrammes :
1. Ouvrir le fichier `.puml` dans VS Code avec l'extension PlantUML
2. Consulter la documentation PlantUML : https://plantuml.com/
3. Vérifier la syntaxe : https://plantuml.com/fr/use-case-diagram

---

**Auteur** : Équipe DZ-Volunteer  
**Date** : 21 décembre 2025  
**Version** : 1.0
