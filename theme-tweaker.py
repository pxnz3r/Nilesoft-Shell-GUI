import streamlit as st
import os
import re
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
    "theme_name": "modern", "dark": "auto", "theme_view": "compact",
    "bg_color": "#0a0a1a", "bg_opacity": 100, "bg_effect": 2,
    "gradient_enabled": True, "grad_type": "linear",
    "lx1v": 0, "lx2v": 100, "ly1v": 0, "ly2v": 0,
    "stops": [[0, "#0a0a1a"], [0.33, "#1a1a3e"], [0.66, "#0f2255"], [1, "#0a0a2e"]],
    "text_normal": "#ffffff", "text_select": "#ffffff",
    "item_bg_normal": "none", "item_bg_select": "#ffffff20", "item_radius": 0,
    "img_c1": "#cccccc", "img_c2": "#aaaaaa", "img_c3": "#888888", "img_align": 2,
    "border_enabled": False, "border_size": 1, "border_color": "#000000",
    "border_opacity": 50, "border_radius": 4,
    "shadow_enabled": True, "shadow_size": 8, "shadow_color": "#000000",
    "shadow_opacity": 40, "shadow_offset": 2,
    "customize_font": False, "font_size": 9, "font_name": "Segoe UI", "font_weight": 4,
}

if "preset" not in st.session_state:
    st.session_state.preset = "Navy Indigo"

def apply_preset(name):
    p = PRESETS[name]
    for k in ["bg_color", "bg_opacity", "bg_effect", "stops", "text_normal", "text_select", "img_c1", "img_c2", "img_c3"]:
        st.session_state[k] = p[k]
    st.session_state.preset = name

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

