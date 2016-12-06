## Useful Feedback from Hacker news

- Distinct vs Unique difference. This is not actually crucial, but might be
better to stay consistent.

- Fingerprint size - It allows fingerprints that are too short, basically less
than 4 bits doesn't allow a reasonable fill capacity. The paper authors only
hinted at this, but check out the fill capacity graphs on page 6. This could be
why your inserts are slowing down around 80 percent level when in my 
experience it doesn't happen till around 93 percent. 

- Modulo bias - your filter capacity code doesn't seem to round the filter size
to a power of two. This is a simple fix, but without it your array indexes will
be skewed by modulo bias, possibly badly if someone picks a nasty number. 

- Alternate bucket positions - your code seems to do a full hash for 
calculating alternate bucket positions. I know the paper mentions this, but I 
haven't seen anyone actually doing it :). It's a lot faster to just XOR with a 
mixing constant. TBH that's what most libraries are doing ... whether it is a 
good idea is debatable :)

- No victim cache - Didn't look too much into it, but I didn't see a victim
slot used in your code. This will cause problems when the first insert fails. 
The problem is, by the time the first insert actually fails, you've 
relocated a bunch of different fingerprints like 500 times. It becomes unclear
which fingerprint you originally tried to insert, and you're left holding a 
dangling item from a random place in the filter that you cannot insert. This 
violates the 'no false negatives' mantra. Even thought the filter is full it 
shouldn't break by deleting a random item when the first insert fails. 
You either need to store this last item or figure out a way to unwind your
insert attempts to be able to reject the item that originally failed to insert. 

Check out my Java library if you want to see how I dealt with these things. 
Also I have a bunch of unit tests there that I either came up with or 
borrowed form other Cuckoo libs. Should be prettry easy to convert some of those
to python :). 

https://github.com/MGunlogson/CuckooFilter4J
