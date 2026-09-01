# v12 结构化候选自审：`perm_5` 多层有限依赖删除

日期：2026-08-10

## 当前裁决

```text
n=3: VALID
n=4: VALID / exact rational certificate independently replayed
n=5 computation-assisted: INTERNAL VALID / route1--8 reverse audit completed
n=5 case-free pure: PARTIAL / orbit-1 fifteen-weight terminal completeness still uses an exact QQ finite certificate
orbit13: VALID / pure structural bound p<=36<39
orbit0 inverse shift: VALID / pure Petersen and slice proof
orbit1/13 inverse shift: INTERNAL VALID / Petersen fibre-profile proof
active 42-direction table: 0
active 14-state visible table: 0
active 12-value crossing marginal table: 0
active witness edges: 0
publication-ready: NO / new results not yet integrated into AMS LaTeX
```

后继总审计见
`n5_lower16_pure_dependency_splice_audit_20260810.md`。它已补上
orbit--13 特殊化的商秩下降分支，并重放全部八路。当前必要计算根缩为
orbit--1 十五权宇宙的 \(\binom{15}{10}=3003\) 个坐标十平面；其后
三个 \(W_0\) 终端和遗漏的 \(W_M\) 终端均由纯相对/赋值论证排除。

这里原来的 `n=5 INTERNAL VALID` 已撤回。新的全局接口复审发现：
orbit--1 的长度二定理只处理一个特定共同商平面，遗漏
\(W_M=q(\operatorname{Sym}^2\langle x_{00},x_{01},x_{02},x_{03}\rangle)\)。
它满足精确 \(p(W_M)=36\)，且是四个最大五平面见证的共同十维包络交。
完整说明和独立精确诊断见
`n5_orbit1_WM_global_interface_blocker_20260810.md` 与
`perm5_orbit1_missing_WM_exact.py`。

后续研究又严格否定了“相对长度一”这一拟议修复。对端点
$x_{10},x_{11}$，两类显式全阶长度五代数给出不同的
$F_A^{(0)},F_A^{(1)}$，但逐生成元满足
$q(F_A^{(0)})=q(F_A^{(1)})$；二阶碰撞理想恰出现十九个
$2\times2$ minor。详见
`n5_orbit1_WM_same_row_collision_analysis_20260810.md` 与
`perm5_orbit1_WM_x10_x11_collision_twojet_exact.py`。新的必要目标是
控制全部高阶提升；后续赋值两行定理已经改用 pairwise 大交而不是总
提升数来闭合这个局部缺口。总体 route 复审完成以前仍不得生成新外审包。

### 2026-08-10 后续局部推进

必要二元关联簇在四个坐标端点的完整切空间现已独立构造。跨行端点的
切空间维数严格为 $124$，恰等于光滑共同四平面子族的维数；正则局部环
论证因此把一阶等号升级为局部概形等号。结合六平面 $E_5$ 交引理，
lower--16 假设中的跨行端点对已被严格排除。见
`n5_orbit1_WM_crossrow_local_commonM_theorem_20260810.md`。

同行端点的切空间维数为 $134$，多出的十维来自竖直 $W$ 碰撞，不能使用
同一正则性论证。全部 $9045$ 个二次单项式的障碍秩显示，任意抽象二次
张量上共同四平面条件多出 $24$ 条方程；但对结合律允许的秩一 $A$，
真实单项对称下的八个支撑代表均在 $\mathbf Q$ 上满足普通秩与附加
共同四平面秩同为 $331$。右下 $2\times2$ 块则不作错误的有限轨道化，
而把三维 $A$ 空间与全部共同切方向整体计算，两矩阵精确秩同为 $461$。
所以同行 Chow 方向已严格证明到二阶不逃逸，尚未证明到全阶。见
`n5_orbit1_WM_same_row_chow_twojet_noescape_20260810.md`。

