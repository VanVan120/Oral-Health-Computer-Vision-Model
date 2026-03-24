import os

# --- 1. IMPROVE CSS (REMOVE TOOTHBRUSH, ENHANCE LOOKS) ---
css_path = "static/css/game.css"
new_css = """/* static/css/game.css */

.game-container {
    position: relative;
    max-width: 850px;
    margin: 0 auto;
    border-radius: 20px;
    overflow: hidden;
    /* Soft glowing border and shadow */
    box-shadow: 0 25px 50px -12px rgba(37, 99, 235, 0.4), 0 0 0 4px rgba(255, 255, 255, 0.1);
    background: #0f0c1b;
    border: 2px solid rgba(255, 255, 255, 0.2);
}

#gameCanvas {
    display: block;
    width: 100%;
    aspect-ratio: 4 / 3;
    /* Richer deep purple/blue nebula background */
    background: radial-gradient(circle at center, #1e152a 0%, #0a0612 100%);
    /* Replace toothbrush with sleek crosshair */
    cursor: crosshair;
}

.combo-box {
    background: linear-gradient(135deg, #f59e0b, #d97706);
    padding: 8px 24px;
    border-radius: 99px;
    color: white;
    font-weight: 800;
    border: 2px solid rgba(255, 255, 255, 0.3);
    font-size: 1.2rem;
    box-shadow: 0 4px 15px rgba(245, 158, 11, 0.4);
    transition: transform 0.15s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    display: flex;
    align-items: center;
    gap: 8px;
    backdrop-filter: blur(10px);
}
.combo-box.pop {
    transform: scale(1.2) rotate(3deg);
}

.screen-flash {
    animation: flash 0.4s ease-out;
}
@keyframes flash {
    0% { filter: brightness(1) contrast(1); }
    15% { filter: brightness(2) contrast(1.5); }
    100% { filter: brightness(1) contrast(1); }
}

.game-ui {
    position: absolute;
    top: 25px;
    left: 25px;
    right: 25px;
    display: flex;
    justify-content: space-between;
    pointer-events: none;
    font-family: 'Inter', sans-serif;
    text-shadow: 0 2px 8px rgba(0,0,0,0.8);
    z-index: 5;
}

.score-box, .health-box {
    background: rgba(15, 23, 42, 0.5);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    padding: 10px 24px;
    border-radius: 99px;
    color: white;
    font-weight: 700;
    border: 1px solid rgba(255, 255, 255, 0.15);
    font-size: 1.2rem;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}

.health-box .health-bar-container {
    width: 120px;
    height: 12px;
    background: rgba(0,0,0,0.6);
    border-radius: 99px;
    overflow: hidden;
    position: relative;
    box-shadow: inset 0 2px 4px rgba(0,0,0,0.5);
}

.health-bar-fill {
    height: 100%;
    background: linear-gradient(90deg, #34d399, #10b981);
    width: 100%;
    transition: width 0.4s cubic-bezier(0.4, 0, 0.2, 1), background-color 0.4s ease;
    border-radius: 99px;
}

.game-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 6, 18, 0.75);
    backdrop-filter: blur(8px);
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: white;
    z-index: 10;
    animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.hidden {
    display: none !important;
}

.game-title {
    font-size: 4.5rem;
    font-weight: 900;
    margin-bottom: 0.5rem;
    background: linear-gradient(to right, #60a5fa, #a78bfa, #f472b6);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    text-shadow: 0 10px 30px rgba(167, 139, 250, 0.3);
    letter-spacing: -1px;
}

.game-subtitle {
    font-size: 1.25rem;
    color: #cbd5e1;
    margin-bottom: 2.5rem;
    text-align: center;
    max-width: 70%;
    line-height: 1.6;
    font-weight: 500;
}

.btn-game {
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 14px 40px;
    font-size: 1.3rem;
    font-weight: 700;
    border-radius: 99px;
    cursor: pointer;
    box-shadow: 0 8px 25px rgba(99, 102, 241, 0.4);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    letter-spacing: 0.5px;
}

.btn-game:hover {
    transform: translateY(-4px) scale(1.05);
    box-shadow: 0 15px 35px rgba(99, 102, 241, 0.6);
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
}

.btn-game:active {
    transform: translateY(1px) scale(0.98);
}

.final-score {
    font-size: 3.5rem;
    font-weight: 900;
    color: #fcd34d;
    margin-bottom: 2rem;
    text-shadow: 0 4px 15px rgba(252, 211, 77, 0.3);
}
"""
with open(css_path, "w", encoding="utf-8") as f:
    f.write(new_css)


# --- 2. PATCH JS (IMPROVE GRAPHICS) ---
js_path = "static/js/ui/game_ui.js"
with open(js_path, "r", encoding="utf-8") as f:
    js_content = f.read()

# Replace drawGumLine with a 3D looking one
old_drawGumLine = """    function drawGumLine(ctx) {
        const topY = canvas.height - bottomZoneHeight;
        
        // Gum background
        ctx.fillStyle = '#db2777'; 
        ctx.beginPath();
        ctx.bezierCurveTo(0, topY - 20, canvas.width/2, topY + 20, canvas.width, topY - 10);
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.fill();

        // Draw Teeth
        const numTeeth = 8;
        const toothWidth = canvas.width / numTeeth;
        ctx.fillStyle = '#ffffff';
        ctx.strokeStyle = '#be185d'; 
        ctx.lineWidth = 3;

        for (let i = 0; i < numTeeth; i++) {
            const tx = i * toothWidth;
            ctx.beginPath();
            ctx.moveTo(tx + 5, canvas.height);
            ctx.quadraticCurveTo(tx + 5, topY - 10, tx + toothWidth/2, topY - 10);
            ctx.quadraticCurveTo(tx + toothWidth - 5, topY - 10, tx + toothWidth - 5, canvas.height);
            ctx.fill();
            ctx.stroke();
        }
    }"""

