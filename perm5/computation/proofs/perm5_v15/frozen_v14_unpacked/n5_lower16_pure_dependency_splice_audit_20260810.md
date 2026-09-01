# \(\operatorname{perm}_5\) lower--16 纯证明依赖拼接审计

日期：2026-08-10

## 1. 当前总裁决

补充：lower--16 不再以前置 lower--15 为入口。基础 Koszul 下界先给
最小项数至少十；保留最小分解中的六个原始项，并以
\(T=\frac12T+\frac12T\) 拆分其余项，即可把任意至多十五项表达式
补成“fixed-six 加九项余式”。因此本审计的 58 态反证直接覆盖
\(r\le15\)，旧 lower--15 的 10GB SAT/DRAT 层不在活跃依赖图中。
完整论证见
\(\texttt{n5\_lower15\_bypass\_padding\_lemma\_20260810.md}\)。

本轮从十五项反设开始，按 fixed-six 的五十八态重新拼接全部活跃路由，
并反向检查最新纯化笔记是否真正替换旧计算根。后续外部复审指出
orbit--1 的 \(p=36\) 坐标终端并非只有正文的 \(W_0\)：还遗漏了
\(W_M=q(\operatorname{Sym}^2M)\)。因此本文件先前的闭合裁决撤回。
在启动本轮反向审计时，临时裁决为

\[
\boxed{
\begin{aligned}
&\texttt{LOWER--16: PARTIAL / FULL REVERSE AUDIT IN PROGRESS},\\
&\texttt{ORBIT--1 }W_M\texttt{ LOCAL SPLICE: PURE VALID.}
\end{aligned}}
\tag{1.1}
\]

式 (1.1) 是审计过程中的 fail-closed 中间状态；完成后的裁决见下式
(1.2)，不得把两者视为同时有效的最终结论。

新的同行赋值定理与两阶段环面拼接已经纯粹排除遗漏的 \(W_M\) 分支；
见
\(\texttt{n5\_lower16\_route4\_orbit1\_WM\_valuative\_splice\_20260810.md}\)。
本轮随后已经完成 route 1--8 的全链反向审计，并补查了 route 4 在
orbit--13 特殊化时可能出现的商秩下降。因此当前裁决更新为

\[
\boxed{
\begin{aligned}
&\texttt{PROGRAM--FREE FINITE--COMBINATORIAL LOWER--16: VALID},\\
&\texttt{CASE-FREE CONCEPTUAL LOWER--16: NOT CLAIMED}.
\end{aligned}}
\tag{1.2}
\]

最后的计算根也已删除。orbit--1 的十五权宇宙现编码为五顶点图：
相对延拓 \(p(W)\) 等于基底三角形、含外点三角形、三个指定四圈与
平方顶点权之和。十类、五十个非零 Möbius 项由两个小局部图直接给出；
若基底图不是 \(K_4\)，统一上界至多三十五；若为 \(K_4\)，八行表给
最大值三十六且等号恰为三个 \(W_b\) 与 \(W_M\)。完整证明见
\(\texttt{n5\_orbit1\_terminal\_pure\_graph\_classification\_20260810.md}\)。

先前已经完成的两个有限手审点仍保留其原有证据等级：

1. 三个 \(d=10\) 终端的一步逆 elementary-compression 见证森林已由
   不导入原生成器的第二实现逐边复核；
2. orbit--13 十四权宇宙中 \(p(W_{10})\le26\) 已展开为覆盖全部
   \(\binom{14}{10}=1001\) 个集合的十行带符号图割表。

冻结的 AMS LaTeX v11 与 PDF 不作修改；只有本轮全局复审完成后才会
生成后继稿。

## 2. 五十八态的无代码宇宙

状态为

\[
(s,d,t,h),\qquad h=t+d,
\]

且

\[
s\in\{19,20,21,22\},\quad d\ge9,\quad
m_s\le t,\quad t+d\le60,
\]

其中

\[
m_{19}=45,\qquad m_{20}=m_{21}=m_{22}=48.
\]

固定 \(s\) 的状态数是

\[
\binom{53-m_s}{2}.
\]

所以总数严格为

\[
\binom82+3\binom52=28+30=58.
\]

八条互斥路由的计数为

\[
38+1+1+9+2+1+1+5=58.
\tag{2.1}
\]