固定同行端点的十九个二阶计算现已进一步完全纯化。直接权分解给出
$q(\operatorname{Sym}^2L_0)\cap q(\operatorname{Sym}^2L_1)
=W_M\oplus kX$，故所有共同十平面全阶地由一个对称形式 $A$ 参数化。
一般引理
\[
\mu_p^A(u,v)=A(u,v)p\text{ 结合}
\iff A(p,-)=0\text{ 或 }\operatorname{rank}A\le1
\]
立即给出秩一锥与右下 $2\times2$ 块的必要充分分类。十九方程脚本不再
承担固定端点分类的逻辑责任。见
`n5_orbit1_WM_same_row_fixed_pair_pure_classification_20260810.md`。

低秩部分也已重新独立复审。对 $E_5$，非零秩不超过五的二次型纯线性
代数地等于 $U\otimes W$，其中两个零对角对称因子秩均为二；所以实际
秩恰为四，且任意五维变量空间与 $E_5$ 的交至多一维。另一方面，全部
秩四点的射影簇只有维数六；lower--16 中至少八维的差空间并不会仅由
维数论被迫与它相交。因此低秩分类本身不能解决 moving-base 接口。见
n5_E5_rank_le5_pure_scope_audit_20260810.md。

同行非零碰撞点的切向接口现已进一步纯化。对固定端点分类允许的任意
非零 $A$，令 $d:M\to V/(M+y_0+y_1)$ 为两个五平面的公共四基运动之差。
在 $\operatorname{rad}A$ 上，商像相等方程逐外部行退化为“对称零对角”
矩阵条件；一个两维以上子空间上的纯线性代数引理先杀掉第零行第五列及
外部三行。剩余第一行的三列再由 $22,33,02,12$ 四个源方程直接杀掉。
故必要二元关联本身已纯粹强迫 $d=0$，不需结合律计算。独立有理矩阵在
十三个代表上给出必要关联秩 $331=331$，完整 Chow--Hilbert 秩按分支为
$338=338,339=339,340=340$。见
`n5_orbit1_WM_same_row_nonzeroA_pure_tangent_rigidity_20260810.md`。

同时发现并保留了一个重要全局反例：
$F_\pm=\langle(x_{0a}\pm x_{1a})(x_{0b}\pm x_{1b}):a<b\rangle$
满足相同 permanent 商像而 $F_+\cap F_-=0$。所以大交结论绝非全局
线性代数事实，必须使用 $W_M$ 的局部 Rees/赋值结构。历史上此处只有
纯切向定理；后续第 2026-08-10 赋值补丁已经排除任意高阶相切逃逸。

非零碰撞点的二阶障碍现又有了明确的纯几何候选解释。秩二零对角矩阵在
坐标边附近由 Schur 补写成 $C=u^{-1}(ab^T+ba^T)$，零对角恰给三式
$a_i b_i=0$；行、列两个因子因此使 $E_5$ 的 rank--4 锥在坐标
permanent 处有 $8\cdot8=64$ 个七维光滑正规化分支、十三维切空间及
六个二次分支方程。新的双素数二阶诊断显示：三个非零 $A$ 代表的标号
差元切像均恰为这十三维空间；普通障碍秩为 $6,8,6$，加入六个 rank--4
方程后的叠加秩仍为 $6,8,6$，加入共同四平面后的叠加秩也不增加。
见 `n5_orbit1_WM_same_row_rank4_normalization_route_20260810.md`。
这把下一步缩成了构造完成局部环到 rank--4 正规化的全阶态射；当前仍
只有纯局部几何加严格有限域二阶证据，不能据此宣称 Rees 接口闭合。

同一脚本现又删除全部结合律行独立重放必要关联：三个代表、两个素数均
给出线性秩 331、切维 69，以及普通/共同四平面/叠加二阶障碍秩
$6/6/6$；标号差元切像仍为 rank--4 锥的十三维切空间，六个正规化
二次式与普通障碍叠加仍只有秩六。因此这六式不是 Chow 结合律造成的
巧合，而是商像关联自身的二阶方程。它仍是有限域二阶证书，不是全阶
局部环同构。

