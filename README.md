## OpenAI Arithmetic Experiments

Following some [prior work](https://github.com/Datamine/OpenAI-Arithmetic)

Objective: as I wrote in a [recent blogpost](https://loeber.substack.com/p/21-everything-we-know-about-llms):
```
There’s an interesting open question as to whether LLMs suffer from: 
a) Not having enough working memory to store and transform intermediate results — for example, “carrying” in addition, or adding up intermediate sums for multiplication;
b) Not being able to apply enough attention to every token in the sequence, thereby losing some information that then causes arithmetic error.
```

In this experiment, I try to answer this question: how confused do LLMs get by "carrying"? My idea is that I'll add integers that never require any carrying, and see 
if that performs any better than integer addition that does require carrying.

Notes so far:

- For tests on integers 0-9, we see deterioration of accuracy pretty quickly toward the middle, clearly the LLM gets confused about positions
- For tests on integers 0-4, we never see a 9 -- so the LLM seems to be doing something right in not hallucinating out-of-scope numbers
- For tests on integers 0-4, if you look at the result for integers with len=1000, after a couple hundred places, it just repeats, as the sum,
the first number, and omits the second number. Weird!
- For tests on integers 0-4, performance is similarly poor after a couple places. So it's not the carry operation that's messing up, just
the positioning. 

Next up:
- compare results between integers 0-9 and integers 0-4: does the deterioration of accuracy happen at the same rate? We can test this by looking at the statistical distribution of correct vs. incorrect digits.
For each digit in the completion string, we can state the probability that the LLM gets it right or wrong. If we do many samples (e.g. 100 experiments) then we'll be able to state for each digit place, the % probability
that the LLM calculates it correctly, and we're able to compare that against the base rate of random chance (e.g. 10% or 20% for the two tests, respectively? would have to check).

- Try to replicate the Abacus Embeddings paper: https://github.com/mcleish7/arithmetic, and try with those techniques -- and then see if the LLM struggles with carry at all, or just the positions.
- Repeat the whole thing with multiplication. Carry in arithmetic is easy because you're only ever carrying one 1 forward at each place -- so you don't need intermediate storage, you can do everything in-place,
which might work well for a transformer. Multiplication is much trickier since you need to store and add many intermediate results.
