'''
    RB tree implemented a la CLRS. Augmented with operation join(concatenate)/split according to Akshal Aniche, McGuill
    University, 2018

    Red-Black trees have 5 properties:
    1- Every node is Red or Black
    2- The root is black
    3- Every leaf is black
    4- If a node is red, then both its children are black
    5- For each node, all simple paths from the node to descendant leaves contain the same number of black nodes 

    Lemma 1: a red-black tree with n internal nodes has a height at most 2lg(n+1)
'''

'''
rank(root(T2)) <= rank(root(T1))
JOIN(T1, T2):
1 Find MIN(T2) (leftmost node); denote the node j.
2 Remove j from T2.
3 FIX(T2nj), and denote the resulting tree B, in O(log n) time.
4 Let r be the rank of the root of B
5
6 Find in the right roof of T1 a black node of rank r. O(log n)
7 // The right roof of a tree is the rightmost path from the root.
8 Denote it a. Let b = p[a], A the subtree rooted at a.
9 // see figure 10
10
11 color[j] = red
12 rank[j] = r + 1
13 left[j] = a
14 right[j] = root[B]
15 parent[j] = b
16 Update the relevant pointers in the other nodes.
17 // Updating all these pointers takes time O(1).
18 // see figure 11
19
20 FIX(j) as in an ordinary red-black tree INSERT. (O(log n))
21 // see definition 14


SPLIT(T, k):
1 SEARCH(k) to find the node with key k.
2 Keep track of the nodes with key smaller than or equal to k,
3 say p1, ..., pi, in decreasing order of key, and their respective
4 left subtree A1, A2, ..., Ai.
5 Let A be the subtree A1 together with p1.
6 // Note that p1 has key k.
7
8 Repeatedly join the subtrees from right to left as such:
9 S2 = JOIN(A, p2, A2)
10 S3 = JOIN(S2, p3, A3)
11 ...
13 Si = JOIN(Si, pi, Ai)
14
15 T1 = Si
16 return T1
'''



import random
import sys
import pdb

class DummyNode():
    def __init__(self):
        self.key = None
        self.parent = None
        self.left = None
        self.right = None
        self.color = 'Black'

rb_tree_dummy = DummyNode()

class Node():
    def __init__(self,key):
        self.key = key
        self.parent = rb_tree_dummy
        self.left =  rb_tree_dummy 
        self.right =  rb_tree_dummy
        self.color = 'Red'

class Rb_tree():
    def __init__(self):
        self.dummy = rb_tree_dummy # all the RB trees have the same dummy node
        self.root = self.dummy 
        self.last_value = 0
        self.bh = 0 # black height in the RB tree

    def create_node(self, val):
        x_node = Node(val)
        x_node.parent = self.dummy
        x_node.left = self.dummy
        x_node.right = self.dummy
        return x_node

    def in_order_traversal(self, node):
        if node != self.dummy:
            self.in_order_traversal(node.left)
            sys.stdout.write(str(node.key) + " color =  " + node.color + " \n" )
            if node.key <= self.last_value:
                print 'node.key == ' + str(node.key) + ' self.last_value = ' + str(self.last_value)
                assert node.key > self.last_value  
            self.last_value = node.key 
            self.in_order_traversal(node.right)


    def pre_order_traversal(self,node):
        if node != self.dummy:
            sys.stdout.write(str(node.key) + " color =  " + node.color + " \n" )
            self.pre_order_traversal(node.left)
            self.pre_order_traversal(node.right)

    def post_order_traversal(node):
        if node != self.dummy:
            self.post_order_traversal(node.left)
            self.post_order_traversal(node.right)
            sys.stdout.write(str(node.key) + " color =  " + node.color + " \n" )


    def left_rotate(self, x_node):
        assert x_node.right != self.dummy

        y_node = x_node.right

        x_node.right = y_node.left
        if y_node.left != self.dummy:
            y_node.left.parent = x_node

        y_node.parent = x_node.parent
        if x_node.parent == self.dummy:
            self.root = y_node
        elif x_node == x_node.parent.left:
            x_node.parent.left = y_node
        else: 
            x_node.parent.right = y_node

        y_node.left = x_node
        x_node.parent = y_node

    def right_rotate(self, x_node):
        assert x_node.left != self.dummy

        y_node = x_node.left 
        x_node.left = y_node.right
        if y_node.right != self.dummy:
            y_node.right.parent = x_node
        
        y_node.parent = x_node.parent
        if x_node.parent == self.dummy:
            self.root = y_node
        elif x_node.parent.left == x_node:
           x_node.parent.left = y_node
        else:
            x_node.parent.right = y_node

        y_node.right = x_node
        x_node.parent = y_node

    def insert_node(self, z_node):
