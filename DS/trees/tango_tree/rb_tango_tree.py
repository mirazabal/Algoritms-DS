'''
Tango tree implementation from:
Erik D. Demaine, Dion Harmon, John Iacono, and Mihai Patrascu. 2007. Dynamic Optimallity, Almost. SIAM J. Comput. 37, 1  

With a base Red-Black tree implemented ala CLRS enhanced with join/split operations from Akshal Aniche, McGuill 2018 

WARNING: This data structure is of very limited use since only search operations are allowed, no insertion or deletion.
         We first create a RB tree and call create_tango_tree from it.
'''

'''
    RB tree implemented a la CLRS. Augmented with operation join/split for using it at the tango tree

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

class TangoNode():
    def __init__(self,key,depth):
        self.key = key
        self.parent = rb_tree_dummy
        self.left =  rb_tree_dummy 
        self.right =  rb_tree_dummy
        self.color = 'Red'

        self.depth = depth
        self.max_depth = -sys.maxint-1
        self.min_depth = sys.maxint
        self.is_marked = False

class Rb_tree():
    def __init__(self):
        self.dummy = rb_tree_dummy # all the RB trees have the same dummy node
        self.root = self.dummy 
        self.last_value = 0
        self.bh = 0 # black height in the RB tree

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
        assert z_node != self.dummy
        assert z_node.left == self.dummy or z_node.left.is_marked == True
        assert z_node.right == self.dummy or z_node.right.is_marked == True
        assert z_node.color == 'Red'
        assert z_node.is_marked == False

        x_node = self.root
        y_node = self.dummy
        # Find leaf to insert 
        while x_node != self.dummy and x_node.is_marked == False:
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
            if x_node != rb_tree_dummy and x_node.is_marked == True:
                if x_node.key < z_node.key:
                    self.root.left = x_node
                else:
                    self.root.right = x_node
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

        if z_node.left == self.dummy or z_node.left.is_marked == True:
            x_node = z_node.right 
            if x_node.is_marked == True:
                x_node = self.dummy 
                self.transplant(z_node, self.dummy)
            else:
                self.transplant(z_node,z_node.right)
            # note that nobody points to z_node, even that z_node still point to parent and right
        elif z_node.right == self.dummy or z_node.right.is_marked == True :
            x_node = z_node.left
            if x_node.is_marked == True:
                x_node = self.dummy 
                self.transplant(z_node,self.dummy)
            else:
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
                if w_node == self.dummy or w_node.is_marked:
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
       while node != self.dummy and node.left != self.dummy and node.left.is_marked==False: 
           assert(node.left.key < node.key)
           node = node.left
       return node

    def find_max(self):
       node = self.root
       while node != self.dummy and node.right != self.dummy and node.right.is_marked==False: 
           assert(node.right.key > node.key)
           node = node.right
       return node
    
    def find_rank(self):
        node = self.root
        if node == self.dummy or node.is_marked == True:
            return 0
        node = node.right
        num_black = 0
        while node != self.dummy and node.is_marked==False:
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
        assert(node.is_marked == False)
        return node

    def find_node_rank_left(self, num_black):
        assert(num_black > -1)
        node = self.root
        while node != self.dummy and num_black != 0:
            node = node.left
            if node.color == 'Black':
                num_black = num_black - 1

        assert(node != self.dummy)
        assert(node.is_marked == False)
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
                node_right = node.right 
                if node.left != self.dummy:
                    left_tree.root = node.left
                    left_tree.root.color = 'Black'
                    node.left.parent = self.dummy
                    node.left = self.dummy
                    node.right = self.dummy 

                if node_right != self.dummy:
                    right_tree.root = node_right
                    right_tree.root.color = 'Black'
                    node_right.parent = self.dummy
                    node_right = self.dummy 
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

    def insert_npc_links(self, nodes):
        for n in nodes:
            assert n.is_marked == True
            node = self.root 
            assert node != rb_tree_dummy
            while True:
                if node.key < n.key:
                    if node.right == rb_tree_dummy:
                        node.right = n
                        n.parent = node
                        break 
                    node = node.right
                else:
                    if node.left == rb_tree_dummy:
                        node.left = n
                        n.parent = node
                        break
                    node = node.left

def concatenate_3(rb_tree_1, node, rb_tree_2):
    assert node != None and node != rb_tree_dummy 
    assert node.left == rb_tree_dummy or node.left.is_marked == True
    assert node.right == rb_tree_dummy or node.right.is_marked == True
    assert node.parent == rb_tree_dummy
    assert rb_tree_1 != None 
    if rb_tree_1.root == rb_tree_dummy or rb_tree_1.root.is_marked == True:
        node.color = 'Red'
        node.is_marked = False
        rb_tree_2.insert_node(node)
        return rb_tree_2
        
    assert rb_tree_2 != None 
    if rb_tree_2.root == rb_tree_dummy or rb_tree_2.root.is_marked == True: 
        node.color = 'Red'
        node.is_marked = False
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
        if node.left != rb_tree_dummy and node.left.is_marked == False: 
            node.left = rb_tree_dummy
        if node.right != rb_tree_dummy and node.right.is_marked == False: 
            node.right = rb_tree_dummy
        node.parent = rb_tree_dummy
    else: # tree 2 is higher and has larger keys
        node = rb_tree_1.find_max()
        assert node != rb_tree_1.dummy
        rb_tree_1.delete(node)
        if node.left != rb_tree_dummy and node.left.is_marked == False: 
            node.left = rb_tree_dummy
        if node.right != rb_tree_dummy and node.right.is_marked == False: 
            node.right = rb_tree_dummy
        node.parent = rb_tree_dummy

    return concatenate_3(rb_tree_1, node, rb_tree_2) 


def assign_max_min_depth(node):
    if node == rb_tree_dummy or node.is_marked == True:
        return

    assign_max_min_depth(node.left)
    assign_max_min_depth(node.right)

    l_depth = sys.maxint
    if node.left != rb_tree_dummy and node.left.is_marked == False:
        l_depth = node.left.min_depth
    r_depth = sys.maxint
    if node.right != rb_tree_dummy and node.right.is_marked == False:
        r_depth = node.right.min_depth
    
    node.min_depth = min(node.depth, min(r_depth,l_depth))

    l_depth = -sys.maxint-1
    if node.left != rb_tree_dummy and node.left.is_marked == False: 
        l_depth = node.left.max_depth
    r_depth = -sys.maxint-1
    if node.right != rb_tree_dummy and node.right.is_marked == False:
        r_depth = node.right.max_depth

    node.max_depth = max(node.depth, max(r_depth,l_depth))


def create_tango_tree_from_rb_tree(node, depth):
    assert depth > -1
    #assert x_node is a node in rb_tree 
    if node == rb_tree_dummy:
        return rb_tree_dummy
    
    aux_tree = Rb_tree()
    t_node = TangoNode(node.key, depth)
    aux_tree.insert_node(t_node) 
     
    npc_link_nodes = []
    aux_tree_np = create_tango_tree_from_rb_tree(node.right, depth+1)
    if aux_tree_np != rb_tree_dummy and aux_tree_np.root != rb_tree_dummy:
        assert  aux_tree_np.root.is_marked == True # Non-prefered children are root of another RB-tree
        npc_link_nodes.append(aux_tree_np.root)

    while node.left != rb_tree_dummy:
        node = node.left
        depth = depth + 1
        tmp_node = TangoNode(node.key,depth)
        aux_tree.insert_node(tmp_node) 
        aux_tree_np = create_tango_tree_from_rb_tree(node.right, depth+1)
        if aux_tree_np != rb_tree_dummy and aux_tree_np.root != rb_tree_dummy:
            npc_link_nodes.append(aux_tree_np.root)

    aux_tree.insert_npc_links(npc_link_nodes)
    assign_max_min_depth(aux_tree.root)

    aux_tree.root.is_marked = True
    return aux_tree 

#node l of minimum key value that has depth greater than d.
def find_l_node(t_node, depth_cut): # read paper for details
    assert depth_cut > -1
    assert t_node != rb_tree_dummy

    smallest = rb_tree_dummy
    if t_node.depth > depth_cut:
        smallest = t_node

    while True:
        if t_node.left != rb_tree_dummy and t_node.left.is_marked == False and t_node.left.max_depth > depth_cut:
            t_node = t_node.left
            if t_node.depth > depth_cut:
                smallest = t_node
        elif t_node.right != rb_tree_dummy and t_node.right.is_marked == False and smallest == rb_tree_dummy and t_node.right.max_depth>depth_cut:
            t_node = t_node.right
            if t_node.depth > depth_cut:
                smallest = t_node
        else:
            return smallest 

#node r of maximum key value that has depth greater than d.
def find_r_node(t_node, depth_cut): # read paper for details
    assert depth_cut > -1
    assert t_node != rb_tree_dummy
   
    greatest = rb_tree_dummy
    if t_node.depth > depth_cut:
        greatest = t_node

    while True:
        if t_node.right != rb_tree_dummy and t_node.right.is_marked==False and t_node.right.max_depth > depth_cut:
            t_node = t_node.right
            if t_node.depth > depth_cut:
                greatest = t_node
        elif t_node.left != rb_tree_dummy and t_node.left.is_marked==False and greatest==rb_tree_dummy and t_node.left.max_depth > depth_cut:
            t_node = t_node.left
            if t_node.depth >= depth_cut:
                greatest = t_node
        else:
            return greatest 

def find_predecessor(node):
    assert node != rb_tree_dummy
    if node.left == rb_tree_dummy or node.left.is_marked == True:
        # go up in the tree
        if node.parent != rb_tree_dummy and node.is_marked == False: 
            grand_parent = node.parent.parent 
            if node.parent.right == node:
                return node.parent
            elif node.parent.left == node and grand_parent !=rb_tree_dummy and grand_parent.right == node.parent:   
                return grand_parent
        return rb_tree_dummy

    node = node.left
    while not_dummy_or_marked(node) and not_dummy_or_marked(node.right):
       node = node.right 
    
    return node

def find_successor(node):
    assert node != rb_tree_dummy
    if node.right == rb_tree_dummy or node.right.is_marked == True:
        if node.parent != rb_tree_dummy and node.parent.left == node:
            return node.parent
        else:
            return rb_tree_dummy

    node = node.right
    while not_dummy_or_marked(node) and not_dummy_or_marked(node.left):
        node = node.left
    return node

def tango_cut(rb_tree, depth):
    assert rb_tree.root != rb_tree_dummy
    assert depth > -1
    node = rb_tree.root
    assert depth <= node.max_depth and depth >= node.min_depth
    l_node = find_l_node(node, depth)             
    l_p = find_predecessor(l_node)
    r_node = find_r_node(node, depth)             
    r_p = find_successor(r_node)
    # Interval where the tree has to be cut (l_p,r_p). Note that rb_tree_dummy denotes infinity.
    # e.g., l_p = rb_tree_dummy, r_p = 3 => (-inf.,3)  
    assert l_p != rb_tree_dummy or r_p != rb_tree_dummy
    
    b_tree = rb_tree_dummy 
    c_tree = rb_tree_dummy
    d_tree = rb_tree_dummy
    e_tree = rb_tree_dummy
   
    if l_p != rb_tree_dummy:
        (node_l, b_tree, c_tree) = rb_tree.split(l_p.key) 
    else:
        c_tree = rb_tree

    if r_p != rb_tree_dummy:
        (node_r, d_tree, e_tree) = c_tree.split(r_p.key) 
    else:
        d_tree = c_tree

    assert d_tree != rb_tree_dummy 
    # mark d_tree as new tree
    d_tree.root.is_marked = True 

    if r_p != rb_tree_dummy:
        tmp_tree = Rb_tree()
        c_tree = concatenate_3(tmp_tree, node_r, e_tree)  # forall(keys(rb_tree_2) > keys(rb_tree)) 
    if l_p != rb_tree_dummy:
        rb_tree = concatenate_3(b_tree, node_l, c_tree)
    else:
        rb_tree = c_tree 

    assert rb_tree != rb_tree_dummy 
    assert d_tree != rb_tree_dummy 
    # Slow but secure. First implementation
    rb_tree.root.is_marked = False
    assign_max_min_depth(rb_tree.root)
    rb_tree.root.is_marked = True

    d_tree.root.is_marked = False
    assign_max_min_depth(d_tree.root)
    d_tree.root.is_marked = True

    #Insert the non-prefered chlid link to the separated tree
    rb_tree.insert_npc_links([d_tree.root])
    return rb_tree

def not_dummy_or_marked(node):
    return node != rb_tree_dummy and node.is_marked == False

# find the biggest node.key smaller than key
def find_link_smaller(node,key):
  
    predecessor = rb_tree_dummy
    if node.key < key:
        predecessor = node

    if node.key > key:
        node = node.left
    elif node.key < key:
        node = node.right
    else:
        assert 0 != 0 

    while not_dummy_or_marked(node) and not_dummy_or_marked(node.left) and node.key > key:
        node = node.left 
    
    if node == rb_tree_dummy or node.is_marked == True or node.key > key:
        return predecessor

    assert node.key < key and node != rb_tree_dummy
    while not_dummy_or_marked(node.right): 
        node = node.right
    
    assert node != rb_tree_dummy
    assert node.key < key
    return node

#find the smallest node.key greater than key 
def find_link_greater(node,key):

    greater = rb_tree_dummy
    if node.key > key:
        greater = node

    if node.key > key:
       node = node.left  
    elif node.key < key:
        node = node.right
    else:
        assert 0 != 0 

    while not_dummy_or_marked(node) and not_dummy_or_marked(node.right) and node.key < key:  
        node = node.right

    if node == rb_tree_dummy or node.is_marked == True or node.key < key:
        return greater
    
    assert node != rb_tree_dummy
    assert node.key > key 
    
    while not_dummy_or_marked(node.left):
        node = node.left

    assert node != rb_tree_dummy
    assert node.key > key
    return node

def find_link(node, key): # find the two nodes between the value
    l_p = find_link_smaller(node, key)
    r_p = find_link_greater(node, key)
    return (l_p, r_p)

def tango_join(rb_tree, d_tree):
    assert rb_tree != None and d_tree != None

    if rb_tree.root == rb_tree_dummy:
        return d_tree

    if d_tree.root == rb_tree_dummy:
        return rb_tree

    assert rb_tree.root.max_depth < d_tree.root.max_depth 
    (l_p,r_p) = find_link(rb_tree.root, d_tree.root.key)

    # The interval where the tree has to be cut (l_p,r_p). Note that rb_tree_dummy denotes infinity.
    # e.g., l_p = rb_tree_dummy, r_p = 3 => (-inf.,3)  
    assert l_p != rb_tree_dummy or r_p != rb_tree_dummy
 
    b_tree = rb_tree_dummy 
    c_tree = rb_tree_dummy
    e_tree = rb_tree_dummy
   
    if l_p != rb_tree_dummy:
        (node_l, b_tree, c_tree) = rb_tree.split(l_p.key) 
    else:
        c_tree = rb_tree

    if r_p != rb_tree_dummy:
        (node_r, tmp_tree, e_tree) = c_tree.split(r_p.key) 
    else:
        d_tree = c_tree

    assert d_tree.root.key < r_p.key or r_p == rb_tree_dummy 
    # unmark d_tree as new tree
    d_tree.root.is_marked = False 
 
    if r_p != rb_tree_dummy:
        c_tree = concatenate_3(d_tree, node_r, e_tree)  # forall(keys(rb_tree_2) > keys(rb_tree)) 

    if l_p != rb_tree_dummy:
        rb_tree = concatenate_3(b_tree, node_l, c_tree)
    else:
        rb_tree = c_tree 

    assert rb_tree != rb_tree_dummy 
    assert d_tree != rb_tree_dummy 
    # Slow but secure. First implementation
    rb_tree.root.is_marked = False
    assign_max_min_depth(rb_tree.root)
    rb_tree.root.is_marked = True

    return rb_tree

def tango_find(rb_tree, key):
    node = rb_tree.root
    while node != rb_tree_dummy:
        if key < node.key:
            if node.left != rb_tree_dummy and node.left.is_marked:
                new_tree = Rb_tree()
                new_tree.root = node.left
                assert new_tree.root.color == 'Black' 
                rb_tree = tango_cut(rb_tree, node.left.min_depth -1)
                rb_tree = tango_join(rb_tree, new_tree)
                node = new_tree.root
            else:
                node = node.left
        elif key > node.key:
            if node.right.is_marked: # and node.right != rb_tree_dummy (implicit) 
                new_tree = Rb_tree()
                new_tree.root = node.right
                assert new_tree.root.color == 'Black' 
                rb_tree = tango_cut(rb_tree, node.right.min_depth -1)
                rb_tree = tango_join(rb_tree, new_tree)
                node = new_tree.root
            else:
                node = node.right
        else:
           return (node,rb_tree) 

if __name__ == "__main__":
    rb_tree = Rb_tree()
    x = [44,22,3,61,34,89,79,65,5,28, 85, 90]
    #x = random.sample(range(1, 100000), 10000)
    for v in x:
        depth = 0
        rb_tree.insert_node(TangoNode(v, depth))

    aux_tree = create_tango_tree_from_rb_tree(rb_tree.root, 0)
    #(node_found, aux_tree) = tango_find(aux_tree, 90)
    (node_found, aux_tree) = tango_find(aux_tree, 28)
