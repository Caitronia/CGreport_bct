# -*- coding: utf-8 -*-
# Windows-safe terminal output (suppresses codec errors on any stray char)
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
"""
# ======================================================#
|        P I N G   P O N G                                            |
|        Full Interactive Arcade Game                                  |
# ======================================================#

Run:
    pip install pygame
    python pong_ultra.py

Controls:
    Player 1  : W / S
    Player 2  : UP / DOWN arrows
    ESC       : Pause
    ENTER     : Confirm
    Mouse     : Full menu interaction
    F         : Toggle FPS
    T         : Cycle themes in-game
"""

import pygame
import sys
import math
import random
import json
import os
import time
import struct
import array
from typing import List, Dict, Tuple, Optional, Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from copy import deepcopy

# ======================================================
#  VIRTUAL CANVAS  (everything renders here, then scales)
# ======================================================
VW, VH = 1280, 720
FPS_CAP = 60
SETTINGS_FILE = "pong_ultra_settings.json"
ACHIEVEMENTS_FILE = "pong_ultra_achievements.json"

# ======================================================
#  COLOR PALETTES
# ======================================================
PALETTES = {
    "NEON": {
        "bg":         (4,    4,   20),
        "bg2":        (8,    6,   35),
        "grid":       (18,  15,   55),
        "p1":         (0,   210,  255),
        "p2":         (255,  60,  200),
        "ball":       (255, 240,   60),
        "ball_fire":  (255,  80,    0),
        "ball_heavy": (160, 100,  255),
        "ball_light": (140, 255,  180),
        "center":     (50,   50,  130),
        "ui_bg":      (8,    8,   28),
        "ui_border":  (60,   60,  160),
        "ui_hi":      (0,   210,  255),
        "text":       (220, 220,  255),
        "text_dim":   (100, 100,  160),
        "gold":       (255, 210,   30),
        "green":      (50,  255,  120),
        "red":        (255,  60,   60),
        "white":      (255, 255,  255),
        "gray":       (120, 120,  150),
        "dark":       (20,  20,   50),
        "pu_speed":   (255, 200,    0),
        "pu_slow":    (0,   180,  255),
        "pu_big":     (0,   255,  100),
        "pu_multi":   (255, 100,  255),
        "pu_shield":  (100, 200,  255),
        "pu_invis":   (200, 200,  220),
        "pu_rev":     (255,  80,   80),
        "pu_magnet":  (255, 160,   80),
    },
    "CLASSIC": {
        "bg":         (0,     0,    0),
        "bg2":        (0,     0,    0),
        "grid":       (0,     0,    0),
        "p1":         (255, 255,  255),
        "p2":         (255, 255,  255),
        "ball":       (255, 255,  255),
        "ball_fire":  (255, 255,  255),
        "ball_heavy": (200, 200,  200),
        "ball_light": (255, 255,  255),
        "center":     (80,   80,   80),
        "ui_bg":      (0,     0,    0),
        "ui_border":  (180, 180,  180),
        "ui_hi":      (255, 255,  255),
        "text":       (255, 255,  255),
        "text_dim":   (150, 150,  150),
        "gold":       (255, 230,   50),
        "green":      (150, 255,  150),
        "red":        (255, 100,  100),
        "white":      (255, 255,  255),
        "gray":       (150, 150,  150),
        "dark":       (30,   30,   30),
        "pu_speed":   (255, 255,    0),
        "pu_slow":    (200, 200,  255),
        "pu_big":     (200, 255,  200),
        "pu_multi":   (255, 200,  255),
        "pu_shield":  (200, 230,  255),
        "pu_invis":   (180, 180,  180),
        "pu_rev":     (255, 180,  180),
        "pu_magnet":  (255, 220,  180),
    },
    "SYNTHWAVE": {
        "bg":         (12,   5,   28),
        "bg2":        (20,   5,   40),
        "grid":       (60,  10,   80),
        "p1":         (255, 100,  200),
        "p2":         (100, 255,  200),
        "ball":       (255, 255,  100),
        "ball_fire":  (255,  50,  100),
        "ball_heavy": (200,  50,  255),
        "ball_light": (100, 255,  255),
        "center":     (100,  20,  120),
        "ui_bg":      (15,   5,   30),
        "ui_border":  (180,  30,  200),
        "ui_hi":      (255, 100,  200),
        "text":       (255, 200,  255),
        "text_dim":   (150,  80,  180),
        "gold":       (255, 230,   60),
        "green":      (100, 255,  180),
        "red":        (255,  60,  120),
        "white":      (255, 230,  255),
        "gray":       (150,  80,  180),
        "dark":       (30,   8,   50),
        "pu_speed":   (255, 200,   50),
        "pu_slow":    (80,  200,  255),
        "pu_big":     (80,  255,  160),
        "pu_multi":   (255,  80,  255),
        "pu_shield":  (80,  160,  255),
        "pu_invis":   (220, 180,  255),
        "pu_rev":     (255,  60,  140),
        "pu_magnet":  (255, 160,   80),
    }
}

# Active palette (mutable reference)
P = dict(PALETTES["NEON"])

def set_theme(name: str):
    global P
    pal = PALETTES.get(name, PALETTES["NEON"])
    P.clear()
    P.update(pal)

# ======================================================
#  ENUMS
# ======================================================
class GameMode(Enum):
    SINGLE    = "SINGLE PLAYER"
    TWO_PLAY  = "TWO PLAYERS"
    TRAINING  = "TRAINING"

class Difficulty(Enum):
    EASY   = "EASY"
    MEDIUM = "MEDIUM"
    HARD   = "HARD"
    INSANE = "INSANE"

class PowerupType(Enum):
    SPEED   = "SPEED BOOST"
    SLOW    = "SLOW MOTION"
    BIG     = "BIG PADDLE"
    MULTI   = "MULTI BALL"
    SHIELD  = "SHIELD"
    INVIS   = "INVISIBLE"
    REVERSE = "REVERSE"
    MAGNET  = "MAGNET"

class BallType(Enum):
    NORMAL   = "NORMAL"
    HEAVY    = "HEAVY"
    LIGHT    = "LIGHT"
    FIREBALL = "FIREBALL"

class Scene(Enum):
    MAIN_MENU   = auto()
    GAME        = auto()
    PAUSED      = auto()
    SETTINGS    = auto()
    HOW_TO_PLAY = auto()
    MATCH_END   = auto()
    ACHIEVEMENTS = auto()

# ======================================================
#  SETTINGS
# ======================================================
@dataclass
class Settings:
    difficulty: str      = "MEDIUM"
    sound: bool          = True
    volume: float        = 0.65
    fullscreen: bool     = False
    quality: str         = "HIGH"
    theme: str           = "NEON"
    powerups: bool       = True
    match_pts: int       = 7
    win_by_2: bool       = True
    show_fps: bool       = False
    shake: bool          = True
    crt: bool            = False
    ball_type: str       = "NORMAL"
    combo: bool          = True
    arcade_score: bool   = True
    training_speed: float = 1.0
    p1_up: int           = pygame.K_w
    p1_dn: int           = pygame.K_s
    p2_up: int           = pygame.K_UP
    p2_dn: int           = pygame.K_DOWN

    def save(self):
        try:
            with open(SETTINGS_FILE, "w") as f:
                json.dump(self.__dict__, f, indent=2)
        except Exception as e:
            print(f"[Settings] Save failed: {e}")

    @classmethod
    def load(cls) -> "Settings":
        s = cls()
        try:
            if os.path.exists(SETTINGS_FILE):
                with open(SETTINGS_FILE) as f:
                    d = json.load(f)
                for k, v in d.items():
                    if hasattr(s, k):
                        setattr(s, k, v)
        except Exception as e:
            print(f"[Settings] Load failed: {e}")
        return s

# ======================================================
#  AUDIO (synthesized, no files needed)
# ======================================================
class Audio:
    def __init__(self, settings: Settings):
        self.s = settings
        self.ok = False
        self._cache: Dict[str, Optional[pygame.mixer.Sound]] = {}
        try:
            pygame.mixer.pre_init(44100, -16, 2, 512)
            pygame.mixer.init()
            self.ok = True
            self._synth_all()
        except Exception as e:
            print(f"[Audio] Init failed: {e}")

    def _make_sound(self, freq: float, dur_ms: int,
                    wave: str = "sine", vol: float = 0.5,
                    decay: float = 0.05) -> Optional[pygame.mixer.Sound]:
        try:
            rate = 44100
            n = int(rate * dur_ms / 1000)
            buf = bytearray()
            for i in range(n):
                t = i / rate
                if wave == "sine":
                    v = math.sin(2 * math.pi * freq * t)
                elif wave == "square":
                    v = 1.0 if math.sin(2 * math.pi * freq * t) > 0 else -1.0
                elif wave == "tri":
                    v = 2 * abs(2 * (t * freq - math.floor(t * freq + 0.5))) - 1
                elif wave == "noise":
                    v = random.uniform(-1, 1)
                else:
                    v = math.sin(2 * math.pi * freq * t)
                env = min(1.0, i / max(1, rate * 0.005))
                env *= max(0.0, 1.0 - i / max(1, rate * decay))
                sample = int(v * vol * env * 32767)
                sample = max(-32768, min(32767, sample))
                b = struct.pack("<hh", sample, sample)
                buf.extend(b)
            return pygame.mixer.Sound(buffer=bytes(buf))
        except Exception as e:
            print(f"[Audio] Synth error: {e}")
            return None

    def _synth_all(self):
        self._cache = {
            "paddle":    self._make_sound(440,  55,  "sine",   0.55, 0.08),
            "wall":      self._make_sound(280,  40,  "sine",   0.40, 0.06),
            "score":     self._make_sound(200,  500, "sine",   0.70, 0.5),
            "powerup":   self._make_sound(660,  220, "tri",    0.50, 0.25),
            "menu_move": self._make_sound(380,  45,  "tri",    0.30, 0.06),
            "menu_sel":  self._make_sound(520,  90,  "tri",    0.40, 0.10),
            "combo":     self._make_sound(880,  80,  "sine",   0.45, 0.10),
            "win":       self._make_sound(660,  900, "sine",   0.70, 1.0),
            "lose":      self._make_sound(220,  700, "tri",    0.60, 0.8),
            "pu_expire": self._make_sound(200,  150, "square", 0.30, 0.18),
        }

    def play(self, name: str):
        if not self.ok or not self.s.sound:
            return
        snd = self._cache.get(name)
        if snd:
            try:
                snd.set_volume(self.s.volume)
                snd.play()
            except Exception:
                pass

# ======================================================
#  FONT MANAGER
# ======================================================
class Fonts:
    _cache: Dict[Tuple, pygame.font.Font] = {}

    @classmethod
    def get(cls, size: int, bold: bool = False) -> pygame.font.Font:
        key = (size, bold)
        if key not in cls._cache:
            try:
                cls._cache[key] = pygame.font.SysFont(
                    "consolas,courier new,monospace", size, bold=bold)
            except Exception:
                cls._cache[key] = pygame.font.Font(None, size)
        return cls._cache[key]

def render_text(surf, text, size, color, cx, cy, bold=False, anchor="center"):
    f = Fonts.get(size, bold)
    txt = f.render(str(text), True, color)
    r = txt.get_rect()
    if anchor == "center":   r.center = (cx, cy)
    elif anchor == "midleft": r.midleft = (cx, cy)
    elif anchor == "midright": r.midright = (cx, cy)
    elif anchor == "topleft": r.topleft = (cx, cy)
    elif anchor == "midbottom": r.midbottom = (cx, cy)
    surf.blit(txt, r)
    return r

