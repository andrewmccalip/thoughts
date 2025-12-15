# Space Datacenters: Orbital vs Terrestrial Economics

> *"It might not be rational. But it might be physically possible."*

An interactive first-principles cost analysis comparing orbital solar power satellites to terrestrial natural gas for datacenter capacity. Built by [Andrew McCalip](https://twitter.com/andrewmccalip).

![Flask](https://img.shields.io/badge/Flask-2.2.3-green?logo=flask)
![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python)
![License](https://img.shields.io/badge/License-MIT-yellow)
![Status](https://img.shields.io/badge/Status-Production%20Ready-blue)

---

## 🎯 What Is This?

This is an interactive economic model that asks a simple question: **Can you make space-based commodity compute cost-competitive with the cheapest terrestrial alternative?**

Instead of hand-waving about "the sun being huge" or "space being big," this tool lets you manipulate the actual variables and see what assumptions need to be true for orbital compute to make economic sense.

### Key Features

- **Interactive Sliders**: Adjust launch costs, satellite hardware costs, specific power, gas prices, PUE, and dozens more parameters
- **Real-Time Calculations**: See cost breakdowns, LCOE, and engineering outputs update instantly
- **Thermal Analysis**: Full bifacial panel thermal model with equilibrium temperature calculations
- **Mobile Responsive**: Works on desktop and mobile with adaptive layouts
- **First-Principles Physics**: Solar flux, Stefan-Boltzmann radiation, cell degradation, view factors
- **Transparent Math**: Formulas are implemented directly in `static/js/math.js`

---

## 📊 The Model

### Orbital Solar
- Starlink V2 Mini heritage bus as reference point
- Configurable specific power (3-75 W/kg)
- Launch costs from theoretical floor ($20/kg) to Falcon 9 ($2,940/kg)
- Cell degradation, GPU failure rates, NRE costs
- Thermal equilibrium calculations for bifacial panels

### Terrestrial (On-Site CCGT)
- H-Class combined cycle gas turbines
- 5-bucket capex model: Power Gen, Electrical, Mechanical, Civil/Shell, Network
- Fuel costs tied to natural gas prices
- PUE and capacity factor adjustments

---

## Verification

Quick verification scripts live in `temp/` and mirror the JavaScript model.

## 🛠️ Tech Stack

```
├── Flask 2.2.3          # Web framework
├── Gunicorn 20.1.0      # Production WSGI server
├── Jinja2               # Templating
├── KaTeX                # Math rendering
├── Vanilla JS           # No framework bloat
└── CSS Custom Props     # Theming & responsive design
```

---

## 🚀 Quick Start

### Local Development

```bash
# Clone the repo
git clone https://github.com/andrewmccalip/thoughts.git
cd thoughts

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Unix/Mac)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py
```

Visit `http://localhost:5000` in your browser.

### Docker

```bash
# Build the image
docker build -t space-datacenters .

# Run the container
docker run -p 8080:8080 space-datacenters
```

Visit `http://localhost:8080` in your browser.

---

## 📁 Project Structure

```
thoughts/
├── app.py                    # Flask application
├── requirements.txt          # Python dependencies
├── Dockerfile               # Container configuration
│
├── audits/                  # Archived review artifacts
├── static/
│   ├── css/
│   │   └── style.css        # All styling (2400+ lines)
│   ├── js/
│   │   ├── math.js          # Cost model calculations
│   │   └── main.js          # UI controller & interactions
│   └── references.json      # Citation data
│
├── templates/
│   ├── index.html           # Landing page
│   ├── space-datacenters.html  # Main analysis page
│   └── (none)
│
├── reports/                 # Research notes
└── temp/                    # Development scripts
```

---

## 🔧 Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server port (Docker) |

---

## 📐 The Math

### Orbital Cost Model

```
Total Cost = Hardware + Launch + Ops + GPU Replacement + NRE

Hardware = $/W × Initial Capacity (degradation-adjusted)
Launch = $/kg × Total Mass
Mass = Initial Capacity / Specific Power (W/kg)
```

### Thermal Equilibrium

```
T_eq = [ΣQ_in / (σ·A·ε_tot) + T_space⁴]^¼

Where:
- Q_in = Q_solar + Q_earthIR + Q_albedo + Q_heatloop
- σ = Stefan-Boltzmann constant
- ε_tot = ε_pv + ε_rad (bifacial)
```

### LCOE Comparison

```
LCOE = Total Cost / Energy Output ($/MWh)

Energy = Capacity × Hours × Capacity Factor
```

---

---

## 📝 Key Findings

From the analysis (with default assumptions):

1. **It's not obviously stupid** — The physics doesn't immediately kill it
2. **The economics are savage** — Currently 3-4x more expensive than terrestrial
3. **Vertical integration is everything** — Margin stacking kills external procurement
4. **One organization is positioned** — SpaceX's integration advantage is the whole ballgame
5. **The math is explicit** — Formulas are in `static/js/math.js`

## 🤝 Contributing

Found an error in the model? Disagree with an assumption? **Good.**

1. Fork the repo
2. Run the numbers yourself
3. Open a PR with your corrections
4. Include sources

The goal is to drag the conversation back to first principles—assumptions you can point at and outputs you can sanity-check.

---

## 📜 License

MIT License — Do whatever you want with it.

---

## 📬 Contact

**Andrew McCalip**
- Twitter: [@andrewmccalip](https://twitter.com/andrewmccalip)
- GitHub: [andrewmccalip](https://github.com/andrewmccalip)

---
