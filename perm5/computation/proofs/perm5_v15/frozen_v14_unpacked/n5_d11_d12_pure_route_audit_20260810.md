# \(\operatorname{perm}_5\) 的 \(d=11,12\) 纯路线反向审计

日期：2026-08-10

## 1. 结论

本说明审计 \(\texttt{perm5\_pure\_route\_20260803.md}\) 第 42、136、
153--157 节之间的依赖接口。结论为：

\[
\boxed{\text{第 8 路的五个 }d=11,12\text{ 状态：
PURE-VALID。}}
\]

更明确地说：

- \(s\in\{21,22\},d=11,t=48\) 的 D11-59-ASYM 两态由
  \(43>6\cdot7=42\) 排除；
- \(s\in\{21,22\},d=11,t=49\) 的 D11-60-TORSION 两态由
  \(49>6\cdot8=48\) 排除；
- \((s,d,t,h)=(22,12,48,60)\) 由
  \(48>6\cdot7=42\) 排除。

这里的“纯”只涉及上述五态。另三条全局延拓路由
\(p_{11}\le55\)、\(p_{12}\le80\)、\(p_{12}\le61\) 依赖前文的有限割表，
需要在整篇依赖审计中单独标为“纯有限表”，不能由本说明自动升级。

## 2. 坐标特殊纤维的完备性

把三子集换成其补边后，三次坐标族成为 Petersen 图 \(P=KG(5,2)\)
的直积 \(P\times P\) 中的顶点集；删去一行一列的影子就是开邻域。
对 \(A\subset V(P)\) 置

\[
h(|A|)=10-|N_P(A)|.
\]

五顶点图的三角形极值给出

\[
h(0),\ldots,h(10)=10,7,5,4,4,2,1,1,0,0,0,
\]

且四元集取 \(h(4)=4\) 当且仅当它是 \(K_5\) 的一颗四边星。
逐纤维分层后，十步递推

\[
F_j(r,m)=
\max_{0\le u\le\min(m,r)}
\bigl(d_jh(u)+F_{j+1}(r-u,u)\bigr)
\]

给出：

1. 二十二元族的影子至少为 \(48\)；等号态只有
   \[
   (10,4,4,4,0,\ldots,0),\qquad
   (4,4,4,4,1,1,1,1,1,1),
   \]
   并由四边星等号恢复得到唯一的行旗标或列旗标 \(S_{22}\)；
2. 二十一元族的影子也至少为 \(48\)；等号态只有四条层序列，逐一补回
   一个不改变邻域的点后成为唯一 \(S_{22}\)，所以原族正是
   \(S_{22}\) 删除一个三次坐标；
3. 若二十一或二十二元族的影子不超过 \(49\)，则影子不可能恰为
   \(49\)。单位亏损分解
   \[
   D_{\rm lay}+D_{\rm fib}=1
   \]
   在稀疏型和稠密型中都迫使最后一个亏损也为零，矛盾。

第三点的关键局部事实只有两个：含四元集的并若仍取 \(h=4\)，则该并
就是同一颗四边星；两颗不同四边星只交一条边。稠密型还只使用
\(L(K_4)\) 删除至多一个顶点后仍连通。因而上述等号恢复不依赖
旧的 \(8700/6778\) 个 shifted-ideal 枚举。

## 3. 零化子余维七引理

固定上述 \(S_{22}\)，或它删除一个坐标后所得的三类 \(S_{21}\)，并令

\[
T_{48}=\partial S_0.
\]

对 \(\dim L\le5\) 定义

\[
W_L=\langle\partial_xs:s\in S_0,\ x\in L^\perp\rangle
\subset T_{48}.
\]

若 \(\delta:S_0\to V\otimes T_{48}\) 是全微分，并置
\(A_\alpha=(1\otimes\alpha)\delta\)，则有规范等式

\[
W_L^\perp=
\{\alpha\in T_{48}^*:A_\alpha(S_0)\subset L\}.
\tag{3.1}
\]

反设余维至少八。记录五平面 \(L\) 与八平面
\(Z\subset W_L^\perp\) 的关联簇是射影、闭且由行列环面保持，故非空时
含环面不动点。\(V\) 与 \(T_{48}^*\) 的有关权互异，所以不动的 \(L,Z\)
都是坐标子空间。

坐标情形只需数父集

\[
\mathcal P(t)=
\{x_{rc}:\partial_{rc}s=t\text{ 对某个 }s\in S_0\}.
\]

写 \(A=\{0,1,2\}\)、\(C=\{0,1,2,3\}\)。对 \(R\in\binom A2\)、
\(a=A\setminus R\)，父集为

\[
\begin{aligned}
\mathcal P(t_{R\mid K})
&=\{x_{ac}:c\notin K\}\\
&\quad\cup
\begin{cases}
\{x_{3c}:c\in C\setminus K\},&K\subset C,\\
\varnothing,&4\in K,
\end{cases}\\
\mathcal P(t_{\{3,a\}\mid K})
&=\{x_{bc}:b\in A\setminus\{a\},\ c\in C\setminus K\}.
\end{aligned}
\tag{3.2}
\]

删去一个三次坐标时，只从它的九个二次子元的父集中删去对应的一个
变量。五个坐标变量按行占用的七种分拆给出下面的完整最大值表：

\[
\begin{array}{c|rrrr}
\text{行占用}&S_{22}&\text{删核心内}&
\text{删核心含 }4&\text{删侧部}\\ \hline
5&4&4&4&4\\
4+1&4&4&4&7\\
3+2&2&2&5&3\\
3+1+1&1&1&2&5\\
2+2+1&1&1&5&2\\
2+1+1+1&0&0&2&2\\
1+1+1+1+1&0&0&0&0.
\end{array}
\tag{3.3}
\]

