# orbit--1 同行 \(W_M\) 碰撞的纯赋值闭合定理

日期：2026-08-10

状态：VALID PURE ALL-ORDER SAME-ROW PAIR THEOREM。结论同时覆盖不同
同行端点和同端点 ramified 弧；不依赖有限域喷射、随机抽样或 Rees
计算证书。本文只闭合 orbit--1 的同行 pair 接口；全局 lower--16
仍须在第 9 节所列入口上重新审计后才能标为 VALID。

## 1. 先前纯约化

使用 n5_orbit1_WM_same_row_maximal_escape_reduction_20260810.md
的第 1--4 节。设 \(\mathcal O=k[[t]]\)、\(K=k((t))\)，且两 Chow
二次空间满足

\[
F_i\subset\operatorname{Sym}^2L_i,\qquad
F_i\cap E_5=0,\qquad q(F_0)=q(F_1)=W,\qquad\dim W=10.
\tag{1.1}
\]

两边特殊纤维都是
\(F_i^*=\operatorname{Sym}^2M\)，其中
\(M=\langle x_{00},x_{01},x_{02},x_{03}\rangle\)；两个特殊五平面
位于同一个外部行，端点可以相同或不同。

若

\[
d=\dim_K(L_0\cap L_1),\qquad s=\dim_K(F_0\cap F_1),
\]

同端点情形可能有 \(d=5\)。此时 \(L_0=L_1\)，而五平面版本的
\(E_5\)-交引理给
\(\dim(E_5\cap\operatorname{Sym}^2L_0)\le1\)，所以直接由共同商像
得到 \(s\ge9\)。以下只需处理 \(0\le d\le4\)。

则

\[
s\le {d+1\choose2},\qquad
\dim\bigl(E_{5,K}\cap(F_0+F_1)\bigr)=10-s.
\tag{1.2}
\]

饱和和空间、行列环面固定点与矩形计数已经纯粹证明：

1. \(d=1,2,3\) 全部不可能；
2. 若 \(d=0\)，则 \(s=0\)，饱和和空间的特殊纤维必须是
   \[
   K_*=\langle x_{0a},x_{1a}:0\le a\le4\rangle,
   \tag{1.3}
   \]
   且饱和关系空间的特殊纤维填满
   \[
   E_{01}:=
   \left\langle x_{0a}x_{1b}+x_{0b}x_{1a}:a<b\right\rangle .
   \tag{1.4}
   \]

同端点时基础格点从六个变成五个，但加入
\(1,2,3,4,5\) 个格点的矩形最大值仍依次为
\[
1,3,6,6,10,
\]
且十维等号型仍唯一为 (1.3)。所以只须排除 (1.3)--(1.4) 的极大
逃逸。

这里把所用矩形计数写成一个不依赖枚举的统一引理。设坐标格点集
\(S\) 含有
\(M=\{00,01,02,03\}\)，令
\(\epsilon\in\{0,1\}\) 记录 \(04\) 是否也在 \(S\) 中，并令
\(n_i\) 是第 \(i>0\) 行的格点数。则

\[
R(S)=\sum_{i>0}{|S_0\cap S_i|\choose2}
     +\sum_{0<i<j}{|S_i\cap S_j|\choose2}
\tag{1.5}
\]

满足

\[
R(S)\le
\sum_{i>0}{\min(n_i,4+\epsilon)\choose2}
+\sum_{0<i<j}{\min(n_i,n_j)\choose2}.
\tag{1.6}
\]

对总新增数
\(q=\epsilon+\sum_{i>0}n_i\le6\)，只需检查 \(q-\epsilon\) 的整数
分拆；(1.6) 依次给出

\[
\begin{array}{c|rrrrrrr}
q&0&1&2&3&4&5&6\\ \hline
\max R&0&0&1&3&6&6&10
\end{array}
\tag{1.7}
\]

最后一个等号必须有
\(\epsilon=1\) 且某个 \(n_i=5\)：若 \(\epsilon=0\)，最危险的分拆
\(3+3\) 在 (1.6) 中也只给九；若 \(\epsilon=1\)，把五格拆到两行
会严格小于 \({5\choose2}\)。端点约束又迫使这个完整外部行就是
第一行。因此不同端点基础的新增数 \(q=2+r\) 给出
\(3,6,6,10\)，同端点基础再加入 \(1,\ldots,5\) 格给出
\(1,3,6,6,10\)，而十维等号型都唯一为 (1.3)。这同时证明了第 4、
第 8 节还会使用的六维和九维上界。

所用环面事实也只是一条标准的射影轨道闭包论证：闭条件
\(\dim(E_5\cap\operatorname{Sym}^2K)\ge h\) 对行列环面不变；其
轨道闭包含坐标固定点。若闭集中只有一个固定点而原点不固定，则所得
正维完备 toric 轨道闭包至少有两个固定点，矛盾。因此十维等号型本身
就是坐标两行块，而不只是拥有该坐标极限。

## 2. 一个零对角交换子引理

令 \(C\) 是五维坐标空间，记 \(C_{\rm off}\subset\operatorname{Sym}^2C\)
为全部对称零对角矩阵。

