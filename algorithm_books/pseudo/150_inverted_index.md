---
rank: 150
slug: inverted_index
---

An inverted index answers keyword search. `add_document(doc_id, text)` indexes a document, `search_and(terms)` returns the ids of the documents that contain every term, and `search_or(terms)` those that contain any of them. It is the index at the back of a book turned into a data structure, from each word to the places it appears. Over six short documents, `search_and(["quick", "dog"])` returns `[3, 4, 6]` and `search_or(["fox", "lazy"])` returns `[1, 2, 4]`.

Scanning every document for every query rereads the whole collection each time. The index does the reading once, when a document arrives: it maps each term to its postings list, the ids of the documents that contain it, and a query then touches only the lists of its own terms. `add_document` lowercases the text, splits it on spaces and appends `doc_id` to each word's list. Ids arrive in increasing order and a list only ever grows at its end, so every postings list is sorted without a single sort. A word repeated in one document finds the document's id already at the end of its list, so checking the last id keeps each document once.

Sorted lists turn AND into a two-pointer walk, the merge of merge sort (#17) with a different rule for what to keep. Put a finger on the front of each list. Equal ids mean the document holds both terms, so keep it and move both fingers; otherwise the smaller id cannot be in the other list, whose remaining ids are all larger, so its finger moves past it. OR is the same walk keeping every id once. With several terms, AND starts from the shortest list: the running result can only shrink, so it is never longer than that first list.

```text
doc  text                            postings, ids in the order added
1    the quick brown fox             the    [1, 2, 4, 6]     doc 4 only once
2    the lazy dog                    quick  [1, 3, 4, 6]
3    a quick brown dog               dog    [2, 3, 4, 5, 6]
4    the dog chased the quick fox    fox    [1, 4]
5    my dog sleeps                   lazy   [2]
6    quick thinking saved the dog    brown  [1, 3]

search_and(quick, dog): quick is the shorter list, so it leads
  i  j   quick[i]  dog[j]   step
  0  0      1        2      1 < 2: 1 is not in dog, i moves
  1  0      3        2      3 > 2: 2 is not in quick, j moves
  1  1      3        3      equal: keep 3, both move
  2  2      4        4      equal: keep 4, both move
  3  3      6        5      6 > 5: j moves
  3  4      6        6      equal: keep 6
  → [3, 4, 6]
search_or(fox, lazy): the same walk keeps every id once → [1, 2, 4]
```

```pseudo
FUNCTION Intersect(a, b)
    result ← empty list
    i ← 0
    j ← 0
    WHILE i < len(a) AND j < len(b)
        IF a[i] = b[j]
            result.append(a[i])             // in both: keep it
            i ← i + 1
            j ← j + 1
        ELSE IF a[i] < b[j]
            i ← i + 1                       // a[i] is not in b
        ELSE
            j ← j + 1                       // b[j] is not in a
    RETURN result

FUNCTION Union(a, b)
    result ← empty list
    i ← 0
    j ← 0
    WHILE i < len(a) AND j < len(b)
        IF a[i] = b[j]
            result.append(a[i])             // in both: keep one copy
            i ← i + 1
            j ← j + 1
        ELSE IF a[i] < b[j]
            result.append(a[i])
            i ← i + 1
        ELSE
            result.append(b[j])
            j ← j + 1
    result.extend(a[i..len(a) - 1])         // one list ran out: copy the rest
    result.extend(b[j..len(b) - 1])
    RETURN result

CLASS InvertedIndex
    FUNCTION Init()
        self.postings ← empty map           // term → sorted doc ids

    FUNCTION AddDocument(doc_id, text)
        lowered ← lowercase(text)
        FOR EACH word IN split(lowered)
            IF word NOT IN self.postings
                self.postings[word] ← empty list
            ids ← self.postings[word]
            IF len(ids) = 0 OR ids[len(ids) - 1] ≠ doc_id  // once per document
                ids.append(doc_id)

    FUNCTION SearchAnd(terms)
        lists ← empty list
        FOR EACH term IN terms
            word ← lowercase(term)
            IF word NOT IN self.postings
                RETURN empty list           // a missing term matches nothing
            lists.append(self.postings[word])
        IF len(lists) = 0
            RETURN empty list
        lists.sort(by length)               // shortest list first
        result ← copy of lists[0]           // the index stays intact
        FOR k FROM 1 TO len(lists) - 1
            result ← Intersect(result, lists[k])
        RETURN result

    FUNCTION SearchOr(terms)
        result ← empty list
        FOR EACH term IN terms
            word ← lowercase(term)
            IF word IN self.postings
                result ← Union(result, self.postings[word])
        RETURN result
```

Indexing costs `O(W)` for a document of W words. An AND query takes time linear in the total length of its lists, one step per id passed; OR folds t lists of N ids in all pairwise in `O(t · N)`, and the heap of list fronts from #20 merges them in `O(N log t)`. Real engines build on the same sorted lists. Each posting also records where the word sits in the document, so a phrase query such as `quick fox` checks that the positions are adjacent. Skip pointers, one every `√L` entries of a list of L ids, let a finger leap ahead when the other is far in front, so the short list drives the cost. The ids are stored as gaps between neighbors, small numbers that compress well, and matches are ranked by TF-IDF: how often the term appears in the document times the log of how rare it is in the collection. A large index is split by document across machines, each shard answering for its slice. The signals are keyword search and "which records have all of these tags". The classic mistake is appending the id once per occurrence: doc 4 says `the` twice, the list of `the` becomes `[1, 2, 4, 4, 6]`, and `search_or(["the"])` reports document 4 twice.

*Practice:* LC 349 Intersection of Two Arrays · LC 350 Intersection of Two Arrays II · LC 1268 Search Suggestions System
