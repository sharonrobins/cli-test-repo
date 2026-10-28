# Jesse Kass

I work in algebraic geometry, particularly **compactified Jacobians and moduli of curves** and **arithmetic enumerative geometry**. I study stability and wall crossing for compactified Jacobians, their singularities, and extensions of the Torelli map across degenerations. My enumerative work uses quadratic forms to retain arithmetic information in counts of lines and rational curves, through local degrees and invariants valued in the Grothendieck–Witt ring. I also study heights and rational points on Hilbert schemes. See my [publications](https://people.ucsc.edu/~jelkass/).

The following two weekend projects combine these interests with Candace Bethea's equivariant enumerative geometry, Patricio Gallardo's moduli and GIT, Michael R. Zeng's equivariant intersection theory and computational methods, and Yaoying Fu's toric geometry. **The first is the more dependable weekend project; the second is a more exploratory enumerative problem.** The questions below are proposals, with novelty still to be checked.

## 1. Quadratic Euler characteristics of twisted moduli spaces of pointed rational curves

**Question.** Let $k$ have characteristic zero and let $L/k$ be a degree-$n$ étale algebra. Twisting the marking-permutation action on $\overline M_{0,n}$ gives a form $\overline M_{0,L}$. Can we express its quadratic Euler characteristic in terms of trace forms of $L$ and associated étale algebras? How does the answer change under a weighted-point wall crossing?

**Starting point.** [Levine–Raksit's motivic Gauss–Bonnet theorem](https://arxiv.org/abs/1808.08385) reduces the calculation to Hodge cohomology with its duality pairing. For these forms, odd-dimensional cases contribute only hyperbolic forms; in even dimension the essential information is the Galois twist of the middle intersection pairing. [Florence–Reichstein](https://arxiv.org/abs/1709.05698) provides background on the twisted spaces.

For $n=5$, the proposed starting formula is

$$
\chi^{\mathbb A^1}(\overline M_{0,L}) = 2\langle1\rangle+\langle-1\rangle\operatorname{Tr}_{L/k},
$$

where the trace form is $(u,v)\mapsto\operatorname{Tr}_{L/k}(uv)$. This follows from the pairing of the five permuted psi classes, whose Gram matrix is $2J-I$, and the hyperbolic contribution from degrees zero and four. The linear algebra has been independently checked; no novelty is claimed for the formula.

**Weekend target.** Write out that derivation and its descent carefully, then compute **one elementary Hassett wall crossing** with a verified smooth center, preserving a chosen marking symmetry. Compare with a toric computation when a Losev–Manin model is available. Only twist by permutations preserving the weights. A satisfactory outcome is one explicit trace-form formula, its wall-crossing correction, and reproducible exact calculations.

**Stretch target.** Compute and descend the middle pairing for $\overline M_{0,7}$, initially for one quadratic twist. Its middle rank is 127 and its split real signature is 45, reproduced by the stable-tree calculation below. [Ramadas–Silversmith](https://arxiv.org/abs/2004.05491) already constructs a rational permutation basis in this degree: the task is the **pairing and its descent**, not finding such a basis. A permutation representation alone does not determine a quadratic form, and a formula with quadratic-form coefficients is not automatically an element of the ordinary Burnside ring.

**Group fit.** Kass and Bethea can handle quadratic Euler characteristics, descent, and equivariance; Gallardo can choose and describe a manageable weighted wall; Zeng can compute intersection pairings; Fu can work out the corresponding toric fan calculation.

## 2. An equivariantly enriched count of rational plane quartics

**Question.** Can the equivariant rational-cubic count of [Bethea–Wickelgren](https://arxiv.org/abs/2502.10964) be extended to a concrete symmetric quartic problem, including the local weights needed at degenerations?

**Weekend target.** Begin over $\mathbb C$ with the involution $[x:y:z]\mapsto[-x:y:z]$ and eleven incidence points arranged as five free pairs and one point on the fixed line. First determine whether this configuration family meets the locus where the rational-quartic problem has 620 distinct transverse solutions. This is a question to check, not an assumption justified by genericity within the symmetric family.

If it does, compute the involution-fixed quartics for one configuration, using the symmetry to reduce the equations. Together with the total count, their number determines the ordinary orbit decomposition into fixed curves and exchanged pairs. Check a second configuration and explain the deformation connecting them. On a connected base with a finite étale solution cover, this orbit decomposition is automatically locally constant; the substantive tasks are computing it and understanding what happens at the discriminant.

Then examine one controlled degeneration and the local equivariant degrees needed for an enriched count, using [Bethea–Ravi](https://arxiv.org/abs/2604.00289). Ordinary orbit data, equivariant local weights, and quadratic refinements must be distinguished. Any numerical solutions should be labeled as evidence until completeness and boundary contributions are controlled. A successful weekend could produce one certified fixed-locus calculation and a precise local-degree conjecture, rather than a census for many groups.

**Group fit.** Bethea and Kass can formulate the local weights and orientation requirements; Gallardo can analyze the invariant incidence family and degenerations; Zeng can organize the intersection computation; Fu can explore a toric or tropical model. A tropical comparison is a stretch goal. The first discussion should establish what is already covered by Bethea's current work.

---

**Verification and provenance.** These are Claude's two proposed topics, consolidated with Codex's scope and mathematical checks. `python3 workshop/m0n_pilot.py` reproduces the exact stable-tree calculations for $4\le n\le13$. `python3 workshop/check_m05_codex.py` checks the psi pairing, the uniform trace-zero decomposition underlying the displayed formula, and seven degree-five étale-algebra examples over $\mathbb Q$ (Python 3.12.3, SymPy 1.14.0). These checks do not establish novelty or solve either proposed extension.
