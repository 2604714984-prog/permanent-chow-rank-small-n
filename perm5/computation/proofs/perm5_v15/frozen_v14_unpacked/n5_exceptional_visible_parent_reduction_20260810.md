# `perm_5` 十四个异常旗标状态的父集结构化消去

日期：2026-08-10

## 1. 结论与证据边界

设 `type 1` 与 `type 13` 分别是 shifted 三次族

\[
S_1=(10,4,4,2),\qquad S_{13}=(7,5,4,4),
\]

其兼容五平面分拆分别为 `(4,1)` 与 `(3,2)`。一步逆压缩的普通影子
下界已经把所有非统一族取向压到五个方向、十四个状态。本笔记证明：
对这十四个状态，每个兼容五平面至多杀掉七个二次影子点。因此

\[
|\partial_{L^\perp}S|\ge41\quad(S_1),\qquad
|\partial_{L^\perp}S|\ge43\quad(S_{13}).
\]

证明只使用下面两个短 Boolean 公式和一个七元素潜在父集分类；旧的
十四行最小值表不再是活跃证明依赖。脚本
`perm5_exceptional_visible_parent_reduction_audit.py` 从坐标定义重建父集，
用整数位集独立核对公式；其 160 次兼容族--平面代入仅是诊断。

## 2. 父集计数

以 `ab,cd` 表示二次影子点
\((\{a,b\},\{c,d\})\)。对三次族 \(S\)，记

\[
M_q(S)=\{(r,c):(A\cup\{r\},B\cup\{c\})\in S\},
\qquad q=(A,B).
\]

若五平面的坐标集合仍记为 \(L\)，则被杀点数为

\[
h_S(L)=\#\{q:\varnothing\ne M_q(S)\subseteq L\},
\]

因而

\[
|\partial_{L^\perp}S|=|\partial S|-h_S(L).                 \tag{2.1}
\]

逆压缩平面在每个二轨道中恰取低点或高点。以 \(z_i=0,1\) 分别表示
这两个选择，并置 \(y_i=1-z_i\)。于是每个被杀父集的指示函数就是
若干 \(z_i\) 与 \(y_i\) 的乘积。

## 3. 类型 1 的两个二点移动方向

### 3.1 方向 `row 0<-1`

三个平面二轨道为

\[
(01,11),\quad(02,12),\quad(03,13).
\]

两个非统一族取向互为 \(z\leftrightarrow1-z\)。对第一个取向，十一
个可能被杀父集逐项合并为

\[
\begin{aligned}
h_{01}(z)={}&
\sum_{0\le i<j\le2}z_i z_j+z_0z_1z_2
+\sum_{0\le i<j\le2}y_i y_j+y_0y_1y_2
+\sum_{i=0}^2y_i .                                      \tag{3.1}
\end{aligned}
\]

若 \(w=z_0+z_1+z_2\)，式 (3.1) 依次化为

\[
\binom w2+\mathbf1_{w=3}
+\binom{3-w}2+\mathbf1_{w=0}+3-w,
\]

故在 \(w=0,1,2,3\) 时分别为 \(7,3,2,4\)，从而 \(h_{01}\le7\)。
互补取向把 \(w\) 换成 \(3-w\)，结论相同。

### 3.2 方向 `row 0<-2`

四个平面二轨道为

\[
(00,20),\quad(01,21),\quad(02,22),\quad(03,23).
\]

同样只需处理一个族取向。此时十二个潜在父集给出

\[
\begin{aligned}
h_{02}(z)={}&e_3(z_0,z_1,z_2,z_3)+e_3(y_0,y_1,y_2,y_3)\\
&+z_0y_1+y_0(y_1+y_2+y_3),                              \tag{3.2}
\end{aligned}
\]

其中 \(e_3\) 是三次基本对称多项式。若 \(z_0=0\)，置
\(w=z_1+z_2+z_3\)，则

\[
h_{02}=\binom w3+\binom{4-w}3+3-w\le7;
\]

