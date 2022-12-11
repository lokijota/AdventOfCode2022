# Advent of Code 2022

Last year I did this with C# and struggled with the lack of dynamic constructs available in languages like Python, so this year going at it with Python. Less familiar with it, not Pythonic code in general, but that's not stopping me :-).

**Challenge 11 part 2** was the first challenging one, where brute force iteration can't make it. I went around in circles looking at prime factorization (obvs too slow), and concluding that must continuing to do adds/multiplications wouldn't work due to ever huge numbers. So the solution had to be simpler and via another path. The numbers of the module are all the lower primes, but ended up not using that. Essentially looked for patterns, in the # of iterations, and after about 50 rounds my key two top monkeys (#2 and #7) showed regularies when adding in blocks of 3 (sum = 36). So I just used the totals up to 88 and then did math to calculate the total. I'm sure there's a much simpler approach, but... this worked.
