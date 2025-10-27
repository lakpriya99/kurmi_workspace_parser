# Kurmi Vendor Filter - Preset Groups

## What are Presets?

Presets are pre-configured vendor groups that can be selected with a single command, making it easier to filter vendors for common deployment scenarios.

---

## Available Presets

### 📦 Cisco (`cisco`)

**Description:** Cisco on-premises infrastructure vendors

**Command:** Type `cisco` in the vendor selection menu

**Includes:**
- `Allocations` - Resource allocation management
- `Cisco` - Cisco collaboration services
- `Directory` - Directory services and connectors
- `ForgottenPassword` - Password recovery services
- `Technical` - Technical utilities and tools
- `User` - User management and provisioning
- `WrongAttempt` - Login attempt tracking
- `common` - Common libraries and utilities
- `licensing` - License management

**Use Case:** Cisco on-premises deployments where you want to keep core infrastructure, Cisco services, and common components while removing cloud/third-party vendors.

**Example:**
```bash
python3 kurmi_vendor_filter.py

# In the menu:
Your choice: cisco
Your choice: done

# Confirms and removes all other vendors
```

---

### 📦 Microsoft (`microsoft`)

**Description:** Microsoft cloud and collaboration vendors

**Command:** Type `microsoft` in the vendor selection menu

**Includes:**
- `Microsoft` - Microsoft Teams and collaboration services
- `m365` - Microsoft 365 services
- `office365` - Office 365 services
- `office365graph` - Office 365 Graph API services

**Use Case:** Microsoft 365/Teams deployments where you want to keep Microsoft cloud services, Teams, and related components.

**Example:**
```bash
python3 kurmi_vendor_filter.py

# In the menu:
Your choice: microsoft
Your choice: done

# Confirms and removes all other vendors
```

---

### 📦 Webex (`webex`)

**Description:** Cisco Webex collaboration and contact center vendors

**Command:** Type `webex` in the vendor selection menu

**Includes:**
- `webex` - Webex Calling, Meetings, and collaboration services
- `webexContactCenter` - Webex Contact Center services
- `webexcontactcenter` - Webex Contact Center services (alternate case)

**Use Case:** Webex Calling, Meetings, and Contact Center deployments where you want to keep Webex collaboration and contact center components.

**Example:**
```bash
python3 kurmi_vendor_filter.py

# In the menu:
Your choice: webex
Your choice: done

# Confirms and removes all other vendors
```

---

## How to Use Presets

**Important:** Presets are **additive** - you can apply multiple presets and they will combine their vendor selections.

### Basic Usage

1. Run the vendor filter:
   ```bash
   python3 kurmi_vendor_filter.py
   ```

2. Type the preset name:
   ```
   Your choice: cisco
   ```

3. Confirm and continue:
   ```
   Your choice: done
   ```

### Combining Multiple Presets

You can apply multiple presets to combine their vendor selections:

1. Apply first preset:
   ```
   Your choice: cisco
   ```

2. Apply second preset (adds to selection):
   ```
   Your choice: microsoft
   ```

3. Continue:
   ```
   Your choice: done
   ```

This will select all vendors from both presets.

### Combine Presets with Manual Selection

You can use a preset and then manually adjust the selection:

**Example: Cisco + Microsoft**
```
Your choice: cisco         # Applies Cisco preset
Your choice: 7             # Toggle Microsoft (add it)
Your choice: done          # Continue
```

**Example: Cisco but without licensing**
```
Your choice: cisco         # Applies Cisco preset
Your choice: 9             # Toggle licensing (remove it)
Your choice: done          # Continue
```

---

## Preset vs Manual Selection

### Use Presets When:
- ✅ You have a standard deployment type (e.g., on-premises)
- ✅ You want quick, consistent vendor filtering
- ✅ You need to filter multiple workspaces the same way
- ✅ You're not sure which vendors to keep

### Use Manual Selection When:
- ✅ You need very specific vendors
- ✅ Your deployment is non-standard
- ✅ You want fine-grained control
- ✅ You need a combination not covered by presets

---

## Creating Custom Presets

