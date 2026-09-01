# `perm_5` lower--15 依赖的拆项绕行引理

日期：2026-08-10

## 命题

若 fixed-six 论证能排除所有形如

\[
\operatorname{perm}_5=T_1+\cdots+T_6+R_1+\cdots+R_9
\]

的十五个非零 Chow 项表达式，则它已经直接证明

\[
\operatorname{ChowRank}(\operatorname{perm}_5)\ge 16,
\]

不需要预先证明 lower--15，也不需要 lower--15 的 SAT/DRAT 层。

## 证明

基础 Koszul 展平给

\[
\operatorname{ChowRank}(\operatorname{perm}_5)
\ge \left\lceil 2400/240\right\rceil=10.
\]

反设秩为 `r<=15`，并取一个最小的 `r` 项表达式。于是 `10<=r<=15`。
保留其中六个原始项作为 fixed-six 块。剩余 `r-6` 个项的数目介于四和
九之间。对任意非零 Chow 项 `T`，特征零中

\[
T=\frac12T+\frac12T
\]

把它写成两个非零 Chow 项；标量可吸收到任意一个线性因子中。每次拆项
使余项数增加一而不改变多项式。重复 `15-r` 次，余式恰成为九个非零
Chow 项之和，而 fixed-six 的六个原始项保持不变。

因此任何至多十五项表达式都会产生 fixed-six 论证所排除的十五项
表达式。证毕。

## 逻辑边界

1. 该引理只用 Chow 锥对非零标量封闭；不使用项的参数一般性。
2. fixed-six 后续的秩、影子和耦合不等式只要求余式是至多九项之和；
   拆分产生的重复项不会破坏这些上界。
3. 若后续某个局部终端需要四个互异或直和的块，该性质由终端自身的
   `h,t,d` 等号条件推出，不是由拆项假设推出。
4. 所以旧 lower--15 的约 10GB SAT/DRAT 数据既不需要嵌入，也不再是
   `ChowRank(perm_5)=16` 活跃证明链的先决条件。
