Skip to content
Chat history




You said:
help me brainstorm a structure in which tell this story in my article online. This will be for my interactive ingraphic on space datacenters. Lets work on an overall narrative structure 

Prompt:

I want to rewrite this narrative. We need to shape it into a story that portrays the writer as a reasonable engineer, good guy greg, trying to facilitate higher quality discussion. He’s slightly pissed, but ultimately his motivations are good. He’s the guy that brought you LK99, the rogue engineer.  



*the slightly artsy whimsical intro**

It may not be rational, but it might be physically possible. 

Or. 

Why we need more irrational billionaires 



So here’s the thing, I love space. I live and breath it. I am fortunate to brush the heavens with my wn metal and code.  I love AI and subscribe to maximum unbounded scale. I want to make the biggest bets. I grew up afraid we would never have another Apollo or Manhattan. I want to do the BigThing. 


Why I’m annoyed is that everyone has been trying to armchair the economics of a multi variable problem, and doing a terrible job at it.  Radiation is not hard. Cost of goods is not hard. Common guys, let’s up the quality of discourse. Run the freaking numbers. 

Here’s my idea. SpaceX is going public. Elon should have this big crazy barely possible goalpost, just like the big Tesla options grant. Give the man a trillion dollars of equity if he makes the world $5trillion. 

But here’s the deal, the goal should be physically achievable within a reasonable amount of time. 

The below analysis shows that probably only SpaceX could come close to making this work. If they go balls to the wall, they might get the economics within striking distance of a comparable terrestrial solutoion. 

Now, putting on my public markets hat, this might be a slightly mediocre use of capital. High risk for achieve an end result that has a fungible earthly alternative. GPUs are pretty darn happy living on the ground in Orgen.

However. The secondary knockdown benefits for humanity are probaby immeasurable. No sane person would attempt to do this. No rational person. 

There is beauty in the irrational. This is art. This is like   






The purpose of this analysis is to strip the orbital compute debate down to its governing parameter: the cost of hosting compute. If orbital power is going to support commodity compute, it must outperform the cheapest large-scale electricity available on Earth. This infographic builds that comparison from the ground up by pairing the most mass-efficient flight hardware flying today with a standard one gigawatt natural gas plant on a five-year horizo




Motivation and Framing
I am annoyed by the current quality of discourse around space-based datacenters.


The analysis quality is far below what would be expected from even a basic sell-side diligence exercise.


This is not an unknowable or speculative physics problem.


The governing physics are closed-form, well understood, and easy to bound.


Materials, orbits, power generation, and radiation physics are all known quantities.


Confident public claims in either direction are not credible without doing the math.


Invoking Stefan–Boltzmann alone is not analysis.


This fits on one page, but not on a napkin.



Personal Positioning
I want to come across as a rational, technically credible voice.


This is high-leverage, reputationally risky territory.


The goal is to influence the market, not hype it.


Ultimately, this positions me to one day raise a venture fund focused on rational space investments.


The tone should be slightly annoyed, slightly pissed-off PhD engineer.


Think The Big Short or Margin Call energy, but with a potentially positive outcome.



Core Thesis
We should put pen to paper before spending trillions of dollars.


There is a difference between rational enthusiasm and irrational enthusiasm.


If the numbers work, even barely, then it is worth running hard.


If they do not, the idea should not be insulated by vibes or confidence.


The correct first step is a basic sensitivity analysis.


The second step is a direct comparison against the existing terrestrial alternative.



Commodity Reality
This is a commodity business.


We are housing GPUs to do inference and possibly training.


The market already provides this service.


The only real question is cost competitiveness.


Can orbital compute provide the same commodity at a better price?


Everything else is secondary.



Findings and Implications
The system appears to be just barely possible.


It is mass-heavy and extremely constrained.


Even with aggressive launch cost reductions, it barely closes.


SpaceX is uniquely positioned.


Anyone not vertically integrated faces a much steeper economic cliff.


This does not mean others are incompetent.


Execution can be excellent and the economics can still be brutal.


The numbers are what the numbers are.



Broader Interpretation
The primary value may not be near-term cost competitiveness.


The secondary value may be accelerating humanity toward a spacefaring civilization.


Fiscally, this is aggressive and difficult.


Civilizationally, it is compelling.


This is exactly the type of project irrational capital should fund.


Billionaires exist to do the irrational things that move humanity forward.


Markets may not be comfortable with this framing.


That discomfort is itself informative.



Market and Incentives
If SpaceX goes public, shareholders should set extreme but physically achievable goalposts.


Similar to Tesla’s comp structure.


Barely possible goals attract a certain type of builder.


The market’s role is to define the goalposts and align incentives.


There is some degree of narrative pumping involved.


There is also real opportunity to create enormous value.



Analytical Lens
I think about engineered systems in terms of dollars per pound.


All NRE, labor, facilities, payroll, and overhead collapse into this metric.


This mirrors Elon’s “idiot index.”


Cost-per-pound cuts cleanly across complex sensitivity analyses.


This framing underpins industrialization.


The automobile-versus-cheese cost graphic captures this intuition.


Modern society is built on reducing cost per unit mass.



Overall Conclusion
This deserves real math, not vibes.


It is not obviously stupid.


It is not obviously brilliant.


It is barely feasible.


That makes it interesting.


The correct posture is skeptical, rigorous optimism.


Do the analysis first.


Then decide whether it is a goal worth running at.





Economics of Orbital vs Terrestrial DataCenters[← Andrew McCalip](/)
# Economics of Orbital vs
Terrestrial DataCenters

A first-principles cost model for 1 GW capacity over 5 years

Before we get nerd sniped by the shiny engineering details, it's worth asking the only question that matters. Why put compute in orbit at all? Why should a watt or a flop be more valuable 250 miles up than on the surface? What economic or strategic advantage justifies the effort required to run something as ordinary as matrix multiplication in low Earth orbit?

That "why" is almost missing from the public conversation. The discourse skips straight to implementation, as if the business case is obvious. It isn't. Most of the excitement is dri
ven by FOMO, aesthetic futurism, and a shallow reading of orbital mechanics rather than a clear value proposition.

If you can't answer the "why," everything downstream — engineering, economics, deployment — becomes speculation.**Real engineering starts with value, not hardware.**

The simplest way to ground the discussion is to take the most mass-efficient power hardware flying today, scale it to a 1 GW system, and tally the orbital bill. A Starlink V2 Mini–class bus is the right reference point. Its mass, solar area, and delivered power provide a real, flight-proven specific power baseline.

