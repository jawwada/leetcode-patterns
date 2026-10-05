# Accounts Merge
*LeetCode 721 · Medium · Pattern: Union-Find (disjoint set union) · Reading time ~10 min*

## The problem

accounts[i] = [name, email1, email2, ...]. Two accounts belong to the same person if they share at least one email;
names can repeat across different people. Merge the accounts and return each person's [name, sorted emails...] in any
order.

```text
Example:
  [["John","a@m","b@m"],["John","b@m","c@m"],["Mary","d@m"]] ->
  [["John","a@m","b@m","c@m"],["Mary","d@m"]].
```

## What the problem is really asking

Each account is a list `[name, email1, email2, ...]`. Two accounts belong to the same person
if they share **at least one email**. That relation is transitive. If account A shares an
email with B, and B shares a different email with C, then A, B and C are one person, even
though A and C have nothing in common. Names prove nothing, because two different people
can both be called John. For each person, output their name followed by every email they
own, sorted.

The answer is a list of groups, so this is connected components again. But nobody hands you
the edges. The nodes are accounts, and an edge exists wherever two accounts list the same
email. The hard part is finding those edges without comparing every pair of accounts.

```text
  #  account
  0  Ann  a@x                   0 ---a@x--- 3 ---c@x--- 2
  1  Bob  b@x
  2  Ann  c@x                   1   (alone)
  3  Ann  a@x c@x
                               output:
  accounts 0 and 2 share       [Ann, a@x, c@x]
  nothing directly; 3 bridges  [Bob, b@x]
```

Without account 3, there would be two separate Anns, and the output would list two `Ann`
rows. Merging by name would be wrong.

## Do it by hand first

Read the accounts top to bottom with a notepad. For every email, write down which account
you first saw it in. When an email shows up again, you have caught two accounts that are
the same person, so draw a line between them.

```text
  read      email   seen before?   notepad (email -> acct)
  acct 0    a@x     no             a@x->0
  acct 1    b@x     no             a@x->0 b@x->1
  acct 2    c@x     no             ... c@x->2
  acct 3    a@x     yes, acct 0    join 3 with 0
  acct 3    c@x     yes, acct 2    join 3 with 2
                                   => {0,2,3} and {1}
```

Your hand kept two things. One is a **first-owner table** from email to account. It turns
"does anyone else have this email?" into a lookup instead of a search. The other is the
groups being joined, and those only ever grow. That second thing is union-find, keyed by
account index.

## The first honest attempt

Treat each account as a node. For every pair of accounts `(i, j)`, intersect their email
sets, and add an edge if the intersection is non-empty. Then run a DFS to find the
components and collect emails.

```text
  pairs checked          share?
  (0,1)  {a}   & {b}     no
  (0,2)  {a}   & {c}     no
  (0,3)  {a}   & {a,c}   yes
  (1,2)  {b}   & {c}     no
  (1,3)  {b}   & {a,c}   no
  (2,3)  {c}   & {a,c}   yes
  6 pair tests for 2 real links; A accounts -> A^2/2 tests
```

With `A` accounts of up to `k` emails, that is `O(A^2 * k)`, plus `O(A^2)` space for edges.
Most pairs share nothing, yet every pair is tested. The repeated work is asking every
account about every email, when each email only needs to be asked about once.

## The turning point

**Claim: two accounts are directly linked exactly when some email appears in both, and one
hash map from email to first owner finds every such link in a single pass.**

When account `i` lists email `e` and the map already says `owner[e] = j`, then `i` and `j`
share `e`, which is a link. Every link is found this way, because if `i` and `j` share `e`,
whichever of them lists `e` second hits the map entry left by the other. Some links are not
found as direct pairs. If three accounts share `e`, we link the second and the third to the
first, but never the second to the third. That is fine: we only need the components, and a
star joins the same set as a complete graph.

Now each discovered link is a union, and "same person" is exactly "same root." We never
store edges. The union-find from Number of Connected Components works unchanged, except for
two details. The keys are account indices `0..A-1`. And this solution links roots directly,
with `parent[find(i)] = find(owner[e])` and no rank. That is acceptable here because path
halving alone keeps finds `O(log A)` amortised.

