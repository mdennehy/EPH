# EPH
Implementation of E Pluribus Hugo (and testing)

http://sasquan.org/business-meeting/agenda/#epluribus

```
3.8.1: Except as provided below, the final Award ballots shall list in each
category the five eligible nominees receiving the most nominations. If there
is a tie including fifth place, all the tied eligible nominees shall be
listed. determined by the process described in section 3.A.
```
Insert new section 3.A after Section 3.8 as follows:
```
Section 3.A: Finalist Selection Process

3.A.1: For each category, the finalist selection process shall be conducted as
elimination rounds consisting of three phases:

(1) Calculation Phase: First, the total number of nominations (the number of
ballots on which each nominee appears) from all eligible ballots shall be
tallied for each remaining nominee. Next, a single “point” shall be assigned
to each nomination ballot. That point shall be divided equally among all
remaining nominees on that ballot. Finally, all points from all nomination
ballots shall be totaled for each nominee in that category. These two numbers,
point total and number of nominations, shall be used in the Selection and
Elimination Phases.

(2) Selection Phase: The two nominees with the lowest point totals shall be
selected for comparison in the Elimination Phase. (See 3.A.3 for ties.)

(3) Elimination Phase: Nominees chosen in the Selection Phase shall be
compared, and the nominee with the fewest number of nominations shall be
eliminated and removed from all ballots for the Calculation Phase of all
subsequent rounds. (See 3.A.3 for ties.)

3.A.2: The phases described in 3.A.1 are repeated in order for each category
until the number of finalists specified in 3.8.1 remain. If elimination would
reduce the number of finalists to fewer than the number specified in section
3.8.1, then instead no nominees will be eliminated during that round, and all
remaining nominees shall appear on the final ballot, extending it if
necessary.

3.A.3: Ties shall be handled as described below:

(1) During the Selection Phase, if two or more nominees are tied for the
lowest point total, all such nominees shall be selected for the Elimination
Phase.

(2) During the Selection Phase, if one nominee has the lowest point total and
two or more nominees are tied for the second-lowest point total, then all such
nominees shall be selected for the Elimination Phase.

(3) During the Elimination Phase, if two or more nominees are tied for the
fewest number of nominations, the nominee with the lowest point total at that
round shall be eliminated.

(4) During the Elimination Phase, if two or more nominees are tied for both
fewest number of nominations and lowest point total, then all such nominees
tied at that round shall be eliminated.

3.A.4: After the initial Award ballot is generated, if any finalist(s) are
removed for any reason, the finalist selection process shall be rerun as
though the removed finalist(s) had never been nominee(s). None of the
remaining original finalists who have been notified shall be removed as a
result of this rerun. The new finalist(s) shall be merged with the original
finalists, extending the final ballot if necessary.
```

Tests to try:

http://www.antipope.org/charlie/blog-static/2015/08/bad-puppies-no-awards.html#comment-1978724
```> If I were being Evil...
That is in fact a valid question you're raising. The test is: can you sufficiently game the EPH system (assuming you have perfectly loyal minions) to control a statistically significant portion of the outcome that you should not be able to control, ie. if your group makes up 20% of the nominators, can you control 40% or more of the outcome?

1. I need to go do the math myself to make sure that 40% is the right threshold, I'm just using a POMA estimate there.

2. The great thing about all that documentation and test data? You can run the numbers yourself and get an answer. You don't even need to code, you can do it by hand on pencil and paper if you really want to. And it's an interesting question to boot...

3. I need more free time, this is sounding like a wonderfully juicy analysis problem...


Oh, and DeMarquis, same story - it's a valid question that's readily studied using existing public datasets and algorithms.

The great thing in both your cases is that you can actually get an answer. No
hand-waving needed. Just actually run the simulations or the tests with the
data and look at the outcomes.```

http://file770.com/?p=24533&cpage=19#comment-328182
```> Hey Mark,
> I don’t know if we’re in disagreement, but I didn’t understand what point you were making in your response. Simulations are *fantastic*. But a basic understanding of the EPH model gives us enough to know how some relatively simple datasets would pan out, and that’s valuable too.

Eh, you’re kindof blurring the lines a little – by looking at the underlying algorithm you can mathematically predict where the breaking points would be… but that’s functionally the same as running simulations (and if you wanted to test for sensitivity to starting conditions you usually wind up doing simulation for monte carlo analysis anyway).

> The point I’m trying to make is that one of the crucial factors in an attempt to capture the ballot with a slate is how diffuse, how scattered, the non-slate nominations are.

Yup, but when you say that, I want to know what the numerical value of “how diffuse” is “too diffuse”. Where do we say it breaks down? How do we define “breaks down”? If 20% of the voters can control 30% of the output if the other 80% are “too diffuse” is that statistically significant?
And does that even happen?
And happily, you can actually go and model those conditions, run EPH against them and come back with actual answers rather than yet more questions.
That’s a major strength in the system from my point of view.

> Take a trivial example: N slate-voters, M non-slate voters. But imagine each of the M nonslate voters nominates only one work, and it’s a work that nobody else nominates.
> In an extreme case like this, N can be 10, and M can be six billion. The slate will carry the whole ballot, even though their percentage of the voting body is tiny. You don’t need to run code for that; just understand the system.

Okay, but N=10, M=6e8 isn’t a useful example because there won’t be 6e8 unique eligible valid selections.
BUT, you’re pointing at what I was talking about; namely, what does the curve look like for EPH as you vary N and M? Where’s the breaking point? Is the breaking point out past the point where it’s a possible scenario (ie. N+M < MaxPossibleTotal and so on).

To me, that’s a lovely natty little bit of analysis to get into, and best of all, you get real hard answers out of it.

> But what I’m trying to demonstrate here is that the *number* of Puppy voters and of non-Puppy voters isn’t very important.

How unimportant is it? Or, to use the right terminology, how sensitive is the system to the N/M ratio? That’s a mathematically determinable value, right now. We can go and find it.

> What matters is *the size of clusters of agreement in non-slate voting.*

But is that right? Again, we can do an sensitivity analysis and get an actual numerical, hard answer. We don’t have to wave our hands about and guess. (And I love that about this approach).

> Can’t simulate new patterns until we’ve seen ’em, either.

Er, that’s just wrong. I mean, we’ve never seen half the things that this entire field of literature is talking about, but that doesn’t mean we can’t simulate them 😀
And simulation often finds completely new things humans have never thought of
before – the memristor for example.```

http://file770.com/?p=24505&cpage=11#comment-329097
```> 1: Oh, and BTW, EPH is still utterly gameable, even by outsiders. Short version:
> A: Put together a slate of your preferred nominees
> B: Have a web site where your supporters can go to get their Ballot
> C: Every time someone goes there, generate a new ballot, with one random pick from each category
> D: Since ballots are random, it doesn’t matter how often opponents of the Slate go to the site to “get” ballots, so can’t beat the system that way.
> Once EPH passes, I’ll run some simulations to see which “size” ballot is best. EPH privileges 1 vote ballots, so my starting assumption is that 1 vote’s best, but it will be no problem to run the sims.

Go for it! Math is always neat and you can always have someone else check your
results!```
