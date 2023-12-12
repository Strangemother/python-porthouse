# Graph Path Reduction

For may hops on many messages we can route through closer hops.
This is done by reading the hope of three messages, and reducing the hops of the last to match the shortest path of the previous.

Given

    m-> (v) -> a,b,c,d,e,f,g,v
    m-> (v) -> f,t,v
    m-> (v) -> a,e,t,g,v
    m-> (t) -> a,t

Wanted

    m-> (v) -> a,t,v