#        z_node = self.create_node(val)
        assert z_node != self.dummy
        assert z_node.left == self.dummy
        assert z_node.right == self.dummy
        assert z_node.color == 'Red'

        x_node = self.root
        y_node = self.dummy
        # Find leaf to insert 
        while x_node != self.dummy:
            y_node = x_node
            if z_node.key < x_node.key:
                if x_node.left != self.dummy: 
                    assert (x_node.left.key < x_node.key)
                x_node = x_node.left
            else:
                if x_node.right != self.dummy:
                    assert(x_node.key < x_node.right.key)
                x_node = x_node.right

        z_node.parent = y_node
        if y_node == self.dummy:
            self.root = z_node
        elif z_node.key < y_node.key: 
            y_node.left = z_node
        else:
            y_node.right = z_node


        self.insert_fixup(z_node)

    def insert_fixup(self,z_node):

        while z_node.parent.color == 'Red':
            # z_node.parent.color == 'Red' which means 
            #1- violating only property 4 of the red-black tree
            #2- z_node_parent was not the root by property 2, root must be black
            #3- z_node.parent.parent must exist and is Black, since Red-Red is illegal
            parent = z_node.parent 
            grand_parent = z_node.parent.parent 
            if parent == grand_parent.left:
                uncle_node = grand_parent.right
                # Case 1: uncle is Red, flip colors and continue up the tree
                if uncle_node.color == 'Red':
                    parent.color = 'Black'
                    uncle_node.color = 'Black'
                    grand_parent.color = 'Red'
                    z_node = grand_parent

                else: # uncle is Black
                    #Case 2: z_node at right
                    if z_node == parent.right:
                        z_node = parent
                        self.left_rotate(z_node)
                        parent = z_node.parent # the grand_parent is the same, so do not refresh 

                    #Case 3: z_node at left
                    parent.color = 'Black' 
                    grand_parent.color = 'Red'
                    self.right_rotate(grand_parent)
            else:
                uncle_node = z_node.parent.parent.left
                if uncle_node.color == 'Red':
                    z_node.parent.color = 'Black'
                    uncle_node.color = 'Black'
                    z_node.parent.parent.color = 'Red'
                    z_node = z_node.parent.parent

                else: # uncle node color = Black
                    if z_node == z_node.parent.left:
                        z_node = z_node.parent
                        self.right_rotate(z_node)

                    z_node.parent.color = 'Black' 
                    z_node.parent.parent.color = 'Red'
                    self.left_rotate(z_node.parent.parent)
       
            #Assure that not violating property 2 of the red-black tree
        if self.root.color == 'Red':
            self.bh += 1 # if the root is red after inserting, the black height of the tree has increased.
            self.root.color = 'Black'

    def __print_helper(self, node, indent, last):
        if node != self.dummy:
            sys.stdout.write(indent)
            if last:
                sys.stdout.write("R----")
                indent += "     "
            else:
                sys.stdout.write("L----")
                indent += "|    "

            print str(node.key) + "(" +  node.color + ")"
            self.__print_helper(node.left, indent, False)
            self.__print_helper(node.right, indent, True)

    def print_tree(self):
        self.__print_helper(self.root, "", True )

    def transplant(self, u_node, v_node):
        assert u_node != self.dummy

        if u_node.parent == self.dummy:
            self.root = v_node
        elif u_node == u_node.parent.left:
            u_node.parent.left = v_node
        else:
            u_node.parent.right = v_node

        v_node.parent = u_node.parent

    def minimum(self,x_node):
        while x_node.left != self.dummy:
            assert(x_node.left.key < x_node.key)
            x_node = x_node.left
        return x_node

    def find(self, node, value):
        while node != self.dummy and node.key != value:
            if value < node.key: 
                if node.left != self.dummy:
                    assert(node.left.key < node.key)
                node = node.left
            else: 
                if node.right != self.dummy:
                    assert(node.right.key > node.key)
                node = node.right
        return node 

    def delete(self, z_node):
        original_color = z_node.color
        #x_node = z_node
        #y_node = z_node

        if z_node.left == self.dummy:
            x_node = z_node.right
            self.transplant(z_node,z_node.right)
            # note that nobody points to z_node, even that z_node still point to parent and right
        elif z_node.right == self.dummy:
            x_node = z_node.left
            self.transplant(z_node,z_node.left)
        else:
            y_node = self.minimum(z_node.right)
            original_color = y_node.color
            x_node = y_node.right

            if y_node.parent == z_node:
                x_node.parent = y_node # necessary when x_node is the dummy node
            else:
                self.transplant(y_node, y_node.right)
                y_node.right = z_node.right
                y_node.right.parent = y_node
            self.transplant(z_node,y_node)
            y_node.left = z_node.left
            y_node.left.parent = y_node
            y_node.color = z_node.color

        if original_color == 'Black':
            self.delete_fixup(x_node)

    def delete_fixup(self, x_node):
        while x_node != self.root and x_node.color == 'Black':
            if x_node == x_node.parent.left:
                w_node = x_node.parent.right
                # Case 1: x's sibling is Red
                if w_node.color == 'Red': 
                    w_node.color = 'Black'
                    x_node.parent.color = 'Red'
                    self.left_rotate(x_node.parent)
                    w_node = x_node.parent.right

                assert w_node.color == 'Black'
                #Case 2: x's siblings nodes are both black and w itself is black
                if w_node.left.color =='Black' and w_node.right.color =='Black': 
                   w_node.color = 'Red'
                   # if we come from case 1, this will terminate, as x_node.parent == 'Red'
                   # else, spread the problem to upper levels in the tree (maybe left and right 
                   # branch decompensated after removing a black node in the left branch
                   x_node = x_node.parent
                else: 
                    #Case 3: x's sibling w is black w.left = red and w.right = black
                    if  w_node.right.color == 'Black':
                        assert w_node.color ==  'Black'
                        assert w_node.left.color ==  'Red'
                        w_node.left.color = 'Black'
                        w_node.color = 'Red'
                        self.right_rotate(w_node)
                        w_node = x_node.parent.right
                    #Case 4: x's sibling is black and w's right child is red
                    assert w_node.color == 'Black'
                    assert w_node.right.color == 'Red'
                    w_node.color = x_node.parent.color
                    x_node.parent.color = 'Black'
                    # since w_node.right.color == 'Red' we insert a new black in the w_node path, changing the color
                    w_node.right.color = 'Black'
                    # the rotation adds one black in the x_node path and deletes one in w_node path
                    # as a result, after the function, the x_node path gets one extra black and the w_node 
                    #path ends with the same number of blacks +1, -1
                    self.left_rotate(x_node.parent)
                    x_node = self.root

            else:
                w_node = x_node.parent.left
                # Case 1: x's sibling is Red
                if w_node.color == 'Red': 
                    w_node.color = 'Black'
                    x_node.parent.color = 'Red'
                    self.right_rotate(x_node.parent)
                    w_node = x_node.parent.left

                assert w_node.color == 'Black'
                if w_node == self.dummy:
                    pdb.set_trace()
                #Case 2: x's siblings nodes are both black and w itself is black
                if w_node.left.color=='Black' and w_node.right.color == 'Black': 
                   w_node.color = 'Red'
                   x_node = x_node.parent
                else: 
                    #Case 3: x's sibling w is black w.left = red and w.right = black
                    if w_node.left.color == 'Black':
                        assert w_node.color ==  'Black'
                        assert w_node.right.color ==  'Red'
                        w_node.right.color = 'Black'
                        w_node.color = 'Red'
                        self.left_rotate(w_node)
                        w_node = x_node.parent.left
                    #Case 4: x's sibling is black and w's left child is red
                    assert w_node.color == 'Black'
                    assert w_node.left.color == 'Red'
                    w_node.color = x_node.parent.color
                    x_node.parent.color = 'Black'
                    w_node.left.color = 'Black'
                    self.right_rotate(x_node.parent)
                    x_node = self.root

        x_node.color = 'Black'

    def find_min(self):
       node = self.root
       while node != self.dummy and node.left != self.dummy: 
           assert(node.left.key < node.key)
           node = node.left
       return node

    def find_max(self):
       node = self.root
       while node != self.dummy and node.right != self.dummy: 
           assert(node.right.key > node.key)
           node = node.right
       return node
    
    def find_rank(self):
        node = self.root
        if node == self.dummy:
            return 0
        node = node.right
        num_black = 0
        while node != self.dummy:
            if node.color == 'Black':
                num_black = num_black + 1
            node = node.right
        return num_black

    def find_node_rank_right(self, num_black):
        assert(num_black > -1)
        node = self.root
        while node != self.dummy and num_black != 0:
            node = node.right
            if node.color == 'Black':
                num_black = num_black - 1

        assert(node != self.dummy)
        return node

    def find_node_rank_left(self, num_black):
        assert(num_black > -1)
        node = self.root
        while node != self.dummy and num_black != 0:
            node = node.left
            if node.color == 'Black':
                num_black = num_black - 1

        assert(node != self.dummy)
        return node

    def split(self, key):
        less = []
        greater = []
        left_tree = Rb_tree() 
        right_tree = Rb_tree()

        node = self.root
        while node != self.dummy:
            if key < node.key:
                greater.append(node)
                node = node.left
            elif key > node.key:
                less.append(node)
                node = node.right
            else:
                assert key == node.key
                if node.left != self.dummy:
                    left_tree.root = node.left
                    left_tree.root.color = 'Black'
                    node.left.parent = self.dummy
                    node.left = self.dummy
                    tmp_tree = Rb_tree()
                    tmp_tree.insert_node(node)
                    left_tree = concatenate(left_tree,tmp_tree) # forall(keys(rb_tree_2) > keys(rb_tree)) 
                else:
                    left_tree.root = node
                    left_tree.root.color = 'Black'
                    
                if node.right != self.dummy:
                    right_tree.root = node.right
                    right_tree.color = 'Black'
                    node.right.parent = self.dummy
                    node.right = self.dummy 
                break 
        
        if node == self.dummy: #key not found, so impossible to split
            return (None,None,None) 

        less.reverse()
        for n in less:
            n.right.parent = rb_tree_dummy
            n.right = rb_tree_dummy
            if n.parent != rb_tree_dummy:
                if n.parent.left == n:
                    n.parent.left = rb_tree_dummy
                else:
                    n.parent.right = rb_tree_dummy
            n.parent = rb_tree_dummy
            tmp_tree = Rb_tree()
            tmp_tree.root = n.left 
            tmp_tree.root.color = 'Black'
            if n.left != rb_tree_dummy:
                n.left.parent = rb_tree_dummy 
            n.left = rb_tree_dummy 
            left_tree = concatenate_3(tmp_tree, n, left_tree)  # forall(keys(rb_tree_2) > keys(rb_tree)) 

        greater.reverse()
        for n in greater:
            n.left.parent = rb_tree_dummy 
            n.left = rb_tree_dummy
            if n.parent != rb_tree_dummy:
                if n.parent.left == n:
                    n.parent.left = rb_tree_dummy
                else:
                    n.parent.right = rb_tree_dummy

            n.parent = rb_tree_dummy 
            tmp_tree = Rb_tree()
            tmp_tree.root = n.right 
            tmp_tree.root.color = 'Black'
            if n.right != rb_tree_dummy:
                n.right.parent = rb_tree_dummy
            n.right = rb_tree_dummy 
            right_tree = concatenate_3(right_tree, n, tmp_tree)  # forall(keys(rb_tree_2) > keys(rb_tree)) 
             
        # By property 2 of the RB trees
        assert left_tree.root.color == 'Black'
        assert right_tree.root.color == 'Black'

        return (node,left_tree,right_tree) 

