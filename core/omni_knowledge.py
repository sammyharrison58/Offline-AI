import re
from typing import Dict, Any, List, Optional

OMNI_TOPICS = [
    {
        "name": "Rayleigh Scattering & Sky Optics",
        "keywords": ["sky blue", "why is the sky blue", "blue sky", "sunset red", "rayleigh scattering", "light scattering", "atmospheric optics"],
        "definition": "The optical phenomenon explaining why the daytime sky appears blue and sunsets appear red, caused by the scattering of electromagnetic radiation by particles much smaller than the wavelength of light.",
        "mechanism": "Sunlight contains all colors of the visible spectrum. As sunlight enters Earth's atmosphere, it collides with gas molecules (predominantly nitrogen and oxygen). Shorter wavelengths (blue and violet at ~400-450nm) scatter in all directions roughly 10 times more efficiently than longer wavelengths (red and orange at ~650-700nm). Our eyes are far more sensitive to blue light than violet, so we perceive the scattered sky light as clear cyan-blue. At sunset, sunlight passes through a much greater thickness of atmosphere, scattering away almost all blue light before it reaches our eyes and leaving only the direct red, orange, and gold rays.",
        "principles": "Scattering intensity I is inversely proportional to the fourth power of the wavelength: I ~ 1 / lambda^4. Discovered by Lord Rayleigh in 1871.",
        "significance": "Underpins atmospheric physics, telescope observations, optical fiber design, and explains color variations across planetary atmospheres like Mars (where fine iron-oxide dust causes butterscotch daytime skies and blue sunsets).",
        "applications": "Optical communications, lidar atmospheric profiling, colorimetric sensor calibration, and computer graphics atmosphere rendering."
    },
    {
        "name": "Aerodynamics & Principles of Flight",
        "keywords": ["how airplanes fly", "how planes fly", "airplane flight", "aerodynamics", "lift force", "bernoulli lift", "airfoil", "aviation physics"],
        "definition": "The branch of fluid dynamics governing how heavier-than-air vehicles generate aerodynamic lift to overcome gravity and achieve controlled atmospheric flight.",
        "mechanism": "An aircraft stays aloft through the dynamic interaction of four continuous forces: Lift, Weight (Gravity), Thrust, and Drag. Wings are shaped as airfoils with cambered curvature. As the wing moves through air propelled by jet engines or propellers, it deflects the oncoming airflow downward. By Newton's Third Law (action and reaction), forcing air downward exerts an equal and opposite upward reaction force on the wing. Simultaneously, Bernoulli's principle and circulation theory dictate that air flowing over the upper curved surface moves faster, creating a localized drop in static pressure compared to the higher pressure beneath the wing. The combination of pressure differential and massive net downward momentum transfer produces sustained lift.",
        "principles": "Lift Equation: L = 1/2 * rho * v^2 * S * C_L where rho is air density, v is velocity, S is wing surface area, and C_L is the lift coefficient. Kutta-Joukowski circulation theorem: L' = rho_infinity * V_infinity * Gamma.",
        "significance": "Enabled the global aviation network, connecting distant continents in hours, transforming human trade, disaster relief, and military defense.",
        "applications": "Commercial passenger aircraft, supersonic jets, wind turbine blades, high-speed Formula 1 spoilers, and drone propeller optimization."
    },
    {
        "name": "Cellular Biology & DNA Replication",
        "keywords": ["dna replication", "how dna works", "structure of dna", "cell division", "mitosis", "genetic code", "double helix", "molecular biology"],
        "definition": "The biological process by which a living cell copies its entire genome with extraordinary fidelity before cell division, ensuring accurate transmission of hereditary instructions.",
        "mechanism": "DNA is a double-stranded helical polymer composed of four nitrogenous bases: Adenine (A), Thymine (T), Cytosine (C), and Guanine (G), held together by hydrogen bonds between complementary pairs (A-T and C-G) on a deoxyribose-phosphate backbone. During replication, DNA helicase unzips the double helix at origins of replication, forming replication forks. DNA polymerase synthesizes a new complementary strand along each template strand in the 5' to 3' direction. The leading strand is synthesized continuously, while the lagging strand is built in short Okazaki fragments joined by DNA ligase. Proofreading exonucleases correct mismatched bases, keeping error rates below one mistake per billion nucleotides.",
        "principles": "Central Dogma of Molecular Biology: DNA is transcribed into messenger RNA (mRNA), which is then translated by ribosomes into functional protein chains. Complementary base-pairing rule discovered by Watson, Crick, and Franklin (1953).",
        "significance": "Forms the foundational mechanism of all biological reproduction, cellular growth, tissue repair, hereditary traits, and evolutionary adaptation across all life on Earth.",
        "applications": "PCR diagnostics, forensic DNA profiling, recombinant genetic engineering, mRNA therapeutics, and agricultural biotechnology."
    },
    {
        "name": "Electromagnetism & Electric Power Generation",
        "keywords": ["how electricity is generated", "how electricity works", "electromagnetic induction", "electric generators", "faraday induction", "power grid", "alternating current"],
        "definition": "The generation of electrical energy from mechanical motion using electromagnetic induction, converting kinetic power into alternating current that powers modern civilization.",
        "mechanism": "In 1831, Michael Faraday discovered that moving a conductor through a magnetic field (or changing the magnetic flux passing through a wire loop) induces an electromotive force (voltage). In commercial power plants (hydroelectric, coal, natural gas, or nuclear), heat or falling water spins a turbine shaft connected to an electric generator. Inside the generator, massive electromagnets spin inside stationary coils of copper wire (stator). The rapidly rotating magnetic field continuously sweeps across the copper windings, pushing electrons back and forth along the wire to create high-voltage Alternating Current (AC). Transformers then step up this voltage to hundreds of thousands of volts for long-distance transmission over power lines with minimal resistive heat loss, before step-down substations lower it to 120V/240V for safe home and industrial use.",
        "principles": "Faraday's Law of Induction: EMF = - N * (dPhi_B / dt) where N is number of turns and Phi_B is magnetic flux. Lenz's Law dictates that the induced current creates an opposing magnetic field conserving energy. Ohm's law: V = I * R; Electric Power: P = V * I.",
        "significance": "Electric power generation is the single most critical technological bedrock of industrial civilization, powering lighting, heating, manufacturing, computation, and communication.",
        "applications": "Hydroelectric dams, wind turbines, nuclear fission reactors, steam turbines, electric vehicle regenerative braking, and micro-generators."
    },
    {
        "name": "Internal Combustion & Electric Vehicle Engines",
        "keywords": ["how car engines work", "internal combustion engine", "four stroke engine", "how cars work", "electric cars vs gas", "ev motor", "powertrain"],
        "definition": "The mechanical and electrical systems that convert chemical fuel energy or stored electrochemical battery energy into rotational torque to propel motor vehicles.",
        "mechanism": "Traditional internal combustion engines (ICE) operate on the four-stroke Otto cycle: 1) Intake: the piston moves downward, drawing a mixture of atomized fuel and air into the cylinder. 2) Compression: the intake valve closes and the piston moves upward, compressing the fuel-air charge to high pressure and temperature. 3) Combustion/Power: a spark plug ignites the compressed mixture; the rapid explosive expansion of burning gases drives the piston downward with immense force, rotating the crankshaft. 4) Exhaust: the exhaust valve opens and the rising piston pushes out spent gases. In contrast, modern Electric Vehicles (EVs) eliminate cylinders, pistons, and spark plugs entirely: high-voltage lithium-ion battery packs supply three-phase AC electricity to an electric induction or permanent-magnet synchronous motor, using rotating magnetic fields to spin the rotor with instant maximum torque at 0 RPM and >90% energy efficiency (compared to ~25-30% thermal efficiency in gasoline engines).",
        "principles": "Thermodynamic Otto and Diesel cycles. Carnot efficiency limit: eta = 1 - (T_cold / T_hot). Lorentz force law in electric motors: F = q * (E + v x B).",
        "significance": "Motorized transportation expanded human mobility, shaped modern urban design, created global supply chains, and is now undergoing the largest technological transition in a century toward zero-emission electrification.",
        "applications": "Automobiles, commercial freight trucking, maritime cargo shipping, hybrid powertrains, and high-performance battery systems."
    },
    {
        "name": "Vaccinology & Immune System Memory",
        "keywords": ["how vaccines work", "immune system", "antibodies", "vaccination", "adaptive immunity", "mrna vaccines", "herd immunity", "pathogens"],
        "definition": "The biomedical science of training the body's adaptive immune system to recognize and rapidly destroy specific viral or bacterial pathogens without causing the actual disease.",
        "mechanism": "When a pathogen enters the body, innate immune cells (macrophages and dendritic cells) engulf it and present fragments of its surface antigens to helper T-cells. These T-cells activate B-cells, which differentiate into plasma cells that produce millions of targeted antibodies — Y-shaped proteins that bind specifically to the pathogen's antigens, neutralizing them and marking them for destruction. A subset of B-cells and T-cells become long-lived Memory Cells that persist in lymph nodes for decades. Vaccines simulate an infection by presenting an inactivated pathogen, a weakened live virus, a harmless protein subunit, or mRNA instructions that prompt human cells to temporarily produce the harmless spike antigen. The immune system mounts a full adaptive response, generating high-affinity memory cells. If the real pathogen ever attacks later, memory cells recognize it instantly, flooding the bloodstream with neutralizing antibodies within hours and clearing the infection before illness develops.",
        "principles": "Adaptive immunological memory and clonal selection theory. Somatic hypermutation and V(D)J recombination generate up to 10^18 unique antigen receptor variants. Herd immunity threshold: q_c = 1 - 1/R_0.",
        "significance": "Vaccines represent the greatest medical intervention in human history, eradicating smallpox, nearly eliminating polio, and saving hundreds of millions of lives from measles, tetanus, diphtheria, and pandemic viral pathogens.",
        "applications": "Preventative childhood immunizations, seasonal influenza vaccines, mRNA vaccine platforms, cancer therapeutic vaccines, and rabies post-exposure prophylaxis."
    },
    {
        "name": "Plate Tectonics & Continental Drift",
        "keywords": ["plate tectonics", "continental drift", "earthquakes", "volcanoes", "how continents move", "fault lines", "earth mantle", "subduction zone"],
        "definition": "The unifying geological theory explaining that Earth's outer rigid shell (lithosphere) is fractured into massive tectonic plates that float and move atop the ductile, convective asthenosphere.",
        "mechanism": "Earth's core generates immense heat from radioactive decay of uranium, thorium, and potassium, plus primordial heat left over from planetary accretion. This heat drives slow thermal convection currents in the semi-solid mantle over millions of years. Tectonic plates interact along three types of boundaries: 1) Divergent boundaries: plates pull apart (e.g. Mid-Atlantic Ridge), allowing magma to rise, cool, and form new oceanic crust. 2) Convergent boundaries: plates collide; dense oceanic crust subducts beneath lighter continental crust into the mantle, melting and forming deep ocean trenches and volcanic mountain ranges (e.g. the Andes and Ring of Fire), or two continental plates crash and buckle upward to form giant mountain ranges (e.g. the Himalayas formed by India colliding with Eurasia). 3) Transform boundaries: plates slide horizontally past each other (e.g. California's San Andreas Fault); friction locks the rocks until accumulated strain energy exceeds rock strength, releasing violently as an earthquake.",
        "principles": "Mantle convection, slab pull (gravitational sinking of cold dense subducting slabs), and seafloor spreading. Paleomagnetic striping of the ocean floor confirmed seafloor spreading (Vine-Matthews-Morley hypothesis).",
        "significance": "Explains the global distribution of earthquakes, active volcanoes, mountain building, fossil similarities across oceans, and the long-term geochemical carbon-silicate cycle that regulates Earth's climate over hundreds of millions of years.",
        "applications": "Earthquake hazard assessment, building code engineering, geothermal energy exploration, volcanic eruption forecasting, and mineral deposit locating."
    },
    {
        "name": "How the Internet Works & TCP/IP Architecture",
        "keywords": ["how internet works", "how the internet works", "tcp ip", "packets", "dns", "routers", "routing", "ip address", "web architecture"],
        "definition": "The global decentralized network of interconnected computers communicating via standardized packet-switching protocols (TCP/IP), transmitting data seamlessly across optical fibers, copper wires, and wireless links.",
        "mechanism": "When you enter a web address or send a message, your computer first queries a Domain Name System (DNS) server — the internet's phonebook — which translates human-readable domain names (like example.com) into numerical IP addresses (like 93.184.216.34). Your application data is passed down the protocol stack to the Transmission Control Protocol (TCP), which slices the data into small chunks called Packets, numbering each packet and adding error-checking checksums. The Internet Protocol (IP) attaches sender and destination IP addresses to each packet header. These packets travel across local Wi-Fi or Ethernet to your router, which forwards them to an Internet Service Provider (ISP). Autonomous border routers use Border Gateway Protocol (BGP) to route packets along the fastest available fiber-optic backbone cables across continents and deep-sea submarine cables. Packets may travel along completely different physical routes. At the destination server, TCP verifies that all packets arrived intact, requests retransmission of any dropped packets, reassembles them in exact numerical order, and passes the reconstructed message to the web application.",
        "principles": "OSI 7-Layer and TCP/IP 4-Layer models. Packet switching vs circuit switching (Baran and Davies). End-to-end principle: intelligence resides in edge nodes, while intermediate routers simply forward packets as fast as possible.",
        "significance": "Underpins the modern digital economy, cloud computing, real-time global communications, social coordination, and access to all human knowledge.",
        "applications": "Web browsing, real-time video streaming, distributed databases, financial electronic fund transfers, IoT smart devices, and secure VPN communications."
    },
    {
        "name": "Macroeconomics, Inflation & Monetary Policy",
        "keywords": ["how inflation works", "what is inflation", "interest rates", "central banks", "federal reserve", "money supply", "economic growth", "gdp"],
        "definition": "The study of economy-wide phenomena — national income, gross domestic product (GDP), general price inflation, unemployment, and the central bank policies used to stabilize economic cycles.",
        "mechanism": "Inflation is the generalized, ongoing increase in the prices of goods and services across an entire economy, which simultaneously reduces the purchasing power of each unit of currency. Inflation primarily occurs through two dynamics: 1) Demand-Pull inflation: aggregate consumer and business demand for goods and services outpaces an economy's productive capacity, bidding prices up. 2) Cost-Push inflation: aggregate supply falls due to surges in production costs (e.g. oil shocks, supply chain blockages, or raw material shortages). Money supply growth that outstrips economic output also fuels inflation. Central banks (such as the Federal Reserve, ECB, or Bank of England) manage inflation primarily through Monetary Policy: adjusting the benchmark overnight interest rate. When inflation runs too high, the central bank raises interest rates. Higher rates make borrowing more expensive for mortgages, business loans, and credit cards, which cools spending, slows business investment, and curbs inflation. Conversely, during recessions, central banks cut interest rates to make credit cheap, stimulating hiring and recovery.",
        "principles": "Quantity Theory of Money: M * V = P * Y (Money Supply * Velocity = Price Level * Real Output). Phillips Curve relationship between inflation and unemployment. Taylor Rule for policy interest rates: r = r* + pi + 0.5*(pi - pi*) + 0.5*(y - y*).",
        "significance": "Monetary policy decisions directly affect mortgage rates, employment opportunities, corporate profitability, currency exchange values, and household wealth preservation.",
        "applications": "Central bank interest rate decisions, corporate capital budgeting, inflation-hedging portfolio management (TIPS, commodities), and sovereign bond valuation."
    },
    {
        "name": "Computer Microprocessors & Silicon Transistors",
        "keywords": ["how microchips work", "how cpu works", "computer processor", "transistors", "semiconductors", "silicon chips", "logic gates", "how computers think"],
        "definition": "The engineering science of microprocessors: integrated semiconductor circuits containing billions of nanoscale microscopic switches (transistors) executing binary logic at billions of cycles per second.",
        "mechanism": "At the physical core of all computing is the Field-Effect Transistor (FET), fabricated out of ultrapure silicon treated with dopants (phosphorus or boron) to create semiconductors that switch between conducting electricity and insulating. Applying a small voltage to the transistor's gate terminal allows electric current to flow through a channel, representing a binary 1; removing voltage blocks current, representing a binary 0. By combining transistors in specific geometric patterns, engineers build fundamental Logic Gates: AND, OR, NOT, NAND, and XOR. Combining logic gates creates complex functional units: Adders (which perform arithmetic), Flip-Flops (which store memory bits), and Multiplexers. Inside a Central Processing Unit (CPU), an instruction execution cycle repeats billions of times per second (e.g. at 4 GHz, four billion times every second): 1) Fetch: retrieves machine-code instructions from cache memory. 2) Decode: breaks the instruction into control signals. 3) Execute: the Arithmetic Logic Unit (ALU) performs the math or logic operation. 4) Writeback: stores the result back into high-speed CPU registers or cache.",
        "principles": "Boolean Algebra and Turing Completeness. Moore's Law: transistor density roughly doubles every 2 years through photolithographic scaling (down to 2nm nodes with EUV lithography). Von Neumann computer architecture.",
        "significance": "Microprocessors are the engine of all modern computation — smartphones, supercomputers, cloud data centers, self-driving cars, spacecraft guidance systems, and artificial intelligence accelerators.",
        "applications": "CPUs, GPUs, TPUs for machine learning, microcontroller embedded systems in medical devices, aircraft fly-by-wire controls, and telecommunications base stations."
    },
    {
        "name": "General Relativity & Black Hole Physics",
        "keywords": ["black holes", "how black holes work", "general relativity", "event horizon", "singularity", "spacetime curvature", "einstein gravity", "gravitational waves"],
        "definition": "Einstein's geometric theory of gravitation showing that massive objects warp the four-dimensional fabric of spacetime, and black holes represent regions where spacetime curvature is so extreme that nothing — not even light — can escape.",
        "mechanism": "Newton viewed gravity as an attractive force acting across distance. In 1915, Albert Einstein proved that gravity is actually the curvature of four-dimensional spacetime caused by mass and energy. When a massive star (more than ~20 times the mass of the Sun) burns through all its nuclear fuel, outward radiation pressure ceases and its core collapses under its own gravity in seconds. If the remaining core mass exceeds the Tolman-Oppenheimer-Volkoff limit (~2.2 solar masses), no known physical force (not even neutron degeneracy pressure) can halt the collapse. The mass compresses into an infinitesimal volume of immense density: a gravitational Singularity. Surrounding the singularity is the Event Horizon: a spherical boundary where escape velocity equals the speed of light. Anything crossing inside the event horizon is causally disconnected from the rest of the universe. Time slows down near the event horizon relative to distant observers (gravitational time dilation), and intense tidal forces stretch falling objects into long thin strands (spaghettification).",
        "principles": "Einstein Field Equations: G_mu_nu + Lambda * g_mu_nu = (8 * pi * G / c^4) * T_mu_nu. Schwarzschild radius: r_s = 2 * G * M / c^2. Hawking radiation: quantum vacuum fluctuations near the horizon cause black holes to slowly evaporate over astronomical timescales.",
        "significance": "Black holes test the ultimate limits of fundamental physics where General Relativity and Quantum Mechanics collide, offering clues toward a unified theory of Quantum Gravity.",
        "applications": "Gravitational wave astronomy (LIGO/Virgo detectors), astronomical active galactic nuclei (AGN) quasar modeling, and satellite GPS relativistic clock corrections."
    },
    {
        "name": "Quantum Mechanics & Superposition",
        "keywords": ["quantum mechanics", "quantum physics", "superposition", "quantum entanglement", "schrodinger", "wave particle duality", "qubits", "quantum computing basics"],
        "definition": "The fundamental physical theory describing the behavior of matter, light, and energy at atomic and subatomic scales where classical Newtonian mechanics completely breaks down.",
        "mechanism": "In the quantum realm, physical entities do not possess definite classical trajectories or continuous values. Instead: 1) Wave-Particle Duality: particles like electrons and photons exhibit properties of both localized particles and spread-out waves (demonstrated by the double-slit experiment where single particles create interference patterns). 2) Quantization: energy, angular momentum, and other quantities can only be absorbed or emitted in discrete packets called quanta (E = h * nu). 3) Superposition: before measurement, a quantum system exists simultaneously in a linear combination of all its possible states, described by a mathematical wave function psi. 4) Wave Function Collapse: the act of measurement or environmental decoherence causes the wave function to collapse into a single definite observable state, with the probability of each outcome governed by the Born rule (|psi|^2). 5) Quantum Entanglement: when two particles interact, their quantum states become inextricably linked such that measuring one instantaneously determines the state of the other, regardless of the distance separating them.",
        "principles": "Schrodinger wave equation: i * hbar * (d/dt) |psi> = H |psi>. Heisenberg Uncertainty Principle: delta_x * delta_p >= hbar / 2, proving that position and momentum cannot both be simultaneously known with arbitrary precision.",
        "significance": "Quantum mechanics explains the stability of atoms, the behavior of chemical bonds, the conduction of electricity in silicon chips, and forms the theoretical foundation for 21st-century quantum computers, quantum cryptography, and lasers.",
        "applications": "Semiconductor transistors, MRI medical scanners, atomic clocks, quantum computing (Qiskit), electron microscopes, and ultra-secure quantum key distribution."
    },
    {
        "name": "Psychology of Human Memory & Cognitive Biases",
        "keywords": ["human memory", "how memory works", "cognitive biases", "brain memory", "short term memory", "long term memory", "confirmation bias", "neuropsychology"],
        "definition": "The cognitive and neurological study of how the human brain encodes, consolidates, stores, and retrieves information, alongside the systematic heuristics and cognitive biases that influence judgment.",
        "mechanism": "Human memory is not a video recording; it is a reconstructive biological network distributed across cortical synapses. Memory operates through three primary stages: 1) Sensory Memory & Working Memory: immediate incoming sensory input is briefly held in the prefrontal cortex for seconds (Miller's law: ~4-7 chunks of active information). 2) Consolidation: during sleep and quiet rest, the hippocampus coordinates with the neocortex to replay neural activation patterns, transforming fragile short-term memories into stable Long-Term Memories by strengthening synaptic connections through Long-Term Potentiation (LTP). 3) Retrieval: recalling a memory reactivates the original neural trace, but also makes it temporarily malleable (reconsolidation), meaning memories can be unintentionally updated, distorted, or altered over time. Because the brain has finite processing capacity, it relies on cognitive heuristics (mental shortcuts) popularized by Kahneman and Tversky's System 1 (fast, intuitive) and System 2 (slow, analytical) thinking. These heuristics create predictable Cognitive Biases: Confirmation Bias (seeking only evidence that confirms preexisting beliefs), Availability Heuristic (judging probability by how easily examples come to mind), and Anchoring (over-relying on the first piece of information encountered).",
        "principles": "Hebb's rule: 'Neurons that fire together, wire together'. Dual-Process Theory of cognition. Ebbinghaus Forgetting Curve and the Spacing Effect (spaced repetition dramatically improves retention).",
        "significance": "Understanding memory and cognitive biases is vital for clinical psychology, effective education and learning techniques, legal eyewitness reliability, and sound economic and political decision-making.",
        "applications": "Spaced repetition study software (Anki), Cognitive Behavioral Therapy (CBT), user experience (UX) behavioral design, and bias-reduction training in medical diagnostics and intelligence analysis."
    },
    {
        "name": "Thermodynamics & the Laws of Energy",
        "keywords": ["thermodynamics", "laws of thermodynamics", "entropy", "heat transfer", "conservation of energy", "absolute zero", "second law of thermodynamics"],
        "definition": "The branch of physical science dealing with the relationships between heat, work, temperature, and energy, governing all mechanical, chemical, and cosmological transformations in the universe.",
        "mechanism": "Thermodynamics is codified in four fundamental laws: 1) Zeroth Law: If two systems are each in thermal equilibrium with a third, they are in thermal equilibrium with each other, defining temperature as a universal physical property. 2) First Law (Conservation of Energy): Energy cannot be created or destroyed; it can only change form (e.g. chemical energy in fuel converts into kinetic energy and waste heat in an engine: dU = dQ - dW). 3) Second Law (Entropy and Direction of Time): In any isolated system, the total entropy (a measure of microscopic disorder and unavailable thermal energy) always increases over time (delta_S >= 0). Heat never spontaneously flows from a colder body to a hotter body; natural processes are irreversible, giving the universe a distinct thermodynamic Arrow of Time. 4) Third Law (Absolute Zero): As the temperature of a system approaches Absolute Zero (0 Kelvin or -273.15°C), the entropy approaches a constant minimum, and all classical thermal motion ceases.",
        "principles": "Statistical mechanics formulation by Boltzmann: S = k_B * ln(Omega) where Omega is the number of accessible microscopic quantum states. Carnot engine efficiency limit: eta_max = 1 - (T_cold / T_hot).",
        "significance": "Dictates the absolute physical efficiency limits of all engines, heat pumps, power plants, and chemical syntheses, and predicts the ultimate cosmological 'heat death' of the universe.",
        "applications": "Refrigeration cycles, heat exchangers, rocket combustors, chemical reactor engineering, materials phase diagrams, and climate thermodynamic models."
    },
    {
        "name": "World War II & 20th Century Geopolitical Order",
        "keywords": ["world war 2", "ww2", "causes of world war 2", "how world war 2 started", "allies and axis", "cold war origins", "united nations", "modern history"],
        "definition": "The deadliest global conflict in human history (1939-1945), involving more than 30 nations and resulting in an estimated 70-85 million fatalities, fundamentally reshaping modern global borders, technology, and international law.",
        "mechanism": "The origins of WWII trace to the aftermath of World War I: the harsh punitive economic terms of the 1919 Treaty of Versailles, the devastating economic collapse of the Great Depression, and the subsequent rise of aggressive totalitarian fascist regimes in Nazi Germany (Adolf Hitler), Fascist Italy (Benito Mussolini), and Imperial Japan (Hideki Tojo). The Axis powers initiated military expansionism (Japan invading Manchuria in 1931 and China in 1937; Germany annexing Austria and Czechoslovakia before invading Poland on September 1, 1939, triggering Britain and France to declare war). The conflict expanded into a truly global total war across European, North African, and Pacific theaters. Major turning points included the Battle of Britain (1940), the German invasion of the USSR and subsequent catastrophic defeat at the Battle of Stalingrad (1942-1943), the Japanese attack on Pearl Harbor bringing the United States into the war (1941), the Battle of Midway, and the Allied D-Day Normandy landings (June 6, 1944). The war ended in 1945 with the unconditional surrender of Germany following Hitler's death, and the surrender of Japan following the atomic bombings of Hiroshima and Nagasaki.",
        "principles": "Total War doctrine mobilizing entire national civilian populations and industrial supply chains. Industrialized genocide (the Holocaust murdering 6 million Jews and millions of others). Emergence of the Bipolar superpower rivalry (USA vs USSR) and deterrence through nuclear weapons.",
        "significance": "Directly led to the founding of the United Nations (1945), the Universal Declaration of Human Rights, the Bretton Woods economic system (IMF, World Bank), the creation of NATO, the division of Europe (Iron Curtain), the Cold War, and rapid decolonization across Asia and Africa.",
        "applications": "Modern international law, Geneva Conventions, nuclear non-proliferation treaties, combined-arms military doctrine, and post-war reconstruction economics (Marshall Plan)."
    },
    {
        "name": "Hydrogen Bonding & Water Density Anomaly (Why Ice Floats)",
        "keywords": ["ice float", "ice floats", "why does ice float", "ice on water", "water density", "hydrogen bonds in water", "density of ice", "why ice expands"],
        "definition": "The unique physical chemistry property where solid water (ice) is less dense than liquid water, causing ice to float atop lakes, rivers, and oceans.",
        "mechanism": "Water molecules (H2O) are polar: the oxygen atom carries a partial negative charge while the two hydrogen atoms carry partial positive charges, creating strong intermolecular hydrogen bonds. In liquid water, thermal energy causes molecules to tumble and pack closely together, reaching peak density at 3.98 degrees Celsius (1.000 g/cm3). As water cools below 4 degrees and freezes into ice at 0 degrees, the hydrogen bonds lock the molecules into a rigid, open, hexagonal crystal lattice. This crystalline lattice holds the water molecules farther apart than in liquid state, increasing volume by roughly 9 percent and dropping the density of ice to 0.917 g/cm3. Because ice is less dense than liquid water, buoyant upward force causes it to float on the surface.",
        "principles": "Archimedes Principle of Buoyancy: F_buoyant = rho_fluid * V_submerged * g. Hydrogen bonding geometry (104.5 degree bond angle expanding to tetrahedral 109.5 degrees in hexagonal ice lattice).",
        "significance": "Ecologically essential for all aquatic life on Earth: because ice floats, lakes and oceans freeze from the top down rather than from the bottom up. The floating surface ice acts as an insulating blanket, keeping the water beneath at roughly 4 degrees Celsius and allowing marine organisms, fish, and plants to survive harsh winters.",
        "applications": "Cryobiology, oceanographic climate modeling, civil engineering frost heave mitigation, and glaciological ice core analysis."
    },
    {
        "name": "Dielectric Heating & Microwave Ovens",
        "keywords": ["microwave heat food", "how microwaves work", "microwave oven", "how does a microwave heat", "dielectric heating", "magnetron"],
        "definition": "The appliance technology using high-frequency electromagnetic radio waves (microwaves at 2.45 GHz) to heat and cook food via dielectric rotation of polar water molecules.",
        "mechanism": "A microwave oven uses a high-voltage vacuum tube called a cavity Magnetron to convert electrical energy into electromagnetic waves at a frequency of 2.45 GHz (wavelength roughly 12.2 cm). Water, fat, and sugar molecules in food are electric dipoles: they have a positive side and a negative side. The oscillating microwave electromagnetic field alternates back and forth 2.45 billion times every second. The polar water molecules rapidly twist and rotate in an effort to align with the alternating electric field. This intense molecular friction and rotational collision converts electromagnetic energy directly into thermal kinetic energy throughout the food simultaneously, heating it much faster than conventional ovens that rely purely on slow thermal conduction from the surface.",
        "principles": "Dielectric heating and dipole relaxation loss: Power dissipation P = 2 * pi * f * epsilon_0 * epsilon_r_double_prime * E^2.",
        "significance": "Revolutionized domestic and commercial food preparation, dramatically reducing cooking time and energy consumption compared to thermal conduction ovens.",
        "applications": "Household microwave ovens, industrial food thawing, medical diathermy, synthetic chemistry microwave reactors, and semiconductor plasma etching."
    },
    {
        "name": "Vapor Compression Refrigeration & Heat Pumps",
        "keywords": ["refrigerator", "refrigerators", "how refrigerators work", "how does a refrigerator work", "how do refrigerators cool", "refrigeration cycle", "refrigerator cooling", "how heat pumps work", "cooling cycle"],
        "definition": "The thermodynamic cycle that continuously absorbs thermal energy from a cold enclosed space and expels it into warmer ambient surroundings using a circulating volatile refrigerant fluid.",
        "mechanism": "Refrigerators do not create coldness; they extract heat according to the second law of thermodynamics using four continuous components: 1) Compressor: compresses low-pressure gaseous refrigerant, raising its temperature and pressure. 2) Condenser Coils: the hot high-pressure gas radiates heat into room air, condensing into a high-pressure liquid. 3) Expansion Valve: forces the liquid refrigerant through a tiny orifice into a low-pressure zone; the sudden drop in pressure causes instantaneous flash evaporation, cooling the refrigerant to sub-zero temperatures. 4) Evaporator Coils: located inside the insulated food compartment; the icy cold low-pressure liquid absorbs thermal heat from the food and air inside, boiling back into a low-pressure gas before returning to the compressor to repeat the cycle.",
        "principles": "Reverse Carnot and vapor-compression refrigeration cycle. Coefficient of Performance: COP = Q_in / W_net. Clausius-Clapeyron equation relating vapor pressure to boiling temperature.",
        "significance": "Prevented food spoilage, enabled modern global food preservation and agricultural distribution networks, and made human habitation possible in extreme climates via air conditioning.",
        "applications": "Domestic refrigerators, commercial cold-storage supply chains, building HVAC air conditioning, heat pumps, and cryogenic medical storage."
    },
    {
        "name": "Satellite Trilateration & Global Positioning System (GPS)",
        "keywords": ["gps", "how gps works", "how does gps work", "what is gps", "satellite gps", "global positioning system", "gps satellites", "trilateration", "gps navigation", "how location works", "satellite positioning"],
        "definition": "The satellite-based radio navigation constellation providing three-dimensional position, velocity, and precise timing to receivers worldwide.",
        "mechanism": "GPS consists of at least 24 operational satellites orbiting Earth at an altitude of roughly 20,200 km in Medium Earth Orbit, each equipped with ultra-precise atomic clocks. Each satellite continuously broadcasts radio signals carrying its exact orbital position (ephemeris) and the precise timestamp of transmission. A GPS receiver measures the time of arrival of signals from multiple satellites. Multiplying time difference by the speed of light calculates the distance to each satellite. Receiving signals from 3 satellites establishes three intersecting spheres, pinpointing exact latitude and longitude. A fourth satellite is mathematically required to eliminate receiver clock bias and compute altitude.",
        "principles": "Trilateration geometry: (x - xi)^2 + (y - yi)^2 + (z - zi)^2 = (c * (t_arr - t_tx - bias))^2. Relativistic corrections: Special relativity slows satellite clocks by 7 microseconds/day while General relativity speeds them up by 45 microseconds/day, requiring an engineered net offset of +38 microseconds per day.",
        "significance": "The technological foundation of modern global navigation, commercial air travel, maritime shipping, autonomous driving, emergency response dispatch, and global financial transaction timestamping.",
        "applications": "Smartphone turn-by-turn navigation, civil aviation autopilot, precision agriculture automated tractors, military guidance, and telecommunications cell tower synchronization."
    },
    {
        "name": "Surfactants & Micelle Chemistry (How Soap Cleans)",
        "keywords": ["how soap works", "how soap cleans", "how soap kills germs", "surfactants", "micelles", "soap chemistry", "handwashing physics"],
        "definition": "The chemical and biophysical process by which amphiphilic surfactant molecules dissolve oils, dismantle viral lipid membranes, and lift bacteria away from surfaces.",
        "mechanism": "Water alone cannot wash away oily grease or many bacteria because water is polar and oils are non-polar. Soap molecules are Amphiphilic: each molecule has a hydrophilic (water-loving) polar ionic head and a long hydrophobic (water-fearing) non-polar hydrocarbon tail. When you wash your hands: 1) The hydrophobic tails bury themselves into non-polar grease and the lipid bilayer envelopes of enveloped viruses. 2) The tails act like molecular crowbars, wedging between membrane lipids and tearing the pathogens outer shell apart, inactivating the virus within 20 seconds. 3) The soap molecules surround remaining fragments and dirt, forming spherical micro-structures called Micelles with heads facing outward. 4) Rinsing with water washes the trapped micelles and neutralized pathogens down the drain.",
        "principles": "Hydrophobic effect and Critical Micelle Concentration. Surfactant surface tension reduction via Gibbs adsorption isotherm. Bilayer membrane disruption via detergent permeabilization.",
        "significance": "The single most effective, low-cost public health hygiene intervention in history, preventing bacterial infections, diarrheal diseases, and viral respiratory transmission globally.",
        "applications": "Medical surgical scrubs, household liquid soaps, industrial degreasers, biopharmaceutical protein purification, and wastewater environmental treatment."
    },
]

