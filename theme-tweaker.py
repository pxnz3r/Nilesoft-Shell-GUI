import streamlit as st
import os
import re
from html import escape
import io
import json
import math
import shutil
import zipfile
from datetime import datetime

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
THEME_PATH = os.path.join(_SCRIPT_DIR, "imports", "theme.nss")
CUSTOM_PATH = os.path.join(_SCRIPT_DIR, "imports", "custom.nss")
MODIFY_PATH = os.path.join(_SCRIPT_DIR, "imports", "modify.nss")
SHELL_PATH = os.path.join(_SCRIPT_DIR, "shell.nss")

PRESETS = {
    "Navy Indigo": {
        "bg_color": "#0a0a1a", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#0a0a1a"], [0.33, "#1a1a3e"], [0.66, "#0f2255"], [1, "#0a0a2e"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Dark Red": {
        "bg_color": "#0a0000", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#0a0000"], [0.33, "#3d0505"], [0.66, "#6a0a0a"], [1, "#2a0000"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Crimson Navy": {
        "bg_color": "#0a0a2e", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#2a0505"], [0.33, "#b3182a"], [0.66, "#3a2a6b"], [1, "#0a0a2e"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Bright Red": {
        "bg_color": "#1a0000", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#1a0000"], [0.33, "#990000"], [0.66, "#ff2222"], [1, "#cc0000"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Light Blue": {
        "bg_color": "#0a1a2a", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#0a1a2a"], [0.33, "#3a7ab5"], [0.66, "#87ceeb"], [1, "#4a90d9"]],
        "text_normal": "#000000", "text_select": "#000000",
        "img_c1": "#333333", "img_c2": "#555555", "img_c3": "#777777",
    },
    "Dark Blue": {
        "bg_color": "#050a14", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#050a14"], [0.33, "#0a1628"], [0.66, "#0d1f3c"], [1, "#1a3a6b"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Forest": {
        "bg_color": "#050a05", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#050a05"], [0.33, "#0a1a0a"], [0.66, "#1a3a1a"], [1, "#0d4a0d"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Twilight": {
        "bg_color": "#0a001a", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#0a001a"], [0.33, "#2a004a"], [0.66, "#4a006a"], [1, "#1a003a"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Amber Glow": {
        "bg_color": "#0a0500", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#0a0500"], [0.33, "#3a1a00"], [0.66, "#6a3a00"], [1, "#2a1500"]],
        "text_normal": "#ffffff", "text_select": "#ffffff",
        "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888",
    },
    "Midnight": {
        "bg_color": "#0d1117", "bg_opacity": 100, "bg_effect": 2,
        "stops": [[0, "#0d1117"], [0.33, "#161b22"], [0.66, "#0d1117"], [1, "#161b22"]],
        "text_normal": "#e6edf3", "text_select": "#e6edf3",
        "img_c1": "#e6edf3", "img_c2": "#8b949e", "img_c3": "#6e7681",
    },
}

DEFAULTS = {
    "theme_name": "modern", "dark": "default", "theme_view": "compact",
    "bg_color": "#0a0a1a", "bg_opacity": 100, "bg_effect": 2,
    "gradient_enabled": True, "grad_type": "linear",
    "lx1v": 0, "lx2v": 100, "ly1v": 0, "ly2v": 0,
    "rcx": 100, "rcy": 100, "rr": 150, "rfx": 100, "rfy": 100,
    "stops": [[0.0, "#0a0a1a"], [0.33, "#1a1a3e"], [0.66, "#0f2255"], [1.0, "#0a0a2e"]],
    "text_normal": "#ffffff", "text_select": "#ffffff",
    "item_bg_normal": "none", "item_bg_select": "#ffffff20", "item_radius": 0,
    "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888", "img_align": 2,
    "border_enabled": False, "border_size": 1, "border_color": "#000000",
    "border_opacity": 50, "border_radius": 4,
    "shadow_enabled": True, "shadow_size": 8, "shadow_color": "#000000",
    "shadow_opacity": 40, "shadow_offset": 2,
    "customize_font": False, "font_size": 9, "font_name": "Segoe UI", "font_weight": 4, "font_italic": False,
}
MAX_STOPS = 6
# Widget limits; values read from theme.nss are clamped so out-of-range numbers can't crash a slider.
RANGES = {
    "bg_opacity": (0, 100), "bg_effect": (0, 3), "item_radius": (0, 3), "img_align": (0, 2),
    "lx1v": (0, 100), "lx2v": (0, 100), "ly1v": (0, 100), "ly2v": (0, 100),
    "rcx": (0, 100), "rcy": (0, 100), "rr": (0, 200), "rfx": (0, 100), "rfy": (0, 100),
    "border_size": (0, 10), "border_opacity": (0, 100), "border_radius": (0, 20),
    "shadow_size": (0, 30), "shadow_opacity": (0, 100), "shadow_offset": (0, 30),
    "font_size": (6, 24), "font_weight": (1, 9),
}


def read_file_safe(path):
    """Read a text file as UTF-8 (BOM stripped), falling back to cp1252. Missing file -> ''."""
    try:
        with open(path, "r", encoding="utf-8-sig") as f:
            return f.read()
    except FileNotFoundError:
        return ""
    except UnicodeDecodeError:
        with open(path, "r", encoding="cp1252") as f:
            return f.read()


def hex6(value):
    """Normalize #rgb / #rrggbb to #rrggbb, or None for anything a color picker can't show."""
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", value.strip())
    if not m: return None
    h = m.group(1)
    return "#" + (h if len(h) == 6 else "".join(c * 2 for c in h)).lower()


def parse_theme(text):
    """Read the values the editor understands from a theme.nss. Anything unrecognized keeps its default."""
    def block(name, src):
        m = re.search(rf"\b{name}\s*\{{", src)
        if not m: return None
        depth, i = 1, m.end()
        while i < len(src) and depth:
            depth += {"{": 1, "}": -1}.get(src[i], 0)
            i += 1
        return src[m.end():i - 1]

    def own(src):
        """Drop nested blocks so only this block's direct properties remain."""
        prev = None
        while prev != src:
            prev, src = src, re.sub(r"\w+\s*\{[^{}]*\}", "", src)
        return src

    def val(key, src):
        if src is None: return None
        m = re.search(rf"(?m)^\s*{re.escape(key)}\s*=\s*(.+?)\s*(?://.*)?$", src)
        return m.group(1).strip("\"'") if m else None

    def num(x):
        return int(x) if x is not None and re.fullmatch(r"\d+", x) else None

    def flag(x):
        return None if x is None else x.lower() in ("true", "1")

    v = {}
    theme = block("theme", text)
    if theme is None: return v
    top = own(theme)
    if val("name", top) in ("modern", "classic", "white", "black"): v["theme_name"] = val("name", top)
    dark = val("dark", top)
    if dark in ("default", "auto", "true", "false"): v["dark"] = "default" if dark == "auto" else dark
    view = (val("view", top) or "").replace("view.", "")
    if view in ("auto", "compact", "small", "medium", "large", "wide"): v["theme_view"] = view

    bg = block("background", theme)
    if bg is not None:
        bg_own = own(bg)
        v.update({k: x for k, x in (("bg_color", hex6(val("color", bg_own) or "")), ("bg_opacity", num(val("opacity", bg_own))),
                                    ("bg_effect", num(val("effect", bg_own)))) if x is not None})
        grad = block("gradient", bg)
        v["gradient_enabled"] = grad is not None and flag(val("enabled", grad)) is not False
        if grad is not None:
            lin = re.search(r"linear\s*=\s*\[([^\]]*)\]", grad)
            rad = re.search(r"radial\s*=\s*\[([^\]]*)\]", grad)
            nums = lambda m: [int(float(n)) for n in re.findall(r"-?[\d.]+", m.group(1))]
            if rad:
                v["grad_type"] = "radial"
                v.update(zip(["rcx", "rcy", "rr", "rfx", "rfy"], nums(rad)))
            elif lin:
                v["grad_type"] = "linear"
                v.update(zip(["lx1v", "lx2v", "ly1v", "ly2v"], nums(lin)))
            stops = [[float(o), hex6(c)] for o, c in re.findall(r"\[\s*([\d.]+)\s*,\s*(#[0-9a-fA-F]{3,6})\b", grad)]
            if len(stops) >= 2: v["stops"] = stops[:MAX_STOPS]

    item = block("item", theme)
    if item is not None:
        if num(val("radius", own(item))) is not None: v["item_radius"] = num(val("radius", own(item)))
        for sub, prefix in (("text", "text_"), ("back", "item_bg_")):
            b = block(sub, item)
            for state in ("normal", "select"):
                x = val(state, b)
                if x is None: continue
                if prefix == "text_":
                    if hex6(x): v[prefix + state] = hex6(x)
                else:
                    v[prefix + state] = x

    image = block("image", theme)
    if image is not None:
        colors = re.findall(r"#[0-9a-fA-F]{3,6}\b", val("color", own(image)) or "")
        for k, c in zip(["img_c1", "img_c2", "img_c3"], colors): v[k] = hex6(c)
        if num(val("align", own(image))) in (0, 1, 2): v["img_align"] = num(val("align", own(image)))

    for name in ("border", "shadow"):
        b = block(name, theme)
        v[f"{name}_enabled"] = b is not None and flag(val("enabled", b)) is not False
        if b is None: continue
        for k in ("size", "opacity", "radius", "offset"):
            if num(val(k, b)) is not None: v[f"{name}_{k}"] = num(val(k, b))
        if hex6(val("color", b) or ""): v[f"{name}_color"] = hex6(val("color", b))

    font = block("font", theme)
    v["customize_font"] = font is not None
    if font is not None:
        if val("name", font): v["font_name"] = val("name", font)
        for k in ("size", "weight"):
            if num(val(k, font)) is not None: v[f"font_{k}"] = num(val(k, font))
        v["font_italic"] = bool(flag(val("italic", font)))
    for k, (lo, hi) in RANGES.items():
        if k in v: v[k] = max(lo, min(hi, v[k]))
    return {k: x for k, x in v.items() if k in DEFAULTS}


