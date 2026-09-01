# `perm_5` crossing 边际的闭式密度界

日期：2026-08-10

## 1. 结论

固定一个 crossing 权 \(x=X_{01;01}\)，并设已有 \(N\) 个坐标商方向。
加入 \(x\) 后相对延拓核的增量记为 \(\Delta_xp\)。旧证明把
\(N=0,\ldots,11\) 的十二个上界逐项写成

\[
0,1,2,3,4,4,5,6,6,7,8,9.
\]

本笔记把该表替换为闭式定理

\[
\boxed{
\Delta_xp\le
\begin{cases}
N,&0\le N\le4,\\
\lceil3N/4\rceil,&5\le N\le11.
\end{cases}}                                                   \tag{1.1}
\]

证明只使用四边形、六边关系图和 \(K_{3,3}\) 的最小割结构。旧十二项
表不再是活跃证明依赖。

## 2. 非角块的割代价

先固定局部图的定义。对一个三次行列环面权，以该权的三次单项式为
顶点；对每个变量与二次商权 \(q\)，偏导条件给出一个系数行。两项行
画成带符号的 \(q\)-标号边，一项行把相应顶点锚定到零。选择
\(q\) 等价于删除全部 \(q\)-标号关系。在下面的四边形、六边图和
\(K_{3,3}\) 中，符号经顶点换号后相容，因此相对核就是未锚连通
分量数，新增 crossing 的边际就是删边后新产生的未锚分量数。

免费加入 crossing 矩形的四条边界边后，十二个重复块分成六个组，
九个 matching 块由一个 \(3\times3\) 格标记。每个重复组有两条
side crossing；两个六边块还分别有一对互不相交的 external 标签。
六边图的 \(x\)-割说明：每激活一块，至少选一条属于该块的 external
edge，且该组必须 side-positive；每组至多承载两块。

matching 格的六个顶点是三行三列上的六个完美匹配，奇偶二分后的
关系图为 \(K_{3,3}\)，九条边以九个 \(2\times2\) 矩形标号。删去
\(x\) 后，四条 side 标签分属横、纵两组，另四条 diagonal 标签为
该格独有。列出六个置换即可检查：

1. 横、纵组都 double-side 时，diagonal 代价可为零；
2. 两组都 side-positive 时，除前一种情形外至少需一条 diagonal；
3. 其余情形至少需两条 diagonal。

不同格的 diagonal 标签互不相交，所以代价逐格相加。令

\[
u=h_2+h_1,\qquad v=v_2+v_1,qquad
\alpha=h_2,\qquad\gamma=v_2,
\]

其中 \(0\le\alpha\le u\le3\)、\(0\le\gamma\le v\le3\)；下标 2、1
表示相应组选择了两个或一个 side crossing。再置

\[
P=u+v,\qquad A=P+\alpha+\gamma,\qquad
z=\alpha\gamma,qquad o=uv.                                  \tag{2.1}
\]

若激活 \(r\) 个重复块和 \(m\) 个 matching 块，则六边图割给

\[
r\le2P,                                                       \tag{2.2}
\]

而每个格的 \(K_{3,3}\) 割给 diagonal 总代价

\[
D(m;z,o)=
\begin{cases}
0,&m\le z,\\
m-z,&z<m\le o,\\
2m-o-z,&m>o.
\end{cases}                                                   \tag{2.3}
\]

三类方向互不相交，所以所需非角辅助方向数 \(q\) 满足

\[
q\ge Q:=r+A+D(m;z,o).                                        \tag{2.4}
\]

这些式子正是上述 inclusion-minimal cuts 的整数汇总。

## 3. 密度引理

### 引理 3.1

若 \(Q\le11\)，则

\[
4(r+m)\le3Q.                                                   \tag{3.1}
\]

#### 证明

先记两个初等事实。

1. 若 \(z>0\)，则 \(1\le\alpha,\gamma\le3\)，并且
   \[
   z+3\le2(\alpha+\gamma)\le A.                              \tag{3.2}
   \]
   第一不等式只需按 \(\alpha=1,2,3\) 写成
   \(\gamma-1\ge0\)、\(1\ge0\)、\(3-\gamma\ge0\)。
2. 若 \(A\le9\)，则
   \[
   o+3z\le P+3\alpha+3\gamma+2,                              \tag{3.3}
   \]
   唯一例外是 \((u,v,\alpha,\gamma)=(3,3,0,0)\)。
   事实上令 \(w=\alpha+\gamma\)。由 \(A\ge2w\) 得 \(w\le4\)。
   当 \(w=0\) 时，(3.3) 等价于 \(uv\le u+v+2\)，仅 \(u=v=3\)
   失败。当 \(1\le w\le3\) 时，
   \(uv-u-v\le3\) 且
   \(\alpha\gamma-\alpha-\gamma\le-1\)。当 \(w=4\) 时
   \(u+v\le5\)，故前者至多一，后者至多零。

现在按 (2.3) 的三个区间证明。

**第一段 \(m\le z\)。** 若 \(m=0\)，则
\(r\le2P\le2A<3A\)，立即得到
\(4r\le3(r+A)=3Q\)。若 \(m>0\)，由 \(Q\le11\)、(3.2) 得

\[
r+4m\le11-A+4z\le3A-1.
\]

于是 \(4(r+m)=3r+(r+4m)<3(r+A)=3Q\)。

**第二段 \(z<m\le o\)。** 此时 \(D=m-z\)，所求等价于

\[
r+m+3z\le3A.                                                  \tag{3.4}
\]

若 \(z>0\)，则

