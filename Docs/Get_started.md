# Get Started

This tutorial will teach you the basics of Shell. It is not necessary to have any prior experience.

To start using Shell, you need a text editor, like Notepad, to write Shell code.

## Quickstart

Let's create our first menu item.

Open the configuration file `shell.nss` and write the following code and save:

```nss
item(title='Hello, World!' cmd=msg('Hello @user.name'))
```

> **Tip:** You find the configuration file `shell.nss` in the Shell program folder. To find the Shell program folder, use **Shift + Right-click** on the Taskbar. The Shell menu will appear at the top of the context menu. In its submenu, you can click on **directory** to open the folder where the Shell configuration files are saved.

Don't worry if you don't understand the code above — we will discuss it in detail in later chapters.

> **Tip:** After editing any `.nss` file, you'll need to update changes: hold **Ctrl + Right-click** on the desktop area or Taskbar to force Shell to reload the nss files. Alternatively, you can restart Windows Explorer.

The result will look something like this when you press the right-click in an empty place on the desktop:

---

Congratulations! You have now added your first menu item to the context menu.
