
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
import re
import socket
import subprocess
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule, ScratchPad, DropDown 
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer, LaunchBar

from enum import Enum

home = os.path.expanduser('~')

class KeyboardKey(Enum):
    SUPER = "mod4"
    ALT = "mod1"
    CONTROL = "control"
    SHIFT = "shift"
    ESCAPE = "Escape"
    RETURN = "Return"
    ENTER = "KP_Enter"
    PRINT = "Print"
    SPACE = "space"
    LEFT = "Left"
    RIGHT = "Right"
    UP = "Up"
    DOWN = "Down"

class GroupLayout(Enum):
    MONADTALL = "monadtall"
    MONADWIDE = "monadwide"
    BSP = "bsp"
    MAX = "max"
    MATRIX = "matrix"
    FLOATING = "floating"
    RATIO_TILE = "ratiotile"

class CustomFont(Enum):
    TEXT = "Fira Sans"
    TEXT_BOLD = "Fira Sans Bold"
    ICON = "FontAwesome"
    MONO = "PragmataPro"

class CustomApp(Enum):
    BROWSER = "firefox"
    TERMINAL = "kitty"
    FILE_MANAGER = "thunar"
    MUSIC = "spotify"
    PASS_MANAGER = "enpass"
    MINI_CALENDAR = "gsimplecal"

class CustomDropDown(Enum):
    TERMINAL = "terminal"
    PASS_MANAGER = "pass_manager"
    TERMINAL_STICK = "terminal_stick"
    PASS_MANAGER_STICK = "pass_manager_stick"

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

keys = [

# FUNCTION KEYS

# SUPER + FUNCTION KEYS

    Key([KeyboardKey.SUPER.value], "a", lazy.spawn("xfce4-appfinder")),
    Key([KeyboardKey.SUPER.value], "f", lazy.window.toggle_fullscreen()),
    Key([KeyboardKey.SUPER.value], "q", lazy.window.kill()),
    Key([KeyboardKey.SUPER.value], "d", lazy.spawn(f"dmenu_run -i -fn '{CustomFont.TEXT.value}' -h 30 -nb '#222222' -sb '#3366cc' -shf '#000022' -shb '#3366cc' -nhf '#99ccff' -nhb '#222222'")),
    Key([KeyboardKey.SUPER.value], "f", lazy.spawn(CustomApp.FILE_MANAGER.value)),
    Key([KeyboardKey.SUPER.value], "b", lazy.spawn(CustomApp.BROWSER.value)),
    Key([KeyboardKey.SUPER.value], KeyboardKey.ESCAPE.value, lazy.spawn('xkill')),
    Key([KeyboardKey.SUPER.value], KeyboardKey.RETURN.value, lazy.spawn(CustomApp.TERMINAL.value)),
    Key([KeyboardKey.SUPER.value], KeyboardKey.ENTER.value, lazy.spawn(CustomApp.TERMINAL.value)), 
    Key([KeyboardKey.SUPER.value], "s", lazy.spawn('xfce4-settings-manager')),
    Key([KeyboardKey.SUPER.value], "u", lazy.spawn("pamac-manager")),
    Key([KeyboardKey.SUPER.value], "m", lazy.spawn(CustomApp.MUSIC.value)),
 
    # Key([KeyboardKey.SUPER.value], "r", lazy.spawn('rofi-theme-selector')),
    #Key([mod], "F11", lazy.spawn('rofi -show run -fullscreen')),
    #Key([mod], "F12", lazy.spawn('rofi -show run')),
    # Key([mod], "c", lazy.spawn('conky-toggle')),

# SUPER + SHIFT KEYS

  
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], "r", lazy.restart()),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], "x", lazy.shutdown()),