切锥论证现已被压成一个纯闭合判据。rank--4 正规化的每个支撑分支可
纯参数化为：射影 rank--4 元 6 维、含其本质四空间的六平面 38 维、
满足一个双线性式的两超平面 9 维、十一维交中的十平面 10 维，总计
63 维。六十四个光滑共同四平面分支的切平面并恰由平方自由完全交
$(a_2b_2,a_3b_3,a_4b_4,c_2d_2,c_3d_3,c_4d_4)$ 定义。若同行必要
关联的二次初始理想含这六式，则切锥理想被两边夹逼而必与该完全交相等，
从而约化局部支撑就是这六十四个共同四平面分支。完整判据见
`n5_orbit1_WM_same_row_tangent_cone_closure_criterion_20260810.md`。
后续纯证明已经把六个二次首项统一到任意非零允许形式 (A)：三个行
冲突落在互异行平方块；三个列冲突经映射
(B:M\to\langle e_2,e_3,e_4\rangle) 的反对称部分与零对角条件排除。
因而二次初始空间在特征零下纯粹等于上述六维完全交，切锥夹逼对每个
实际非零同行碰撞点给出六十四个共同四平面分支的约化局部等号。有限域
代表已降为独立复核，不再承担该定理的逻辑责任。仍缺的是把 (A=0)
的任意 DVR 弧严格提升到这个非零局部模型的 Rees/严格变换引理；因此
不能误报为 lower--16 定理。

rank--one 八支撑仍已在两个素数上独立重放，十六条记录统一为
$6/6/6$，且与 rank--4 六式叠加不增秩；它现在只复核纯定理。右下
$2\times2$ 的连续 rank--2 参数也已由同一纯余核权块论证覆盖，不再是
未决分类。历史上唯一保留的同行局部缺口是 (A=0) 到非零法锥点的
Rees 拼接。后续
\(\texttt{n5\_orbit1\_WM\_same\_row\_valuative\_two\_row\_closure\_20260810.md}\)
不再沿切锥路线，而从饱和和空间的矩形极值出发：交维下降只能一次降到
零，十维 \(E_5\)-交再强迫总十平面为 \(U\otimes\mathbf C^5\)，两个
共同商像 Chow 五平面只能是符号型
\((a\pm\delta b)\otimes\mathbf C^5\)，其任何赋值极限都不可能是
\(M+\langle x_{10}\rangle\) 型。故同行 pair 全阶满足
\(\dim(F_0\cap F_1)\ge9\)。对应 route--4 的两阶段环面拼接见
\(\texttt{n5\_lower16\_route4\_orbit1\_WM\_valuative\_splice\_20260810.md}\)。
小矩阵与矩形程序只作独立精确复核。旧证书脚本为
`perm5_orbit1_WM_same_row_qonly_rank1_supports_Fp_exact.py`。

此前的结构化工作删除 orbit--13
的十权子集分类、orbit--0 的 92 条逆压缩见证边，以及类型 1、13 的
250 条一步 witness 边；本轮又删除 shifted 终态分类中的 1405 轮廓
遍历、七行兼容纤维选择表及 49 项可见影子表。
本轮还以三个移动模式的显式父集结构删除了十四个异常状态的五行最小值表，
并以三段割代价的闭式密度定理删除了十二项 crossing 边际表。

## 新的 orbit--13 证明链

1. 五格支撑 `L_A={00,01,02,10,11}` 的二次商像有十一条非 crossing
   权和三条 crossing 权。
2. 对任意非 crossing 集合 `C`，关系图公式为
   \[
   p(C)=5\tau+\sum_v(a_v+1)(b_v+1).
   \]
   端点计费及两个剩余小情形给出统一界 `p(C)<=3|C|`。
3. 对任意 crossing `q` 及任意已选集合 `D`，加入 `q` 的二十五个
   导数权块分成：
   - 5 个支撑变量块，每块秩降至多一；
   - 11 个外部重复行列块，被 `U_A` 外的权锚到零；
   - 9 个外部三行三列块，为 `K_{3,3}` 去匹配后仍连通。
   因而 `p(D+q)-p(D)<=5`。
4. 若十权集合含 `u<=3` 个 crossing，则
   \[
   p(W)\le3(10-u)+5u\le36<39.
   \]
5. lower--16 的 orbit--13 状态要求 `p(W)>=39`，矛盾。