> **引理 2.1。** 若 \(A\in\operatorname{End}(C)\) 且
> \(BA\) 对每个 \(B\in C_{\rm off}\) 都是对称矩阵，则
> \(A\) 是标量矩阵。特别地，若总有 \(BA\in C_{\rm off}\)，结论
> 当然仍成立。

证明。取 \(B=E_{ij}+E_{ji}\)。对与 \(i,j\) 都不同的 \(k\) 比较
\((i,k)\) 与 \((k,i)\) 元，先得到 \(A\) 的全部非对角元为零；再比较
\((i,j)\) 与 \((j,i)\) 元，得到所有对角元相同。证毕。

还要使用同一计算的反对称版本：

> **引理 2.2。** 若
> \[
> AS+SA^{\mathsf T}=0\qquad(\forall S\in C_{\rm off}),
> \]
> 则 \(A=0\)。

证明。仍取 \(S=E_{ij}+E_{ji}\)。比较 \((i,i)\) 元先杀掉全部非对角
元；此后 \((i,j)\) 元给出任意两个对角元之和为零。因
\(\dim C\ge3\)，全部对角元也为零。证毕。

## 3. 十维 \(E_5\)-交强迫张量积两行块

固定 \(K_*\) 的坐标补空间。以 \(K_*\) 为特殊纤维的饱和十平面格到
\(K_*\otimes\mathcal O\) 的投影在特殊纤维为恒等；Nakayama 引理
说明它在 \(\mathcal O\) 上是同构。因此其泛纤维唯一写成

\[
K=\Gamma(h),\qquad
h:K_*=\langle r_0,r_1\rangle\otimes C
\longrightarrow\langle r_2,r_3,r_4\rangle\otimes C,
\qquad h\equiv0\pmod t.
\tag{3.1}
\]

写

\[
\begin{aligned}
h(r_0\otimes c)&=\sum_{u=2}^4r_u\otimes P_uc,\\
h(r_1\otimes c)&=\sum_{u=2}^4r_u\otimes Q_uc.
\end{aligned}
\tag{3.2}
\]

因为 (1.4) 的饱和关系格有十维并且专门化为整个 \(E_{01}\)，而一个
\(E_5\cap\operatorname{Sym}^2K\) 元投影到 \(K_*^2\) 后只能位于

\[
(r_0\odot r_1)\otimes C_{\rm off},
\]

该投影又因 \(K\) 是图而单射，所以交维恰为十，并且对每个
\(B\in C_{\rm off}\)，

\[
(1+h)^{\odot2}\bigl((r_0\odot r_1)\otimes B\bigr)\in E_5.
\tag{3.3}
\]

比较第零行--第 \(u\) 行块和第一行--第 \(u\) 行块，分别得到

\[
BQ_u^{\mathsf T}\in C_{\rm off},\qquad
BP_u^{\mathsf T}\in C_{\rm off}
\qquad(\forall B\in C_{\rm off}).
\tag{3.4}
\]

引理 2.1 给出 \(P_u=p_uI,Q_u=q_uI\)。置

\[
a=r_0+\sum p_ur_u,\qquad
b=r_1+\sum q_ur_u.
\]

再比较 (3.3) 的外部行平方块，得到 \(a\odot b\) 零对角。因此

\[
\boxed{
K=U\otimes C,\qquad U=\langle a,b\rangle,\qquad
E_5\cap\operatorname{Sym}^2K
=k(a\odot b)\otimes C_{\rm off}.}
\tag{3.5}
\]

这是泛纤维上的全阶恒等式，不是切空间结论。

## 4. 两个 Chow 项的本质空间必须都是五维

若某一项的本质因子空间至多四维，则两个本质空间之和至多九维。其
饱和特殊纤维包含 \(M\)。对任意至多九维且包含 \(M\) 的坐标终端，
至多再加入五个格点；(1.5)--(1.7) 给出最大值六。行列环面
固定点论证于是给

\[
\dim(E_5\cap\operatorname{Sym}^2K)\le6,
\]

与 (1.4) 的十维关系矛盾。因此两边的五个因子在泛纤维均线性无关，
其本质五平面就是 \(L_i\)。

## 5. 两个五平面都横截同一个行因子

按 (3.5) 记

\[
\mathcal A=a\otimes C,\qquad
\mathcal B=b\otimes C,\qquad K=\mathcal A\oplus\mathcal B.
\]

投影 \(F_i\to\operatorname{Sym}^2\mathcal A\) 在特殊纤维
\(F_i^*=\operatorname{Sym}^2M\) 上有秩十，故泛纤维仍有秩十。两边
的像因共同商像且 (3.5) 的核只有交叉行块而相同，记为 \(D\)。

若 \(L_i\to\mathcal A\) 的秩为四，则
\(D=\operatorname{Sym}^2H_i\) 对某个四维超平面 \(H_i\subset C\)。
同一个 \(D\) 强迫 \(H_0=H_1\)，于是
\(L_0+L_1\) 到 \(\mathcal A\) 的像只有四维，与
\(L_0+L_1=K\) 矛盾。若一边秩五、另一边秩四，则 \(D\) 的本质空间
分别为五维和四维，同样不可能相同。

