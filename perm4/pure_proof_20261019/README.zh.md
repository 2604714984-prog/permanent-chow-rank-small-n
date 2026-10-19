# perm4：完整的无计算证明改写

日期：2026-10-19。范围：普通 Chow rank，不是 border Chow rank。

## 本轮结论

已经得到一份完整的纯数学证明，保留原来的“减去一项”下界框架，替换三处计算依赖：基础秩 560、单项秩 92、以及对所有非零向量成立的 rank-99 引理。关键变化不是把大行列式手算一遍，而是证明一个遗漏单个导数的三次式分类，再作显式行列缩放。

正文为 `main.tex`；本轮编译的阅读版为 7 页 PDF，随对话交付。这里的“完整”指论证链已经闭合，不表示经过外部同行评审或形式化证明系统认证。旧稿、旧证书和 main 分支均未覆盖。新稿包含 AI 辅助说明。

## 核心突破一：少检查一个导数，只多出一个立方项

设

\[
E=\operatorname{span}\{x_{ia}x_{jb}+x_{ib}x_{ja}:i<j,\ a<b\},
\]

设 \(D\) 为 16 个三阶子 permanent 张成的空间，\(z=x_{00}\)。新证明的核心引理是

\[
\{g\in\operatorname{Sym}^{3}V:\partial_{ij}g\in E\text{ 对一切 }(i,j)\ne(0,0)\}
=D\oplus\mathbb K z^3.
\]

证明不是计算这个空间的矩阵秩，而是检查哪些三次单项式可以有非零系数。

**普通禁项。** 不含 \(z\) 的坏单项式，可以选一个非 \(z\) 的导数，留下同一行、同一列或平方的二次单项式，因而系数必须为零。\(z^2u\)（\(u\ne z\)）由对 \(u\) 求导排除。\(zuw\) 中若 \(u\) 或 \(w\) 位于第零行或第零列，也可直接排除。

**必须单独处理的例外。** 剩下可能漏掉的是 \(zuw\)，其中 \(u,w\) 都是内部变量，但彼此同一行或同一列。令 \(w=x_{ab}\)。对 \(u\) 求导，\(E\) 的矩形系数条件要求 \(z x_{ab}\) 与 \(x_{0b}x_{a0}\) 的系数相等。因此 \(zuw\) 的系数被迫关联到 \(u x_{0b}x_{a0}\) 的系数。后者再对一个边界变量求导，就会留下同一行或同一列的禁项，所以其系数为零，前者也必须为零。\(u=w\) 的情况仅多出非零倍数 2，同样成立。

**匹配项系数仍然相等。** 固定三行三列后，六个匹配项的系数由交换条件联系。遗漏 \(\partial_{00}\) 最多删掉一条联系；这条联系可由三步替代：

\[
\begin{aligned}
z x_{ia}x_{kb}
&\leftrightarrow x_{0a}x_{i0}x_{kb}\\
&\leftrightarrow x_{0a}x_{ib}x_{k0}
\leftrightarrow z x_{ib}x_{ka}.
\end{aligned}
\]

三步使用的共同因子都不是 \(z\)，因此没有使用被遗漏的导数。六个系数仍然相等，贡献一个三阶子 permanent。唯一新增的单项式是 \(z^3\)。

## 核心突破二：只须证明坐标点，不必控制一般向量的大矩阵

对于原稿的映射

\[
\psi_v:\operatorname{Sym}^2V/E\to
(V\otimes\Lambda^2V)/\delta(E\otimes V),\qquad
[q]\mapsto[\delta(q\otimes v)],
\]

上述引理与 Koszul 核的梯度描述给出

\[
\ker\psi_z=\mathbb K[z^2],\qquad\operatorname{rank}\psi_z=99.
\]

对任意非零 \(v\)，先置换行列使 \(v_{00}\ne0\)。再作

\[
\tau_t(x_{ij})=t^{\mathbf1_{i\ne0}+\mathbf1_{j\ne0}}x_{ij}.
\]

这意味着角点不变、边界变量乘 \(t\)、内部变量乘 \(t^2\)。同一矩形的两个单项式权重相等，因此 \(t\ne0\) 时 \(\tau_t\) 保持 \(E\)，并保持相关映射的秩。而

\[
\tau_t v\longrightarrow v_{00}x_{00}\quad(t\to0).
\]

矩阵秩在这种特殊化中只能下降，不能上升。因此

\[
99=\operatorname{rank}\psi_{v_{00}x_{00}}
\le\operatorname{rank}\psi_v\le99.
\]

这就证明了所有非零 \(v\) 的 rank-99 引理。没有计算 659 阶子式，也没有计算 99 阶 Schur 补或检验 156 条支撑边。

注意：这里不让某个核向量随退化移动，所以没有“核向量在极限消失或与平方方向合并”的漏洞。比较的是固定商空间之间的一族矩阵的秩。

## 从新引理回到 Chow rank = 8

其余论证已经逐步重写在正文中：

1. 完整三次 prolongation 恰好是 \(D\)，得到 \(36\cdot16-16=560\)。单项的 prolongation 恰好由四个平方自由三次项张成，得到 \(6\cdot16-4=92\)。
2. \(E\) 中非零二次型的秩至少为四；秩为四时的结构给出 \(\dim(E\cap E_T)\le1\)。
3. rank-99 引理推出新增任意 \(q\notin E\) 至少贡献 15 维，从而得到 575。
4. 同时使用行空间和列空间，得到减去任意非零 Chow 项后的秩至少为 559。
5. 七项分解减去一项只剩六项，秩至多 \(6\cdot92=552\)，与 \(559>552\) 矛盾。Glynn 恒等式给出八项上界。

## 六阶段完成情况

| 阶段 | 本轮结果 |
|---|---|
| 审计计算依赖 | 明确三处替换目标，检查固定映射、对偶配对和依赖顺序 |
| 基础秩去计算 | 560、92 均有系数分类证明 |
| chart 引理 | 遗漏导数引理 + 显式行列缩放，证明所有非零向量 |
| 结构与延拓 | 秩四分类、交集界、575 和 559 的推导已完整写出 |
| 替代总体路线 | 无须另造 flattening；普通 tensor rank 结果不直接转移 |
| 交付与检查 | 自包含正文、内部审计、交接、可选独立检验和阅读 PDF |

没有宣称所有可能的替代方法都已穷尽，也不由此推出其他 n 的普通或 border Chow rank 等式。

## 关于检验程序

`verify_supplementary.py` 是本轮重新写的独立交叉检查，不导入旧项目模块。它检查禁项规则、六匹配连接、行列权重、Glynn 展开，以及有理数和两个素数下的有关维数。结果记录在 `supplementary_results.json`。

**删除检验程序后，正文证明仍然完整。** 这些结果只用于发现实现或推导错误，不是定理的前提。

复核命令：

```sh
python -B verify_supplementary.py --output supplementary_results.json
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
pdflatex -no-shell-escape -interaction=nonstopmode -halt-on-error main.tex
```