这部分由
\(\texttt{n5\_fixed\_six\_58\_routes\_pure\_arithmetic\_20260810.md}\)
完整证明，不再依赖状态生成脚本。

## 3. 路由 1：三十八个全局预算态

### 3.1 所用纯上界

商延拓函数 \(p(W)\) 满足

\[
p_9\le35,\qquad p_{10}\le50,\qquad
p_d\le50+25(d-10)\quad(d\ge10).
\tag{3.1}
\]

证明结构为：

1. 无 crossing 权集合有精确图公式
   \[
   p(A)=5\sum_i t(G_i)+5\sum_a t(H_a)
   +\sum_{S_{ia}\in A}(d_{G_i}(a)+1)(d_{H_a}(i)+1);
   \]
2. crossing 的边际由四边形、六边关系图和 \(K_{3,3}\) 的最小割控制；
3. 八维总界 \(p_8\le28\) 与单 crossing 边际至多六给
   \(p_9\le35\)；
4. 九维单 crossing 边际至多七给 \(p_{10}\le50\)；
5. 每增加一个商方向，延拓核最多增加 \(\dim V=25\)。

这里包含五顶点图及少量整数最小化表，但不含域上矩阵秩。

### 3.2 路由矛盾

- \(d=9\) 且 \(h-s>35\) 的十七态与 \(p_9\le35\) 矛盾；
- \(s=19,d\ge10\) 的二十一态满足
  \[
  \operatorname{rank}K(R)
  \ge2400+25d-[50+25(d-10)]-(475-45)
  =2170>2160.
  \]

故路由 1 的三十八态为

\[
\boxed{\texttt{VALID / PURE FINITE GRAPH TABLES}.}
\]

本轮重放
\(\texttt{perm5\_p9\_nocrossing\_exact.py}\)、
\(\texttt{perm5\_crossing\_integer\_tables\_exact.py}\)、
\(\texttt{perm5\_p11\_global\_graph\_bound\_exact.py}\) 与
\(\texttt{perm5\_p12\_global\_graph\_bound\_exact.py}\)，均精确 PASS；
这些运行只检查抄表。

## 4. 路由 2：\((19,9,45,54)\)

十九元 Petersen 乘积族的影子至少为 \(45\)。等号恢复给出
\[
\mathcal F(p,\varepsilon;q,\varphi)
=\{\varepsilon\}\times B(\varphi)
\cup(\operatorname{St}(p)\setminus\{\varepsilon\})
\times\operatorname{St}(q)
\]
及其转置，共 \(800\) 个显式旗标，但“800”不是证明输入。

对
\[
\widehat H=E\oplus
\langle x_{0a}x_{0b}:ab\ne34\rangle
\]
的第一次延拓，行列权分类直接给出一百条普通 permanent 线和三十五条
混合线，共 \(135\) 条。任意九平面退化为九条权线。若其中 \(e\) 条
来自 \(E\setminus T\)，普通块数和混合块数分别满足

\[
\begin{array}{c|rrrrrrrrrr}
e&0&1&2&3&4&5&6&7&8&9\\ \hline
\text{普通}&0&0&0&3&3&3&3&4&5&9\\
\text{混合}&25&25&20&20&10&5&5&0&0&0.
\end{array}
\]

每列总数至多 \(25\)。连同十九条恒存线，

\[
\dim(T+X)^{(1)}\le44<54.
\]

因此

\[
\boxed{\texttt{ROUTE 2: VALID / PURE PETERSEN--TRIANGLE COUNT}.}
\]

本轮自包含审计器再次得到
\(800\) 个旗标、\(135\) 条权线、补全上界 \(25\) 和延拓上界 \(44\)。

## 5. 路由 3：\((22,9,48,57)\)

预算给 \(p(W_9)\ge35\)。近极大耦合给 \(H=U\)，六个 Chow 二次块中
至少三个是十维饱和块；每个饱和块 \(F\) 满足

\[
\dim(E_5\cap F)=1,\qquad q(F)=W_9.
\]

分两类：

1. 五个因子独立。交线的秩四矩形结构把环面极限限制到两个十四权
   宇宙；纯最小割表给
   \[
   p(q(F))\le22;
   \]
2. 因子只张成四维。此时 \(F=\operatorname{Sym}^2L\)，矩形退化及
   上半连续性给
   \[
   p(q(F))=20.
   \]

两者都与 \(p(W_9)\ge35\) 矛盾。因此

