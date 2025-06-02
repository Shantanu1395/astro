#!/usr/bin/env python3
"""
Script to fix all import statements after restructuring
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path: Path, import_mappings: dict):
    """Fix imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Apply import mappings
        for old_import, new_import in import_mappings.items():
            # Handle different import patterns
            patterns = [
                f"from {old_import} import",
                f"import {old_import}",
            ]
            
            for pattern in patterns:
                if pattern in content:
                    if "from" in pattern:
                        content = content.replace(f"from {old_import} import", f"from {new_import} import")
                    else:
                        content = content.replace(f"import {old_import}", f"import {new_import}")
        
        # Write back if changed
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✅ Fixed imports in {file_path}")
            return True
        else:
            print(f"⏭️  No changes needed in {file_path}")
            return False
            
    except Exception as e:
        print(f"❌ Error fixing {file_path}: {e}")
        return False

def main():
    """Main function to fix all imports."""
    
    # Get project root
    project_root = Path(__file__).parent.parent
    
    print("🔧 FIXING IMPORTS AFTER RESTRUCTURING")
    print("=" * 50)
    
    # Define import mappings (old -> new)
    import_mappings = {
        # Models
        "models": "src.models.models",
        
        # Utils
        "utils": "src.utils.utils",
        "date_calculator": "src.utils.date_calculator",
        "personality_analysis_methods": "src.utils.personality_analysis_methods",
        
        # Core components
        "vedic_calculator": "src.core.vedic_calculator",
        "vedic_analysis": "src.core.vedic_analysis",
        "prediction_engine": "src.core.prediction_engine",
        "divisional_analyzer": "src.core.divisional_analyzer",
        "current_influences": "src.core.current_influences",
        "advanced_timing": "src.core.advanced_timing",
        "planetary_combination_descriptions": "src.core.planetary_combination_descriptions",
        "astrological_systems": "src.core.astrological_systems",
        "other_systems": "src.core.other_systems",
        "vedic_system": "src.core.vedic_system",
        
        # Services
        "specialized_engines": "src.services.specialized_engines",
        "engine_manager": "src.services.engine_manager",
        "pricing_system": "src.services.pricing_system",
        "system_manager": "src.services.system_manager",
        
        # Config
        "config": "config.config",
    }
    
    # Files to process
    files_to_process = []
    
    # Add all Python files in src/
    for root, dirs, files in os.walk(project_root / "src"):
        for file in files:
            if file.endswith('.py'):
                files_to_process.append(Path(root) / file)
    
    # Add test files
    for root, dirs, files in os.walk(project_root / "tests"):
        for file in files:
            if file.endswith('.py'):
                files_to_process.append(Path(root) / file)
    
    # Add config files
    for root, dirs, files in os.walk(project_root / "config"):
        for file in files:
            if file.endswith('.py'):
                files_to_process.append(Path(root) / file)
    
    print(f"📁 Found {len(files_to_process)} Python files to process")
    print()
    
    # Process each file
    fixed_count = 0
    for file_path in files_to_process:
        if fix_imports_in_file(file_path, import_mappings):
            fixed_count += 1
    
    print()
    print("=" * 50)
    print(f"✅ IMPORT FIXING COMPLETE!")
    print(f"📊 Fixed imports in {fixed_count} files")
    print(f"📁 Processed {len(files_to_process)} total files")
    print("=" * 50)

if __name__ == "__main__":
    main()
