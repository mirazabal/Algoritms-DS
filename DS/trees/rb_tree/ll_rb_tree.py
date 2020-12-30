'''
    Left-leaning RB tree. Implemented according to the LLRB paper from Sedgewick.
'''
import pdb
import random

class Node:
    def __init__(self,key):
        self.key = key
        self.left = None
        self.right = None
        self.color = 'Red'

class Rb_tree:
    def __init__(self):
        self.root = None

    def rotate_left(self,h):
        assert h != None
        assert h.right != None
        x = h.right
        h.right = x.left
        x.left = h
        x.color = h.color
        h.color = 'Red'
        return x

    def rotate_right(self,h):
        assert h != None
        assert h.left != None
        x = h.left
        h.left = x.right
        x.right = h
        x.color = h.color
        h.color = 'Red'
        return x

    def flip_colors(self, h):
        h.color = 'Black' if h.color == 'Red' else 'Red'
        h.left.color = 'Black' if h.left.color == 'Red' else 'Red'
        h.right.color = 'Black' if h.right.color == 'Red' else 'Red'

    def create_node(self,key):
        x_node = Node(key)
        return x_node
    
    def fix_up(self,h):
        if (h.right!=None and h.right.color=='Red') and (h.left==None or h.left.color=='Black'):
            h = self.rotate_left(h)
        if (h.left!=None and h.left.color=='Red') and (h.left!=None and h.left.left!=None and h.left.left.color=='Red'):
            h = self.rotate_right(h)
        if (h.left!=None and h.left.color=='Red') and (h.right!=None and h.right.color=='Red'):
            self.flip_colors(h)
        return h

    def insert(self,key):
        self.root = self.insert_fixup(self.root,key)
        self.root.color = 'Black'

    def insert_fixup(self,h,key):

        if h == None:
            return self.create_node(key)

        if key == h.key:
            print 'Same key asked, so replace'
        elif key < h.key: 
            h.left = self.insert_fixup(h.left,key)
        else:
            h.right = self.insert_fixup(h.right,key)

        h = self.fix_up(h)
        return h

    def print_tree(self,x_node):
        if x_node != None:
            self.print_tree(x_node.left)
            print "Value = " + str(x_node.key)
            self.print_tree(x_node.right)


    def move_red_left(self,h):
        self.flip_colors(h)
        if h.right != None and h.right.left != None and h.right.left.color == 'Red':
            assert h.right.left != None
            h.right = self.rotate_right(h.right)
            h = self.rotate_left(h)
            self.flip_colors(h)
            assert h.left.left.color == 'Red'
        return h

    def move_red_right(self,h):
        self.flip_colors(h)
        if h.left != None and h.left.left != None and h.left.left.color == 'Red':
            h = self.rotate_right(h)
            self.flip_colors(h)
            assert h.right.right.color == 'Red'
        return h


    def delete(self, key):
        self.root = self.delete_fixup(self.root,key)
        if self.root != None:
            self.root.color = 'Black'
   
# Idea: Move to the left, since the minimum while be on the left most leaf of the tree.
# Maintain the invariant, that either the actual node or the node's left child is red. (BST 3-Node).
# Use the move_red_left to maintain it.
# Since, there are no two consecutive red's in a rb-tree and the leaf's child is 'Black', when 
# the algorithm reaches the min leaf, it must be 'Red' and can therefore be deleted without causing
# any violation. On the way up the stack, fix possible right leaning Red links with fix_up
    def delete_min(self,h):
        if h.left == None:
            assert h.color == 'Red'
            return None

        if h.left.color == 'Black' and (h.left.left == None or h.left.left.color == 'Black'):
            h = self.move_red_left(h)
        
        assert h.color == 'Red' or h.left.color == 'Red' 
        h.left = self.delete_min(h.left)
        
        return self.fix_up(h)

    def minimum(self,node):
        while node.left != None:
            node = node.left
        return node

# Idea. Find the node to delete. Exchange it with the successor, that is on the right subtree. 
# Delete the successor (delete_min). While searching the succesor, change the nodes color, so that
# when the succesor is found, it is red. Red nodes from the leafs can be deleted without violatng
# any invariant. Fixup the tree while unwinding the stack to preserve the left-leaning property
    def delete_fixup(self,h,key):
        if key < h.key:
            l_black = (h.left == None or h.left.color == 'Black') 
            ll_black = h.left != None and (h.left.left == None or h.left.left.color == 'Black')

            root = True if h == self.root else False
            if l_black and ll_black:
                h = self.move_red_left(h)

            if root == True: 
                assert h.color == 'Red' or h.left.color == 'Red' or h.left.left.color == 'Red' 
            else:
                assert h.color == 'Red' or h.left.color == 'Red'  

            # Same argument as delete_min
            h.left = self.delete_fixup(h.left,key)
        else:
            # Rotate to move red link to the right
            if h.left != None and h.left.color == 'Red':
                h = self.rotate_right(h)
            
            # We are at the bottom leaf, so we can securely delete the node 
            # if h.right == None, it could only either h.left.color == 'Red' or h.left == None 
            # to maintain rb-tree property of equal black nodes in the path
            # (None considered as Black). If h.left.color == 'Red', we have already rotate it,
            # so this possibility cannot exist
            if key == h.key and h.right == None:
                assert h.color == 'Red' or h == self.root 
                assert h.left == None
                return None

            # Create a red in the links searching for the deletion node 
            if (h.right!=None and h.right.color=='Black') and (h.right.left==None or h.right.left.color=='Black'):
                assert h.left != None
                h = self.move_red_right(h)

            if key == h.key:
                # find the successor node 
                succ_node = self.minimum(h.right)
                # change content
                h.key = succ_node.key
                # delete the succesor node. Create red invariants on the way
                h.right = self.delete_min(h.right)
            else:
                h.right = self.delete_fixup(h.right,key)

        # while unwinding the stack, redo the invariants
        return self.fix_up(h)


if __name__ == "__main__":
    rb_tree = Rb_tree()

    x = random.sample(range(1, 1000000), 100000)
#    x = [44,22,3,61,34,89,79,65,5,28]
#    x = [88,11,91,25,17,81,3,94,43,58]
#    x = [571,865,298,769,533,638,875,412,515,827,110,281,254,696,82,167,748,55,186,257]
    for v in x:
        print 'Inserting v = ' + str(v)
        rb_tree.insert(v)

    flag = True
    for v in reversed(x):
        if flag == True:
            print ' Deleting v = ' + str(v)
            rb_tree.delete(v)
            flag = False
        else:
            flag = True

    rb_tree.print_tree(rb_tree.root)