\[
\boxed{\texttt{ROUTE 3: VALID / PURE FINITE CUT TABLE}.}
\]

这里不需要把一般 \(W_9\) 从“有一个 \(K_5-e\) 坐标极限”错误提升成
字面坐标平面；界 \(22/20\) 直接作用于一般 Chow 块的商像。

## 6. 路由 4：九个 \(d=10\) 状态

九态为

\[
s\in\{20,21,22\},\quad d=10,\quad t\in\{48,49,50\}.
\]

四个饱和且可选四个直和的 Chow 块给出一个坐标二十维子旗标
\((S,L)\)，满足

\[
|S|=20,\qquad |\partial S|\le50,\qquad
|\partial_{L^\perp}S|\le40.
\tag{6.1}
\]

### 6.1 已严格补好的压缩接口

同时 row/column elementary compression 满足强包含

\[
\partial_{(CL)^\perp}(CS)
\subset C(\partial_{L^\perp}S).
\]

此前“纤维初段化可逆”的错误接口已经删除。新的稳定性补丁直接对原
shifted ideal 的大小轮廓证明：

- 总面积二十的 order-reversing 轮廓恰有 \(1405\) 个；
- 轮廓下界 \(B(k)\le50\) 恰有十四个；
- 每个轮廓至多六个兼容一维纤维选择，只有一个的实际影子不超过五十。

故真实 elementary-shift 终点就是十四个 Ferrers 型。再与七种五格
Ferrers 图配对，只剩 orbit--0、1、13。

### 6.2 三个终端

- **orbit--1：PURE TERMINAL CLASSIFICATION AND LOCAL SPLICE VALID。** 十五权
  宇宙中 \(p=36\) 的十元集共有四个：三个是 \(W_0\) 的列置换，
  第四个是 \(W_M=q(\operatorname{Sym}^2M)\)。前三个由既有长度二
  相对 Nakayama 定理排除。对 \(W_M\)，固定旗标的特殊五平面族是
  \(M+\mathbf P\langle x_{10},x_{11},x_{20},x_{21}\rangle\)。
  对四个直和块再作保持 \(E_5,W_M\) 的行列环面退化，四个端点变为
  上述四个坐标方向中的四个（允许重复）；其中必有两个位于同一外部
  行。同行全阶赋值定理给这两个 \(F\)-空间至少九维交，与四块直和
  矛盾。完整无循环拼接见
  \(\texttt{n5\_lower16\_route4\_orbit1\_WM\_valuative\_splice\_20260810.md}\)。
  四个 \(p=36\) 终端的完备性由五顶点闭式、十类 Möbius 项族及
  \(K_4\) 八行表纯粹证明；3003 项 \(\mathbf Q\) 重放只作冗余诊断。
- **orbit--0：VALID。** 完整旗标切图由非对角列锚和列包含图连通性
  从 \(4100\) 顶点降到 \(41\) 个行侧顶点、八个自由分量；列群作用
  平凡遂提升到全形式邻域。六块按列分离后，Boolean Fourier 刚性与
  纯 Koszul 界
  \[
  2215>9\cdot245=2205
  \]
  排除九项余式。
- **orbit--13：VALID。** 五格 \(3+2\) 支撑给十四个不同商权；任意
  十维商像是其中十权子集。十行带符号图割表按 crossing 数和
  无-crossing 核值分组，情形数为
  \(11+165+495+330=1001\)，逐行给 \(p(W)\le26<39\)。

这里还必须处理一个在旧摘要中没有写出的秩下降分支。特殊化时可能有
\(\dim(E_5\cap F^*)=1\)，从而 \(q(F^*)\) 只有九维，不能直接断言
\(q(F^*)=W^*\)。此时低秩交分类给出独立因子型九维 Chow 商像；第
15 节的一维交旗标包络对任意包含它的十平面给
\[
p(W^*)\le26<39,
\]
所以秩下降分支先被排除。剩余分支才有 \(q(F^*)=W^*\)，并合法进入
十四权十子集结构界。orbit--0 与 orbit--1 的终端满足
\(E_5\cap\operatorname{Sym}^2L^*=0\)，故在那里没有同类秩下降。

### 6.3 一步逆压缩的独立复核

一步逆 elementary compression 的人类可读证书已经给出：

