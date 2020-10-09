'''
    RB tree implemented a la CLRS

    Red-Black trees have 5 properties:
    1- Every node is Red or Black
    2- The root is black
    3- Every leaf is black
    4- If a node is red, then both its children are black
    5- For each node, all simple paths from the node to descendant leaves contain the same number of black nodes 

    Lemma 1: a red-black tree with n internal nodes has a height at most 2lg(n+1)
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

class Node():
    def __init__(self,key):
        self.key = key
        self.parent = None
        self.left = None
        self.right = None
        self.color = 'Red'

class Rb_tree():
    def __init__(self):
        self.dummy = DummyNode()
        self.root = self.dummy 
        self.last_value = 0


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


    def insert(self,z_node):
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
                x_node = x_node.left
            else:
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
 #

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
            x_node = x_node.left
        return x_node

    def find(self, node, value):
        while node != self.dummy and node.key != value:
            if value < node.key: 
                node = node.left
            else: 
                node = node.right

        return node 

    def create_dummy_node(self, parent_node, direction):
        assert direction == 'r' or direction == 'l'
        x_node = DummyNode()
        x_node.parent = parent_node
        if direction == 'r':
            parent_node.right = x_node
        else:
            parent_node.left = x_node

        return x_node


    def delete(self, z_node):
        original_color = z_node.color
        x_node = z_node
        y_node = z_node

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



if __name__ == "__main__":
    rb_tree = Rb_tree()

    #x = [44,22,3,61,34,89,79,65,5,28]
    x = random.sample(range(1, 100000), 10000)
    for v in x:
        rb_tree.insert(rb_tree.create_node(v));

    odd = True
    for v in x:
        if odd == True:
            print 'delete node = ' + str(v)
            node_del = rb_tree.find(rb_tree.root,v)
            assert node_del != rb_tree.dummy
            rb_tree.delete(node_del)
            odd = False
        else:
            odd = True

    rb_tree.in_order_traversal(rb_tree.root)
