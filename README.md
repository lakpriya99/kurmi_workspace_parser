# Kurmi Workspace Parser

## Ultimate Simplicity - Fully Automatic Mode

The Kurmi Workspace Parser automatically organizes Kurmi workspace export files into categorized folders with interactive menus for easy selection.

---

## 🚀 Quick Start

**Just run it - that's all you need!**

```bash
# Step 1: Extract workspace
python3 kurmi_workspace_parser.py

# Step 2: Filter vendors (optional)
python3 kurmi_vendor_filter.py
```

The parser will:
1. 📁 Auto-detect all workspace files in the current directory
2. 📋 Show an interactive menu to select which workspace to parse
3. ✅ Show an interactive menu to select which categories to extract
4. 📂 Extract files to kurmi_workspace_extraction/ directory

The vendor filter will (optional):
1. 🔍 Scan all extracted categories for vendor directories (excluding scenarios/)
2. 📋 Show which vendors exist in each category
3. ✅ Allow interactive selection of vendors to keep (none selected by default)
4. 🗑️ Remove all non-selected vendor directories (scenarios/ preserved)

---

## 📝 Usage Examples

### 1. Fully Automatic (RECOMMENDED)
```bash
python3 kurmi_workspace_parser.py
```
- Auto-detects workspace files
- Interactive selection menus
- Extracts to kurmi_workspace_extraction/ folder

### 2. Specify workspace file
```bash
python3 kurmi_workspace_parser.py -i workspace.zip
```

---

## 🎯 Features

### Auto-Detection
- ✅ Scans current directory for `*.configfile.zip` files
- ✅ Also checks `workspaceExport/` subdirectory
- ✅ Sorts files by modification date (newest first)

### Output Directory
- ✅ Fixed output directory: `kurmi_workspace_extraction/`
- ✅ All workspace files extract to the same location
- ✅ Consistent and predictable output location

### Interactive Menus

**STEP 1: Workspace Selection**
```
======================================================================
SELECT WORKSPACE FILE TO PARSE
======================================================================

  1. ntt.configfile.zip
     Size: 2.01 MB | Modified: 2025-10-27 06:17

  2. Kurmi_export_config_202510270037.configfile.zip
     Size: 2.66 MB | Modified: 2025-10-27 06:07

  ...
```

**STEP 2: Category Selection**
```
======================================================================
SELECT CATEGORIES TO EXTRACT
======================================================================

  1. [x] service_definitions      - Kurmi service definitions
  2. [x] service_inference        - Kurmi service inference files
  3. [x] quickfeatures            - QuickFeature files
  4. [x] js_libraries             - JavaScript libraries
  5. [x] widgets                  - Widget files
  6. [x] scenarios                - Scenario files, schemas, rules
  7. [x] connectors               - Connector files
  8. [x] directory_connectors     - Directory connector files
  9. [x] emails                   - Email template files

Commands:
  - Enter numbers to toggle (e.g., 1,3,5 or 1-3)
  - Type 'all' to select all
  - Type 'none' to deselect all
  - Press Enter to continue
```

---

## 📂 Categories

The parser organizes files into 9 categories:

| Category | Description | File Patterns |
|----------|-------------|---------------|
| **service_definitions** | Service definitions | `*.service.xml`, `*.serviceorder.json` |
| **service_inference** | Service inference files | `*.inference.js` |
| **quickfeatures** | QuickFeature files | `*.quickfeature.xml`, `*.quickfeature.js`, `*.quickfeature.properties` |
| **js_libraries** | JavaScript libraries | `*.util.js`, `*.apiutil.js`, `*.postProcessing.js` |
| **widgets** | Widget files | `*.widget.js` |
| **scenarios** | Scenario files & schemas | `*.scenario.json`, `*.schema.json`, `*.rules.json`, `*.data.json`, `*.options.json`, `*.choice.json`, `*.kurmiApi.js`, `*.configuration.js`, `*.import.js`, `*.export.js`, `*.externalTask.js`, `*.processing.js`, `*.discovery.js`, `*.ruleSet.json`, `*.componentAdjustment.js`, `*.mergeAdjust.js` |
| **connectors** | Connector files | `*.advancedConnector.xml`, `*.connector.xml`, `*.connector.properties` |
| **directory_connectors** | Directory connectors | `*.directoryModel.xml` |
| **emails** | Email templates | `*.mail.js` |

---

## 📊 Output Structure

After parsing, your output directory will look like:

```
kurmi_workspace_extraction/
├── service_definitions/
│   ├── Avaya/
│   ├── Cisco/
│   ├── Microsoft/
│   └── ...
├── service_inference/
├── quickfeatures/
├── js_libraries/
├── widgets/
├── scenarios/
├── connectors/
├── directory_connectors/
└── emails/
```