# CONTROL + ALT KEYS

    # Key(["mod1", "control"], "Next", lazy.spawn('conky-rotate -n')),
    # Key(["mod1", "control"], "Prior", lazy.spawn('conky-rotate -p')),
    # Key([KeyboardKey.ALT.value, KeyboardKey.CONTROL.value], "p", lazy.spawn(f"dmenu_run -i -fn '{CustomFont.TEXT.value}' -h 30 -nb '#222222' -sb '#3366cc' -shf '#000022' -shb '#3366cc' -nhf '#99ccff' -nhb '#222222' -c -l 10")),
    Key(
        [KeyboardKey.ALT.value, KeyboardKey.CONTROL.value], "d", 
        lazy.spawn(f"dmenu_run -i -fn '{CustomFont.TEXT.value}' -h 30 -nb '#222222' -sb '#3366cc' -shf '#000022' -shb '#3366cc' -nhf '#99ccff' -nhb '#222222' -c -l 10")
    ),
    Key(
        [KeyboardKey.ALT.value, KeyboardKey.CONTROL.value], "t", 
        lazy.group["scratchpad"].dropdown_toggle(CustomDropDown.TERMINAL.value)
    ),
    Key(
        [KeyboardKey.ALT.value, KeyboardKey.CONTROL.value], "p", 
        lazy.group["scratchpad"].dropdown_toggle(CustomDropDown.PASS_MANAGER.value)
    ),
    Key(
        [KeyboardKey.ALT.value, KeyboardKey.CONTROL.value, KeyboardKey.SHIFT.value], "t", 
        lazy.group["scratchpad"].dropdown_toggle(CustomDropDown.TERMINAL_STICK.value)
    ),
    Key(
        [KeyboardKey.ALT.value, KeyboardKey.CONTROL.value, KeyboardKey.SHIFT.value], "p", 
        lazy.group["scratchpad"].dropdown_toggle(CustomDropDown.PASS_MANAGER_STICK.value)
    ),

# CONTROL + SHIFT KEYS

    Key([KeyboardKey.CONTROL.value, KeyboardKey.SHIFT.value], KeyboardKey.ESCAPE.value, lazy.spawn('xfce4-taskmanager')),

# SCREENSHOTS

    Key([KeyboardKey.CONTROL.value], KeyboardKey.PRINT.value, lazy.spawn('xfce4-screenshooter')),
    # Key([KeyboardKey.CONTROL.value, KeyboardKey.SHIFT.value], KeyboardKey.PRINT.value, lazy.spawn('gnome-screenshot -i')),

# MULTIMEDIA KEYS

# INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),

# INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),

    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),

# QTILE LAYOUT KEYS
    Key([KeyboardKey.SUPER.value], "n", lazy.layout.normalize()),
    Key([KeyboardKey.SUPER.value], KeyboardKey.SPACE.value, lazy.next_layout()),

# CHANGE FOCUS

    Key([KeyboardKey.SUPER.value], KeyboardKey.LEFT.value, lazy.screen.prev_group()),
    Key([KeyboardKey.SUPER.value], KeyboardKey.RIGHT.value, lazy.screen.next_group()),
    Key([KeyboardKey.SUPER.value], "k", lazy.layout.up()),
    Key([KeyboardKey.SUPER.value], "j", lazy.layout.down()),
    Key([KeyboardKey.SUPER.value], "h", lazy.layout.left()),
    Key([KeyboardKey.SUPER.value], "l", lazy.layout.right()),


# RESIZE UP, DOWN, LEFT, RIGHT
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], "l",
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], KeyboardKey.RIGHT.value,
        lazy.layout.grow_right(),
        lazy.layout.grow(),
        lazy.layout.increase_ratio(),
        lazy.layout.delete(),
        ),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], "h",
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], KeyboardKey.LEFT.value,
        lazy.layout.grow_left(),
        lazy.layout.shrink(),
        lazy.layout.decrease_ratio(),
        lazy.layout.add(),
        ),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], "k",
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], KeyboardKey.UP.value,
        lazy.layout.grow_up(),
        lazy.layout.grow(),
        lazy.layout.decrease_nmaster(),
        ),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], "j",
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),
    Key([KeyboardKey.SUPER.value, KeyboardKey.CONTROL.value], KeyboardKey.DOWN.value,
        lazy.layout.grow_down(),
        lazy.layout.shrink(),
        lazy.layout.increase_nmaster(),
        ),


