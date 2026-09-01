# `perm_5` 无 crossing 层的压缩与闭式极值证明

## 1. 结论与证据等级

本文给出一个不依赖 square 轨道枚举表的组合证明，证明无 crossing
坐标权集合满足

\[
B_9\le 35,\qquad B_{10}\le 50,\qquad
B_{11}\le 55,\qquad B_{12}\le 60.
\]

而且 (B_9=35) 的等号集合恰为一个固定 row 或 column 中的
(K_5-e)；未压缩坐标中共有

\[
5\binom52+5\binom52=100
\]

个等号集合。

证据等级如下。

- 下述压缩引理、关联上界和终端分类是手写特征零组合证明；
- `perm5_nocrossing_compression_diagnostic.py` 只作独立精确整数反例筛查；
- 该脚本的 (2206,4057,7247,12612) 个 shifted 状态枚举不是证明依赖；
- 本证明尚未经过独立外审，不能据此把整篇 `perm_5` lower--16 链提升为
  外部 VALID。

## 2. 无 crossing 图公式

选中的无 crossing 权写成三部分：

- square 集 (A\subset [5]\times[5])；
- 对每一行 (i)，列顶点上的简单图 (G_i)；
- 对每一列 (a)，行顶点上的简单图 (H_a)。

记 (t(G)) 为三角形数，(d_G(v)) 为顶点度数。局部系数图直接给出

\[
p(A,G,H)=5\sum_i t(G_i)+5\sum_a t(H_a)
+\sum_{(i,a)\in A}(d_{G_i}(a)+1)(d_{H_a}(i)+1). \tag{1}
\]

最后一项展开为四类非负模式计数：

\[
|A|+P_R+P_C+P_{RC}, \tag{2}
\]

分别是 square、square--row-edge 关联、square--column-edge 关联和带横纵
两臂的 corner。

## 3. 二点压缩不降低 (p)

固定两个行标号 (u<v)。对所有权同时作标准 ((u,v))-压缩：

- square 的行切片作 singleton 压缩；
- (G_u,G_v) 变成 (G_u\cup G_v,G_u\cap G_v)；
- 每个 (H_a) 在顶点 (u,v) 上作图压缩。

### 3.1 两个基本不等式

对 (x,y,a,b\in\{0,1\})，有二点重排不等式

\[
(x\vee y)(a\vee b)+(x\wedge y)(a\wedge b)\ge xa+yb. \tag{3}
\]

若 (X) 是顶点集，(K) 是简单图，置

\[
I(X,K)=\sum_{v\in X}d_K(v).
\]

同时压缩 (X,K) 不降低 (I)。事实上，对每个
(k\notin\{u,v\})，令

\[
x=1_{u\in X},\quad y=1_{v\in X},\quad
a=1_{uk\in K},\quad b=1_{vk\in K},\quad z=1_{k\in X}.
\]

压缩前后这对边对关联数的贡献分别为

\[
ax+by+z(a+b)
\]

和

\[
(a\vee b)(x\vee y)+(a\wedge b)(x\wedge y)+z(a+b).
\]

式 (3) 给出单调性；边 (uv) 的贡献不变。

### 3.2 六类模式逐项单调

1. square 数保持不变。
2. 对固定 (a,b)，square--row-edge 关联在两行上的变化正是式 (3)。
3. 对固定列 (a)，square--column-edge 关联是
   (I(A^a,H_a))，由上一小节不减。
