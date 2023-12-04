# Determine the Angle of Attack Separation Point

from the function written by origin writer, the determination of the separation code is as below:

```python
def locate_sep_buffet(AoAs, CLs, mUys, dAoA, index_dAoA: int):
    '''
    >>> AoA_sep, AoA_buffet = locate_sep_buffet(AoAs, CLs, mUys, index_dAoA: int)
    '''
    f_mUy, mUy_low, mUy_upp = interplot(np.array(AoAs), np.array(mUys), kind=1)
    f_CL,  CL_low,  CL_upp  = interplot(np.array(AoAs), np.array(CLs),  kind=0)

    _dAoA = dAoA[index_dAoA]

    AoA_sep = 0.0
    mUy = 1.0
    aa  = np.arange(mUy_low, mUy_upp, _dAoA)
    for i in range(aa.shape[0]):
        mUy_= mUy
        mUy = f_mUy(aa[i])
        if mUy<=0.0 and mUy_>0.0:
            AoA_sep = aa[i]
            break
    AoA_sep = int(AoA_sep/_dAoA)*_dAoA
    AoA_sep = float('%.3f'%(AoA_sep))

    AoA_buffet = 0.0
    dCL0 = (CLs[2]-CLs[0])/(AoAs[2]-AoAs[0]) - 0.1
    aa   = np.arange(AoAs[2], CL_upp, _dAoA)
    dCLs = []
    for i in range(aa.shape[0]-1):
        dCLs.append((f_CL(aa[i+1])-f_CL(aa[i]))/_dAoA)

    ii = np.argmin(np.abs(np.array(dCLs)-dCL0))
    AoA_buffet = int(aa[ii]/_dAoA)*_dAoA
    AoA_buffet = float('%.3f'%(AoA_buffet))
    AoA_buffet = max(AoA_buffet, AoA_sep)

    return AoA_sep, AoA_buffet
```

Let's consider $C_L=C_L(\alpha)$, and $u_y=\frac{\partial u}{\partial y}=u_y(\alpha)$. Here are 2 critical $\alpha$: $\alpha_{sep},\alpha_{buffet}$.

The $\alpha_{sep}$ is the separation point, which is defined as the $\alpha$ when $u_y=0$.

```python
    for i in range(aa.shape[0]):
        mUy_= mUy
        mUy = f_mUy(aa[i])
        if mUy<=0.0 and mUy_>0.0:
            AoA_sep = aa[i]
            break
```

$$
\begin{equation}
  \begin{aligned}
    u_y(\alpha_{sep})=0
  \end{aligned}
\end{equation}
$$

And $\alpha_{buffet}$ is the $\alpha$ when $\frac{\partial C_L}{\partial \alpha}=C_{l\alpha}(\alpha)=C_{l0}-0.1$ where $C_{l0}$ is $\lim_{\alpha\to 0}C_{l\alpha}(\alpha)$：

$$
\begin{equation}
  \begin{aligned}
    C_{l\alpha}(\alpha_{buffet})=C_{l0}-0.1
  \end{aligned}
\end{equation}
$$

```python
    AoA_buffet = 0.0
    dCL0 = (CLs[2]-CLs[0])/(AoAs[2]-AoAs[0]) - 0.1
    aa   = np.arange(AoAs[2], CL_upp, _dAoA)
    dCLs = []
    for i in range(aa.shape[0]-1):
        dCLs.append((f_CL(aa[i+1])-f_CL(aa[i]))/_dAoA)

    ii = np.argmin(np.abs(np.array(dCLs)-dCL0))
    AoA_buffet = int(aa[ii]/_dAoA)*_dAoA
```

Finally, let $\alpha_{buffet} = \max(\alpha_{buffet},\alpha_{sep})$.

```python
    AoA_buffet = max(AoA_buffet, AoA_sep)
```