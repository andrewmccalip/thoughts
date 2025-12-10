**Intro:**

Before we do the classic engineer thing and get nerd sniped by all the shiny technical problems, let's back up and ask the fundamentally important question.   **Why put compute in orbit at all?**

Why should a watt of power or a flop of compute be more valuable 250 miles above Earth than on the surface?\
What economic or strategic advantage justifies the enormous effort required to perform something as mundane as matrix multiplication in low Earth orbit?

Right now, that "why" is almost entirely missing from the public conversation. The discourse tends to skip straight to implementation details, as if the business case is already so obvious it doesn't need to be stated. In reality, the opposite is true. The excitement is being driven by a mix of FOMO, aesthetic futurism, and a surface-level reading of orbital mechanics rather than by a clearly defined value proposition.

If you can't answer the "why" with conviction, everything downstream --- the engineering, the economics, the deployment concept --- collapses into speculation. Serious engineering starts by defining value. Without that, the rest is just a creative way to dodge first principles.

**It's disappointing to see industry leaders blur this distinction and default to the big-numbers game. It isn't good enough to toss out a strawman like "we're going to run out of energy on Earth" and treat that as a business case.**

**"how do we one day have data centers in space so that we can better harness the energy from the sun that is 100 trillion times more energy than what we produce on all of Earth today?" Sundar Pichai**

**"You cannot build power plants of that scale---say, with 1 terawatt of continuous output---it's simply impossible. It must be done in space". Elon Musk @ U.S.-Saudi Investment Forum Interview**

These statements sound bold and visionary, but they skip the critical step. They assume the value rather than demonstrating it. They imply that because the sun is bright and space is big, the economics must work out in space's favor. That is not how engineering decisions are made. The only relevant question is whether a watt or a flop in orbit delivers more value per dollar than one on Earth. If the answer is no, the idea fails immediately, regardless of how inspiring the narrative sounds.

**Use Cases**
-------------

To discuss Compute in orbit, we should dividie into two broad categories:

1.  **Space-critical compute** -- where latency or bandwidth make local processing essential.

2.  **Everything else** -- commidity workloads where you're competing with the AWS datacnter sof the world

**Space-critical compute**

The first category is the *steelman* argument for putting GPUs or CPUs in orbit.

There's really only one scenario where putting compute in orbit makes sense: you're producing data faster than you can get it to the ground. Everything else collapses under basic geometry and link physics.

Satellites have no trouble generating enormous amounts of raw data. A modern 48MP camera shooting raw easily pushes **2--5 gigabits per second** continuously, and SAR systems run even higher; commercial X-band radars regularly exceed **5--8 Gbps**, with government systems going above **20 Gbps** internally. That's why a single 10-minute overpass can leave you sitting on hundreds of gigabytes that you now have to get off the spacecraft.

The problem is the downlink. A typical LEO satellite only sees a ground station for **8--12 minutes** per pass, and even a high-end Ka-band link taps out around **3--5 Gbps** under perfect conditions. Many operators never see that number, because antennas are shared, weather intervenes, and scheduling windows are rationed across dozens of customers. Commercial networks like KSAT and SSC frequently run near saturation; access often needs to be booked **days to weeks** in advance. This is why onboard or near-board pre-processing sounds appealing: turn terabytes into megabytes and send down only what matters.

On paper, that's the steelman.

Where it breaks is when you actually look at orbital distances. A satellite at 550 km altitude is five hundred fifty kilometers from the Earth's surface; that never changes. But in a dense constellation like Starlink, the nearest neighbor is usually **1,200--1,500 km** away once you account for plane spacing and relative phasing. That's not a hand-wave; Starlink Gen-2 shells have planes separated by **5--7 degrees**, and even within a plane, satellites sit roughly **1--2 degrees** apart, which works out to hundreds of kilometers of physical separation. The lowest slant-range ISL paths routinely exceed a thousand kilometers.

Now imagine trying to send that firehose of raw sensor data horizontally to an "orbital compute node" instead of vertically to Earth. If you posit four such nodes in LEO, spaced evenly around the planet, the average slant range from any imaging satellite to the nearest node is on the order of **4,000--5,000 km**. That's simply the chord length across a ring at 550 km altitude divided into quadrants. It's not a back-of-the-envelope trick --- it's basic spherical geometry.

A link that long is dramatically harder to close. Beam divergence grows with distance; pointing stability demands increase; received power drops by nearly **20 dB** between a 1,000 km link and a 5,000 km one. Even laser ISLs, which Starlink uses at roughly **40--100 Gbps** over ~1,000--2,000 km paths, start falling apart fast when you extend to intercontinental-scale orbital distances. And unlike a ground station, which can house multi-meter-class dishes and powerful tracking systems, any orbital node is mass-constrained and thermally limited.

This leads to the uncomfortable conclusion: the closest, cheapest, highest-throughput place to send your data is still Earth. A 550 km downlink path into a hardened, fiber-backed ground station beats a 1,500--5,000 km sideways link into a spacecraft with tighter mass, power, and aperture constraints. And once you reach Earth, you're effectively already inside a hyperscale data center backbone.

So even this "best case" argument --- the one that's supposed to justify orbital GPUs --- fails once you run real numbers. The physics favors the planet. The infrastructure is already there. And the geometry ensures the sideways hop is always worse than the straight-down one.

**Generic Compute**
-------------------

Once you separate out the narrow class of missions that genuinely require local processing in space, you're left with everything else --- the overwhelming majority of computing done on Earth. This is **generic, location-agnostic compute**. Model training, inference, indexing, recommender systems, search, storage, analytics, batch jobs. Ninety-nine point many nines percent of global compute demand lives here.