**Note:**This analysis is vibe-coded using publicly available information — a collation of public statements, filings, and reports. No proprietary data. These are Andrew's personal thoughts and do not represent the views of any company or organization.

*****analysis infographic block of text with sliders*******

## Why Put Compute in Orbit?

The purpose of this analysis is to strip the orbital compute debate down to its governing parameter: the cost of producing usable electrical power. All the arguments about solar flux, microgravity, radiation, or exotic orbital architectures reduce to a single number once you require a real economic comparison. If orbital power is going to support commodity compute, it must outperform the cheapest large-scale electricity available on Earth. This infographic builds that comparison from the ground up by pairing the most mass-efficient flight hardware flying today with a standard one gigawatt natural gas plant on a five-year horizon.

It's disappointing to see industry leaders blur this distinction and default to the big-numbers game. It isn't good enough to toss out a strawman like "we're going to run out of energy on Earth" and treat that as a business case.

> 
"How do we one day have data centers in space so that we can better harness the energy from the sun that is 100 trillion times more energy than what we produce on all of Earth today?"

— Sundar Pichai

> 
"You cannot build power plants of that scale—say, with 1 terawatt of continuous output—it's simply impossible. It must be done in space."

— Elon Musk, U.S.-Saudi Investment Forum Interview

These statements sound bold and visionary, but they skip the critical step. They assume the value rather than demonstrating it. They imply that because the sun is bright and space is big, the economics must work out in space's favor. That is not how engineering decisions are made. The only relevant question is whether a watt or a flop in orbit delivers more value per dollar than one on Earth. If the answer is no, the idea fails immediately, regardless of how inspiring the narrative sounds.

### Use Cases

To discuss compute in orbit, we should divide into two broad categories:

  - **Space-critical compute**— where latency or bandwidth make local processing essential.
  - **Everything else**— commodity workloads where you're competing with the AWS datacenters of the world.

#### Space-Critical Compute

The first category is the*steelman*argument for putting GPUs or CPUs in orbit. There's really only one scenario where putting compute in orbit makes sense: you're producing data faster than you can get it to the ground. Everything else collapses under basic geometry and link physics.

Satellites have no trouble generating enormous amounts of raw data. A modern 48MP camera shooting raw easily pushes**2–5 gigabits per second**continuously, and SAR systems run even higher; commercial X-band radars regularly exceed**5–8 Gbps**, with government systems going above**20 Gbps**internally. That's why a single 10-minute overpass can leave you sitting on hundreds of gigabytes that you now have to get off the spacecraft.

The problem is the downlink. A typical LEO satellite only sees a ground station for**8–12 minutes**per pass, and even a high-end Ka-band link taps out around**3–5 Gbps**under perfect conditions. Many operators never see that number, because antennas are shared, weather intervenes, and scheduling windows are rationed across dozens of customers. Commercial networks like KSAT and SSC frequently run near saturation; access often needs to be booked**days to weeks**in advance. This is why onboard or near-board pre-processing sounds appealing: turn terabytes into megabytes and send down only what matters.

On paper, that's the steelman.

Where it breaks is when you actually look at orbital distances. A satellite at 550 km altitude is five hundred fifty kilometers from the Earth's surface; that never changes. But in a dense constellation like Starlink, the nearest neighbor is usually**1,200–1,500 km**away once you account for plane spacing and relative phasing. That's not a hand-wave; Starlink Gen-2 shells have planes separated by**5–7 degrees**, and even within a plane, satellites sit roughly**1–2 degrees**apart, which works out to hundreds of kilometers of physical separation. The lowest slant-range ISL paths routinely exceed a thousand kilometers.

Now imagine trying to send that firehose of raw sensor data horizontally to an "orbital compute node" instead of vertically to Earth. If you posit four such nodes in LEO, spaced evenly around the planet, the average slant range from any imaging satellite to the nearest node is on the order of**4,000–5,000 km**. That's simply the chord length across a ring at 550 km altitude divided into quadrants. It's not a back-of-the-envelope trick—it's basic spherical geometry.

A link that long is dramatically harder to close. Beam divergence grows with distance; pointing stability demands increase; received power drops by nearly**20 dB**between a 1,000 km link and a 5,000 km one. Even laser ISLs, which Starlink uses at roughly**40–100 Gbps**over ~1,000–2,000 km paths, start falling apart fast when you extend to intercontinental-scale orbital distances. And unlike a ground station, which can house multi-meter-class dishes and powerful tracking systems, any orbital node is mass-constrained and thermally limited.

This leads to the uncomfortable conclusion: the closest, cheapest, highest-throughput place to send your data is still Earth. A 550 km downlink path into a hardened, fiber-backed ground station beats a 1,500–5,000 km sideways link into a spacecraft with tighter mass, power, and aperture constraints. And once you reach Earth, you're effectively already inside a hyperscale data center backbone.

So even this "best case" argument—the one that's supposed to justify orbital GPUs—fails once you run real numbers. The physics favors the planet. The infrastructure is already there. And the geometry ensures the sideways hop is always worse than the straight-down one.

### Generic Compute

Once you separate out the narrow class of missions that genuinely require local processing in space, you're left with everything else—the overwhelming majority of computing done on Earth. This is**generic, location-agnostic compute**. Model training, inference, indexing, recommender systems, search, storage, analytics, batch jobs. Ninety-nine point many nines percent of global compute demand lives here.

And this entire category shares one defining trait:**it does not care where it runs**. Its inputs and outputs are bits moving across fiber. It doesn't ask for altitude, vacuum, microgravity, or a laser link. It asks for**the cheapest and most reliable flops available**.

That's why hyperscale operators build wherever unit economics are optimized. AWS builds in Oregon, Iowa, Northern Virginia, and Sweden because that's where you get the right mix of cheap electricity, cheap land, cool climates, and dense fiber backbones. Crusoe, whose entire business model is squeezing flops out of stranded natural gas and surplus renewable power, pushes this to the logical extreme. Their message is the same: compute is a commodity pipeline, and the winner is the operator who delivers the lowest cost per flop.

So when someone proposes running generic compute in orbit, they are making an extraordinary claim: that**the full datacenter stack**—power generation, cooling, networking, hardware, structures, and operations—can be done*more cheaply in orbit*than inside a tilt-wall datacenter tied into a 200- to 500-MW substation.

A flop in orbit is not a special flop. A watt in orbit is not a special watt. They do not acquire new economic properties at 550 kilometers altitude. They cost what they cost.

