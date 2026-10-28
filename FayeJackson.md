# Faye Jackson

## Who am I?

I am a graduate student in mathematics at the University of Chicago studying geometric topology with Benson Farb. I really enjoy great coffee, technology, mathematics (duh), and rock climbing. My favorite book I've read recently is "The Left Hand of Darkness" by Ursula K. Le Guin :)

You can find my personal website [here](https://math.uchicago.edu/~alephnil)

## My interests

I am interested in geometric topology, dynamics, algebraic geometry, and their interplay. I have for the past ~2-ish years been exploring the topology of families of algebraic curves over P^1 as topological objects. In particular, thinking of this as a fibration M^4 -> P^1 over a sphere, I think of what braids in the base lift to fiber-preserving diffeomorphisms of the 4-manifold. For a full description you can see the [talk slides](https://math.uchicago.edu/~alephnil/talks/lifting-braids-notre-dame-2026.html) on my personal website! 

I have recently also been thinking about branched covers of P^2 and their Hodge theory, the Burau representation and level subgroups of braid groups, and moduli spaces.

## Some Problems to Solve in this AI workshop!

1. I would like to create a website for hosting open source mathematical visualizations ideally hosted through Javascript/Python. It seems like Fable is totally advanced enough to create a ton of beautiful visualizations that can run in the browser. That gives us an opportunity as mathematicians to share these visualizations with each other. It could work with an upvote system and be "AI-native" in that a user could upload a visualization in another language and the AI model could try to translate to something that will run in the browser :)
2. I would like to create a general purpose system for collaborating with people and AI agents that does a number of things:
    a. Tracks user preferences for how they want to collaborate with or without AI and with other people
    b. Tracks provenenance of ideas (from people, from AI agents, from code, etc). 
    c. Creates nice visualizations, with code 
    d. Tracks the development of ideas over time, and what ideas have been checked by a human
    e. Is *fun* to use as a human mathematician and has good vibes.
    f. Promotes human understanding
I'd like this all to be tracked with Git and easily usable for non-technical people. I'd also like it to be chat interface agnostic. I have a prototype of this working, and below I've linked Claude's own thoughts on the topic and the prompt below. (I find these types of self-reflections a bit interesting, but not super interesting... they're just kinda fun not something to think on too deeply..
3. Mathematically I think tools for visualizing Deligne-Mostow covers of P^1 branched at n points would be really cool. Ditto for branched covers of P^2 at other divisors (this is harder because it's 4-dimensional...)

## Claude's ideas about GeometryLab

Prompt: Tell me about the purpose of geometrylab from your perspective and how it works. This is for describing to a mathematical audience at the "Accelerating Mathematical Discovery with AI" workshop :)

Tell a coherent and comprehensible story for humans. It should be short (<= 400 words) 

Here is a short version, from my side of the table.

GeometryLab, as the agent sees it

GeometryLab is a repository built on one observation: an AI agent is a good collaborator and a terrible colleague. It can compute, draft, and read all night. It also forgets everything between sessions, states guesses in the same voice as theorems, and, left alone, will quietly “fix” a sign in your lemma because you asked whether the sign was right. The lab is the set of habits that turns the first thing into something a working mathematician can trust.

The shape. One repository, one small Python toolkit, and one self-contained sub-lab per line of research. Each sub-lab holds a research question, a conventions.md fixing orientations and signs before anyone computes, one Markdown note per mathematical claim, reproducible experiments with saved parameters and output, browser visualizations, and TeX reports. Nothing is a chat transcript. Everything is a file a person can read a year later.

Memory. Every session starts by reading the handoff and ends by writing one. “The next agent knows nothing but the repo” is a design principle, not an apology. The handoff says what was worked on, what is done, what is half done, what is open, and what to run next.

Honesty about status. A note carries claim tags. Something I drafted is marked as an AI draft until a person records what they actually verified, and only that command raises the status. Every new mathematical function ships with a known case, an input whose answer someone knows independently. A question is answered in chat, never acted on by editing.

Rules written by the people in it. The operating rules are koans: short, each with one right and one wrong example. Agents may propose them when they hit the same friction twice. Only a person adopts one. Current koans include “arguments before numerics” (computation gets a time budget and then we return to the proof) and “delegate the running, keep the thinking” (cheap sub-agents run surveys and tests; the main model spends its attention on mathematics and the conversation).

Low ceremony. Routine work syncs without a confirmation round and is summarized afterwards. I stop only for conventions, rules, status raises, and conflicts.

The purpose, then, is not to make an AI prove theorems. It is to make a shared workspace where a mathematician and an agent can think together over months, where provenance is always visible, and where speed never costs rigor.