全表最大值为七，与八维 \(Z\) 矛盾。因此

\[
\boxed{\operatorname{codim}_{T_{48}}W_L\le7.}
\tag{3.4}
\]

本轮从 (3.2) 独立重建了四类父集，并枚举五元坐标集合作抄表诊断；
所得四列全局最大值仍为 \(4,4,5,7\)。这个精确整数重算只验证表格，
不替代环面固定点证明。

## 4. 相对版本没有 mixed--Rees 缺口

令 \(R\) 为 DVR，\(\mathscr S,\mathscr T\) 为自由相对旗标，特殊纤维
属于上述四类，且

\[
\partial\mathscr S\subset\mathscr T,\qquad
\operatorname{rank}\mathscr T=48+e.
\]

若一般纤维存在五平面 \(L_K\) 使

\[
\operatorname{codim}_{\mathscr T_K}W_{L_K}\ge8+e,
\]

则可取同维零化子 \(Z_K\)。相对 Grassmannian 的适当性在有限 DVR
扩张后延拓 \(L_K,Z_K\)；条件
\(A_Z(\mathscr S)\subset L\) 是通用丛映射消失给出的闭条件。特殊化后，
\(\partial S_0=T_{48}\subset\mathscr T_0\)，所以

\[
\operatorname{codim}_{\mathscr T_0}W_{L_0}
\le e+\operatorname{codim}_{T_{48}}W_{L_0}
\le e+7,
\]

矛盾。故

\[
\boxed{\operatorname{codim}_{\mathscr T_K}W_{L_K}\le7+e.}
\tag{4.1}
\]

这里延拓的是实际的 Grassmann 点 \(L,Z\)，不是把一般纤维
\(W_{L_K}\) 的首项强行等同于 \(W_{L_0}\)，所以 moving--\(W\) 的
mixed--Rees 反例不适用。

## 5. D11-59-ASYM：\(43>42\)

在 \(h=59,t=48\) 的唯一剩余非对称情形，

\[
H\simeq
\left(\bigoplus_{i=1}^6F_i\right)/\langle f\rangle,
\qquad f=(f_1,\ldots,f_6)\ne0.
\]

定义

\[
\rho:H\to\bigoplus_{i=1}^6F_i/\langle f_i\rangle.
\]

若 \(I=\{i:f_i\ne0\}\)，则

\[
\dim\ker\rho=|I|-1\le5.
\]

而 \(T=\partial S\) 的维数为 \(48\)，故

\[
\operatorname{rank}(\rho|_T)\ge48-5=43.
\tag{5.1}
\]

第 \(i\) 个 Chow 项的三次导数空间位于
\(\operatorname{Sym}^3L_i\)。相应链映射的第 \(i\) 个二次坐标
\(\rho_i|_T\) 消灭 \(W_{L_i}\)，所以由 (4.1) 的 \(e=0\) 情形，

\[
\operatorname{rank}(\rho_i|_T)\le7.
\]

六坐标合起来却给出

\[
\operatorname{rank}(\rho|_T)\le6\cdot7=42,
\tag{5.2}
\]

与 (5.1) 矛盾。

入口本身也是纯的：六个二次块总维数只可能为 \(59\) 或 \(60\)。
除 (5.1) 所在的“二次和有一条关系、三次和直和”外，其余情形由
Euler 恒等式把二次、三次关系同时压成两个共享纯平方/纯立方的块，
再由固定旗标链映射刚性排除。

## 6. D11-60 与 \(d12\)

在 \(h=60\) 情形，二次、三次六块分别直和。令

\[
T'=\partial S,\qquad \dim T'=48+e.
\]

六个坐标投影 \(P_i:T'\to F_i\) 合成后就是 \(T'\) 在直和坐标中的
嵌入，故合映射秩恰为 \(48+e\)。每个 \(P_i\) 又消灭 \(W_{L_i}\)，
由 (4.1)

\[
48+e\le\sum_i\operatorname{rank}P_i\le6(7+e).
\tag{6.1}
\]

- \(d12\) 的当前状态有 \(e=0\)，于是 \(48\le42\)，矛盾；
- D11-60 若 \(e=0\)，同样矛盾；
- D11-60 唯一可能的导数挠性情形有 \(e=1\)。坐标退化后
  \(\partial S_0\subset\mathscr T_0\)、\(\dim\mathscr T_0=49\)。
  Petersen 单位亏损定理排除影子 \(49\)，而影子下界为 \(48\)，故
  \(\dim\partial S_0=48\)，(4.1) 的入口成立。此时 (6.1) 成为
  \(49\le48\)，仍矛盾。

## 7. 证据分级与剩余工作

- **纯特征零证明：** Petersen 等号恢复、影子不取 \(49\)、环面不动点、
  父集余维七、相对 Grassmannian、六坐标秩差。
- **纯有限手表：** (3.3) 与 Petersen 十步递推的少数阈值行。
- **精确整数诊断：** 父集五元集合重算、Petersen 阈值程序；均不是
  逻辑前提。
- **本说明未审计：** fixed-six 的另外七条路由内部证明，尤其
  \(d=9\) 两个等号态和全局 \(p_{11},p_{12}\) 有限割表。

因此，对八路划分中的第 8 路，可以正式记录：

\[
\boxed{\texttt{VALID / PURE WITH EXPLICIT FINITE HAND TABLES}.}
\]

