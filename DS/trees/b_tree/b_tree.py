'''
Simple B-tree implementation from CLRS with minimum degree t = 4.
'''

import pdb
import random

class Node():
    def __init__(self):
        self.num = 0
        self.keys = [None,None,None,None,None,None,None]
        self.pointers = [None,None,None,None,None,None,None,None]
        self.is_leaf = True

class B_tree():
    def __init__(self):
        self.root = Node() 

def search(node, key):
    assert node != None
    #assert node.num == len(num.keys)
    i = 0
    while i < node.num and node.keys[i] < key:
        i = i + 1
    if i < 7 and node.keys[i] == key:
        return (node,i)
    elif node.is_leaf == True:
        return (None,None)
    else:
        return search(node.pointers[i], key)
  
def fill(arr, first, last, val):
    while first != last:
        arr[first] = val
        first += 1

def copy_arr(arr, first, last, d_arr, d_first):
    while first != last:
        d_arr[d_first] = arr[first]
        d_first = d_first + 1
        first = first + 1

def copy(arr, first, last, d_first):
    assert d_first < first
    while first != last:
        arr[d_first] = arr[first]
        d_first = d_first + 1
        first = first + 1

def copy_backwards(arr, first, last, d_last):
    assert d_last >= last
    print "first = " + str(first) + ' last=' + str(last) + ' dlast=' + str(d_last)
    while first < last:
        arr[d_last-1] = arr[last-1] 
        d_last = d_last - 1
        last = last -1

def is_node_full(node):
    assert node.num < 8
    return node.num == 7 # 2t -1 

def find_if(start, last, arr, key):
    i = start
    while i < last and arr[i] < key:
        i = i + 1
    return i

def ascending_order(node):
    assert node != None
    assert node.num != 0
    if node.num < 7:
        assert node.keys[node.num] == None
        assert node.pointers[node.num+1] == None

    i = 0
    while i < node.num - 1:
        if node.keys[i] > node.keys[i+1]:
            return False
        i = i + 1
    return True

def pointers_exist(node):
    assert node != None
    assert node.is_leaf == False
    i = 0
    while i < node.num+1:
        if node.pointers[i] == None:
            return False
        i = i + 1
    return True

def well_formed(root, node):
    assert root != None 
    assert node != None
    assert node.num != 0
    rc = ascending_order(node)
    if node.is_leaf == False:
        rc = rc and pointers_exist(node)
    if root != node:
        rc = rc and node.num >=3 
    return rc

def insert_non_full(node, key):
    if node.is_leaf == True and node.pointers[0] != None:
        pdb.set_trace()
        assert 0 != 0 

    if node.is_leaf == True:
        i = find_if(0, node.num, node.keys, key)
        copy_backwards(node.keys, i, node.num, node.num+1)
        node.keys[i] = key
        node.num = node.num + 1
    else:
        i = find_if(0, node.num, node.keys, key)
        if node.keys[i] == key:
            return (node,i)
        
        if is_node_full(node.pointers[i]):
            split_child(node,i)
            if key > node.keys[i]:
                i = i + 1
        insert_non_full(node.pointers[i],key)

def insert(b_tree, key):
    r = b_tree.root
    if is_node_full(r): # root is full
        s = Node()
        b_tree.root = s
        s.num = 0
        s.pointers[0] = r
        s.is_leaf = False
        split_child(s,0)
        insert_non_full(s, key)
        
        assert well_formed(b_tree.root,s)
        assert well_formed(b_tree.root, s.pointers[0]) 
        assert well_formed(b_tree.root, s.pointers[1]) 
    else:
        insert_non_full(r, key)

def split_child(node,i):
    assert node != None
    assert i > -1 and i < node.num +1
    assert node.pointers[i] != None 
    assert is_node_full(node.pointers[i])  # node is full 2t-1 keys  

    left = node.pointers[i]
    right = Node()
    right.is_leaf = left.is_leaf

    copy_arr(left.keys, 4, 7, right.keys, 0)
    fill(left.keys, 4, 7, None)
    left.num -= 3
    right.num += 3
    copy_arr(left.pointers, 4, 8, right.pointers, 0)
    fill(left.pointers, 4, 8, None)
    #Make place at the node position i
    assert not is_node_full(node) # 2t since node cannot be full. -1 since arrays start at 0 
    copy_backwards(node.keys, i, node.num, node.num+1)

    #Copy pointers at node
    assert node.num + 1 < 2*4 # 2t + 1 since node cannot be full. -1 since arrays start at 0 
    copy_backwards(node.pointers, i+1, node.num+1, node.num+2)
    node.pointers[i+1] = right
   
    node.keys[i] = left.keys[3] # position 3 is the middle of arrays of 7 elements
    left.keys[3] = None
    left.num = left.num - 1
    node.num = node.num + 1
    
    assert left.num == 3
    assert right.num == 3

def find_predeccesor(node,i):
    assert node != None
    node = node.pointers[i]
    while node.is_leaf == False:
        node = node.pointers[node.num]
    return node.keys[node.num-1]

def find_successor(node,i):
    assert node != None
    node = node.pointers[i+1]
    while node.is_leaf == False:
        node = node.pointers[0]
    return node.keys[0]