def render_glow(surf, text, size, color, cx, cy, bold=True, layers=3):
    """Render text with a multi-layer glow bloom effect."""
    f = Fonts.get(size, bold)
    # Glow layers (larger, dimmer, additive blended)
    for i in range(layers, 0, -1):
        gcol = tuple(min(255, int(c * (0.3 / i))) for c in color)
        g = f.render(str(text), True, gcol)
        gs = pygame.transform.scale(g,
            (g.get_width() + i*6, g.get_height() + i*4))
        gr = gs.get_rect(center=(cx, cy))
        surf.blit(gs, gr, special_flags=pygame.BLEND_ADD)
    # Main text
    txt = f.render(str(text), True, color)
    r = txt.get_rect(center=(cx, cy))
    surf.blit(txt, r)
    return r

# ======================================================
#  EASING FUNCTIONS
# ======================================================
def ease_out_cubic(t: float) -> float:
    return 1 - (1 - t) ** 3

def ease_in_out(t: float) -> float:
    return t * t * (3 - 2 * t)

def lerp(a, b, t):
    return a + (b - a) * t

def lerp_color(a, b, t):
    return tuple(int(lerp(a[i], b[i], max(0, min(1, t)))) for i in range(3))

# ======================================================
#  PARTICLE SYSTEM
# ======================================================
@dataclass
class Particle:
    x: float; y: float
    vx: float; vy: float
    color: Tuple
    life: float; max_life: float
    size: float
    gravity: float = 0.0
    glow: bool = False
    shrink: bool = True

class ParticleSystem:
    def __init__(self):
        self.pool: List[Particle] = []

    def emit(self, x, y, color, n=10, speed=4.0, gravity=0.0,
             life=(0.4, 1.0), size=(2, 6), glow=False,
             direction=None, spread=math.pi * 2, shrink=True):
        for _ in range(n):
            if direction is not None:
                a = direction + random.uniform(-spread/2, spread/2)
            else:
                a = random.uniform(0, math.pi * 2)
            spd = random.uniform(speed * 0.4, speed)
            vx, vy = math.cos(a) * spd, math.sin(a) * spd
            l = random.uniform(*life)
            sz = random.uniform(*size)
            self.pool.append(Particle(x, y, vx, vy, color, l, l, sz,
                                       gravity, glow, shrink))

    def trail(self, x, y, color, size=3, life=0.18):
        self.pool.append(Particle(x, y, 0, 0, color, life, life, size,
                                   0, False, True))

    def update(self, dt):
        keep = []
        for p in self.pool:
            p.x += p.vx * dt * 60
            p.y += p.vy * dt * 60
            p.vy += p.gravity * dt * 60
            p.vx *= 0.96
            p.life -= dt
            if p.life > 0:
                keep.append(p)
        self.pool = keep

    def draw(self, surf, quality: str):
        for p in self.pool:
            a = max(0.0, p.life / p.max_life)
            sz = max(1, int(p.size * (a if p.shrink else 1.0)))
            col = tuple(int(c * a) for c in p.color[:3])
            ix, iy = int(p.x), int(p.y)
            if quality == "HIGH" and p.glow:
                for gl in range(3, 0, -1):
                    ga = int(a * 60 / gl)
                    gs = pygame.Surface((sz*gl*4+2, sz*gl*4+2), pygame.SRCALPHA)
                    pygame.draw.circle(gs, (*col, ga),
                                       (sz*gl*2+1, sz*gl*2+1), sz*gl)
                    surf.blit(gs, (ix - sz*gl*2-1, iy - sz*gl*2-1),
                              special_flags=pygame.BLEND_ADD)
            pygame.draw.circle(surf, col, (ix, iy), sz)

# ======================================================
#  SCREEN SHAKE
# ======================================================
class ShakeEffect:
    def __init__(self):
        self.mag = 0.0
        self.offset = (0, 0)

    def trigger(self, strength: float):
        self.mag = max(self.mag, strength)

    def update(self, dt):
        if self.mag > 0.5:
            self.offset = (random.uniform(-self.mag, self.mag),
                           random.uniform(-self.mag, self.mag))
            self.mag *= 0.82
        else:
            self.mag = 0
            self.offset = (0, 0)

# ======================================================
#  TRANSITION MANAGER
# ======================================================
class Transition:
    def __init__(self):
        self.alpha = 255.0
        self.dir = -1     # -1 = fade in, +1 = fade out
        self.speed = 480.0
        self.done = False
        self._cb: Optional[Callable] = None

    def fade_in(self):
        self.alpha = 255
        self.dir = -1
        self.done = False
        self._cb = None

    def fade_out(self, cb: Optional[Callable] = None):
        self.alpha = 0
        self.dir = 1
        self.done = False
        self._cb = cb

    def update(self, dt):
        if self.done:
            return
        self.alpha += self.dir * self.speed * dt
        self.alpha = max(0.0, min(255.0, self.alpha))
        if self.dir == -1 and self.alpha <= 0:
            self.done = True
        elif self.dir == 1 and self.alpha >= 255:
            self.done = True
            if self._cb:
                self._cb()

    def draw(self, surf):
        if self.alpha > 0:
            ov = pygame.Surface((VW, VH))
            ov.set_alpha(int(self.alpha))
            ov.fill((0, 0, 0))
            surf.blit(ov, (0, 0))

# ======================================================
#  ANIMATED BACKGROUND
# ======================================================
class Background:
    def __init__(self):
        self.stars = [
            {"x": random.uniform(0, VW),
             "y": random.uniform(0, VH),
             "spd": random.uniform(8, 50),
             "sz": random.uniform(0.5, 2.2),
             "b": random.uniform(0.15, 0.75)}
            for _ in range(160)
        ]
        self.t = 0.0
        # Pre-bake static grid surface
        self._grid_surf = pygame.Surface((VW, VH), pygame.SRCALPHA)
        self._build_grid()
        self._theme = ""

    def _build_grid(self):
        self._grid_surf.fill((0, 0, 0, 0))
        gs = 64
        col = (*P["grid"], 60)
        for gx in range(0, VW + gs, gs):
            pygame.draw.line(self._grid_surf, col, (gx, 0), (gx, VH))
        for gy in range(0, VH + gs, gs):
            pygame.draw.line(self._grid_surf, col, (0, gy), (VW, gy))

    def draw(self, surf, dt: float, quality: str, theme: str):
        self.t += dt
        if theme != self._theme:
            self._theme = theme
            self._build_grid()

        surf.fill(P["bg"])

        # Animated gradient horizon (NEON/SYNTHWAVE)
        if quality != "LOW" and theme != "CLASSIC":
            gh = VH // 2
            for gy in range(0, gh, 3):
                ratio = gy / gh
                c = lerp_color(P["bg2"], P["bg"], ratio)
                pygame.draw.line(surf, c, (0, VH - gy), (VW, VH - gy))

        # Grid
        if quality != "LOW" and theme != "CLASSIC":
            surf.blit(self._grid_surf, (0, 0))

        # Stars
        if quality != "LOW":
            for star in self.stars:
                star["x"] -= star["spd"] * dt
                if star["x"] < 0:
                    star["x"] = VW
                    star["y"] = random.uniform(0, VH)
                b = int(star["b"] * 200)
                col = (b, b, min(255, b + 30))
                sz = max(1, int(star["sz"]))
                pygame.draw.circle(surf, col, (int(star["x"]), int(star["y"])), sz)

    def draw_center_line(self, surf, quality: str, t: float):
        cx = VW // 2
        dash, gap = 18, 10
        y = 0
        while y < VH:
            prog = 0.55 + 0.3 * math.sin(t * 2.2 - y * 0.04)
            col = tuple(int(c * prog) for c in P["center"])
            pygame.draw.rect(surf, col, (cx - 2, y, 4, dash), border_radius=2)
            y += dash + gap

# ======================================================
#  PADDLE
# ======================================================
class Paddle:
    W = 15
    H = 100
    MAX_SPD = 540.0
    ACCEL   = 2600.0
    FRICTION = 0.80

    def __init__(self, x: float, side: int, color):
        self.x = x
        self.side = side      # 0 = left, 1 = right
        self.color = color
        self.y = VH / 2.0
        self.vy = 0.0
        self.h = self.H
        self.score = 0
        self.arcade_pts = 0
        self.combo = 0
        self.combo_t = 0.0
        self.shield = False
        self.shield_hp = 0
        self.magnet = False
        self.hit_flash = 0.0
        self.reverse = False

    def reset_size(self):
        self.h = self.H

    @property
    def rect(self):
        return pygame.Rect(self.x - self.W/2,
                           self.y - self.h/2,
                           self.W, self.h)

    def move(self, direction: float, dt: float):
        if self.reverse:
            direction = -direction
        if direction != 0:
            self.vy += direction * self.ACCEL * dt
        else:
            self.vy *= self.FRICTION ** (dt * 60)
        self.vy = max(-self.MAX_SPD, min(self.MAX_SPD, self.vy))
        self.y += self.vy * dt
        half = self.h / 2
        self.y = max(half, min(VH - half, self.y))

    def update(self, dt):
        if self.hit_flash > 0:
            self.hit_flash = max(0.0, self.hit_flash - dt)
        if self.combo_t > 0:
            self.combo_t -= dt
            if self.combo_t <= 0:
                self.combo = 0

    def draw(self, surf, quality: str):
        col = self.color
        r = self.rect

        # Glow layers
        if quality != "LOW":
            for gl in range(5, 0, -1):
                alpha = max(0, 22 - gl * 3)
                gs = pygame.Surface((r.w + gl*10, r.h + gl*8), pygame.SRCALPHA)
                gc = (*col, alpha)
                pygame.draw.rect(gs, gc, gs.get_rect(), border_radius=8)
                surf.blit(gs, (r.x - gl*5, r.y - gl*4),
                          special_flags=pygame.BLEND_ADD)

        # Hit flash blend
        draw_col = col
        if self.hit_flash > 0:
            t = min(1.0, self.hit_flash / 0.12)
            draw_col = lerp_color(col, (255, 255, 255), t * 0.7)

        # Body with rounded rect
        pygame.draw.rect(surf, draw_col, r, border_radius=7)
        # Bright edge highlight
        highlight = lerp_color(draw_col, (255, 255, 255), 0.5)
        edge_r = pygame.Rect(r.left if self.side == 1 else r.right - 3,
                             r.top, 3, r.height)
        pygame.draw.rect(surf, highlight, edge_r, border_radius=2)

        # Shield arc
        if self.shield:
            pulse = 0.7 + 0.3 * math.sin(time.time() * 6)
            scol = tuple(int(c * pulse) for c in P["pu_shield"])
            ax = r.left - 6 if self.side == 1 else r.right + 6
            pygame.draw.arc(surf, scol,
                            (ax - 16, int(self.y) - 55, 32, 110),
                            -math.pi/2, math.pi/2, 3)

        # Combo counter above/below paddle
        if self.combo >= 2:
            cmb_col = lerp_color(P["white"], P["gold"],
                                  min(1.0, self.combo / 8))
            cy_pos = int(self.y - self.h/2 - 22)
            render_glow(surf, f"x{self.combo}", 20, cmb_col,
                        int(self.x), cy_pos, bold=True, layers=2)

