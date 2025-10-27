#!/usr/bin/env python3
"""
Kurmi Vendor Filter
Scans kurmi_workspace_extraction folder and allows selective removal of vendor files/directories.
"""

import os
import sys
import shutil
import logging
from pathlib import Path
from typing import Dict, Set, List
from collections import defaultdict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/opt/workspace_parser/vendor_filter.log')
    ]
)
logger = logging.getLogger(__name__)


class VendorFilter:
    """Filter vendor files and directories from extracted workspace."""

    # Preset vendor groups
    VENDOR_PRESETS = {
        'cisco': {
            'name': 'Cisco',
            'description': 'Cisco on-premises infrastructure vendors',
            'vendors': {
                'Allocations', 'Cisco', 'Directory', 'ForgottenPassword',
                'Technical', 'User', 'WrongAttempt', 'common', 'licensing'
            }
        },
        'microsoft': {
            'name': 'Microsoft',
            'description': 'Microsoft cloud and collaboration vendors',
            'vendors': {
                'Microsoft', 'm365', 'office365', 'office365graph'
            }
        },
        'webex': {
            'name': 'Webex',
            'description': 'Cisco Webex collaboration and contact center vendors',
            'vendors': {
                'webex', 'webexContactCenter', 'webexcontactcenter'
            }
        }
    }

    def __init__(self, extraction_dir: str = "kurmi_workspace_extraction"):
        """
        Initialize the vendor filter.

        Args:
            extraction_dir: Path to the extracted workspace directory
        """
        self.extraction_dir = Path(extraction_dir)
        self.vendors_by_category = defaultdict(set)
        self.all_vendors = set()

        # Validate extraction directory exists
        if not self.extraction_dir.exists():
            raise FileNotFoundError(f"Extraction directory not found: {self.extraction_dir}")

        logger.info(f"Initialized vendor filter for: {self.extraction_dir}")

    def scan_vendors(self) -> Dict[str, Set[str]]:
        """
        Scan all categories and identify vendors in each.

        Returns:
            Dictionary mapping category names to sets of vendor names
        """
        logger.info("Scanning for vendors in each category...")

        # Categories to skip during vendor scanning
        SKIP_CATEGORIES = {'scenarios'}

        # Get all category directories
        category_dirs = [d for d in self.extraction_dir.iterdir() if d.is_dir()]

        for category_dir in category_dirs:
            category_name = category_dir.name

            # Skip scenarios directory
            if category_name in SKIP_CATEGORIES:
                logger.info(f"Skipping category: {category_name} (excluded from vendor scanning)")
                continue

            logger.debug(f"Scanning category: {category_name}")

            # Get all subdirectories (vendors) in this category
            vendor_dirs = [d for d in category_dir.iterdir() if d.is_dir()]

            for vendor_dir in vendor_dirs:
                vendor_name = vendor_dir.name
                self.vendors_by_category[category_name].add(vendor_name)
                self.all_vendors.add(vendor_name)

        logger.info(f"Found {len(self.all_vendors)} unique vendors across {len(self.vendors_by_category)} categories")
        return dict(self.vendors_by_category)

    def display_vendor_summary(self):
        """Display summary of vendors found in each category."""
        if not self.vendors_by_category:
            self.scan_vendors()

        print("\n" + "=" * 80)
        print("VENDOR DISTRIBUTION BY CATEGORY")
        print("=" * 80)
        print()

        for category in sorted(self.vendors_by_category.keys()):
            vendors = sorted(self.vendors_by_category[category])
            print(f"{category}:")
            print(f"  Vendors ({len(vendors)}): {', '.join(vendors)}")
            print()

        print("=" * 80)
        print(f"ALL UNIQUE VENDORS ({len(self.all_vendors)}):")
        print("=" * 80)
        for vendor in sorted(self.all_vendors):
            # Count in how many categories this vendor appears
            category_count = sum(1 for vendors in self.vendors_by_category.values() if vendor in vendors)
            print(f"  {vendor:<30} (in {category_count} categories)")
        print()

    def interactive_vendor_selection(self) -> Set[str]:
        """
        Interactive vendor selection menu.

        Returns:
            Set of selected vendor names to KEEP
        """
        if not self.all_vendors:
            self.scan_vendors()

        # Start with no vendors selected (user must explicitly choose which to keep)
        selected = {vendor: False for vendor in sorted(self.all_vendors)}
        vendor_list = sorted(self.all_vendors)

        while True:
            print("\n" * 2)
            print("=" * 80)
            print("SELECT VENDORS TO KEEP (others will be removed)")
            print("=" * 80)
            print()

            # Display vendors with selection state
            for idx, vendor in enumerate(vendor_list, 1):
                checkbox = "[x]" if selected[vendor] else "[ ]"
                # Count categories
                category_count = sum(1 for vendors in self.vendors_by_category.values() if vendor in vendors)
                print(f"  {idx:2d}. {checkbox} {vendor:<30} (in {category_count} categories)")

            print()
            print("=" * 80)
            print("Commands:")
            print("  - Enter numbers to toggle (e.g., 1,3,5 or 1-3)")
            print("  - Type 'all' to select all vendors")
            print("  - Type 'none' to deselect all vendors")
            print()
            print("Presets:")
            for preset_key, preset_info in self.VENDOR_PRESETS.items():
                # Display preset key as-is
                display_key = preset_key
                print(f"  - Type '{display_key}' for {preset_info['name']} ({preset_info['description']})")
            print()
            print("  - Press Enter or type 'done' to continue")
            print("  - Type 'q' to quit without changes")
            print("=" * 80)

            user_input = input("\nYour choice: ").strip().lower()

            if user_input in ['q', 'quit']:
                logger.info("User cancelled vendor selection")
                return None
            elif user_input in ['', 'done']:
                break
            elif user_input == 'all':
                selected = {vendor: True for vendor in vendor_list}
            elif user_input == 'none':
                selected = {vendor: False for vendor in vendor_list}
            elif user_input.replace(' ', '') in self.VENDOR_PRESETS:
                # Apply preset (additive - adds to current selection)
                preset_key = user_input.replace(' ', '')
                preset = self.VENDOR_PRESETS[preset_key]
                preset_vendors = preset['vendors']
                # Add preset vendors to current selection (additive)
                for vendor in vendor_list:
                    if vendor in preset_vendors:
                        selected[vendor] = True
                print(f"\nApplied preset: {preset['name']}")
                matched = sum(1 for v in vendor_list if v in preset_vendors)
                print(f"Added {matched} vendors from preset")
                total_selected = sum(1 for v in selected.values() if v)
                print(f"Total vendors selected: {total_selected}")
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

                    # Toggle selected vendors
                    for num in numbers:
                        if 1 <= num <= len(vendor_list):
                            vendor = vendor_list[num - 1]
                            selected[vendor] = not selected[vendor]
                        else:
                            print(f"Warning: Number {num} is out of range")
                except ValueError:
                    print("Invalid input. Please enter numbers, ranges (1-3), or commands (all/none/done)")

        # Get selected vendors
        selected_vendors = {vendor for vendor, is_selected in selected.items() if is_selected}

        if not selected_vendors:
            print("\nWarning: No vendors selected. All vendor files will be removed!")
            confirm = input("Are you sure? (yes/no): ").strip().lower()
            if confirm != 'yes':
                return None

        print(f"\nSelected {len(selected_vendors)} vendors to KEEP:")
        for vendor in sorted(selected_vendors):
            print(f"  - {vendor}")
        print()

        # Confirm deletion
        vendors_to_remove = self.all_vendors - selected_vendors
        if vendors_to_remove:
            print(f"\nThe following {len(vendors_to_remove)} vendors will be REMOVED:")
            for vendor in sorted(vendors_to_remove):
                print(f"  - {vendor}")
            print()
            confirm = input("Proceed with removal? (yes/no): ").strip().lower()
            if confirm != 'yes':
                logger.info("User cancelled vendor removal")
                return None

        return selected_vendors

    def remove_vendors(self, vendors_to_keep: Set[str]):
        """
        Remove all vendor directories except those in vendors_to_keep.

        Args:
            vendors_to_keep: Set of vendor names to keep
        """
        logger.info(f"Starting vendor removal (keeping {len(vendors_to_keep)} vendors)...")

        # Categories to skip during vendor removal
        SKIP_CATEGORIES = {'scenarios'}

        removal_stats = defaultdict(int)
        total_removed = 0

        # Iterate through each category
        for category_dir in self.extraction_dir.iterdir():
            if not category_dir.is_dir():
                continue

            category_name = category_dir.name

            # Skip scenarios directory
            if category_name in SKIP_CATEGORIES:
                logger.info(f"Skipping removal in category: {category_name} (excluded from vendor filtering)")
                continue

            # Iterate through vendor directories in this category
            for vendor_dir in category_dir.iterdir():
                if not vendor_dir.is_dir():
                    continue

                vendor_name = vendor_dir.name

                # Remove if not in keep list
                if vendor_name not in vendors_to_keep:
                    logger.info(f"Removing: {category_name}/{vendor_name}")
                    try:
                        shutil.rmtree(vendor_dir)
                        removal_stats[category_name] += 1
                        total_removed += 1
                    except Exception as e:
                        logger.error(f"Failed to remove {vendor_dir}: {e}")

        # Display removal statistics
        logger.info("=" * 60)
        logger.info("VENDOR REMOVAL COMPLETE - STATISTICS")
        logger.info("=" * 60)
        for category in sorted(removal_stats.keys()):
            count = removal_stats[category]
            logger.info(f"{category:25s}: {count:3d} vendors removed")
        logger.info("=" * 60)
        logger.info(f"{'TOTAL':25s}: {total_removed:3d} vendors removed")
        logger.info(f"{'KEPT':25s}: {len(vendors_to_keep):3d} vendors")
        logger.info("=" * 60)