# FLIP LAYOUT FOR MONADTALL/MONADWIDE
    Key([KeyboardKey.SUPER.value, KeyboardKey.SHIFT.value], "f", lazy.layout.flip()),

# FLIP LAYOUT FOR BSP
    Key([KeyboardKey.SUPER.value, KeyboardKey.ALT.value], "k", lazy.layout.flip_up()),
    Key([KeyboardKey.SUPER.value, KeyboardKey.ALT.value], "j", lazy.layout.flip_down()),
    Key([KeyboardKey.SUPER.value, KeyboardKey.ALT.value], "l", lazy.layout.flip_right()),
    Key([KeyboardKey.SUPER.value, KeyboardKey.ALT.value], "h", lazy.layout.flip_left()),

# MOVE WINDOWS UP OR DOWN BSP LAYOUT
    Key([KeyboardKey.SUPER.value, KeyboardKey.SHIFT.value], "k", lazy.layout.shuffle_up()),
    Key([KeyboardKey.SUPER.value, KeyboardKey.SHIFT.value], "j", lazy.layout.shuffle_down()),
    Key([KeyboardKey.SUPER.value, KeyboardKey.SHIFT.value], "h", lazy.layout.shuffle_left()),
    Key([KeyboardKey.SUPER.value, KeyboardKey.SHIFT.value], "l", lazy.layout.shuffle_right()),

# TOGGLE FLOATING LAYOUT
    Key([KeyboardKey.SUPER.value, KeyboardKey.SHIFT.value], KeyboardKey.SPACE.value, lazy.window.toggle_floating()),]

# GROUPS

groups = [
    ScratchPad(
        name ="scratchpad",
        dropdowns = [
            DropDown(
                name = CustomDropDown.TERMINAL.value, 
                cmd = CustomApp.TERMINAL.value,
                opacity = 0.9,
                on_focus_lost_hide = True
            ),
            DropDown(
                name = CustomDropDown.PASS_MANAGER.value, 
                cmd = CustomApp.PASS_MANAGER.value,
                opacity = 0.95,
                on_focus_lost_hide = True
            ),
            DropDown(
                name = CustomDropDown.TERMINAL_STICK.value, 
                cmd = CustomApp.TERMINAL.value,
                opacity = 0.9,
                on_focus_lost_hide = False
            ),
            DropDown(
                name = CustomDropDown.PASS_MANAGER_STICK.value, 
                cmd = CustomApp.PASS_MANAGER.value,
                opacity = 0.9,
                on_focus_lost_hide = False
            )
        ]
    ),
    Group(
        name = "1",
        label = "Start-I",
        layout = GroupLayout.FLOATING.value
    ),
    Group(
        name = "2",
        label = "System",
        layout = GroupLayout.BSP.value,
        spawn = CustomApp.TERMINAL.value
    ),
    Group(
        name = "3",
        label = "Internet-III",
        layout = GroupLayout.MONADTALL.value,
        spawn = CustomApp.BROWSER.value
    ),
    Group(
        name = "4",
        label = "Coding",
        layout = GroupLayout.BSP.value
    ),
    Group(
        name = "5",
        label = "Gaming-V",
        layout = GroupLayout.MAX.value
    ),
    Group(
        name = "6",
        label = "Media",
        layout = GroupLayout.FLOATING.value
    ),
    Group(
        name = "7",
        label = "Office-VII",
        layout = GroupLayout.RATIO_TILE.value,
        spawn = CustomApp.FILE_MANAGER.value
    ),
    Group(
        name = "8",
        label = "Other",
        layout = GroupLayout.FLOATING.value
    )
]

# We can also use FontAwesome icons
# group_labels = ["", "", "", "", "", "", "", "", "", "",]

