# Favorite Applications and Directories Example

```nss
menu(type='desktop|taskbar' title='Favorites' image=#00ff00)
{
	menu(title='Applications' image=#ff0000)
	{
		item(title='Command prompt' image cmd='cmd.exe')
		item(title='PowerShell' image cmd='powershell.exe')
		item(title='Registry editor' image cmd='regedit.exe')
		separator
		item(title='Paint' image cmd='mspaint.exe')
		item(title='Notepad' image cmd='notepad.exe')
	}
	separator
	menu(title='Directories' image=#0000ff)
	{
		item(title='Downloads' cmd=user.downloads)
		item(title='Pictures' cmd=user.pictures)
		item(title='Home' cmd=user.directory)
		separator
		item(title='Windows' cmd=sys.directory)
		item(title='Program files' cmd=sys.prog())
	}
}
```
