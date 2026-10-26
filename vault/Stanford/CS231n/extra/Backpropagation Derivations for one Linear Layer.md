
Backpropagation for 1 linear layer:

$$ y = XW$$
$$L = L(y)$$
Where 
- X has shape (N, D) 
- W has shape (D, M)
- Y has shape (N, M)

The derivatives we want to find are the following:

$$\frac{\partial L}{\partial X},\ \frac{\partial L}{\partial W}$$

We will eventually find that these derivatives end up being:

$$\frac{\partial L}{\partial X} = \frac{\partial L}{\partial y}W^T$$
$$\frac{\partial L}{\partial W} = X^T\frac{\partial L}{\partial y}$$
First, lets tackle $\frac{\partial L}{\partial X}$. 

First, take a note on the shape that these two must be. Because the loss function is a scalar valued function, $\frac{\partial L}{\partial X}$ must be a tensor of (1) x (N, D), which we can write as simply (N, D). we can express the entire derivative as:

$$\frac{\partial L}{\partial X} = \underbrace{
\begin{bmatrix} 
\frac{\partial L}{\partial X_{11}} &  \frac{\partial L}{\partial X_{12}}  & \dots & \frac{\partial L}{\partial X_{1D}} \\
\frac{\partial L}{\partial X_{21}} &  \frac{\partial L}{\partial X_{22}}  & \dots & \frac{\partial L}{\partial X_{2D}} \\
\vdots &  \vdots  & \ddots & \vdots \\ 
\frac{\partial L}{\partial X_{N1}} &  \frac{\partial L}{\partial X_{N2}}  & \dots & \frac{\partial L}{\partial X_{ND}} 
\end{bmatrix} \\[10pt]}_{\text{Matrix that is N x D, same shape as X}}$$


To find the value of each individual element of the matrix, we can use the chain rule

$$\frac{\partial L}{X_{ij}} = \frac{\partial L}{\partial y} \frac{\partial y}{X_{ij}}$$
$$\frac{\partial L}{X_{ij}} = \sum_{p}\sum_{q}\frac{\partial L}{\partial y_{pq}}\frac{\partial y_{pq}}{\partial X_{ij}}$$
to find the value of $\frac{\partial y_{pq}}{\partial X_{ij}}$ , lets look at the construction of y 

y = XW, the matrix multiplication of X and W. when doing matrix multiplication, the $pq^{th}$ element of y ($y_{pq}$) is the dot product of the $p^{th}$ row in X and the $q^{th}$ column in W. 

$X_{ij}$ again represents the value in the $i^{th}$ row and $j^{th}$ column. 

Combining these two facts, we can make sense in our head that any element in the first row of y ($p = 1$) should *only* depend on values in the first row of X ($i=1$). Thus, for any combinations of p and i where $p \neq i$, the derivative $\frac{\partial y_{pq}}{\partial X_{ij}}$ immediately becomes 0. 

for $p=i$, we see that $y_{pq} = x_{p1}w_{1q} + x_{p2}w_{2q} + \dots + x_{pD}w_{Dq}$ 

$$\frac{\partial\ x_{p1}w_{1q} + x_{p2}w_{2q} + \dots + x_{pD}w_{Dq}}{\partial x_{pj}} = w_{jq}$$

so 

$$\text{if p = i : }\frac{\partial y_{pq}}{\partial X_{ij}} = w_{jq}$$
$$\text{if p $\neq$ i : }\frac{\partial y_{pq}}{\partial X_{ij}} = 0$$

Combining these two facts, lets rewrite $\frac{\partial L}{X_{ij}}$:

$$\frac{\partial L}{X_{ij}} = \sum_{p}\sum_{q}\frac{\partial L}{\partial y_{pq}}\frac{\partial y_{pq}}{\partial X_{ij}}$$
$$\frac{\partial L}{X_{ij}} = \sum_{q}\frac{\partial L}{\partial y_{iq}}\frac{\partial y_{iq}}{\partial X_{ij}}$$
$$\frac{\partial L}{X_{ij}} = \sum_{q}\frac{\partial L}{\partial y_{iq}}w_{jq}$$

We can recognize this as the formula for an outer product. In order to keep the final derivative's shape (N, D) this is the outer product of:

$$\frac{\partial L}{\partial X} = \frac{\partial L}{\partial y} W^T$$

Now to look at $\frac{\partial L}{\partial W}$, we follow a similar process. The derivative should look something like this:

$$\frac{\partial L}{\partial W} = \underbrace{
\begin{bmatrix} 
\frac{\partial L}{\partial W_{11}} &  \frac{\partial L}{\partial W_{12}}  & \dots & \frac{\partial L}{\partial W_{1M}} \\
\frac{\partial L}{\partial W_{21}} &  \frac{\partial L}{\partial W_{22}}  & \dots & \frac{\partial L}{\partial W_{2M}} \\
\vdots &  \vdots  & \ddots & \vdots \\ 
\frac{\partial L}{\partial W_{D1}} &  \frac{\partial L}{\partial W_{D2}}  & \dots & \frac{\partial L}{\partial W_{DM}} 
\end{bmatrix} \\[10pt]}_{\text{Matrix that is D x M, same shape as W}}$$

Looking at each value $\frac{\partial L}{\partial W_{ij}}$, we can use the chain rule and express the value as:

$$\frac{\partial L}{\partial W_{ij}} = \frac{\partial L}{\partial y} \frac{\partial y}{\partial W_{ij}}$$
$$\frac{\partial L}{\partial W_{ij}} = \sum_{p}\sum_{q}\frac{\partial L}{\partial y_{pq}}\frac{\partial y_{pq}}{\partial W_{ij}}$$
Again, recall the that the $pq^{th}$ item of y is composed of the dot product between the $p^{th}$ row of X and the $q^{th}$ column of W. This means that any item of y in a column q where $q \neq j$ will not depend on $W_{ij}$, regardless of p or i. We can therefore collapse this summation into:

$$\frac{\partial L}{\partial W_{ij}} = \sum_p \frac{\partial L}{\partial y_{pj}}\frac{\partial y_{pj}}{\partial W_{ij}}$$

 Again, looking at the composition of y at index pj (The dot product between the $p^{th}$ row of X and the $j^{th}$ column of W), we see that:

$$y_{pj} = X_{p1}W_{1j} + X_{p2}W_{2j} + \dots + X_{pD}W_{Dj}$$

where taking the derivative with respect to $W_{ij}$ is:

$$\frac{\partial y_{pj}}{\partial W_{ij}} = X_{pi}$$

Plugging that back into our derivative:

$$\frac{\partial L}{\partial W_{ij}} = \sum_p \frac{\partial L}{\partial y_{pj}}X_{pi}$$
We can recognize this as the general formula for each element within an **inner product** of $X^T$ and $\frac{\partial L}{\partial y}$

$$\frac{\partial L}{\partial W} = X^T\frac{\partial L}{\partial y}$$