这条链没有遍历 `C(14,10)=1001` 个集合。旧的精确最大值 `26` 不再是
逻辑前提。

## 独立精确诊断

运行 `perm5_orbit13_structural36_audit.py`，得到
`n5_orbit13_structural36_audit_exact.json`：

- 域：`Q`；
- 相关三次权块：238；
- 全部 `2^14=16384` 个子集均满足结构加权界；
- 2048 个非 crossing 子集均满足显式图公式；
- 三个 crossing 的局部形状计数均为 `5+11+9`；
- 外部二十块的精确最大边际为零，支撑五块各至多一；
- 十权结构上界为 36，实际最大值诊断仍为 26。

这些数据是反例搜索和抄录复核，不是结构证明的前提。

## crossing 十二项边际表删除

固定一个 crossing 权，令 `N<=11` 为已有方向数。新证明把十二个旧值
统一为

\[
\Delta_xp\le
\begin{cases}
N,&0\le N\le4,\\
\lceil3N/4\rceil,&5\le N\le11.
\end{cases}
\]

非角块用 `(u,v,alpha,gamma)` 四个整数参数编码。六边割与
`K_{3,3}` matching 割给出三段代价 `D=0,m-z,2m-o-z`；在
`Q<=11` 下逐段证明 `4(r+m)<=3Q`，并单独加强为 `F(4)<=2`。
四个角块满足 `c<=min(4,s+floor(b^2/4))`，唯一两个密度例外
`(s,b)=(4,0),(0,4)` 正由 `F(4)<=2` 闭合。因此旧十二项值只保留为
诊断输出，不承担逻辑责任。完整证明和整数反例搜索分别在
`n5_crossing_marginal_density_reduction_20260810.md` 与
`perm5_crossing_marginal_density_audit.py`。
正文现从三次单项式、偏导系数行及二次商权标签直接定义局部关系图，
并逐项写出六边重复块和六匹配 `K_{3,3}` 的三类割；因此割代价
`Q=r+A+D` 也不依赖预存真值表。

### p11/p12 等号残差修复

自审曾发现仅由 B10<=50 与 crossing 边际 mu10=8 不能推出
p11<=55，因为粗加法只给 58。当前正文已单独处理无 crossing 等号核：

- 十个 pure row/column 方向若达到 50，必为一整层 K5；
- 在该层上加入任意 crossing 的边际为零；
- 若底层另含一个 square，加入 crossing 的边际至多一。

这由显式六边与 K3,3 割逐块检查。于是 p11 的一个 crossing 分支分别
为 43+8<=51、35+8<=43 或 50+0=50。p12 的一个/两个 crossing 分支
相应为 56、59、60；三个至十二个 crossing 的粗值为

    59,58,60,61,56,57,57,58,56,55.

故全局得到 p11<=55、p12<=61。这一等号残差现在是正文显式证明，
不再藏在“逐层相加”中。

## orbit--1 长度二接口的自包含修复

本轮局部审查发现：旧正文只用内部编号 e0,e1,... 指称共同商平面
W0，且没有展开 (B^2,C,D) 的系数链；旧诊断脚本还导入未嵌入的项目
模块。这是可复现性缺口，虽未发现数值反例，也不能保持不改。

当前正文已直接写出

\[
\begin{aligned}
W_0=\operatorname{Span}\{&
S_{00},S_{01},S_{02},R_{0;01},R_{0;02},R_{0;03},\\
&R_{0;12},R_{0;13},R_{0;23},C_{01;0}\}.
\end{aligned}
\]

在 y=x10+B*x11+C*x20+D*x21 的图表中，比较八个显式商权依次得到

\[
a_0=1,\quad a_1=B,\quad C=0,\quad a_2=a_3=a_4=0,\quad
B^2=0,\quad D-BC=0.
\]

反向见证 x00*y+B*x01*y 证明方案论理想恰为 (B^2,C,D)，不是只证明
根集。新增 perm5_orbit1_length2_standalone_exact.py 只使用矩形关系
q(x_ia*x_jb)=-q(x_ib*x_ja)，没有项目导入；其精确 QQ 输出为
n5_orbit1_length2_standalone_exact.json。脚本与输出均已加入 PDF
附件及轻量重放顺序，但仍只作正文手算的独立诊断。