Files are organized preserving their original folder structure within each category.

---

## 🎨 Interactive Commands

### Workspace Selection Menu
- Enter a number (1-9) to select a workspace
- Type `q` to quit

### Category Selection Menu
- Enter numbers to toggle: `1,3,5` or `1-3` (ranges)
- Type `all` to select all categories
- Type `none` to deselect all categories
- Press Enter or type `done` to continue

---

## 🛠️ Command Line Options

```
-i, --input     Path to workspace file (optional - auto-detects if not specified)
-v, --verbose   Enable verbose logging
-h, --help      Show help message
```

Output is always saved to: `kurmi_workspace_extraction/`

---

## 📋 Requirements

- Python 3.6+
- No external dependencies required (uses standard library only)

---

## 📝 Logging

The parser creates a log file: `parser.log` in the current directory with detailed execution information.

---

## ✨ Benefits

- ✅ **Zero configuration** - just run it!
- ✅ **No file paths to remember** - auto-detection finds everything
- ✅ **Visual feedback** - see exactly what will be extracted
- ✅ **Organized output** - files sorted into logical categories
- ✅ **Preserves structure** - original folder hierarchy maintained
- ✅ **Flexible** - can still specify files manually if needed

---

## 🎯 Example Session

```bash
$ python3 kurmi_workspace_parser.py

2025-10-27 06:00:00,000 - INFO - Scanning for workspace files...


======================================================================
SELECT WORKSPACE FILE TO PARSE
======================================================================

  1. ntt.configfile.zip
     Size: 2.01 MB | Modified: 2025-10-27 06:17
  ...

Your choice: 1

Selected: ntt.configfile.zip

2025-10-27 06:00:05,000 - INFO - Output directory: kurmi_workspace_extraction


======================================================================
SELECT CATEGORIES TO EXTRACT
======================================================================
  ...

Your choice: (press Enter to select all)

Selected 9 categories:
  - service_definitions
  - service_inference
  ...

2025-10-27 06:00:10,000 - INFO - Extracting workspace zip file...
2025-10-27 06:00:12,000 - INFO - Starting file categorization...
2025-10-27 06:00:15,000 - INFO - ============================================================
2025-10-27 06:00:15,000 - INFO - PARSING COMPLETE - STATISTICS
2025-10-27 06:00:15,000 - INFO - ============================================================
2025-10-27 06:00:15,000 - INFO - service_definitions      :   27 files
2025-10-27 06:00:15,000 - INFO - service_inference        :   14 files
2025-10-27 06:00:15,000 - INFO - scenarios                : 1580 files
...
2025-10-27 06:00:15,000 - INFO - TOTAL                    : 1791 files
2025-10-27 06:00:15,000 - INFO - ============================================================

Output files available at: kurmi_workspace_extraction
```

---

## 🔧 Vendor Filtering (Optional)

After extracting the workspace, you can optionally filter vendors to remove unwanted vendor directories:

```bash
python3 kurmi_vendor_filter.py
```

### What It Does:
- Scans category folders (service_definitions, quickfeatures, etc.)
- Excludes scenarios/ directory from vendor filtering
- Shows which vendors exist in each category
- Allows interactive selection of vendors to keep
- Removes all non-selected vendor directories

### Preset Groups:
- **Cisco**: Type `cisco` to select Cisco on-premises infrastructure vendors
  - Includes: Allocations, Cisco, Directory, ForgottenPassword, Technical, User, WrongAttempt, common, licensing
- **Microsoft**: Type `microsoft` to select Microsoft cloud and collaboration vendors
  - Includes: Microsoft, m365, office365, office365graph
- **Webex**: Type `webex` to select Cisco Webex collaboration and contact center vendors
  - Includes: webex, webexContactCenter, webexcontactcenter

**Note:** Presets are additive - you can combine multiple presets (e.g., `cisco` + `webex`)

### Example Use Cases:
- **Cisco on-premises deployment**: Use `cisco` preset for Cisco on-premises infrastructure
- **Microsoft 365/Teams deployment**: Use `microsoft` preset for Microsoft cloud services
- **Webex Calling/Contact Center deployment**: Use `webex` preset for Webex services
- **Hybrid deployment**: Combine presets (e.g., `cisco` + `webex` + `microsoft`) or add vendors manually
- **Custom selection**: Mix presets with manual toggle for specific needs

### Safety Features:
- ✅ Shows vendor distribution before filtering
- ✅ Confirms which vendors will be removed
- ✅ Allows cancellation at any time
- ⚠️ **Warning**: Deletion cannot be undone

For detailed information, see [VENDOR_FILTER_README.md](VENDOR_FILTER_README.md)

---

## 📄 License

Kurmi Workspace Parser - Internal Tool

---

**Happy Parsing! 🚀**
