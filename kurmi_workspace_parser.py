#!/usr/bin/env python3
"""
Kurmi Workspace Parser
Parses Kurmi workspace export files and organizes them into categorized folders.
"""

import os
import sys
import shutil
import zipfile
import argparse
import tempfile
import logging
from pathlib import Path
from typing import List, Dict, Tuple

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/opt/workspace_parser/parser.log')
    ]
)
logger = logging.getLogger(__name__)


class KurmiWorkspaceParser:
    """Parser for Kurmi workspace export files."""

    # Category definitions with file patterns
    CATEGORIES = {
        'service_definitions': {
            'patterns': ['*.service.xml', '*.serviceorder.json'],
            'description': 'Kurmi service definitions'
        },
        'service_inference': {
            'patterns': ['*.inference.js'],
            'description': 'Kurmi service inference files'
        },
        'quickfeatures': {
            'patterns': ['*.quickfeature.xml', '*.quickfeature.js', '*.quickfeature.properties'],
            'description': 'QuickFeature files (JS/XML/properties)'
        },
        'js_libraries': {
            'patterns': ['*.util.js', '*.apiutil.js', '*.postProcessing.js', '*.builtin.util.js'],
            'description': 'JavaScript libraries and utilities'
        },
        'widgets': {
            'patterns': ['*.widget.js'],
            'description': 'Widget files'
        },
        'scenarios': {
            'patterns': ['*.scenario.json', '*.schema.json', '*.rules.json', '*.data.json', '*.options.json', '*.choice.json', '*.kurmiApi.js', '*.configuration.js', '*.import.js', '*.export.js', '*.externalTask.js', '*.processing.js', '*.discovery.js', '*.ruleSet.json', '*.componentAdjustment.js', '*.mergeAdjust.js'],
            'description': 'Scenario files, schemas, rules, and related libraries'
        },
        'connectors': {
            'patterns': ['*.advancedConnector.xml', '*.connector.xml', '*.connector.properties'],
            'description': 'Connector files (XML/properties)'
        },
        'directory_connectors': {
            'patterns': ['*.directoryModel.xml'],
            'description': 'Directory connector files'
        },
        'emails': {
            'patterns': ['*.mail.js'],
            'description': 'Email template files'
        }
    }

    def __init__(self, workspace_zip: str, output_dir: str, categories: List[str] = None):
        """
        Initialize the parser.

        Args:
            workspace_zip: Path to the workspace export zip file
            output_dir: Directory where categorized files will be output
            categories: List of categories to parse (None = all categories)
        """
        self.workspace_zip = Path(workspace_zip)
        self.output_dir = Path(output_dir)
        self.categories_to_parse = categories if categories else list(self.CATEGORIES.keys())
        self.temp_dir = None
        self.stats = {category: 0 for category in self.categories_to_parse}

        # Validate inputs
        if not self.workspace_zip.exists():
            raise FileNotFoundError(f"Workspace zip not found: {self.workspace_zip}")

        logger.info(f"Initialized parser for: {self.workspace_zip}")
        logger.info(f"Output directory: {self.output_dir}")
        logger.info(f"Categories to parse: {', '.join(self.categories_to_parse)}")

    def extract_workspace(self) -> Path:
        """Extract workspace zip to temporary directory."""
        logger.info("Extracting workspace zip file...")
        self.temp_dir = tempfile.mkdtemp(prefix='kurmi_workspace_')
        temp_path = Path(self.temp_dir)

        try:
            with zipfile.ZipFile(self.workspace_zip, 'r') as zip_ref:
                zip_ref.extractall(temp_path)
            logger.info(f"Extracted to temporary directory: {temp_path}")
            return temp_path
        except Exception as e:
            logger.error(f"Failed to extract workspace: {e}")
            raise

    def matches_pattern(self, filename: str, patterns: List[str]) -> bool:
        """
        Check if filename matches any of the given patterns.

        Args:
            filename: Name of the file to check
            patterns: List of glob patterns (e.g., '*.service.xml')

        Returns:
            True if filename matches any pattern, False otherwise
        """
        file_path = Path(filename)
        for pattern in patterns:
            # Convert glob pattern to check
            # For example: '*.service.xml' checks if filename ends with '.service.xml'
            if pattern.startswith('*'):
                suffix = pattern[1:]  # Remove the '*'
                if filename.endswith(suffix):
                    return True
        return False

    def get_category_for_file(self, filename: str) -> str:
        """
        Determine which category a file belongs to.

        Args:
            filename: Name of the file

        Returns:
            Category name or None if file doesn't match any category
        """
        for category in self.categories_to_parse:
            patterns = self.CATEGORIES[category]['patterns']
            if self.matches_pattern(filename, patterns):
                return category
        return None

    def copy_file_preserving_structure(self, source_file: Path, base_dir: Path, category: str):
        """
        Copy file to category folder while preserving relative folder structure.

        Args:
            source_file: Full path to source file
            base_dir: Base directory (extracted workspace root)
            category: Category name for output folder
        """
        # Get relative path from base directory
        relative_path = source_file.relative_to(base_dir)

        # Create destination path
        dest_path = self.output_dir / category / relative_path

        # Create parent directories if they don't exist
        dest_path.parent.mkdir(parents=True, exist_ok=True)

        # Copy file
        shutil.copy2(source_file, dest_path)
        logger.debug(f"Copied: {relative_path} -> {category}/")

    def parse_workspace(self):
        """Main parsing logic."""
        try:
            # Extract workspace
            extracted_path = self.extract_workspace()

            # Create output directory
            self.output_dir.mkdir(parents=True, exist_ok=True)

            # Walk through all files in extracted workspace
            logger.info("Starting file categorization...")
            for root, dirs, files in os.walk(extracted_path):
                for filename in files:
                    # Skip workspace.txt
                    if filename == 'workspace.txt':
                        continue

                    # Determine category
                    category = self.get_category_for_file(filename)

                    if category:
                        source_file = Path(root) / filename
                        self.copy_file_preserving_structure(source_file, extracted_path, category)
                        self.stats[category] += 1

            # Log statistics
            logger.info("=" * 60)
            logger.info("PARSING COMPLETE - STATISTICS")
            logger.info("=" * 60)
            total_files = 0
            for category in self.categories_to_parse:
                count = self.stats[category]
                total_files += count
                description = self.CATEGORIES[category]['description']
                logger.info(f"{category:25s}: {count:4d} files - {description}")
            logger.info("=" * 60)
            logger.info(f"{'TOTAL':25s}: {total_files:4d} files")
            logger.info("=" * 60)

        except Exception as e:
            logger.error(f"Error during parsing: {e}")
            raise
        finally:
            # Clean up temporary directory
            if self.temp_dir and os.path.exists(self.temp_dir):
                logger.info(f"Cleaning up temporary directory: {self.temp_dir}")
                shutil.rmtree(self.temp_dir)

    def get_stats(self) -> Dict[str, int]:
        """Return parsing statistics."""
        return self.stats.copy()


