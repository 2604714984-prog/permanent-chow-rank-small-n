# orbit--0 完整旗标的列刚性：从 4100 顶点降到 41 个行侧顶点

日期：2026-08-10

## 1. 结论

设

\[
U_0=\langle a_{012},a_{013}\rangle\subset A_3,\qquad
R_0=\partial U_0
=\langle a_{01},a_{02},a_{12},a_{03},a_{13}\rangle\subset A_2,
\]

并置

\[
S_0=U_0\otimes B_3,\qquad T_0=R_0\otimes B_2.
\]

考虑闭旗标关联胚

\[
\mathcal F=\{(S,T)\in\operatorname{Gr}(20,D)\times
\operatorname{Gr}(50,E_5):\partial S\subset T\}.
\]

本文给出以下纯特征零结论：

\[
\boxed{
\dim T_{(S_0,T_0)}\mathcal F=8,\qquad
T_C\rtimes\mathfrak S_5\text{ 在该切空间上作用平凡}.}
\tag{1.1}
\]

原来的 4100 顶点整数图只是一种展开方式。利用列子集包含图的连通性，
它可先纯粹压到 41 个行侧顶点，再由八行表手检。

## 2. 图坐标与线性化方程

三子集、二子集都取自 \([5]\)。记

\[
\mathcal U=\{012,013\},\qquad
\mathcal R=\{01,02,12,03,13\},
\]

并令 \(\mathcal U^c,\mathcal R^c\) 分别是十个三子集、二子集中的补集。
Grassmann 图坐标写成

\[
\sigma_{uK}^{vL}
\quad
(u\in\mathcal U,\ v\in\mathcal U^c,\ K,L\in\tbinom{[5]}3)
\]

和

\[
\tau_{rJ}^{sM}
\quad
(r\in\mathcal R,\ s\in\mathcal R^c,\ J,M\in\tbinom{[5]}2).
\]

线性化 \(\partial S\subset T\) 后，每条非零方程至多有两项。若从
\(u\otimes b_K\) 沿格点 \((i,a)\) 求导，并在
\((s,M)\in\mathcal R^c\times\binom{[5]}2\) 的商坐标读取系数，则：

- 当 \(v=s\cup\{i\}\)、\(L=M\cup\{a\}\) 时出现
  \(\sigma_{uK}^{vL}\)；
- 当 \(i\in u\)、\(a\in K\)、\(r=u\setminus\{i\}\)、
  \(J=K\setminus\{a\}\) 时出现 \(-\tau_{rJ}^{sM}\)。

所以一项方程是锚，二项方程只给出“两个系数相等”的边；没有特征或
矩阵秩问题。

## 3. 所有非对角列移动都被直接锚定

先取 \(\sigma_{uK}^{vL}\) 且 \(K\ne L\)。选
\(a\in L\setminus K\)。因 \(v\notin\mathcal U\)，可选 \(i\in v\)
使 \(s=v\setminus\{i\}\in\mathcal R^c\)。在以
\((i,a;s,L\setminus\{a\})\) 标记的方程中出现该 \(\sigma\)，但
\(a\notin K\)，所以没有 \(\tau\) 项；该顶点被直接锚定。

再取 \(\tau_{rJ}^{sM}\) 且 \(J\ne M\)。选
\(a\in M\setminus J\)。由 \(R_0=\partial U_0\)，存在
\(i\notin r\) 使 \(u=r\cup\{i\}\in\mathcal U\)。取
\(K=J\cup\{a\}\)。相应方程含该 \(\tau\)，但 \(a\in M\)，不满足
产生 \(\sigma\) 项所需的 \(a\notin M\)；故该顶点也被直接锚定。

因此任何未锚分量只能含

\[
K=L,\qquad J=M.
\tag{3.1}
\]

这已概念性证明所有存活切方向保持列权。

## 4. 列包含图把每个方向的十份复制粘合

在 (3.1) 下，二项方程沿

\[
J=K\setminus\{a\},\qquad
J\in\binom{[5]}2,\quad K\in\binom{[5]}3
\tag{4.1}
\]

连接三列块和二列块。二部包含图

\[
\binom{[5]}3\ \longleftrightarrow\ \binom{[5]}2
\]

是连通的：任意两个三子集可逐次交换一个元素，相邻两步共享一个
二子集。因此固定一个兼容的行移动后，十个三列复制及十个二列复制
全部属于同一连通分量，且边只要求其系数相等。

于是 4100 顶点图的未锚部分完全由下列 41 个行侧顶点决定：

\[
\sigma_{u}^{v}
\quad(u\in\mathcal U,\ v\in\mathcal U^c),\qquad
\tau_r^s
\quad(r\in\mathcal R,\ s\in\mathcal R^c).
\]

总数为

\[
2\cdot8+5\cdot5=41.
\]

## 5. 41 顶点行图的八个自由分量