def concatenate_3(rb_tree_1, node, rb_tree_2):
    assert node != None and node != rb_tree_dummy 
    assert node.left == rb_tree_dummy and node.right == rb_tree_dummy
    assert node.parent == rb_tree_dummy

    assert rb_tree_1 != None 
    if rb_tree_1.root == rb_tree_dummy:
        node.color = 'Red'
        rb_tree_2.insert_node(node)
        return rb_tree_2
        
    assert rb_tree_2 != None 
    if rb_tree_2.root == rb_tree_dummy:
        node.color = 'Red'
        rb_tree_1.insert_node(node)
        return rb_tree_1

    
    assert node.key > rb_tree_1.find_max().key    
    assert node.key < rb_tree_2.find_min().key    

    num_black_1 = rb_tree_1.find_rank() 
    num_black_2 = rb_tree_2.find_rank() 
    tree_1_higher = num_black_1 >= num_black_2 # tree 1 is higher and has smaller keys

    rb_tree = None
    alfa_node = rb_tree_dummy
    if tree_1_higher:
        alfa_node = rb_tree_1.find_node_rank_right(num_black_1-num_black_2)  
        node.left = alfa_node
        node.right = rb_tree_2.root
        rb_tree = rb_tree_1 
    else:
        alfa_node = rb_tree_2.find_node_rank_left(num_black_2-num_black_1)  
        node.left = rb_tree_1.root
        node.right = alfa_node
        rb_tree = rb_tree_2 
 
    beta_node = alfa_node.parent
    node.color = 'Red'
    node.parent = beta_node
    
    if tree_1_higher:
        rb_tree_2.root.parent = node
        if beta_node != rb_tree_dummy:
            beta_node.right = node
    else:
        rb_tree_1.root.parent = node
        if beta_node != rb_tree_dummy:
            beta_node.left = node

    alfa_node.parent = node
    if beta_node != rb_tree_dummy:
        rb_tree.insert_fixup(node)
    else:
        rb_tree.root = node
        rb_tree.root.color = 'Black'
    return rb_tree