- orbit--1 与 orbit--13 共 \(250\) 条可见影子见证边；
- orbit--0 共 \(92\) 条普通影子见证边；
- 四个非统一例外的全影子为 \(54,58,51,53\)。

每条边都可由至多九个父点直接核查。新的独立解析器不导入原生成器，
重新构造父点并核查 \(50\) 个合法方向、\(342\) 条边和 \(5076\) 个
局部布尔赋值；四个例外也精确重现。

新的纯闭式审计器在全部 \(2^{15}=32768\) 个子集上逐项比较五顶点
公式与独立 \(\mathbf Q\)/带符号图引擎，全部相等；其十元子集重放得到
\[
\max p=36,\qquad \#\{W:p(W)=36\}=4,
\]
即三个 \(W_0\) 列置换和一个 \(W_M\)。结合上述三个终端及秩下降
分支，得到

\[
\boxed{\texttt{ROUTE 4: VALID / PURE GRAPH TERMINAL CLASSIFICATION
+ PURE LOCAL EXCLUSIONS}.}
\]

## 7. 路由 5--7：全局 \(p_{11},p_{12}\) 表

### 路由 5

两个 \(s=20,d=11\) 状态要求 \(p(W_{11})\ge63\)，而纯图表给

\[
p_{11}\le55.
\]

### 路由 6

\((20,12,48,60)\) 要求 \(p(W_{12})\ge88\)。由

\[
p_{12}\le p_{11}+25\le80
\]

矛盾。

### 路由 7

\((21,12,48,60)\) 要求 \(p(W_{12})\ge63\)，而 crossing 分类给更强的

\[
p_{12}\le61.
\]

本轮还反向检查了最新版正文的统一证明：无 crossing 部分由同时压缩、
Kruskal--Katona 三角形包络和三个显式 Ferrers 例外闭合；crossing
部分由四角、六边 repeat 与 \(K_{3,3}\) 割的密度不等式闭合。旧的
按 square 数硬编码表不再是逻辑前提。两个审计器只重放整数算术，均
PASS。因此

\[
\boxed{\texttt{ROUTES 5--7: VALID / PURE GRAPH INEQUALITIES
+ FINITE INTEGER AUDIT}.}
\]

## 8. 路由 8：五个旗标零化子态

该路由已经由
\(\texttt{n5\_d11\_d12\_pure\_route\_audit\_20260810.md}\)
独立审计。核心是

\[
\operatorname{codim}_{T_{48}}W_L\le7
\]

及其相对版本

\[
\operatorname{codim}_{\mathscr T_K}W_{L_K}\le7+e.
\]

Petersen 等号恢复保证特殊纤维只有 \(S_{22}\) 或其三类单删
\(S_{21}\)，并纯排除影子四十九。六个坐标投影给出：

\[
43>42,\qquad49>48,\qquad48>42.
\]

故

\[
\boxed{\texttt{ROUTE 8: VALID / PURE WITH EXPLICIT PARENT-SET TABLE}.}
\]

## 9. 最终内部裁决与论文义务

当前活跃链已经排除全部五十八态，并且 lower--15 的历史 10GB
SAT/DRAT 层不再参与。严格区分如下：

1. **已证明：** 特征零几何、图论、赋值、相对 Grassmannian、
   Fourier/Koszul 论证，以及 orbit--1 五顶点终端闭式；
2. **精确计算证书：** 五阶 lower--16 的活跃依赖中没有程序证书；
3. **冗余诊断：** 本轮重放的有限整数、QQ 与模素数脚本；其中 3003
   项终端扫描与旧模
   素数资产已不承担 route 4、orbit--13 或 orbit--0 的结论；
4. **尚未完成：** 对 AMS LaTeX v13 作独立外部复审；纯闭式、同行
   赋值定理、\(W_M\) 拼接、秩下降分支及新证据分级已并入 v13。

因此数学层面的内部结论是
\[
\boxed{
\operatorname{ChowRank}(\operatorname{perm}_5)=16
\quad\texttt{VALID BY A PROGRAM--FREE FINITE--COMBINATORIAL PROOF}.}
\]
这里没有把“程序不进入逻辑前提”偷换为“无有限分类”：正文仍有十类
Möbius 项和八行 \(K_4\) 表。冻结的 v11、v12 PDF 与 reviewer ZIP
均未覆盖；v13 在独立外审前仍标记 EXTERNAL REVIEW PENDING。