## shifted 终点的 1405 轮廓遍历删除

令 `k_R` 为实际 shifted 族的纤维大小，`lambda=k^downarrow`，并置
`H_j={R:k_R>=j}`。新证明使用层缺陷恒等式

\[
B(k)-\Phi(\lambda)
=\sum_j\bigl(n(j)-n(j-1)\bigr)
 \bigl(|\partial H_j|-n(|H_j|)\bigr)\ge0.
\]

因此任意实际轮廓先由同面积 Ferrers 分拆控制。只需六个首行长度的
整数算术即可得到七个低分拆及其共轭。转置到至多四行后，非标准大小四
支撑在第一层已经产生 `3*2=6` 的缺陷，而所有低分拆的余量至多 2；
故支撑必须是链 `J_4=(0,1,3,6)`。实际嵌套纤维再满足

\[
|\partial S|-\Phi(\lambda)=3e(F_1)+2e(F_2)+e(F_3),
\]

由一维 ideals 的五个非零缺陷 `1,2,1,1,1` 逐层强迫全部纤维标准。
所以旧 1405 轮廓递推和每型至多六个纤维选择的七行表均不再承担逻辑
责任。完整纯证明在
`n5_shifted_profile_layer_defect_reduction_20260810.md`；独立整数程序
`perm5_shifted_profile_layer_defect_audit.py` 只作交叉诊断。

## 五格可见影子的 49 项表删除

对列二元组 \(B\) 定义
\[
P_k(B)=\{c\notin B:B+c\in J_k\},
\]
再以 \(g_{p,q}(u,v)\) 计数两个父列集合分别落入长度 \(u,v\) 初段的
二元组。若标准族的四行长度为 \((a,b,c,d)\)，五格 Ferrers 平面的
行长为 \((u_0,\ldots,u_4)\)，六个行二元组直接给出
\[
\begin{aligned}
h={}&g_{a,b}(u_2,u_3)+g_{a,c}(u_1,u_3)+g_{b,c}(u_1,u_2)\\
&+g_{a,d}(u_0,u_3)+g_{b,d}(u_0,u_2)+g_{c,d}(u_0,u_1).
\end{aligned}
\]
面积五蕴含 \(u_1\le2\)、\(u_2,u_3\le1\)。四个长度六的一维序列及
三个截面把四个非幸存族的最大杀点数统一界为 \(7,7,6,6\)，所以
可见影子分别至少为 \(41,41,42,42\)。三个幸存族的父集等号分别
强迫 \((5),(4,1),(3,2)\)，其中类型 1、13 的等号平面数为四、二。

因此 49 个逐项值不再承担逻辑责任。完整证明在
`n5_visible_shadow_structural_reduction_20260810.md`；独立精确整数
程序 `perm5_visible_shadow_structural_reduction_audit.py` 仍重算旧
49 值及每族全部 \(\binom{25}{5}=53130\) 个平面，但只用于发现抄录错误。

## 一步逆压缩的 42 个方向记录删除

层缺陷恒等式现加强到任意 Petersen 大小轮廓：
\[
B(k)-\Phi(k^\downarrow)
=\sum_j\Delta_j\{|N(H_j)|-n(|H_j|)\}\ge0.
\]
所以任意一步逆反射先由同一组十四个低分拆控制。把类型 1、13 的行
轮廓及其转置后的列轮廓写在 Petersen 十条边上，四点邻域等号集恰为
五个星，七点等号集恰为十个 \(N(v)^c\)。分拆重数与这两个等号分类
把旧 42 个方向记录统一压成三种移动模式：

\[
r_1:(4,2),\qquad r_1:(10,2),\qquad c_{13}:(2,0),(1,0).
\]

它们分别对应五个例外方向；已有并纤维公式再留下 \(4+6+4=14\) 个
非统一族状态。完整证明在
`n5_inverse_shift_layer_orbit_reduction_20260810.md`；独立整数程序
`perm5_inverse_shift_layer_orbit_reduction_audit.py` 遍历四十个无向
换位只作反例诊断。旧 42 行方向表已不活跃，十四状态的兼容五平面
下界现由下一节的父集公式闭合。