This is why the economics are decisive. Commodity compute is not a physics problem. It is a cost competition with AWS, with Crusoe, with every hyperscale operator that already sits directly on top of cheap electricity and mature supply chains. If orbit wants to win, it must beat them on price. Not elegance. Not novelty.**Price.**

### The Economics

Before getting lost in hardware diagrams and thermal edge cases, the first step is to anchor everything to the governing economic question. If orbital compute is going to be more than an aesthetic idea, its unit economics must beat the cheapest terrestrial alternatives. That reduces the entire concept to one parameter:**cost per watt**. Everything else—solar arrays, radiators, thermal loops, GPUs, vacuum, microgravity—sits downstream of that number.

The cleanest way to evaluate this is to pick the most mass-efficient power hardware flying today, scale it to a 1-GW system, and compute the full orbital bill. A Starlink V2 Mini class bus is the logical reference point. Its mass, solar area, and delivered electrical power give a real, flight-proven specific power. Once those numbers are fixed, the required constellation mass and total hardware cost fall straight out of the math.

Launch cost is the next step. Pick a few reasonable scenarios—Falcon 9, early-Starship, mature-Starship—apply them to the total delivered mass, and you get the full orbital system cost.

Then compare that directly to a 1-GW natural-gas combined-cycle plant over the same five-year window, including capital cost, fuel burn, and O&M. This produces a clean, constrained, physics-bounded economic comparison with no hand-waving. The question it answers is simple:

**Is one watt generated and consumed in orbit cheaper than one watt generated and consumed on Earth?**

The numbers say no. Not marginally no. Even under optimistic Starship pricing, the launch bill alone overwhelms the entire five-year cost of a terrestrial NGCC plant. And that's before accounting for the additional mass and complexity required to run high-density compute hardware in vacuum.


*********
⚠ STOP ⚠ STOP ⚠ STOP ⚠ STOP ⚠ STOP ⚠ STOP ⚠
YOU ARE NOW ENTERING THE TECHNICAL ENGINEERING SECTION

If you skipped straight here looking for cool thermal diagrams and orbital mechanics—go back and read the economics section ***

The economics are the whole point. The technical challenges are interesting footnotes, but they don't matter if the unit economics don't close.**No amount of clever engineering fixes a 10× cost gap.**

Seriously. Go back up. The sliders are fun. Play with them.

### Technical Engineering Challenges

The governing constraint for orbital compute is**thermodynamics**. Terrestrial datacenters leverage convective cooling—dumping waste heat into the atmosphere or water sources, effectively using the planet as an infinite cold reservoir. In the vacuum of space, convection is impossible. Heat rejection relies exclusively on radiation.

Every object in space settles to an equilibrium temperature where absorbed power equals radiated power. If heat generation exceeds radiative capacity, the temperature rises until the $T^4$ term in the Stefan-Boltzmann law balances the equation:

$$\dot{Q}_{\text{rad}} = \varepsilon \sigma A T^4$$
The engineering challenge is ensuring this equilibrium temperature remains below the safe operating limits of silicon processors.

#### Energy Balance and Heat Rejection

To dimension the radiator surface, we must account for the total thermal load managed by the satellite bus. In this model, based on a Starlink-style bifacial architecture (PV on front, radiator on back), the system must reject the aggregate energy of two distinct paths:

  - **Incident Solar Flux:**The sun delivers $G_{\text{sc}} = 1361\;\text{W/m}^2$ (AM0). With a solar absorptivity $\alpha = 0.92$, the panel absorbs approximately $\sim 1250\;\text{W/m}^2$.
  - **Energy Partitioning:**
    - **Electrical Path ($\sim$22%):**High-efficiency cells convert $\sim 300\;\text{W/m}^2$ into electricity. This power drives the compute payload and is converted entirely back into heat by the processors. A liquid cooling loop collects this heat and returns it to the panel structure for rejection.
    - **Thermal Absorption ($\sim$70%):**The remaining $\sim 950\;\text{W/m}^2$ is not converted to electricity but is absorbed immediately as lattice heat (phonon generation) within the panel structure.
  - **Total Heat Load:**The radiator must reject the sum of both the immediate thermal absorption and the returned electrical waste heat—effectively**100% of the absorbed solar flux**.

This imposes a strict area density limit. High-power compute requires large collection areas, which inherently absorb large amounts of solar heat. The radiator must be sized to reject this aggregate load while maintaining an operating temperature below the junction limit.

#### Operating Temperature Limits

Modern AI accelerators (H100/B200 class) typically throttle at junction temperatures $T_j > 85\text{–}100\degree\text{C}$. To maintain a junction at 85°C, and accounting for the thermal gradient across cold plates and interface materials ($\Delta T \approx 10\degree\text{C}$), the radiator surface temperature $T_{\text{rad}}$ is constrained to approximately 75°C.

The model below calculates the equilibrium temperature for a bifacial array in a terminator orbit ($\beta = 90^\circ$). It accounts for solar flux, Earth IR ($\sim 237\;\text{W/m}^2$), and albedo. If the calculated equilibrium temperature $T_{\text{eq}}$ exceeds the target radiator temperature, the design fails.


Two parameters dominate the thermal environment of any LEO spacecraft: the**orbit beta angle (β)**and**Earth's albedo**. Understanding them is essential to sizing radiators and predicting equilibrium temperatures.

**Beta Angle (β)**is the angle between the orbital plane and the Sun vector. It determines how much time a satellite spends in sunlight versus shadow, and how the Sun's rays strike the spacecraft:

  - **β = 0°:**The orbital plane contains the Sun. The satellite experiences maximum eclipse time (~35% of each orbit in shadow) and the most extreme thermal cycling—baking in full sun, then plunging into Earth's shadow.
  - **β = 90°:**The orbital plane is perpendicular to the Sun vector—a "terminator orbit." The satellite rides the day-night boundary, seeing nearly continuous sunlight (~98%) with minimal thermal cycling. This is the coldest steady-state configuration because the sun strikes only the edge of the orbit, reducing direct heating while maintaining constant power generation.
  - **Intermediate values (60°–75°):**Represent seasonal extremes for sun-synchronous orbits. Lower beta angles increase both eclipse fraction and albedo loading from sunlit Earth below.

For orbital compute, high-beta (terminator) orbits are attractive: near-constant power, minimal battery mass, and the coldest achievable equilibrium temperature. The tradeoff is orbital slot availability and potential conjunction density.

**Earth Albedo**is the fraction of sunlight Earth reflects back into space; a practical global-average value is**ρ ≈ 0.30**(but it varies a lot with clouds and surface).

