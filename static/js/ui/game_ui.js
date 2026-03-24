/**
 * Plaque Attack Game Engine
 * Featuring Procedural Audio, Combos, Power-ups!
 */

document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('gameCanvas');
    if (!canvas) return; // Not on the game page

    const ctx = canvas.getContext('2d');
    
    // UI Elements
    const startScreen = document.getElementById('startScreen');
    const gameOverScreen = document.getElementById('gameOverScreen');
    const scoreDisplay = document.getElementById('scoreDisplay');
    const comboDisplay = document.getElementById('comboDisplay');
    const finalScoreDisplay = document.getElementById('finalScoreDisplay');
    const healthBar = document.getElementById('healthBar');
    const btnStartGame = document.getElementById('btnStartGame');
    const btnRestartGame = document.getElementById('btnRestartGame');

    // Audio Engine (Procedural Synthesis)
    let audioCtx = null;
    const playSound = (type) => {
        if (!audioCtx) return;
        const osc = audioCtx.createOscillator();
        const gainNode = audioCtx.createGain();
        osc.connect(gainNode);
        gainNode.connect(audioCtx.destination);
        
        const now = audioCtx.currentTime;
        
        if (type === 'hit') { // Pop sound
            osc.type = 'sine';
            osc.frequency.setValueAtTime(400, now);
            osc.frequency.exponentialRampToValueAtTime(800, now + 0.1);
            gainNode.gain.setValueAtTime(0.3, now);
            gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.1);
            osc.start(now);
            osc.stop(now + 0.1);
        } else if (type === 'damage') { // Buzz sound
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(150, now);
            osc.frequency.linearRampToValueAtTime(100, now + 0.2);
            gainNode.gain.setValueAtTime(0.4, now);
            gainNode.gain.linearRampToValueAtTime(0.01, now + 0.2);
            osc.start(now);
            osc.stop(now + 0.2);
        } else if (type === 'powerup') { // Sweep up
            osc.type = 'square';
            osc.frequency.setValueAtTime(200, now);
            osc.frequency.exponentialRampToValueAtTime(1200, now + 0.3);
            gainNode.gain.setValueAtTime(0.2, now);
            gainNode.gain.exponentialRampToValueAtTime(0.01, now + 0.3);
            osc.start(now);
            osc.stop(now + 0.3);
        }
    };

    // Game Variables
    let isPlaying = false;
    let animationId;
    let score = 0;
    let combo = 0;
    let health = 100;
    const maxHealth = 100;
    let frameCount = 0;
    
    // Entities
    let enemies = [];
    let particles = [];
    let shockwaves = [];
    let floatingTexts = [];
    let bubbles = []; // Background ambiance
    
    // Config
    const bottomZoneHeight = 80;
    let baseSpawnRate = 60;
    let currentSpawnRate = 60; 
    let baseSpeed = 2;

    // Helper functions for random
    const randomRange = (min, max) => Math.random() * (max - min) + min;
    const intRange = (min, max) => Math.floor(randomRange(min, max));

    // Initialize background bubbles
    for(let i=0; i<30; i++) {
        bubbles.push({
            x: randomRange(0, 800),
            y: randomRange(0, 600),
            r: randomRange(2, 8),
            speed: randomRange(0.5, 2),
            wobble: randomRange(0.01, 0.05),
            offset: randomRange(0, Math.PI*2)
        });
    }

    // Enemy Types (Added Toothpaste Powerup and better stats)
    const ENEMY_TYPES = [
        { type: 'plaque', color: '#84cc16', points: 10, radius: 26, speedMult: 1, symbol: '??', isPowerup: false },
        { type: 'sugar', color: '#f472b6', points: 20, radius: 22, speedMult: 1.4, symbol: '??', isPowerup: false },
        { type: 'tartar', color: '#fbbf24', points: 30, radius: 32, speedMult: 0.7, symbol: '??', isPowerup: false },
        { type: 'boss_plaque', color: '#ef4444', points: 50, radius: 42, speedMult: 1.3, symbol: '??', isPowerup: false },
        { type: 'toothpaste', color: '#38bdf8', points: 0, radius: 30, speedMult: 1.5, symbol: '??', isPowerup: true }
    ];

    class Enemy {
        constructor() {
            const rand = Math.random();
            let typeConfig;
            
            // Spawn logic
            if (rand > 0.96) typeConfig = ENEMY_TYPES[4];      // 4% Toothpaste
            else if (rand > 0.92) typeConfig = ENEMY_TYPES[3]; // 4% Boss
            else typeConfig = ENEMY_TYPES[intRange(0, 3)];     // Normal mix
            
            this.radius = typeConfig.radius;
            this.x = randomRange(this.radius, canvas.width - this.radius);
            this.y = -this.radius;
            this.speed = baseSpeed * typeConfig.speedMult + (score * 0.003); // Increase speed over time
            this.type = typeConfig.type;
            this.color = typeConfig.color;
            this.points = typeConfig.points;
            this.symbol = typeConfig.symbol;
            this.isPowerup = typeConfig.isPowerup;
            
            // Animation
            this.wiggleOffset = Math.random() * Math.PI * 2;
            this.wiggleSpeed = randomRange(0.02, 0.05);
            this.startX = this.x;
            this.rotation = 0;
            this.rotSpeed = randomRange(-0.05, 0.05);
        }

        update() {
            this.y += this.speed;
            this.x = this.startX + Math.sin(frameCount * this.wiggleSpeed + this.wiggleOffset) * (this.isPowerup ? 40 : 20);
            this.rotation += this.rotSpeed;
        }

        draw(ctx) {
            ctx.save();
            ctx.translate(this.x, this.y);
            
            // Add pulse effect to powerups/bosses
            let currentRadi = this.radius;
            if (this.isPowerup || this.type === 'boss_plaque') {
                currentRadi += Math.sin(frameCount * 0.1) * 3;
            }

            ctx.rotate(this.rotation);

            // Glow for powerup
            if(this.isPowerup) {
                ctx.shadowColor = this.color;
                ctx.shadowBlur = 15;
            }

            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(0, 0, currentRadi, 0, Math.PI * 2);
            ctx.fill();

            ctx.shadowBlur = 0; // reset
            ctx.strokeStyle = "rgba(0,0,0,0.3)";
            ctx.lineWidth = 3;
            ctx.stroke();
            
            // Inner symbol
            ctx.font = `${currentRadi * 0.9}px Arial`;
            ctx.textAlign = 'center';
            ctx.textBaseline = 'middle';
            ctx.fillText(this.symbol, 0, 2);
            
            ctx.restore();
        }
    }

    class Particle {
        constructor(x, y, color) {
            this.x = x;
            this.y = y;
            this.vx = randomRange(-5, 5);
            this.vy = randomRange(-5, 5);
            this.radius = randomRange(3, 8);
            this.color = color;
            this.alpha = 1;
            this.decay = randomRange(0.02, 0.06);
        }
        update() {
            this.x += this.vx;
            this.y += this.vy;
            this.alpha -= this.decay;
        }
        draw(ctx) {
            ctx.save();
            ctx.globalAlpha = Math.max(0, this.alpha);
            ctx.fillStyle = this.color;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
            ctx.fill();
            ctx.restore();
        }
    }

    class Shockwave {
        constructor(x, y, color) {
            this.x = x;
            this.y = y;
            this.r = 10;
            this.color = color;
            this.alpha = 1;
        }
        update() {
            this.r += 25; // Expanding speed
            this.alpha -= 0.03;
        }
        draw(ctx) {
            ctx.save();
            ctx.globalAlpha = Math.max(0, this.alpha);
            ctx.strokeStyle = this.color;
            ctx.lineWidth = 8 * this.alpha;
            ctx.beginPath();
            ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
            ctx.stroke();
            ctx.fillStyle = this.color;
            ctx.globalAlpha = Math.max(0, this.alpha * 0.2);
            ctx.fill();
            ctx.restore();
        }
    }

    class FloatingText {
        constructor(x, y, text, color, scale = 1) {
            this.x = x;
            this.y = y;
            this.text = text;
            this.color = color;
            this.alpha = 1;
            this.vy = -2;
            this.scale = scale;
        }
        update() {
            this.y += this.vy;
            this.alpha -= 0.02;
        }
        draw(ctx) {
            ctx.save();
            ctx.globalAlpha = Math.max(0, this.alpha);
            ctx.fillStyle = this.color;
            ctx.font = `bold ${20 * this.scale}px Inter, sans-serif`;
            ctx.textAlign = 'center';
            ctx.shadowColor = 'black';
            ctx.shadowBlur = 4;
            ctx.fillText(this.text, this.x, this.y);
            ctx.restore();
        }
    }

    function initGame() {
        if (!audioCtx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            audioCtx = new AudioContext();
        }
        if(audioCtx.state === 'suspended') audioCtx.resume();

        score = 0;
        combo = 0;
        health = maxHealth;
        enemies = [];
        particles = [];
        shockwaves = [];
        floatingTexts = [];
        frameCount = 0;
        baseSpeed = 2;
        currentSpawnRate = baseSpawnRate;
        
        updateUI();
        startScreen.classList.add('hidden');
        gameOverScreen.classList.add('hidden');
        
        if (animationId) cancelAnimationFrame(animationId);
        
        isPlaying = true;
        gameLoop();
    }

    function spawnParticles(x, y, color, count=15) {
        for (let i = 0; i < count; i++) {
            particles.push(new Particle(x, y, color));
        }
    }

    function triggerClearBoardPowerup(px, py) {
        playSound('powerup');
        shockwaves.push(new Shockwave(px, py, '#38bdf8')); // Cyan shockwave
        
        canvas.classList.add('screen-flash');
        setTimeout(() => canvas.classList.remove('screen-flash'), 500);

        // Score all enemies safely
        for(let i=enemies.length-1; i>=0; i--) {
            const e = enemies[i];
            if(!e.isPowerup) {
                spawnParticles(e.x, e.y, e.color, 5);
                score += e.points * (1 + Math.floor(combo / 5)); // apply current combo 
            }
        }
        enemies = []; // wipe them out
        combo += 5; // Free combo bonus
        floatingTexts.push(new FloatingText(canvas.width/2, canvas.height/2, "CLEANSING BLAST!", '#38bdf8', 2.5));
        updateUI();
    }

    function drawGumLine(ctx) {
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
    }

    function drawBubbles(ctx) {
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
    }

    function updateUI() {
        scoreDisplay.textContent = score;
        
        // Combo UI
        if(combo > 1) {
            comboDisplay.classList.remove('hidden');
            comboDisplay.innerHTML = `?? x${combo}`;
            // Add a little pop effect based on CSS animation trigger by toggling class
            comboDisplay.classList.remove('pop');
            void comboDisplay.offsetWidth; // trigger reflow
            comboDisplay.classList.add('pop');
            
            // Colors shift at high combos
            if(combo > 20) comboDisplay.style.background = 'linear-gradient(135deg, #ef4444, #b91c1c)';
            else if(combo > 10) comboDisplay.style.background = 'linear-gradient(135deg, #a855f7, #7e22ce)';
            else comboDisplay.style.background = 'linear-gradient(135deg, #f59e0b, #d97706)';
        } else {
            comboDisplay.classList.add('hidden');
        }

        // Health bar
        const healthPercent = Math.max(0, (health / maxHealth) * 100);
        healthBar.style.width = `${healthPercent}%`;
        if (healthPercent > 50) healthBar.style.backgroundColor = '#10b981';
        else if (healthPercent > 20) healthBar.style.backgroundColor = '#f59e0b';
        else healthBar.style.backgroundColor = '#ef4444';
    }

    function gameOver() {
        isPlaying = false;
        playSound('damage');
        finalScoreDisplay.innerHTML = `Score: <span style="color:#fff">${score}</span><br><span style="font-size: 1.5rem; color:#f59e0b;">Max Combo: x${combo}</span>`;
        gameOverScreen.classList.remove('hidden');
    }

    function processInput(clientX, clientY) {
        if (!isPlaying && !audioCtx) return; // Ignore if game over
        
        // Handle audio context initialization if blocked
        if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
        
        if (!isPlaying) return;

        const rect = canvas.getBoundingClientRect();
        const scaleX = canvas.width / rect.width;
        const scaleY = canvas.height / rect.height;
        const mouseX = (clientX - rect.left) * scaleX;
        const mouseY = (clientY - rect.top) * scaleY;

        let hit = false;

        for (let i = enemies.length - 1; i >= 0; i--) {
            const enemy = enemies[i];
            const dist = Math.hypot(mouseX - enemy.x, mouseY - enemy.y);
            
            if (dist < enemy.radius + 15) { // Generous hitbox for toothbrush
                enemies.splice(i, 1);
                hit = true;
                
                if (enemy.isPowerup) {
                    triggerClearBoardPowerup(enemy.x, enemy.y);
                } else {
                    playSound('hit');
                    combo++;
                    // Apply combo multiplier
                    let mult = 1 + Math.floor(combo / 5); // 0.2x multiplier scaling
                    let earned = enemy.points * mult;
                    score += earned;
                    
                    spawnParticles(enemy.x, enemy.y, enemy.color);
                    
                    let textScale = 1 + Math.min(combo * 0.05, 1);
                    floatingTexts.push(new FloatingText(enemy.x, enemy.y, `+${earned}`, (combo>10?'#fcd34d':'#34d399'), textScale));
                    
                    // Difficulty mechanic
                    if (score % 150 < 50 && currentSpawnRate > 15) {
                        currentSpawnRate -= 0.5; // Gradually spawn faster
                    }
                }
                
                updateUI();
                break; // Break loop so we only hit one per tap
            }
        }

        if (!hit) {
            // Miss! Break combo
            if(combo > 5) playSound('damage'); // mini penalty sound
            combo = 0; 
            updateUI();
            
            // Draw swipe/miss effect purely aesthetic
            ctx.strokeStyle = 'rgba(255, 255, 255, 0.4)';
            ctx.lineWidth = 4;
            ctx.beginPath();
            ctx.arc(mouseX, mouseY, 15, 0, Math.PI * 2);
            ctx.stroke();
        }
    }

    // Input Events
    canvas.addEventListener('mousedown', (e) => processInput(e.clientX, e.clientY));
    canvas.addEventListener('touchstart', (e) => {
        e.preventDefault();
        for (let i = 0; i < e.changedTouches.length; i++) {
            processInput(e.changedTouches[i].clientX, e.changedTouches[i].clientY);
        }
    }, { passive: false });

    function gameLoop() {
        if (!isPlaying) return;

        ctx.clearRect(0, 0, canvas.width, canvas.height);
        frameCount++;

        // Draw Sub-background
        drawBubbles(ctx);

        // Spawn
        if (frameCount % Math.floor(currentSpawnRate) === 0) enemies.push(new Enemy());

        // Draw Gums/Teeth
        drawGumLine(ctx);

        // Shockwaves (render behind enemies)
        for (let i = shockwaves.length - 1; i >= 0; i--) {
            const sw = shockwaves[i];
            sw.update();
            sw.draw(ctx);
            if (sw.alpha <= 0) shockwaves.splice(i, 1);
        }

        // Update & Draw Particles 
        for (let i = particles.length - 1; i >= 0; i--) {
            const p = particles[i];
            p.update();
            p.draw(ctx);
            if (p.alpha <= 0) particles.splice(i, 1);
        }

        // Update & Draw Enemies
        for (let i = enemies.length - 1; i >= 0; i--) {
            const enemy = enemies[i];
            enemy.update();
            enemy.draw(ctx);

            // Reached Bottom Zone
            if (enemy.y + enemy.radius > canvas.height - bottomZoneHeight + 20) {
                if(!enemy.isPowerup) {
                    health -= 15;
                    combo = 0; // Combo drops on hit
                    playSound('damage');
                    spawnParticles(enemy.x, enemy.y, '#ef4444', 20); 
                    floatingTexts.push(new FloatingText(enemy.x, enemy.y - 20, '-15', '#ef4444', 1.5));
                    
                    canvas.style.boxShadow = "inset 0 0 100px rgba(239, 68, 68, 0.8)";
                    setTimeout(() => canvas.style.boxShadow = "none", 150);

                    if (health <= 0) gameOver();
                }
                
                enemies.splice(i, 1);
                updateUI();
            }
        }

        // Texts (Top Layer)
        for (let i = floatingTexts.length - 1; i >= 0; i--) {
            const ft = floatingTexts[i];
            ft.update();
            ft.draw(ctx);
            if (ft.alpha <= 0) floatingTexts.splice(i, 1);
        }

        if (isPlaying) {
            animationId = requestAnimationFrame(gameLoop);
        }
    }

    // Wiring
    btnStartGame.addEventListener('click', initGame);
    btnRestartGame.addEventListener('click', initGame);
});