If you need additional presets for your organization, you can modify the script:

Edit `/opt/workspace_parser/kurmi_vendor_filter.py` and add to the `VENDOR_PRESETS` dictionary:

```python
VENDOR_PRESETS = {
    'onprem': {
        'name': 'On-Prem',
        'description': 'On-premises infrastructure vendors',
        'vendors': {
            'Allocations', 'Cisco', 'Directory', 'ForgottenPassword',
            'Technical', 'User', 'WrongAttempt', 'common', 'licensing'
        }
    },
    # Add your custom preset here:
    'cloud': {
        'name': 'Cloud',
        'description': 'Cloud-based vendors',
        'vendors': {
            'Microsoft', 'm365', 'webex', 'zoom', 'Spark'
        }
    }
}
```

Then use it in the menu:
```
Your choice: cloud
```

---

## Preset Comparison

| Preset | Command | Vendors Included | Best For |
|--------|---------|------------------|----------|
| **Cisco** | `cisco` | 9 vendors (Allocations, Cisco, Directory, ForgottenPassword, Technical, User, WrongAttempt, common, licensing) | Cisco on-premises deployments with core infrastructure |
| **Microsoft** | `microsoft` | 4 vendors (Microsoft, m365, office365, office365graph) | Microsoft 365/Teams cloud deployments |
| **Webex** | `webex` | 3 vendors (webex, webexContactCenter, webexcontactcenter) | Webex Calling, Meetings, and Contact Center deployments |

---

## Tips

1. **Start with presets**: Apply a preset first, then fine-tune with manual toggles
2. **Combine multiple presets**: Type multiple preset commands to combine their selections (e.g., `cisco` then `microsoft`)
3. **Presets are additive**: Each preset adds vendors to your selection - they don't replace previous selections
4. **Check the list**: After applying presets, review the selected vendors before confirming
5. **Create custom presets**: If you repeatedly use the same vendor combination, add it as a custom preset

---

## Example Workflows

### Workflow 1: Standard Cisco Deployment
```bash
# Extract workspace
python3 kurmi_workspace_parser.py

# Filter to Cisco vendors only
python3 kurmi_vendor_filter.py
> cisco
> done
> yes
```

### Workflow 2: Cisco + Microsoft Teams
```bash
# Extract workspace
python3 kurmi_workspace_parser.py

# Filter to Cisco + Microsoft
python3 kurmi_vendor_filter.py
> cisco
> 7      # Add Microsoft
> done
> yes
```

### Workflow 3: Microsoft 365/Teams Deployment
```bash
# Extract workspace
python3 kurmi_workspace_parser.py

# Filter to Microsoft vendors only
python3 kurmi_vendor_filter.py
> microsoft
> done
> yes
```

### Workflow 4: Webex Deployment
```bash
# Extract workspace
python3 kurmi_workspace_parser.py

# Filter to Webex vendors only
python3 kurmi_vendor_filter.py
> webex
> done
> yes
```

### Workflow 5: Hybrid Deployment (Cisco + Microsoft using multiple presets)
```bash
# Extract workspace
python3 kurmi_workspace_parser.py

# Filter to Cisco + Microsoft vendors using both presets
python3 kurmi_vendor_filter.py
> cisco
> microsoft
> done
> yes
```
This combines both presets automatically (13 vendors total)

### Workflow 6: Cisco + Webex
```bash
# Extract workspace
python3 kurmi_workspace_parser.py

# Filter to Cisco + Webex vendors
python3 kurmi_vendor_filter.py
> cisco
> webex
> done
> yes
```
This combines both presets (12 vendors total)

---

## Quick Reference

| Action | Command |
|--------|---------|
| Apply Cisco preset | `cisco` |
| Apply Microsoft preset | `microsoft` |
| Apply Webex preset | `webex` |
| Select all vendors | `all` |
| Deselect all vendors | `none` |
| Toggle specific vendors | `1,3,5` or `1-5` |
| Continue | `done` or `Enter` |
| Quit | `q` |

---

**Need help?** Run: `python3 kurmi_vendor_filter.py --help`
