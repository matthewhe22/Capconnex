import sqlite3, json

DB = "/opt/ghost/content/data/ghost.db"

html = r'''
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Smart EV Charging Manager | Capconnex Energy Intelligence</title>

<div class="capconnex-tesla-page">

<style>
.capconnex-tesla-page *,
.capconnex-tesla-page *::before,
.capconnex-tesla-page *::after { box-sizing: border-box; margin: 0; padding: 0; }

.capconnex-tesla-page {
  font-family: 'Mulish', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  background: #1a2d4a;
  color: #ffffff;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
  overflow-x: hidden;
}

.capconnex-tesla-page a { color: #c8a951; text-decoration: none; transition: opacity 0.2s; }
.capconnex-tesla-page a:hover { opacity: 0.8; }

.capconnex-tesla-page .container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 24px;
}

.capconnex-tesla-page .hero {
  position: relative;
  min-height: 70vh;
  display: flex;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 120px 24px 80px;
  background: linear-gradient(135deg, #1a2d4a 0%, #1a3d30 40%, #1a4d3a 70%, #1a2d4a 100%);
  overflow: hidden;
}

.capconnex-tesla-page .hero::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at 30% 50%, rgba(200, 169, 81, 0.06) 0%, transparent 60%),
              radial-gradient(circle at 70% 30%, rgba(200, 169, 81, 0.04) 0%, transparent 50%);
  animation: heroGlow 12s ease-in-out infinite alternate;
}

@keyframes heroGlow {
  0% { transform: translate(0, 0); }
  100% { transform: translate(-2%, -2%); }
}

.capconnex-tesla-page .hero-content {
  position: relative;
  z-index: 2;
  max-width: 900px;
}

.capconnex-tesla-page .hero-badge {
  display: inline-block;
  padding: 6px 18px;
  border: 1px solid rgba(200, 169, 81, 0.3);
  border-radius: 100px;
  font-size: 0.8rem;
  font-weight: 600;
  letter-spacing: 0.08em;
  text-transform: uppercase;
  color: #c8a951;
  margin-bottom: 24px;
}

.capconnex-tesla-page .hero h1 {
  font-size: clamp(2.4rem, 6vw, 4.2rem);
  font-weight: 700;
  line-height: 1.15;
  margin-bottom: 20px;
  letter-spacing: -0.02em;
}

.capconnex-tesla-page .hero h1 .gold { color: #c8a951; }
.capconnex-tesla-page .hero p {
  font-size: clamp(1rem, 2vw, 1.25rem);
  color: rgba(255,255,255,0.88);
  max-width: 700px;
  margin: 0 auto 36px;
  line-height: 1.7;
}

.capconnex-tesla-page .hero-cta-group {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

.capconnex-tesla-page .btn-primary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  background: #c8a951;
  color: #0a1628;
  font-weight: 700;
  font-size: 0.95rem;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.25s ease;
}

.capconnex-tesla-page .btn-primary:hover {
  background: #dbb85e;
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(200, 169, 81, 0.25);
}

.capconnex-tesla-page .btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 32px;
  background: transparent;
  color: #ffffff;
  font-weight: 600;
  font-size: 0.95rem;
  border: 1px solid rgba(255,255,255,0.2);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.25s ease;
}

.capconnex-tesla-page .btn-secondary:hover {
  border-color: #c8a951;
  color: #c8a951;
  transform: translateY(-2px);
}

.capconnex-tesla-page .stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background: rgba(255,255,255,0.06);
  border-radius: 16px;
  overflow: hidden;
  margin-top: -40px;
  margin-bottom: 80px;
  position: relative;
  z-index: 3;
  box-shadow: 0 8px 32px rgba(0,0,0,0.3);
}

.capconnex-tesla-page .stat-item {
  background: rgba(20, 35, 60, 0.9);
  backdrop-filter: blur(12px);
  padding: 36px 24px;
  text-align: center;
  transition: background 0.3s;
}

.capconnex-tesla-page .stat-item:hover {
  background: rgba(10, 22, 40, 0.7);
}

.capconnex-tesla-page .stat-number {
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 800;
  color: #c8a951;
  line-height: 1.1;
  margin-bottom: 8px;
  letter-spacing: -0.02em;
}

.capconnex-tesla-page .stat-label {
  font-size: 0.9rem;
  color: rgba(255,255,255,0.82);
  text-transform: uppercase;
  letter-spacing: 0.06em;
  font-weight: 500;
}

.capconnex-tesla-page .section {
  padding: 80px 0;
}

.capconnex-tesla-page .section-label {
  display: inline-block;
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 0.1em;
  text-transform: uppercase;
  color: #c8a951;
  margin-bottom: 12px;
}

.capconnex-tesla-page .section h2 {
  font-size: clamp(1.8rem, 3.5vw, 2.6rem);
  font-weight: 700;
  margin-bottom: 16px;
  letter-spacing: -0.015em;
}

.capconnex-tesla-page .section .section-desc {
  font-size: 1.05rem;
  color: rgba(255,255,255,0.82);
  max-width: 600px;
  margin-bottom: 48px;
  line-height: 1.7;
}

.capconnex-tesla-page .text-center { text-align: center; }
.capconnex-tesla-page .mx-auto { margin-left: auto; margin-right: auto; }

.capconnex-tesla-page .steps-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.capconnex-tesla-page .step-card {
  background: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 32px 24px;
  text-align: center;
  transition: all 0.3s ease;
  position: relative;
}

.capconnex-tesla-page .step-card:hover {
  border-color: rgba(200, 169, 81, 0.3);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}

.capconnex-tesla-page .step-number {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(200, 169, 81, 0.12);
  border: 1px solid rgba(200, 169, 81, 0.25);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1.1rem;
  color: #c8a951;
  margin: 0 auto 16px;
}

.capconnex-tesla-page .step-card h3 {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.capconnex-tesla-page .step-card p {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.55);
  line-height: 1.6;
}

.capconnex-tesla-page .formula-section {
  background: linear-gradient(180deg, rgba(200, 169, 81, 0.04) 0%, transparent 100%);
  border-top: 1px solid rgba(200, 169, 81, 0.18);
  border-bottom: 1px solid rgba(200, 169, 81, 0.18);
}

.capconnex-tesla-page .formula-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
  margin: 40px 0;
}

.capconnex-tesla-page .formula-node {
  background: rgba(10, 22, 40, 0.8);
  border: 1px solid rgba(200, 169, 81, 0.2);
  border-radius: 12px;
  padding: 20px 28px;
  text-align: center;
  min-width: 140px;
  transition: all 0.3s;
}

.capconnex-tesla-page .formula-node:hover {
  border-color: #c8a951;
  box-shadow: 0 0 20px rgba(200, 169, 81, 0.1);
}

.capconnex-tesla-page .formula-node .node-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.4);
  margin-bottom: 4px;
}

.capconnex-tesla-page .formula-node .node-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #c8a951;
}

.capconnex-tesla-page .formula-arrow {
  font-size: 1.5rem;
  color: #c8a951;
  opacity: 0.6;
}

.capconnex-tesla-page .formula-equals {
  font-size: 1.8rem;
  font-weight: 800;
  color: #c8a951;
  padding: 0 8px;
}

.capconnex-tesla-page .formula-result {
  background: linear-gradient(135deg, rgba(200, 169, 81, 0.15) 0%, rgba(200, 169, 81, 0.05) 100%);
  border: 1px solid #c8a951;
  border-radius: 12px;
  padding: 20px 32px;
  text-align: center;
  min-width: 180px;
}

.capconnex-tesla-page .formula-result .node-label {
  font-size: 0.7rem;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: rgba(255,255,255,0.78);
  margin-bottom: 4px;
}

.capconnex-tesla-page .formula-result .node-value {
  font-size: 1.1rem;
  font-weight: 700;
  color: #ffffff;
}

.capconnex-tesla-page .formula-details {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  max-width: 800px;
  margin: 32px auto 0;
}

.capconnex-tesla-page .formula-detail-item {
  background: rgba(255,255,255,0.03);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 10px;
  padding: 16px 20px;
  font-size: 0.88rem;
  color: rgba(255,255,255,0.88);
}

.capconnex-tesla-page .formula-detail-item strong {
  color: #c8a951;
  display: block;
  margin-bottom: 4px;
  font-size: 0.95rem;
}

.capconnex-tesla-page .benefits-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.capconnex-tesla-page .benefit-card {
  background: linear-gradient(180deg, rgba(255,255,255,0.04) 0%, rgba(255,255,255,0.01) 100%);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 32px 28px;
  transition: all 0.3s ease;
}

.capconnex-tesla-page .benefit-card:hover {
  border-color: rgba(200, 169, 81, 0.25);
  transform: translateY(-3px);
  box-shadow: 0 8px 30px rgba(0,0,0,0.2);
}

.capconnex-tesla-page .benefit-icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  background: rgba(200, 169, 81, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.3rem;
  margin-bottom: 16px;
}

.capconnex-tesla-page .benefit-card h3 {
  font-size: 1.05rem;
  font-weight: 700;
  margin-bottom: 8px;
}

.capconnex-tesla-page .benefit-card p {
  font-size: 0.85rem;
  color: rgba(255,255,255,0.55);
  line-height: 1.65;
}

.capconnex-tesla-page .cta-section {
  padding: 100px 0;
  text-align: center;
  background: linear-gradient(180deg, #0a1628 0%, #0d2a1e 50%, #0a1628 100%);
  position: relative;
  overflow: hidden;
}

.capconnex-tesla-page .cta-section::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 800px;
  height: 800px;
  transform: translate(-50%, -50%);
  background: radial-gradient(circle, rgba(200, 169, 81, 0.05) 0%, transparent 70%);
}

.capconnex-tesla-page .cta-section .container {
  position: relative;
  z-index: 2;
}

.capconnex-tesla-page .cta-section h2 {
  font-size: clamp(2rem, 4vw, 2.8rem);
  font-weight: 700;
  margin-bottom: 16px;
}

.capconnex-tesla-page .cta-section p {
  color: rgba(255,255,255,0.82);
  font-size: 1.05rem;
  max-width: 600px;
  margin: 0 auto 32px;
  line-height: 1.7;
}

.capconnex-tesla-page .cta-buttons {
  display: flex;
  gap: 16px;
  justify-content: center;
  flex-wrap: wrap;
}

@media (max-width: 1024px) {
  .capconnex-tesla-page .steps-grid { grid-template-columns: repeat(2, 1fr); }
  .capconnex-tesla-page .benefits-grid { grid-template-columns: repeat(2, 1fr); }
}

@media (max-width: 768px) {
  .capconnex-tesla-page .hero { min-height: 60vh; padding: 100px 20px 60px; }
  .capconnex-tesla-page .stats-row { grid-template-columns: 1fr; margin-top: 0; margin-bottom: 60px; }
  .capconnex-tesla-page .stat-item { padding: 28px 20px; }
  .capconnex-tesla-page .section { padding: 60px 0; }
  .capconnex-tesla-page .steps-grid { grid-template-columns: 1fr; }
  .capconnex-tesla-page .benefits-grid { grid-template-columns: 1fr; }
  .capconnex-tesla-page .formula-flow { flex-direction: column; gap: 8px; }
  .capconnex-tesla-page .formula-arrow { transform: rotate(90deg); }
  .capconnex-tesla-page .formula-details { grid-template-columns: 1fr; }
  .capconnex-tesla-page .cta-section { padding: 70px 0; }
}

@media (max-width: 480px) {
  .capconnex-tesla-page .hero h1 { font-size: 1.8rem; }
  .capconnex-tesla-page .hero p { font-size: 0.95rem; }
  .capconnex-tesla-page .hero-cta-group { flex-direction: column; align-items: center; }
  .capconnex-tesla-page .btn-primary,
  .capconnex-tesla-page .btn-secondary { width: 100%; justify-content: center; }
  .capconnex-tesla-page .formula-node,
  .capconnex-tesla-page .formula-result { min-width: 100px; padding: 16px 20px; }
}
</style>

<!-- ===== Hero ===== -->
<section class="hero">
  <div class="hero-content">
    <span class="hero-badge">⚡ Energy Intelligence</span>
    <h1>Smart EV Charging<br><span class="gold">Manager</span></h1>
    <p>Intelligent, automated EV charging for your Tesla. Powered by solar + battery — zero grid import, zero peak tariffs, zero touch.</p>
    <div class="hero-cta-group">
      <a href="#contact" class="btn-primary">Get Started →</a>
      <a href="#how-it-works" class="btn-secondary">How It Works</a>
    </div>
  </div>
</section>

<!-- ===== Stats Row ===== -->
<div class="container">
  <div class="stats-row">
    <div class="stat-item">
      <div class="stat-number">$0 Grid</div>
      <div class="stat-label">Peak Tariff Cost</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">100%</div>
      <div class="stat-label">Clean Energy</div>
    </div>
    <div class="stat-item">
      <div class="stat-number">2min</div>
      <div class="stat-label">Charge Cycle</div>
    </div>
  </div>
</div>

<!-- ===== How It Works ===== -->
<section class="section" id="how-it-works">
  <div class="container text-center">
    <span class="section-label">How It Works</span>
    <h2>Smart Charging in <span style="color:#c8a951;">Four Steps</span></h2>
    <p class="section-desc mx-auto">From sunrise to spirited drives — intelligent orchestration for your Tesla.</p>
    <div class="steps-grid">
      <div class="step-card">
        <div class="step-number">01</div>
        <h3>Solar + Battery Monitor</h3>
        <p>Alpha ESS reads solar generation, battery SOC, and household load in real time — every 2 minutes.</p>
      </div>
      <div class="step-card">
        <div class="step-number">02</div>
        <h3>Formula Engine</h3>
        <p>Available power = Solar + Battery − Household Load. If surplus &lt; 200W, charging pauses.</p>
      </div>
      <div class="step-card">
        <div class="step-number">03</div>
        <h3>Tesla Wall Connector</h3>
        <p>Adjusts charge current dynamically via API. Safe, seamless — no app needed.</p>
      </div>
      <div class="step-card">
        <div class="step-number">04</div>
        <h3>Recalculate &amp; Repeat</h3>
        <p>Every 2 minutes. Charges from 5A up to 32A. Zero grid import. Zero touch.</p>
      </div>
    </div>
  </div>
</section>

<!-- ===== Smart Charging Formula ===== -->
<section class="section formula-section">
  <div class="container text-center">
    <span class="section-label">The Science</span>
    <h2>Smart Charging <span style="color:#c8a951;">Formula</span></h2>
    <p class="section-desc mx-auto">Our algorithm balances solar, battery, and household demand — optimised for your Tesla.</p>

    <div class="formula-flow">
      <div class="formula-node">
        <div class="node-label">Solar Gen</div>
        <div class="node-value">☀️ 2,525 W</div>
      </div>
      <div class="formula-arrow">→</div>
      <div class="formula-node">
        <div class="node-label">Battery Max</div>
        <div class="node-value">🔋 +5,000 W</div>
      </div>
      <div class="formula-arrow">→</div>
      <div class="formula-node">
        <div class="node-label">Household Load</div>
        <div class="node-value">🏠 −312 W</div>
      </div>
      <div class="formula-equals">=</div>
      <div class="formula-result">
        <div class="node-label">To Your Tesla</div>
        <div class="node-value">⚡ 7,213 W → 16A</div>
      </div>
    </div>

    <div class="formula-details">
      <div class="formula-detail-item">
        <strong>☀️ Solar Generation</strong>
        Real-time PV yield from your rooftop — every watt goes into your Tesla, not the grid at 5¢ feed-in.
      </div>
      <div class="formula-detail-item">
        <strong>🔋 5,000 W Battery Buffer</strong>
        Alpha ESS discharge provides up to 5 kW. SOC ≥ 15% unlocks max discharge.
      </div>
      <div class="formula-detail-item">
        <strong>🏠 Non-EV Load Subtracted</strong>
        Household consumption (excluding Wall Connector) is deducted. Ensures charging never pulls from grid.
      </div>
      <div class="formula-detail-item">
        <strong>⚡ Zero-Grid Guarantee</strong>
        Final charge delivered with 0 W grid import. Saves $300+/year vs peak-rate charging.
      </div>
    </div>
  </div>
</section>

<!-- ===== Key Benefits ===== -->
<section class="section">
  <div class="container text-center">
    <span class="section-label">Why Capconnex</span>
    <h2>Key <span style="color:#c8a951;">Benefits</span></h2>
    <p class="section-desc mx-auto">Purpose-built for Tesla owners with solar and battery.</p>
    <div class="benefits-grid">
      <div class="benefit-card">
        <div class="benefit-icon">💰</div>
        <h3>Zero Peak Tariffs</h3>
        <p>Your Tesla charges entirely from solar + battery. Zero peak-rate electricity purchased — save $300+/year.</p>
      </div>
      <div class="benefit-card">
        <div class="benefit-icon">🌱</div>
        <h3>100% Solar Energy</h3>
        <p>Every kWh delivered to your Tesla is from stored solar. Maximise self-consumption over low-value feed-in.</p>
      </div>
      <div class="benefit-card">
        <div class="benefit-icon">🤖</div>
        <h3>Zero-Touch Automation</h3>
        <p>No apps, no timers. Set once and forget — adjusts itself every 2 minutes. Works while you sleep.</p>
      </div>
      <div class="benefit-card">
        <div class="benefit-icon">🏔</div>
        <h3>Peak Shaving</h3>
        <p>Shifts charging away from 3–9 PM peak window. Combined battery + solar cuts household peak demand by up to 40%.</p>
      </div>
      <div class="benefit-card">
        <div class="benefit-icon">🔋</div>
        <h3>Battery Health</h3>
        <p>Prevents deep discharge below 20% SOC. Intelligent limits extend Alpha ESS battery life by 2–3 years.</p>
      </div>
      <div class="benefit-card">
        <div class="benefit-icon">📊</div>
        <h3>Real-Time Dashboard</h3>
        <p>Live view of solar yield, battery levels, charge rate, and savings. Track carbon reduction in real time.</p>
      </div>
    </div>
  </div>
</section>

<!-- ===== CTA ===== -->
<section class="cta-section" id="contact">
  <div class="container">
    <h2>Ready to <span style="color:#c8a951;">Charge Your Tesla</span><br>for Free?</h2>
    <p>Let us configure your Alpha ESS + Tesla Wall Connector for zero-grid EV charging.</p>
    <div class="cta-buttons">
      <a href="mailto:Matthew.he@capconnex.com.au?subject=Smart%20EV%20Charging%20Manager%20Enquiry" class="btn-primary">Contact Us →</a>
      <a href="/contact" class="btn-secondary">Book a Demo</a>
    </div>
  </div>
</section>

</div>
'''

