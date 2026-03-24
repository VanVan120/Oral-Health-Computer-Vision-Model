import io

readme_path = "README.md"
with open(readme_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Table of Contents
toc_old = "- [?? Preventative Care Hub](#-preventative-care-hub)"
toc_new = "- [?? Preventative Care Hub](#-preventative-care-hub)\n- [?? Plaque Attack Minigame](#-plaque-attack-minigame)"

content = content.replace(toc_old, toc_new)

# 2. Update Key Features Table
feature_old = "| **?? Gamification & Engagement** | Score celebration popup with animated confetti, star ratings, emoji feedback, and level-based achievements (Starter ? Legendary) to encourage consistent oral hygiene. |"
feature_new = "| **?? Plaque Attack Game** | Built-in custom HTML5 2D Canvas action game to educate users through highly engaging, fast-paced bacteria-busting gameplay featuring combos, power-ups, and synthesized audio. |\n| **?? Gamification & Engagement** | Score celebration popup with animated confetti, star ratings, emoji feedback, and level-based achievements (Starter ? Legendary) to encourage consistent oral hygiene. |"

content = content.replace(feature_old, feature_new)

# 3. Add Plaque Attack details section right before Preventative Care Hub breakdown
section_insertion = """## ?? Plaque Attack Minigame

To increase patient engagement and make oral health education fun (especially for younger users), the platform features a fully custom-built 2D action game engineered entirely in vanilla JavaScript and HTML5 Canvas.

### Game Mechanics
*   **Dynamic Difficulty:** Bacteria (plaque, tartar, sugar) fall from the top of the canvas. The game dynamically increases the spawn rate and fall velocity as the user's score climbs.
*   **Combo System:** Stringing together rapid, accurate clicks builds a combo multiplier (`x2, x5, etc.`), rewarding precision without missing.
*   **Procedural Web Audio API:** All sound effects (hits, damage buzzes, power-up sweeps) are generated mathematically on the fly via the browser's `AudioContext`, requiring zero external asset loading.
*   **3D Lighting & Particle Engine:** The game features high-performance visual effects, including a glowing ambient dust background (`globalCompositeOperation`), CSS-styled glassmorphism UI, a 3D procedurally drawn gum-line, and responsive explosion particles when bacteria are destroyed.
*   **Special Power-ups:** Players can occasionally find special items like the *Toothpaste Bottle*, which triggers a screen-clearing AoE (Area of Effect) shockwave.

---

## ?? Preventative Care Hub"""

content = content.replace("## ?? Preventative Care Hub", section_insertion, 1)

with open(readme_path, "w", encoding="utf-8") as f:
    f.write(content)

print("README.md updated with Plaque Attack details.")
