# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import subprocess
from libqtile import bar, extension, hook, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, KeyChord, Match, Screen
from libqtile.lazy import lazy
# Make sure 'qtile-extras' is installed or this config will not work.
from qtile_extras import widget
from qtile_extras.widget.decorations import BorderDecoration
#from qtile_extras.widget import StatusNotifier
import colors

colors = colors.Nord


mod = "mod4"
terminal = "kitty"
browser = "thorium-browser"
explorer = "thunar"
the_font = "JetBrainsMono Nerd Font"
vol_up = "amixer sset Master 5%+ unmute"
vol_down = "amixer sset Master 5%- unmute"
vol_mute = "amixer sset Master toggle"

# Custom function to swap master window and focused window
def swap_master_with_focused(qtile):
    layout = qtile.current_layout
    if len(layout.clients) < 2:
        return  # No point in swapping if there's only one window

    # Master window is the first window in the layout
    master = layout.clients[0]
    
    # Swap the focused window with the master window
    current_window = layout.clients[1]

    layout.swap(master, current_window)


keys = [
    # Volume control
    Key([mod], "Page_Up", lazy.spawn(vol_up), desc="Raise volume"),
    Key([mod], "Page_Down", lazy.spawn(vol_down), desc="Lower volume"),
    Key([mod], "Pause", lazy.spawn(vol_mute), desc="Mute/unmute volume"),
    # The essentials
    Key([mod], "x", lazy.spawn(terminal), desc="Terminal"),
    Key([mod], "r", lazy.spawn("rofi -show drun"), desc='Run Launcher'),
    Key([mod], "w", lazy.spawn(browser), desc='Web browser'),
    Key([mod], "b", lazy.hide_show_bar(position='all'), desc="Toggles the bar to show/hide"),
    Key([mod], "q", lazy.window.kill(), desc="Kill focused window"),
    Key([mod], "e", lazy.spawn(explorer), desc="Run explorer"),
    Key([mod, "shift"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "n", lazy.layout.reset(), desc="Reset all window sizes"),
    Key([mod], "j", lazy.layout.down(), desc="Move focus down"),
    Key([mod], "k", lazy.layout.up(), desc="Move focus up"),
    Key([mod], "h", lazy.layout.shrink(), desc="Grow window to the left"),
    Key([mod], "l", lazy.layout.grow(), desc="Grow window to the right"),
    Key([mod, "control"], "q", lazy.shutdown(), desc="Shutdown Qtile"),
    Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config"),
    Key([mod], "Return", lazy.function(swap_master_with_focused)),
    Key([mod], "equal",
        lazy.layout.grow_left().when(layout=["bsp", "columns"]),
        lazy.layout.grow().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    Key([mod], "minus",
        lazy.layout.grow_right().when(layout=["bsp", "columns"]),
        lazy.layout.shrink().when(layout=["monadtall", "monadwide"]),
        desc="Grow window to the left"
    ),
    
    # Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left"),
    # Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right"),
    # Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down"),
    # Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up"),

    Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down"),
    Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up"),
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    # Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal"),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key([mod], "t", lazy.window.toggle_floating(), desc="Toggle floating on the focused window"),
    # Key([mod], "r", lazy.spawncmd(), desc="Spawn a command using a prompt widget"),
]

groups = []
group_names = ["1", "2", "3", "4", "5",]
group_labels = ["", "", "", "", "",]
group_layouts = ["monadtall" for _ in range (len(group_names))]

for idx in range(len(group_names)):
    groups.append(
        Group(
            name = group_names[idx],
            layout = group_layouts[idx],
            label = group_labels[idx],
        )
    )

for i in groups:
    keys.extend(
        [
            # mod + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod + shift + group number = switch to & move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name, switch_group=True),
                desc="Switch to & move focused window to group {}".format(i.name),
            ),
            # Or, use below if you prefer not to switch to that group.
            # # mod + shift + group number = move focused window to group
            # Key([mod, "shift"], i.name, lazy.window.togroup(i.name),
            #     desc="move focused window to group {}".format(i.name)),
        ]
    )

layout_theme = {
    "border_width": 2,
    "margin": 8,
    "border_focus": colors[8],
    "border_normal": colors[8]
}

layouts = [
    layout.MonadTall(**layout_theme),
    layout.Columns(border_focus_stack=["#d75f5f", "#8f3d3d"], border_width=4),
    layout.Max(),
    # Try more layouts by unleashing below layouts.
    # layout.Stack(num_stacks=2),
    # layout.Bsp(),
    # layout.Matrix(),
    # layout.MonadTall(),
    # layout.MonadWide(),
    # layout.RatioTile(),
    # layout.Tile(),
    # layout.TreeTab(),
    # layout.VerticalTile(),
    # layout.Zoomy(),
]

widget_defaults = dict(
    font=the_font,
    fontsize=16,
    padding=0,
    fontweight="bold",
    background=colors[0]
)

extension_defaults = widget_defaults.copy()

screens = [
    Screen(
        top=bar.Bar(
            [
                widget.Image(
                    # filename = "~/.config/qtile/icons/logo.png",
                    scale = "False",
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal)},
                ),
                widget.CurrentLayoutIcon(
                    # custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                    foreground = colors[1],
                    padding = 4,
                    scale = 0.6
                ),
                widget.GroupBox(
                    fontsize = 16,
                    margin_y = 5,
                    margin_x = 5,
                    padding_y = 5,
                    padding_x = 5,
                    borderwidth = 2,
                    active = colors[8],
                    inactive = colors[1],
                    rounded = False,
                    highlight_color = colors[2],
                    highlight_method = "line",
                    this_current_screen_border = colors[7],
                    this_screen_border = colors [4],
                    other_current_screen_border = colors[7],
                    other_screen_border = colors[4],
                ),
                widget.CurrentLayout(
                    foreground = colors[1],
                    padding = 5
                ),
                widget.Prompt(
                    font=the_font,
                    fontsize=14,
                    foreground = colors[1]
                ),
                widget.WindowName(
                    foreground = colors[6],
                    max_chars = 100
                ),
                widget.AGroupBox(
                    center_aligned = False,
                    
                    border = colors[3],
                    foreground = colors[0],
                    background = colors[3],
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.CryptoTicker(
                    api = 'coinbase',
                    foreground = colors[0],
                    background = colors[5],
                    update_interval = 600,
                    crypto = 'BTC',
                    format = '  {amount:.2f} ',
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.CPU(
                    format = '  {load_percent}% ',
                    background = colors[4],
                    foreground = colors[0],
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.ThermalSensor(
                    tag_sensor='Package id 0',
                    format = '  {temp:.0f}{unit} ',
                    foreground = colors[0],
                    background = colors[5],
                    threshold=70.0,
                    mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(terminal + ' -e btop')},
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.Memory(
                    foreground = colors[0],
                    background = colors[8],
                    measure_mem='G',
                    format = '{MemUsed:.0f}{mm}/{MemTotal:.0f}{mm} ',
                    fmt = '  {}',
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.Volume(
                    foreground = colors[0],
                    background = colors[7],
                    fmt = '  {} ',
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.KeyboardLayout(
                    foreground = colors[0],
                    background = colors[4],
                    fmt = '  {} ',
                    decorations=[
                            BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.Wlan(
                    interface='wlan0',
                    format='  {essid} ',
                    disconnected_message='',
                    foreground = colors[0],
                    background = colors[3],
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                # widget.Spacer(length = 8),
                # widget.Battery(
                #     format='  {percent:.0f}% ',
                #     foreground = colors[0],
                #     background = colors[7],
                #     decorations=[
                #         BorderDecoration(
                #             colour=colors[0],
                #             border_width=[3, 3, 3, 3],
                #         )
                #     ],
                # ),
                widget.Spacer(length = 8),
                widget.Clock(
                    foreground = colors[0],
                    background = colors[8],
                    format = "  %d-%m-%y  %H:%M ",
                    decorations=[
                        BorderDecoration(
                            colour = colors[0],
                            border_width = [3, 3, 3, 3],
                        )
                    ],
                ),
                widget.Spacer(length = 8),
                widget.Systray(padding = 3),
                widget.Spacer(length = 8),
            ],
            30,
            # border_width=[2, 0, 2, 0],  # Draw top and bottom borders
            # border_color=["ff00ff", "000000", "ff00ff", "000000"]  # Borders are magenta
        ),
        # You can uncomment this variable if you see that on X11 floating resize/moving is laggy
        # By default we handle these events delayed to already improve performance, however your system might still be struggling
        # This variable is set to None (no cap) by default, but you can set it to 60 to indicate that you limit it to 60 events per second
        # x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

# xcursor theme (string or None) and size (integer) for Wayland backend
wl_xcursor_theme = None
wl_xcursor_size = 24

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])


# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
