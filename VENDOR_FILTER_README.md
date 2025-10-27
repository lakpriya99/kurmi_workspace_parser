# Kurmi Vendor Filter

## Purpose

After extracting workspace files with `kurmi_workspace_parser.py`, use this script to filter and remove unwanted vendor directories from the `kurmi_workspace_extraction/` folder.

---

## 🚀 Quick Start

**Step 1: Extract workspace first**
```bash
python3 kurmi_workspace_parser.py
```

**Step 2: Filter vendors**
```bash
python3 kurmi_vendor_filter.py
```

---

## 📝 What It Does

1. **Scans** category folders (service_definitions, quickfeatures, etc.)
2. **Identifies** all vendor subdirectories in each category
3. **Displays** vendor distribution across categories
4. **Allows interactive selection** of vendors to keep
5. **Removes** all non-selected vendor directories

**Note:** The `scenarios/` directory is excluded from vendor scanning and filtering to preserve all scenario files.

---

## 📊 Example Output

### Vendor Distribution by Category:

```
================================================================================
VENDOR DISTRIBUTION BY CATEGORY
================================================================================

connectors:
  Vendors (1): audiocodes

directory_connectors:
  Vendors (1): audiocodes

quickfeatures:
  Vendors (6): Cisco, Microsoft, Spark, common, m365, webex

service_definitions:
  Vendors (15): Alcatel, Avaya, BroadWorks, Cisco, Directory, Genesys, ...

service_inference:
  Vendors (4): BroadWorks, Genesys, redsky, webex

================================================================================
ALL UNIQUE VENDORS (15):
================================================================================
  Alcatel                        (in 1 category)
  Avaya                          (in 1 category)
  BroadWorks                     (in 3 categories)
  Cisco                          (in 3 categories)
  Directory                      (in 1 category)
  Genesys                        (in 2 categories)
  Microsoft                      (in 2 categories)
  Spark                          (in 2 categories)
  common                         (in 1 category)
  imagicle                       (in 1 category)
  m365                           (in 1 category)
  redsky                         (in 2 categories)
  webex                          (in 3 categories)
  webexcontactcenter             (in 2 categories)
  zoom                           (in 1 category)
```

### Interactive Selection Menu:

```
================================================================================
SELECT VENDORS TO KEEP (others will be removed)
================================================================================

   1. [ ] Alcatel                        (in 1 category)
   2. [ ] Avaya                          (in 1 category)
   3. [ ] BroadWorks                     (in 3 categories)
   4. [ ] Cisco                          (in 3 categories)
   5. [ ] Directory                      (in 1 category)
   6. [ ] Genesys                        (in 2 categories)
   7. [ ] Microsoft                      (in 2 categories)
   8. [ ] Spark                          (in 2 categories)
   9. [ ] common                         (in 1 category)
  10. [ ] imagicle                       (in 1 category)
  11. [ ] m365                           (in 1 category)
  12. [ ] redsky                         (in 2 categories)
  13. [ ] webex                          (in 3 categories)
  14. [ ] webexcontactcenter             (in 2 categories)
  15. [ ] zoom                           (in 1 category)

================================================================================
Commands:
  - Enter numbers to toggle (e.g., 1,3,5 or 1-3)
  - Type 'all' to select all vendors
  - Type 'none' to deselect all vendors

Presets:
  - Type 'cisco' for Cisco (Cisco on-premises infrastructure vendors)
  - Type 'microsoft' for Microsoft (Microsoft cloud and collaboration vendors)
  - Type 'webex' for Webex (Cisco Webex collaboration and contact center vendors)

  - Press Enter or type 'done' to continue
  - Type 'q' to quit without changes
================================================================================

Your choice: _
```

---

## 🎨 Interactive Commands

### Selection Commands:
- **Toggle vendors**: Enter numbers like `6,10,12` or ranges like `6-15`
- **Select all**: Type `all`
- **Deselect all**: Type `none`
- **Continue**: Press `Enter` or type `done`
- **Quit**: Type `q` (no changes will be made)

### Preset Groups:
- **Cisco**: Type `cisco` to select Cisco on-premises infrastructure vendors
  - Includes: Allocations, Cisco, Directory, ForgottenPassword, Technical, User, WrongAttempt, common, licensing
  - Use this for Cisco on-premises deployments where you want to keep core infrastructure and common components