所以两边都横截于 \(\mathcal B\)，可写成

\[
L_i=\Gamma(T_i),\qquad T_i:C\longrightarrow C.
\tag{5.1}
\]

由 \(L_0\cap L_1=0\)，
\(\Delta:=T_0-T_1\) 可逆。

## 6. 两行块中的双提升只有符号型

用共同的 \(\mathcal A^2\) 分量 \(S\in D\) 标号两个 \(F_i\) 中
商像相同的二次式。它们之差落在
\(k(a\odot b)\otimes C_{\rm off}\)，故

\[
S\Delta^{\mathsf T}\in C_{\rm off},\qquad
T_0ST_0^{\mathsf T}=T_1ST_1^{\mathsf T}
\qquad(\forall S\in D).
\tag{6.1}
\]

第一式中的映射 \(S\mapsto S\Delta^{\mathsf T}\) 可逆到其像；定义域
与 \(C_{\rm off}\) 都是十维，所以其像恰为 \(C_{\rm off}\)。令
\(A=\Delta^{-\mathsf T}\)。于是

\[
BA=A^{\mathsf T}B\qquad(\forall B\in C_{\rm off}).
\]

引理 2.1 的同一基矩阵证明给出 \(A\) 为标量，因而

\[
\Delta=\delta I,\qquad D=C_{\rm off}.
\tag{6.2}
\]

置 \(C_0=(T_0+T_1)/2\)。把 (6.2) 代入 (6.1) 的第二式，得到

\[
C_0S+SC_0^{\mathsf T}=0
\qquad(\forall S\in C_{\rm off}).
\]

引理 2.2 给出 \(C_0=0\)。所以

\[
\boxed{
T_0=\frac{\delta}{2}I,\qquad
T_1=-\frac{\delta}{2}I.}
\tag{6.3}
\]

## 7. 符号型没有所需特殊极限

在 (3.5) 中 \(a\equiv r_0,b\equiv r_1\pmod t\)。考察
\(\delta\in K^*\) 的赋值：

1. 若 \(\nu(\delta)>0\)，两个图 (6.3) 都专门化到整条第零行
   \(r_0\otimes C\)；
2. 若 \(\nu(\delta)=0\)，两个特殊图仍互不相交；
3. 若 \(\nu(\delta)<0\)，把图基除以 \(\delta\) 后可见两边都专门化
   到整条第一行 \(r_1\otimes C\)。

三种情形都不可能给出
\(M+\langle x_{10}\rangle\) 与
\(M+\langle x_{11}\rangle\)，也不可能两边同时给出
\(M+\langle x_{10}\rangle\)。所以极大逃逸不存在。

结合第 1 节：

\[
\boxed{
\dim_K(L_0\cap L_1)=4
\quad\text{对所有同行（含同端点）碰撞成立。}}
\tag{7.1}
\]

## 8. 二次空间的大交

令 \(K=L_0+L_1\)，则 \(\dim K=6\)。把其饱和格专门化并重复第 1 节
的环面固定点论证：包含相应特殊同行端点的六平面至多含一个矩形关系，
故

\[
\dim(E_5\cap\operatorname{Sym}^2K)\le1.
\]

式 (1.2) 立刻给出

\[
\boxed{\dim(F_0\cap F_1)\ge9.}
\tag{8.1}
\]

因此任何两个专门化到同一外部行的共同商像 Chow 提升，无论特殊端点
相同或不同，都会单独贡献至少九维总关系核，不可能出现在 lower--16
的 \(k\le2\) 等号态中。

## 9. 证据边界与全局接口

- **已证明、纯数学、全阶：** (3.5)、(6.3)、(7.1)、(8.1)。
- **不再承担逻辑责任：** 同行二阶喷射、两个素数秩表、径向 conormal
  模证书。
- **独立精确诊断：**
  \(\texttt{perm5\_orbit1\_WM\_same\_row\_valuative\_small\_lemmas\_QQ\_exact.py}\)
  在 \(\mathbf Q\) 上得到引理 2.1、2.2 的系数矩阵秩分别为
  \(24,25\)，并穷尽核对 (1.7) 的小矩形极值；脚本与 JSON 的
  SHA--256 分别为
  \(\texttt{EF192A6FEC5F66BCB34FE48416C1C34E5DDC10FD808721736C8FE20DDFA02A5E}\)
  与
  \(\texttt{11B4369CFB2072CE3F7BCE8FF4B3E940DF030DB733983D840061BBAC12F770F6}\)。
  该诊断不承担证明责任。
- **仍须独立复审：** lower--16 等号链是否无循环地给出六个两两不同
  饱和块、共同 \(W_M\) 终端、四个外部端点穷尽、跨行 pair 排除，以及
  总关系核 \(k\le2\)。

只有这些全局入口全部重新通过后，才能把 \(n=5\) 从 PARTIAL/BLOCKED
改为 VALID。