def concatenate(rb_tree_1, rb_tree_2):
    # Assert that all the keys from rb_tree_2 are bigger than rb_tree_1 keys
    assert rb_tree_1.root != rb_tree_1.dummy or rb_tree_2.root != rb_tree_2.dummy

    if rb_tree_1.root == rb_tree_1.dummy: 
        return rb_tree_2
    elif rb_tree_2.root == rb_tree_2.dummy:
        return rb_tree_1

    num_black_1 = rb_tree_1.find_rank() 
    num_black_2 = rb_tree_2.find_rank() 
    node = rb_tree_dummy
    if num_black_1 > num_black_2: # tree 1 is higher and has smaller keys
        node = rb_tree_2.find_min() 
        assert node != rb_tree_2.dummy
        rb_tree_2.delete(node)
        node.left = rb_tree_dummy
        node.right = rb_tree_dummy
        node.parent = rb_tree_dummy

    else: # tree 2 is higher and has larger keys
        node = rb_tree_1.find_max()
        assert node != rb_tree_1.dummy
        rb_tree_1.delete(node)
        node.left = rb_tree_dummy
        node.right = rb_tree_dummy
        node.parent = rb_tree_dummy

    return concatenate_3(rb_tree_1, node, rb_tree_2) 

if __name__ == "__main__":
    rb_tree = Rb_tree()
    x = [44,22,3,61,34,89,79,65,5,28, 85, 90]
    #x = random.sample(range(1, 100000), 10000)
    for v in x:
        rb_tree.insert_node(Node(v))

    rb_tree_2 = Rb_tree()
    y = [200, 300, 500]
    for v in y:
        rb_tree_2.insert_node(Node(v))

    concat_tree = concatenate(rb_tree,rb_tree_2)
    (node,left_tree,right_tree) = concat_tree.split(90)

    left_tree.print_tree()
    right_tree.print_tree()

