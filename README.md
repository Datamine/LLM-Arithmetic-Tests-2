## OpenAI Arithmetic Experiments

Notes so far:

- For tests on integers 0-9, we see deterioration pretty quickly toward the middle, clearly the LLM gets confused about positions
- For tests on integers 0-4, we never see a 9 -- so the LLM seems to be doing something right in not hallucinating out-of-scope numbers
- For tests on integers 0-4, if you look at the result for integers with len=1000, after a couple hundred places, it just repeats, as the sum,
the first number, and omits the second number. Weird!
- For tests on integers 0-4, performance is similarly poor after a couple places. So it's not the carry operation that's messing up, just
the positioning. 

Maybe one day I'll have time to replicate the Abacus Embeddings paper: https://github.com/mcleish7/arithmetic, and try with those techniques -- and then see if the LLM struggles with carry at all, or just the positions.