Thermally, albedo is “extra sunlight” added to any surface that can see Earth, roughly scaling with solar flux ×**ρ**× Earth view factor × absorptivity × area, and typically decreasing as**β**increases (less sunlit Earth in view). This is one reason high-beta/terminator-like geometries tend to run cooler.

*More analysis to come on thermal management, radiation hardening, and orbital mechanics constraints...*

[Follow on Twitter](https://twitter.com/AndrewMcCalip)
ChatGPT said:

Thought for 6s
Here’s a narrative structure that reads like a story (not a whitepaper), keeps you “reasonable engineer with good motives,” and lets the interactive infographic do the heavy lifting.

The spine
Arc: I want this to be true → people are hand-waving → here’s the one parameter that governs everything → steelman the best case → run the math → the result is “barely” → so what should we do about it?

You want the reader to feel: “He’s rooting for space, he’s not a hater, but he’s also not letting vibes win.”

Act 1: Hook, character, and the sin you’re fighting
1) Cold open: the artsy irrational thesis (10 seconds)
Goal: give permission to love the idea while admitting it might be dumb economically.

Options for the opener:

“It might not be rational. It might still be physically possible.”

“We don’t need more optimism. We need more math.”

“Irrational projects are how civilization levels up. But physics still collects rent.”

“Space datacenters are either the next cathedral or the next Theranos. The difference is a spreadsheet.”

2) Establish narrator: “I’m a space guy, and I’m trying to help”
Goal: lock in “good guy Greg,” not a snark account.

Be explicit about your bias in a disarming way:

You love space.

You love scale.

You want the BigThing to exist.

You are annoyed because the discourse is lazy, not because the ambition is.

Micro-beat: “I’m rooting for it. That’s why I’m being strict.”

3) Name the enemy: armchair economics on a multivariable system
Goal: define the problem without sounding superior.

Key line: “This is not unknowable. It’s bounded.”
Then list 4 things that are “closed form / estimable”: solar flux, cell efficiency, Stefan–Boltzmann, launch $/kg, datacenter $/W.

Put your first on-page promise:

“I’m going to steelman this.”

“I’m going to show assumptions.”

“I’m going to tell you what would change my mind.”

This is where the “rogue engineer LK99 energy” fits: you are willing to publish numbers and take arrows, but you are not claiming certainty.

Act 2: The governing parameter and the interactive model
4) The frame: reduce the entire debate to one number
Goal: get the reader to accept the rules of the game.

The rule: If it’s commodity compute, it’s a cost-per-watt race against Earth.
Everything else is a footnote until this closes.

Put this as a box:

If orbital power cannot beat cheap terrestrial watts, orbital commodity compute is dead on arrival.

If it can, then all the interesting engineering becomes worth doing.

5) Split the world into two use cases (your “fairness” credibility move)
Goal: show you are not straw-manning.

A. Space-critical compute (bandwidth-limited sensing, autonomy, tactical latency)
B. Generic compute (training, inference, batch) where location does not matter

Then do a clean bridge sentence:

“Category A is real and already justified. This article is about Category B, where the only honest question is price.”

6) The interactive infographic enters: “Let’s play the sliders”
Goal: make the reader participate so they feel ownership of the conclusion.

Interactive sequence (order matters):

Start with Earth baseline: NGCC $/W over 5 years (capex + fuel + O&M)

Orbit baseline: specific power (W/kg), $/kg to orbit, satellite $/kg, lifetime

Output: cost per delivered watt (and cost per kWh equivalent)

Make the UI teach the logic:

Big number on top: “All-in $/W (5-year)”

Under it: “This is what the sliders change.”

7) The “Good faith” section: assumptions, not secrets
Goal: protect yourself from “you picked numbers to win.”

Add a persistent drawer called Assumptions with:

ranges

sources later

and a “make it harder / easier” toggle (optimistic vs conservative presets)

Crucial tone: “If you hate any assumption, change it. The model is right there.”

8) Results: deliver the punchline without gloating
Goal: “barely possible” is your signature.

Deliver in three layers:

Base case: doesn’t close economically

Best case: only barely approaches

Who can do it: vertical integration matters (SpaceX-shaped advantage)

Then immediately add the humility brake:

“Execution can be excellent and still lose to physics + supply chain reality.”

Act 3: The technical section as a gated “nerd door”
You already have the “⚠ STOP ⚠” gate. Keep it. It’s good writing. Make it do two jobs:

prevent nerd-sniping

reinforce: economics first

9) Technical reality, presented as constraints not trivia
Goal: keep it first-principles, not a thermal textbook.

Make each technical subsection answer one question:

Thermal: “Can you reject 100% of absorbed solar plus payload heat while staying under silicon limits?”

Power: “How much area is required per kW, and what mass follows?”

Comms: “Do you actually need orbit compute, or does geometry make Earth cheaper anyway?”

Reliability/ops: “Who swaps failed GPUs? What is the implied spares mass?”

Each ends with a “so what” sentence tying back to $/W.

10) The philosophical turn: “irrational capital has a job”
Goal: you want to land somewhere uplifting without losing rigor.

This is where your “irrational billionaires” riff lives, but keep it grounded:

Markets optimize for near-term ROI.

Civilizational leaps often look stupid until they work.

It can be a mediocre trade financially and still be a huge win technologically.

Key framing: “This is art, but it must be physically and economically bounded.”

11) The incentive proposal: public markets goalposts
Goal: end with a constructive call, not just critique.

Your Tesla-comp style idea becomes:

If SpaceX is public, the comp plan should reward physically achievable, clearly measurable milestones.

Example milestones: delivered $/kg, on-orbit $/W, operational uptime, constellation MW.

Make it feel like governance, not pumping:

“Define the goalposts. Publish the metrics. Let reality score the narrative.”

“Reasonable engineer” voice guardrails
What to say often
“I want this to work.”

“Here is the steelman.”

“Change the assumptions and see what happens.”

“If I’m wrong, it will be wrong in a specific place.”

What to avoid
dunking on specific teams

implying anyone is stupid

saying “obvious” or “anyone who understands…”
Replace with: “the numbers are constrained” or “the physics is not negotiable.”

A recurring motif that works
“This fits on one page, but not on a napkin.”
Use it as a refrain each time you transition from vibes to math.

Page-level outline you can directly implement
Hero: title + 2-line hook + “I’m rooting for this, so I’m doing the math.”

The problem: discourse quality + why you built the model

Two use cases: space-critical vs commodity

The governing parameter: cost per watt

Interactive model: sliders + presets + assumptions drawer

