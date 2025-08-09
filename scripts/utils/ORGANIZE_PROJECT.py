#!/usr/bin/env python3
"""
Script d'organisation automatique du projet ALX Project Nexus
Nettoie et organise tous les fichiers selon la structure appropriée
"""

import os
import shutil
from pathlib import Path
import json

class ProjectOrganizer:
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.docs_dir = self.project_root / "docs"
        self.scripts_dir = self.project_root / "scripts"
        self.moved_files = []
        self.deleted_files = []
        
    def organize_files(self):
        """Organise tous les fichiers selon la structure appropriée"""
        
        print("🧹 ORGANISATION AUTOMATIQUE DU PROJET ALX PROJECT NEXUS")
        print("=" * 60)
        
        # Fichiers à organiser par catégorie
        file_mappings = {
            # Documentation API
            "docs/api/": [
                "DOCUMENTATION_SWAGGER_FINALE.md",
                "SWAGGER_DOCUMENTATION_FINAL_REPORT.md",
                "REPONSE_FINALE_COMPLETE.md",
                "documentation_swagger_complete.json"
            ],
            
            # Guides utilisateur
            "docs/guides/": [
                "GUIDE_DEBUTANT_COMPLET.md",
                "GUIDE_ULTRA_SIMPLE.md"
            ],
            
            # Rapports finaux
            "docs/": [
                "FINAL_STATUS_REPORT.md",
                "PRESENTATION_ALX.md"
            ],
            
            # Scripts de test
            "scripts/tests/": [
                "TEST_FRONTEND_INTEGRATION.py",
                "TEST_CLARTE_DEBUTANT.py",
                "FINAL_VALIDATION_TEST.py",
                "TEST_COMPLET_FINAL.py",
                "TEST_ENDPOINTS_RAPIDE.py"
            ],
            
            # Scripts utilitaires
            "scripts/utils/": [
                "AUDIT_SWAGGER_COMPLET.py",
                "CONFIGURE_SWAGGER_ENGLISH.py",
                "SETUP_CELERY_SWAGGER.py",
                "SETUP_PRODUCTION_SWAGGER.py",
                "SWAGGER_INTERFACE_ALX.py",
                "SOLUTION_FINALE_ALX.py",
                "FIX_URGENCE_ALX.py"
            ]
        }
        
        # Fichiers à supprimer (temporaires/obsolètes)
        files_to_delete = [
            "TEST_RAPIDE_NAVIGATEUR.txt",
            "celerybeat-schedule"
        ]
        
        # Organiser les fichiers
        for target_dir, files in file_mappings.items():
            self._move_files_to_directory(target_dir, files)
        
        # Supprimer les fichiers obsolètes
        self._delete_obsolete_files(files_to_delete)
        
        # Créer un rapport d'organisation
        self._create_organization_report()
        
        print("\n✅ ORGANISATION TERMINÉE !")
        print(f"📁 Fichiers déplacés: {len(self.moved_files)}")
        print(f"🗑️ Fichiers supprimés: {len(self.deleted_files)}")
    
    def _move_files_to_directory(self, target_dir, files):
        """Déplace les fichiers vers le répertoire cible"""
        
        target_path = self.project_root / target_dir
        target_path.mkdir(parents=True, exist_ok=True)
        
        for filename in files:
            source_path = self.project_root / filename
            if source_path.exists():
                destination_path = target_path / filename
                
                try:
                    shutil.move(str(source_path), str(destination_path))
                    self.moved_files.append({
                        'file': filename,
                        'from': str(source_path),
                        'to': str(destination_path)
                    })
                    print(f"📁 Déplacé: {filename} → {target_dir}")
                except Exception as e:
                    print(f"❌ Erreur déplacement {filename}: {e}")
    
    def _delete_obsolete_files(self, files):
        """Supprime les fichiers obsolètes"""
        
        for filename in files:
            file_path = self.project_root / filename
            if file_path.exists():
                try:
                    if file_path.is_file():
                        file_path.unlink()
                    elif file_path.is_dir():
                        shutil.rmtree(file_path)
                    
                    self.deleted_files.append(filename)
                    print(f"🗑️ Supprimé: {filename}")
                except Exception as e:
                    print(f"❌ Erreur suppression {filename}: {e}")
    
    def _create_organization_report(self):
        """Crée un rapport d'organisation"""
        
        report = {
            "organization_date": "2025-01-09",
            "project_name": "ALX Project Nexus",
            "moved_files": self.moved_files,
            "deleted_files": self.deleted_files,
            "final_structure": self._get_project_structure()
        }
        
        report_path = self.docs_dir / "ORGANIZATION_REPORT.json"
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"📊 Rapport créé: {report_path}")
    
    def _get_project_structure(self):
        """Récupère la structure finale du projet"""
        
        structure = {}
        
        for root, dirs, files in os.walk(self.project_root):
            # Ignorer certains répertoires
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['venv', '__pycache__', 'staticfiles']]
            
            rel_path = os.path.relpath(root, self.project_root)
            if rel_path == '.':
                rel_path = 'root'
            
            structure[rel_path] = {
                'directories': dirs,
                'files': [f for f in files if not f.startswith('.') and not f.endswith('.pyc')]
            }
        
        return structure

def main():
    """Fonction principale"""
    
    # Détermine le répertoire racine du projet
    current_dir = Path(__file__).parent.parent.parent
    
    organizer = ProjectOrganizer(current_dir)
    organizer.organize_files()
    
    print("\n🎊 PROJET PARFAITEMENT ORGANISÉ !")
    print("\n📁 STRUCTURE FINALE:")
    print("├── docs/")
    print("│   ├── api/          # Documentation API")
    print("│   ├── guides/       # Guides utilisateur")
    print("│   └── *.md          # Rapports finaux")
    print("├── scripts/")
    print("│   ├── tests/        # Scripts de test")
    print("│   └── utils/        # Scripts utilitaires")
    print("└── social_media_backend/  # Code source")

if __name__ == "__main__":
    main()