def load_theme_state(values):
    """Push theme values into widget state. Only call before the theme widgets render (or from a callback)."""
    for k, x in values.items():
        if k == "stops":
            st.session_state.num_stops = len(x)
            for i, (off, col) in enumerate(x):
                st.session_state[f"so_{i}"] = float(off)
                st.session_state[f"sc_{i}"] = col
        else:
            st.session_state[k] = x


def current_stops():
    s = st.session_state
    n = int(s.get("num_stops", len(DEFAULTS["stops"])))
    if not all(f"so_{i}" in s and f"sc_{i}" in s for i in range(n)):
        return DEFAULTS["stops"]
    return [[round(s[f"so_{i}"], 2), s[f"sc_{i}"]] for i in range(n)]


def apply_preset():
    name = st.session_state.preset_selector
    if name:
        load_theme_state(PRESETS[name])


if "_theme_loaded" not in st.session_state:
    load_theme_state({**DEFAULTS, **parse_theme(read_file_safe(THEME_PATH))})
    st.session_state._theme_loaded = True
if "_pending_state" in st.session_state:
    load_theme_state(st.session_state.pop("_pending_state"))
# Re-assign theme keys so Streamlit keeps them while their widgets are hidden (e.g. font options toggled off).
for _k in list(st.session_state.keys()):
    if _k in DEFAULTS or re.fullmatch(r"(so|sc)_\d+|num_stops", _k):
        st.session_state[_k] = st.session_state[_k]

st.set_page_config(page_title="Nilesoft Shell GUI", page_icon="🎨", layout="wide")
st.markdown("""
<style>
.block-container { padding-top: 1.5rem; }
.stTabs [data-baseweb="tab-list"] { gap: 0; }
.stTabs [data-baseweb="tab"] { padding: 0.5rem 1.2rem; }
.sub-tabs [role="tablist"] { background: #0e1117; border-radius: 8px; padding: 2px; }
.sub-tabs [data-baseweb="tab"] { font-size: 0.85rem; }
</style>
""", unsafe_allow_html=True)

logo_svg = """
<svg width="40" height="40" viewBox="0 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect x="6" y="4" width="28" height="32" rx="6" fill="url(#g)" stroke="#555" stroke-width="1.2"/>
  <rect x="11" y="11" width="18" height="2.5" rx="1.25" fill="#eee"/>
  <rect x="11" y="17" width="18" height="2.5" rx="1.25" fill="#888"/>
  <rect x="11" y="23" width="18" height="2.5" rx="1.25" fill="#888"/>
  <rect x="11" y="29" width="10" height="2.5" rx="1.25" fill="#555"/>
  <defs>
    <linearGradient id="g" x1="6" y1="4" x2="34" y2="36" gradientUnits="userSpaceOnUse">
      <stop stop-color="#1a1a2e"/>
      <stop offset="1" stop-color="#0f3460"/>
    </linearGradient>
  </defs>
</svg>"""
st.markdown(f'<div style="display:flex;align-items:center;gap:12px;margin-bottom:4px"><div style="flex-shrink:0">{logo_svg}</div><h1 style="margin:0">Nilesoft Shell GUI</h1></div>', unsafe_allow_html=True)
st.markdown("Visually customize your Windows context menu — no manual editing.  \n[![GitHub](https://img.shields.io/badge/GitHub-moudey/shell-181717?logo=github)](https://github.com/moudey/shell) — [📖 Official Docs](https://nilesoft.org/docs)")

IMPORTS_DIR = os.path.join(_SCRIPT_DIR, "imports")

def parse_shell_settings(content):
    s = {"priority": "1", "showdelay": "200", "tip_enabled": True, "remove_duplicate": True, "exclude_where": ""}
    m = re.search(r"settings\s*\{([^}]*)\}", content)
    for line in (m.group(1) if m else "").split("\n"):
        kv = re.match(r"\s*([\w.]+)\s*=\s*(.*?)\s*$", line)
        if not kv: continue
        key, value = kv.groups()
        if key == "priority" and value.isdigit(): s["priority"] = value
        elif key == "showdelay" and value.isdigit(): s["showdelay"] = value
        elif key == "tip.enabled": s["tip_enabled"] = value.lower() in ("1", "true")
        elif key == "modify.remove.duplicate": s["remove_duplicate"] = value.lower() in ("1", "true")
        elif key == "exclude.where": s["exclude_where"] = value
    return s


def nss_str(value):
    """Quote a value as an NSS string, picking a quote char the value doesn't contain."""
    return f'"{value}"' if "'" in value else f"'{value}'"


def import_paths(shell_text):
    """Paths from import lines in shell.nss, skipping commented-out lines."""
    return re.findall(r"(?m)^\s*import\s+['\"]([^'\"]+)['\"]", shell_text)