Results: base case, best case, who can do it

Implications: what it means, what it does not mean

Tech section (gated): thermal, comms, reliability, ops

Irrational capital: why this still might be worth doing

Goalposts: how to align incentives if it goes public

What would change my mind: explicit falsifiers

Appendix: sources, derivations, units, version history

Two killer sections that increase trust
“What would change my mind” (add near the top)
Examples:

“If Starship delivers sustained <$X/kg to LEO with Y cadence.”

“If on-orbit specific power improves to >A W/kg including radiator mass.”

“If a credible architecture shows thermal closure at <T radiator with realistic view factors.”

“If terrestrial $/W moves materially (fuel price, capex, permitting).”

“Version history”
Put a changelog at the bottom. It screams intellectual honesty.

If you want, I can take your existing draft text and map each paragraph into this structure (keep your best lines, cut redundancies, and write the missing transitions so it reads like one continuous story).

You said:
This is awesome. Can you write the entire essay for me. Take your own tone, you don't have to borrow too much from my words, except for the opening bits that are a bit more punchy and artsy. 

we want to trend positive on spaceX, but also hold them accountable. We want to imply that it appears absolutely impossible for anyone else to do it. 

we want to keep the bit about irrational billionaires, that whole line of thinking is worth keeping. 
ChatGPT said:
It might not be rational.

It might still be physically possible.

And that combination is exactly how civilization upgrades itself.

I love space. I love the smell of “barely possible.” I love the idea that a small group of stubborn people can brute force a new industry into existence with metal, software, and a refusal to accept polite limits. I also love AI and the whole “unbounded scale” mindset. If you told me we could move a meaningful fraction of global compute off-planet in my lifetime, some irrational part of my brain would immediately start cheering.

That is why I’m annoyed.

The current discourse around “space datacenters” is wildly confident and wildly under-modeled. People are trying to armchair the economics of a brutally multivariable system and then speaking in absolutes. They are cherry-picking one physics fact, one sexy number, one dramatic quote, and calling it analysis.

Radiation is not hard. Cost modeling is not hard. The hard part is having the discipline to actually do it.

This essay is my attempt to raise the floor of the conversation. Not to dunk on anyone. Not to declare victory for or against the idea. Just to drag the debate back into the domain where engineering belongs: explicit assumptions, closed-form physics, sensitivity analysis, and a direct comparison against the real alternative on Earth.

If you want to be taken seriously in public markets, you do not get to skip the spreadsheet.

The core claim
If you are proposing space-based datacenters for commodity workloads, you are making one claim and only one claim:

You can host compute more cheaply in orbit than on Earth.

Not cooler. Not more inspiring. Not “more energy from the sun.” Not “bigger scale.” Cheaper.

Because the moment you leave the narrow category of “space-critical compute,” you are competing with hyperscalers who already sit on top of cheap land, cheap electrons, mature supply chains, and fiber networks that are boring only because they are devastatingly efficient.

A flop in orbit is not a special flop. A watt in orbit is not a special watt. They do not gain magical economic properties at 550 km altitude. They cost what they cost.

So we strip the debate down to its governing parameter:

Cost per watt.

Cost per watt of delivered electrical power that can be turned into heat inside GPUs, rejected by radiators, maintained for years, and operated at scale.

If you are building a space datacenter, you are not building “compute.” You are building the entire datacenter stack, except now every subsystem has to fly.

Power generation. Thermal rejection. Structure. Deployment. Attitude control. Communications. Operations. Spares. Reliability. Launch. Replacement cadence. Insurance. Everything.

That stack has to beat Earth on price.

That is the whole game.

Step zero: separate the real use case from the vibe use case
There are two fundamentally different categories of “compute in orbit,” and a lot of confusion comes from mixing them.

Category A: Space-critical compute
This is the steelman. This is real.

If you are producing data in space faster than you can ship it to the ground, onboard processing can be rational. Earth observation, SAR, hyperspectral imaging, missile warning, autonomy, tactical latency. You can easily create scenarios where you want to compress terabytes into megabytes before downlink, or where you need decisions made locally without waiting for a ground loop.

Compute is valuable here because it reduces bandwidth requirements or improves mission capability. In those cases you are not competing with AWS on cost per flop. You are buying capability.

This category already exists and will grow.

Category B: Generic compute
This is what most “space datacenter” conversations imply, whether they admit it or not.

Training, inference, indexing, recommender systems, batch processing, general purpose GPU farms. The stuff that makes up nearly all terrestrial compute demand.

This category does not care where it runs. It cares about price, uptime, and throughput. The physical location is just logistics.

If you propose moving this category to orbit, you are not proposing a new physics trick. You are proposing to win a commodity cost war against Earth.

So for the rest of this essay, we are talking about Category B.

The interactive infographic: what it is really doing
The infographic is not a fancy animation. It is an argument you can interrogate.

It does one thing: it takes a plausible, flight-proven “power hardware” baseline and scales it to a 1 GW system. Then it compares that orbital bill to a 1 GW terrestrial power alternative over a five-year horizon.

The reason to use 1 GW is not because anyone will build a 1 GW space datacenter tomorrow. It is because big round numbers force honesty. If your story only works at toy scale, it is not a story about industry. It is a story about a demo.

At a high level, the model has three blocks:

How many watts can you generate per kilogram in orbit?
This sets the orbital mass required for a given power level.

How many dollars does it cost to put that mass where it needs to go and keep it operating?
This includes launch and hardware.

What is the terrestrial benchmark?
A 1 GW terrestrial power plant plus the supporting infrastructure that makes commodity compute cheap.

Then the infographic asks the only question that matters:

Is one watt generated and consumed in orbit cheaper than one watt generated and consumed on Earth?

If the answer is no by a large factor, nothing else matters. Not thermal cleverness. Not orbital mechanics. Not vision. You can’t “engineer” your way out of an order-of-magnitude cost gap with narrative.

If the answer is yes, or even within striking distance, then the whole topic becomes legitimately interesting. Because now you are in a regime where execution, integration, and iteration speed can decide the outcome.

That is why the sliders exist. They are there to show you where the fulcrums are, and what would have to be true for the idea to close.

Why the discourse is broken
A lot of public conversation does this:

“The sun is huge.”

“Space is cold.”

“Launch will be cheap.”

“Therefore space datacenters will be inevitable.”

That is not analysis. That is a mood board.

The governing physics here are not exotic. They are closed-form and brutal:

Solar flux is a known constant to first order.

Solar cell efficiency is bounded by physics and manufacturing.