对一个行三子集移动 \(u\to v\)，若存在 \(i\in v\setminus u\) 使
\(v\setminus\{i\}\in\mathcal R^c\)，对应方程只有 \(\sigma_u^v\)
一项，故它被锚定。其余情形在共同元素 \(i\in u\cap v\) 上连接

\[
\sigma_u^v\sim
\tau_{u\setminus\{i\}}^{v\setminus\{i\}}.
\tag{5.1}
\]

反向地，若某个 \(\tau_r^s\) 对 \(r\subset u\in\mathcal U\) 的缺失
元素 \(i=u\setminus r\) 满足 \(i\in s\)，则相应方程只有 \(\tau_r^s\)
一项，故它被锚定。把这两个判据代入十个三子集和十个二子集，唯一
不含锚的分量是：

\[
\begin{array}{c|l}
&\text{同一自由分量中的行移动}\\ \hline
1&\sigma_{012}^{014},\ \tau_{02}^{04},\ \tau_{12}^{14}\\
2&\sigma_{012}^{023},\ \tau_{12}^{23}\\
3&\sigma_{012}^{024},\ \sigma_{013}^{034},\
   \tau_{01}^{04},\ \tau_{12}^{24},\ \tau_{13}^{34}\\
4&\sigma_{012}^{123},\ \tau_{02}^{23}\\
5&\sigma_{012}^{124},\ \sigma_{013}^{134},\
   \tau_{01}^{14},\ \tau_{02}^{24},\ \tau_{03}^{34}\\
6&\sigma_{013}^{014},\ \tau_{03}^{04},\ \tau_{13}^{14}\\
7&\sigma_{013}^{023},\ \tau_{13}^{23}\\
8&\sigma_{013}^{123},\ \tau_{03}^{23}.
\end{array}
\tag{5.2}
\]

表外其余 41 个行顶点均由上述单项判据锚定。每个 (5.2) 分量贡献一个
自由参数，所以切空间维数恰为八。

## 6. 列群作用平凡

由第 3 节，未锚分量中的每个图变量都满足列源等于列目标。由第 4 节，
对固定行移动，所有列子集复制又由“系数相等”的边连成一个分量。
因此：

- 列环面在每个自由参数上的权为零；
- 任意列置换只在同一等系数分量内置换复制，故在该一维参数上作用为
  恒等。

这证明 (1.1)，而不需要检查 \(120\) 个置换。

## 7. 从一阶平凡提升到完整形式局部环

令

\[
G=T_C\rtimes\mathfrak S_5.
\]

特征零下 \(G\) 线性约化。设
\(R=\widehat{\mathcal O}_{\mathcal F,(S_0,T_0)}\)，极大理想为
\(\mathfrak m\)。由 (1.1)，\(G\) 在
\(\mathfrak m/\mathfrak m^2\) 上作用平凡。对一组余切基任取提升，再用
完备 Reynolds 算子投影到 \(G\)-不变量，可得同一余切基的
\(G\)-不变提升。这些元素由完备 Nakayama 引理拓扑生成 \(R\)，所以
\(G\) 在整个 \(R\) 上作用平凡。

因此每条专门化到 \((S_0,T_0)\) 的形式弧都落在 \(G\)-不动点胚。
列环面先迫使

\[
S=\bigoplus_{|K|=3}U_K\otimes b_K,\qquad
T=\bigoplus_{|J|=2}R_J\otimes b_J,
\]

而在当前 Grassmann 图表中
\(\dim U_K=2,\dim R_J=5\)。列置换群在两类子集上传递，并且不作用于
行因子，因此所有 \(U_K\) 相同、所有 \(R_J\) 相同：

\[
S=U\otimes B_3,\qquad T=R\otimes B_2.
\tag{7.1}
\]

特殊点处 \(\partial S_0=T_0\) 的一个五十阶子式非零；这个开条件在
形式邻域内保持。结合 \(\partial S\subset T\) 和 \(\dim T=50\)，得到

\[
\boxed{\partial S=T,\qquad R=\partial U.}
\tag{7.2}
\]

这是真正作用于移动旗标的全阶结论，不是固定纤维切空间结论。

## 8. 证据边界

- **纯证明：** 非对角列移动的单项锚、列包含图连通、41 顶点行表、
  列群切表示平凡、线性约化群的完整局部环提升。
- **有限手表：** (5.2) 只有 41 个候选行顶点，可直接按两个锚定判据
  复核。
- **冗余整数诊断：**
  \(\texttt{perm5\_s20\_orbit0\_fullflag\_tangent\_graph\_exact.py}\)
  展开全部 4100 个图变量；它不再是逻辑前提。
- **未在本说明证明：** 后续六个 Chow 块按列分离、符号 Fourier 刚性
  及十项余式 Koszul 下界；这些由独立笔记处理。

故 orbit--0 的完整旗标 mixed--Rees 入口可标为

\[
\boxed{\texttt{VALID / PURE WITH A 41-VERTEX HAND TABLE}.}
\]

