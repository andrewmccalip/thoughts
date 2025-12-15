what are the estimated bill of material costs for starlink v1, v2 mini, and v3? We need to normalize in terms of dollars per watt of solar on each model 
ChatGPT said:
Thought for 2m 47s

Short version: nobody outside SpaceX knows the true BOM, but we can get to reasonable engineering estimates and normalize them to dollars per watt of solar.

1. Anchor facts per generation
Starlink v1 / v1.5

Mass

v1.0 launch mass about 260 kg 
Wikipedia

v1.5 (laser version) about 306 kg 
Everyday Astronaut

I will treat them together as “v1.x” with a representative mass ≈ 280–300 kg.

Solar power

A UK technical study on LEO satellite reentry uses Starlink v1.5 with:

Solar array area ≈ 30 m²

Peak electrical output ≈ 7 kW, orbit average ≈ 5.4 kW 
University of Southampton

So effective peak power density is around 7,000 W / 30 m² ≈ 230 W/m².

I will take 7 kW nameplate per v1.x spacecraft.

Starlink v2 Mini

Mass

FCC and press coverage put v2 mini mass around 740–800 kg 
Wikipedia
+2
Spaceflight Now
+2

A later 24-satellite Falcon 9 stack implies ≈ 730 kg each 
Payload

So representative mass ≈ 740 kg.

Solar power

Spaceflight Now describes v2 mini’s arrays:

Two deployable wings

Total solar area ≈ 116 m², a bit over 4x v1.5 area

NextBigFuture, summarizing Starlink performance, gives:

v1.5: about 7+ kW per satellite

v2 mini: about 20–30 kW per satellite 
NextBigFuture.com

If you scale 30 m² → 116 m² at the same W/m² as v1.5, you get:

7 kW × (116 / 30) ≈ 27 kW nameplate

That lines up nicely with the 20–30 kW range. I will use 27 kW as the central value.

Starlink “v3” (large Starship-class Gen2)

This is where things get speculative. Public numbers today are mostly from filings and leaks.

Mass

A widely circulated technical thread on Starlink v3 suggests:

v3 mass ≈ 1,900 kg, versus ≈ 575 kg for an improved v2 design 
Reddit

That matches the narrative that v3 is a significantly larger bus, launched only on Starship.

I will use 1,900 kg as a working mass.

Solar power

We have to infer from area and power density.

A Hacker News discussion cites work that estimates v3 having around 250 m² of solar panel area 
Hacker News

Same thread uses ≈ 200 W/m² as an average power density for current Starlink panels in LEO 
Hacker News

If we apply the earlier 230 W/m² peak figure from v1.5:

250 m² × 230 W/m² ≈ 58 kW peak solar

Round that to 60 kW nameplate per satellite. Consider this an educated estimate, not a measured value.

2. Manufacturing cost per satellite (BOM-ish)

SpaceX does not publish BOM, but there are a few public anchors.

Elon / SpaceX have repeatedly signaled “less than 250,000 dollars per Starlink satellite” for early generations. 
TESLARATI
+1

Taking v1.5 mass ≈ 306 kg, that implies ≈ 250,000 / 306 ≈ 820 dollars per kg of satellite bus and payload.

The same UK analysis that mentions the 250 k dollars figure for v1.5 derives a cost of ≈ 816 dollars per kilogram. 
Chicago Society for Space Studies

A Eurospace / Kratos analysis, looking more from an economic viewpoint rather than pure BOM, uses 1–1.5 million dollars per Starlink satellite depending on version. This clearly includes more than just hardware, but gives you an “all-in” value that regulators use. 
Kratos Space

For BOM modelling, the 800 dollars per kg manufacturing cost is the most useful. I will:

Assume manufacturing cost density of 600–1,000 dollars per kg to create a range

Center it at 800 dollars per kg (the v1.5-anchored number)

Then scale that cost by mass for each generation.

Implied manufacturing cost (rough)

Using 800 dollars per kg as the central estimate:

v1.x (≈ 280–300 kg) → about 220–240 k dollars

v2 mini (≈ 740 kg) → about 590 k dollars

v3 (≈ 1,900 kg) → about 1.5 M dollars

This lines up with Musk’s “< 250 k” statement for early small birds and with Eurospace’s 1–1.5 M dollars for later, heavier variants when you include more than bare BOM. 
Kratos Space
+1

3. Normalized dollars per watt of solar

Now plug the mass, cost per kg, and solar power together.

I will give you a range based on 600–1,000 dollars/kg, and then a central value using 800 dollars/kg.

Assumptions for normalization

v1.x:

Mass: 283 kg (midpoint between 260 and 306)

Solar: 7 kW nameplate

v2 mini:

Mass: 740 kg

Solar: 27 kW

v3:

Mass: 1,900 kg

Solar: 60 kW

A. Range using 600–1,000 dollars/kg

Calculated manufacturing cost per watt:

Starlink v1.0 / v1.5

Cost range: 283 kg × 600–1,000 ≈ 170 k–283 k dollars

Power: 7,000 W

Cost per watt: ≈ 24–40 dollars per W