After all the unions, the output is a grouping step. Walk the notepad. Each email goes into
the bucket of `find(owner[e])`. Each bucket is one person. Their name is the name on the
root account, which is safe because every account in one component belongs to the same
person and so carries the same name. Sort each bucket.

```text
  email -> owner -> find(owner) -> bucket
  a@x   ->   0   ->     2       -> bucket 2: a@x
  b@x   ->   1   ->     1       -> bucket 1: b@x
  c@x   ->   2   ->     2       -> bucket 2: a@x c@x
```

## Watch it work

`accounts = [["Ann","a@x"],["Bob","b@x"],["Ann","c@x"],["Ann","a@x","c@x"]]`,
`parent = [0,1,2,3]`.

```text
Frame 1  accts 0,1,2: every email is new
  owner:  a@x->0  b@x->1  c@x->2
  index:  0 1 2 3         0   1   2   3
  parent: 0 1 2 3
```
There are no repeats yet, so every account is its own root. Four people, so far.

```text
Frame 2  acct 3, email a@x: owner is 0
  find(3)=3, find(0)=0  -> parent[3] = 0
  index:  0 1 2 3         0   1   2
  parent: 0 1 2 0         |
                          3
```
Account 3 is the same person as account 0. Account 3's root now hangs under account 0's
root.

```text
Frame 3  acct 3, email c@x: owner is 2
  find(3)=0, find(2)=2  -> parent[0] = 2
  index:  0 1 2 3         2     1
  parent: 2 1 2 0         |
                          0
                          |
                          3
```
We union the *roots*. Root 0 goes under root 2, and that drags account 3 along. Accounts 0
and 2 are now one person without ever sharing an email.

```text
Frame 4  group emails by find(owner[e])
  a@x: find(0) -> 0 points to 2 -> root 2
  b@x: find(1) -> root 1
  c@x: find(2) -> root 2
  buckets  {2: [a@x, c@x], 1: [b@x]}
  output   [["Ann","a@x","c@x"], ["Bob","b@x"]]
```
Each bucket takes the name of its root account (`accounts[2][0]` is Ann) and is sorted.

What stayed invariant: two accounts had the same root exactly when a chain of shared emails,
among the emails read so far, connected them. `owner` held one account per email, and that
was enough, because every later holder of the email got unioned with that account.

## Why it is correct

Look at the graph whose nodes are accounts and whose edges join accounts that share an
email. The correct groups are its connected components. Every union we perform joins two
accounts that share an email, so we never merge two different people. For completeness:
suppose accounts `i` and `j` share `e`, and `j` is read first. Then `owner[e]` is either
`j` itself or an earlier account that `j` was unioned with when `j` read `e`. When `i`
reads `e`, it is unioned with `owner[e]`. Either way `i` and `j` end up in one set. So every
edge's endpoints end up in the same set, and union-find sets are closed under chains of edges. The sets
therefore equal the components. Every email is in `owner`, so the grouping step places
each email in exactly the bucket of its component.

## Cost

- Time `O(N * alpha(A) + N log N)`, where `N` is the total number of emails. There is one
  hash lookup and at most one union per email, and sorting the buckets is the dominant
  cost.
- Space `O(N + A)`, for the `owner` map, the buckets and `parent`.
- The pairwise brute force is `O(A^2 * k)` time and `O(A^2)` space.

## Variations you will meet

- **Union-find keyed by email instead of account.** Union the first email of each account
  with every other email in that account. Then group emails by root. This is equivalent,
  but the keys are strings, so `parent` is a dict.
- **DFS on an email graph.** Build edges `first_email <-> each email` per account, then
  flood each component. This is the same complexity. It is useful when you also need to
  traverse.
- **Similar-string groups or synonymous sentences.** Whenever "A ~ B" is given as pairs and
  the relation is transitive, the answer is union-find over the items plus a grouping
  pass. Similar String Groups (839) and Synonymous Sentences (1258) both follow this
  template.

## What to carry forward

When the links are hidden inside the data, a first-owner hash map finds them in one pass.
Every repeat is a union, and the answer comes from grouping by root. The next problem,
Number of Islands II, keeps union-find but brings the nodes in one at a time. The answer is
needed after *every* insertion, so the running count becomes the output.
