import matplotlib.pyplot as plt
import numpy as np

def midpoint_ellipse_hacker_bacteria(rx, ry, xc, yc, delay=0.005,
                                    n_bacteria=120, seed=7):
    rng = np.random.default_rng(seed)

    plt.ion()
    fig, ax = plt.subplots(figsize=(7.5, 4.8))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")

    # ---- VIEW ----
    pad = 30
    x_min, x_max = xc - rx - pad, xc + rx + pad
    y_min, y_max = yc - ry - pad, yc + ry + pad
    ax.set_aspect("equal")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(y_min, y_max)

    # ---- STYLE ----
    ax.grid(True, alpha=0.12)
    for spine in ax.spines.values():
        spine.set_color("#00ff66")
    ax.tick_params(colors="#00ff66")
    ax.set_title(">> MIDPOINT ELLIPSE // NEON BIO-SCANNER", color="#00ff66", fontsize=12)
    ax.set_xlabel("X", color="#00ff66")
    ax.set_ylabel("Y", color="#00ff66")

    # ---- BACKGROUND: "NEON BACTERIA" FALLING ----
    # bacteria positions + speed + size
    bx = rng.uniform(x_min, x_max, n_bacteria)
    by = rng.uniform(y_min, y_max, n_bacteria)
    bspeed = rng.uniform(0.6, 2.3, n_bacteria)  # fall speed
    bsize = rng.uniform(8, 60, n_bacteria)      # different blob sizes
    bwiggle = rng.uniform(0.6, 2.2, n_bacteria) # sideways wobble

    # two layers: glow + core
    bact_glow = ax.scatter(bx, by, s=bsize*2.3, c="#00ff66", alpha=0.06, linewidths=0)
    bact_core = ax.scatter(bx, by, s=bsize,    c="#00ff66", alpha=0.15, linewidths=0)

    # ---- SCANLINE ----
    scan = ax.axhline(y=y_min, color="#00ff66", alpha=0.18, linewidth=1.2)

    # ---- ELLIPSE POINTS ----
    X, Y = [], []

    # multi-layer glow for ellipse
    glow3 = ax.scatter([], [], s=220, c="#00ff66", alpha=0.03, marker=".", linewidths=0)
    glow2 = ax.scatter([], [], s=120, c="#00ff66", alpha=0.06, marker=".", linewidths=0)
    glow1 = ax.scatter([], [], s=55,  c="#00ff66", alpha=0.12, marker=".", linewidths=0)
    core  = ax.scatter([], [], s=12,  c="#00ff66", alpha=0.95, marker=".", linewidths=0)

    # ---- MIDPOINT ALGO ----
    x, y = 0, ry
    rx2, ry2 = rx * rx, ry * ry
    p1 = ry2 - (rx2 * ry) + (0.25 * rx2)

    dx = 2 * ry2 * x
    dy = 2 * rx2 * y

    frame = 0

    def update_background(frame):
        nonlocal bx, by

        # falling
        by -= bspeed

        # wiggle sideways (bacteria wobble)
        bx += 0.35 * np.sin(frame / 7.0 + bwiggle)

        # wrap when out of screen
        out = by < y_min
        by[out] = y_max + rng.uniform(0, 20, out.sum())
        bx[out] = rng.uniform(x_min, x_max, out.sum())

        # keep inside x-range
        bx = np.clip(bx, x_min, x_max)

        # pulsing alpha
        pulse = 0.10 + 0.08 * (0.5 + 0.5 * np.sin(frame / 9.0))

        bact_core.set_offsets(np.column_stack([bx, by]))
        bact_glow.set_offsets(np.column_stack([bx, by]))
        bact_core.set_alpha(pulse)
        bact_glow.set_alpha(pulse * 0.45)

        # scanline movement
        scan_y = y_min + (frame % int((y_max - y_min) + 1))
        scan.set_ydata([scan_y, scan_y])

    def update_ellipse(frame):
        # pulse brightness for neon ellipse
        pulse = 0.65 + 0.35 * (0.5 + 0.5 * np.sin(frame / 6.0))

        data = np.column_stack([X, Y])
        core.set_offsets(data)
        glow1.set_offsets(data)
        glow2.set_offsets(data)
        glow3.set_offsets(data)

        core.set_alpha(0.55 + 0.45 * pulse)
        glow1.set_alpha(0.08 + 0.10 * pulse)
        glow2.set_alpha(0.04 + 0.07 * pulse)
        glow3.set_alpha(0.02 + 0.04 * pulse)

    def maybe_glitch(frame):
        # occasional glitch: quick jitter of ellipse points
        if frame % 45 == 0 and len(X) > 30:
            jitter = rng.integers(-1, 2)
            # small shake of last ~40 points
            for i in range(max(0, len(X) - 40), len(X)):
                X[i] += jitter
                Y[i] -= jitter

    # -------- Region 1 --------
    while dx < dy:
        pts = [(xc + x, yc + y), (xc - x, yc + y),
               (xc + x, yc - y), (xc - x, yc - y)]
        for px, py in pts:
            X.append(px); Y.append(py)

        update_background(frame)
        maybe_glitch(frame)
        update_ellipse(frame)

        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(delay)

        if p1 < 0:
            x += 1
            dx += 2 * ry2
            p1 += dx + ry2
        else:
            x += 1
            y -= 1
            dx += 2 * ry2
            dy -= 2 * rx2
            p1 += dx - dy + ry2

        frame += 1

    # -------- Region 2 --------
    p2 = (ry2 * (x + 0.5) ** 2) + (rx2 * (y - 1) ** 2) - (rx2 * ry2)

    while y >= 0:
        pts = [(xc + x, yc + y), (xc - x, yc + y),
               (xc + x, yc - y), (xc - x, yc - y)]
        for px, py in pts:
            X.append(px); Y.append(py)

        update_background(frame)
        maybe_glitch(frame)
        update_ellipse(frame)

        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(delay)

        if p2 > 0:
            y -= 1
            dy -= 2 * rx2
            p2 += rx2 - dy
        else:
            y -= 1
            x += 1
            dx += 2 * ry2
            dy -= 2 * rx2
            p2 += dx - dy + rx2

        frame += 1

    plt.ioff()
    plt.show()


# RUN
midpoint_ellipse_hacker_bacteria(80, 50, 0, 0, delay=0.003, n_bacteria=150)