def delete(root, node, key):

    assert well_formed(root, node)

    i = find_if(0, node.num, node.keys, key)
    if i < 7 and node.keys[i] == key: 
        # Case 1: key in the node and node is a leaf, delete the key
        if node.is_leaf == True:
            assert node.num >=4 # t value
            copy(node.keys, i+1, node.num, i) # move right
            node.num = node.num - 1
            node.keys[node.num] = None  
            assert well_formed(root, node)
            return
        # Case 2: key in the node but node is not leaf
        assert well_formed(root, node.pointers[i])
        assert well_formed(root, node.pointers[i+1])

        # Case 2.1: Left subtree more than t keys 
        if node.pointers[i].num >= 4:
            # Find predeccessor of node.keys[i]
            new_key = find_predeccesor(node,i)
            node.keys[i] = new_key 
            assert well_formed(root,node)
            delete(root, node.pointers[i],new_key)
             
        # Case 2.2: Left subtree less than t keys, but right subtree more than t keys
        elif node.pointers[i+1].num >= 4:
            # Find successor of node.keys[i]
            new_key = find_successor(node,i)
            node.keys[i] = new_key 
            assert well_formed(root,node)
            delete(root, node.pointers[i+1],new_key)

        #Case 2.3: Merge both subtrees  
        else: 
            #assert node.pointers[i].num == 3
            #assert node.pointers[i+1].num == 3
            #Merge left and right nodes
            left = node.pointers[i]
            right = node.pointers[i+1]
            copy_arr(right.keys, 0, 3, left.keys, 4)
            copy_arr(right.pointers,0, 4, left.pointers, 4) 

            left.keys[3] = node.keys[i]
            left.num += 4
            assert well_formed(root, left)

            copy(node.keys, i+1, node.num, i)
            node.keys[node.num-1] = None
            copy(node.pointers, i+2, node.num + 1, i+1) 
            node.pointers[node.num] = None
            node.num -= 1
            if node.num == 0:
                assert node == root
                root = node.pointers[i]
            else:
                assert well_formed(root, node)
            delete(root, node.pointers[i], key)
    else:
    #Case 3:  
        assert well_formed(root, node.pointers[i])
        if node.pointers[i].num > 3:
            delete(root, node.pointers[i], key)
            return
        left = node.pointers[i-1]
        right = None
        if i < 7: 
            right = node.pointers[i+1]
        head = node.pointers[i]
        # Take key from the left sibling
        if i > 0 and left.num > 3:
            copy_backwards(head.keys,0, head.num, head.num+1)
            head.keys[0] = node.keys[i-1]
            copy_backwards(head.pointers, 0, head.num+1, head.num+2) 
            head.pointers[0] = left.pointers[left.num]
            head.num += 1
            assert well_formed(root,head)
            node.keys[i-1] = left.keys[left.num-1]
            assert well_formed(root,node)
            left.keys[left.num-1] = None
            left.pointers[left.num] = None
            left.num -= 1
            assert well_formed(root,left)
            delete(root, head, key)
        # Take key from the right sibling
        elif i < node.num and right != None and right.num > 3:
            head.keys[head.num] = node.keys[i] 
            head.pointers[head.num+1] = right.pointers[0]
            head.num += 1
            assert well_formed(root,head)
            node.keys[i] = right.keys[0]
            assert well_formed(root,node)
            copy(right.keys, 1, right.num, 0) 
            right.keys[right.num-1] = None
            copy(right.pointers, 1, right.num+1, 0)
            right.pointers[right.num] = None
            right.num -= 1
            assert well_formed(root,right)
            delete(root, head, key)
        # Merge node.pointer[i] with node.pointer[i-1] or  node.pointer[i+1] 
        else:
            #Merge with the left subtree
            if i > 0:
                copy_arr(head.keys, 0, head.num, left.keys, 4)
                copy_arr(head.pointers, 0, head.num + 1, left.pointers, 4)
                left.keys[3] = node.keys[i-1]
                left.num += head.num + 1
                assert well_formed(root,left)
                copy(node.keys, i, node.num, i-1)
                copy(node.pointers, i+1, node.num+1, i)
                node.keys[node.num-1] = None
                node.pointers[node.num] = None
                node.num -= 1
                assert well_formed(root,node)
                delete(root, left, key)
            #Merge with the right subtree
            else:
                copy_arr(right.keys, 0, right.num, head.keys, 4)
                copy_arr(right.pointers, 0, right.num+1, head.pointers, 4)
                head.keys[3] = node.keys[i]
                head.num += right.num + 1
                assert well_formed(root,head)
                copy(node.keys,i+1, node.num, i) 
                copy(node.pointers, i+2, node.num +1, i+1)
                node.keys[node.num-1] = None
                node.pointers[node.num] = None
                node.num -= 1
                assert well_formed(root,node)
                delete(root, head, key)

def print_in_order(node):
    if node.is_leaf == True:
        for i in range(node.num):
            print 'val =' + str(node.keys[i])
        return
    for i in range(node.num+1):
        print_in_order(node.pointers[i])
        if i != node.num:
            print 'val = ' + str(node.keys[i])

if __name__ == "__main__":
    b_tree = B_tree()
    #x = [1,4,56,2,34,21,23,57,76,54,3,24,58, 102, 3902,13,32,50, 20,10,7, 3789,234,3267,76,900] 
    #x = [1,2,3,4,5,6,7,8,9,10,11,12] 
    x = random.sample(range(1, 100000), 10000)
    for x_i in x:
        insert(b_tree, x_i)

    print_in_order(b_tree.root)
    flag = True
    for x_i in x:
        if x_i % 2:
            if flag == True:
                (node,i) = search(b_tree.root, x_i)                
                assert node != None and i != None
                print 'Found node.keys[i] = ' + str(node.keys[i]) + ' and x_i = ' + str(x_i)
                delete(b_tree.root, b_tree.root,x_i) 
                flag = False
            else:
                flag = True
    print_in_order(b_tree.root)
