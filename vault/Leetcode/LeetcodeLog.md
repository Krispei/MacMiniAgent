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

# Oct 26 2026
101 Symmetric Tree
- My solution made sure that both the left - right pairs were either occupied or none before adding to the stack / not adding, and also remember the symmetry
111 Minimum Depth of Binary Tree
- First did a dfs like search but then i realized i can do a much faster solution if i simply to BFS and quit once i find a child.
112 Path Sum
- Did this recursively -- end condition was when the node was a leaf node. I also added the sum when processing the node not when calling the function -- effectively the same but helps clean up the last step