mobiledoc = json.dumps({
    "version": "0.3.1", "atoms": [], "markups": [], "sections": [[10, 0]],
    "cards": [["html", {"html": html}]]
})

plaintext = (
    "Smart EV Charging Manager by Capconnex Energy Intelligence. "
    "Intelligent automated EV charging for Tesla. Powered by solar + battery. "
    "Zero grid import, zero peak tariffs, zero touch. "
    "Integrates with Alpha ESS solar battery and Tesla Wall Connector. "
    "Real-time charge current adjustment every 2 minutes. "
    "Maximise solar self-consumption for Tesla EV charging. "
    "Australian property owners. capconnex.com.au"
)

code_head = (
    '<script type="application/ld+json">\n'
    '{\n'
    '  "@context": "https://schema.org",\n'
    '  "@type": "Product",\n'
    '  "name": "Smart EV Charging Manager",\n'
    '  "description": "Intelligent automated EV charging for Tesla owners. Zero-grid charging powered by solar and battery storage.",\n'
    '  "brand": {"@type": "Brand", "name": "Capconnex Energy Intelligence"},\n'
    '  "category": "EV Charging Management",\n'
    '  "audience": {"@type": "Audience", "name": "Tesla Owners with Solar + Battery"}\n'
    '}\n'
    '</script>\n'
    '<meta name="keywords" content="Tesla EV charging, solar EV charging, smart charging, EV charge management, Tesla Wall Connector, Alpha ESS, zero grid charging, Capconnex, energy intelligence, Australia">\n'
    '<meta name="robots" content="index, follow">\n'
)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""UPDATE posts SET
    title=?,
    html=?,
    mobiledoc=?,
    plaintext=?,
    codeinjection_head=?,
    updated_at=datetime('now')
WHERE slug=?""", (
    "Smart EV Charging Manager | Capconnex Energy Intelligence",
    html,
    mobiledoc,
    plaintext,
    code_head,
    "tesla-auto-charging"
))

# Update posts_meta for SEO fields
cur.execute("""UPDATE posts_meta SET
    meta_title=?,
    meta_description=?,
    og_title=?,
    og_description=?
WHERE post_id IN (SELECT id FROM posts WHERE slug=?)""", (
    "Smart EV Charging Manager — Zero-Grid Tesla Charging | Capconnex",
    "Smart EV Charging Manager by Capconnex. Intelligent automated EV charging for Tesla owners with solar + battery. Zero grid import, real-time 2-minute adjustment. Save $300+/year.",
    "Smart EV Charging Manager | Capconnex Energy Intelligence",
    "Intelligent, automated EV charging for your Tesla. Powered by solar + battery — zero grid import, zero peak tariffs.",
    "tesla-auto-charging"
))

conn.commit()
conn.close()
print("Page updated successfully!")
print(f"HTML length: {len(html)}")
