#!/usr/bin/env python3
"""
Utility script to manage utterance output folders
"""

import os
import shutil
from datetime import datetime, timedelta


def list_output_folders():
    """List all utterance output folders."""
    folders = []
    for item in os.listdir('.'):
        if os.path.isdir(item) and item.startswith('utterance_outputs_'):
            folders.append(item)
    return sorted(folders)


def clean_old_folders(days_old=7):
    """Clean folders older than specified days."""
    cutoff_date = datetime.now() - timedelta(days=days_old)
    cleaned = []
    
    for folder in list_output_folders():
        try:
            # Extract date from folder name
            date_str = folder.replace('utterance_outputs_', '')
            folder_date = datetime.strptime(date_str, '%Y%m%d')
            
            if folder_date < cutoff_date:
                shutil.rmtree(folder)
                cleaned.append(folder)
                print(f"🗑️  Cleaned old folder: {folder}")
        except ValueError:
            print(f"⚠️  Skipped folder with invalid date format: {folder}")
    
    return cleaned


def show_folder_stats():
    """Show statistics about output folders."""
    folders = list_output_folders()
    
    if not folders:
        print("No output folders found.")
        return
    
    print(f"📊 Found {len(folders)} output folder(s):")
    
    total_files = 0
    for folder in folders:
        files = [f for f in os.listdir(folder) if f.endswith('.csv')]
        total_files += len(files)
        print(f"   📁 {folder}: {len(files)} CSV files")
    
    print(f"\nTotal CSV files: {total_files}")


def main():
    """Main utility function."""
    print("🗂️  Utterance Output Folder Manager")
    print("=" * 40)
    
    while True:
        print("\nOptions:")
        print("1. List output folders")
        print("2. Show folder statistics")
        print("3. Clean old folders (7+ days)")
        print("4. Exit")
        
        choice = input("\nSelect option (1-4): ").strip()
        
        if choice == '1':
            folders = list_output_folders()
            if folders:
                print(f"\n📁 Output folders:")
                for folder in folders:
                    print(f"   {folder}")
            else:
                print("\nNo output folders found.")
        
        elif choice == '2':
            print()
            show_folder_stats()
        
        elif choice == '3':
            print("\n🧹 Cleaning folders older than 7 days...")
            cleaned = clean_old_folders(7)
            if cleaned:
                print(f"Cleaned {len(cleaned)} folders.")
            else:
                print("No old folders to clean.")
        
        elif choice == '4':
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()