for i in groups[1:]:
    keys.extend([

#CHANGE WORKSPACES
        Key([KeyboardKey.SUPER.value], i.name, lazy.group[i.name].toscreen()),


# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND STAY ON WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),
# MOVE WINDOW TO SELECTED WORKSPACE 1-10 AND FOLLOW MOVED WINDOW TO WORKSPACE
        Key([KeyboardKey.SUPER.value, KeyboardKey.SHIFT.value], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

# LAYOUT

default_layout_config = dict(
        margin = 6,
        border_width = 3,
        border_focus = "#5e81ac",
        border_normal = "#4c566a"
)

layouts = [
    layout.MonadTall(single_border_width = 0, ratio = 0.6, single_margin = 0, **default_layout_config),
    layout.MonadWide(**default_layout_config),
    layout.Matrix(**default_layout_config),
    layout.Bsp(**default_layout_config),
    layout.Floating(**default_layout_config),
    layout.RatioTile(**default_layout_config),
    layout.Max(margin = 0, border_width = 0)
]

# COLORS FOR THE BAR

def init_colors():
    return [["#222222", "#222222"], # color 0
            ["#222222", "#222222"], # color 1 (bar color)
            ["#aaaaaa", "#aaaaaa"], # color 2
            ["#fba922", "#fba922"], # color 3 (yellow)
            ["#3366cc", "#3366cc"], # color 4 (blue)
            ["#f3f4f5", "#f3f4f5"], # color 5
            ["#cd1f3f", "#cd1f3f"], # color 6
            ["#62FF00", "#62FF00"], # color 7
            ["#6790eb", "#6790eb"], # color 8 (dark blue)
            ["#ffffff", "#ffffff"]] # color 9


colors = init_colors()


# WIDGETS FOR THE BAR

widget_defaults = dict(
    font = CustomFont.TEXT.value,
    fontsize = 16,
    background = colors[1]
)

def open_calendar(qtile):
    qtile.cmd_spawn(CustomApp.MINI_CALENDAR.value)

def close_calendar(qtile):
    qtile.cmd_spawn(f"killall -q {CustomApp.MINI_CALENDAR.value}")

def open_taskmanager(qtile):
    qtile.cmd_spawn("xfce4-taskmanager")

def open_htop(qtile):
    qtile.cmd_spawn(f"{CustomApp.TERMINAL.value} -e htop")

def init_widgets_list():
    prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())
    widgets_list = [
               widget.Spacer(length = 8, background = colors[1]),
               widget.LaunchBar(
                    progs = [("", "xfce4-appfinder", "Launch apps")], 
                    background = colors[1],
                    padding = 0
               ),
               widget.GroupBox(
                        font = CustomFont.TEXT.value,
                        fontsize = 16,
                        margin_y = 4,
                        margin_x = 0,
                        padding_y = 0,
                        padding_x = 6,
                        borderwidth = 0,
                        disable_drag = True,
                        active = colors[9],
                        inactive = colors[2],
                        rounded = False,
                        highlight_method = "line",
                        highlight_color = colors[4],
                        this_current_screen_border = colors[8],
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.CurrentLayout(
                        font = CustomFont.TEXT_BOLD.value,
                        fontsize = 14,
                        foreground = colors[5],
                        background = colors[1]
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.WindowName(
                        font = CustomFont.TEXT.value,
                        fontsize = 14,
                        foreground = colors[5],
                        background = colors[1],
                        ),
                widget.Net(
                         font = CustomFont.MONO.value,
                         fontsize = 14,
                         interface = "eno1",
                         foreground = colors[2],
                         background = colors[1],
                         padding = 0,
                         ),
                widget.Sep(
                         linewidth = 1,
                         padding = 10,
                         foreground = colors[2],
                         background = colors[1]
                         ),
               # widget.NetGraph(
               #          font="Noto Sans",
               #          fontsize=12,
               #          bandwidth="down",
               #          interface="auto",
               #          fill_color = colors[8],
               #          foreground=colors[2],
               #          background=colors[1],
               #          graph_color = colors[8],
               #          border_color = colors[2],
               #          padding = 0,
               #          border_width = 1,
               #          line_width = 1,
               #          ),
               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # # do not activate in Virtualbox - will break qtile
               # widget.ThermalSensor(
               #          foreground = colors[5],
               #          foreground_alert = colors[6],
               #          background = colors[1],
               #          metric = True,
               #          padding = 3,
               #          threshold = 80
               #          ),

               # widget.Sep(
               #          linewidth = 1,
               #          padding = 10,
               #          foreground = colors[2],
               #          background = colors[1]
               #          ),
               # widget.Battery(
               #          font="Noto Sans",
               #          update_interval = 10,
               #          fontsize = 12,
               #          foreground = colors[5],
               #          background = colors[1],
	           #          ),
               widget.TextBox(
                        font = CustomFont.ICON.value,
                        text = "  ",
                        foreground = colors[5],
                        background = colors[1],
                        padding = 0,
                        fontsize = 18
                        ),
               widget.CPUGraph(
                        border_color = colors[2],
                        fill_color = colors[8],
                        graph_color = colors[8],
                        background = colors[1],
                        border_width = 1,
                        line_width = 1,
                        core = "all",
                        type = "box",
                        mouse_callbacks = dict(Button1 = open_htop)
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.TextBox(
                        font = CustomFont.ICON.value,
                        text = "  ",
                        foreground = colors[4],
                        background = colors[1],
                        padding = 0,
                        fontsize = 18
                        ),
               widget.Memory(
                        font = CustomFont.MONO.value,
                        format = '{MemUsed}M/{MemTotal}M',
                        update_interval = 10,
                        fontsize = 16,
                        foreground = colors[5],
                        background = colors[1],
                        mouse_callbacks = dict(Button1 = open_taskmanager)
                       ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.TextBox(
                        font = CustomFont.ICON.value,
                        text ="  ",
                        foreground = colors[3],
                        background = colors[1],
                        padding = 0,
                        fontsize = 18
                        ),
               widget.Clock(
                        font = CustomFont.MONO.value,
                        foreground = colors[5],
                        background = colors[1],
                        fontsize = 16,
                        format = "%Y-%m-%d %H:%M",
                        mouse_callbacks = {'Button1': open_calendar, 'Button3': close_calendar}
                        ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               # widget.Volume(),
               widget.LaunchBar(
                    progs = [
                        ("  ", "xfce4-settings-manager", "Settings"),
                        ('  ', 'qshell:self.qtile.cmd_shutdown()', 'Logout from qtile'),
                        ("  ", "systemctl suspend", "Suspend"),
                        ("  ", "systemctl poweroff", "Power Off")
                    ], 
                    background = colors[1],
                    padding = 0
               ),
               widget.Sep(
                        linewidth = 1,
                        padding = 10,
                        foreground = colors[2],
                        background = colors[1]
                        ),
               widget.Systray(
                        background = colors[1],
                        icon_size = 27,
                        padding = 8
                        ),
               widget.Spacer(length = 8, background = colors[1])
              ]
    return widgets_list

widgets_list = init_widgets_list()


def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_widgets_screen2():
    widgets_screen2 = init_widgets_list()
    return widgets_screen2

widgets_screen1 = init_widgets_screen1()
widgets_screen2 = init_widgets_screen2()


def init_screens():
    return [
            Screen(
                wallpaper = "/home/daniel/Pictures/Wallpapers/manjaro.png",
                wallpaper_mode = 'fill',
                top = bar.Bar(widgets=init_widgets_screen1(), size=30)
            ),
            Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=30))
            ]
screens = init_screens()


# MOUSE CONFIGURATION
mouse = [
     Drag([KeyboardKey.SUPER.value], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
     Drag([KeyboardKey.SUPER.value], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
     Click([KeyboardKey.SUPER.value], "Button2", lazy.window.toggle_floating())
]

dgroups_key_binder = None
dgroups_app_rules = []

# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME
# BEGIN

# @hook.subscribe.client_new
# def assign_app_group(client):
#     d = {}
#     #########################################################
#     ################ assgin apps to groups ##################
#     #########################################################
#     d["1"] = ["Navigator", "Firefox", "Vivaldi-stable", "Vivaldi-snapshot", "Chromium", "Google-chrome", "Brave", "Brave-browser",
#               "navigator", "firefox", "vivaldi-stable", "vivaldi-snapshot", "chromium", "google-chrome", "brave", "brave-browser", ]
#     d["2"] = [ "Atom", "Subl3", "Geany", "Brackets", "Code-oss", "Code", "TelegramDesktop", "Discord",
#                "atom", "subl3", "geany", "brackets", "code-oss", "code", "telegramDesktop", "discord", ]
#     d["3"] = ["Inkscape", "Nomacs", "Ristretto", "Nitrogen", "Feh",
#               "inkscape", "nomacs", "ristretto", "nitrogen", "feh", ]
#     d["4"] = ["Gimp", "gimp" ]
#     d["5"] = ["Meld", "meld", "org.gnome.meld" "org.gnome.Meld" ]
#     d["6"] = ["Vlc","vlc", "Mpv", "mpv" ]
#     d["7"] = ["VirtualBox Manager", "VirtualBox Machine", "Vmplayer",
#               "virtualbox manager", "virtualbox machine", "vmplayer", ]
#     d["8"] = ["Thunar", "Nemo", "Caja", "Nautilus", "org.gnome.Nautilus", "Pcmanfm", "Pcmanfm-qt",
#               "thunar", "nemo", "caja", "nautilus", "org.gnome.nautilus", "pcmanfm", "pcmanfm-qt", ]
#     d["9"] = ["Evolution", "Geary", "Mail", "Thunderbird",
#               "evolution", "geary", "mail", "thunderbird" ]
#     d["0"] = ["Spotify", "Pragha", "Clementine", "Deadbeef", "Audacious",
#               "spotify", "pragha", "clementine", "deadbeef", "audacious" ]
#     ##########################################################
#     wm_class = client.window.get_wm_class()[0]
#
#     for i in range(len(d)):
#         if wm_class in list(d.values())[i]:
#             group = list(d.keys())[i]
#             client.togroup(group)
#             client.group.cmd_toscreen()

# END
# ASSIGN APPLICATIONS TO A SPECIFIC GROUPNAME



main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autorun.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for() or window.window.get_wm_type() in floating_types):
        window.floating = True

@hook.subscribe.client_managed
def set_windows_positions(window):
    window_class = window.window.get_wm_class()[0]
    if (window_class == 'xfce4-appfinder'):
        window.tweak_float(x=0, y=30, dx=0, dy=0, w=500, h=500, dw=0, dh=0)
    if (window_class == 'gsimplecal'):
        window.tweak_float(x=2050, y=30, dx=0, dy=0, w=0, h=0, dw=0, dh=0)

floating_types = ["notification", "toolbar", "splash", "dialog"]

follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
  float_rules = [
    {'wmclass': 'Arcolinux-welcome-app.py'},
    {'wmclass': 'Arcolinux-tweak-tool.py'},
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},
    {'wmclass': 'makebranch'},
    {'wmclass': 'maketag'},
    {'wmclass': 'Arandr'},
    {'wmclass': 'feh'},
    {'wmclass': 'Galculator'},
    {'wmclass': 'arcolinux-logout'},
    {'wmclass': 'xfce4-terminal'},
    {'wmclass': 'xfce4-appfinder'},
    {'wmclass': 'uget-gtk'},
    {'wmclass': 'Uget-gtk'},
    {'wmclass': 'krunner'},
    {'wmclass': 'gsimplecal'},
    {'wname': 'uGet'},
    {'wname': 'branchdialog'},
    {'wname': 'Open File'},
    {'wname': 'pinentry'},
    {'wmclass': 'ssh-askpass'},
  ],  
  fullscreen_border_width = 0, 
  border_width = 0
)

auto_fullscreen = True

focus_on_window_activation = "focus" # or smart

wmname = "LG3D"