And this entire category shares one defining trait: **it does not care where it runs**. Its inputs and outputs are bits moving across fiber. It doesn't ask for altitude, vacuum, microgravity, or a laser link. It asks for **the cheapest and most reliable flops available**.

That's why hyperscale operators build wherever unit economics are optimized. AWS builds in Oregon, Iowa, Northern Virginia, and Sweden because that's where you get the right mix of cheap electricity, cheap land, cool climates, and dense fiber backbones. Crusoe, whose entire business model is squeezing flops out of stranded natural gas and surplus renewable power, pushes this to the logical extreme. Their message is the same: compute is a commodity pipeline, and the winner is the operator who delivers the lowest cost per flop.

So when someone proposes running generic compute in orbit, they are making an extraordinary claim: that **the full datacenter stack** --- power generation, cooling, networking, hardware, structures, and operations --- can be done *more cheaply in orbit* than inside a tilt-wall datacenter tied into a 200- to 500-MW substation.

A flop in orbit is not a special flop. A watt in orbit is not a special watt. They do not acquire new economic properties at 550 kilometers altitude. They cost what they cost.

This is why the economics are decisive. Commodity compute is not a physics problem. It is a cost competition with AWS, with Crusoe, with every hyperscale operator that already sits directly on top of cheap electricity and mature supply chains. If orbit wants to win, it must beat them on price. Not elegance. Not novelty. **Price.**

**Economics:**

Before getting lost in hardware diagrams and thermal edge cases, the first step is to anchor everything to the governing economic question. If orbital compute is going to be more than an aesthetic idea, its unit economics must beat the cheapest terrestrial alternatives. That reduces the entire concept to one parameter: **cost per watt**. Everything else --- solar arrays, radiators, thermal loops, GPUs, vacuum, microgravity --- sits downstream of that number.

The cleanest way to evaluate this is to pick the most mass-efficient power hardware flying today, scale it to a 1-GW system, and compute the full orbital bill. A Starlink V2 Mini class bus is the logical reference point. Its mass, solar area, and delivered electrical power give a real, flight-proven specific power. Once those numbers are fixed, the required constellation mass and total hardware cost fall straight out of the math.

Launch cost is the next step. Pick a few reasonable scenarios --- Falcon 9, early-Starship, mature-Starship --- apply them to the total delivered mass, and you get the full orbital system cost.

Then compare that directly to a 1-GW natural-gas combined-cycle plant over the same five-year window, including capital cost, fuel burn, and O&M. This produces a clean, constrained, physics-bounded economic comparison with no hand-waving. The question it answers is simple:

**Is one watt generated and consumed in orbit cheaper than one watt generated and consumed on Earth?**

The numbers say no. Not marginally no. Orders-of-magnitude no. Even under optimistic Starship pricing, the launch bill alone overwhelms the entire five-year cost of a terrestrial NGCC plant. And that's before accounting for the additional mass and complexity required to run high-density compute hardware in vacuum.

What follows is the minimal set of assumptions needed to quantify this comparison. 

Assumptions
-----------

### **Global**

-   We compare **1 GW** of nameplate electrical capacity over a **5-year** period.

-   All numbers are rounded; this is a first-principles, order-of-magnitude economic comparison.

### **Orbital Solar System (Starlink-class satellites)**

-   Use a **Starlink V2 Mini--style bus** as the reference unit:

    -   About **105 m²** deployed solar array area.

    -   About **600 kg** mass.

    -   About **27--30 kW** of electrical power at 1 AU (consistent with silicon-class efficiency, packing losses, and DC conversion).

-   This yields an **effective specific power of ~45 W/kg**.

-   To reach **1 GW**, such a system requires:

    -   **22.2 million kg** delivered to LEO.

    -   Hardware cost of **250,000 dollars per satellite**, which works out to roughly **9 dollars per watt**.

    -   Total hardware cost: **~9.0 billion dollars** for a 1 GW constellation.

-   We assume **no fuel cost** in orbit and ignore O&M because it is small relative to launch and hardware costs.

### **Launch Costs**

-   **Falcon 9**: 2,939 dollars per kg (67M dollars / 22,800 kg).

-   **Starship** scenarios:

    -   1,000 dollars per kg.

    -   500 dollars per kg.

    -   100 dollars per kg (aggressive long-run target).

-   Launch cost is applied to the full **22.2 million kg** required for the orbital system.

### **Natural Gas Combined Cycle (NGCC) System**

-   Use standard U.S. EIA values:

    -   **898 dollars per kW** overnight capital cost → **0.898 billion dollars** to build 1 GW.

-   Use representative operating assumptions for modern NGCC plants:

    -   **65 percent capacity factor** over 5 years.

    -   Heat rate and fuel price chosen to give **~25 dollars per MWh** fuel cost.

    -   Fixed + variable O&M consistent with typical NGCC values.

-   Under these inputs, the **total 5-year NGCC cost** (build + fuel + O&M) is about **1.78 billion dollars**.

--

5-Year Total System Cost (final numbers)
----------------------------------------

-   Natural gas (build + 5 years fuel & O&M) = 1.8 billion dollars

-   Falcon 9 (2,939 dollars/kg) = 74.3 billion dollars

-   Starship (1,000 dollars/kg) = 31.2 billion dollars

-   Starship (500 dollars/kg) = 20.1 billion dollars

-   Starship (100 dollars/kg) = 11.2 billion dollars

**\
**

**Technical engineerin challenges: **

more to say here later
* * * * *

