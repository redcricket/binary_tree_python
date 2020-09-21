class Node:
    def __init__(self, value, left=None, right=None, level=0):
        self.value = value
        self.left = left
        self.right = right
        self.level = level

    def __str__(self):
        left_value = None
        if self.left:
            left_value = self.left.value
        right_value = None
        if self.right:
            right_value = self.right.value

        return f"l={self.level} v={self.level} {left_value} {right_value}."

    def set_left(self, node):
        self.left = node

    def set_right(self, node):
        self.right = node

    def insert(self, value, level=0):
        if value < self.value:
            if self.left is None:
                self.left = Node(value=value, level=level)
            else:
                self.left.insert(value=value, level=level+1)
        else:
            if self.right is None:
                self.right = Node(value=value, level=level)
            else:
                self.right.insert(value=value, level=level+1)

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        left, n, p, x = self.left._display_aux()
        right, m, q, y = self.right._display_aux()
        s = '%s' % self.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            left += [n * ' '] * (q - p)
        elif q < p:
            right += [m * ' '] * (p - q)
        zipped_lines = zip(left, right)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2

class Tree:
    def __init__(self):
        self.root = None

    def preorder_dlr(self, node, level=0):
        if not node:
            return None

        print(f"{level} {node.value}")
        self.preorder_dlr(node.left, level=level + 1)
        self.preorder_dlr(node.right, level=level + 1)

    def inorder_ldr(self, node, level=0):
        if not node:
            return None
        self.inorder_ldr(node.left, level=level + 1)
        print(f"{level} {node.value}")
        self.inorder_ldr(node.right, level=level + 1)

    def get_highest_left(self, node, level=0):
        if not node:
            return node

        current = node
        print(f"get_highest_left({node}) {node.level}")

        while current.right:
            print(node)
            current = current.right
        return current

    def postorder_lrd(self, node, level=0):
        if not node:
            return None

        self.postorder_lrd(node.left, level=level + 1)
        self.postorder_lrd(node.right, level=level + 1)
        print(f"{level} {node.value}")

    def set_levels(self, node, visited=None, level=0):
        if visited is None:
            visited = []
        if not node:
            return None

        if node not in visited:
            print(f"{level} {node.value}")
            node.level = level
            visited.append(node)
            for child in [node.left, node.right]:
                self.set_levels(node=child, visited=visited, level=level+1)

    def dfs(self, node, visited=None, level=0):
        if visited is None:
            visited = []

        print( f"len(dfs) visited is {len(visited)} level is {level}.")
        if not node:
            return None

        if node not in visited:
            print(f"{level} {node.value}")
            visited.append(node)
            for child in [node.left, node.right]:
                self.dfs(node=child, visited=visited, level=level+1)

    def breath_first(self, node):
        queue = []
        if not node:
            return None
        print(f"{node.level} {node.value}")
        queue.append(node)
        while queue:
            n = queue[0]
            print(f"{n.level} {n.value}")
            if n.left:
                queue.append(n.left)
            if n.right:
                queue.append(n.right)
            queue.pop(0)

    def insert(self, value, level=0):
        if self.root == None:
            self.root = Node(value, level=level)
            return

        if value < self.root.value:
            if self.root.left is None:
                self.root.left = Node(value=value, level=self.root.level + 1)
                return
            self.root.left.insert(value, level+1)
        else:
            if self.root.right is None:
                self.root.right = Node(value=value, level=self.root.level + 1)
                return
            self.root.insert(value, level+1)

    def find(self, node, value):
        queue = []
        if not node:
            return None
        if node.value == value:
            return node
        queue.append(node)
        while len(queue) > 0:
            n = queue[0]
            if n.value == value:
                return n
            print(f"{n.level} {n.value}")
            if n.left:
                queue.append(n.left)
            if n.right:
                queue.append(n.right)
            queue.pop(0)

    def delete_node(self, node, key):
        if self.root.value == key:
            right = self.root.right
            left = self.root.left
            # get last right node on left tree.
            # do depth first tranversal of right tree and get the last node.
            last_node = self.get_highest_left(left, level=0)
            print(f"get_highest_left() returned last_node {last_node}")
            last_node.right = right
            self.root = left
            return node

        # if node doesn't exist, just return it
        if not node:
            return node
        # Find the node in the left subtree	if key value is less than node value
        if node.value > key:
            node.left = self.delete_node(node.left, key)
        # Find the node in right subtree if key value is greater than node value,
        elif node.value < key:
            node.right = self.delete_node(node.right, key)
        # Delete the node if node.value == key
        else:
            # If there is no right children delete the node and new node would be node.left
            if not node.right:
                return node.left
            # If there is no left children delete the node and new node would be node.right
            if not node.left:
                return node.right
            # If both left and right children exist in the node replace its value with
            # the minmimum value in the right subtree. Now delete that minimum node
            # in the right subtree
            temp_val = node.right
            mini_val = temp_val.value
            while temp_val.left:
                temp_val = temp_val.left
                mini_val = temp_val.value
            # Delete the minimum node in right subtree
            node.right = self.delete_node(node.right, node.value)
        return node

"""
# Definition: Binary tree node.
class TreeNode(object):
    def __init__(self, x):
         self.val = x
         self.left = None
         self.right = None

def delete_node(root, key):
  # if root doesn't exist, just return it
	if not root: 
		return root
	# Find the node in the left subtree	if key value is less than root value
	if root.val > key: 
		root.left = delete_node(root.left, key)
	# Find the node in right subtree if key value is greater than root value, 
	elif root.val < key: 
		root.right= delete_node(root.right, key)
	# Delete the node if root.value == key
	else: 
	# If there is no right children delete the node and new root would be root.left
		if not root.right:
			return root.left
	# If there is no left children delete the node and new root would be root.right	
		if not root.left:
			return root.right
  # If both left and right children exist in the node replace its value with 
  # the minmimum value in the right subtree. Now delete that minimum node
  # in the right subtree
		temp_val = root.right
		mini_val = temp_val.val
		while temp_val.left:
			temp_val = temp_val.left
			mini_val = temp_val.val
  # Delete the minimum node in right subtree
		root.right = deleteNode(root.right,root.val)
	return root

def preOrder(node): 
    if not node: 
        return      
    print(node.val)
    preOrder(node.left) 
    preOrder(node.right)   
    
root = TreeNode(5)  
root.left = TreeNode(3)  
root.right = TreeNode(6) 
root.left.left = TreeNode(2)  
root.left.right = TreeNode(4) 
root.left.right.left = TreeNode(7)  
print("Original node:")
print(preOrder(root))
result = delete_node(root, 4)
print("After deleting specified node:")
print(preOrder(result))
"""