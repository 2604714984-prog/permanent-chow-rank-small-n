# lower--16 route 4 的 orbit--1 \(W_M\) 纯赋值拼接

日期：2026-08-10

状态：VALID PURE LOCAL SPLICE。本文只替换 route 4 中遗漏的
\(W_M\) 终端；route 4 到 orbit--1 坐标旗标的压缩分类仍由其各自的
纯证明或精确有限证书承担。本文不把该有限分类冒充为纯数学定理。

## 1. 无循环入口

只使用 route 4 在进入 orbit--1 终端以前已经得到的以下事实：

1. 泛纤维存在四个十维 Chow 二次块
   \[
   F_i\subset\operatorname{Sym}^2L_i\qquad(1\le i\le4),
   \]
   每个都与 \(E_5\) 横截；
2. 四个商像相同：
   \[
   q(F_1)=\cdots=q(F_4)=W,\qquad \dim W=10;
   \]
3. 四个 \(F_i\) 的和是直和；
4. orbit--1 的当前终端为
   \[
   W^*=W_M=q(\operatorname{Sym}^2M),\qquad
   M=\langle x_{00},x_{01},x_{02},x_{03}\rangle,
   \]
   且每个 \(L_i^*\) 位于固定旗标局部族
   \[
   \mathbf P(N),\qquad
   N=\langle x_{10},x_{11},x_{20},x_{21}\rangle,
   \]
   即 \(L_i^*=M+\langle y_i\rangle\)。

前三条来自 fixed--six 的四饱和直和块引理；第四条是 orbit--1
旗标的纯局部描述。这里不使用旧的“\(W_M\) 相对长度一”、四分支
枚举、跨行 pair 定理、六块两两不同或总关系核 \(k\le2\)。

## 2. 同时把四个端点坐标化

令行列对角环面作用在 \(V\) 上。它保持 \(E_5\)、\(M\) 与 \(W_M\)。
取一个在
\[
x_{10},x_{11},x_{20},x_{21}
\]
上权重两两不同的一参数子群 \(\lambda(u)\)。对每个非零
\(y_i\in N\)，射影极限
\[
\lim_{u\to0}\lambda(u)[y_i]
\]
是其非零支撑中最小权的一个坐标点。因此同一个 \(\lambda\) 同时把
四个 \(L_i^*\) 送到
\[
M+\langle x_{10}\rangle,\quad
M+\langle x_{11}\rangle,\quad
M+\langle x_{20}\rangle,\quad
M+\langle x_{21}\rangle
\tag{2.1}
\]
中的四个（允许重复）。

这一步可与原 DVR 退化合并成一条 DVR 弧。若原参数为 \(t\)，考虑
二参数族
\[
\lambda(u)\cdot(F_i(t),L_i(t),W(t)).
\]
在有限多个 Plücker 坐标上取先 \(t\)、后 \(u\) 的字典序初项；取
\(t=s^N,u=s\) 且 \(N\gg0\)，便由一参数曲线实现同一个初项。泛纤维
仍是四个直和 Chow 块，商像仍共同，而特殊纤维正是 (2.1) 的坐标
端点。这是标准的有限权一参数合并，不引入完成局部环或 Rees
有限生成假设。

在坐标端点
\(L^*=M+\langle x_{ra}\rangle\) 上，
\[
E_5\cap\operatorname{Sym}^2L^*=0.
\tag{2.2}
\]
确实，一个 \(E_5\) 的矩形基元需要外部行中的两个不同列，而
\(L^*\) 在该行只有一个坐标。共同商像的闭关联条件给
\(q(F_i^*)\subset W_M\)；由 (2.2) 及两边都是十维，必有
\[
F_i^*=\operatorname{Sym}^2M.
\tag{2.3}
\]
所以合并后的任意一对都满足同行赋值定理的全部特殊纤维假设。

## 3. 鸽巢矛盾

(2.1) 的四个坐标端点只分布在外部第 1、2 两行。四个块中必有两个
\(F_i,F_j\) 的端点位于同一外部行；端点可以相同，也可以不同。

由
\(\texttt{n5\_orbit1\_WM\_same\_row\_valuative\_two\_row\_closure\_20260810.md}\)
的全阶纯赋值定理，
\[
\dim(F_i\cap F_j)\ge9.
\tag{3.1}
\]
但 route 4 的入口已经给
\[
F_1\oplus F_2\oplus F_3\oplus F_4,
\]
故左端必须为零，矛盾。

因此
\[
\boxed{\text{route 4 的 orbit--1 }W_M\text{ 终端不存在。}}
\tag{3.2}
\]

这个论证同时覆盖 \(t=48,49,50\) 的 orbit--1 后代，因为新增的旗标
坐标不改变四个块的共同商像、直和性或上述特殊 \(W_M\) 分支。

## 4. 证据边界

- **已证明、纯数学：** 两阶段 DVR 合并、坐标端点处 (2.2)--(2.3)、
  鸽巢选择及由同行定理得到的矛盾。
- **不再需要：** \(W_M\) 的全提升数上界、跨行 pair 排除、六块
  pairwise distinct、\(k\le2\)。
- **仍由独立入口承担：** 一般反例压缩到 route 4、四个直和饱和块、
  orbit--1 旗标与四个 \(p=36\) 坐标商终端的完备分类。
- **全局裁决：** 在重新审计上述入口及 route 1--3、5--8 以前，
  \(\operatorname{ChowRank}(\operatorname{perm}_5)\ge16\) 仍标记为
  PARTIAL，而不是提前标记 VALID。
