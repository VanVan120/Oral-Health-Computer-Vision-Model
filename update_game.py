import os

# Update HTML
html_path = "static/html/views/game.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

html = html.replace("<div class=\"score-box\">", "<div class=\"combo-box hidden\" id=\"comboDisplay\">x1</div>\n                    <div class=\"score-box\">")

instructions_old = "<span><strong>Tap or Click</strong> quickly on the falling green blobs (plaque) and candies (sugar) to destroy them.</span>"
instructions_new = "<span><strong>Tap or Click</strong> quickly on the falling green blobs (plaque) and candies (sugar) to destroy them. Use your ?? cursor!</span>"

instructions_old_2 = "<span>Each enemy destroyed gives you points. As your score increases, the enemies will fall faster!</span>"
instructions_new_2 = "<span><strong>Combos & Power-ups:</strong> String together rapid hits without missing to build a ?? Combo Multiplier! Watch out for the blue ?? Toothpaste to unleash a screen-clearing blast!</span>"

html = html.replace(instructions_old, instructions_new)
html = html.replace(instructions_old_2, instructions_new_2)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

# Update CSS
css_path = "static/css/game.css"
with open(css_path, "r", encoding="utf-8") as f:
    css = f.read()

# Make canvas cursor a toothbrush
new_cursor = """#gameCanvas {
    display: block;
    width: 100%;
    aspect-ratio: 4 / 3;
    background: radial-gradient(circle at center, #2e1b38 0%, #170d1e 100%);
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" style="font-size: 24px"><text y="24">??</text></svg>') 0 32, crosshair;
}

.combo-box {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    padding: 10px 20px;
    border-radius: 99px;
    color: white;
    font-weight: 900;
    border: 2px solid #fef3c7;
    font-size: 1.2rem;
    box-shadow: 0 0 15px rgba(245, 158, 11, 0.5);
    transition: transform 0.1s;
    display: flex;
    align-items: center;
    gap: 5px;
}
.combo-box.pop {
    transform: scale(1.3) rotate(-5deg);
}

.screen-flash {
    animation: flash 0.5s ease-out;
}
@keyframes flash {
    0% { filter: brightness(1); }
    10% { filter: brightness(5); }
    100% { filter: brightness(1); }
}
"""
css = css.replace("""#gameCanvas {
    display: block;
    width: 100%;
    /* Keep aspect ratio */
    aspect-ratio: 4 / 3;
    background: radial-gradient(circle at center, #2e1b38 0%, #170d1e 100%);
    cursor: crosshair;
}""", new_cursor)

with open(css_path, "w", encoding="utf-8") as f:
    f.write(css)