new_drawGumLine = """    function drawGumLine(ctx) {
        const topY = canvas.height - bottomZoneHeight;
        
        // Add subtle shadow behind the gums
        ctx.shadowColor = 'rgba(0, 0, 0, 0.5)';
        ctx.shadowBlur = 15;
        ctx.shadowOffsetY = -5;

        // 3D Gum background gradient
        const gumGradient = ctx.createLinearGradient(0, topY, 0, canvas.height);
        gumGradient.addColorStop(0, '#f472b6'); // Highlight edge
        gumGradient.addColorStop(0.2, '#be185d'); // Base pink
        gumGradient.addColorStop(1, '#831843'); // Deep shadow
        
        ctx.fillStyle = gumGradient; 
        ctx.beginPath();
        ctx.bezierCurveTo(0, topY - 15, canvas.width/2, topY + 15, canvas.width, topY - 10);
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.fill();

        ctx.shadowColor = 'transparent'; // Reset shadow
        ctx.shadowBlur = 0;

        // Draw 3D Teeth
        const numTeeth = 8;
        const toothWidth = canvas.width / numTeeth;
        
        for (let i = 0; i < numTeeth; i++) {
            const tx = i * toothWidth;
            const toothCenter = tx + toothWidth / 2;
            
            // 3D Tooth Gradient (Cylindrical lighting)
            const toothGradient = ctx.createLinearGradient(tx, 0, tx + toothWidth, 0);
            toothGradient.addColorStop(0, '#e2e8f0'); // Left shadow
            toothGradient.addColorStop(0.5, '#ffffff'); // Center highlight
            toothGradient.addColorStop(1, '#cbd5e1'); // Right shadow

            ctx.fillStyle = toothGradient;
            ctx.strokeStyle = '#9d174d'; 
            ctx.lineWidth = 2;

            ctx.beginPath();
            ctx.moveTo(tx + 6, canvas.height);
            // Smooth rounded top for tooth
            ctx.bezierCurveTo(tx + 6, topY - 15, toothCenter - toothWidth/4, topY - 20, toothCenter, topY - 20);
            ctx.bezierCurveTo(toothCenter + toothWidth/4, topY - 20, tx + toothWidth - 6, topY - 15, tx + toothWidth - 6, canvas.height);
            
            ctx.fill();
            
            // Add slight shine to tooth
            ctx.fillStyle = 'rgba(255,255,255,0.6)';
            ctx.beginPath();
            ctx.ellipse(toothCenter - 10, topY + 10, 5, 15, Math.PI/6, 0, Math.PI*2);
            ctx.fill();

            // Outline
            ctx.stroke();
        }
        
        // Front lip overhang for extra depth
        ctx.fillStyle = 'rgba(131, 24, 67, 0.4)';
        ctx.beginPath();
        ctx.bezierCurveTo(0, topY + 30, canvas.width/2, topY + 60, canvas.width, topY + 30);
        ctx.lineTo(canvas.width, canvas.height);
        ctx.lineTo(0, canvas.height);
        ctx.fill();
    }"""

js_content = js_content.replace(old_drawGumLine, new_drawGumLine)

# Replace drawBubbles with a glowing dust particle system
old_drawBubbles = """    function drawBubbles(ctx) {
        ctx.save();
        for(let i=0; i<bubbles.length; i++) {
            let b = bubbles[i];
            b.y -= b.speed;
            b.x += Math.sin(frameCount * b.wobble + b.offset) * 1;
            
            // Loop bubbles
            if(b.y < -20) { b.y = canvas.height + 20; b.x = randomRange(0, 800); }
            
            ctx.fillStyle = 'rgba(255, 255, 255, 0.05)';
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r, 0, Math.PI*2);
            ctx.fill();
        }
        ctx.restore();
    }"""

new_drawBubbles = """    function drawBubbles(ctx) {
        ctx.save();
        // Give ambient glowing dust feeling
        ctx.globalCompositeOperation = 'screen';
        for(let i=0; i<bubbles.length; i++) {
            let b = bubbles[i];
            b.y -= b.speed * 0.5;
            b.x += Math.sin(frameCount * b.wobble + b.offset) * 0.5;
            
            // Loop dust
            if(b.y < -20) { b.y = canvas.height + 20; b.x = randomRange(0, 800); }
            
            const gradient = ctx.createRadialGradient(b.x, b.y, 0, b.x, b.y, b.r * 2);
            gradient.addColorStop(0, 'rgba(167, 139, 250, 0.15)'); // Purple glow
            gradient.addColorStop(1, 'rgba(167, 139, 250, 0)');
            
            ctx.fillStyle = gradient;
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r * 2, 0, Math.PI*2);
            ctx.fill();
            
            // Inner core
            ctx.fillStyle = 'rgba(255, 255, 255, 0.1)';
            ctx.beginPath();
            ctx.arc(b.x, b.y, b.r * 0.5, 0, Math.PI*2);
            ctx.fill();
        }
        ctx.globalCompositeOperation = 'source-over';
        ctx.restore();
    }"""

js_content = js_content.replace(old_drawBubbles, new_drawBubbles)

with open(js_path, "w", encoding="utf-8") as f:
    f.write(js_content)

print("Game appearance improved and toothbrush cursor removed!")