BACKUP_DIR = os.path.join(_SCRIPT_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_file(filepath):
    """Save a timestamped backup before overwriting."""
    if not os.path.exists(filepath): return
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.basename(filepath)
        shutil.copy2(filepath, os.path.join(BACKUP_DIR, f"{fname}.{ts}"))
    except OSError as e:
        st.warning(f"Backup failed for {filepath}: {e}")

def list_backups(filepath):
    """Return sorted list of (timestamp, backup_path) for a given file."""
    fname = os.path.basename(filepath)
    pattern = f"{fname}."
    backups = []
    if not os.path.isdir(BACKUP_DIR): return backups
    for b in os.listdir(BACKUP_DIR):
        ts = b[len(pattern):]
        if b.startswith(pattern) and re.fullmatch(r"\d{8}_\d{6}", ts):
            backups.append((ts, os.path.join(BACKUP_DIR, b)))
    return sorted(backups, reverse=True)

main_tab_items, main_tab_modify, main_tab_settings, main_tab_imports, main_tab_theme, main_tab_icons, main_tab_find, main_tab_export, main_tab_history, main_tab_help = st.tabs(
    ["➕ Menu Items", "🔄 Modify", "⚙️ Settings", "📂 Imports", "🎨 Theme", "🖼️ Icons", "🔍 Find", "📦 Export", "📜 History", "❓ Help"]
)

with main_tab_items:
    st.markdown("## Create custom menu items")
    st.caption("Define new items and submenus. Saved to `imports/custom.nss`.")

    if not os.path.exists(CUSTOM_PATH):
        st.info("`custom.nss` doesn't exist yet. Append your first item to create it (the import is added to shell.nss for you).")

    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            item_title = st.text_input("Item title", "My App", key="ci_title")
            item_cmd = st.text_input("Command", "notepad.exe", key="ci_cmd",
                help="Full path or executable name")
            item_args = st.text_input("Arguments", "", key="ci_args",
                help="Use @sel.path for selected item path")
            item_icon = st.text_input("Icon", "", key="ci_icon",
                help="icon.pin, icon.settings, or path to .exe/.dll")
        with col_b:
            item_where = st.text_input("Where condition", "", key="ci_where",
                help="e.g. sel.count>0, leave blank for always")
            item_type = st.text_input("Type filter", "", key="ci_type",
                help="'file', 'dir', '*', blank = all")
            item_admin = st.toggle("Run as admin", False, key="ci_admin")
            item_sep = st.selectbox("Separator", ["none", "top", "bottom", "both"], key="ci_sep")

    st.markdown("### Preview")
    parts = []
    if item_type: parts.append(f"type={nss_str(item_type.strip(chr(39) + chr(34)))}")
    if item_where: parts.append(f"where={item_where}")
    cmd_str = f"cmd={nss_str(item_cmd)}"
    if item_args: cmd_str += f" args={nss_str(item_args)}"
    parts.append(f"title={nss_str(item_title)}")
    parts.append(cmd_str)
    if item_sep != "none": parts.append(f'sep=sep.{item_sep}')
    if item_admin: parts.append("admin")
    if item_icon: parts.append(f"image={item_icon}")
    indent = "\n    "
    preview_code = f"item({indent}{indent.join(parts)}\n)"
    st.code(preview_code, language="nss")

    if st.button("➕ Append to custom.nss", type="primary", width="stretch"):
        try:
            backup_file(CUSTOM_PATH)
            with open(CUSTOM_PATH, "a", encoding="utf-8") as f:
                f.write("\n" + preview_code + "\n")
            shell_raw = read_file_safe(SHELL_PATH)
            if "imports/custom.nss" not in import_paths(shell_raw):
                backup_file(SHELL_PATH)
                with open(SHELL_PATH, "a", encoding="utf-8") as sf:
                    sf.write("\nimport 'imports/custom.nss'\n")
            st.success("Appended!")
        except OSError as e:
            st.error(f"Failed to write: {e}")

    custom_content = read_file_safe(CUSTOM_PATH)
    if custom_content.strip():
        with st.expander("📄 Current custom.nss", expanded=False):
            st.code(custom_content, language="nss")

    with st.expander("📋 Item Library — pre-built templates"):
        st.caption("Use the copy icon on a snippet, then paste it into custom.nss (📂 Imports tab).")
        templates = [
            ("Open folder in VS Code", "item(title='Open in VS Code' image=\\uE26E cmd='code' args='\"@sel.path\"')"),
            ("Copy file path", "item(title='Copy Path' image=icon.copy_path cmd=command.copy(sel.path))"),
            ("Run as admin (cmd)", "item(title='Command Prompt (Admin)' admin image=\\uE17A cmd='cmd.exe')"),
            ("Open Terminal here", "item(title='Terminal Here' image=icon.run_with_powershell cmd='powershell.exe' args='-noexit -command Set-Location -Path \"@sel.dir\\.\"')"),
            ("Open with Notepad", "item(type='file' title='Open with Notepad' image cmd='@sys.bin\\notepad.exe' args='\"@sel.path\"')"),
            ("Take Ownership", "item(type='file|dir' title='Take Ownership' admin image=[\\uE194,#f00] cmd args='/K takeown /f \"@sel.path\" && icacls \"@sel.path\" /grant *S-1-5-32-544:F /c /l /q')"),
            ("Create new folder", "item(title='New Folder' image=icon.new_folder cmd=io.dir.create(sys.datetime('ymdHMSs')))"),
            ("Copy file name", "item(mode='single' type='file|dir' title=sel.file.name cmd=command.copy(sel.file.name))"),
            ("Open CMD here", "item(title='Command Prompt' image cmd='cmd.exe' args='/K TITLE Command Prompt & PUSHD \"@sel.dir\"')"),
            ("Open PowerShell here", "item(title='Windows PowerShell' image cmd='powershell.exe' args='-noexit -command Set-Location -Path \"@sel.dir\\.\"')"),
        ]
        for label, code in templates:
            st.markdown(f"**{label}**")
            st.code(code, language="nss")

with main_tab_modify:
    st.markdown("## Modify & reorder items")
    st.caption("Move, hide, or reorganize existing context menu items. Appended to `imports/modify.nss`.")

    common_ids = [
        "", "id.copy_as_path", "id.customize_this_folder", "id.send_to", "id.share",
        "id.create_shortcut", "id.set_as_desktop_background", "id.pin_to_start",
        "id.pin_to_taskbar", "id.unpin_from_start", "id.unpin_from_taskbar",
        "id.open_powershell_window_here", "id.restore_previous_versions",
        "id.cast_to_device", "id.empty_recycle_bin", "id.format", "id.eject",
        "id.give_access_to", "id.include_in_library", "id.print",
        "id.map_network_drive", "id.disconnect_network_drive", "id.rotate_left",
        "id.rotate_right", "id.properties",
    ]

    with st.container(border=True):
        col_a, col_b = st.columns(2)
        with col_a:
            mod_action = st.selectbox("Action", ["Move to menu", "Hide (remove)", "Set position"], key="ma")
            mod_target = st.selectbox("Target item (ID)", common_ids, key="mt")
            mod_target_custom = st.text_input("Or custom ID/pattern", "", key="mtc",
                help="e.g. this.id==id.something or find='pattern'")
        with col_b:
            mod_where_type = st.text_input("Type filter", "", key="mwt",
                help="'file', 'dir', 'dir.back|drive.back', blank = all")
            mod_menu = st.text_input("Target menu", "file manage", key="mm",
                help="Where to move it")
            mod_pos = st.selectbox("Position", ["", "top", "middle", "bottom", "0", "1", "2"], key="mp",
                help="Blank = keep current position")
            mod_sep = st.selectbox("Separator", ["none", "top", "bottom", "both"], key="ms")

    st.markdown("### Preview")
    target_expr = mod_target_custom if mod_target_custom else (f"this.id=={mod_target}" if mod_target else "this.id==id.properties")
    mod_lines = []
    if not mod_target and not mod_target_custom:
        mod_lines.append("// Select a target item or enter a custom pattern above")
    elif mod_action == "Hide (remove)":
        type_part = f'type="{mod_where_type}" ' if mod_where_type else ""
        mod_lines.append(f"modify({type_part}where={target_expr} vis=vis.remove)")
    else:
        parts = [f"where={target_expr}"]
        if mod_where_type: parts.insert(0, f'type="{mod_where_type}"')
        if mod_pos: parts.append(f'pos={mod_pos}' if mod_pos.isdigit() else f'pos="{mod_pos}"')
        if mod_sep != "none": parts.append(f'sep="{mod_sep}"')
        if mod_action == "Move to menu": parts.append(f'menu="{mod_menu}"')
        mod_lines.append("modify(" + " ".join(parts) + ")")

    mod_code = "\n".join(mod_lines)
    st.code(mod_code, language="nss")

    if st.button("➕ Append to modify.nss", type="primary", width="stretch",
                 disabled=not (mod_target or mod_target_custom)):
        try:
            backup_file(MODIFY_PATH)
            with open(MODIFY_PATH, "a", encoding="utf-8") as f:
                f.write("\n" + mod_code + "\n")
            st.success("Appended!")
        except OSError as e:
            st.error(f"Failed to write modify.nss: {e}")

    mod_content = read_file_safe(MODIFY_PATH)
    if mod_content.strip():
        with st.expander("📄 Current modify.nss", expanded=False):
            st.code(mod_content, language="nss")

    with st.expander("📋 Reference — common modify patterns"):
        st.markdown("""
        **Hide by ID:** ``modify(where=this.id==id.restore_previous_versions vis=vis.remove)``
        **Move by name pattern:** ``modify(find="unpin*" pos="bottom" menu="Pin/Unpin")``
        **Move to position with separator:** ``modify(type="dir.back" where=this.id==id.customize_this_folder pos=1 sep="top" menu="file manage")``
        **Move multiple at once:** ``modify(mode=mode.multiple where=this.id(id.send_to, id.share) pos=1 menu=title.more_options)``
        """)

with main_tab_settings:
    st.markdown("## ⚙️ Shell Settings")
    st.caption("Global settings from `shell.nss` — controls how Shell behaves.")

    with st.expander("🔧 Shell Installation Path", expanded=False):
        st.markdown("Set where Nilesoft Shell is installed (where `shell.exe` lives). Used to locate `shell.log`.")
        shell_install = st.text_input(
            "Shell install directory",
            value=st.session_state.get("shell_install_dir", ""),
            placeholder="C:\\Program Files\\Nilesoft Shell",
            help="Directory containing shell.exe / shell.dll",
            key="shell_install_dir_input"
        )
        if shell_install != st.session_state.get("shell_install_dir", ""):
            st.session_state["shell_install_dir"] = shell_install
        if shell_install and os.path.isdir(shell_install):
            has_exe = os.path.isfile(os.path.join(shell_install, "shell.exe"))
            has_dll = os.path.isfile(os.path.join(shell_install, "shell.dll"))
            st.markdown(f"{'✅' if has_exe else '❌'} `shell.exe` — {'found' if has_exe else 'missing'}")
            st.markdown(f"{'✅' if has_dll else '❌'} `shell.dll` — {'found' if has_dll else 'missing'}")
            log_path = os.path.join(shell_install, "shell.log")
            if os.path.isfile(log_path):
                with open(log_path, "r", encoding="utf-8", errors="ignore") as f:
                    log_content = f.read()
                if log_content.strip():
                    st.code(log_content[-2000:], language="text")
                else:
                    st.caption("shell.log is empty")
            else:
                st.caption("No shell.log found yet (appears after Shell runs)")
        elif shell_install:
            st.warning("Directory not found")

    shell_raw = read_file_safe(SHELL_PATH)
    shell_settings = parse_shell_settings(shell_raw)

    col_a, col_b = st.columns(2)
    with col_a:
        with st.container(border=True):
            st.markdown("**General**")
            s_priority = st.number_input("Priority", 0, 10, min(int(shell_settings["priority"]), 10),
                help="Higher = menus load after others (default 1)")
            s_showdelay = st.number_input("Show delay (ms)", 0, 2000, min(int(shell_settings["showdelay"]), 2000),
                help="Delay before menu appears (default 200)")
            s_exclude = st.text_input("Exclude condition", shell_settings["exclude_where"],
                help="e.g. !process.is_explorer to only show in Explorer")
    with col_b:
        with st.container(border=True):
            st.markdown("**Options**")
            s_tip = st.toggle("Enable tooltips", shell_settings["tip_enabled"])
            s_remove_dup = st.toggle("Remove duplicate items", shell_settings["remove_duplicate"],
                help="modify.remove.duplicate — cleans up duplicates from other apps")

    st.code(f"""settings
{{
    priority={s_priority}
    {"exclude.where = " + s_exclude if s_exclude else "// exclude.where = !process.is_explorer"}
    showdelay = {s_showdelay}
    modify.remove.duplicate={1 if s_remove_dup else 0}
    tip.enabled={"true" if s_tip else "false"}
}}""", language="nss")

    if st.button("💾 Write settings to shell.nss", type="primary", width="stretch"):
        try:
            backup_file(SHELL_PATH)
            new_settings = "settings\n{\n"
            new_settings += f"\tpriority={s_priority}\n"
            if s_exclude: new_settings += f"\texclude.where = {s_exclude}\n"
            new_settings += f"\tshowdelay = {s_showdelay}\n"
            new_settings += f"\tmodify.remove.duplicate={1 if s_remove_dup else 0}\n"
            new_settings += f"\ttip.enabled={'true' if s_tip else 'false'}\n"
            new_settings += "}"
            m = re.search(r"settings\s*\{[^}]*\}", shell_raw, re.DOTALL)
            if m:
                new_content = shell_raw[:m.start()] + new_settings + shell_raw[m.end():]
            else:
                new_content = new_settings + "\n\n" + shell_raw
            with open(SHELL_PATH, "w", encoding="utf-8") as f:
                f.write(new_content)
            st.toast("✅ Settings written to shell.nss!", icon="✅")
        except OSError as e:
            st.error(f"Failed to write settings: {e}")

with main_tab_imports:
    st.markdown("## 📂 Import Manager")
    st.caption("View and toggle all imported `.nss` files.")

    import_files = import_paths(read_file_safe(SHELL_PATH))
    available = sorted(f for f in os.listdir(IMPORTS_DIR) if f.endswith(".nss")) if os.path.isdir(IMPORTS_DIR) else []

    st.markdown("### Current imports in shell.nss")
    col_a, col_b = st.columns([1, 1])
    with col_a:
        with st.container(border=True):
            st.markdown("**Imported**")
            for f in import_files:
                st.markdown(f"- `{f}`")
    with col_b:
        with st.container(border=True):
            st.markdown("**Available in imports/**")
            for f in available:
                st.markdown(f"- `{f}` {'✅' if f'imports/{f}' in import_files else '❌ Not imported'}")

    with st.container(border=True):
        st.markdown("**Quick actions**")
        for f in available:
            full_ref = f"imports/{f}"
            is_in = full_ref in import_files
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1: st.text(f)
            with col2:
                if st.button("Open", key=f"open_{f}", width="stretch"):
                    st.session_state[f"editor_{f}"] = read_file_safe(os.path.join(IMPORTS_DIR, f))
                    st.session_state.pop(f"area_{f}", None)
            with col3:
                label = "Remove import" if is_in else "Add import"
                if st.button(label, key=f"toggle_{f}", width="stretch"):
                    try:
                        backup_file(SHELL_PATH)
                        shell_text = read_file_safe(SHELL_PATH)
                        if is_in:
                            shell_text = re.sub(rf"(?m)^\s*import\s+['\"]{re.escape(full_ref)}['\"].*\n?", "", shell_text)
                        else:
                            shell_text = shell_text.rstrip("\n") + f"\nimport '{full_ref}'\n"
                        with open(SHELL_PATH, "w", encoding="utf-8") as sf:
                            sf.write(shell_text)
                        st.rerun()
                    except OSError as e:
                        st.error(f"Failed to update imports: {e}")
            if f"editor_{f}" in st.session_state:
                with st.expander(f"📄 {f}", expanded=True):
                    edited = st.text_area(f"Edit {f}", st.session_state[f"editor_{f}"], height=300, key=f"area_{f}")
                    save_col, close_col = st.columns(2)
                    if save_col.button(f"💾 Save {f}", key=f"save_{f}", width="stretch"):
                        try:
                            backup_file(os.path.join(IMPORTS_DIR, f))
                            with open(os.path.join(IMPORTS_DIR, f), "w", encoding="utf-8") as fp:
                                fp.write(edited)
                            st.success(f"Saved {f}!")
                        except OSError as e:
                            st.error(f"Failed to save {f}: {e}")
                    if close_col.button("✖ Close", key=f"close_{f}", width="stretch"):
                        st.session_state.pop(f"editor_{f}")
                        st.session_state.pop(f"area_{f}", None)
                        st.rerun()

    with st.expander("✅ Syntax Checker — validate NSS files"):
        st.caption("Checks for common issues: unmatched braces, parens, and invalid syntax.")
        sc_file = st.selectbox("Select file to check", ["shell.nss"] + sorted([f for f in os.listdir(IMPORTS_DIR) if f.endswith(".nss")]), key="sc_file")
        sc_path = SHELL_PATH if sc_file == "shell.nss" else os.path.join(IMPORTS_DIR, sc_file)
        sc_content = read_file_safe(sc_path)
        if st.button("🔍 Check Syntax", key="sc_check", width="stretch"):
            errors = []
            lines = sc_content.split("\n")
            brace_depth = 0
            paren_depth = 0
            in_sq = in_dq = in_block = False
            for ln, line in enumerate(lines, 1):
                i = 0
                while i < len(line):
                    c = line[i]
                    if in_block:
                        if line.startswith("*/", i):
                            in_block = False
                            i += 1
                    elif c == "'" and not in_dq: in_sq = not in_sq
                    elif c == '"' and not in_sq: in_dq = not in_dq
                    elif not in_sq and not in_dq:
                        if line.startswith("//", i): break
                        if line.startswith("/*", i):
                            in_block = True
                            i += 1
                        elif c == "{": brace_depth += 1
                        elif c == "}": brace_depth -= 1
                        elif c == "(": paren_depth += 1
                        elif c == ")": paren_depth -= 1
                    i += 1
                if brace_depth < 0:
                    errors.append(f"Line {ln}: Extra closing brace '}}' (depth={brace_depth})")
                    brace_depth = 0
                if paren_depth < 0:
                    errors.append(f"Line {ln}: Extra closing paren ')' (depth={paren_depth})")
                    paren_depth = 0
            if brace_depth > 0:
                errors.append(f"Unclosed braces: {brace_depth} '{{' remain open at end of file")
            if paren_depth > 0:
                errors.append(f"Unclosed parens: {paren_depth} '(' remain open at end of file")

            st.markdown(f"**{len(errors)} issue{'s' if len(errors)!=1 else ''}**")
            if errors:
                for e in errors: st.error(e)
            else:
                st.success("✅ No syntax issues found!")

with main_tab_theme:
    st.markdown("## 🎨 Theme editor")
    st.caption("Customize the look of your context menu. Values start from your current `imports/theme.nss`.")

    preset_cols = st.columns([2, 1, 1])
    with preset_cols[0]:
        st.selectbox("Color scheme preset", list(PRESETS.keys()), index=None, placeholder="Pick a preset to apply...",
            key="preset_selector", on_change=apply_preset)
    with preset_cols[1]:
        st.markdown("")
        st.markdown("")
        st.button("📖 Reload theme.nss", width="stretch", help="Discard unsaved edits and read the file again",
            on_click=lambda: load_theme_state({**DEFAULTS, **parse_theme(read_file_safe(THEME_PATH))}))
    with preset_cols[2]:
        st.markdown("")
        st.markdown("")
        st.button("↺ Reset defaults", width="stretch", on_click=lambda: load_theme_state(DEFAULTS))

    sub_bg, sub_item, sub_icon, sub_border, sub_shadow, sub_font = st.tabs(
        ["🎨 Background", "📝 Items", "🖼️ Icons", "🧱 Border", "🌓 Shadow", "🔤 Font"]
    )

    with sub_bg:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**General**")
                theme_name = st.selectbox("Theme name", ["modern", "classic", "white", "black"],
                    key="theme_name")
                dark = st.selectbox("Dark mode", ["default", "true", "false"],
                    help="default follows the Windows app mode", key="dark")
                theme_view = st.selectbox("Menu density", ["auto", "compact", "small", "medium", "large", "wide"],
                    key="theme_view")
                bg_color = st.color_picker("Base color", key="bg_color")
                bg_opacity = st.slider("Opacity", 0, 100, key="bg_opacity")
                bg_effect = st.selectbox("Effect", [0, 1, 2, 3],
                    format_func=lambda x: {0: "0 - Solid", 1: "1 - Transparent", 2: "2 - Blur", 3: "3 - Acrylic"}[x],
                    key="bg_effect")
        with c2:
            with st.container(border=True):
                st.markdown("**Gradient**")
                gradient_enabled = st.toggle("Enable", key="gradient_enabled")
                if gradient_enabled:
                    grad_type = st.selectbox("Type", ["linear", "radial"], key="grad_type")
                    if grad_type == "linear":
                        cols = st.columns(4)
                        with cols[0]: lx1v = st.number_input("X1", 0, 100, key="lx1v")
                        with cols[1]: lx2v = st.number_input("X2", 0, 100, key="lx2v")
                        with cols[2]: ly1v = st.number_input("Y1", 0, 100, key="ly1v")
                        with cols[3]: ly2v = st.number_input("Y2", 0, 100, key="ly2v")
                    else:
                        cols = st.columns(5)
                        with cols[0]: rcx = st.number_input("CX", 0, 100, key="rcx")
                        with cols[1]: rcy = st.number_input("CY", 0, 100, key="rcy")
                        with cols[2]: rr = st.number_input("R", 0, 200, key="rr")
                        with cols[3]: rfx = st.number_input("FX", 0, 100, key="rfx")
                        with cols[4]: rfy = st.number_input("FY", 0, 100, key="rfy")
                    num_stops = st.number_input("Stops", min_value=2, max_value=MAX_STOPS, key="num_stops")
                    for i in range(int(num_stops)):
                        st.session_state.setdefault(f"so_{i}", round(i / (num_stops - 1), 2))
                        st.session_state.setdefault(f"sc_{i}", "#000000")
                        sc1, sc2 = st.columns([1, 2])
                        with sc1:
                            st.slider(f"S{i+1}", 0.0, 1.0, step=0.01, key=f"so_{i}", label_visibility="collapsed")
                        with sc2:
                            st.color_picker(f"C{i+1}", key=f"sc_{i}", label_visibility="collapsed")
                    grad_bar = "linear-gradient(to right" + "".join(f", {c} {int(o*100)}%" for o, c in current_stops()) + ")"
                    st.markdown(f'<div style="height:20px;border-radius:6px;border:1px solid #444;background:{grad_bar};margin-top:8px"></div>', unsafe_allow_html=True)
                stops = current_stops()

    with sub_item:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**Text colors**")
                text_normal = st.color_picker("Normal", key="text_normal")
                text_select = st.color_picker("Hover", key="text_select")
        with c2:
            with st.container(border=True):
                st.markdown("**Item background**")
                item_bg_normal = st.text_input("Normal",
                    help="Hex color or 'none'", key="item_bg_normal")
                item_bg_select = st.text_input("Hover",
                    help="e.g. #ffffff20", key="item_bg_select")
                item_radius = st.slider("Corner radius", 0, 3, key="item_radius")

    with sub_icon:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**Colors**")
                img_c1 = st.color_picker("Color 1 (main)", key="img_c1")
                img_c2 = st.color_picker("Color 2", key="img_c2")
                img_c3 = st.color_picker("Color 3", key="img_c3")
        with c2:
            with st.container(border=True):
                st.markdown("**Display**")
                img_align = st.selectbox("Alignment", [0, 1, 2],
                    format_func=lambda x: {0: "Check mark only", 1: "Image only", 2: "Both"}[x],
                    key="img_align")
                swatches = f'<div style="display:flex;gap:10px;padding:8px;background:#1a1a2e88;border-radius:6px">'
                for c in [img_c1, img_c2, img_c3]:
                    swatches += f'<div style="width:24px;height:24px;background:{c};border-radius:4px;border:1px solid #555"></div>'
                swatches += '<span style="color:#888;font-size:12px;margin-left:8px">← Slots</span></div>'
                st.markdown(swatches, unsafe_allow_html=True)

    with sub_border:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                border_enabled = st.toggle("Enable", key="border_enabled")
                border_size = st.slider("Size", 0, 10, key="border_size")
                border_color = st.color_picker("Color", key="border_color")
        with c2:
            with st.container(border=True):
                border_opacity = st.slider("Opacity", 0, 100, key="border_opacity")
                border_radius = st.slider("Radius", 0, 20, key="border_radius")

    with sub_shadow:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                shadow_enabled = st.toggle("Enable", key="shadow_enabled")
                shadow_size = st.slider("Size", 0, 30, key="shadow_size")
                shadow_color = st.color_picker("Color", key="shadow_color")
        with c2:
            with st.container(border=True):
                shadow_opacity = st.slider("Opacity", 0, 100, key="shadow_opacity")
                shadow_offset = st.slider("Offset", 0, 30, key="shadow_offset")

    with sub_font:
        customize_font = st.checkbox("Customize font (disable to use system default — DPI-aware)", key="customize_font")
        if customize_font:
            c1, c2 = st.columns(2)
            with c1:
                with st.container(border=True):
                    font_name = st.text_input("Font",
                        help="Must be installed on your system", key="font_name")
                    font_size = st.slider("Size", 6, 24, key="font_size")
            with c2:
                with st.container(border=True):
                    font_weight = st.slider("Weight", 1, 9, key="font_weight")
                    font_italic = st.toggle("Italic", key="font_italic")
        else:
            st.caption("Using system default font with DPI scaling. Enable the checkbox above to customize.")

    def generate_theme():
        s = st.session_state
        l = []
        l.append("theme\n{")
        l.append(f'    name="{s.get("theme_name", DEFAULTS["theme_name"])}"')
        l.append(f'    dark={s.get("dark", DEFAULTS["dark"])}')
        tv = s.get("theme_view", DEFAULTS["theme_view"])
        if tv != "compact":
            l.append(f"    view=view.{tv}")
        l.append("    background\n    {")
        l.append(f'        color={s.get("bg_color", DEFAULTS["bg_color"])}')
        l.append(f'        opacity={s.get("bg_opacity", DEFAULTS["bg_opacity"])}')
        l.append(f'        effect={s.get("bg_effect", DEFAULTS["bg_effect"])}')
        if s.get("gradient_enabled", DEFAULTS["gradient_enabled"]):
            l.append("        gradient\n        {\n            enabled=true")
            grad_type = s.get("grad_type", DEFAULTS["grad_type"])
            if grad_type == "linear":
                l.append(f'            linear=[{s.get("lx1v", 0)}, {s.get("lx2v", 100)}, {s.get("ly1v", 0)}, {s.get("ly2v", 0)}]')
            else:
                l.append(f'            radial=[{s.get("rcx", 100)}, {s.get("rcy", 100)}, {s.get("rr", 150)}, {s.get("rfx", 100)}, {s.get("rfy", 100)}]')
            l.append("            stop=[")
            stops_list = current_stops()
            for idx, s_top in enumerate(stops_list):
                comma = "," if idx < len(stops_list) - 1 else ""
                l.append(f"                [{s_top[0]}, {s_top[1]}]{comma}")
            l.append("            ]\n        }")
        l.append("    }")
        l.append("    item\n    {")
        radius = s.get("item_radius", DEFAULTS["item_radius"])
        if radius > 0: l.append(f"        radius={radius}")
        l.append("        text\n        {")
        l.append(f'            normal={s.get("text_normal", DEFAULTS["text_normal"])}')
        l.append(f'            select={s.get("text_select", DEFAULTS["text_select"])}')
        l.append("        }")
        ibg_n = s.get("item_bg_normal", DEFAULTS["item_bg_normal"])
        ibg_s = s.get("item_bg_select", DEFAULTS["item_bg_select"])
        if ibg_n != "none" or ibg_s != "#ffffff20":
            l.append("        back\n        {")
            if ibg_n != "none": l.append(f"            normal={ibg_n}")
            if ibg_s != "#ffffff20": l.append(f"            select={ibg_s}")
            l.append("        }")
        l.append("    }")
        l.append("    image\n    {")
        l.append(f'        color=[{s.get("img_c1", DEFAULTS["img_c1"])}, {s.get("img_c2", DEFAULTS["img_c2"])}, {s.get("img_c3", DEFAULTS["img_c3"])}]')
        l.append(f'        align={s.get("img_align", DEFAULTS["img_align"])}')
        l.append("    }")
        if s.get("border_enabled", DEFAULTS["border_enabled"]):
            l.append("    border\n    {\n        enabled=true")
            l.append(f'        size={s.get("border_size", DEFAULTS["border_size"])}\n        color={s.get("border_color", DEFAULTS["border_color"])}')
            l.append(f'        opacity={s.get("border_opacity", DEFAULTS["border_opacity"])}\n        radius={s.get("border_radius", DEFAULTS["border_radius"])}\n    }}')
        if s.get("shadow_enabled", DEFAULTS["shadow_enabled"]):
            l.append("    shadow\n    {\n        enabled=true")
            l.append(f'        size={s.get("shadow_size", DEFAULTS["shadow_size"])}\n        color={s.get("shadow_color", DEFAULTS["shadow_color"])}')
            l.append(f'        opacity={s.get("shadow_opacity", DEFAULTS["shadow_opacity"])}\n        offset={s.get("shadow_offset", DEFAULTS["shadow_offset"])}\n    }}')
        if s.get("customize_font", DEFAULTS["customize_font"]):
            l.append("    font\n    {")
            l.append(f'        name="{s.get("font_name", DEFAULTS["font_name"])}"')
            l.append(f'        size={s.get("font_size", DEFAULTS["font_size"])}\n        weight={s.get("font_weight", DEFAULTS["font_weight"])}')
            if s.get("font_italic", False): l.append("        italic=1")
            l.append("    }")
        l.append("}")
        return "\n".join(l) + "\n"

    st.divider()
    col_code, col_preview, col_btn = st.columns([2, 2, 1])
    with col_code:
        with st.container(border=True):
            st.markdown("**📄 Generated NSS code**")
            st.code(generate_theme(), language="nss")
    def extract_title_from_item(raw_text):
        """Extract title='...' or title=\"...\" or title=bare_value from item/menu raw args."""
        # Match single-quoted, double-quoted, or bare
        m = re.search(r"title=('([^']*)'|\"([^\"]*)\"|([^\s\)]+))", raw_text)
        if not m:
            return None
        title = m.group(2) or m.group(3) or m.group(4)
        if title and (title.startswith("title.") or title.startswith("icon.")):
            title = title.split(".", 1)[1].replace("_", " ").title()
        return title

    def find_closing_paren(text, start):
        """Find index of closing paren matching opening paren at start."""
        depth = 1
        i = start + 1
        while i < len(text):
            if text[i] == "(": depth += 1
            elif text[i] == ")": depth -= 1
            elif text[i] in ("'", '"'):
                quote = text[i]
                i += 1
                while i < len(text) and text[i] != quote:
                    if text[i] == "\\": i += 1
                    i += 1
            if depth == 0: return i
            i += 1
        return -1

    def quote_aware_paren_depth(s):
        """Count ( depth minus ) depth, ignoring parens inside quotes."""
        depth = 0
        in_sq = in_dq = False
        i = 0
        while i < len(s):
            c = s[i]
            if c == "'" and not in_dq: in_sq = not in_sq
            elif c == '"' and not in_sq: in_dq = not in_dq
            elif not in_sq and not in_dq:
                if c == "(": depth += 1
                elif c == ")": depth -= 1
            i += 1
        return depth

    def parse_menu_tree(text, parent="root"):
        """Build a nested tree of menus and items from NSS text."""
        tree = []
        i = 0
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        lines = text.split("\n")
        while i < len(lines):
            line = lines[i]
            stripped = line.strip()
            if not stripped or stripped.startswith("//") or stripped.startswith("#") or stripped.startswith("$"):
                i += 1; continue
            # Separator
            if re.match(r'^sep(?:arator)?(?:\s|\(|$)', stripped):
                tree.append({"type": "sep"})
                i += 1; continue
            # Menu or Item block — need paren depth matching
            m = re.match(r'(menu|item)\(', stripped)
            if m:
                kind = m.group(1)
                # Collect full block across lines until parens close (quote-aware)
                full_block = line
                paren_depth = quote_aware_paren_depth(stripped)
                if paren_depth > 0:
                    j = i + 1
                    while j < len(lines) and paren_depth > 0:
                        next_line = lines[j]
                        full_block += "\n" + next_line
                        paren_depth += quote_aware_paren_depth(next_line)
                        j += 1
                    i = j
                else:
                    i += 1
                # Find args between outer parens
                idx = full_block.index("(")
                close = find_closing_paren(full_block, idx)
                if close == -1: continue
                args = full_block[idx + 1:close]
                rest = full_block[close + 1:].strip()
                title = extract_title_from_item(args)
                if kind == "item":
                    if title:
                        tree.append({"type": "item", "title": title})
                else:  # menu
                    # Check for brace block
                    children = []
                    if rest.startswith("{"):
                        brace_depth = 1
                        brace_start = close + 2
                        for ci in range(close + 2, len(full_block)):
                            ch = full_block[ci]
                            if ch == "{": brace_depth += 1
                            elif ch == "}": brace_depth -= 1
                            elif ch in ("'", '"'):
                                q = ch
                                ci += 1
                                while ci < len(full_block) and full_block[ci] != q:
                                    if full_block[ci] == "\\": ci += 1
                                    ci += 1
                            if brace_depth == 0:
                                body = full_block[brace_start:ci]
                                children = parse_menu_tree(body)
                                break
                    tree.append({"type": "menu", "title": title or "Menu", "children": children})
                continue
            i += 1
        # Collapse consecutive seps, trim leading/trailing
        filtered = []
        prev_sep = False
        for node in tree:
            if node["type"] == "sep":
                if prev_sep: continue
                prev_sep = True
                filtered.append(node)
            else:
                prev_sep = False
                filtered.append(node)
        while filtered and filtered[0]["type"] == "sep": filtered.pop(0)
        while filtered and filtered[-1]["type"] == "sep": filtered.pop()
        return filtered

    def collect_all_items():
        roots = []
        sources = [SHELL_PATH] + [os.path.join(IMPORTS_DIR, f) for f in sorted(os.listdir(IMPORTS_DIR)) if f.endswith(".nss")]
        for fp in sources:
            if not os.path.exists(fp): continue
            label = os.path.basename(fp).replace(".nss", "")
            content = read_file_safe(fp)
            tree = parse_menu_tree(content)
            if tree:
                roots.append({"source": label, "children": tree})
        return roots

    with col_preview:
        with st.container(border=True):
            st.markdown("**👁️ Live Preview**")

            menu_roots = collect_all_items()

            # Build gradient CSS
            grad_css = ""
            if gradient_enabled:
                ss = st.session_state
                stops_str = ", ".join(f"{c} {int(o*100)}%" for o, c in stops)
                if ss.grad_type == "linear":
                    # NSS linear=[x1, x2, y1, y2]; CSS angles run clockwise from "to top".
                    dx, dy = ss.lx2v - ss.lx1v, ss.ly2v - ss.ly1v
                    angle = math.degrees(math.atan2(dx, -dy)) if (dx or dy) else 90
                    grad_css = f"linear-gradient({angle:.0f}deg, {stops_str})"
                else:
                    grad_css = f"radial-gradient(circle at {ss.rcx}% {ss.rcy}%, {stops_str})"

            # Build shadow
            shadow_css = "none"
            if shadow_enabled:
                r, g, b = int(shadow_color[1:3], 16), int(shadow_color[3:5], 16), int(shadow_color[5:7], 16)
                shadow_css = f"0 {shadow_offset}px {shadow_size}px rgba({r},{g},{b},{shadow_opacity/100})"

            # Build border
            border_css = "none"
            if border_enabled:
                border_css = f"{border_size}px solid {border_color}"

            # Font fallback for preview when customize_font is off
            font_name = st.session_state.get("font_name", DEFAULTS["font_name"])
            font_size = st.session_state.get("font_size", DEFAULTS["font_size"])
            font_weight = st.session_state.get("font_weight", DEFAULTS["font_weight"])
            font_italic = st.session_state.get("font_italic", False)
            font_style = "italic" if font_italic else "normal"
            font_w = font_weight * 100
            item_rad = f"{item_radius}px" if item_radius > 0 else "0"

            def hex_to_rgba(h, a):
                h = h.lstrip("#")
                r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
                return f"rgba({r},{g},{b},{a})"

            icon_colors = [img_c1, img_c2, img_c3]
            icon_idx = [0]

            def render_tree(nodes, depth=0):
                html = ""
                for node in nodes:
                    if node["type"] == "sep":
                        html += f'<div style="height:1px;background:{hex_to_rgba(text_normal, 0.15)};margin:3px {8 + depth * 12}px;"></div>\n'
                    elif node["type"] == "item":
                        ci = icon_idx[0] % 3
                        icon_idx[0] += 1
                        icon_style = f"background:linear-gradient(135deg, {icon_colors[ci]}, {icon_colors[(ci + 1) % 3]})"
                        hover_bg = item_bg_select if icon_idx[0] == 3 else "transparent"
                        hover_rad = item_rad if icon_idx[0] == 3 else "0"
                        html += f'<div style="padding:2px {8 + depth * 12}px 2px {4 + depth * 12}px;display:flex;align-items:center;gap:8px;background:{hover_bg};border-radius:{hover_rad};">\n'
                        html += f'  <span style="width:14px;height:14px;border-radius:2px;{icon_style};display:inline-block;flex-shrink:0;"></span>\n'
                        html += f'  <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{escape(node["title"])}</span>\n'
                        html += '</div>\n'
                    elif node["type"] == "menu":
                        ci = icon_idx[0] % 3
                        icon_idx[0] += 1
                        icon_style = f"background:linear-gradient(135deg, {icon_colors[ci]}, {icon_colors[(ci + 1) % 3]})"
                        html += f'<div style="padding:2px {8 + depth * 12}px 2px {4 + depth * 12}px;display:flex;align-items:center;gap:8px;">\n'
                        html += f'  <span style="width:14px;height:14px;border-radius:2px;{icon_style};display:inline-block;flex-shrink:0;"></span>\n'
                        html += f'  <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">▶ {escape(node["title"])}</span>\n'
                        html += '</div>\n'
                        # Render children at increased depth
                        if node.get("children"):
                            html += render_tree(node["children"], depth + 1)
                return html

            tree_html = ""
            for root in menu_roots:
                tree_html += f'<div style="padding:2px 12px 1px;font-size:10px;color:{hex_to_rgba(text_normal, 0.4)};text-transform:uppercase;letter-spacing:0.5px;">{escape(root["source"])}</div>\n'
                tree_html += render_tree(root["children"])
                tree_html += f'<div style="height:1px;background:{hex_to_rgba(text_normal, 0.08)};margin:2px 8px;"></div>\n'

            preview_html = (
                '<div style="'
                f'width:fit-content;min-width:180px;max-width:360px;padding:4px 0;'
                f'background:{grad_css if gradient_enabled else bg_color};'
                f'background-color:{bg_color};'
                f'opacity:{bg_opacity/100};'
                f'border:{border_css};'
                f'border-radius:{border_radius}px;'
                f'box-shadow:{shadow_css};'
                f"font-family:'{font_name}',sans-serif;"
                f'font-size:{font_size}px;'
                f'font-weight:{font_w};'
                f'font-style:{font_style};'
                f'color:{text_normal};'
                f'line-height:1.4;'
                '">'
                f'{tree_html}'
                '</div>'
            )
            st.markdown(preview_html, unsafe_allow_html=True)
            st.caption(f"Menu tree from {len(menu_roots)} source files. Third item highlighted as hover state.")
    with col_btn:
        with st.container(border=True):
            st.markdown("**💾 File**")
            if st.button("💾 Write to theme.nss", type="primary", width="stretch"):
                try:
                    backup_file(THEME_PATH)
                    with open(THEME_PATH, "w", encoding="utf-8") as f:
                        f.write(generate_theme())
                    st.toast("✅ Written! Reload Shell (Ctrl+Right-click → Update)", icon="✅")
                except OSError as e:
                    st.error(f"Failed to write theme.nss: {e}")
            st.caption(f"`{THEME_PATH}`")

with main_tab_icons:
    st.markdown("## 🖼️ SVG Icon Browser")
    st.caption("Browse all SVG icons from `images.nss`. Colors are substituted with your current theme slots.")

    content = read_file_safe(os.path.join(IMPORTS_DIR, "images.nss"))
    if not content or len(content) < 100:
        st.error(f"images.nss not found or too short at {os.path.join(IMPORTS_DIR, 'images.nss')} (len={len(content)})")
    icons = []
    for m in re.finditer(r"@(\w[\w, ]*)\s*=\s*'", content):
        start = m.end()
        end = content.find("</svg>'", start)
        if end == -1:
            end = content.find("'", start)
            svg = content[start:end] if end != -1 else content[start:]
        else:
            svg = content[start:end + 6]
        names = [n.strip() for n in m.group(1).split(",") if n.strip()]
        icons.append({"names": names, "svg": svg})

    slot1, slot2, slot3 = (st.session_state.get(k, DEFAULTS[k]) for k in ("img_c1", "img_c2", "img_c3"))
    st.caption("Icon colors come from 🎨 Theme → Icons (image.color1/2/3).")
    # Single-line $variables (e.g. $clipPath, $svg_window_template) that icon bodies reference as @name
    svg_vars = dict(re.findall(r"(?m)^\$(\w+)\s*=\s*'([^']*)'", content))

    def render_svg(svg_text, s1, s2, s3):
        """Substitute variables and color slots so the SVG renders in the browser."""
        r = re.sub(r"@(\w+)\b(?!\.)", lambda m: svg_vars.get(m.group(1), m.group(0)), svg_text)
        r = r.replace("@image.color1", s1).replace("@image.color2", s2).replace("@image.color3", s3)
        r = r.replace("@color3", s3).replace("@color_islight_WB", "#ffffff")
        extras = 'width="24" height="24" xmlns="http://www.w3.org/2000/svg"'
        r = re.sub(r'<svg\s+', f'<svg {extras} ', r, count=1)
        return " ".join(r.split())

    search_icon = st.text_input("🔍 Filter icons by name", "", key="icon_search")

    displayed = [ic for ic in icons if not search_icon or any(search_icon.lower() in n.lower() for n in ic["names"])]
    st.markdown(f"**{len(displayed)} icons** (of {len(icons)} total)")

    cols = st.columns(4)
    for idx, ic in enumerate(displayed):
        with cols[idx % 4]:
            svg_html = render_svg(ic["svg"], slot1, slot2, slot3)
            icon_name = ic["names"][0]
            preview_div = f'<div style="width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:#2a2a3e;border-radius:6px;border:1px solid #444;">{svg_html}</div>'
            st.markdown(f'<div style="display:flex;justify-content:center;padding:8px 0 4px">{preview_div}</div>', unsafe_allow_html=True)
            st.code(icon_name, language=None)

with main_tab_find:
    st.markdown("## 🔍 Find & Replace")
    st.caption("Search across all `.nss` files in the project.")

    find_cols = st.columns([3, 1, 1])
    with find_cols[0]:
        find_term = st.text_input("Search for", "", key="find_term", placeholder="e.g. cmd, title, sel.path")
    with find_cols[1]:
        replace_term = st.text_input("Replace with", "", key="replace_term", placeholder="(leave empty to just find)")
    with find_cols[2]:
        st.markdown("")
        st.markdown("")
        case_sensitive = st.toggle("Aa", value=False, key="find_case", help="Case sensitive")

    if find_term:
        results = []
        sources = [SHELL_PATH] + [os.path.join(IMPORTS_DIR, f) for f in sorted(os.listdir(IMPORTS_DIR)) if f.endswith(".nss")]
        for fp in sources:
            if not os.path.exists(fp): continue
            label = os.path.basename(fp)
            content = read_file_safe(fp)
            lines = content.split("\n")
            flags = 0 if case_sensitive else re.IGNORECASE
            for ln, line in enumerate(lines, 1):
                if re.search(re.escape(find_term), line, flags):
                    results.append({"file": label, "path": fp, "line": ln, "text": line.strip()})

        st.markdown(f"**{len(results)} match{'es' if len(results)!=1 else ''}** across {len(sources)} files")

        with st.container(border=True):
            prev_file = None
            for r in results:
                if r["file"] != prev_file:
                    st.markdown(f"**📄 {r['file']}**")
                    prev_file = r["file"]
                col_a, col_b = st.columns([0.1, 0.9])
                with col_a: st.text(r["line"])
                with col_b:
                    display = r["text"][:150]
                    m = re.search(re.escape(find_term), display, flags)
                    if m:
                        start = max(0, m.start() - 30)
                        before = display[:m.start()] if start == 0 else "..." + display[start:m.start()]
                        matched = display[m.start():m.end()]
                        after = display[m.end():m.end() + 60]
                        st.html(f'<code>{escape(before)}<mark>{escape(matched)}</mark>{escape(after)}</code>')

            if not results:
                st.info("No matches found.")

        if replace_term and results:
            st.divider()
            st.markdown("### Replace")
            st.warning(f"This will replace **{find_term}** → **{replace_term}** in {len(set(r['file'] for r in results))} file(s). Backups will be created.")
            if st.button("🔄 Replace All", type="primary", width="stretch"):
                count = 0
                fails = 0
                flags = 0 if case_sensitive else re.IGNORECASE
                for fp in sources:
                    if not os.path.exists(fp): continue
                    try:
                        content = read_file_safe(fp)
                        new_content = re.sub(re.escape(find_term), lambda _: replace_term, content, flags=flags)
                        if new_content != content:
                            backup_file(fp)
                            with open(fp, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            count += 1
                    except OSError as e:
                        fails += 1
                        st.error(f"Failed to replace in {fp}: {e}")
                if count:
                    st.success(f"Replaced in {count} file(s)! Reload Shell to see changes.")
                if fails:
                    st.error(f"{fails} file(s) failed — check errors above")
    else:
        st.info("Enter a search term above.")

with main_tab_export:
    st.markdown("## 📦 Export / Import Config")
    st.caption("Save your entire setup as a single file, or reload it later.")

    tab_export, tab_import = st.tabs(["📤 Export", "📥 Import"])

    with tab_export:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            with st.container(border=True):
                st.markdown("**Include files**")
                include_backups = st.checkbox("Include backups/ folder", value=False, key="export_backups")
                include_state = st.checkbox("Include theme state (colors, fonts)", value=True, key="export_state")

        if st.button("📦 Generate Export", type="primary", width="stretch"):
            buf = io.BytesIO()
            with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
                base = _SCRIPT_DIR
                skip_dirs = {".streamlit", "__pycache__", ".venv", "venv", ".git", ".opencode", "node_modules"}
                for root_dir, dirs, files in os.walk(base):
                    dirs[:] = [d for d in dirs if d not in skip_dirs]
                    for fn in files:
                        fp = os.path.join(root_dir, fn)
                        rel = os.path.relpath(fp, base)
                        if rel.startswith("backups") and not include_backups: continue
                        if rel == os.path.basename(__file__): continue
                        if fn.endswith(".nss") or fn in ("AGENTS.md", "SKILL.md"):
                            zf.write(fp, rel)
                if include_state:
                    state = {k: st.session_state.get(k, DEFAULTS[k]) for k in DEFAULTS if k != "stops"}
                    state["stops"] = current_stops()
                    zf.writestr("_state.json", json.dumps(state, indent=2))
            st.download_button("💾 Download export.zip", data=buf.getvalue(), file_name="nileshell-config.zip", mime="application/zip", width="stretch")
            st.caption("The export includes all `.nss` files, AGENTS.md, SKILL.md, and optionally backups + theme state.")

    with tab_import:
        uploaded = st.file_uploader("Upload a config ZIP file", type=["zip"], key="import_zip")
        if uploaded:
            st.warning("⚠️ This will overwrite your current `.nss` files. Backups will be created first.")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📥 Import & Overwrite", type="primary", width="stretch"):
                    try:
                        buf = io.BytesIO(uploaded.read())
                        written = []
                        with zipfile.ZipFile(buf, "r") as zf:
                            for name in zf.namelist():
                                if name == "_state.json":
                                    state_data = json.loads(zf.read(name))
                                    st.session_state._pending_state = {k: v for k, v in state_data.items() if k in DEFAULTS}
                                    continue
                                # Only restore .nss files at the root or in imports/, never paths outside the project.
                                if not re.fullmatch(r"(imports/)?[\w.-]+\.nss", name): continue
                                dest = os.path.join(_SCRIPT_DIR, *name.split("/"))
                                os.makedirs(os.path.dirname(dest), exist_ok=True)
                                backup_file(dest)
                                with open(dest, "wb") as f:
                                    f.write(zf.read(name))
                                written.append(name)
                        st.toast(f"✅ Imported {len(written)} file(s). Reload Shell to see changes.")
                        st.rerun()
                    except (OSError, zipfile.BadZipFile, json.JSONDecodeError) as e:
                        st.error(f"Import failed: {e}")
            with col_b:
                if st.button("🚫 Cancel", width="stretch"):
                    st.rerun()

with main_tab_history:
    st.markdown("## 📜 Change History")
    st.caption("Every time you write a file, a timestamped backup is saved. Restore any previous version here.")

    tracked_files = {
        "shell.nss": SHELL_PATH,
        "theme.nss": THEME_PATH,
        "modify.nss": MODIFY_PATH,
        "custom.nss": CUSTOM_PATH,
    }
    for fn in sorted(os.listdir(IMPORTS_DIR)):
        fp = os.path.join(IMPORTS_DIR, fn)
        if fn.endswith(".nss") and fn not in tracked_files:
            tracked_files[fn] = fp

    file_choice = st.selectbox("Select a file to browse history", list(tracked_files.keys()), key="hist_file")
    filepath = tracked_files[file_choice]

    col_a, col_b = st.columns([1, 1])
    with col_a:
        with st.container(border=True):
            st.markdown("**Current file**")
            if os.path.exists(filepath):
                st.code(read_file_safe(filepath), language="nss")
            else:
                st.caption("File doesn't exist yet")
    with col_b:
        with st.container(border=True):
            st.markdown("**Backups**")
            backups = list_backups(filepath)
            if not backups:
                st.caption("No backups yet — make a change to create one.")
            for ts, bak_path in backups:
                dt = datetime.strptime(ts, "%Y%m%d_%H%M%S")
                label = dt.strftime("%Y-%m-%d %H:%M:%S")
                with st.expander(f"🕐 {label}"):
                    st.code(read_file_safe(bak_path), language="nss")
                    if st.button(f"↩ Restore this version", key=f"restore_{ts}"):
                        try:
                            backup_file(filepath)
                            shutil.copy2(bak_path, filepath)
                            st.rerun()
                        except OSError as e:
                            st.error(f"Restore failed: {e}")

    st.divider()
    st.markdown("**All backups** are stored in the `backups/` folder — you can also browse them manually.")

with main_tab_help:
    st.markdown("## ❓ Help & Guide")

    st.markdown("#### 📖 Official Resources")
    st.markdown("- [**nilesoft.org/docs**](https://nilesoft.org/docs) — full reference for all NSS syntax, functions, variables, and IDs.")
    st.markdown("- [**GitHub: moudey/shell**](https://github.com/moudey/shell) — source code, issues, and community contributions.")

    with st.expander("🚀 Getting started", expanded=True):
        st.markdown("""
        1. **➕ Menu Items** — define items with title, command, icon, where-condition. Click **Append to custom.nss** to save
        2. **🔄 Modify** — hide or reposition existing system items. Click **Append to modify.nss** to save
        3. **⚙️ Settings** — change priority, delay, tooltips, exclude condition. Click **Write settings** to save
        4. **📂 Imports** — toggle, open, and edit individual `.nss` files without leaving the app
        5. **🎨 Theme** — edit colors, gradient, font, border, shadow. Click **Write to theme.nss** to save
        6. **Reload Shell** — hold **Ctrl** + **right-click** desktop/taskbar → **Shell → Update changes**
        """)
    with st.expander("📁 File structure"):
        st.markdown("""
        - `shell.nss` — main entry point. Contains `settings` block and imports for all modules below
        - `imports/theme.nss` — visual theme (menu background, colors, gradient, font, border, shadow)
        - `imports/modify.nss` — modify rules: hide, move, reposition existing system items
        - `imports/custom.nss` — your custom items (appended by the Menu Items tab; auto-created)
        - `imports/images.nss` — ~100 SVG image definitions (browse them in 🖼️ Icons)
        - `imports/terminal.nss` — terminal/command prompt entries
        - `imports/file-manage.nss` — file operations (copy path, attributes, ownership, etc.)
        - `imports/develop.nss` — dev tools (VS Code, dotnet, etc.)
        - `imports/goto.nss` — quick navigation shortcuts
        - `imports/taskbar.nss` — taskbar-specific items
        - `backups/` — auto-created timestamps backups of every file before overwrite
        - `AGENTS.md`, `SKILL.md` — AI assistant context files (included in exports)
        """)
    with st.expander("➕ Menu Items guide"):
        st.markdown("""
        - **Title** — the label shown in the context menu (default: `My App`)
        - **Command** — executable name or full path (e.g. `notepad.exe`, `code`, `cmd.exe`)
        - **Arguments** — extra args; use `@sel.path` for the selected file/folder path
        - **Icon** — use `icon.name` (built-in Shell icons), a glyph like `\\uE10A`, or a path to an `.exe`/`.dll`/image
        - **Where condition** — NSS expression controlling visibility. Examples: `sel.count>0`, `sel.type=='file'`, `window.is_desktop`
        - **Type filter** — one of `'file'`, `'dir'`, `'drive'`, `'*'` (blank = all). Wraps the item: `item(type='file' ...)`
        - **Run as admin** — adds the `admin` flag to the item definition
        - **Separator** — adds `sep=sep.top`, `sep=sep.bottom`, or `sep=sep.both`
        - Click **Append to custom.nss** to save. If the `import 'imports/custom.nss'` line is missing from `shell.nss`, it is added automatically
        """)
    with st.expander("🔄 Modify reference"):
        st.markdown("""
        - **Action dropdown**: `Move to menu`, `Hide (remove)`, or `Set position`
        - **Target item ID** — select from the dropdown of 20+ built-in IDs (e.g. `id.copy_as_path`, `id.properties`, `id.format`)
        - **Custom pattern** — override with `find="text*"` (match by name) or `this.id==id.xxx` (match by ID)
        - **Type filter** — `'file'`, `'dir'`, `'dir.back|drive.back'`, blank = all. Prepended as `type=...` in the `modify()` call
        - **Target menu** — name of your custom menu to move items into (default: `file manage`)
        - **Position** — `top`, `middle`, `bottom`, a number, or blank (unchanged)
        - **Separator** — `top`, `bottom`, or `both` around the item in its new position
        - The append button is disabled until a target ID or custom pattern is set
        - Appends to `imports/modify.nss` — must be imported by `shell.nss`
        """)
    with st.expander("⚙️ Settings guide"):
        st.markdown("""
        - **Priority** — integer 0–10. Higher = this menu loads after lower-priority menus. Default: 1
        - **Show delay** — milliseconds before the menu appears. Default: 200
        - **Exclude condition** — NSS where-expression that hides the Shell menu. Default: `!process.is_explorer` (only shown in Explorer)
        - **Enable tooltips** — toggles `tip.enabled`. When on, items can show a tooltip on hover
        - **Remove duplicate items** — toggles `modify.remove.duplicate`. Removes duplicate items injected by other software
        - Click **Write settings to shell.nss** to save. The settings block is replaced in-place via regex — only the `settings { ... }` block is touched, everything else in `shell.nss` is preserved
        - If no existing settings block is found, one is prepended to the file
        """)
    with st.expander("📂 Imports guide"):
        st.markdown("""
        - Lists all `.nss` files found in `imports/` directory
        - **✅/❌** badge shows whether each file is currently imported by `shell.nss`
        - **Add import** — appends `import 'imports/filename.nss'` to `shell.nss`
        - **Remove import** — removes the exact import line from `shell.nss` (doesn't delete the file) — checks for both single and double quotes
        - **Open** — loads the file content into a `st.text_area` for inline editing
        - **Save** — writes the edited content back to the file (with backup first)
        - Useful for temporarily disabling a module without deleting files
        - The inline editor is per-file and persists across reruns until closed
        """)
    with st.expander("🖼️ Icon Browser guide"):
        st.markdown("""
        - Browse all SVG images defined in `imports/images.nss` — parsed from `@name='<svg>...'` declarations
        - Colors come from **🎨 Theme → Icons**: `@image.color1` (main), `@image.color2` (accent), `@image.color3` / `@color3` (tertiary)
        - Each icon shows its first name with a copy button
        - Built-in Shell icons use the `icon.name` notation (e.g. `image=icon.pin`)
        - Use the **search box** to filter icons by name
        """)
    with st.expander("🔍 Find & Replace guide"):
        st.markdown("""
        - **Search** across `shell.nss` and all `.nss` files in `imports/`
        - Results show **file name**, **line number**, and a **bold-highlighted match** with surrounding context
        - Toggle **Aa** for case-sensitive matching (default: case-insensitive)
        - **Replace All** only shows when results exist — backs up each changed file first (see 📜 History)
        - Per-file error handling: failures in one file don't stop replacements in others
        - Each matching line is shown with ~60 chars context before/after the match
        - Always verify replacements in the **📜 History** tab afterward
        """)
    with st.expander("📦 Export/Import guide"):
        st.markdown("""
        - **Export** bundles all `.nss` files + `AGENTS.md` + `SKILL.md` into a single ZIP
        - Optionally include **backups/** folder and **theme state** (theme colors, font, gradient, border, shadow settings — not editor content or search state)
        - **Import** restores `.nss` files (project root and `imports/` only) and theme state from a previously exported ZIP — every overwritten file is backed up first
        - The app's own code (`theme-tweaker.py`) is **never** included in exports
        - Junk directories (`.streamlit`, `__pycache__`, `.venv`, `.git`, `node_modules`) are automatically excluded
        - Theme state contains only theme editor values (colors, gradient, border, shadow, font)
        """)
    with st.expander("✅ Syntax Checker guide"):
        st.markdown("""
        - Select any `.nss` file from the dropdown (`shell.nss` or any file in `imports/`)
        - Tracks **brace depth** `{ }` and **parenthesis depth** `( )` across the file
        - Reports:
          - **Line-level errors**: extra `}` or `)` on each line (resets depth to 0)
          - **File-level errors**: unclosed braces/parens remaining at EOF
        - `//` and `/* */` comments are skipped
        - Content inside single-quoted `'...'` and double-quoted `"..."` strings is ignored
        - Does **not** check: NSS keyword validity, variable references, image names, or type correctness
        - For detailed runtime errors, check `shell.log` in your Shell installation folder
        """)
    with st.expander("📋 Item Library guide"):
        st.markdown("""
        - Pre-built snippets for common context menu actions (VS Code, Terminal, Notepad, Take Ownership, Copy Path, and more)
        - Use the copy icon on a snippet, then paste it into `custom.nss` via the **📂 Imports** editor
        - Edit the title, icon, or command to taste before saving
        """)
    with st.expander("🎨 Theme tips"):
        st.markdown("""
        - **Effect 2 (Blur)** or **3 (Acrylic)** + gradient = best look on modern Windows, but GPU-dependent
        - **Effect 0 (Disable)** = no transparency effect, most compatible
        - **Effect 1 (Transparent)** = simple transparency without blur
        - The editor starts from `imports/theme.nss`; **📖 Reload theme.nss** discards unsaved edits, **Pick a preset** applies colors only
        - If text is unreadable on your gradient, toggle between **black** and **white** text colors
        - Use **presets** as a starting point, then tweak individual sliders
        - The **gradient preview bar** shows exactly how your colors will blend
        - The **live preview pane** renders a simplified mockup of your menu tree with the current theme values
        - **Write to theme.nss** replaces the entire file with your current settings (a backup is saved first)
        """)
    with st.expander("🤖 LLM Instructions (copy-paste for AI assistants)"):
        st.markdown("""
        Give the following to any AI assistant to give them full context about this project:

        **Quick context (short version):**
        ```
        I use Nilesoft Shell to customize my Windows context menu. All config files are in the script folder. The main entry is shell.nss which imports modules from imports/. After editing any .nss file, reload with Ctrl+right-click desktop → Shell → Update changes. Check shell.log for errors. Official docs at https://nilesoft.org/docs
        ```
        """)
        with st.container(border=True):
            st.markdown("**📄 Full context (AGENTS.md):**")
            agents_content = read_file_safe(os.path.join(_SCRIPT_DIR, "AGENTS.md"))
            st.code(agents_content, language="markdown")

        with st.container(border=True):
            st.markdown("**🎯 Skill instructions (SKILL.md):**")
            skill_content = read_file_safe(os.path.join(_SCRIPT_DIR, "SKILL.md"))
            st.code(skill_content, language="markdown")

        st.markdown("These files also exist on disk at `AGENTS.md` and `SKILL.md` — you can share them directly with any AI assistant.")
    with st.expander("💾 Reload & troubleshooting"):
        st.markdown("""
        **Reloading after changes:**
        1. Hold the **Ctrl** key
        2. **Right-click** on your desktop or taskbar
        3. From the context menu, click **Shell → Update changes**
        4. Or restart Windows Explorer from Task Manager

        **If something breaks:**
        - The **Syntax Checker** (in Imports tab) catches unmatched `{}` / `()` before they cause issues
        - If errors occur after reload, check `shell.log` in your Shell installation folder
        - The log shows file path, line number, and a description of the error
        - Open the reported file in the **📂 Imports** tab editor, fix the issue, and save
        - Use the **📜 History** tab to restore a previous working version of any file
        - Restart Explorer (Task Manager → Windows Explorer → Restart) to force a clean reload
        - If nothing works, restore the most recent backup from the `backups/` folder

        **Official support:**
        - Docs: [nilesoft.org/docs](https://nilesoft.org/docs)
        - GitHub: [github.com/moudey/shell](https://github.com/moudey/shell)
        """)
