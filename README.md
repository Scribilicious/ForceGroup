# ForceGroup

A Sublime Text plugin that forces files to open in a specific group (pane), no matter which group is focused when they are opened.

Useful for multi-pane layouts where you want, for example, the editor group to always receive new files instead of a sidebar or terminal group.

The main reason I created this plugin is to keep, for example, an AI agent in the right pane and the files you edit in the left pane. When the agent is focused and you click a file in the file list, Sublime opens it in the focused (right) pane next to the agent. ForceGroup moves it to the left pane instead.

## How it works

When a file is shown, ForceGroup moves it to the configured target group and focuses it there. By default (`allow_manual_move`) this only happens the first time a file is shown, so you can drag it to another group afterwards. It skips:

- untitled buffers (no file on disk)
- `.sublime-settings` files, so **Edit Settings** keeps its side-by-side layout
- widgets such as the find panel
- windows with only one group

## Installation

### Package Control

1. Open the Command Palette (`Ctrl/Cmd+Shift+P`).
2. Run **Package Control: Install Package**.
3. Select **ForceGroup**.

### Manual

Clone this repository into your Sublime Text `Packages` directory (**Preferences → Browse Packages…**), named `ForceGroup`:

```sh
cd ~/Library/Application\ Support/Sublime\ Text/Packages   # macOS
git clone git@github.com:Scribilicious/ForceGroup.git ForceGroup
```

## Settings

Open **Preferences → Package Settings → ForceGroup → Settings**. The defaults are on the left, and your overrides go in the right-hand pane (saved to `Packages/User/ForceGroup.sublime-settings`):

| Setting   | Default | Description |
|-----------|---------|-------------|
| `enabled` | `true`  | Set to `false` to disable the plugin. |
| `group`   | `1`     | Group that files are forced into (1 = first group). If the layout has fewer groups, the last group is used. |
| `allow_manual_move` | `true` | `true`: a file is only forced into the group the first time it is shown, so you can drag it elsewhere afterwards. `false`: files are moved back whenever they are activated. |

## Commands

Available from the Command Palette (`Ctrl/Cmd+Shift+P`):

- **Force Group: Toggle** – turn the plugin on or off. The state is saved to the settings file.
- **Preferences: ForceGroup Settings** – open the default and user settings side by side.

## License

MIT – see [LICENSE](LICENSE).