- **Microsoft**: Type `microsoft` to select Microsoft cloud and collaboration vendors
  - Includes: Microsoft, m365, office365, office365graph
  - Use this for Microsoft 365/Teams deployments where you want to keep Microsoft-related services

- **Webex**: Type `webex` to select Cisco Webex collaboration and contact center vendors
  - Includes: webex, webexContactCenter, webexcontactcenter
  - Use this for Webex Calling, Meetings, and Contact Center deployments

**Note:** Presets are additive - you can apply multiple presets to combine vendor selections.

### Examples:

**Use Cisco preset (recommended for Cisco on-premises deployments):**
```
Your choice: cisco
Your choice: done
```
This selects: Allocations, Cisco, Directory, ForgottenPassword, Technical, User, WrongAttempt, common, licensing

**Use Microsoft preset (recommended for Microsoft 365/Teams deployments):**
```
Your choice: microsoft
Your choice: done
```
This selects: Microsoft, m365, office365, office365graph

**Use Webex preset (recommended for Webex Calling/Contact Center deployments):**
```
Your choice: webex
Your choice: done
```
This selects: webex, webexContactCenter, webexcontactcenter

**Keep only Cisco and Microsoft:**
```
Your choice: 4,7
Your choice: done
```

**Keep all BroadWorks-related vendors:**
```
Your choice: 3,6,12,13,14
Your choice: done
```

**Keep first 5 vendors:**
```
Your choice: 1-5
Your choice: done
```

**Combine multiple presets (hybrid deployment):**
```
Your choice: cisco
Your choice: microsoft
Your choice: done
```
This selects all vendors from both presets (13 total vendors)

**Use preset then add specific vendors:**
```
Your choice: microsoft
Your choice: 4        # Add Cisco
Your choice: done
```

**Select all vendors first, then deselect some:**
```
Your choice: all
Your choice: 6,10,15
Your choice: done
```

---

## 🛠️ Command Line Options

```
-d, --directory    Path to extraction directory (default: kurmi_workspace_extraction)
-v, --verbose      Enable verbose logging
-h, --help         Show help message
```

### Usage Examples:

**Standard usage:**
```bash
python3 kurmi_vendor_filter.py
```

**Custom extraction directory:**
```bash
python3 kurmi_vendor_filter.py -d /path/to/extraction
```

**Verbose logging:**
```bash
python3 kurmi_vendor_filter.py -v
```

---

## ⚠️ Important Notes

### Before Running:
1. ✅ **Run `kurmi_workspace_parser.py` first** to extract the workspace
2. ✅ Ensure `kurmi_workspace_extraction/` directory exists
3. ✅ **Make a backup** if you want to preserve the original extraction

### Safety Features:
- ⚠️ Confirms before removing vendors
- ⚠️ Shows which vendors will be removed
- ⚠️ Allows cancellation at any time (type `q`)
- ⚠️ Logs all operations to `vendor_filter.log`

### Caution:
- ❌ **This operation CANNOT be undone**
- ❌ Removed vendor directories are permanently deleted
- ❌ Re-run the parser to restore removed vendors

---

## 📋 Requirements

- Python 3.6+
- No external dependencies (uses standard library only)
- Must have extracted workspace in `kurmi_workspace_extraction/` directory

---

## 📝 Logging

The script creates a log file: `vendor_filter.log` in the current directory with detailed execution information.

---

## 🎯 Complete Workflow

**Full workflow for parsing and filtering:**

```bash
# Step 1: Parse workspace and extract all files
python3 kurmi_workspace_parser.py

# Step 2: Filter vendors (keep only what you need)
python3 kurmi_vendor_filter.py

# Result: Clean extraction with only selected vendors
```

---

## 📊 Statistics

After completion, you'll see statistics like:

```
============================================================
VENDOR REMOVAL COMPLETE - STATISTICS
============================================================
connectors               :   0 vendors removed
directory_connectors     :   0 vendors removed
quickfeatures            :   2 vendors removed
scenarios                :  10 vendors removed
service_definitions      :  10 vendors removed
service_inference        :   2 vendors removed
============================================================
TOTAL                    :  24 vendors removed
KEPT                     :   5 vendors
============================================================
```

---

## ✨ Benefits

- ✅ **Clean extraction** - Remove unnecessary vendor files
- ✅ **Reduce size** - Keep only the vendors you need
- ✅ **Better organization** - Clearer workspace structure
- ✅ **Interactive selection** - Visual feedback during selection
- ✅ **Safe operations** - Confirmation before deletion

---

**Happy Filtering! 🚀**
