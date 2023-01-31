from node import Node

class AVL:
    def __init__(self):
        self.root = None

    def add(self, value):
        if self.root is None:
            self.root = Node(value)
        else:
            #call recursive add
            self._add(value, self.root)
        return self

    def _add(self, value, current):
        #checks to see where to place the new node
        if value < current.value:
            if current.left is None:
                current.left = Node(value)
                current.left.parent = current
                self.check_insert(current.left)
            else:
                self._add(value, current.left)
        elif value > current.value:
            if current.right is None:
                current.right = Node(value)
                current.right.parent = current
                self.check_insert(current.right)
            else:
                self._add(value, current.right)

    #basic height method
    def height(self):
        if self.root is not None:
            #calls recursive method
            return self._height(self.root, 0)
        else:
            return 0

    #recursive height method
    def _height(self, node, current=0):
        #base case
        if node is None:
            return current

        leftvalue = self._height(node.left, current+1)
        rightvalue = self._height(node.right, current+1)

        if leftvalue > rightvalue:
            return leftvalue
        else:
            return rightvalue

    #bane of my existence function
    def remove(self, value):
        node = self.find(value)
        if node is not None:
            return self.remove_node(node)
        else:
            return self

    #sleepless night function
    def remove_node(self, data):

        #[Static]
        def min_value(newnode):
            current = newnode
            if current is None:
                return None
            while current.right is not None:
                current = current.right
            return current

        #[STATIC FUNCTION]
        def num_child(newnode):
            num = 0
            if newnode.left is not None:
                #print("left",newnode.left.value)
                num += 1
            if newnode.right is not None:
                # print("right",newnode.right.value)
                num += 1
            # print(num)
            return num

        if data is None or self.find(data.value) is None:
            return None

        newparent = data.parent
        children = num_child(data)

        #case 1
        #If the current node has no children
        if children == 0:
            if newparent is not None:
                if newparent.left == data:
                    newparent.left = None
                else:
                    newparent.right = None
            else:
                self.root = None

        #case 2
        #if the current node has a single child
        elif children == 1:
            if data.left is not None:
                newchild = data.left
            else:
                newchild = data.right

            if newparent is not None:
                if newparent.left == data:
                    newparent.left = newchild
                else:
                    newparent.right = newchild
            else:
                self.root = newchild

            newchild.parent = newparent

        #case 3
        #if the current node has two children :( so sad
        elif children == 2:
            swap = min_value(data.left)
            data.value = swap.value
            self.remove_node(min_value(swap))
            return self

        if newparent is not None:
            newparent.height = 1 + max(self._height(newparent.left), self._height(newparent.right))
            self.check_delete(newparent)

        return self

    #For final project! (similar to contains)
    def find(self, value):
        if self.root is not None:
            return self._find(value, self.root)
        else:
            return None

    #recurses through to find value of a given node (similar to contains)
    def _find(self, value, current):
        if current.value == value:
            return current

        elif (current.value > value) and (current.left is not None):
            return self._find(value, current.left)

        elif (current.value < value) and (current.right is not None):
            return self._find(value, current.right)

    #Simple contains call
    def contains(self, value):
        if self.root is not None:
            return self._contains(value, self.root)
        else:
            return False

    #Recursive implementation of contains
    def _contains(self, value, current):
        if current.value == value:
            return True

        elif (current.value > value) and (current.left is not None):
            return self._contains(value, current.left)

        elif (current.value < value) and (current.right is not None):
            return self._contains(value, current.right)

        return False

    # size function
    def size(self):
        if self.root is None:
            return 0
        else:
            return int(self._size(self.root))

    #recursive size function that recurses through, and finds the size
    def _size(self, node):
        if node is None:
            return 0
        else:
            if node.left is not None and node.right is not None:
                return self._size(node.left) + self._size(node.right) + 1
            if node.left is None and node.right is None:
                return 1
            if node.left is None:
                return self._size(node.right) + 1
            if node.right is None:
                return self._size(node.left) + 1

    def check_insert(self, current, trace=None):
        if trace is None:
            trace = []
        if current.parent is None:
            return self
        trace = [current] + trace

        height_left = self._height(current.parent.left)
        height_right = self._height(current.parent.right)

        if height_right - height_left >= 2 or height_right - height_left <= -2:
            trace = [current.parent]+trace
            self.balance(trace[0], trace[1], trace[2])
            return self

        height = 1 + current.height
        if height > current.parent.height:
            current.parent.height = height

        self.check_insert(current.parent, trace)
        return self

    def check_delete(self, current):
        if current is None:
            return self

        height_left = self._height(current.left)
        height_right = self._height(current.right)

        if (height_right - height_left >= 2) or (height_right - height_left) <= -2:
            curr_child = self.node_child(current)
            child_child = self.node_child(curr_child)
            self.balance(current, curr_child, child_child)

        self.check_delete(current.parent)

        return self

    def balance(self, curr, curr_child, child_child):
        if curr_child == curr.left and child_child == curr_child.left:
            self.rotate_right(curr)
        elif curr_child == curr.left and child_child == curr_child.right:
            self.rotate_left(curr_child)
            self.rotate_right(curr)
        elif curr_child == curr.right and child_child == curr_child.right:
            self.rotate_left(curr)
        elif curr_child == curr.right and child_child == curr_child.left:
            self.rotate_right(curr_child)
            self.rotate_left(curr)

        return self

    def rotate_right(self, curr):
        newroot = curr.parent
        curr_child = curr.left
        t3_swap = curr_child.right
        curr_child.right = curr
        curr.parent = curr_child
        curr.left = t3_swap
        if t3_swap is not None:
            t3_swap.parent = curr
        curr_child.parent = newroot
        if curr_child.parent is None:
            self.root = curr_child
        else:
            if curr_child.parent.left == curr:
                curr_child.parent.left = curr_child
            else:
                curr_child.parent.right = curr_child
        curr.height = 1 + max(self._height(curr.left), self._height(curr.right))
        curr_child.height = 1 + max(self._height(curr_child.left), self._height(curr_child.right))

        return self

    def rotate_left(self, curr):
        newroot = curr.parent
        curr_child = curr.right
        t2_swap = curr_child.left
        curr_child.left = curr
        curr.parent = curr_child
        curr.right = t2_swap
        if t2_swap is not None:
            t2_swap.parent = curr
        curr_child.parent = newroot
        if curr_child.parent is None:
            self.root = curr_child
        else:
            if curr_child.parent.left == curr:
                curr_child.parent.left = curr_child
            else:
                curr_child.parent.right = curr_child
        curr.height = 1 + max(self._height(curr.left), self._height(curr.right))
        curr_child.height = 1 + max(self._height(curr_child.left), self._height(curr_child.right))

        return self

    def node_height(self, current):
        if current is None:
            return 0
        return current.height

    def node_child(self, current):
        left = self._height(current.left)
        right = self._height(current.right)
        if left >= right:
            return current.left
        else:
            return current.right

    #pre-order list
    def asList(self):
        returnlist = []
        if self.root is not None:
            self._asList(self.root, returnlist)
        return returnlist

    #pre-order list
    def _asList(self, node, returnlist):
        if node is not None:
            returnlist.append(node.value)
            self._asList(node.left, returnlist)
            self._asList(node.right, returnlist)