\[
r+m+3z\le11-A+4z\le3A-1.
\]

若 \(z=0,A\ge3\)，左端至多 \(11-A\le8<3A\)。若
\(z=0,A\le2\)，由 \(m>0,m\le uv\) 得 \(u=v=1,A=2\)；故
\(r\le4,m\le1\)，仍有 \(r+m<3A\)。

**第三段 \(m>o\)。** 此时 \(D=2m-o-z\)，且 \(m\ge o+1\)。若
\(A\ge10\)，因 \(o\ge z\)，有
\(D\ge o+2-z\ge2\)，与 \(Q\le11\) 矛盾。故 \(A\le9\)。排除
(3.3) 的唯一例外后，

\[
\begin{aligned}
r+3o+3z
&\le2P+3o+3z\\
&\le3P+2o+3\alpha+3\gamma+2\\
&=3A+2o+2\le3A+2m.
\end{aligned}
\]

这正等价于 (3.1)。在例外
\((u,v,\alpha,\gamma)=(3,3,0,0)\) 中 \(o=9\)，而总共只有九个
matching 块，所以 \(m>o\) 不可能。证毕。

因此若 \(F(q)\) 表示 \(q\) 个非角方向可激活的非角块最大数，则

\[
F(q)\le\lfloor3q/4\rfloor,\qquad0\le q\le11.                \tag{3.5}
\]

### 引理 3.2

在 \(q=4\) 时还有严格加强

\[
F(4)\le2.                                                      \tag{3.6}
\]

#### 证明

反设 \(Q\le4\) 且 \(r+m\ge3\)，仍按三段处理。

- 若 \(m\le z\)：当 \(m=0\) 时，\(r\ge3\) 与
  \(r\le2P\) 给 \(Q=r+A\ge3+2=5\)；当 \(m>0\) 时
  \(A\ge4\)，预算迫使 \(A=4,r=0\)，而这时
  \(u=v=\alpha=\gamma=1,m\le z=1\)。
- 若 \(z<m\le o\)：\(z>0\) 时 \(A\ge4,D\ge1\)；\(z=0\) 时
  \(A\ge2,D=m\)，故 \(r+m\le2\)。
- 若 \(m>o\)：总有 \(D\ge2\)。若 \(r>0\)，则 \(A\ge1\)，预算只
  可能留下 \(A=r=1,D=2\)，这强迫 \(o=z=0,m=1\)。若
  \(r=0,m\ge3\)，则 \(o\ge2\) 时 \(A\ge3,D\ge2\)；\(o=0\) 时
  \(D=2m\ge6\)；\(o=1\) 时 \(A\ge2,D\ge2m-2\ge4\)。
  均与 \(Q\le4\) 矛盾。

故 (3.6) 成立。

## 4. 从非角密度到完整边际

设已有 \(N\) 个方向中，\(s\) 个是 crossing 矩形的角 square，\(b\)
个是四条边界边，剩下 \(q=N-s-b\) 个为非角方向。若边界中有 \(i\)
条水平边、\(j\) 条竖直边，则它们额外激活至多 \(ij\) 个角。因此

\[
g(b)=\max_{i+j=b,\ 0\le i,j\le2}ij
=\lfloor b^2/4\rfloor=(0,0,1,2,4)_b,                        \tag{4.1}
\]

且角块数 \(c\) 满足

\[
c\le\min\{4,s+g(b)\}.                                      \tag{4.2}
\]

若 \(N\le4\)，由 \(g(b)\le b\)、\(c\le s+b\) 及 \(F(q)\le q\)，
立即得 \(c+F(q)\le N\)。

以下设 \(5\le N\le11\)，并令 \(a=s+b\)。由 (4.1)--(4.2) 逐个
\(b=0,1,2,3,4\) 比较可得

\[
c\le\lceil3a/4\rceil,                                      \tag{4.3}
\]

具体地，\(b=0\) 时只有 \(s=4\) 例外；\(b=1\) 时直接用
\(c\le s\)；\(b=2\) 时分 \(s\le2\) 与 \(s\ge3\)；\(b=3\) 时分
\(s=0,1\) 与 \(s\ge2\)；\(b=4\) 时只有 \(s=0\) 例外。因此唯一
例外是 \((s,b)=(4,0),(0,4)\)，此时 \(a=c=4\)。在非例外情形，

\[
c+F(q)\le
\lceil3a/4\rceil+\lfloor3q/4\rfloor
\le\lceil3N/4\rceil.                                       \tag{4.4}
\]

在两个例外情形，\(q=N-4\in\{1,\ldots,7\}\)。若 \(q\ne4\)，
\(\lfloor3q/4\rfloor=\lceil3q/4\rceil-1\)；若 \(q=4\)，使用
(3.6)。两者统一给

\[
F(q)\le\lceil3q/4\rceil-1,
\]

所以 \(4+F(q)\le\lceil3N/4\rceil\)。这就证明闭式界 (1.1)。

## 5. 精确诊断

运行

```text
python perm5_crossing_marginal_density_audit.py
```

必须输出

```text
PASS_EXACT_INTEGER_CROSSING_MARGINAL_DENSITY_AUDIT
cut_cost_regimes = 3
exact_noncorner_F_0_through_11 = 0,0,1,2,2,3,4,5,5,6,7,8
exact_marginal_0_through_11 = 0,1,2,3,4,4,5,6,6,7,8,9
active_12_value_marginal_table_required = false
```

程序用整数遍历三段割代价参数，只用于寻找反例和核对旧值；正文证明
使用 (3.1)、(3.6)、(4.4)，不使用这十二个逐项输出。