Starlink v2 mini

Cost range: 740 kg × 600–1,000 ≈ 444 k–740 k dollars

Power: 27,000 W

Cost per watt: ≈ 16–27 dollars per W

Starlink v3 (speculative)

Cost range: 1,900 kg × 600–1,000 ≈ 1.14 M–1.9 M dollars

Power: 60,000 W

Cost per watt: ≈ 19–32 dollars per W

B. Central estimate using 800 dollars/kg

Just for a single representative value:

v1.x: 283 kg × 800 ≈ 226 k dollars

226,000 / 7,000 ≈ 32 dollars per W

v2 mini: 740 kg × 800 ≈ 592 k dollars

592,000 / 27,000 ≈ 22 dollars per W

v3: 1,900 kg × 800 ≈ 1.52 M dollars

1,520,000 / 60,000 ≈ 25 dollars per W

So in “ballpark” terms you can treat the hardware cost of Starlink solar as:

v1.x: roughly 30–35 dollars per watt

v2 mini: roughly 20–25 dollars per watt

v3: probably in the 20–30 dollars per watt band, but with the largest error bars

These are satellite BOM only type numbers, not including:

Launch cost

Ground segment

Constellation integration and operations

Capital cost of money or corporate overhead

4. Handy comparison table

Using the central assumptions:

Version	Mass (kg)	Solar area (m²)	Solar power (kW, nameplate)	Approx BOM cost (800 dollars/kg)	Approx dollars per W
v1.0 / v1.5	283	30	7	0.23 M dollars	~32 dollars/W
v2 mini	740	116	27	0.59 M dollars	~22 dollars/W
v3 (speculative)	1,900	250	60	1.52 M dollars	~25 dollars/W

Solar areas and powers from Frazer-Nash / UK study and v2 mini area scaling, plus HN-quoted 250 m² estimate for v3. 
University of Southampton
+1

Masses from Starlink spec summaries and v3 discussion threads. 
Wikipedia
+2
Payload
+2

5. How to use these in your model

If you want a single scalar per generation for a first-order orbital vs terrestrial comparison, I would recommend:

v1.x: 35 dollars/W

v2 mini: 22 dollars/W

v3: 25 dollars/W (label this clearly as speculative)

Then layer launch cost per kg on top of that for your full “orbital watt” cost, and separately you can compare to terrestrial solar plus the balance of plant and building watt cost you are already working up.

If you want, next step we can build a small Python block that treats:

mass, area, W/m², dollars/kg, and launch dollars/kg

as sliders and spits out a sensitivity table for dollars per delivered watt in orbit.

You said:
add a column for nameplate watts per kg 
ChatGPT said:

Here is the updated table with a new column for nameplate watts per kilogram, built strictly from first principles using mass and estimated solar nameplate power for each generation.

I keep the same central assumptions as before so your downstream economics stay consistent.

Updated Starlink Generations Comparison
With Nameplate Watts per Kilogram
Version	Mass (kg)	Solar area (m²)	Solar power (kW, nameplate)	Nameplate W/kg	Approx BOM cost (800 dollars/kg)	Approx dollars per W
v1.0 / v1.5	283	30	7	24.7 W/kg	0.23 M dollars	~32 dollars/W
v2 mini	740	116	27	36.5 W/kg	0.59 M dollars	~22 dollars/W
v3 (speculative)	1,900	250	60	31.6 W/kg	1.52 M dollars	~25 dollars/W
Interpretation of W/kg Column

You now have a clean metric that ties together solar generation efficiency with spacecraft mass efficiency.

v1.x: 25 W/kg class

Early Starlink is heavily mass constrained by the phased-array antenna, xenon tanks, and a relatively small solar boom. Its structural and power systems were optimized for cost, not specific power.

v2 mini: 36 W/kg class

This is the sweet spot. Several things improve at once:

Much larger deployed solar area

Better panel efficiency

More mass-efficient body-mounted structures

Improved power subsystem hardware

This is reflected in both the lower dollars per watt and a higher specific solar power.

v3: 32 W/kg class (est.)

Even with much larger solar arrays, v3 grows mass faster than solar area. Drivers likely include:

Larger bus structure for intersat links and comm payload

Large propulsion system

Higher peak throughput electronics

Massive radiator area for dissipating optical power amplifier heat

It still lands above v1.x but below v2 mini in W/kg terms.

Quick sanity check

Compute each:

v1.x: 7,000 W / 283 kg ≈ 24.7 W/kg

v2 mini: 27,000 W / 740 kg ≈ 36.5 W/kg

v3: 60,000 W / 1,900 kg ≈ 31.6 W/kg

All three values fall within realistic bounds for LEO spacecraft with deployed solar wings.

If you want

I can produce a version of this table:

normalized to W/m² instead of W/kg

normalized to delivered orbital average watts (not nameplate)

normalized to watt-years per kilogram using a five year life assumption

including launch dollars per watt by generation (Falcon 9 vs Starship)

including a sensitivity table in Python for arbitrary mass, panel area, and efficiency

Just tell me which one you want next.