Waste heat must be rejected by radiation, which scales with 
T
4
T 
4
 .

Hardware masses and costs scale in predictable ways.

Launch cost is a lever, but it is not a magic wand.

You do not get to invoke Stefan–Boltzmann as a talisman. You have to actually close the heat balance under realistic operating temperatures and view factors.

You do not get to wave at “Starship” like it is a cheat code. You have to pick a $/kg, pick a cadence, pick a lifetime, and do the multiplication.

This fits on one page. It does not fit on a napkin.

The uncomfortable conclusion
After you run the numbers across reasonable ranges, a pattern emerges:

1) It is not obviously stupid
The concept does not collapse instantly on first principles. Under the right orbit, the right geometry, and with aggressive assumptions about launch and mass efficiency, you can build a system that is physically plausible. Thermal is hard but not mystical. Power is constrained but not impossible. The physics does not outright forbid it.

That matters. It is why the idea keeps coming back.

2) It is not obviously brilliant
Even under optimistic assumptions, the economics are punishing. The orbital system carries costs Earth simply does not. Every kilogram is expensive. Every watt implies area, mass, structure, deployment, and heat rejection. Every failure implies replacement mass. Every upgrade cycle implies a relaunch.

Earth does not have to pay those taxes.

3) It appears close enough that only one player can realistically attempt it
This is the part people dance around.

If the economics are barely within striking distance at all, the winner is not “the smartest.” It is the most vertically integrated, the most launch-advantaged, and the most willing to iterate at uncomfortable cadence.

In practice, that means one company.

It appears absolutely impossible for anyone else to do this competitively.

Not because others are incompetent. Not because nobody else has good engineers. Because everyone else has to buy their cost structure from the market. They buy launch. They buy buses. They buy integration. They buy operations. They buy supply chain. They buy schedule risk. Every interface adds margin and friction.

When you are trying to close a cost gap that is already brutal, margin stack kills you.

If this ever works for commodity compute, it will be because a vertically integrated launch provider forced the cost basis down through sheer scale and repetition, then used that same machinery to manufacture and deploy power and thermal hardware at industrial cadence.

That is a SpaceX-shaped path.

You do not need to “like” SpaceX to see this. It falls out of the structure of the problem.

Why I’m positive on SpaceX, and why I still want accountability
If you care about space industrialization, you should want SpaceX to keep winning. They are the only actor that has repeatedly demonstrated the ability to turn absurd goals into industrial reality by compressing timelines, collapsing interfaces, and iterating in hardware at software tempo.

But being positive is not the same thing as being credulous.

SpaceX deserves praise for execution. SpaceX also deserves to be held accountable to numbers. Especially if this idea becomes a public-market narrative, where hype can outrun diligence.

If you are going to pitch “space datacenters” as a serious economic frontier, you do not get to hide behind destiny. You have to publish assumptions and let the world touch the model.

That is not criticism. That is respect for engineering.

The “irrational billionaires” argument, properly stated
There is a real tension here:

If you judge purely on near-term risk-adjusted return, this might be a mediocre use of capital. You are taking extreme execution risk to deliver a commodity that already exists on Earth. GPUs are perfectly happy living in Oregon. They are even happier living next to cheap power, cheap cooling, and mature logistics.

So why do it?

Because not all projects are funded to maximize near-term ROI. Some projects are funded because they expand the feasible frontier. They create second-order capabilities that are hard to price but civilization-changing if they happen.

A rational market is good at building the tenth iteration of a known business. It is not always good at building cathedrals.

This is where irrational capital has a job.

Irrational billionaires exist, at their best, to fund projects that are just barely possible and socially valuable, but too weird, too slow, or too high-variance for normal capital.

Not because they are saviors. Because the system needs a mechanism for financing the edge cases that markets cannot justify until after they work.

If you take this framing seriously, you get a cleaner conclusion:

As a commodity compute play, orbit needs to close the cost gap.

As a civilization play, orbit can be worth doing even if it does not close immediately, because the knock-on benefits are enormous.

A lot of beautiful infrastructure began as irrational art.

But art still has to obey physics. You do not get to romanticize your way around 
T
4
T 
4
  and dollars per kilogram.

What the infographic is trying to teach you
The sliders are not there to “prove” anything. They are there to show you which assumptions are load-bearing.

A few examples of how to think about them:

Launch cost is a lever, not a moral belief
If your conclusion depends on a fantasy $/kg, you do not have a conclusion. You have a wish.

So the model forces you to pick scenarios. Falcon 9-like. Early Starship-like. Mature Starship-like. Then you watch the system move.

If you need miracles, you will see it immediately.

Specific power is the quiet killer
People love to talk about “the sun is huge,” but the sun does not matter if your watts per kilogram are mediocre. You cannot talk your way out of mass.

Specific power drives how many tons you need to loft for a given delivered electrical output. Tons drive launch. Launch drives cost. Cost drives everything.

Thermal is the tax nobody wants to pay
In space, heat rejection is not a footnote. It is the governing constraint for dense compute.

Even if you are “just” converting sunlight into electricity, remember the brutal accounting:

Most incident solar energy is absorbed as heat in the panel if it is not converted.

All generated electricity ends up as heat in the compute payload.

If you consume all generated electricity onboard, then effectively you must reject nearly all absorbed solar power as heat, plus whatever environmental loads you take from Earth view.

That pushes you into a regime where radiator area and allowable temperature become hard constraints. The system will happily equilibrate at whatever temperature closes the balance, including temperatures that cook your silicon.

In other words, the Universe will solve your thermal model for you. You just might not like the answer.

The part everyone avoids saying out loud
Let’s be blunt.

If this idea ever becomes real at scale for commodity compute, it will be because SpaceX turns launch into an industrial utility and then uses that utility to build and refresh a constellation like a factory line.

That implies a few things that people should say explicitly:

The economic moat is not “AI in space.”
The moat is mass throughput, manufacturing, and cadence.

If you are not vertically integrated, you are not “slightly disadvantaged.”
You are dead.

This is not a debate about clever architecture.
It is a debate about who can close a brutal cost basis.

So yes, I’m positive on SpaceX here. Not because I want a hero narrative. Because the structure of the cost model points to them as the only actor with a plausible path.

And that is also why I want accountability. If one company holds the only plausible key, then their claims matter. Their numbers matter. Their willingness to be audited by reality matters.

If SpaceX goes public: the right way to set the incentives
Here is my constructive proposal.

If SpaceX ever becomes a public company, shareholders should reward extreme ambition in the Tesla-comp sense, but only if the goals are:

Physically achievable

Quantitatively measurable

Economically relevant

Not “build a space datacenter.” That is a slogan.

Instead: define concrete goalposts that map directly to the governing metric. Examples:

Sustained delivered $/kg to LEO at a defined cadence

Demonstrated on-orbit $/W for a power platform at scale

Verified thermal closure at specified compute power density without derating

Multi-year operational uptime and replacement cadence metrics

Full system cost per delivered watt over a five-year window

If you hit those numbers, you deserve the trillion-dollar equity outcome. Because you did not just build a product. You created a new industrial base.

This is how you align irrational ambition with real accountability. You let the market pay for measurable reality, not for vibes.

What would change my mind
I want to be explicit about falsifiers, because this is where “reasonable engineer” lives.

If any of the following become true, I update my view:

Launch $/kg reaches a sustained level that is materially lower than current expectations, and does so at true industrial cadence, not a one-off demo.

On-orbit specific power including thermal rejection hardware improves dramatically beyond current flight-proven baselines.

A credible architecture shows thermal closure at compute-relevant temperatures without hiding behind unrealistic radiator temperatures or perfect view factors.

Terrestrial power and datacenter economics shift materially enough that the benchmark changes, such as massive increases in regulatory cost, fuel pricing, or grid constraints, in a way that persists over the relevant horizon.

The point is not that I “want” a specific outcome. The point is that the argument should be tethered to levers we can measure.

So where do I land?
This deserves real math, not vibes.

It is not obviously stupid. It is not obviously brilliant. It is barely feasible under aggressive assumptions, and that makes it interesting.

It also appears, with uncomfortable clarity, that the only entity with a plausible path to closing the economics is SpaceX. Everyone else is staring at a margin stack and a mass tax they cannot escape.

That is not a moral statement. It is a structural one.

And finally, even if the unit economics for commodity compute never cleanly beat Earth in the near term, the act of trying might still be one of the most valuable irrational projects a civilization can fund. It could accelerate launch cadence, space manufacturing, power platforms, and operational maturity in ways that ripple outward for decades.

There is beauty in the irrational.

But if we are going to do cathedral-building with rockets, we should at least do the courtesy of running the spreadsheet first.

Play with the sliders. Break my assumptions. Show me where the model is wrong.

If the idea survives that, it deserves to be taken seriously.

If it does not, then we should stop pretending inspiration is a substitute for arithmetic.

You said:
can we add a little bit more of the pining for the incredible future, but keep the brutal realism? 
ChatGPT said:
It might not be rational.

It might still be physically possible.

And that combination is exactly how civilization upgrades itself.

I love space in the specific way that makes you slightly unwell. Not as a hobby. As a belief that we are supposed to be out there. That the long arc of competent civilizations bends toward building heavy industry off-planet. That the point of rockets is not to take selfies in microgravity, but to move the center of gravity of human capability. I want the incredible future. I want the scaffolding. I want the orbital shipyards, the power stations, the boring logistics that make “spacefaring” a supply chain instead of a genre.

I also love AI. I buy the argument that compute is the new industrial input, like steel or electricity, and that whoever can scale it cheapest gets to write a lot of the next chapter. So when someone says “space datacenters,” a part of my brain sees the cathedral. The absurd, shining thing on the horizon that makes you forgive a decade of hard work.

That is why I’m annoyed.

Because we’re trying to talk ourselves into a cathedral while skipping the math that determines whether the foundation even holds. The public discourse around space-based datacenters is confident in the way only an under-modeled idea can be. People wave at the sun, wave at Starship, wave at “infinite energy,” and then speak as if the economics are inevitable.

Physics does not care about inevitability. Economics cares even less.

This essay and the accompanying interactive infographic are my attempt to raise the floor of the conversation. Not to throw cold water on ambition, but to protect it from self-deception. If this is going to be real, it will survive a spreadsheet. If it can’t survive a spreadsheet, it was never real. It was just a mood.

This is the deal I’m proposing: we keep the dream, and we pay the rent.

The core claim
If you are proposing space-based datacenters for commodity workloads, you are making one claim and only one claim:

You can host compute more cheaply in orbit than on Earth.

Not cooler. Not more inspiring. Not “100 trillion times more solar energy.” Cheaper.

Because the moment you leave the narrow category of space-critical compute, you are competing with hyperscalers who already sit on top of cheap land, cheap electrons, mature supply chains, and fiber networks that are boring only because they are brutally efficient.

A flop in orbit is not a sacred flop. A watt in orbit is not a premium watt. They do not gain magical economic properties at 550 km altitude. They cost what they cost.

So we strip the debate down to its governing parameter:

Cost per watt.

Cost per watt of delivered electrical power that can be turned into heat inside GPUs, rejected by radiators, maintained for years, and operated at scale.

If you are building a space datacenter, you are not building “compute.” You are building the entire datacenter stack, except now every subsystem has to fly.

Power generation. Thermal rejection. Structure. Deployment. Attitude control. Communications. Operations. Spares. Reliability. Launch. Replacement cadence. Insurance. Everything.

That stack has to beat Earth on price.

That is the whole game.

Step zero: separate the real use case from the vibe use case
There are two fundamentally different categories of “compute in orbit,” and a lot of confusion comes from mixing them.

Category A: Space-critical compute
This is the steelman. This is real.

If you are producing data in space faster than you can ship it to the ground, onboard processing can be rational. Earth observation, SAR, hyperspectral imaging, missile warning, autonomy, tactical latency. You can easily create scenarios where you want to compress terabytes into megabytes before downlink, or where you need decisions made locally without waiting for a ground loop.

Compute is valuable here because it reduces bandwidth requirements or improves mission capability. In those cases you are not competing with AWS on cost per flop. You are buying capability.

This category already exists and will grow.

Category B: Generic compute
This is what most “space datacenter” conversations imply, whether they admit it or not.

Training, inference, indexing, recommender systems, batch processing, general purpose GPU farms. The stuff that makes up nearly all terrestrial compute demand.

This category does not care where it runs. It cares about price, uptime, and throughput. The physical location is just logistics.

If you propose moving this category to orbit, you are not proposing a new physics trick. You are proposing to win a commodity cost war against Earth.

So for the rest of this essay, we are talking about Category B.

The interactive infographic: the argument you can touch
The infographic is not decoration. It is an argument you can interrogate.

It does one thing: it takes a plausible, flight-proven “power hardware” baseline and scales it to a 1 GW system. Then it compares that orbital bill to a 1 GW terrestrial power alternative over a five-year horizon.