## 十四状态可见最小值表删除

对 `r01`，三个平面位的被杀数只依赖 Hamming 重量，依次为
\(7,3,2,4\)。对 `r02`，四变量公式
\[
e_3(z)+e_3(1-z)+z_0(1-z_1)
 +(1-z_0)(3-z_1-z_2-z_3)
\]
按 \(z_0\) 分开后至多七。对 `r03`，六个状态的潜在被杀点集
不是逐平面最小值表，而只可能是四元素共同集 \(Q_0\)，或给它增加
三个显式点，故大小至多七。两个类型 13 列方向统一满足
\[
7-2z_0-z_1+2z_0z_1\le7.
\]
于是类型 1、13 的可见影子分别至少 \(48-7=41\) 与 \(50-7=43\)。
完整证明与独立整数诊断分别为
`n5_exceptional_visible_parent_reduction_20260810.md` 和
`perm5_exceptional_visible_parent_reduction_audit.py`；后者的 160 次
兼容代入仅交叉核对公式。

## orbit--0 的 92 条见证边删除

对一个十变量移动块，以 \(X\) 表示取高方向的第二坐标三元组集合。
Petersen 图连通且含五圈，因此非平凡 \(X\) 总满足
\[
N_P(X)\cap N_P(X^c)\ne\varnothing.
\]
这迫使每个十变量块统一；两个同时移动块若统一位相反，则第一坐标
一维影子为六、乘积影子为六十。归一化 \(S=S_0\) 后，五格平面的
可见影子由
\[
\begin{cases}
50-2\binom{k}{3}-2\binom{5-k}{3},&b=1,\\
50-2\binom{5-k}{3},&b=2,3,4
\end{cases}
\]
给出，阈值四十只留下同轨完整行。

旧附件把 \(30+3k(5-k)\) 错误地用于所有行反射；该式只对应
\(b=1\)。主文原证明使用 92 条见证边，没有依赖这个错误通用化；
现已用上述分段公式修正附件，并把 92 条边降为非活跃诊断。

精确整数诊断核对了 Petersen 图的 1022 个非平凡子集、31 个有效
方向、8 个非平凡族方向及全部两行五格分布；诊断不参与证明。

## 类型 1、13 的 250 条见证边删除

对任意乘积族，把第一坐标纤维记为 (S_R)。Petersen 字典给出

\[
|\partial S|=\sum_A\left|N_P\!\left(\bigcup_{R\sim A}S_R\right)\right|
\ge\sum_A n\!\left(\left|\bigcup_{R\sim A}S_R\right|\right)
\ge\sum_A n\!\left(\max_{R\sim A}|S_R|\right).
\]

一个 ground-set 反射只有三个二轨道，故末式只含至多三个整数移动量。
任意轮廓层缺陷恒等式与四点/七点等号刚性把它们压成 3 种移动模式；
并纤维公式再把普通影子至多五十的非统一取向缩到 5 个方向、14 个族
状态。再用父变量集

\[
M_q(S)=\{(r,c):(A+r,B+c)\in S\}
\]

分类固定族上的五点平面：类型 1 恰有 4 个可见影子四十的平面，类型
13 恰有 2 个，均为稳定子单轨道。十四个非统一族状态再由上一节的
三个父集结构情形给出被杀数至多七，故全部排除。

纯结构展开位于
`n5_flag_fibre_profile_structural_reduction_20260810.md` 与
`n5_exceptional_visible_parent_reduction_20260810.md`。独立整数程序
`perm5_flag_fibre_profile_reduction_audit.py` 不读取旧 witness 文件，
精确核对旧的 42、5、14、41 与 (4+2) 个等号平面；
`perm5_exceptional_visible_parent_reduction_audit.py` 从坐标定义重建
新父集公式。两者都只作诊断。

## 负面结果：稳定子对称不足以删除 witness forest

`perm5_flag_direction_symmetry_audit.py` 的精确整数诊断给出：