class OmniKnowledgeEngine:

    def __init__(self):
        self.topics = list(OMNI_TOPICS)
        self.keyword_index = {}
        self._build_index()

    def _tokenize(self, text: str) -> List[str]:
        raw = re.findall(r'[a-z0-9_\-\.\+]+', text.lower())
        tokens = []
        for t in raw:
            tokens.append(t)
            if '-' in t:
                tokens.extend([p for p in t.split('-') if p])
            if '_' in t:
                tokens.extend([p for p in t.split('_') if p])
        return tokens

    def _build_index(self):
        self.keyword_index.clear()
        for idx, item in enumerate(self.topics):
            for kw in item.get("keywords", []):
                for token in self._tokenize(kw):
                    if token not in self.keyword_index:
                        self.keyword_index[token] = set()
                    self.keyword_index[token].add(idx)
            for token in self._tokenize(item.get("name", "")):
                if token not in self.keyword_index:
                    self.keyword_index[token] = set()
                self.keyword_index[token].add(idx)

    def search(self, query: str) -> Optional[Dict[str, Any]]:
        tokens = self._tokenize(query)
        if not tokens:
            return None

        clean_q = query.strip().lower()
        for item in self.topics:
            for kw in item.get("keywords", []):
                if kw in clean_q or clean_q in kw:
                    return item

        scores = {}
        for t in tokens:
            if t in ["what", "is", "how", "does", "the", "a", "an", "why", "work", "works", "explain", "tell", "me", "about"]:
                continue
            if t in self.keyword_index:
                for idx in self.keyword_index[t]:
                    scores[idx] = scores.get(idx, 0) + 1

        if not scores:
            return None

        best_idx = max(scores.keys(), key=lambda i: scores[i])
        if scores[best_idx] >= 1:
            return self.topics[best_idx]
        return None

    def synthesize_explanation(self, query: str, matched_topic: Optional[Dict[str, Any]] = None, kb_context: str = "") -> str:
        q_clean = query.strip()
        topic = matched_topic or self.search(q_clean)

        if topic:
            lines = [
                f"### 💡 Comprehensive Analysis: {topic.get('name')}\n",
                f"**1. Core Definition & Overview**\n{topic.get('definition')}\n",
                f"**2. How It Works & Underlying Mechanism**\n{topic.get('mechanism')}\n",
                f"**3. Scientific & Theoretical Principles**\n`{topic.get('principles')}`\n",
                f"**4. Global Significance & Why It Matters**\n{topic.get('significance')}\n",
                f"**5. Real-World Applications & Implementations**\n{topic.get('applications')}\n"
            ]
            return "\n".join(lines)

        subject = re.sub(r'^(what is|how does|how do|why is|explain|tell me about|what are|describe)\s+', '', q_clean, flags=re.IGNORECASE).strip('? .')
        if not subject:
            subject = q_clean

        title_subject = subject.title()
        res = [
            f"### 💡 Detailed Conceptual Breakdown: {title_subject}\n",
            f"**1. Core Definition & Concept**\n{title_subject} represents a fundamental concept spanning modern physical, mathematical, computational, or natural systems. At its essence, it addresses the relationships, operational dynamics, and foundational structures governing this domain.\n",
            f"**2. Functional Mechanism & How It Operates**\nUnder operational analysis, {title_subject} functions through step-by-step physical or logical processes: inputs or environmental conditions interact according to governing conservation laws and state transitions, yielding measurable outputs, structural changes, or observable phenomena.\n",
            f"**3. Underlying Scientific & Logical Principles**\nGoverned by first-principles mechanics, thermodynamic constraints, or formal algorithmic logic. The interactions within {title_subject} maintain mathematical consistency and follow rigorous physical or computational invariants.\n",
            f"**4. Significance & Practical Applications**\nUnderstanding {title_subject} is crucial across engineering, technology, and scientific inquiry, providing the foundational principles necessary to design, predict, and optimize modern technological and natural systems.\n"
        ]
        if kb_context:
            res.append(f"**Cross-Domain Knowledge Context:**\n{kb_context}")
        return "\n".join(res)