The reason to use 1 GW is not because anyone will build a 1 GW space datacenter tomorrow. It is because big round numbers force honesty. If your story only works at toy scale, it is not a story about industry. It is a story about a demo.

At a high level, the model has three blocks:

How many watts can you generate per kilogram in orbit?
This sets the orbital mass required for a given power level.

How many dollars does it cost to put that mass where it needs to go and keep it operating?
Launch plus hardware plus operations reality.

What is the terrestrial benchmark?
A 1 GW terrestrial alternative over the same horizon.

Then the infographic asks the only question that matters:

Is one watt generated and consumed in orbit cheaper than one watt generated and consumed on Earth?

If the answer is no by a large factor, nothing else matters. Not thermal cleverness. Not orbital mechanics. Not vision. You can’t “engineer” your way out of an order-of-magnitude cost gap with narrative.

If the answer is yes, or even within striking distance, then the whole topic becomes legitimately interesting. Because now you are in a regime where execution, integration, and iteration speed can decide the outcome.

That is why the sliders exist. They are there to show you where the fulcrums are, and what would have to be true for the idea to close.

The future worth pining for (and what this idea is really about)
Let me say the quiet part out loud.

Even if orbital commodity compute never wins cleanly on price, the act of trying could still be one of the most important industrial projects we attempt this century. Not because GPUs in orbit are inherently meaningful, but because the enabling infrastructure is.

If you can deploy megawatts, then tens of megawatts, then hundreds of megawatts of reliable power generation in orbit, you have built a piece of civilization. A thing that can support everything else we keep pretending we want: manufacturing, refueling, high-duty communications, large-scale sensing, autonomy, and eventually the logistics backbone that makes deep space feel closer.

Power is the primitive. In any environment.

A lot of the “space datacenter” narrative is secretly a story about power platforms and mass throughput, wearing a trendy compute jacket because that is what gets attention right now. Compute is the marketing. Infrastructure is the prize.

But infrastructure is also where physics and economics come to collect rent. You do not get cathedrals without quarries.

So yes, I’m pining for the incredible future. I want the off-planet industrial base. I want the moment where “space economy” stops meaning launch and starts meaning output.

I’m also here to remind everyone that you cannot skip the rent.

Why the discourse is broken
A lot of public conversation does this:

“The sun is huge.”

“Space is cold.”

“Launch will be cheap.”

“Therefore space datacenters are inevitable.”

That is not analysis. That is a mood board.

The governing physics here are not exotic. They are closed-form and unforgiving:

Solar flux is a known constant to first order.

Solar cell efficiency is bounded by physics and manufacturing.

Waste heat must be rejected by radiation, which scales with 
T
4
T 
4
 .

Hardware masses and costs scale in predictable ways.

Launch cost is a lever, but it is not a magic wand.

You do not get to invoke Stefan–Boltzmann as a talisman. You have to actually close the heat balance under realistic operating temperatures and view factors.

You do not get to wave at “Starship” like it is a cheat code. You have to pick a $/kg, pick a cadence, pick a lifetime, and do the multiplication.

This fits on one page. It does not fit on a napkin.

The uncomfortable conclusion
After you run the numbers across reasonable ranges, a pattern emerges.

1) It is not obviously stupid
The concept does not collapse instantly on first principles. Under the right orbit, the right geometry, and with aggressive assumptions about launch and mass efficiency, you can build a system that is physically plausible. Thermal is hard but not mystical. Power is constrained but not impossible. The physics does not outright forbid it.

That matters. It is why the idea keeps coming back.

2) It is not obviously brilliant
Even under optimistic assumptions, the economics are punishing. The orbital system carries costs Earth simply does not. Every kilogram is expensive. Every watt implies area, mass, structure, deployment, and heat rejection. Every failure implies replacement mass. Every upgrade cycle implies a relaunch.

Earth does not have to pay those taxes.

3) If it works at scale, it will be because of one company
This is the part people dance around.

If the economics are barely within striking distance at all, the winner is not “the smartest.” It is the most vertically integrated, the most launch-advantaged, and the most willing to iterate at uncomfortable cadence.

In practice, that means one player.

It appears absolutely impossible for anyone else to do this competitively.

Not because others are incompetent. Not because nobody else has good engineers. Because everyone else has to buy their cost structure from the market. They buy launch. They buy buses. They buy integration. They buy operations. They buy supply chain. They buy schedule risk. Every interface adds margin and friction.

When you are trying to close a cost gap that is already brutal, margin stack kills you.

If this ever works for commodity compute, it will be because a vertically integrated launch provider forced the cost basis down through scale and repetition, then used that same machinery to manufacture and deploy power and thermal hardware at industrial cadence.

That is a SpaceX-shaped path.

You do not need to like SpaceX to see this. It falls out of the structure of the problem.

Why I’m positive on SpaceX, and why I still want accountability
If you care about space industrialization, you should want SpaceX to keep winning. They are the only actor that has repeatedly demonstrated the ability to turn absurd goals into industrial reality by compressing timelines, collapsing interfaces, and iterating in hardware at software tempo.

But being positive is not the same thing as being credulous.

SpaceX deserves praise for execution. SpaceX also deserves to be held accountable to numbers, especially if this becomes a public-market narrative where hype can outrun diligence.

If you are going to pitch “space datacenters” as a serious economic frontier, you do not get to hide behind destiny. You have to publish assumptions and let the world touch the model.

That is not criticism. That is respect for engineering.

The “irrational billionaires” argument, properly stated
There is a real tension here.

If you judge purely on near-term risk-adjusted return, this might be a mediocre use of capital. You are taking extreme execution risk to deliver a commodity that already exists on Earth. GPUs are perfectly happy living in Oregon. They are even happier living next to cheap power, cheap cooling, and mature logistics.

So why do it?

Because not all projects are funded to maximize near-term ROI. Some projects are funded because they expand the feasible frontier. They create second-order capabilities that are hard to price but civilization-changing if they happen.

A rational market is good at building the tenth iteration of a known business. It is not always good at building cathedrals.

This is where irrational capital has a job.

Irrational billionaires exist, at their best, to fund projects that are just barely possible and socially valuable, but too weird, too slow, or too high-variance for normal capital.

Not because they are saviors. Because the system needs a mechanism for financing the edge cases that markets cannot justify until after they work.

If you take this framing seriously, you get a cleaner conclusion:

As a commodity compute play, orbit needs to close the cost gap.

As a civilization play, orbit can be worth doing even if it does not close





No file chosenNo file chosen
ChatGPT can make mistakes. Check important info.
