# v11 严格自审：`perm_3,perm_4,perm_5` Chow 秩

日期：2026-08-10

## 裁决

```text
n=3: VALID
n=4: VALID / exact rational certificate independently replayed
n=5: INTERNAL VALID / finite-certificate proof / external review pending
publication-ready: NO, until independent external review
```

这里的 `INTERNAL VALID` 不是外审通过。五阶证明仍含公开的有限分类表、
witness forest 和小图割；它不是无分类的概念性证明。

## 本轮发现并修复的关键逻辑问题

早先 v11 草稿用一段过短的 fixed-four 文字替代 lower--15 的大型证书，
该段并没有逐条证明旧证书的所有几何入口，不能作为闭合证明。现在已
完全删除这条前置依赖。

新的入口是拆项绕行：基础 Koszul 下界给最小秩至少十。若存在
`r<=15` 的最小分解，保留六个原始项，并对其余项反复使用

\[
T=\frac12T+\frac12T.
\]

于是余式恰成为九项之和，fixed-six 反证直接覆盖所有 `r<=15`。因此
旧 lower--15 的约 10GB SAT/DRAT 层不再是五阶定理的逻辑前提。

同时补明了缺一行支撑时从行 catalecticant 秩十到 25 变量三次导数
空间维数一百的列极化步骤；还把形式线性化引理改写为有限商
`R/m^N` 的分次滤过与线性约化分裂，避免对无限维完备环直接选截面。

## 当前活跃五阶链

1. `rank K(perm_5)=2400`，单 Chow 项至多 `240`；
2. 拆项绕行把 `rank<=15` 化为 fixed-six 加九项余式；
3. Petersen 影子、双商不等式与 `t<=51` 给 58 个状态；
4. 七条非 `d=10` 路由及相对 `d=11,12` 路由由小图表、父集表和
   相对 Grassmann 论证排除；
5. `d=10` 通过同时 shifting、14 个 shifted 轮廓、49 项可见影子表
   和 342 条一步逆压缩 witness 边缩到 orbit `0,1,13`；
6. orbit--1 的相对局部长度至多二，orbit--13 的 1001 个十权集合满足
   `p<=26`；
7. orbit--0 由列群形式刚性、Boolean Fourier 和
   `2215>9*245=2205` 排除；
8. Glynn 十六项恒等式给上界。

## 精确重放

本轮重新运行并通过：

- `n=3`: `80/26`，下界四；
- `n=4`: `560/92`、图表常数 `-32768`；
- fixed-six: 58 状态；
- `s19d9`: 800 个等号旗标、上界 44；
- `p_9,p_10,p_11,p_12`: `35,50,55,61`；
- shifted: 1405 轮廓、14 个低轮廓；
- witness forest: 50 个方向、342 条边、5076 个布尔赋值；
- orbit--13: 1001 个十权集合、最大 `p=26`；
- orbit--1: 四个固定旗标核维均为三；
- orbit--0: 4100 顶点切图核维八；
- Fourier: 600 个秩四六点集诊断均与纯界一致。

## PDF 与可复现性

AMS PDF 为 26 页，内嵌 55 个附件；`attachment_manifest.json` 对其余
54 个附件记录字节数及 SHA--256，已从 PDF 内嵌字节重新计算并全部
一致。LaTeX 无 overfull、缺字或未定义引用；只有两处无害 underfull。

## 剩余风险

1. 五阶链需要真正独立的外部审查者重写或重放有限表，内部同源复核
   不能替代外审。
2. 主文为 26 页压缩版；完整有限表与推导说明作为 PDF 内嵌附件存在。
   审稿人必须把这些附件视为证明附录，而不是只读主文摘要。
3. 若外审发现任一状态语义、退化闭性或局部到相对提升接口不成立，
   五阶结论必须立即退回 `PARTIAL`；不得以已有 PASS 字符串抗辩。