- orbit--0：稳定子大小 480，8 个合法方向压到 3 个方向轨道；
- orbit--1：稳定子大小 2，21 个合法方向仍有 17 个方向轨道；
- orbit--13：稳定子大小 2，21 个合法方向仍有 17 个方向轨道。

所以只按终端稳定子取轨道不能实质替代 orbit--1/orbit--13 的 250 条
见证边；完整等号图的 13、15 个粗签名也不能。随后找到的纤维轮廓路线
不依赖稳定子压缩或统一图模板，故这些旧的否定性诊断与新证明不冲突。

## 无 crossing square 轨道表删除

无 crossing 集合写成 square Ferrers 集 (A)、五个 row 图 (G_i)
及五个 column 图 (H_a)。式

\[
p=5\sum_i t(G_i)+5\sum_a t(H_a)
+\sum_{(i,a)\in A}(d_{G_i}(a)+1)(d_{H_a}(i)+1)
\]

的六类模式计数在 simultaneous row/column compression 下均不减。
最难的 corner 项对固定横臂化为中心点集与 column 图的关联数；二点
重排不等式

\[
(x\vee y)(a\vee b)+(x\wedge y)(a\wedge b)\ge xa+yb
\]

直接给出单调性。压缩后 (A) 为 Ferrers ideal，row/column 图分别
嵌套且 shifted。

Kruskal--Katona 给出五图三角形包络

\[
\tau(e)=(0,0,0,1,1,2,4,4,5,7,10,10,10)_e.
\]

若三类方向数为 (s,r,c)，square 项满足闭式界

\[
Q\le s+R_0+C_0+\min\{rc,4R_0,4C_0\},
\quad R_0=\min(4s,2r),\quad C_0=\min(4s,2c).
\]

该式直接解决 (d=10) 和除十种数值候选外的 (d=9,11,12)。十种
候选由 one-square、row-domino、row-triple 与 L 形闭式度界全部关闭，
得到无 crossing 极值 (35,50,55,60)；九维等号恰为一百个 pure
row/column (K_5-e)。完整证明位于
`n5_nocrossing_compression_structural_reduction_20260810.md`。独立程序
`perm5_nocrossing_compression_diagnostic.py` 穷尽局部二进制不等式，
并枚举 2206、4057、7247、12612 个 shifted 状态作反例诊断；枚举不
承担证明责任。旧七 square 轨道、按 square 数的 (d=10,11,12)
最大值和四-square 十型均已不活跃。

## 当前活跃有限依赖

仍需外审的主要有限对象为：

1. fixed-six 的 58 态计数及八路由分拆已化为
   `C(8,2)+3C(5,2)=58` 与 `38+1+1+9+2+1+1+5=58` 的纯算术；
   无 crossing 小图包络已由二点压缩、Kruskal--Katona 和十种闭式候选
   处理；十二项 crossing 边际表已由三段密度定理删除；仍需外审的是
   这两条结构证明与它们合成的全局 `p_11,p_12` 图界；
2. shifted 终点的层缺陷恒等式、六行分拆算术及 14 个结论轮廓；旧
   1405 轮廓遍历和七行纤维选择表已不活跃；
3. 六边父集公式、四个长度六序列及四个可见影子结构界；旧 49 项表
   已不活跃；
4. 任意轮廓层缺陷恒等式、3 种例外移动模式、5 个例外方向、14 个
   非统一族状态、3 个异常父集结构情形及 6 个五平面等号态；旧 42 个
   方向记录、十四状态最小值表和所有 witness 边均不活跃；
5. orbit--1 的局部长度二消元；
6. orbit--0 的局部图与 Fourier/Koszul 结构链。

## 交付边界

既有 v11 PDF/ZIP 是冻结交付物，没有被覆盖。本文件与改写后的 LaTeX
目前只是 v12 研究候选。候选 PDF 已完成 LaTeX 编译、全页渲染检查、
附件 manifest 字节核对和十八个活跃检查器重放；随附 reviewer ZIP
仅是最终 PDF、LaTeX 源和清单的传输封装。v12 尚未接受新的独立外审，
因此不能表述为“已外审版本”。
