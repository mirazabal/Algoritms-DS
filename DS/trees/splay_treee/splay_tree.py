'''
Splay tree implementation from Tarjan, R.E. Sequential access in splay trees takes linear time. Combinatorica 5, 367-378 (1985)
'''

import random
import sys
import pdb

class Node():
    def __init__(self, val):
        self.p = None # parent pointer
        self.l = None # left pointer
        self.r = None # right pointer
        self.val = val

class Splay_tree():
    def __init__(self):
        self.root = None

    def insert(self, val):
        print 'insert node = ' + str(val)
        node = Node(val)
        if self.root == None:
            self.root = node
            return

        n = self.root
        while(True):
            if node.val < n.val:
                if n.l == None:
                    n.l = node
                    node.p = n
                    break
                n = n.l
            elif node.val > n.val:
                if n.r == None:
                    n.r = node
                    node.p = n
                    break
                n = n.r
            else:
                print 'inserting duplicate value..'
                assert(False == True)
        self.splay(node)
        assert(node.r != node and node.l != node)

    def delete(self, val):
        if self.find(val) == True:
            if self.root != None and self.root.l != None and self.root.r != None:
                assert(self.root.val < self.root.r.val and self.root.val > self.root.l.val)
            if self.root.l != None:
                n = self.root.l
                while n.r != None:
                    assert(n.r.p == n)
                    if n.r != None:
                        assert( n.r.val > n.val)
                    n = n.r

                if n.p == self.root:
                    n.r = self.root.r
                    if n.r != None:
                        n.r.p = n
                    n.p = None
                    self.root.r = None
                    self.root.l = None
                    self.root = n
                else:
                    if n.l != None:
                        n.l.p = n.p
                    n.p.r = n.l
                    n.p = None
                    if self.root.l != None: 
                        self.root.l.p = n
                    if self.root.r != None:
                        self.root.r.p = n
                    
                    n.l = self.root.l
                    n.r = self.root.r

                    if n.l != None:
                        assert(n.l.val < n.val)
                    if self.root.r != n.r:
                        n.r = self.root.r
                        assert(n.r.val > n.val)

                    self.root = n
            elif self.root.r != None:
                n = self.root.r
                while n.l != None:
                    n = n.l

                if n.p == self.root:
                    n.l = self.root.l
                    if n.l != None:
                        n.l.p = n
                    n.p = None
                    self.root.r = None
                    self.root.l = None
                    self.root = n
                else:
                    if n.r != None:
                        n.r.p = n.p
                    n.p.l = n.r
                    n.p = None
                    if self.root.l != None: 
                        self.root.l.p = n
                    if self.root.r != None:
                        self.root.r.p = n
                    n.l = self.root.l
                    n.r = self.root.r
                    self.root = n
            else:
                self.root = None
            
            assert(self.root.l != self.root)
            assert(self.root.r != self.root)
            if self.root.l != None:
                assert(self.root.l.val < self.root.val)
            if self.root.r != None:
                assert(self.root.r.val > self.root.val)

    def find(self, val):
        if self.root == None:
            return False
        
        node = self.root
        while (node != None and node.val != val):
           if val < node.val:
               if node == node.l:
                   pdb.set_trace()
               assert(node != node.l)
               node = node.l
           else:
               assert(node != node.r)
               node = node.r
        if node != None:
            self.splay(node)

        return node != None


    def right_rotate(self, node):
        assert(node != None and node.p != None)
        parent = node.p

        parent.l = node.r
        if node.r != None:
            node.r.p = parent
        node.r = parent
        node.p = parent.p
        if parent.p != None and parent.p.l == parent:
            parent.p.l = node
        elif parent.p != None and parent.p.r == parent:
            parent.p.r = node
        parent.p = node

        assert(node.r != node and node.l != node)

    def left_rotate(self, node):
        assert(node != None and node.p != None)
        parent = node.p

        parent.r = node.l
        if node.l != None:
            node.l.p = parent
        node.l = parent
        node.p = parent.p
        if parent.p != None and parent.p.r == parent:
            parent.p.r = node
        elif parent.p != None and parent.p.l == parent:
            parent.p.l = node
        parent.p = node

        assert(node.r != node and node.l != node)

    def zig(self, node):
        assert(node != None)
        assert(node.p != None)
        parent = node.p
        if parent.l == node :
            self.right_rotate(node)
        elif parent.r == node:
            self.left_rotate(node)
        else:
            assert('Data structure malformed...')

    def zig_zig_left(self, node):
        assert(node != None and node.p != None and node.p.p != None)
        self.right_rotate(node)
        self.right_rotate(node)
        
    def zig_zig_right(self, node):
        assert(node != None and node.p != None and node.p.p != None)
        self.left_rotate(node)
        self.left_rotate(node)

    def zig_zag_right(self, node):
        assert(node != None and node.p != None and node.p.p != None)
        self.left_rotate(node)
        self.right_rotate(node)

    def zig_zag_left(self, node):
        assert(node != None and node.p != None and node.p.p != None)
        self.right_rotate(node)
        self.left_rotate(node)

    def splay(self, node):
        if node == None or node.p == None:
            return

        while node != None and node.p != None:
            grand_parent = node.p.p
            parent = node.p
            if grand_parent == None:
                self.zig(node)
            elif grand_parent.l == parent and parent.l == node:
                self.zig_zig_left(node)
            elif grand_parent.r == parent and parent.r == node:
                self.zig_zig_right(node)
            elif grand_parent.l == parent and parent.r == node:
                self.zig_zag_right(node)
            elif grand_parent.r == parent and parent.l == node:
                self.zig_zag_left(node)
            else:
                assert('Data structure malformed...')

        self.root = node

    def in_order_traversal(self, n):
        if n.l != None:
            self.in_order_traversal(n.l)
        print 'Val =  ' + str(n.val)
        if n.r != None:
            self.in_order_traversal(n.r)
    

if __name__ == "__main__":
    splay_tree = Splay_tree()

#    x = [44,22,3,61,34,89,79,65,5,28]
    x =  list(set(random.sample(range(1, 100000), 10000)))
    for v in x:
        splay_tree.insert(v);
    splay_tree.in_order_traversal(splay_tree.root)
    
    delete_x = x[0::2]
    for v in delete_x:
        print 'delete node = ' + str(v) 
        splay_tree.delete(v)

    splay_tree.in_order_traversal(splay_tree.root)

