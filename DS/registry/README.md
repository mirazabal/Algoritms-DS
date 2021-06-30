Data structure based on Sean parent's presentation Better Code: Relationships
https://sean-parent.stlab.cc/papers-and-presentations/#better-code-relationships
It associates an ID with some data that is stored and can be latter accessed. 
It replaces the std::map data structure. 
It is implemented as an ordered array (key_id is a monotonically increasing 
value) so that searches are always O(logN) and memory is always contiguous,
contrary to the std::map that is a node based data structure
It shrinks, compacts and expands as neccessary