def read_file_safe(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        try:
            with open(path, "r", encoding="cp1252") as f:
                return f.read()
        except:
            return ""

def parse_shell_settings(content):
    s = {"priority": "1", "showdelay": "200", "tip_enabled": True, "remove_duplicate": True, "exclude_where": ""}
    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("priority="): s["priority"] = line.split("=", 1)[1]
        elif line.startswith("showdelay="): s["showdelay"] = line.split("=", 1)[1]
        elif line.startswith("tip.enabled="): s["tip_enabled"] = line.split("=", 1)[1] == "1" or line.split("=", 1)[1].lower() == "true"
        elif line.startswith("modify.remove.duplicate="): s["remove_duplicate"] = line.split("=", 1)[1] == "1" or line.split("=", 1)[1].lower() == "true"
        elif line.startswith("exclude.where"):
            if "=" in line:
                s["exclude_where"] = line.split("=", 1)[1].strip()
    return s

BACKUP_DIR = os.path.join(_SCRIPT_DIR, "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)

def backup_file(filepath):
    """Save a timestamped backup before overwriting."""
    if not os.path.exists(filepath): return
    try:
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        fname = os.path.basename(filepath)
        bak = os.path.join(BACKUP_DIR, f"{fname}.{ts}")
        with open(filepath, "r", encoding="utf-8") as src:
            with open(bak, "w", encoding="utf-8") as dst:
                dst.write(src.read())
    except Exception as e:
        st.warning(f"Backup failed for {filepath}: {e}")

def list_backups(filepath):
    """Return sorted list of (timestamp, backup_path) for a given file."""
    fname = os.path.basename(filepath)
    pattern = f"{fname}."
    backups = []
    if not os.path.isdir(BACKUP_DIR): return backups
    for b in os.listdir(BACKUP_DIR):
        if b.startswith(pattern):
            ts = b[len(pattern):]
            backups.append((ts, os.path.join(BACKUP_DIR, b)))
    return sorted(backups, reverse=True)

main_tab_items, main_tab_modify, main_tab_settings, main_tab_imports, main_tab_theme, main_tab_icons, main_tab_find, main_tab_export, main_tab_history, main_tab_help = st.tabs(
    ["➕ Menu Items", "🔄 Modify", "⚙️ Settings", "📂 Imports", "🎨 Theme", "🖼️ Icons", "🔍 Find", "📦 Export", "📜 History", "❓ Help"]
)

with main_tab_items:
    st.markdown("## Create custom menu items")
    st.caption("Define new items and submenus. Saved to `imports/custom.nss`.")

    if not os.path.exists(CUSTOM_PATH):
        st.info("`custom.nss` doesn't exist yet. Append your first item to create it.")
        if st.button("➕ Add import to shell.nss automatically"):
            with open(SHELL_PATH, "a", encoding="utf-8") as f:
                f.write("\nimport 'imports/custom.nss'\n")
            st.success("Added `import 'imports/custom.nss'` to shell.nss")

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
    if item_type: parts.append(f'type={item_type}')
    if item_where: parts.append(f"where={item_where}")
    cmd_str = f"cmd='{item_cmd}'"
    if item_args: cmd_str += f" args='{item_args}'"
    parts.append(f"title='{item_title}'")
    parts.append(cmd_str)
    if item_sep != "none": parts.append(f'sep=sep.{item_sep}')
    if item_admin: parts.append("admin")
    if item_icon: parts.append(f"image={item_icon}")
    indent = "\n    "
    preview_code = f"item({indent}{indent.join(parts)}\n)"
    st.code(preview_code, language="nss")

    if st.button("➕ Append to custom.nss", type="primary", use_container_width=True):
        try:
            backup_file(CUSTOM_PATH) if os.path.exists(CUSTOM_PATH) else None
            with open(CUSTOM_PATH, "a", encoding="utf-8") as f:
                f.write("\n" + preview_code + "\n")
            shell_raw = read_file_safe(SHELL_PATH)
            import_q_single = "import 'imports/custom.nss'"
            import_q_double = 'import "imports/custom.nss"'
            if import_q_single not in shell_raw and import_q_double not in shell_raw:
                backup_file(SHELL_PATH)
                with open(SHELL_PATH, "a", encoding="utf-8") as sf:
                    sf.write(f"\n{import_q_single}\n")
            st.success("Appended!")
        except Exception as e:
            st.error(f"Failed to write: {e}")

    custom_content = ""
    if os.path.exists(CUSTOM_PATH):
        with open(CUSTOM_PATH, "r", encoding="utf-8") as f:
            custom_content = f.read()
    if custom_content.strip():
        with st.expander("📄 Current custom.nss", expanded=False):
            st.code(custom_content, language="nss")

    with st.expander("📋 Item Library — pre-built templates"):
        st.caption("Click an item to copy its NSS code, then paste into your custom.nss or edit above.")
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
            if st.button(f"📋 {label}", key=f"tmpl_{label}", use_container_width=True):
                st.toast(f"Copied: {label}")
                st.session_state["copied_template"] = code

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
            mod_pos = st.selectbox("Position", ["", "top", "bottom", "1", "2", "last"], key="mp")
            mod_sep = st.selectbox("Separator", ["none", "top", "bottom", "both"], key="ms")

    st.markdown("### Preview")
    target_expr = mod_target_custom if mod_target_custom else (f"this.id=={mod_target}" if mod_target else "this.id==id.properties")
    mod_lines = []
    if not mod_target and not mod_target_custom:
        mod_lines.append("// Select a target item or enter a custom pattern above")
    elif mod_action == "Hide (remove)":
        mod_lines.append(f"modify(where={target_expr} vis=vis.remove)")
    else:
        parts = [f"where={target_expr}"]
        if mod_where_type: parts.insert(0, f'type="{mod_where_type}"')
        if mod_pos: parts.append(f'pos={mod_pos}' if mod_pos.isdigit() else f'pos="{mod_pos}"')
        if mod_sep != "none": parts.append(f'sep="{mod_sep}"')
        if mod_action == "Move to menu": parts.append(f'menu="{mod_menu}"')
        mod_lines.append("modify(" + " ".join(parts) + ")")

    mod_code = "\n".join(mod_lines)
    st.code(mod_code, language="nss")

    if st.button("➕ Append to modify.nss", type="primary", use_container_width=True):
        try:
            backup_file(MODIFY_PATH)
            with open(MODIFY_PATH, "a", encoding="utf-8") as f:
                f.write("\n" + mod_code + "\n")
            st.success("Appended!")
        except Exception as e:
            st.error(f"Failed to write modify.nss: {e}")

    mod_content = ""
    if os.path.exists(MODIFY_PATH):
        with open(MODIFY_PATH, "r") as f:
            mod_content = f.read()
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
            s_priority = st.number_input("Priority", 0, 10, int(shell_settings["priority"]),
                help="Higher = menus load after others (default 1)")
            s_showdelay = st.number_input("Show delay (ms)", 0, 2000, int(shell_settings["showdelay"]),
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

    if st.button("💾 Write settings to shell.nss", type="primary", use_container_width=True):
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
        except Exception as e:
            st.error(f"Failed to write settings: {e}")

with main_tab_imports:
    st.markdown("## 📂 Import Manager")
    st.caption("View and toggle all imported `.nss` files.")

    imports_content = read_file_safe(SHELL_PATH)
    import_lines = [l.strip() for l in imports_content.split("\n") if l.strip().startswith("import")]

    st.markdown("### Current imports in shell.nss")
    import_files = []
    for l in import_lines:
        path = l.split("'")[1] if "'" in l else l.split('"')[1]
        import_files.append(path)

    available = []
    if os.path.isdir(IMPORTS_DIR):
        available = sorted([f for f in os.listdir(IMPORTS_DIR) if f.endswith(".nss")])

    col_a, col_b = st.columns([1, 1])
    with col_a:
        with st.container(border=True):
            st.markdown("**Imported**")
            for f in import_files:
                fname = os.path.basename(f.replace("imports/", ""))
                st.markdown(f"- `{fname}`")
    with col_b:
        with st.container(border=True):
            st.markdown("**Available in imports/**")
            for f in available:
                full_path = os.path.join("imports", f)
                is_imported = full_path in import_files or f"'{full_path}'" in import_lines or f'"{full_path}"' in import_lines
                st.markdown(f"- `{f}` {'✅' if is_imported else '❌ Not imported'}")

    with st.container(border=True):
        st.markdown("**Quick actions**")
        for f in available:
            full_ref = f"imports/{f}"
            is_in = full_ref in import_files
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1: st.text(f)
            with col2:
                if st.button("Open", key=f"open_{f}", use_container_width=True):
                    fp = os.path.join(IMPORTS_DIR, f)
                    content = read_file_safe(fp)
                    st.session_state[f"editor_{f}"] = content
            with col3:
                label = "Remove import" if is_in else "Add import"
                if st.button(label, key=f"toggle_{f}", use_container_width=True):
                    try:
                        if is_in:
                            lines = open(SHELL_PATH, "r").readlines()
                            lines = [l for l in lines if f"import '{full_ref}'" not in l and f'import "{full_ref}"' not in l]
                            open(SHELL_PATH, "w", encoding="utf-8").writelines(lines)
                        else:
                            with open(SHELL_PATH, "a") as sf:
                                sf.write(f"\nimport '{full_ref}'")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update imports: {e}")
            if st.session_state.get(f"editor_{f}"):
                with st.expander(f"📄 {f}", expanded=True):
                    edited = st.text_area(f"Edit {f}", st.session_state[f"editor_{f}"], height=200, key=f"area_{f}")
                    if st.button(f"💾 Save {f}", key=f"save_{f}"):
                        try:
                            backup_file(os.path.join(IMPORTS_DIR, f))
                            with open(os.path.join(IMPORTS_DIR, f), "w", encoding="utf-8") as fp:
                                fp.write(edited)
                            st.success(f"Saved {f}!")
                        except Exception as e:
                            st.error(f"Failed to save {f}: {e}")

    with st.expander("✅ Syntax Checker — validate NSS files"):
        st.caption("Checks for common issues: unmatched braces, parens, and invalid syntax.")
        sc_file = st.selectbox("Select file to check", ["shell.nss"] + sorted([f for f in os.listdir(IMPORTS_DIR) if f.endswith(".nss")]), key="sc_file")
        sc_path = SHELL_PATH if sc_file == "shell.nss" else os.path.join(IMPORTS_DIR, sc_file)
        sc_content = read_file_safe(sc_path)
        if st.button("🔍 Check Syntax", key="sc_check", use_container_width=True):
            errors = []
            lines = sc_content.split("\n")
            brace_depth = 0
            paren_depth = 0
            in_sq = in_dq = False
            for ln, line in enumerate(lines, 1):
                stripped = line.strip()
                if stripped.startswith("//") or stripped.startswith("#"): continue
                i = 0
                while i < len(line):
                    c = line[i]
                    if c == "'" and not in_dq: in_sq = not in_sq
                    elif c == '"' and not in_sq: in_dq = not in_dq
                    elif not in_sq and not in_dq:
                        if c == "{": brace_depth += 1
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
    st.caption("Customize the look of your context menu.")

    preset_cols = st.columns([2, 1])
    with preset_cols[0]:
        selected = st.selectbox("Color scheme preset", list(PRESETS.keys()),
            index=list(PRESETS.keys()).index(st.session_state.preset), key="preset_selector")
        if selected != st.session_state.preset:
            apply_preset(selected)
            st.rerun()
    with preset_cols[1]:
        st.markdown("")
        st.markdown("")
        if st.button("↺ Reset defaults", use_container_width=True):
            for k in DEFAULTS:
                st.session_state.pop(k, None)
            st.session_state.preset = "Navy Indigo"
            st.rerun()

    sub_bg, sub_item, sub_icon, sub_border, sub_shadow, sub_font = st.tabs(
        ["🎨 Background", "📝 Items", "🖼️ Icons", "🧱 Border", "🌓 Shadow", "🔤 Font"]
    )

    with sub_bg:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**General**")
                theme_name = st.selectbox("Theme name", ["modern", "classic", "white", "black"],
                    index=["modern", "classic", "white", "black"].index(st.session_state.get("theme_name", DEFAULTS["theme_name"])),
                    key="theme_name")
                dark = st.selectbox("Dark mode", ["auto", "true", "false"],
                    index=["auto", "true", "false"].index(st.session_state.get("dark", DEFAULTS["dark"])),
                    key="dark")
                theme_view = st.selectbox("Menu density", ["compact", "small", "medium", "large", "wide"],
                    index=["compact", "small", "medium", "large", "wide"].index(st.session_state.get("theme_view", DEFAULTS["theme_view"])),
                    key="theme_view")
                bg_color = st.color_picker("Base color", st.session_state.get("bg_color", DEFAULTS["bg_color"]), key="bg_color")
                bg_opacity = st.slider("Opacity", 0, 100, st.session_state.get("bg_opacity", DEFAULTS["bg_opacity"]), key="bg_opacity")
                bg_effect = st.selectbox("Effect", [0, 1, 2, 3],
                    index=[0, 1, 2, 3].index(st.session_state.get("bg_effect", DEFAULTS["bg_effect"])),
                    format_func=lambda x: {0: "0 - Solid", 1: "1 - Transparent", 2: "2 - Blur", 3: "3 - Acrylic"}[x],
                    key="bg_effect")
        with c2:
            with st.container(border=True):
                st.markdown("**Gradient**")
                gradient_enabled = st.toggle("Enable", st.session_state.get("gradient_enabled", DEFAULTS["gradient_enabled"]), key="gradient_enabled")
                if gradient_enabled:
                    grad_type = st.selectbox("Type", ["linear", "radial"],
                        index=["linear", "radial"].index(st.session_state.get("grad_type", DEFAULTS["grad_type"])), key="grad_type")
                    if grad_type == "linear":
                        cols = st.columns(4)
                        with cols[0]: lx1v = st.number_input("X1", 0, 100, st.session_state.get("lx1v", 0), key="lx1v")
                        with cols[1]: lx2v = st.number_input("X2", 0, 100, st.session_state.get("lx2v", 100), key="lx2v")
                        with cols[2]: ly1v = st.number_input("Y1", 0, 100, st.session_state.get("ly1v", 0), key="ly1v")
                        with cols[3]: ly2v = st.number_input("Y2", 0, 100, st.session_state.get("ly2v", 0), key="ly2v")
                    else:
                        cols = st.columns(5)
                        with cols[0]: rcx = st.number_input("CX", 0, 100, 100)
                        with cols[1]: rcy = st.number_input("CY", 0, 100, 100)
                        with cols[2]: rr = st.number_input("R", 0, 200, 150)
                        with cols[3]: rfx = st.number_input("FX", 0, 100, 100)
                        with cols[4]: rfy = st.number_input("FY", 0, 100, 100)
                    stops_data = st.session_state.get("stops", DEFAULTS["stops"])
                    num_stops = st.number_input("Stops", min_value=2, max_value=6, value=len(stops_data), key="num_stops")
                    stops = []
                    for i in range(int(num_stops)):
                        sc1, sc2 = st.columns([1, 2])
                        with sc1:
                            off = st.slider(f"S{i+1}", 0.0, 1.0,
                                value=float(stops_data[i][0] if i < len(stops_data) else i / (num_stops - 1) if num_stops > 1 else 0.5),
                                step=0.01, key=f"so_{i}", label_visibility="collapsed")
                        with sc2:
                            col = st.color_picker(f"C{i+1}", stops_data[i][1] if i < len(stops_data) else "#000000",
                                key=f"sc_{i}", label_visibility="collapsed")
                        stops.append([off, col])
                    grad_bar = "linear-gradient(to right" + "".join(f", {s[1]} {int(s[0]*100)}%" for s in stops) + ")"
                    st.markdown(f'<div style="height:20px;border-radius:6px;border:1px solid #444;background:{grad_bar};margin-top:8px"></div>', unsafe_allow_html=True)
                else:
                    stops = DEFAULTS["stops"]

    with sub_item:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**Text colors**")
                text_normal = st.color_picker("Normal", st.session_state.get("text_normal", DEFAULTS["text_normal"]), key="text_normal")
                text_select = st.color_picker("Hover", st.session_state.get("text_select", DEFAULTS["text_select"]), key="text_select")
        with c2:
            with st.container(border=True):
                st.markdown("**Item background**")
                item_bg_normal = st.text_input("Normal", st.session_state.get("item_bg_normal", DEFAULTS["item_bg_normal"]),
                    help="Hex color or 'none'", key="item_bg_normal")
                item_bg_select = st.text_input("Hover", st.session_state.get("item_bg_select", DEFAULTS["item_bg_select"]),
                    help="e.g. #ffffff20", key="item_bg_select")
                item_radius = st.slider("Corner radius", 0, 3, st.session_state.get("item_radius", DEFAULTS["item_radius"]), key="item_radius")

    with sub_icon:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                st.markdown("**Colors**")
                img_c1 = st.color_picker("Color 1 (main)", st.session_state.get("img_c1", DEFAULTS["img_c1"]), key="img_c1")
                img_c2 = st.color_picker("Color 2", st.session_state.get("img_c2", DEFAULTS["img_c2"]), key="img_c2")
                img_c3 = st.color_picker("Color 3", st.session_state.get("img_c3", DEFAULTS["img_c3"]), key="img_c3")
        with c2:
            with st.container(border=True):
                st.markdown("**Display**")
                img_align = st.selectbox("Alignment", [0, 1, 2],
                    index=[0, 1, 2].index(st.session_state.get("img_align", DEFAULTS["img_align"])),
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
                border_enabled = st.toggle("Enable", st.session_state.get("border_enabled", DEFAULTS["border_enabled"]), key="border_enabled")
                border_size = st.slider("Size", 0, 10, st.session_state.get("border_size", DEFAULTS["border_size"]), key="border_size")
                border_color = st.color_picker("Color", st.session_state.get("border_color", DEFAULTS["border_color"]), key="border_color")
        with c2:
            with st.container(border=True):
                border_opacity = st.slider("Opacity", 0, 100, st.session_state.get("border_opacity", DEFAULTS["border_opacity"]), key="border_opacity")
                border_radius = st.slider("Radius", 0, 20, st.session_state.get("border_radius", DEFAULTS["border_radius"]), key="border_radius")

    with sub_shadow:
        c1, c2 = st.columns(2)
        with c1:
            with st.container(border=True):
                shadow_enabled = st.toggle("Enable", st.session_state.get("shadow_enabled", DEFAULTS["shadow_enabled"]), key="shadow_enabled")
                shadow_size = st.slider("Size", 0, 30, st.session_state.get("shadow_size", DEFAULTS["shadow_size"]), key="shadow_size")
                shadow_color = st.color_picker("Color", st.session_state.get("shadow_color", DEFAULTS["shadow_color"]), key="shadow_color")
        with c2:
            with st.container(border=True):
                shadow_opacity = st.slider("Opacity", 0, 100, st.session_state.get("shadow_opacity", DEFAULTS["shadow_opacity"]), key="shadow_opacity")
                shadow_offset = st.slider("Offset", 0, 30, st.session_state.get("shadow_offset", DEFAULTS["shadow_offset"]), key="shadow_offset")

    with sub_font:
        customize_font = st.checkbox("Customize font (disable to use system default — DPI-aware)", 
            value=st.session_state.get("customize_font", DEFAULTS["customize_font"]), key="customize_font")
        if customize_font:
            c1, c2 = st.columns(2)
            with c1:
                with st.container(border=True):
                    font_name = st.text_input("Font", st.session_state.get("font_name", DEFAULTS["font_name"]),
                        help="Must be installed on your system", key="font_name")
                    font_size = st.slider("Size", 6, 24, st.session_state.get("font_size", DEFAULTS["font_size"]), key="font_size")
            with c2:
                with st.container(border=True):
                    font_weight = st.slider("Weight", 1, 9, st.session_state.get("font_weight", DEFAULTS["font_weight"]), key="font_weight")
                    font_italic = st.toggle("Italic", False, key="font_italic")
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
            stops_list = s.get("stops", DEFAULTS["stops"])
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
        l.append("\n}")
        return "\n".join(l)

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
                if grad_type == "linear":
                    dx = lx2v - lx1v
                    dy = ly2v - ly1v
                    if dx == 0 and dy == 0: angle = "0deg"
                    elif dx == 0: angle = "to bottom" if dy > 0 else "to top"
                    elif dy == 0: angle = "to right" if dx > 0 else "to left"
                    else: angle = f"{90 - (dy/dx) * 45 if dx != 0 else 0}deg"  # approximate
                    stops_str = ", ".join(f"{s[1]} {int(s[0]*100)}%" for s in stops)
                    grad_css = f"{angle}, {stops_str}"
                else:
                    stops_str = ", ".join(f"{s[1]} {int(s[0]*100)}%" for s in stops)
                    grad_css = f"circle at {rcx}% {rcy}%, {stops_str}"

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
                        html += f'  <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">{node["title"]}</span>\n'
                        html += '</div>\n'
                    elif node["type"] == "menu":
                        ci = icon_idx[0] % 3
                        icon_idx[0] += 1
                        icon_style = f"background:linear-gradient(135deg, {icon_colors[ci]}, {icon_colors[(ci + 1) % 3]})"
                        html += f'<div style="padding:2px {8 + depth * 12}px 2px {4 + depth * 12}px;display:flex;align-items:center;gap:8px;">\n'
                        html += f'  <span style="width:14px;height:14px;border-radius:2px;{icon_style};display:inline-block;flex-shrink:0;"></span>\n'
                        html += f'  <span style="flex:1;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">▶ {node["title"]}</span>\n'
                        html += '</div>\n'
                        # Render children at increased depth
                        if node.get("children"):
                            html += render_tree(node["children"], depth + 1)
                return html

            tree_html = ""
            for root in menu_roots:
                tree_html += f'<div style="padding:2px 12px 1px;font-size:10px;color:{hex_to_rgba(text_normal, 0.4)};text-transform:uppercase;letter-spacing:0.5px;">{root["source"]}</div>\n'
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
            item_count = sum(1 for r in menu_roots for c in r["children"] if c["type"] == "item")
            st.caption(f"Menu tree from {len(menu_roots)} source files. Third item highlighted as hover state.")
    with col_btn:
        with st.container(border=True):
            st.markdown("**💾 File**")
            if st.button("📖 Read theme.nss", use_container_width=True):
                if os.path.exists(THEME_PATH):
                    with open(THEME_PATH, "r") as f:
                        st.session_state.theme_content = f.read()
                    st.success("Loaded")
            if st.button("💾 Write to theme.nss", type="primary", use_container_width=True):
                try:
                    backup_file(THEME_PATH)
                    with open(THEME_PATH, "w", encoding="utf-8") as f:
                        f.write(generate_theme())
                    st.toast("✅ Written! Reload Shell (Ctrl+Right-click → Update)", icon="✅")
                except Exception as e:
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

    # Color slot preview
    c1, c2, c3 = st.columns(3)
    with c1: slot1 = st.color_picker("Slot 1 (image.color1)", st.session_state.get("img_c1", DEFAULTS["img_c1"]), key="icon_slot1")
    with c2: slot2 = st.color_picker("Slot 2 (image.color2)", st.session_state.get("img_c2", DEFAULTS["img_c2"]), key="icon_slot2")
    with c3: slot3 = st.color_picker("Slot 3 (image.color3)", st.session_state.get("img_c3", DEFAULTS["img_c3"]), key="icon_slot3")

    def render_svg(svg_text, s1, s2, s3):
        """Substitute color slots and render SVG."""
        r = svg_text.replace("@image.color1", s1).replace("@image.color2", s2).replace("@image.color3", s3)
        r = r.replace("@color3", s3).replace("@color_islight_WB", "#ffffff")
        clip = '<defs><clipPath id="clip0"><path fill="#fff" d="M0 0h16v16H0z"/></clipPath></defs>'
        r = r.replace("@clipPath", clip)
        r = re.sub(r"@if\([^)]+\)", "#ffffff", r)
        extras = 'width="24" height="24" xmlns="http://www.w3.org/2000/svg"'
        r = re.sub(r'<svg\s+', f'<svg {extras} ', r, count=1)
        return r

    search_icon = st.text_input("🔍 Filter icons by name", "", key="icon_search")

    displayed = [ic for ic in icons if not search_icon or any(search_icon.lower() in n.lower() for n in ic["names"])]
    st.markdown(f"**{len(displayed)} icons** (of {len(icons)} total)")

    cols = st.columns(4)
    for idx, ic in enumerate(displayed):
        with cols[idx % 4]:
            svg_html = render_svg(ic["svg"], slot1, slot2, slot3)
            icon_name = ic["names"][0]
            preview_div = f'<div style="width:48px;height:48px;display:flex;align-items:center;justify-content:center;background:#2a2a3e;border-radius:6px;border:1px solid #444;">{svg_html}</div>'
            st.markdown(f'<div style="text-align:center;padding:8px 0">{preview_div}<div style="font-size:11px;color:#aaa;margin-top:4px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap">{icon_name}</div></div>', unsafe_allow_html=True)
            if st.button("📋 Copy name", key=f"copy_icon_{idx}", use_container_width=True):
                st.toast(f"Copied: {icon_name}")
                st.session_state["copied_icon"] = icon_name

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
                        st.markdown(f'{before}**{matched}**{after}', unsafe_allow_html=True)

            if not results:
                st.info("No matches found.")

        if replace_term and results:
            st.divider()
            st.markdown("### Replace")
            st.warning(f"This will replace **{find_term}** → **{replace_term}** in {len(set(r['file'] for r in results))} file(s). Backups will be created.")
            if st.button("🔄 Replace All", type="primary", use_container_width=True):
                count = 0
                fails = 0
                flags = 0 if case_sensitive else re.IGNORECASE
                for fp in sources:
                    if not os.path.exists(fp): continue
                    try:
                        content = read_file_safe(fp)
                        new_content = re.sub(re.escape(find_term), replace_term, content, flags=flags)
                        if new_content != content:
                            backup_file(fp)
                            with open(fp, "w", encoding="utf-8") as f:
                                f.write(new_content)
                            count += 1
                    except Exception as e:
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

    import json, base64, io, zipfile

    tab_export, tab_import = st.tabs(["📤 Export", "📥 Import"])

    with tab_export:
        col_a, col_b = st.columns([1, 1])
        with col_a:
            with st.container(border=True):
                st.markdown("**Include files**")
                include_backups = st.checkbox("Include backups/ folder", value=False, key="export_backups")
                include_state = st.checkbox("Include theme state (colors, fonts)", value=True, key="export_state")

        if st.button("📦 Generate Export", type="primary", use_container_width=True):
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
                    state = {k: st.session_state[k] for k in st.session_state if not k.startswith("_") and not k.startswith("ci_") and not k.startswith("mt") and not k.startswith("mwt") and not k.startswith("mm") and not k.startswith("mp") and not k.startswith("ms") and not k.startswith("ma") and "editor_" not in k and "area_" not in k and "icon_" not in k and k not in ("preset_selector", "hist_file", "find_term", "replace_term", "find_case", "shell_install_dir")}
                    zf.writestr("_state.json", json.dumps(state, indent=2))
            st.download_button("💾 Download export.zip", data=buf.getvalue(), file_name="nileshell-config.zip", mime="application/zip", use_container_width=True)
            st.caption("The export includes all `.nss` files, AGENTS.md, SKILL.md, and optionally backups + theme state.")

    with tab_import:
        uploaded = st.file_uploader("Upload a config ZIP file", type=["zip"], key="import_zip")
        if uploaded:
            st.warning("⚠️ This will overwrite your current `.nss` files. Backups will be created first.")
            col_a, col_b = st.columns(2)
            with col_a:
                if st.button("📥 Import & Overwrite", type="primary", use_container_width=True):
                    try:
                        buf = io.BytesIO(uploaded.read())
                        with zipfile.ZipFile(buf, "r") as zf:
                            for name in zf.namelist():
                                if name == "_state.json":
                                    state_data = json.loads(zf.read(name))
                                    for k, v in state_data.items():
                                        st.session_state[k] = v
                                    continue
                                if name.startswith("backups"): continue
                                dest = os.path.join(_SCRIPT_DIR, name)
                                parent = os.path.dirname(dest)
                                if parent: os.makedirs(parent, exist_ok=True)
                                if os.path.exists(dest): backup_file(dest)
                                with open(dest, "wb") as f:
                                    f.write(zf.read(name))
                        st.success("✅ Imported! Reload Shell to see changes.")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Import failed: {e}")
            with col_b:
                if st.button("🚫 Cancel", use_container_width=True):
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
                            with open(bak_path, "r") as src:
                                with open(filepath, "w", encoding="utf-8") as dst:
                                    dst.write(src.read())
                            st.success(f"Restored version from {label}!")
                            st.rerun()
                        except Exception as e:
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
        - `imports/images.nss` — ~100 SVG icon definitions used via `image=@name` syntax
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
        - **Icon** — use `icon.name` (built-in Shell icons), a path to `.exe`/`.dll`, or `@svg_name` for an icon from `images.nss`
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
        - **Position** — `top`, `bottom`, `1` (numeric), `last`, or blank (unchanged)
        - **Separator** — `top`, `bottom`, or `both` around the item in its new position
        - When no target is selected, a comment is shown in preview. The append button still writes it as `// ...`
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
        - Browse all SVG icons defined in `imports/images.nss` — parsed from `@name` declarations
        - **3 color slot pickers** at the top let you preview how different colors affect each SVG
        - **Slot 1** → `@image.color1` — primary fill color in most icons
        - **Slot 2** → `@image.color2` — secondary accent color
        - **Slot 3** → `@image.color3` / `@color3` — background/tertiary color
        - Click **📋 Copy name** to store the icon name in app state (e.g. `copy_path`)
        - Reference SVGs in items with `image=@name` (e.g. `image=@copy_path`)
        - Built-in Shell icons use the `icon.name` notation (e.g. `image=icon.pin`) — these are separate
        - Use the **search box** to filter icons by name
        """)
    with st.expander("🔍 Find & Replace guide"):
        st.markdown("""
        - **Search** across `shell.nss` and all `.nss` files in `imports/`
        - Results show **file name**, **line number**, and a **bold-highlighted match** with surrounding context
        - Toggle **Aa** for case-sensitive matching (default: case-insensitive)
        - **Replace All** only shows when results exist — creates `.bak` backups via the History system
        - Per-file error handling: failures in one file don't stop replacements in others
        - Each matching line is shown with ~60 chars context before/after the match
        - Always verify replacements in the **📜 History** tab afterward
        """)
    with st.expander("📦 Export/Import guide"):
        st.markdown("""
        - **Export** bundles all `.nss` files + `AGENTS.md` + `SKILL.md` into a single ZIP
        - Optionally include **backups/** folder and **theme state** (theme colors, font, gradient, border, shadow settings — not editor content or search state)
        - **Import** restores a previously exported ZIP — creates `.bak` backups for every overwritten file
        - The app's own code (`theme-tweaker.py`) is **never** included in exports
        - Junk directories (`.streamlit`, `__pycache__`, `.venv`, `.git`, `node_modules`) are automatically excluded
        - Theme state excludes: editor content, search terms, icon color pickers, and transient UI keys
        """)
    with st.expander("✅ Syntax Checker guide"):
        st.markdown("""
        - Select any `.nss` file from the dropdown (`shell.nss` or any file in `imports/`)
        - Tracks **brace depth** `{ }` and **parenthesis depth** `( )` across the file
        - Reports:
          - **Line-level errors**: extra `}` or `)` on each line (resets depth to 0)
          - **File-level errors**: unclosed braces/parens remaining at EOF
        - Lines starting with `//` or `#` are skipped entirely
        - Content inside single-quoted `'...'` and double-quoted `"..."` strings is ignored
        - Does **not** check: NSS keyword validity, variable references, image names, or type correctness
        - For detailed runtime errors, check `shell.log` in your Shell installation folder
        """)
    with st.expander("📋 Item Library guide"):
        st.markdown("""
        - Pre-built templates for common context menu actions
        - Click any template button → code is stored in app state (visible as a toast)
        - The code then appears in the **preview** area above — append it like any item
        - Templates cover: VS Code, Terminal, Notepad, Take Ownership, Copy Path, and more
        - Edit the pasted code (title, icon, command) before appending to `custom.nss`
        """)
    with st.expander("🎨 Theme tips"):
        st.markdown("""
        - **Effect 2 (Blur with acrylic)** + gradient = best look on modern Windows, but GPU-dependent
        - **Effect 0 (Solid)** = fastest, no transparency, most compatible
        - **Effect 1 (Transparent)** = simple transparency without blur
        - If text is unreadable on your gradient, toggle between **black** and **white** text colors
        - Use **presets** as a starting point, then tweak individual sliders
        - The **gradient preview bar** shows exactly how your colors will blend
        - The **live preview pane** renders a simplified mockup of your menu tree with the current theme values
        - `color=auto` uses Windows accent color, but the picker still sets the value in theme.nss
        - Border, shadow, and font settings only affect top-level menus, not submenus, per Nilesoft Shell limitations
        - **Write to theme.nss** replaces the entire file with your current settings
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