# ======================================================
#  BALL
# ======================================================
class Ball:
    BASE_R   = 10
    BASE_SPD = 370.0
    MAX_SPD  = 1100.0

    def __init__(self, btype: BallType = BallType.NORMAL, direction: int = 1):
        self.btype = btype
        self.r = self.BASE_R
        self._direction = direction
        self.trail: List[Tuple[float, float]] = []
        self.alive = True
        self.invisible = False
        self.invis_t = 0.0
        self.spin = 0.0
        self.attracted_to: Optional[Paddle] = None
        self._reset()
        self._apply_type()

    def _reset(self):
        self.x = float(VW / 2)
        self.y = float(VH / 2)
        angle = random.uniform(-math.pi/5, math.pi/5)
        spd = self.BASE_SPD
        self.vx = math.cos(angle) * spd * self._direction
        self.vy = math.sin(angle) * spd
        self.speed = spd
        self.trail.clear()
        self.invisible = False
        self.spin = 0.0
        self.attracted_to = None

    def _apply_type(self):
        if self.btype == BallType.HEAVY:
            self.vx *= 0.72; self.vy *= 0.72
            self.speed *= 0.72; self.r = 13
        elif self.btype == BallType.LIGHT:
            self.vx *= 1.28; self.vy *= 1.28
            self.speed *= 1.28; self.r = 8
        elif self.btype == BallType.FIREBALL:
            self.vx *= 1.12; self.vy *= 1.12
            self.speed *= 1.12

    @property
    def color(self):
        ratio = min(1.0, self.speed / (self.BASE_SPD * 2.2))
        if self.btype == BallType.HEAVY:
            return lerp_color(P["ball_heavy"], P["pu_rev"], ratio)
        if self.btype == BallType.LIGHT:
            return lerp_color(P["ball_light"], P["ball"], ratio)
        if self.btype == BallType.FIREBALL:
            return lerp_color(P["ball"], P["ball_fire"], ratio)
        return lerp_color(P["ball"], P["ball_fire"], ratio)

    def accelerate(self, factor=1.045):
        cur = math.hypot(self.vx, self.vy)
        new = min(cur * factor, self.MAX_SPD)
        if cur > 0:
            scale = new / cur
            self.vx *= scale
            self.vy *= scale
        self.speed = math.hypot(self.vx, self.vy)

    def apply_spin(self, dt):
        if abs(self.spin) > 0.05:
            self.vy += self.spin * dt * 55
            self.spin *= 0.96

    def update(self, dt: float, slow: float = 1.0) -> Optional[str]:
        eff = dt * slow
        self.apply_spin(dt)

        # Magnet attraction
        if self.attracted_to is not None:
            p = self.attracted_to
            dx = p.x - self.x
            dy = p.y - self.y
            dist = max(1, math.hypot(dx, dy))
            force = 300.0 / dist
            self.vx += (dx / dist) * force * dt
            self.vy += (dy / dist) * force * dt

        self.x += self.vx * eff
        self.y += self.vy * eff

        # Trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > 25:
            self.trail.pop(0)

        # Invisible countdown
        if self.invisible:
            self.invis_t -= dt
            if self.invis_t <= 0:
                self.invisible = False

        # Wall bounce
        if self.y - self.r <= 0:
            self.y = self.r
            self.vy = abs(self.vy)
            return "wall"
        if self.y + self.r >= VH:
            self.y = VH - self.r
            self.vy = -abs(self.vy)
            return "wall"
        return None

    def draw(self, surf, quality: str, t: float):
        if self.invisible and int(t * 9) % 2 == 0:
            return   # flicker when invisible

        col = self.color
        ix, iy = int(self.x), int(self.y)

        # Trail
        if quality != "LOW" and len(self.trail) > 1:
            for i, (tx, ty) in enumerate(self.trail):
                ratio = i / len(self.trail)
                tsz = max(1, int(self.r * ratio * 0.7))
                tc = tuple(int(c * ratio * 0.55) for c in col)
                if quality == "HIGH":
                    tsurf = pygame.Surface((tsz*4+2, tsz*4+2), pygame.SRCALPHA)
                    pygame.draw.circle(tsurf, (*tc, int(ratio * 160)),
                                       (tsz*2+1, tsz*2+1), tsz)
                    surf.blit(tsurf, (int(tx)-tsz*2-1, int(ty)-tsz*2-1),
                              special_flags=pygame.BLEND_ADD)
                else:
                    if tsz > 0:
                        pygame.draw.circle(surf, tc, (int(tx), int(ty)), tsz)

        # Glow
        if quality == "HIGH":
            for gl in range(6, 0, -1):
                ga = int(28 / gl)
                gs = pygame.Surface(
                    ((self.r + gl*6)*2+2, (self.r + gl*6)*2+2),
                    pygame.SRCALPHA)
                pygame.draw.circle(gs, (*col, ga),
                                   (self.r + gl*6+1, self.r + gl*6+1),
                                   self.r + gl*6)
                surf.blit(gs, (ix - self.r - gl*6-1, iy - self.r - gl*6-1),
                          special_flags=pygame.BLEND_ADD)
        elif quality == "MEDIUM":
            for gl in range(3, 0, -1):
                ga = int(40 / gl)
                gs = pygame.Surface(
                    ((self.r + gl*4)*2+2, (self.r + gl*4)*2+2),
                    pygame.SRCALPHA)
                pygame.draw.circle(gs, (*col, ga),
                                   (self.r + gl*4+1, self.r + gl*4+1),
                                   self.r + gl*4)
                surf.blit(gs, (ix - self.r - gl*4-1, iy - self.r - gl*4-1),
                          special_flags=pygame.BLEND_ADD)

        # Core
        pygame.draw.circle(surf, col, (ix, iy), self.r)
        # Specular highlight
        hcol = lerp_color(col, (255, 255, 255), 0.6)
        pygame.draw.circle(surf, hcol,
                           (ix - self.r//3, iy - self.r//3),
                           max(1, self.r//3))

        # Fireball sparks
        if self.btype == BallType.FIREBALL and quality != "LOW":
            for _ in range(2):
                sx = ix + random.randint(-self.r, self.r)
                sy = iy + random.randint(-self.r, self.r)
                sc = lerp_color(P["ball"], P["ball_fire"], random.random())
                pygame.draw.circle(surf, sc, (sx, sy), random.randint(1, 4))

# ======================================================
#  POWERUP ITEM (collectible on court)
# ======================================================
PU_COLORS = {
    PowerupType.SPEED:   "pu_speed",
    PowerupType.SLOW:    "pu_slow",
    PowerupType.BIG:     "pu_big",
    PowerupType.MULTI:   "pu_multi",
    PowerupType.SHIELD:  "pu_shield",
    PowerupType.INVIS:   "pu_invis",
    PowerupType.REVERSE: "pu_rev",
    PowerupType.MAGNET:  "pu_magnet",
}
PU_ICONS = {
    PowerupType.SPEED:   ">>",
    PowerupType.SLOW:    "||",
    PowerupType.BIG:     "[]",
    PowerupType.MULTI:   "##",
    PowerupType.SHIELD:  "<>",
    PowerupType.INVIS:   "~~",
    PowerupType.REVERSE: "vv",
    PowerupType.MAGNET:  "())",
}

class PowerupItem:
    def __init__(self, x: float, y: float, ptype: PowerupType):
        self.x = x
        self.y = y
        self.ptype = ptype
        self.r = 22
        self.t = 0.0
        self.alive = True

    @property
    def color(self):
        return P[PU_COLORS[self.ptype]]

    def update(self, dt):
        self.t += dt

    def draw(self, surf, quality: str):
        col = self.color
        pulse = 0.8 + 0.2 * math.sin(self.t * 4.5)
        r = int(self.r * pulse)
        ix, iy = int(self.x), int(self.y)

        # Glow ring
        if quality != "LOW":
            for gl in range(3, 0, -1):
                gs = pygame.Surface((r*gl*4+4, r*gl*4+4), pygame.SRCALPHA)
                pygame.draw.circle(gs, (*col, 25//gl),
                                   (r*gl*2+2, r*gl*2+2), r*gl)
                surf.blit(gs, (ix-r*gl*2-2, iy-r*gl*2-2),
                          special_flags=pygame.BLEND_ADD)

        # Hexagon outline
        pts = [(ix + r * math.cos(math.pi/2 + k*math.pi/3 + self.t*0.8),
                iy + r * math.sin(math.pi/2 + k*math.pi/3 + self.t*0.8))
               for k in range(6)]
        pygame.draw.polygon(surf, col, pts, 2)
        pygame.draw.circle(surf, (*col, 40), (ix, iy), r-4)

        # Icon text
        icon = PU_ICONS[self.ptype]
        render_text(surf, icon, 14, col, ix, iy, bold=True)

# ======================================================
#  ACTIVE POWERUP (timed effect)
# ======================================================
@dataclass
class ActivePU:
    ptype: PowerupType
    target: int       # 0=p1, 1=p2, -1=global
    duration: float
    remaining: float

# ======================================================
#  AI CONTROLLER
# ======================================================
class AIController:
    def __init__(self, diff: Difficulty):
        self.diff = diff
        cfg = {
            Difficulty.EASY:   dict(react=0.55, err=90, spd=0.52, pred=0.08, adapt=0),
            Difficulty.MEDIUM: dict(react=0.20, err=38, spd=0.78, pred=0.52, adapt=0.1),
            Difficulty.HARD:   dict(react=0.07, err=14, spd=0.91, pred=0.82, adapt=0.25),
            Difficulty.INSANE: dict(react=0.02, err=3,  spd=1.00, pred=0.97, adapt=0.5),
        }[diff]
        self.react      = cfg["react"]
        self.err_range  = cfg["err"]
        self.spd_frac   = cfg["spd"]
        self.pred_frac  = cfg["pred"]
        self.adapt_rate = cfg["adapt"]
        self._timer     = 0.0
        self._target_y  = VH / 2
        self._adapt     = 0.0

    def update(self, paddle: Paddle, balls: List[Ball], dt: float):
        # Pick the most threatening ball
        threat = None
        for b in balls:
            if not b.alive:
                continue
            coming = (paddle.side == 0 and b.vx < 0) or (paddle.side == 1 and b.vx > 0)
            if coming:
                if threat is None or abs(b.x - paddle.x) < abs(threat.x - paddle.x):
                    threat = b

        self._timer -= dt
        if self._timer <= 0:
            self._timer = self.react + random.uniform(0, 0.04)
            if threat is not None:
                if random.random() < self.pred_frac:
                    # Trajectory prediction with bounces
                    travel = abs(threat.x - paddle.x)
                    ttr = travel / max(1, abs(threat.vx))
                    py = threat.y + threat.vy * ttr
                    # Reflect off walls
                    while py < 0 or py > VH:
                        if py < 0:    py = -py
                        if py > VH:   py = 2*VH - py
                    self._target_y = py + self._adapt
                else:
                    self._target_y = threat.y + self._adapt
                # Add error
                self._target_y += random.uniform(-self.err_range, self.err_range)
            else:
                self._target_y = VH / 2

        # Adapt slightly after lost point (called externally via adapt())
        diff = self._target_y - paddle.y
        dead = 10.0
        if abs(diff) > dead:
            direction = 1 if diff > 0 else -1
            spd = min(1.0, abs(diff) / 120) * self.spd_frac
            paddle.move(direction * spd, dt)
        else:
            paddle.move(0, dt)

    def adapt(self, lost: bool):
        if self.adapt_rate > 0:
            self._adapt += (random.uniform(-4, 4) if lost else 0)
            self._adapt *= (1 - self.adapt_rate * 0.1)

# ======================================================
#  MATCH STATISTICS
# ======================================================
@dataclass
class MatchStats:
    hits:       Dict[int, int] = field(default_factory=lambda: {0: 0, 1: 0})
    rally:      int = 0
    best_rally: int = 0
    max_speed:  float = 0.0
    pu_used:    Dict[int, int] = field(default_factory=lambda: {0: 0, 1: 0})
    winner:     str = ""

# ======================================================
#  ACHIEVEMENTS
# ======================================================
ACHIEVE_DEFS = {
    "rally_10":    ("RALLY KING",    "10-hit rally",              "gold"),
    "rally_20":    ("UNSTOPPABLE",   "20-hit rally",              "gold"),
    "speed_900":   ("SPEED DEMON",   "Ball exceeded 900 px/s",    "pu_speed"),
    "perfect":     ("PERFECTION",    "Win without conceding",     "green"),
    "comeback":    ("COMEBACK KID",  "Win after trailing by 3+",  "pu_shield"),
    "combo_6":     ("COMBO MASTER",  "6x combo streak",           "pu_multi"),
    "pu_hoarder":  ("POWER HUNGRY",  "10 powerups in one match",  "pu_magnet"),
    "insane_win":  ("INSANE SLAYER", "Beat Insane AI",            "pu_rev"),
}

class Achievements:
    def __init__(self):
        self.unlocked: Dict[str, bool] = {}
        self.queue: List[Dict] = []
        self._load()

    def _load(self):
        try:
            if os.path.exists(ACHIEVEMENTS_FILE):
                with open(ACHIEVEMENTS_FILE) as f:
                    self.unlocked = json.load(f)
        except Exception:
            pass

    def _save(self):
        try:
            with open(ACHIEVEMENTS_FILE, "w") as f:
                json.dump(self.unlocked, f)
        except Exception:
            pass

    def unlock(self, key: str):
        if not self.unlocked.get(key, False):
            self.unlocked[key] = True
            self._save()
            title, desc, col_key = ACHIEVE_DEFS[key]
            self.queue.append({
                "title": title,
                "desc":  desc,
                "col":   col_key,
                "t":     4.0,
                "max_t": 4.0,
            })
            print(f"[Achievement] Unlocked: {title}")

    def update(self, dt):
        for q in self.queue:
            q["t"] -= dt
        self.queue = [q for q in self.queue if q["t"] > 0]

    def draw(self, surf):
        y_base = VH - 90
        for q in self.queue[-2:]:
            a = min(1.0, q["t"] * 2.0)
            box_w, box_h = 340, 62
            bx = VW - box_w - 12
            by = y_base

            bg = pygame.Surface((box_w, box_h), pygame.SRCALPHA)
            bg.fill((*P["ui_bg"], int(a * 210)))
            pygame.draw.rect(bg, (*P[q["col"]], int(a * 255)),
                             bg.get_rect(), 2, border_radius=10)
            surf.blit(bg, (bx, by))

            icon = Fonts.get(13).render("** ACHIEVEMENT", True, P[q["col"]])
            surf.blit(icon, (bx + 10, by + 6))
            title = Fonts.get(17, True).render(q["title"], True, P["white"])
            surf.blit(title, (bx + 10, by + 24))
            desc = Fonts.get(13).render(q["desc"], True, P["text_dim"])
            surf.blit(desc, (bx + 10, by + 44))
            y_base -= 70

# ======================================================
#  POPUP LABELS (floating score text etc)
# ======================================================
@dataclass
class Popup:
    text: str
    x: float; y: float
    vy: float
    color: Tuple
    size: int
    t: float; max_t: float
    bold: bool = True

class PopupManager:
    def __init__(self):
        self.items: List[Popup] = []

    def add(self, text, x, y, color, size=26, duration=1.6, bold=True):
        self.items.append(Popup(text, x, y, -55.0, color, size, duration, duration, bold))

    def update(self, dt):
        for p in self.items:
            p.y  += p.vy * dt
            p.vy *= 0.94
            p.t  -= dt
        self.items = [p for p in self.items if p.t > 0]

    def draw(self, surf):
        for p in self.items:
            a = min(1.0, p.t / p.max_t * 2)
            col = (*p.color[:3],)
            f = Fonts.get(p.size, p.bold)
            txt = f.render(p.text, True, col)
            txt.set_alpha(int(a * 255))
            r = txt.get_rect(center=(int(p.x), int(p.y)))
            surf.blit(txt, r)

# ======================================================
#  INTERACTIVE UI WIDGETS
# ======================================================
class Button:
    """Animated, glow-on-hover button."""
    def __init__(self, label, cx, cy, w=300, h=54, tag=None):
        self.label = label
        self.rect  = pygame.Rect(cx - w//2, cy - h//2, w, h)
        self.tag   = tag or label
        self.hov   = False
        self.sel   = False
        self._anim = 0.0   # 0..1 hover progress

    def update(self, dt, mouse, clicked) -> bool:
        self.hov = self.rect.collidepoint(mouse)
        self._anim = lerp(self._anim, 1.0 if self.hov else 0.0, dt * 12)
        return self.hov and clicked

    def draw(self, surf, accent=None):
        col = accent or P["p1"]
        a = self._anim

        # Background fill
        bg = pygame.Surface((self.rect.w, self.rect.h), pygame.SRCALPHA)
        bg_alpha = int(15 + 70 * a)
        bg.fill((*col, bg_alpha))
        if a > 0.01:
            for gl in range(3, 0, -1):
                gs = pygame.Surface((self.rect.w + gl*10, self.rect.h + gl*8),
                                    pygame.SRCALPHA)
                gs.fill((*col, int(12 * a / gl)))
                surf.blit(gs,
                          (self.rect.x - gl*5, self.rect.y - gl*4),
                          special_flags=pygame.BLEND_ADD)
        surf.blit(bg, self.rect)

        # Border
        bc = lerp_color(P["ui_border"], col, a)
        pygame.draw.rect(surf, bc, self.rect, 2, border_radius=10)

        # Label
        tc = lerp_color(P["text_dim"], P["white"], a)
        if self.sel:
            tc = col
        f = Fonts.get(22, bold=self.hov or self.sel)
        txt = f.render(self.label, True, tc)
        surf.blit(txt, txt.get_rect(center=self.rect.center))

class ToggleButton(Button):
    """Button that shows ON/OFF state."""
    def __init__(self, label, value, cx, cy, w=360, h=50):
        super().__init__(label, cx, cy, w, h)
        self.value = value

    @property
    def label(self):
        return self._lbl

    @label.setter
    def label(self, v):
        self._lbl = v

    def draw(self, surf, accent=None):
        # Draw base
        super().draw(surf, accent)
        # ON/OFF badge
        badge_col = P["green"] if self.value else P["red"]
        badge_txt = " ON" if self.value else "OFF"
        f = Fonts.get(16, True)
        bt = f.render(badge_txt, True, badge_col)
        surf.blit(bt, bt.get_rect(midright=(self.rect.right - 14,
                                             self.rect.centery)))

class SliderWidget:
    """Interactive horizontal slider."""
    def __init__(self, label, cx, cy, w, vmin, vmax, value, fmt="{:.2f}"):
        self.label = label
        self.cx = cx; self.cy = cy; self.w = w
        self.vmin = vmin; self.vmax = vmax
        self.value = value
        self.fmt = fmt
        self.drag = False
        self.bar = pygame.Rect(cx - w//2, cy - 6, w, 12)

    def update(self, dt, mouse, held):
        if held and self.bar.inflate(0, 24).collidepoint(mouse):
            self.drag = True
        if not held:
            self.drag = False
        if self.drag:
            t = (mouse[0] - self.bar.x) / self.bar.w
            self.value = self.vmin + max(0, min(1, t)) * (self.vmax - self.vmin)

    def draw(self, surf, col=None):
        col = col or P["p1"]
        t = (self.value - self.vmin) / max(0.001, self.vmax - self.vmin)

        # Track
        pygame.draw.rect(surf, P["dark"], self.bar, border_radius=6)
        # Fill
        fw = int(self.bar.w * t)
        if fw > 0:
            pygame.draw.rect(surf, col,
                             (self.bar.x, self.bar.y, fw, self.bar.h),
                             border_radius=6)
        # Knob
        kx = self.bar.x + fw
        ky = self.cy
        pygame.draw.circle(surf, P["white"], (kx, ky), 12)
        pygame.draw.circle(surf, col, (kx, ky), 9)

        # Label
        f = Fonts.get(17)
        lbl = f.render(f"{self.label}: {self.fmt.format(self.value)}", True, P["text"])
        surf.blit(lbl, lbl.get_rect(midright=(self.bar.x - 16, self.cy)))

class CycleButton(Button):
    """Button that cycles through a list of options."""
    def __init__(self, label_prefix, options, current_idx, cx, cy, w=380, h=50):
        self.prefix = label_prefix
        self.options = options
        self.idx = current_idx
        super().__init__(self._full_label(), cx, cy, w, h)

    def _full_label(self):
        return f"{self.prefix}:  {self.options[self.idx]}"

    def cycle(self, audio=None):
        self.idx = (self.idx + 1) % len(self.options)
        self.label = self._full_label()
        if audio:
            audio.play("menu_sel")

    @property
    def current(self):
        return self.options[self.idx]

    def draw(self, surf, accent=None):
        col = accent or P["p1"]
        super().draw(surf, col)
        # Arrow indicators
        f = Fonts.get(20, True)
        arr = f.render("<  >", True, lerp_color(P["text_dim"], col, self._anim))
        surf.blit(arr, arr.get_rect(midright=(self.rect.right - 10,
                                              self.rect.centery)))

# ======================================================
#  CARD PANEL (translucent backdrop)
# ======================================================
def draw_card(surf, cx, cy, w, h, border_col=None, alpha=190, radius=16):
    border_col = border_col or P["ui_border"]
    bg = pygame.Surface((w, h), pygame.SRCALPHA)
    bg.fill((*P["ui_bg"], alpha))
    pygame.draw.rect(bg, (*border_col, 220), bg.get_rect(), 2, border_radius=radius)
    surf.blit(bg, (cx - w//2, cy - h//2))

# ======================================================
#  CRT OVERLAY
# ======================================================
_crt_surf: Optional[pygame.Surface] = None

def draw_crt(surf):
    global _crt_surf
    if _crt_surf is None or _crt_surf.get_size() != surf.get_size():
        _crt_surf = pygame.Surface(surf.get_size(), pygame.SRCALPHA)
        for y in range(0, surf.get_height(), 4):
            pygame.draw.line(_crt_surf, (0, 0, 0, 55), (0, y), (surf.get_width(), y))
        # Vignette
        w, h = surf.get_size()
        for edge in range(80):
            a = int(140 * (1 - edge / 80) ** 2)
            pygame.draw.rect(_crt_surf, (0, 0, 0, a),
                             (edge, edge, w - 2*edge, h - 2*edge), 1)
    surf.blit(_crt_surf, (0, 0))

# ======================================================
#  SCOREBOARD HUD
# ======================================================
def draw_hud(surf, p1: Paddle, p2: Paddle, balls: List[Ball],
             stats: MatchStats, settings: Settings,
             mode: GameMode, t: float, quality: str,
             active_pus: List[ActivePU]):
    cx = VW // 2

    # Score card background
    draw_card(surf, cx, 44, 280, 74, alpha=160)

    # Player labels
    lbl1 = "PLAYER 1"
    lbl2 = "PLAYER 2" if mode == GameMode.TWO_PLAY else "AI"
    render_text(surf, lbl1, 14, P["p1"], VW//4, 14, bold=True)
    render_text(surf, lbl2, 14, P["p2"], VW*3//4, 14, bold=True)

    # Scores (big)
    render_glow(surf, str(p1.score), 60, P["p1"], cx - 110, 46, bold=True, layers=2)
    render_glow(surf, str(p2.score), 60, P["p2"], cx + 110, 46, bold=True, layers=2)

    # Separator
    pygame.draw.line(surf, P["center"], (cx, 12), (cx, 76), 2)

    # Arcade pts
    if settings.arcade_score:
        render_text(surf, str(p1.arcade_pts), 13, P["text_dim"], VW//4, 78)
        render_text(surf, str(p2.arcade_pts), 13, P["text_dim"], VW*3//4, 78)

    # Ball speed
    if balls:
        spd = int(max(b.speed for b in balls))
        ratio = min(1.0, spd / 900)
        sc = lerp_color(P["text"], P["ball_fire"], ratio)
        render_text(surf, f"SPD {spd}", 13, sc, cx, 86)

    # Rally counter
    if stats.rally >= 4:
        ratio = min(1.0, stats.rally / 18)
        rc = lerp_color(P["white"], P["gold"], ratio)
        render_text(surf, f"RALLY  {stats.rally}", 15, rc, cx, 100)

    # Active powerup bars (left side)
    py_offset = 120
    for ap in active_pus:
        col = P[PU_COLORS[ap.ptype]]
        ratio = ap.remaining / ap.duration
        bw = 120
        bx, by_pos = 10, py_offset
        pygame.draw.rect(surf, P["dark"], (bx, by_pos, bw, 10), border_radius=5)
        pygame.draw.rect(surf, col, (bx, by_pos, int(bw*ratio), 10), border_radius=5)
        f = Fonts.get(11)
        lbl = f.render(ap.ptype.value[:10], True, col)
        surf.blit(lbl, (bx, by_pos - 13))
        py_offset += 28

    # Match goal
    pts_lbl = Fonts.get(13).render(f"FIRST TO {settings.match_pts}", True, P["text_dim"])
    surf.blit(pts_lbl, pts_lbl.get_rect(midbottom=(cx, VH - 8)))

# ======================================================
#  GAME SCENE
# ======================================================
class GameScene:
    PU_SPAWN_INTERVAL = (9.0, 20.0)
    REPLAY_DURATION   = 2.2

    def __init__(self, settings: Settings, audio: Audio,
                 mode: GameMode, achieve: Achievements):
        self.s       = settings
        self.audio   = audio
        self.mode    = mode
        self.achieve = achieve

        set_theme(settings.theme)
        self.particles = ParticleSystem()
        self.shake     = ShakeEffect()
        self.popups    = PopupManager()
        self.bg        = Background()

        self._init_objects()

        self.stats     = MatchStats()
        self.replay_t  = 0.0
        self.slow      = 1.0
        self.score_flash_t = 0.0
        self.t         = 0.0
        self.next_pu   = self.t + random.uniform(*self.PU_SPAWN_INTERVAL)
        self.pu_items: List[PowerupItem] = []
        self.active_pu: List[ActivePU]   = []
        self.total_pu_collected = 0

    def _init_objects(self):
        col1 = P["p1"]; col2 = P["p2"]
        margin = 42
        self.p1 = Paddle(margin, 0, col1)
        self.p2 = Paddle(VW - margin, 1, col2)

        bt = BallType(self.s.ball_type)
        self.balls: List[Ball] = [Ball(bt, random.choice([-1, 1]))]

        diff = Difficulty(self.s.difficulty)
        self.ai = AIController(diff) if self.mode == GameMode.SINGLE else None

    def reset_after_score(self, scorer: int):
        bt = BallType(self.s.ball_type)
        direction = 1 if scorer == 0 else -1
        self.balls = [Ball(bt, direction)]
        self.pu_items.clear()

    # -- INPUT ------------------------------------------
    def handle_input(self, keys, dt):
        # P1
        d1 = 0
        if keys[self.s.p1_up]:  d1 = -1
        if keys[self.s.p1_dn]:  d1 =  1
        self.p1.move(d1, dt)

        # P2 or AI
        if self.ai:
            self.ai.update(self.p2, self.balls, dt)
        else:
            d2 = 0
            if keys[self.s.p2_up]: d2 = -1
            if keys[self.s.p2_dn]: d2 =  1
            self.p2.move(d2, dt)

    # -- UPDATE -----------------------------------------
    def update(self, dt) -> Optional[str]:
        """Returns None or 'scored_p1'/'scored_p2'/'match_end'."""
        self.t += dt
        self.shake.update(dt)
        self.particles.update(dt)
        self.popups.update(dt)

        # Replay slow-motion
        if self.replay_t > 0:
            self.replay_t -= dt
            self.slow = 0.22
        else:
            self.slow = 1.0

        # Training speed override
        if self.mode == GameMode.TRAINING:
            self.slow *= self.s.training_speed

        # Balls
        scored = None
        for ball in self.balls[:]:
            result = ball.update(dt, self.slow)
            if result == "wall":
                self._on_wall(ball)
            # Scoring
            if ball.x - ball.r < 0:
                scored = 1    # p2 scored
                self.balls.remove(ball)
            elif ball.x + ball.r > VW:
                scored = 0    # p1 scored
                self.balls.remove(ball)
            else:
                self._check_paddle(ball, self.p1)
                self._check_paddle(ball, self.p2)
                self.stats.max_speed = max(self.stats.max_speed, ball.speed)

        if scored is not None:
            return self._handle_score(scored)

        if not self.balls:
            bt = BallType(self.s.ball_type)
            self.balls = [Ball(bt, 1)]

        # Powerups
        if self.s.powerups and self.t > self.next_pu and len(self.pu_items) < 3:
            self._spawn_pu()
            self.next_pu = self.t + random.uniform(*self.PU_SPAWN_INTERVAL)

        for item in self.pu_items[:]:
            item.update(dt)
            for ball in self.balls:
                if math.hypot(ball.x - item.x, ball.y - item.y) < ball.r + item.r:
                    self._collect_pu(item, ball)
                    self.pu_items.remove(item)
                    break

        # Active PU timers
        for ap in self.active_pu[:]:
            ap.remaining -= dt
            if ap.remaining <= 0:
                self._expire_pu(ap)
                self.active_pu.remove(ap)
                self.audio.play("pu_expire")

        # Paddle update
        self.p1.update(dt)
        self.p2.update(dt)

        # Trail particles
        if self.s.quality != "LOW":
            for ball in self.balls:
                self.particles.trail(ball.x, ball.y, ball.color,
                                     size=max(2, int(ball.r * 0.45)))

        return None

    def _on_wall(self, ball: Ball):
        self.audio.play("wall")
        self.particles.emit(int(ball.x), int(ball.y), P["white"],
                            n=5, speed=2.5, gravity=0.04, glow=False)
        if self.s.shake:
            self.shake.trigger(2.5)

    def _check_paddle(self, ball: Ball, paddle: Paddle):
        r  = paddle.rect
        br = ball.r

        # AABB quick reject
        if not (r.left - br <= ball.x <= r.right + br and
                r.top  - br <= ball.y <= r.bottom + br):
            return

        # Circle-rect
        cx = max(r.left, min(ball.x, r.right))
        cy = max(r.top,  min(ball.y, r.bottom))
        if math.hypot(ball.x - cx, ball.y - cy) > br:
            return

        # Deflect
        rel = (ball.y - paddle.y) / (paddle.h / 2)
        rel = max(-1.0, min(1.0, rel))
        angle = rel * math.radians(62)
        spd = math.hypot(ball.vx, ball.vy)
        dir_x = 1 if paddle.side == 0 else -1
        ball.vx = math.cos(angle) * spd * dir_x
        ball.vy = math.sin(angle) * spd
        ball.spin = paddle.vy * 0.07

        # Push out
        if paddle.side == 0:
            ball.x = r.right + br + 1
        else:
            ball.x = r.left  - br - 1

        ball.accelerate(1.045)

        # Magnet hold (slight)
        if paddle.magnet:
            ball.attracted_to = paddle

        # Stats
        self.stats.hits[paddle.side] += 1
        self.stats.rally += 1
        if self.stats.rally > self.stats.best_rally:
            self.stats.best_rally = self.stats.rally

        # Combo
        if self.s.combo:
            paddle.combo += 1
            paddle.combo_t = 3.2
            if paddle.combo >= 6:
                self.achieve.unlock("combo_6")
            if paddle.combo >= 2:
                self.audio.play("combo")
                pts = 10 * paddle.combo
                col = lerp_color(P["white"], P["gold"], min(1.0, paddle.combo / 8))
                self.popups.add(f"x{paddle.combo}  +{pts}", int(paddle.x), int(paddle.y - 60), col, 22)
                paddle.arcade_pts += pts

        # Achievements
        if self.stats.best_rally >= 10:
            self.achieve.unlock("rally_10")
        if self.stats.best_rally >= 20:
            self.achieve.unlock("rally_20")
        if self.stats.max_speed >= 900:
            self.achieve.unlock("speed_900")

        # Effects
        paddle.hit_flash = 0.14
        if self.s.shake and ball.speed > Ball.BASE_SPD * 1.4:
            self.shake.trigger(min(11, ball.speed / 95))
        self.particles.emit(int(ball.x), int(ball.y), paddle.color,
                            n=14, speed=5, gravity=0.06, glow=True,
                            direction=math.atan2(ball.vy, ball.vx),
                            spread=math.pi * 0.7)
        self.audio.play("paddle")

    def _handle_score(self, scorer: int) -> str:
        """scorer: 0=p1 got point (ball left p2 side), 1=p2 got point."""
        # scorer=1 means ball left screen on LEFT side -> p2 scored
        # scorer=0 means ball left on RIGHT side -> p1 scored
        self.stats.rally = 0
        self.audio.play("score")
        if self.s.shake:
            self.shake.trigger(14)

        scoring_p = self.p1 if scorer == 0 else self.p2
        scoring_p.score += 1
        scoring_p.arcade_pts += 100

        if self.ai:
            self.ai.adapt(lost=(scorer == 1))

        # Celebration particles
        bx = VW * 0.15 if scorer == 0 else VW * 0.85
        col = scoring_p.color
        self.particles.emit(int(bx), VH//2, col, n=80, speed=9,
                            gravity=0.05, glow=True)
        self.popups.add("POINT!", int(bx), VH//2 - 50, col, 44, 2.0)

        # Replay
        self.replay_t = self.REPLAY_DURATION

        # Training infinite lives
        if self.mode == GameMode.TRAINING:
            self.reset_after_score(scorer)
            return "training_score"

        # Check win
        pts = self.s.match_pts
        p1s, p2s = self.p1.score, self.p2.score
        win_by_2 = self.s.win_by_2
        p1_win = p1s >= pts and (not win_by_2 or p1s - p2s >= 2)
        p2_win = p2s >= pts and (not win_by_2 or p2s - p1s >= 2)

        if p1_win or p2_win:
            winner = "PLAYER 1" if p1_win else \
                     ("PLAYER 2" if self.mode == GameMode.TWO_PLAY else "AI")
            self.stats.winner = winner
            # Achievements
            if p1_win and p2s == 0:
                self.achieve.unlock("perfect")
            if p1_win and (p2s - p1s >= 3 or p2s - p1s >= 3):
                pass  # comeback (simplified)
            if self.mode == GameMode.SINGLE and p1_win and \
               Difficulty(self.s.difficulty) == Difficulty.INSANE:
                self.achieve.unlock("insane_win")
            self.audio.play("win" if p1_win else "lose")
            return "match_end"

        self.reset_after_score(scorer)
        return f"scored_p{scorer+1}"

    def _spawn_pu(self):
        ptype = random.choice(list(PowerupType))
        x = random.uniform(VW * 0.22, VW * 0.78)
        y = random.uniform(80, VH - 80)
        self.pu_items.append(PowerupItem(x, y, ptype))

    def _collect_pu(self, item: PowerupItem, ball: Ball):
        ptype = item.ptype
        self.audio.play("powerup")
        self.total_pu_collected += 1
        if self.total_pu_collected >= 10:
            self.achieve.unlock("pu_hoarder")

        dur = 8.0
        self.particles.emit(int(item.x), int(item.y), item.color,
                            n=30, speed=6, gravity=0.08, glow=True)
        self.popups.add(f"** {ptype.value}", VW//2, VH//2 - 80,
                        item.color, 28, 1.8)

        if ptype == PowerupType.SPEED:
            spd = math.hypot(ball.vx, ball.vy)
            scale = min(Ball.MAX_SPD / max(1, spd), 1.4)
            ball.vx *= scale; ball.vy *= scale
        elif ptype == PowerupType.SLOW:
            self.active_pu.append(ActivePU(ptype, -1, dur, dur))
        elif ptype == PowerupType.BIG:
            side = random.choice([0, 1])
            p = self.p1 if side == 0 else self.p2
            p.h = min(Paddle.H * 2.2, p.h * 1.6)
            self.active_pu.append(ActivePU(ptype, side, dur, dur))
        elif ptype == PowerupType.MULTI:
            bt = BallType(self.s.ball_type)
            nb = Ball(bt, -1 if ball.vx > 0 else 1)
            nb.x, nb.y = ball.x, ball.y
            self.balls.append(nb)
        elif ptype == PowerupType.SHIELD:
            side = random.choice([0, 1])
            p = self.p1 if side == 0 else self.p2
            p.shield = True; p.shield_hp = 1
            self.active_pu.append(ActivePU(ptype, side, dur, dur))
        elif ptype == PowerupType.INVIS:
            ball.invisible = True
            ball.invis_t = 4.5
        elif ptype == PowerupType.REVERSE:
            side = random.choice([0, 1])
            p = self.p1 if side == 0 else self.p2
            p.reverse = True
            self.active_pu.append(ActivePU(ptype, side, 5.0, 5.0))
        elif ptype == PowerupType.MAGNET:
            side = random.choice([0, 1])
            p = self.p1 if side == 0 else self.p2
            p.magnet = True
            self.active_pu.append(ActivePU(ptype, side, dur, dur))

    def _expire_pu(self, ap: ActivePU):
        if ap.ptype == PowerupType.BIG:
            p = self.p1 if ap.target == 0 else self.p2
            p.reset_size()
        elif ap.ptype == PowerupType.SHIELD:
            p = self.p1 if ap.target == 0 else self.p2
            p.shield = False
        elif ap.ptype == PowerupType.REVERSE:
            p = self.p1 if ap.target == 0 else self.p2
            p.reverse = False
        elif ap.ptype == PowerupType.MAGNET:
            p = self.p1 if ap.target == 0 else self.p2
            p.magnet = False
            for b in self.balls:
                b.attracted_to = None

    def draw(self, surf, quality: str):
        self.bg.draw(surf, 0.016, quality, self.s.theme)
        self.bg.draw_center_line(surf, quality, self.t)

        # Shake offset
        ox, oy = (int(self.shake.offset[0]), int(self.shake.offset[1])) \
                  if self.s.shake else (0, 0)

        # Game objects surface (shakeable)
        game_surf = pygame.Surface((VW, VH), pygame.SRCALPHA)
        game_surf.fill((0, 0, 0, 0))

        # Powerup items
        for item in self.pu_items:
            item.draw(game_surf, quality)

        # Particles
        self.particles.draw(game_surf, quality)

        # Paddles
        self.p1.draw(game_surf, quality)
        self.p2.draw(game_surf, quality)

        # Balls
        for ball in self.balls:
            ball.draw(game_surf, quality, self.t)

        surf.blit(game_surf, (ox, oy))

        # HUD (no shake)
        draw_hud(surf, self.p1, self.p2, self.balls, self.stats,
                 self.s, self.mode, self.t, quality, self.active_pu)

        # Popups
        self.popups.draw(surf)

        # Slow-motion indicator
        if self.replay_t > 0:
            rt = Fonts.get(18).render("<<  REPLAY", True, P["gold"])
            surf.blit(rt, rt.get_rect(midbottom=(VW//2, VH - 8)))

        # Training label
        if self.mode == GameMode.TRAINING:
            tl = Fonts.get(14).render("TRAINING -- INFINITE LIVES", True, P["text_dim"])
            surf.blit(tl, tl.get_rect(midbottom=(VW//2, VH - 22)))

# ======================================================
#  MENU SCENE
# ======================================================
class MainMenu:
    def __init__(self, settings: Settings, audio: Audio):
        self.s = settings
        self.audio = audio
        self.bg = Background()
        self.particles = ParticleSystem()
        self.t = 0.0
        self._prev_hov = -1
        cx = VW // 2

        self.buttons = [
            Button("[ 1 ] SINGLE PLAYER",  cx, 310, 360, 58, "single"),
            Button("[ 2 ] TWO PLAYERS",     cx, 378, 360, 58, "two"),
            Button("[ T ] TRAINING MODE",   cx, 446, 360, 58, "training"),
            Button("[ S ] SETTINGS",        cx, 514, 360, 58, "settings"),
            Button("?  HOW TO PLAY",     cx, 582, 360, 58, "howtoplay"),
            Button("[ X ] QUIT",            cx, 650, 360, 58, "quit"),
        ]
        self.colors = [P["p1"], P["p2"], P["green"],
                       P["text"], P["pu_shield"], P["red"]]
        self.sel = 0

    def update(self, dt, mouse, clicked, keys_just) -> Optional[str]:
        self.t += dt

        # Keyboard nav
        if pygame.K_UP in keys_just:
            self.sel = (self.sel - 1) % len(self.buttons)
            self.audio.play("menu_move")
        if pygame.K_DOWN in keys_just:
            self.sel = (self.sel + 1) % len(self.buttons)
            self.audio.play("menu_move")
        if pygame.K_RETURN in keys_just or pygame.K_SPACE in keys_just:
            self.audio.play("menu_sel")
            return self.buttons[self.sel].tag

        # Mouse
        hov_idx = -1
        for i, btn in enumerate(self.buttons):
            col = self.colors[i % len(self.colors)]
            if btn.update(dt, mouse, False):
                pass
            if btn.hov:
                hov_idx = i
                self.sel = i
            btn.sel = (i == self.sel)

        if hov_idx != self._prev_hov and hov_idx >= 0:
            self.audio.play("menu_move")
        self._prev_hov = hov_idx

        if clicked:
            for btn in self.buttons:
                if btn.hov:
                    self.audio.play("menu_sel")
                    return btn.tag

        # Background particles
        if random.random() < dt * 12:
            x = random.uniform(0, VW)
            col = random.choice([P["p1"], P["p2"], P["gold"]])
            self.particles.emit(x, VH + 5, col, n=1, speed=1.5,
                                gravity=-0.05, life=(2, 4), size=(1, 3))

        self.particles.update(dt)
        return None

    def draw(self, surf, quality: str):
        self.bg.draw(surf, 0.016, quality, self.s.theme)
        self.particles.draw(surf, quality)

        # Animated title
        cy = 130 + int(6 * math.sin(self.t * 1.3))
        render_glow(surf, "PING PONG", 88, P["p1"], VW//2, cy, bold=True, layers=4)

        # Decorative corner accents
        for pts in [((0,0),(100,0),(0,100)), ((VW,0),(VW-100,0),(VW,100)),
                    ((0,VH),(100,VH),(0,VH-100)), ((VW,VH),(VW-100,VH),(VW,VH-100))]:
            pygame.draw.lines(surf, P["p1"], False, pts[:2], 2)
            pygame.draw.lines(surf, P["p1"], False, [pts[0], pts[2]], 2)

        # Buttons
        for i, btn in enumerate(self.buttons):
            col = self.colors[i % len(self.colors)]
            btn.draw(surf, col)

        # Controls hint
        render_text(surf, "W/S  ·  ^v  ·  ESC  ·  MOUSE",
                    13, P["text_dim"], VW//2, VH - 12)

# ======================================================
#  SETTINGS SCENE
# ======================================================
class SettingsScene:
    def __init__(self, settings: Settings, audio: Audio):
        self.s = settings
        self.audio = audio
        self.bg = Background()
        self.t = 0.0
        cx = VW // 2
        self._build(cx)

    def _build(self, cx):
        s = self.s
        self.cycles = [
            CycleButton("DIFFICULTY",   ["EASY","MEDIUM","HARD","INSANE"],
                        ["EASY","MEDIUM","HARD","INSANE"].index(s.difficulty),
                        cx, 190, 440),
            CycleButton("MATCH POINTS", ["7","11","21"],
                        ["7","11","21"].index(str(s.match_pts)),
                        cx, 250, 440),
            CycleButton("THEME",        ["NEON","CLASSIC","SYNTHWAVE"],
                        ["NEON","CLASSIC","SYNTHWAVE"].index(s.theme),
                        cx, 310, 440),
            CycleButton("QUALITY",      ["LOW","MEDIUM","HIGH"],
                        ["LOW","MEDIUM","HIGH"].index(s.quality),
                        cx, 370, 440),
            CycleButton("BALL TYPE",    ["NORMAL","HEAVY","LIGHT","FIREBALL"],
                        ["NORMAL","HEAVY","LIGHT","FIREBALL"].index(s.ball_type),
                        cx, 430, 440),
        ]
        self.toggles = [
            ToggleButton("SOUND",        s.sound,       cx, 490, 380),
            ToggleButton("POWERUPS",     s.powerups,    cx, 545, 380),
            ToggleButton("WIN BY 2",     s.win_by_2,    cx, 600, 380),
            ToggleButton("SCREEN SHAKE", s.shake,       cx, 655, 380),
            ToggleButton("CRT FILTER",   s.crt,         cx, 710, 380) if VH > 700 else None,
            ToggleButton("ARCADE SCORE", s.arcade_score,cx+220, 490, 200),
            ToggleButton("COMBO SYSTEM", s.combo,       cx+220, 545, 200),
        ]
        self.toggles = [t for t in self.toggles if t is not None]

        self.vol_slider = SliderWidget("VOLUME", cx, 760, 340,
                                       0.0, 1.0, s.volume, fmt="{:.0%}")
        self.back_btn   = Button("<  BACK", cx, 720 if VH <= 700 else 810, 240, 50)

    def update(self, dt, mouse, clicked, held, keys_just) -> Optional[str]:
        self.t += dt
        if pygame.K_ESCAPE in keys_just:
            self._save()
            return "back"

        for cy in self.cycles:
            if cy.update(dt, mouse, clicked):
                cy.cycle(self.audio)

        for tg in self.toggles:
            if tg.update(dt, mouse, clicked):
                tg.value = not tg.value
                self.audio.play("menu_sel")

        self.vol_slider.update(dt, mouse, held)
        if self.back_btn.update(dt, mouse, clicked) or \
           (pygame.K_RETURN in keys_just and not any(c.hov for c in self.cycles)):
            self._save()
            return "back"
        return None

    def _save(self):
        s = self.s
        s.difficulty    = self.cycles[0].current
        s.match_pts     = int(self.cycles[1].current)
        s.theme         = self.cycles[2].current
        s.quality       = self.cycles[3].current
        s.ball_type     = self.cycles[4].current
        s.sound         = self.toggles[0].value
        s.powerups      = self.toggles[1].value
        s.win_by_2      = self.toggles[2].value
        s.shake         = self.toggles[3].value
        # toggles[4] might be CRT or arcade_score
        for tg in self.toggles:
            if tg._lbl == "CRT FILTER":       s.crt         = tg.value
            if tg._lbl == "ARCADE SCORE":     s.arcade_score= tg.value
            if tg._lbl == "COMBO SYSTEM":     s.combo       = tg.value
            if tg._lbl == "SCREEN SHAKE":     s.shake       = tg.value
        s.volume = self.vol_slider.value
        set_theme(s.theme)
        s.save()
        print("[Settings] Saved.")

    def draw(self, surf, quality: str):
        self.bg.draw(surf, 0.016, quality, self.s.theme)

        # Big card
        draw_card(surf, VW//2, VH//2 + 20, 860, VH - 60, alpha=200)

        render_glow(surf, "SETTINGS", 52, P["p1"], VW//2, 55, bold=True, layers=3)

        # Sections
        render_text(surf, "GAMEPLAY", 14, P["text_dim"], VW//2 - 340, 158, bold=True)
        render_text(surf, "TOGGLES",  14, P["text_dim"], VW//2 - 340, 458, bold=True)

        for cy in self.cycles:
            cy.draw(surf, P["ui_hi"])
        for tg in self.toggles:
            col = P["p2"] if tg.value else P["text_dim"]
            tg.draw(surf, col)

        self.vol_slider.draw(surf, P["p1"])
        self.back_btn.draw(surf, P["gray"])

        render_text(surf, "ESC or BACK to return", 13, P["text_dim"], VW//2, VH - 8)

# ======================================================
#  HOW TO PLAY SCENE
# ======================================================
class HowToPlay:
    def __init__(self, settings: Settings, audio: Audio):
        self.s = settings
        self.audio = audio
        self.bg = Background()
        self.back_btn = Button("<  BACK", VW//2, VH - 38, 220, 48)
        self.t = 0.0

    LINES = [
        ("CONTROLS",       None, "gold", 22, True),
        ("Player 1   :  W / S  --  move paddle up / down",   None, "p1",   17, False),
        ("Player 2   :  ^ / v  --  move paddle up / down",  None, "p2",   17, False),
        ("ESC        :  Pause / back",                        None, "text", 17, False),
        ("F          :  Toggle FPS display",                  None, "text", 17, False),
        ("T          :  Cycle themes in-game",                None, "text", 17, False),
        ("",              None, "text", 8,  False),
        ("GAMEPLAY",       None, "gold", 22, True),
        ("Score points by getting the ball past your opponent.", None, "text", 17, False),
        ("Ball speed increases every rally. Hit angle depends on paddle position.", None, "text", 16, False),
        ("Moving paddle adds spin -- the ball will curve slightly.", None, "text", 16, False),
        ("",              None, "text", 8,  False),
        ("POWERUPS",       None, "gold", 22, True),
        (">> SPEED BOOST  -- Ball launches faster instantly",  None, "pu_speed",  16, False),
        ("|| SLOW MOTION  -- Slows time for everyone",         None, "pu_slow",   16, False),
        ("[] BIG PADDLE   -- Grows a random paddle",           None, "pu_big",    16, False),
        ("## MULTI BALL   -- Spawns an extra ball",            None, "pu_multi",  16, False),
        ("<> SHIELD       -- Absorbs one hit",                 None, "pu_shield", 16, False),
        ("~~ INVISIBLE    -- Ball flickers and hides",         None, "pu_invis",  16, False),
        ("vv REVERSE      -- Inverts paddle controls briefly", None, "pu_rev",    16, False),
        ("() MAGNET       -- Ball curves toward paddle",       None, "pu_magnet", 16, False),
        ("",              None, "text", 8,  False),
        ("TIPS",           None, "gold", 22, True),
        ("Spin + powerups = beating Insane AI. Aim for corners!", None, "text", 16, False),
    ]

    def update(self, dt, mouse, clicked, keys_just) -> Optional[str]:
        self.t += dt
        if pygame.K_ESCAPE in keys_just or pygame.K_RETURN in keys_just:
            return "back"
        if self.back_btn.update(dt, mouse, clicked):
            return "back"
        return None

    def draw(self, surf, quality: str):
        self.bg.draw(surf, 0.016, quality, self.s.theme)
        draw_card(surf, VW//2, VH//2, VW - 60, VH - 40, alpha=210)

        render_glow(surf, "HOW TO PLAY", 46, P["p1"], VW//2, 46, bold=True, layers=3)

        y = 88
        for (text, _, col_key, size, bold) in self.LINES:
            if not text:
                y += size
                continue
            col = P.get(col_key, P["text"])
            f = Fonts.get(size, bold)
            txt = f.render(text, True, col)
            surf.blit(txt, txt.get_rect(midleft=(50, y)))
            y += size + 4

        self.back_btn.draw(surf, P["gray"])

# ======================================================
#  PAUSE SCENE
# ======================================================
class PauseScene:
    def __init__(self, settings: Settings, audio: Audio):
        self.s = settings
        self.audio = audio
        cx = VW // 2
        self.buttons = [
            Button("[ > ] RESUME",        cx, 320, 300, 56, "resume"),
            Button("[ R ] RESTART",       cx, 385, 300, 56, "restart"),
            Button("[ S ] SETTINGS",      cx, 450, 300, 56, "settings"),
            Button("[ Q ] QUIT TO MENU",  cx, 515, 300, 56, "menu"),
        ]
        self.sel = 0
        self._prev_hov = -1

    def update(self, dt, mouse, clicked, keys_just) -> Optional[str]:
        if pygame.K_ESCAPE in keys_just:
            return "resume"
        if pygame.K_UP in keys_just:
            self.sel = (self.sel - 1) % len(self.buttons)
            self.audio.play("menu_move")
        if pygame.K_DOWN in keys_just:
            self.sel = (self.sel + 1) % len(self.buttons)
            self.audio.play("menu_move")
        if pygame.K_RETURN in keys_just or pygame.K_SPACE in keys_just:
            self.audio.play("menu_sel")
            return self.buttons[self.sel].tag

        hov_idx = -1
        for i, btn in enumerate(self.buttons):
            btn.sel = (i == self.sel)
            if btn.update(dt, mouse, clicked):
                self.audio.play("menu_sel")
                return btn.tag
            if btn.hov:
                hov_idx = i
                self.sel = i
        if hov_idx != self._prev_hov and hov_idx >= 0:
            self.audio.play("menu_move")
        self._prev_hov = hov_idx
        return None

    def draw(self, game_surf, surf, quality: str):
        # Blur/dim the game behind
        surf.blit(game_surf, (0, 0))
        ov = pygame.Surface((VW, VH), pygame.SRCALPHA)
        ov.fill((0, 0, 20, 175))
        surf.blit(ov, (0, 0))

        draw_card(surf, VW//2, VH//2 - 10, 380, 360, alpha=210)
        render_glow(surf, "PAUSED", 62, P["p1"], VW//2, 240, bold=True, layers=3)

        for btn in self.buttons:
            btn.draw(surf)

        render_text(surf, "ESC -- RESUME", 13, P["text_dim"], VW//2, VH - 12)

# ======================================================
#  MATCH END SCENE
# ======================================================
class MatchEndScene:
    def __init__(self, settings: Settings, audio: Audio,
                 stats: MatchStats, p1: Paddle, p2: Paddle,
                 mode: GameMode, achieve: Achievements):
        self.s = settings
        self.audio = audio
        self.stats = stats
        self.p1 = p1
        self.p2 = p2
        self.mode = mode
        self.achieve = achieve
        self.bg = Background()
        self.particles = ParticleSystem()
        self.t = 0.0
        cx = VW // 2
        self.buttons = [
            Button("[ R ] PLAY AGAIN",   cx, VH - 120, 280, 52, "again"),
            Button("[ M ] MAIN MENU",    cx, VH - 58,  280, 52, "menu"),
        ]
        self.sel = 0

    def update(self, dt, mouse, clicked, keys_just) -> Optional[str]:
        self.t += dt
        if pygame.K_UP in keys_just or pygame.K_LEFT in keys_just:
            self.sel = (self.sel - 1) % len(self.buttons)
            self.audio.play("menu_move")
        if pygame.K_DOWN in keys_just or pygame.K_RIGHT in keys_just:
            self.sel = (self.sel + 1) % len(self.buttons)
            self.audio.play("menu_move")
        if pygame.K_RETURN in keys_just or pygame.K_SPACE in keys_just:
            self.audio.play("menu_sel")
            return self.buttons[self.sel].tag

        for btn in self.buttons:
            btn.sel = (btn.tag == self.buttons[self.sel].tag)
            if btn.update(dt, mouse, clicked):
                self.audio.play("menu_sel")
                return btn.tag

        # Celebration particles
        self.particles.update(dt)
        if random.random() < dt * 20:
            is_p1 = "1" in self.stats.winner
            col = self.p1.color if is_p1 else self.p2.color
            self.particles.emit(
                random.uniform(0, VW), -5,
                col, n=2, speed=2.5, gravity=0.08,
                life=(3, 5), size=(3, 8), glow=True)

        self.achieve.update(dt)
        return None

    def draw(self, surf, quality: str):
        self.bg.draw(surf, 0.016, quality, self.s.theme)
        self.particles.draw(surf, quality)

        is_p1 = "1" in self.stats.winner
        win_col = self.p1.color if is_p1 else self.p2.color

        # Title
        gy = 80 + int(5 * math.sin(self.t * 2.2))
        render_glow(surf, f"{self.stats.winner}", 68, win_col, VW//2, gy, bold=True, layers=4)
        render_glow(surf, "WINS!", 48, P["white"], VW//2, gy + 72, bold=True, layers=2)

        # Stats card
        draw_card(surf, VW//2, VH//2 + 30, 620, 340, border_col=win_col, alpha=210)

        cx = VW // 2
        sy = VH//2 - 120

        def stat_row(label, val, col_val=None):
            nonlocal sy
            f = Fonts.get(18)
            lbl = f.render(label, True, P["text_dim"])
            surf.blit(lbl, lbl.get_rect(midleft=(cx - 280, sy)))
            vc = col_val or P["white"]
            val_t = Fonts.get(18, True).render(str(val), True, vc)
            surf.blit(val_t, val_t.get_rect(midright=(cx + 280, sy)))
            sy += 34

        stat_row("FINAL SCORE",
                 f"{self.p1.score}  --  {self.p2.score}")
        stat_row("LONGEST RALLY", self.stats.best_rally, P["gold"])
        stat_row("TOTAL HITS",
                 f"{self.stats.hits[0]}  vs  {self.stats.hits[1]}")
        stat_row("MAX BALL SPEED",
                 f"{int(self.stats.max_speed)} px/s",
                 lerp_color(P["white"], P["ball_fire"],
                             min(1.0, self.stats.max_speed / 900)))
        if self.s.arcade_score:
            stat_row("ARCADE SCORE",
                     f"{self.p1.arcade_pts}  --  {self.p2.arcade_pts}",
                     P["gold"])

        for btn in self.buttons:
            col = P["p1"] if btn.tag == "again" else P["gray"]
            btn.draw(surf, col)

        self.achieve.draw(surf)

# ======================================================
#  ACHIEVEMENTS BROWSE SCENE
# ======================================================
class AchievementsScene:
    def __init__(self, settings: Settings, audio: Audio, achieve: Achievements):
        self.s = settings
        self.audio = audio
        self.achieve = achieve
        self.bg = Background()
        self.back_btn = Button("<  BACK", VW//2, VH - 38, 220, 48)
        self.t = 0.0

    def update(self, dt, mouse, clicked, keys_just) -> Optional[str]:
        self.t += dt
        if pygame.K_ESCAPE in keys_just or pygame.K_RETURN in keys_just:
            return "back"
        if self.back_btn.update(dt, mouse, clicked):
            return "back"
        return None

    def draw(self, surf, quality: str):
        self.bg.draw(surf, 0.016, quality, self.s.theme)
        draw_card(surf, VW//2, VH//2, VW - 100, VH - 60, alpha=210)
        render_glow(surf, "ACHIEVEMENTS", 46, P["gold"], VW//2, 46, bold=True, layers=3)

        y = 100
        cols = 2
        items = list(ACHIEVE_DEFS.items())
        for i, (key, (title, desc, col_key)) in enumerate(items):
            unlocked = self.achieve.unlocked.get(key, False)
            col = P.get(col_key, P["text"]) if unlocked else P["dark"]
            border = col if unlocked else P["ui_border"]
            ix = (i % cols) * (VW//2 - 20) + 50 + (VW//2 - 20) * (i % cols == 1)
            iy = y + (i // cols) * 90

            draw_card(surf, VW//4 if i%cols==0 else VW*3//4,
                      iy + 30, VW//2 - 40, 72,
                      border_col=border, alpha=160 if unlocked else 80)
            status = "[*]" if unlocked else "[ ]"
            render_text(surf, f"{status}  {title}", 18, col,
                        (VW//4 if i%cols==0 else VW*3//4), iy + 16, bold=True)
            render_text(surf, desc, 13, P["text_dim"] if not unlocked else P["text"],
                        (VW//4 if i%cols==0 else VW*3//4), iy + 40)

        self.back_btn.draw(surf, P["gray"])

# ======================================================
#  MAIN APPLICATION
# ======================================================
class App:
    def __init__(self):
        pygame.init()
        self.settings = Settings.load()
        set_theme(self.settings.theme)

        # Display
        flags = pygame.SCALED | pygame.RESIZABLE
        if self.settings.fullscreen:
            flags |= pygame.FULLSCREEN
        self.screen = pygame.display.set_mode((VW, VH), flags)
        pygame.display.set_caption("Ping Pong")

        # Virtual surface (always VWxVH)
        self.vsurf = pygame.Surface((VW, VH))

        self.clock    = pygame.time.Clock()
        self.audio    = Audio(self.settings)
        self.achieve  = Achievements()
        self.trans    = Transition()
        self.trans.fade_in()

        # Scenes
        self.scene: Scene = Scene.MAIN_MENU
        self.menu_scene    = MainMenu(self.settings, self.audio)
        self.settings_scene: Optional[SettingsScene] = None
        self.howto_scene:    Optional[HowToPlay]     = None
        self.game_scene:     Optional[GameScene]     = None
        self.pause_scene:    Optional[PauseScene]    = None
        self.match_end:      Optional[MatchEndScene] = None
        self.achieve_scene:  Optional[AchievementsScene] = None

        # Saved game surface for pause overlay
        self._game_snapshot: Optional[pygame.Surface] = None

        self._t    = 0.0
        self._mode: Optional[GameMode] = None

        print("[App] Ping Pong started.")
        print(f"[App] Virtual canvas: {VW}x{VH}, FPS cap: {FPS_CAP}")

    # -- SCENE TRANSITIONS -----------------------------
    def _go(self, scene: Scene, cb=None):
        def _switch():
            self.scene = scene
            self.trans.fade_in()
            if cb:
                cb()
        self.trans.fade_out(_switch)

    def _start_game(self, mode: GameMode):
        self._mode = mode
        set_theme(self.settings.theme)
        self.game_scene = GameScene(self.settings, self.audio, mode, self.achieve)
        self.pause_scene = PauseScene(self.settings, self.audio)
        self._go(Scene.GAME)

    def _restart_game(self):
        self._start_game(self._mode)

    # -- MAIN LOOP -------------------------------------
    def run(self):
        running = True
        while running:
            dt = min(self.clock.tick(FPS_CAP) / 1000.0, 0.05)
            self._t += dt

            # --- Events ---
            mouse_pos   = pygame.mouse.get_pos()
            win_size    = self.screen.get_size()
            # Scale mouse to virtual coords
            sx = VW / max(1, win_size[0])
            sy = VH / max(1, win_size[1])
            vm = (int(mouse_pos[0] * sx), int(mouse_pos[1] * sy))

            mouse_click = False
            mouse_held  = pygame.mouse.get_pressed()[0]
            keys        = pygame.key.get_pressed()
            keys_just: List[int] = []

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    running = False
                elif ev.type == pygame.KEYDOWN:
                    keys_just.append(ev.key)
                    if ev.key == pygame.K_f:
                        self.settings.show_fps = not self.settings.show_fps
                    if ev.key == pygame.K_t and self.scene == Scene.GAME:
                        themes = ["NEON", "CLASSIC", "SYNTHWAVE"]
                        idx = themes.index(self.settings.theme) if self.settings.theme in themes else 0
                        self.settings.theme = themes[(idx+1) % len(themes)]
                        set_theme(self.settings.theme)
                elif ev.type == pygame.MOUSEBUTTONDOWN and ev.button == 1:
                    mouse_click = True

            # --- Update & draw by scene ---
            quality = self.settings.quality

            if self.scene == Scene.MAIN_MENU:
                result = self.menu_scene.update(dt, vm, mouse_click, keys_just)
                self.menu_scene.draw(self.vsurf, quality)
                if result:
                    if result == "single":
                        self._go(Scene.GAME, lambda: self._start_game(GameMode.SINGLE))
                    elif result == "two":
                        self._go(Scene.GAME, lambda: self._start_game(GameMode.TWO_PLAY))
                    elif result == "training":
                        self._go(Scene.GAME, lambda: self._start_game(GameMode.TRAINING))
                    elif result == "settings":
                        self.settings_scene = SettingsScene(self.settings, self.audio)
                        self._go(Scene.SETTINGS)
                    elif result == "howtoplay":
                        self.howto_scene = HowToPlay(self.settings, self.audio)
                        self._go(Scene.HOW_TO_PLAY)
                    elif result == "quit":
                        running = False

            elif self.scene == Scene.SETTINGS:
                result = self.settings_scene.update(dt, vm, mouse_click, mouse_held, keys_just)
                self.settings_scene.draw(self.vsurf, quality)
                if result == "back":
                    self._go(Scene.MAIN_MENU)

            elif self.scene == Scene.HOW_TO_PLAY:
                result = self.howto_scene.update(dt, vm, mouse_click, keys_just)
                self.howto_scene.draw(self.vsurf, quality)
                if result == "back":
                    self._go(Scene.MAIN_MENU)

            elif self.scene == Scene.GAME:
                if pygame.K_ESCAPE in keys_just:
                    # Snapshot current game frame for pause overlay
                    self._game_snapshot = self.vsurf.copy()
                    self._go(Scene.PAUSED)

                if self.game_scene:
                    self.game_scene.handle_input(keys, dt)
                    result = self.game_scene.update(dt)
                    self.game_scene.draw(self.vsurf, quality)
                    self.achieve.update(dt)
                    self.achieve.draw(self.vsurf)

                    if result == "match_end":
                        me = MatchEndScene(
                            self.settings, self.audio,
                            self.game_scene.stats,
                            self.game_scene.p1,
                            self.game_scene.p2,
                            self._mode,
                            self.achieve
                        )
                        self.match_end = me
                        self._go(Scene.MATCH_END)

            elif self.scene == Scene.PAUSED:
                if self.pause_scene and self.game_scene:
                    result = self.pause_scene.update(dt, vm, mouse_click, keys_just)
                    snap = self._game_snapshot or self.vsurf
                    self.pause_scene.draw(snap, self.vsurf, quality)
                    if result == "resume":
                        self._go(Scene.GAME)
                    elif result == "restart":
                        self._go(Scene.GAME, self._restart_game)
                    elif result == "settings":
                        self.settings_scene = SettingsScene(self.settings, self.audio)
                        self._go(Scene.SETTINGS)
                    elif result == "menu":
                        self._go(Scene.MAIN_MENU)

            elif self.scene == Scene.MATCH_END:
                if self.match_end:
                    result = self.match_end.update(dt, vm, mouse_click, keys_just)
                    self.match_end.draw(self.vsurf, quality)
                    if result == "again":
                        self._go(Scene.GAME, self._restart_game)
                    elif result == "menu":
                        self._go(Scene.MAIN_MENU)

            # Transition overlay
            self.trans.update(dt)
            self.trans.draw(self.vsurf)

            # CRT
            if self.settings.crt:
                draw_crt(self.vsurf)

            # FPS
            if self.settings.show_fps:
                fps = int(self.clock.get_fps())
                col = P["green"] if fps >= 55 else (P["gold"] if fps >= 30 else P["red"])
                f = Fonts.get(16, True)
                ft = f.render(f"FPS: {fps}", True, col)
                self.vsurf.blit(ft, (8, VH - 22))

            # Scale & flip
            scaled = pygame.transform.scale(self.vsurf, self.screen.get_size())
            self.screen.blit(scaled, (0, 0))
            pygame.display.flip()

        # Cleanup
        self.settings.save()
        print("[App] Settings saved. Goodbye!")
        pygame.quit()
        sys.exit(0)

# ======================================================
#  ENTRY POINT
# ======================================================
def main():
    """
    PING PONG
    ---------------------
    pip install pygame
    python pong_ultra.py

    Controls:
      Player 1  : W / S
      Player 2  : ^ / v
      ESC       : Pause
      F         : FPS toggle
      T         : Theme cycle (in-game)
      Mouse     : Full UI navigation
    """
    print("=" * 60)
    print("  PING PONG")
    print("  pip install pygame  ->  python pong_ultra.py")
    print("  Controls: W/S  |  UP/DN  |  ESC=Pause  |  F=FPS  |  T=Theme")
    print("=" * 60)

    try:
        app = App()
        app.run()
    except KeyboardInterrupt:
        print("\n[App] Interrupted by user.")
        pygame.quit()
        sys.exit(0)
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")
        import traceback
        traceback.print_exc()
        pygame.quit()
        sys.exit(1)

if __name__ == "__main__":
    main()