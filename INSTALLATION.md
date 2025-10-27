# Kurmi Workspace Parser - Installation Guide

## 📦 Package Contents

This package contains:
- `kurmi_workspace_parser.py` - Main workspace parser script
- `kurmi_vendor_filter.py` - Vendor filtering script
- `README.md` - Complete documentation
- `VENDOR_FILTER_README.md` - Vendor filter documentation
- `VENDOR_PRESETS.md` - Preset groups documentation
- `demo_vendor_filter.sh` - Demo script showing features

## 🚀 Quick Installation

### Requirements
- Python 3.6 or higher
- No external dependencies required (uses Python standard library only)

### Installation Steps

1. **Upload to target machine**
   ```bash
   # Upload all files to your target directory
   # Example: /opt/kurmi_parser/
   ```

2. **Make scripts executable**
   ```bash
   chmod +x kurmi_workspace_parser.py
   chmod +x kurmi_vendor_filter.py
   chmod +x demo_vendor_filter.sh
   ```

3. **Verify Python version**
   ```bash
   python3 --version
   # Should be 3.6 or higher
   ```

## 🎯 Usage

### Step 1: Extract Workspace
```bash
# Place your *.configfile.zip file in the same directory
python3 kurmi_workspace_parser.py
```

The parser will:
- Auto-detect workspace files
- Show interactive menu to select workspace
- Show interactive menu to select categories
- Extract to `kurmi_workspace_extraction/` directory

### Step 2: Filter Vendors (Optional)
```bash
python3 kurmi_vendor_filter.py
```

The filter will:
- Scan extracted categories for vendors
- Show vendor distribution
- Allow selection of vendors to keep
- Remove non-selected vendors

### Preset Commands
- Type `cisco` to select Cisco on-premises vendors (9 vendors)
- Type `microsoft` to select Microsoft cloud vendors (4 vendors)
- Type `webex` to select Webex vendors (3 vendors)
- Presets are additive - combine multiple presets

## 📚 Documentation

- **README.md** - Complete workspace parser documentation
- **VENDOR_FILTER_README.md** - Detailed vendor filter guide
- **VENDOR_PRESETS.md** - Preset groups and workflows

## 🆘 Help

For help with any script:
```bash
python3 kurmi_workspace_parser.py --help
python3 kurmi_vendor_filter.py --help
./demo_vendor_filter.sh  # See vendor filter examples
```

## 📂 Directory Structure

After running the scripts:
```
your_directory/
├── kurmi_workspace_parser.py
├── kurmi_vendor_filter.py
├── README.md
├── VENDOR_FILTER_README.md
├── VENDOR_PRESETS.md
├── demo_vendor_filter.sh
├── your_workspace.configfile.zip  (your workspace file)
├── kurmi_workspace_extraction/    (created by parser)
│   ├── service_definitions/
│   ├── service_inference/
│   ├── quickfeatures/
│   └── ...
├── parser.log                     (created by parser)
└── vendor_filter.log              (created by filter)
```

## ✅ Verification

Test the installation:
```bash
# Show parser help
python3 kurmi_workspace_parser.py --help

# Show vendor filter help
python3 kurmi_vendor_filter.py --help
```

Both should display help messages without errors.

---

**Ready to parse! 🚀**