4. 对固定 (a\ne b)，令
   \[
   X_{a,b}=\{i:(i,a)\in A,\ ab\in G_i\}.
   \]
   若 (X'_{a,b}) 是压缩后的中心集，则在 (u,v) 两点上
   \[
   1_{u\in X'}\ge 1_{u\in C_{uv}X},\qquad
   1_{v\in X'}=1_{v\in C_{uv}X}.
   \]
   因而 (X'_{a,b}\supseteq C_{uv}X_{a,b})。corner 数是
   (I(X_{a,b},H_a))，所以也不减。
5. 三角形指标 (1_{\Delta\subset K}) 对边集是超模函数，故
   \[
   t(K\cup L)+t(K\cap L)\ge t(K)+t(L).
   \]
   这处理 (G_u,G_v)。
6. 标准图压缩不减少 clique 数，特别不减少三角形数。一个直接注入是：
   把含 (v) 不含 (u) 的三角形压到 (u)；若目标三角形原已存在，
   原三角形的两条 (v)-边不会被删除，于是保留原三角形。

由 (1)--(2)，行压缩不降低 (p)。列压缩完全对称。

### 3.3 fully shifted 正规形

先压完行标号，再压完列标号。列压缩保持已经得到的行嵌套关系，因为
图压缩对集合包含单调，且 shifted 图的并、交仍为 shifted 图。最终可设：

\[
G_0\supseteq G_1\supseteq\cdots\supseteq G_4,
\qquad
H_0\supseteq H_1\supseteq\cdots\supseteq H_4, \tag{4}
\]

每个 (G_i,H_a) 都是 shifted 图，而 (A) 是 (5\times5) Ferrers
ideal。该正规化保持集合大小并且只会增大 (p)。

## 4. 三角形包络

若五个简单图共含 (e\le12) 条边，则其三角形总数至多

\[
\tau(e)=(0,0,0,1,1,2,4,4,5,7,10,10,10)_e. \tag{5}
\]

证明使用图的 Kruskal--Katona 定理。对单图，把

\[
e=\binom{k}{2}+\ell,\qquad 0\le\ell<k,
\]

则三角形数至多

\[
\binom{k}{3}+\binom{\ell}{2}. \tag{6}
\]

对 (e\le10)，式 (6) 的包络在合并两个边预算时不减，因此边集中到
一个五顶点图给出 (5)。对 (e=11,12)，一个 (K_5) 加一或两条落在
其他层的边给出 10；若没有 (K_5)，最大候选分别至多
(7+0) 和 (7+1)，故仍不超过 10。

还要记录两个等号事实：

- (	au(6)=4) 的唯一形状是一层 (K_4)；
- (	au(9)=7) 的唯一形状是一层 (K_5-e)；
- (	au(10)=10) 的唯一形状是一层 (K_5)。

它们同样直接来自式 (6) 的等号情形。

## 5. 统一 square 关联上界

置

\[
s=|A|,\qquad r=\sum_i|E(G_i)|,\qquad
c=\sum_a|E(H_a)|.
\]

并记

\[
R=\sum_{(i,a)\in A}d_{G_i}(a),\quad
C=\sum_{(i,a)\in A}d_{H_a}(i),\quad
L=\sum_{(i,a)\in A}d_{G_i}(a)d_{H_a}(i).
\]

每条 row edge 最多碰到两个 square，且每个 square 的 row 度至多四，
所以

\[
R\le \min(4s,2r),\qquad C\le\min(4s,2c). \tag{7}
\]

(L) 计数一个 square、一个相邻 row edge 和一个相邻 column edge 的
三元组。固定一对 row/column edge，它们至多有一个共同中心 cell，故

\[
L\le rc.
\]

又因每个度数至多四，(L\le4R,4C)。因此 square 项 (Q) 满足

\[
Q\le U_s(r,c):=
s+R_0+C_0+\min\{rc,4R_0,4C_0\}, \tag{8}
\]

其中

\[
R_0=\min(4s,2r),\qquad C_0=\min(4s,2c).
\]

结合 (5)，得到统一上界

\[
p\le 5\bigl(\tau(r)+\tau(c)\bigr)+U_s(r,c),
\qquad s+r+c=d. \tag{9}
\]

## 6. 终端极值：只剩十种粗界例外

把 (d=9,10,11,12) 和式 (5) 代入 (9)。按 (r,c) 转置只计一次，
粗界超过目标值的情形恰为：

| (d) | 目标 | 粗界例外 ((s;r,c)) |
|---:|---:|:---|
| 9 | 35 | ((1;2,6),(1;3,5),(2;1,6),(2;3,4)) |
| 10 | 50 | 无 |
| 11 | 55 | ((2;3,6)) |
| 12 | 60 | ((1;1,10),(2;3,7),(2;4,6),(2;5,5),(3;3,6)) |

该表不是轨道枚举：它只是把 (r+c=d-s) 代入一个显式三变量不等式；
每行至多检查 (d+1) 个整数。

### 6.1 一个 square

若 (s=1)，其 row/column 度分别至多 (min(4,r),\min(4,c))，故

\[
Q\le(\min(4,r)+1)(\min(4,c)+1). \tag{10}
\]

对三个例外 ((d;r,c)=(9;2,6),(9;3,5),(12;1,10))，
式 (5) 与 (10) 分别给出

\[
20+15=35,\qquad15+20=35,
\qquad50+10=60. \tag{11}
\]

为了得到九维等号分类，还需排除 (11) 前两项的虚假等号。

- ((r,c)=(2,6))：若三角形总数为四，六边一侧必须是 (K_4)，
  标记顶点度为三，另一侧度至多二，所以 (Q\le12)，从而 (p\le32)；
  若三角形总数至多三，则 (p\le15+15=30)。
- ((r,c)=(3,5))：若三角形总数为三，三边一侧是 (K_3)，五边一侧
  是 (K_4-e)，两个标记度至多二、三，所以 (Q\le12)，从而
  (p\le27)；若三角形总数至多二，则 (p\le10+20=30)。
- ((r,c)=(4,4)) 虽不是粗界例外，却是式 (10) 的最后一个等号候选。
  若两侧各有一个三角形，两个标记度都至多三，故 (p\le10+16=26)；
  否则 (p\le5+25=30)。

所以 (d=9,s=1) 时实际有 (p\le32)。

### 6.2 两个 square

fully shifted 的两格 Ferrers ideal 在转置后是 row domino
({(0,0),(0,1)})。写两格的 row 度为 (g_0,g_1)，column 度为
(h_0,h_1)。只有 row 图中的边 (01) 能被 (g_0+g_1) 重复计数，
而 (h_0,h_1) 来自两个 column 图层。因此

\[
G:=g_0+g_1\le\min\{8,r+1_{r>0}\},\qquad
H:=h_0+h_1\le\min\{8,c\}. \tag{12}
\]

并且

\[
g_0h_0+g_1h_1\le\min\{rc,4G,4H\}.
\]

故

\[
Q\le2+G+H+\min\{rc,4G,4H\}. \tag{13}
\]

对上表所有 (s=2) 情形及其两个方向，式 (13) 均直接低于目标，
唯一剩余的数值候选是 (d=9) 的 row-domino 方向
((r,c)=(1,6))，其粗值为 36。此时唯一 row edge 是 (01)。若
六边一侧有四个三角形，它是一层 (K_4)，于是

\[
(g_0,g_1)=(1,1),\qquad(h_0,h_1)=(3,0),\qquad Q=10,
\]

故 (p=30)。否则三角形至多三，而 (13) 给 (Q\le16)，故
(p\le31)。因此九维 (s=2) 也严格小于 35。

### 6.3 三个 square

三格 Ferrers ideal 在转置后只有两种形状：row triple 和 L 形。

- row triple：三个 row 度同属一个图。三点内部至多三条边会被重复计数，
  所以
  \[
  R\le\min\{12,r+\min(r,3)\},\qquad C\le\min\{12,c\}.
  \]
- L 形：每一侧只有一条内部边可能被重复计数，所以
  \[
  R\le\min\{12,r+1_{r>0}\},\qquad
  C\le\min\{12,c+1_{c>0}\}.
  \]

两种情形仍有 (L\le rc)。对 (d=12) 唯一粗界例外
((r,c)=(3,6)) 及其转置，row triple 给

\[
Q\le3+6+6+18=33,
\]

L 形给 (Q\le3+4+7+18=32)。又
(	au(3)+\tau(6)=5)，所以分别得到 (p\le58,57)。

在 (d=9,s=3,r+c=6) 时，同样代入两种形状，最大值为 32。

### 6.4 (s\ge4) 与九维等号

对 (d=9,s\ge4)，直接用 (8)--(9) 得 (p<35)。上面已经证明
(s=1,2,3) 也严格小于 35。因此等号只能发生在 (s=0)。此时

\[
p=5T\le5\tau(9)=35.
\]

由 (	au(9)) 的等号情形，九条边必须全部位于一个 row/column 图，
并组成 (K_5-e)。这证明 100 个等号集合的分类。

## 7. 最终状态

本结构证明把旧的以下活跃依赖全部降为诊断：

- 七种 (s\le3) square 轨道表；
- (d=10,11,12) 的按 square 数有限最大值表；
- 四-square 的十个同构型枚举。

当前可严格声称：

```text
NO_CROSSING_COMPRESSION_LEMMA = PROVED_IN_HANDWRITTEN_COMBINATORICS
NO_CROSSING_B9_B10_B11_B12   = 35,50,55,60
NO_CROSSING_B9_EQUALITY       = 100 PURE K5-MINUS-EDGE LINES
OLD_SQUARE_ORBIT_TABLES       = DIAGNOSTIC_ONLY
EXTERNAL_REVIEW               = PENDING
```