def scan_for_workspace_files(directory="."):
    """
    Scan directory for Kurmi workspace files.

    Args:
        directory: Directory to scan (default: current directory)

    Returns:
        List of workspace file paths
    """
    import glob

    # Look for .configfile.zip files
    pattern = os.path.join(directory, "*.configfile.zip")
    workspace_files = glob.glob(pattern)

    # Also check in workspaceExport subdirectory if it exists
    workspace_export_dir = os.path.join(directory, "workspaceExport")
    if os.path.exists(workspace_export_dir):
        pattern = os.path.join(workspace_export_dir, "*.configfile.zip")
        workspace_files.extend(glob.glob(pattern))

    # Sort by modification time (newest first)
    workspace_files.sort(key=lambda x: os.path.getmtime(x), reverse=True)

    return workspace_files


def interactive_workspace_selection(workspace_files):
    """
    Interactive workspace file selection menu.

    Args:
        workspace_files: List of workspace file paths

    Returns:
        Selected workspace file path or None
    """
    if not workspace_files:
        print("\n" + "=" * 70)
        print("ERROR: No workspace files found!")
        print("=" * 70)
        print("\nPlease ensure you have Kurmi workspace export files (*.configfile.zip)")
        print("in the current directory or workspaceExport/ subdirectory.")
        print("=" * 70 + "\n")
        return None

    while True:
        print("\n" * 2)
        print("=" * 70)
        print("SELECT WORKSPACE FILE TO PARSE")
        print("=" * 70)
        print()

        # Display workspace files
        for idx, filepath in enumerate(workspace_files, 1):
            filename = os.path.basename(filepath)
            # Get file size
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            # Get modification time
            import time
            mtime = time.strftime('%Y-%m-%d %H:%M', time.localtime(os.path.getmtime(filepath)))
            print(f"  {idx}. {filename}")
            print(f"     Size: {size_mb:.2f} MB | Modified: {mtime}")
            print()

        print("=" * 70)
        print("Enter the number of the workspace file to parse (or 'q' to quit)")
        print("=" * 70)

        user_input = input("\nYour choice: ").strip().lower()

        if user_input == 'q':
            return None

        try:
            choice = int(user_input)
            if 1 <= choice <= len(workspace_files):
                selected_file = workspace_files[choice - 1]
                print(f"\nSelected: {os.path.basename(selected_file)}")
                return selected_file
            else:
                print(f"\nInvalid choice. Please enter a number between 1 and {len(workspace_files)}")
        except ValueError:
            print("\nInvalid input. Please enter a number or 'q' to quit")