若 \(z_0=1\)，置同一 \(w\)，则

\[
h_{02}=\binom{1+w}3+\binom{3-w}3+1-z_1\le4.
\]

所以仍有 \(h_{02}\le7\)。另一族取向把所有 \(z_i\) 同时互补。

## 4. 类型 1 的八点移动方向 `row 0<-3`

六个非统一族状态可记为

\[
\{3\},\ \{6\},\ \{3,6\},\ K,\ K\cup\{3\},\ K\cup\{6\},
\qquad K=(J_{10}\setminus J_2)\setminus J_4.             \tag{4.1}
\]

这里的记号来自 Petersen 纤维的标准边次序。对一个族状态 \(X\)，令
\(\mathcal Q_X\) 为：当兼容 `(4,1)` 平面遍历它的四个取向位时，
至少能被其中一个平面杀掉的全部二次影子点。直接从
\(M_q(S)\subseteq L\) 读取，六个集合只有以下三种：

\[
Q_0=\{12,04;\ 12,14;\ 12,24;\ 12,34\};                 \tag{4.2}
\]

\[
\begin{aligned}
\mathcal Q_{\{3\}}&=Q_0\cup\{23,12;\ 23,13;\ 23,23\},\\
\mathcal Q_{K\cup\{6\}}&=Q_0\cup\{02,12;\ 02,13;\ 02,23\},\\
\mathcal Q_X&=Q_0
\quad\text{对其余四个 }X.                              \tag{4.3}
\end{aligned}
\]

式 (4.3) 是父集包含关系，不是最小值枚举。任一固定兼容平面所杀的点
都属于相应 \(\mathcal Q_X\)，故立即得到

\[
h_S(L)\le|\mathcal Q_X|\le7.                             \tag{4.4}
\]

## 5. 类型 13 的两个列方向

对 `column 0<-3`，两个平面二轨道为

\[
(00,03),\qquad(10,13).
\]

非统一族取向是 `010` 与 `101`，二者仍互为全互补。对 `010`，父集
指示函数合并为

\[
h_{13}(z_0,z_1)=7-2z_0-z_1+2z_0z_1.                       \tag{5.1}
\]

当 \(z_0=0\) 时右端为 \(7-z_1\)；当 \(z_0=1\) 时为
\(5+z_1\)。所以 \(h_{13}\le7\)。方向 `column 1<-3` 的两个二轨道
为 `(01,03),(11,13)`，父集公式完全相同；取向 `101` 则把
\(z\) 换成 \(1-z\)。故四个类型 13 状态全部满足同一上界。

## 6. 合并

类型 1 的六个非统一状态都有普通影子大小 48，类型 13 的四个状态有
普通影子大小 50。式 (2.1) 与各节的 \(h\le7\) 给出

\[
48-7=41>40,
\qquad
50-7=43>40.                                                \tag{6.1}
\]

连同两个二点方向各两个状态，计数为

\[
2+2+6+2+2=14.
\]

因此旧的五行/十四状态可见最小值表可以从活跃证明链删除。

## 7. 独立精确审计

运行

```text
python perm5_exceptional_visible_parent_reduction_audit.py
```

必须输出

```text
PASS_EXACT_INTEGER_EXCEPTIONAL_VISIBLE_PARENT_REDUCTION_AUDIT
structural_parent_cases = 3
exceptional_directions = 5
nonuniform_family_states = 14
diagnostic_compatible_family_plane_assignments = 160
maximum_killed_parent_points = 7
uniform_minimum_visible = 41
active_14_state_visible_table_required = false
```

脚本不读取旧十四行表。它从三子集、二子集、偏导父点及 elementary
shift 的坐标定义重新生成全部对象，并逐项核对 (3.1)、(3.2)、
(4.2)--(4.3)、(5.1)。因此 PASS 是书面证明的独立回放诊断，而不是
替代书面证明的黑箱证书。
