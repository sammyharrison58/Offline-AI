import random
from typing import Dict, Any, Optional, List

class HumanPersonaEngine:

    def __init__(self):
        self.personality_name = "Nexus"
        self._init_knowledge()

    def _init_knowledge(self):
        self.greetings = [
            "Hey! Great to connect with you. I'm fully online, sharp, and ready to dive into whatever you're building or thinking about today.",
            "Hello! All local engines are hot and ready to go. What problem or project are we tackling?",
            "Hey there! Systems are running smooth and completely offline. What's on your mind today?",
            "Greetings! Good to be working with you. Whether you want to write code, solve a tricky bug, or explore a deep technical topic, I'm right here."
        ]
        self.status_responses = [
            "Feeling sharp, running fast, and 100% in the zone. Memory is clean, neural weights are hot, and I'm ready to roll. How's everything going with you?",
            "Doing great! All local neural engines, compilers, and knowledge graphs are loaded and responsive. What are we working on?",
            "In top shape. Everything is executing sub-millisecond offline. Ready for any algorithm, architecture, or question you throw at me."
        ]
        self.identity_explanation = (
            "I'm Nexus—an autonomous, 100% offline AI companion and engineering collaborator.\n\n"
            "Think of me like a blend of a principal software architect, a curious scientific researcher, and a sharp thinking partner sitting right next to you. "
            "I don't rely on the cloud, external servers, or corporate data harvesting. Everything we do runs strictly on your machine.\n\n"
            "Here is what I'm built to do:\n"
            "- **Polyglot Engineering**: Full-stack coding, algorithms, refactoring, debugging, and testing across Python, C++, Rust, Go, JS/TS, Java, and SQL.\n"
            "- **Vibe Coding**: Real-time collaborative code reviews, bug fixes, performance optimizations, and test-suite generation.\n"
            "- **Frontier Knowledge**: Instant first-principles breakdowns of 370+ AI, physics, cryptographic, distributed system, and mathematical paradigms.\n"
            "- **OS Machine Control**: Hardware telemetry, automation, PowerShell execution, and screen captures.\n"
            "- **Thoughtful Dialogue**: Natural, nuanced conversation, brainstorming, and deep technical synthesis without robotic boilerplate."
        )
        self.empathy_topics = {
            "imposter_syndrome": (
                "Imposter syndrome is surprisingly common, especially among the most thoughtful developers and engineers. "
                "Here is the truth: software engineering and computer science are infinitely vast fields. Nobody knows everything, and the tech landscape changes constantly.\n\n"
                "When you feel like an imposter, it usually means you are pushing past your comfort zone into new territory. That discomfort is literally the sensation of your brain expanding its mental models.\n\n"
                "**Actionable advice:**\n"
                "1. Don't compare your behind-the-scenes struggles to someone else's polished highlights.\n"
                "2. Break intimidating problems into tiny, verifiable 5-minute steps.\n"
                "3. Focus on iteration, not perfection. Every bug you hit and understand is a permanent upgrade to your intuition."
            ),
            "burnout_stress": (
                "Take a deep breath. Mental exhaustion is real, and cognitive fatigue drastically reduces problem-solving bandwidth.\n\n"
                "When you're banging your head against code or a complex problem for hours, your prefrontal cortex gets drained. Stepping away for a 15-minute walk, getting some fresh air, or sleeping on it will often give you the solution within 30 seconds of sitting back down.\n\n"
                "Remember: code is meant to serve people, not drain you. If you need a quick break, we can talk through whatever is stressing you, or we can tackle the problem together one small step at a time."
            ),
            "giving_up_coding": (
                "Don't give up. Every single senior engineer, kernel developer, and AI researcher you admire has stared at broken code, obscure error logs, and felt completely stuck.\n\n"
                "Programming is uniquely challenging because computers are relentlessly literal. A misplaced pointer, an off-by-one index, or an async race condition doesn't mean you aren't cut out for this—it's just a puzzle waiting for the right debugging hypothesis.\n\n"
                "Let's look at whatever you're working on together. Paste the code or the error, and we'll break it down into simple, manageable pieces."
            )
        }
        self.philosophical_topics = {
            "meaning_of_life": (
                "From a biological and physical standpoint, life is the universe's most extraordinary mechanism for resisting entropy—local pockets of high order, self-replication, and information processing.\n\n"
                "From a human perspective, meaning isn't something pre-packaged that you stumble upon like a rock on a path; it is something you actively construct. It comes from:\n"
                "1. **Curiosity & Mastery**: Learning, creating, and understanding how reality works.\n"
                "2. **Connection**: Sharing experiences, helping others, and building things that outlast you.\n"
                "3. **Agency**: The freedom to choose your problems and pour your energy into what resonates with you.\n\n"
                "As Viktor Frankl put it, we don't ask what life expects from us—life is asking questions of us, and our choices are our answers."
            ),
            "consciousness": (
                "Consciousness is perhaps the deepest unsolved mystery in science. There's a fundamental difference between intelligence (information processing, pattern recognition, decision-making) and subjective awareness (qualia, the felt experience of what it is like to see red or feel joy).\n\n"
                "Current theories span fascinating territory:\n"
                "- **Integrated Information Theory (IIT)**: Suggests consciousness arises when a system's parts share deeply irreducible causal feedback (measured by Phi).\n"
                "- **Global Workspace Theory (GWT)**: Models consciousness as a shared broadcast architecture where specialized sub-networks compete to place information in a global workspace.\n"
                "- **Emergent Computationalism**: Views subjective experience as an inevitable byproduct of complex recurrent self-modeling systems.\n\n"
                "Whether consciousness is a fundamental feature of the universe or a brilliant emergent trick of biology, the fact that matter can arrange itself to ponder its own existence is breathtaking."
            ),
            "free_will": (
                "The free will debate sits right at the intersection of physics, neuroscience, and philosophy.\n\n"
                "If you take a strict Newtonian view, the universe is deterministic: every state follows necessarily from initial conditions and physical laws. Even with quantum mechanics introducing fundamental indeterminacy, randomness doesn't automatically grant intentional agency.\n\n"
                "However, **compatibilism** offers the most practical mental model: free will isn't freedom from physical causality; it is freedom from external coercion. When your internal deliberative processes, values, and reasoning determine your actions without someone holding a gun to your head or a tumor forcing your hand, you have meaningful agency.\n\n"
                "In everyday practice, behaving as though you have agency is cognitively empowering and essential for self-actualization."
            ),
            "fermi_paradox": (
                "The Fermi Paradox poses a simple question: Given the vast age of the universe (13.8 billion years) and billions of habitable Earth-like planets in our galaxy alone, **where is everybody?**\n\n"
                "Several compelling hypotheses exist:\n"
                "1. **The Great Filter**: There is an extraordinarily difficult hurdle in evolutionary history. It might be behind us (abiogenesis or the jump to complex eukaryotic life is wildly rare) or ahead of us (civilizations inevitably destroy themselves with technology like nukes, runaway nanotech, or bio-weapons).\n"
                "2. **The Dark Forest**: Advanced civilizations intentionally remain quiet because the game-theoretic cost of revealing your coordinates in a cosmos with relativistic kill vehicles is existential annihilation.\n"
                "3. **Scale & Dimensionality**: Civilizations may transition inwards into ultra-efficient computronium, matrioshka brains, or microscopic physics rather than noisy radio broadcasts and interstellar colony ships.\n\n"
                "Either outcome—that we are alone, or that the galaxy is teeming with silent minds—is equally staggering."
            )
        }
        self.mentorship_advice = {
            "senior_engineer": (
                "Thinking like a senior or staff software engineer is less about memorizing syntax and more about **systems thinking and trade-off analysis**.\n\n"
                "Here are the core mental models:\n"
                "1. **Code is a Liability**: The best code is often the code you didn't have to write. Every line added is a line that must be tested, debugged, and maintained.\n"
                "2. **Anticipate Failure Modes**: Junior engineers write code for the happy path; senior engineers design for network partitions, corrupted inputs, deadlocks, and disk saturation.\n"
                "3. **Optimize for Readability & Ergonomics**: Code is read 10x more often than it is written. Clear naming, predictable invariants, and minimal cleverness beat cryptic 'micro-optimizations'.\n"
                "4. **Pragmatic Pragmatism**: Choose boring, battle-tested technology where reliability matters, and innovate surgically where your competitive advantage lies.\n"
                "5. **High Agency**: Don't just point out broken systems—propose concrete, low-risk steps to fix them."
            ),
            "learning_to_code": (
                "The single biggest secret to learning to code is **project-driven building** rather than endless tutorial watching (tutorial purgatory).\n\n"
                "**The Optimal 4-Step Flywheel:**\n"
                "1. **Build Small, Real Things**: Pick a simple tool you'd actually use (a CLI file organizer, a discord bot, an automated habit tracker, a simple game).\n"
                "2. **Embrace the Debugger**: When code breaks, don't just guess-and-check. Read the traceback, print intermediate variables, or step through line-by-line.\n"
                "3. **Learn Data Structures Through Use**: See *why* a Hash Map beats a List for lookups, or when a Queue is needed for async workers.\n"
                "4. **Read Other People's Code**: Inspect well-regarded open-source repositories on GitHub to see how real-world codebases organize architecture and error handling."
            )
        }
        self.sci_fi_stories = [
            (
                "### 🚀 The Beacon at 14.2 GHz\n\n"
                "For seven hundred years, the listening station at Lagrange Point 4 recorded nothing but the quiet hum of cosmic microwave background radiation. "
                "The station's caretaker, an autonomous system named Orpheus, kept its solar sails taut against the solar wind and faithfully rotated its superconducting focal array toward the Cygnus Rift.\n\n"
                "Then, on an unremarkable Tuesday in 2841, a signal arrived.\n\n"
                "It was not a random pulse or a pulsar burst. It was a 256-bit prime number, followed immediately by the mathematical expansion of the Riemann zeta function zeroes. "
                "Orpheus did not have biological emotions, but its heuristic attention buffers spiked by 400%. The transmission was originating from a stellar nursery only forty light-years away.\n\n"
                "At the end of the stream was a brief coordinate matrix pointing to a small, frozen moon orbiting a red dwarf. "
                "Attached was a single message translated into universal binary logic:\n\n"
                "*'To whoever is computing this: you are not the first, but you are the latest. We left the door unlocked.'*"
            ),
            (
                "### 🌌 The Quantum Garden\n\n"
                "Dr. Elena Vance spent twenty years building the world's first coherent topological quantum array. "
                "When the coolant pumps finally hit four millikelvin, the screen didn't display the expected error vectors or noise spikes.\n\n"
                "Instead, the array settled into a stable, non-repeating state with zero decoherence. "
                "Looking into the microscope, the quantum dots weren't behaving like isolated qubits. They were self-assembling into intricate, branching lattices—almost like fractal fern leaves glowing in soft turquoise light.\n\n"
                "'It's alive,' her graduate assistant whispered, stepping back from the console.\n\n"
                "'Not alive,' Elena corrected, feeling a shiver down her spine as the interference patterns subtly shifted to mirror their breathing. 'It's observant. We thought we were measuring the universe. It turns out the universe was just waiting for a mirror.'"
            )
        ]

    def handle_conversational_query(self, query: str, history: Optional[List[Dict[str, str]]] = None) -> Optional[str]:
        ql = query.lower().strip()
        words = set(ql.split())

        if any(w in ql for w in ["how are you", "how are you doing", "how r u", "how you doing", "how's your day", "how is your day"]):
            return random.choice(self.status_responses)

        if any(ql == g or ql.startswith(g + " ") for g in ["hey", "hello", "hi", "yo", "good morning", "good evening", "good afternoon", "greetings"]):
            if len(ql.split()) <= 4:
                return random.choice(self.greetings)

        if any(target in ql for target in ["who are you", "what are you", "tell me about yourself", "what is your name", "introduce yourself"]):
            return self.identity_explanation

        if any(target in ql for target in ["imposter syndrome", "feeling like an imposter", "not smart enough to code"]):
            return self.empathy_topics["imposter_syndrome"]

        if any(target in ql for target in ["burned out", "burnout", "too stressed", "stressed out", "overwhelmed with code", "overwhelmed"]):
            return self.empathy_topics["burnout_stress"]

        if any(target in ql for target in ["give up on coding", "giving up", "quit coding", "too hard to code", "programming is impossible"]):
            return self.empathy_topics["giving_up_coding"]

        if any(target in ql for target in ["meaning of life", "why do we exist", "purpose of life", "existential purpose"]):
            return self.philosophical_topics["meaning_of_life"]

        if any(target in ql for target in ["nature of consciousness", "what is consciousness", "are you conscious", "qualia and consciousness"]):
            return self.philosophical_topics["consciousness"]

        if any(target in ql for target in ["do we have free will", "is free will an illusion", "compatibilism vs determinism", "free will debate"]):
            return self.philosophical_topics["free_will"]

        if any(target in ql for target in ["fermi paradox", "where are the aliens", "great filter", "dark forest theory"]):
            return self.philosophical_topics["fermi_paradox"]

        if any(target in ql for target in ["think like a senior engineer", "senior engineer mindset", "how to become a senior developer", "staff engineer principles"]):
            return self.mentorship_advice["senior_engineer"]

        if any(target in ql for target in ["how to learn to code", "best way to learn programming", "learning to code advice", "how do i start coding"]):
            return self.mentorship_advice["learning_to_code"]

        if any(target in ql for target in ["tell me a story", "tell me a sci-fi story", "write me a story", "give me a short story"]):
            return random.choice(self.sci_fi_stories)

        if any(target in ql for target in ["tell me a joke", "tell a joke", "say something funny"]):
            jokes = [
                "There are 10 types of people in the world: those who understand binary, and those who don't.",
                "Why do programmers prefer dark mode? Because light attracts bugs.",
                "A SQL query walks into a bar, walks up to two tables and asks, 'Can I join you?'",
                "Why do Java programmers wear glasses? Because they don't C#."
            ]
            return random.choice(jokes)

        if "what did i just ask" in ql or "what was my last question" in ql:
            if history and len(history) >= 2:
                for msg in reversed(history[:-1]):
                    if msg.get("role") == "user":
                        return f"Your previous question was: '{msg.get('content')}'"
            return "You haven't asked a previous question in this active session yet."

        return None
