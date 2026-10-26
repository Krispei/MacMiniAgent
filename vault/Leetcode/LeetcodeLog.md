# Oct 25 2026
144 Binary Tree Preorder traversal
- Recursive solution: add order is: Head, then recurse left, recurse right
- Iterative solution: push to the stack in reverse order of what i want to process
94 Binary Tree Inorder Traversal
- Recursive solution: order: recurse left, head, recurse right
- Try to greedily go to the left as far as possible while adding nodes and only try to go right when left has been completely exhausted.
145 Binary Tree Postorder Traversal
- Recursive solution: Order: recurse left, recurse right, head
- Keep a prev tracker and only append when we know that the right tree has finished (when prev is on the right tree)
102 Binary Tree Level Order Traversal
- Recursive solution: should only add a new level if we know that the next levels actually exist and are not None
[226. Invert Binary Tree](https://leetcode.com/problems/invert-binary-tree/)\