def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Filter vendors from kurmi_workspace_extraction directory',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive mode (RECOMMENDED)
  python kurmi_vendor_filter.py

  # Specify custom extraction directory
  python kurmi_vendor_filter.py -d ./my_extraction

The script will:
  1. Scan all categories in the extraction directory
  2. Identify all vendors in each category
  3. Show interactive menu to select vendors to keep
  4. Remove all non-selected vendor directories

CAUTION: This operation cannot be undone!
        """
    )

    parser.add_argument(
        '-d', '--directory',
        default='kurmi_workspace_extraction',
        help='Path to extracted workspace directory (default: kurmi_workspace_extraction)'
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

    try:
        # Initialize vendor filter
        vendor_filter = VendorFilter(extraction_dir=args.directory)

        # Scan vendors
        vendor_filter.scan_vendors()

        # Display summary
        vendor_filter.display_vendor_summary()

        # Interactive selection
        selected_vendors = vendor_filter.interactive_vendor_selection()

        if selected_vendors is None:
            logger.info("Operation cancelled by user")
            return 0

        # Remove non-selected vendors
        vendor_filter.remove_vendors(selected_vendors)

        logger.info("\nVendor filtering complete!")
        return 0

    except FileNotFoundError as e:
        logger.error(f"Error: {e}")
        logger.error("\nPlease ensure you have run kurmi_workspace_parser.py first to extract the workspace.")
        return 1
    except Exception as e:
        logger.error(f"Vendor filter failed: {e}")
        return 1


if __name__ == '__main__':
    sys.exit(main())