def interactive_category_selection(available_categories):
    """
    Interactive category selection menu.

    Args:
        available_categories: Dictionary of category names and their info

    Returns:
        List of selected category names
    """
    # Start with all categories selected
    selected = {cat: True for cat in available_categories.keys()}

    while True:
        # Clear screen (optional - comment out if not desired)
        print("\n" * 2)

        print("=" * 70)
        print("SELECT CATEGORIES TO EXTRACT")
        print("=" * 70)
        print()

        # Display categories with selection state
        category_list = list(available_categories.keys())
        for idx, category in enumerate(category_list, 1):
            checkbox = "[x]" if selected[category] else "[ ]"
            desc = available_categories[category]['description']
            print(f"  {idx}. {checkbox} {category:25s} - {desc}")

        print()
        print("=" * 70)
        print("Commands:")
        print("  - Enter numbers to toggle (e.g., 1,3,5 or 1-3)")
        print("  - Type 'all' to select all categories")
        print("  - Type 'none' to deselect all categories")
        print("  - Press Enter or type 'done' to continue")
        print("=" * 70)

        user_input = input("\nYour choice: ").strip().lower()

        if user_input in ['', 'done']:
            break
        elif user_input == 'all':
            selected = {cat: True for cat in available_categories.keys()}
        elif user_input == 'none':
            selected = {cat: False for cat in available_categories.keys()}
        else:
            # Parse number input
            try:
                numbers = []
                for part in user_input.split(','):
                    part = part.strip()
                    if '-' in part:
                        # Range like 1-3
                        start, end = map(int, part.split('-'))
                        numbers.extend(range(start, end + 1))
                    else:
                        numbers.append(int(part))

                # Toggle selected categories
                for num in numbers:
                    if 1 <= num <= len(category_list):
                        category = category_list[num - 1]
                        selected[category] = not selected[category]
                    else:
                        print(f"Warning: Number {num} is out of range")
            except ValueError:
                print("Invalid input. Please enter numbers, ranges (1-3), or commands (all/none/done)")

    # Return list of selected categories
    selected_categories = [cat for cat, is_selected in selected.items() if is_selected]

    if not selected_categories:
        print("\nWarning: No categories selected. Exiting.")
        return None

    print(f"\nSelected {len(selected_categories)} categories:")
    for cat in selected_categories:
        print(f"  - {cat}")
    print()

    return selected_categories


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Parse Kurmi workspace export and organize files into categories (Interactive Mode)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fully automatic mode (RECOMMENDED)
  python kurmi_workspace_parser.py

  # Specify workspace file
  python kurmi_workspace_parser.py -i workspace.zip

The parser will show interactive menus for:
  1. Workspace file selection (if -i not specified)
  2. Category selection

Output directory:
  - Fixed location: kurmi_workspace_extraction/

Available categories:
  - service_definitions   : Kurmi service definitions (*.service.xml, *.serviceorder.json)
  - service_inference     : Kurmi service inference files (*.inference.js)
  - quickfeatures         : QuickFeature files (*.quickfeature.*)
  - js_libraries          : JavaScript libraries and utilities
  - widgets               : Widget files (*.widget.js)
  - scenarios             : Scenario files, schemas, rules, and related libraries
  - connectors            : Connector files (*.connector.xml, *.connector.properties)
  - directory_connectors  : Directory connector files (*.directoryModel.xml)
  - emails                : Email template files (*.mail.js)
        """
    )

    parser.add_argument(
        '-i', '--input',
        required=False,
        help='Path to Kurmi workspace export zip file (optional - will auto-detect if not specified)'
    )

    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )

    args = parser.parse_args()

    # Set logging level
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Determine workspace file
    workspace_file = args.input

    if not workspace_file:
        # Scan for workspace files in current directory
        logger.info("Scanning for workspace files...")
        workspace_files = scan_for_workspace_files()

        # Show workspace selection menu
        workspace_file = interactive_workspace_selection(workspace_files)
        if workspace_file is None:
            logger.info("No workspace file selected. Exiting.")
            return 1

    # Verify workspace file exists
    if not os.path.exists(workspace_file):
        logger.error(f"Workspace file not found: {workspace_file}")
        return 1

    # Set fixed output directory
    output_dir = "kurmi_workspace_extraction"
    logger.info(f"Output directory: {output_dir}")

    # Show category selection menu
    selected_categories = interactive_category_selection(KurmiWorkspaceParser.CATEGORIES)
    if selected_categories is None:
        return 1  # User selected nothing, exit

    # Run parser
    try:
        workspace_parser = KurmiWorkspaceParser(
            workspace_zip=workspace_file,
            output_dir=output_dir,
            categories=selected_categories
        )
        workspace_parser.parse_workspace()

        logger.info(f"\nOutput files available at: {output_dir}")
        return 0

    except Exception as e:
        logger.error(f"Parser failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
