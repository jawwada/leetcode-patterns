"""
Inverted Index - Postings Lists and Sorted Intersection

Map each word to the sorted ids of the documents that contain it, so a query
walks a few short lists instead of reading every document. Six documents ->
search_and(["quick", "dog"]) = [3, 4, 6] and
search_or(["fox", "lazy"]) = [1, 2, 4].
"""


# --- algorithm ---
def intersect(a, b):
    """Ids in both sorted lists, by two pointers. O(len(a) + len(b))."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])             # in both: keep it
            i += 1
            j += 1
        elif a[i] < b[j]:
            i += 1                          # a[i] is not in b
        else:
            j += 1                          # b[j] is not in a
    return result


def union(a, b):
    """Ids in either sorted list, each once. O(len(a) + len(b))."""
    result = []
    i = 0
    j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            result.append(a[i])             # in both: keep one copy
            i += 1
            j += 1
        elif a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    result.extend(a[i:])                    # one list ran out: copy the rest
    result.extend(b[j:])
    return result


class InvertedIndex:
    """term -> increasing list of the ids of the documents that contain it."""

    def __init__(self):
        self.postings = {}                  # term -> sorted doc ids

    def add_document(self, doc_id, text):
        """Append doc_id once to the list of every word in text; ids must grow
        from call to call. O(words in text)."""
        lowered = text.lower()
        for word in lowered.split():
            if word not in self.postings:
                self.postings[word] = []
            ids = self.postings[word]
            if len(ids) == 0 or ids[-1] != doc_id:  # once per document
                ids.append(doc_id)

    def search_and(self, terms):
        """Ids of the documents holding every term: intersect the lists,
        shortest first. O(total length of the lists)."""
        lists = []
        for term in terms:
            word = term.lower()
            if word not in self.postings:
                return []                   # a missing term matches nothing
            lists.append(self.postings[word])
        if len(lists) == 0:
            return []
        lists.sort(key=len)                 # shortest list first
        result = list(lists[0])             # a copy: the index stays intact
        for k in range(1, len(lists)):
            result = intersect(result, lists[k])
        return result

    def search_or(self, terms):
        """Ids of the documents holding any term: merge the lists pairwise.
        O(terms * total length)."""
        result = []
        for term in terms:
            word = term.lower()
            if word in self.postings:
                result = union(result, self.postings[word])
        return result


# --- try it ---
index = InvertedIndex()
index.add_document(1, "the quick brown fox")
index.add_document(2, "the lazy dog")
index.add_document(3, "a quick brown dog")
index.add_document(4, "the dog chased the quick fox")
index.add_document(5, "my dog sleeps")
index.add_document(6, "quick thinking saved the dog")
print(index.postings["the"])                         # -> [1, 2, 4, 6]
print(index.postings["dog"])                         # -> [2, 3, 4, 5, 6]
print(index.search_and(["quick", "dog"]))            # -> [3, 4, 6]
print(index.search_and(["The", "QUICK", "dog"]))     # -> [4, 6]
print(index.search_or(["fox", "lazy"]))              # -> [1, 2, 4]
print(index.search_and(["quick", "cat"]), index.search_or(["cat"]))  # -> [] []
