"""Fresh exact regression checks from polynomial definitions, not proof premises.
No project modules, stored rank tables, or expected-output files are imported.
"""
from __future__ import annotations
from collections import defaultdict
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
from math import comb
from pathlib import Path
import argparse, json, random, time

def require(ok, context):
    if not ok: raise AssertionError(context)

def basis(columns):
    pivots = {}
    chosen = []
    for original in columns:
        c = {i:F(v) for i,v in original.items() if v}
        while c:
            lead=min(c); val=c[lead]
            if lead not in pivots:
                pivots[lead]={i:v/val for i,v in c.items()}
                chosen.append(original)
                break
            for i,v in pivots[lead].items():
                a=c.get(i,F(0))-val*v
                if a: c[i]=a
                else: c.pop(i,None)
    return chosen

def rank(columns): return len(basis(columns))
def mons(n,j): return list(combinations_with_replacement(range(n),j))
def mul_linear(p, v):
    q=defaultdict(int)
    for mon,c in p.items():
        for j,a in enumerate(v):
            if a: q[tuple(sorted(mon+(j,)))]+=c*a
    return {m:c for m,c in q.items() if c}

def polynomial(factors):
    p={():1}
    for v in factors: p=mul_linear(p,v)
    return p

def derivative(p,j):
    q={}
    for m,c in p.items():
        k=m.count(j)
        if k:
            z=list(m); z.remove(j); q[tuple(z)]=c*k
    return q

def derivative_space(p, n, output_degree):
    degree=len(next(iter(p)))
    cols=[]
    for op in mons(n,degree-output_degree):
        q=p
        for j in op: q=derivative(q,j)
        if q: cols.append(q)
    return basis(cols)

def hessian_rank(q,n):
    cols=[{} for _ in range(n)]
    for (a,b),v in q.items():
        cols[a][b]=cols[a].get(b,0)+v
        cols[b][a]=cols[b].get(a,0)+v
    return rank(cols)

def symbol_rank(U,R,P,n):
    d=len(P); Q=mons(n,2); ix={m:i for i,m in enumerate(Q)}
    killed=[]
    for a in range(d):
        for q in R: killed.append({a*len(Q)+ix[m]:c for m,c in q.items()})
    cols=list(killed)
    for g in U:
        out=defaultdict(F)
        for j in range(n):
            dg=derivative(g,j)
            for a in range(d):
                if P[a][j]:
                    for m,c in dg.items(): out[a*len(Q)+ix[m]]+=c*P[a][j]
        cols.append(dict(out))
    return rank(cols)-rank(killed)

def quotient(n,d,rng,kind):
    if not d: return []
    if kind==0: return [[int(a==j) for j in range(n)] for a in range(d)]
    while True:
        P=[[rng.randint(-2,2) for j in range(n)] for a in range(d)]
        if rank([{j:v for j,v in enumerate(row) if v} for row in P])==d: return P

def random_line(Fspace,n,rng):
    if n<4: return []
    for _ in range(20):
        q=defaultdict(F)
        for v in Fspace:
            a=rng.randint(-2,2)
            for m,c in v.items(): q[m]+=a*c
        q={m:c for m,c in q.items() if c}
        if hessian_rank(q,n)>=4: return [q]
    return []

def local_product_checks(m,rng):
    count=0; products_count=0; min_slack=None; ranks_seen={}
    for n in range(1,m+1):
        coordinate=[[int(i==j) for j in range(n)] for i in range(n)]
        for trial in range(8):
            factors=coordinate[:]
            while len(factors)<m:
                if trial<min(n,4): v=[int(j<=trial) for j in range(n)]
                else:
                    v=[rng.randint(-2,2) for _ in range(n)]
                    if not any(v): v[0]=1
                factors.append(v)
            T=polynomial(factors)
            U=derivative_space(T,n,3); Fs=derivative_space(T,n,2); u=len(U)
            if m==5: require(len(Fs)==u,('adjoint-dimensions',n,trial))
            require(u <= (10 if m==5 else 20),('rank-cap',m,n,trial,u))
            products_count+=1
            ranks_seen.setdefault(str(n),set()).add(u)
            Rs=[[],random_line(Fs,n,rng)] if n>=4 else [[]]
            for d in range(n+1):
                for kind in (0,1,2):
                    P=quotient(n,d,rng,kind)
                    for R in Rs:
                        r=symbol_rank(U,R,P,n)
                        slack=F(r)+F((10 if m==5 else 20)-u,2)-(F(2) if m==5 else F(10,3))*d
                        require(slack>=0,('local-estimate',m,n,trial,d,P,R,u,r))
                        min_slack=slack if min_slack is None else min(min_slack,slack)
                        count+=1
    return {'products':products_count,'quotient_tests':count,'minimum_slack':str(min_slack),'observed_middle_ranks':{k:sorted(v) for k,v in ranks_seen.items()}}

def squarefree_checks():
    result={}
    for n, max_edges in ((5,1),(6,3)):
        edges=list(combinations(range(n),2)); triples=list(combinations(range(n),3))
        cases=0; minima={d:comb(n,3) for d in range(n+1)}
        for bsize in range(n+1):
            for Bt in combinations(range(n),bsize):
                B=set(Bt); O=set(range(n))-B; d=len(O)
                for a in range(max_edges+1):
                    for At in combinations(edges,a):
                        A=set(At)
                        killed=[I for I in triples if all(tuple(j for j in I if j!=i) in A for i in I if i in O)]
                        prediction=comb(bsize,3) if bsize>=3 else 0
                        prediction+=d*sum(set(e)<=B for e in A)
                        prediction+=sum(comb(sum(tuple(sorted((b,o))) in A for o in O),2) for b in B)
                        prediction+=sum(all(e in A for e in combinations(I,2)) for I in combinations(sorted(O),3))
                        require(len(killed)==prediction,('triple-formula',n,B,A))
                        r=len(triples)-len(killed); minima[d]=min(minima[d],r)
                        if n==5: require(r>=2*d,('five-sf',B,A,r))
                        elif d<=5: require(3*r>=10*d,('six-sf',B,A,r))
                        cases+=1
        result[str(n)]={'coordinate_cases':cases,'minimum_ranks':minima}
    require(result['6']['minimum_ranks'][6]==19,'full-quotient triangle negative control')
    return result

def five_span_sextics():
    rows=[]; n=5
    for s in range(1,6):
        fs=[[int(i==j) for j in range(n)] for i in range(n)]+[[int(i<s) for i in range(n)]]
        T=polynomial(fs); U=derivative_space(T,n,3)
        wanted=list(combinations(range(n),3)) if s==1 else [I for I in combinations(range(n),3) if set(range(s)) & (set(range(n))-set(I))]
        require(rank(U+[{I:1} for I in wanted])==len(U),('actual-squarefree-inclusion',s))
        missing=10-len(wanted)
        require(2*missing<=20-len(U),('defect-budget',s,len(U),missing))
        rows.append({'s':s,'actual_u':len(U),'chosen_squarefree_dim':len(wanted),'missing':missing})
    return rows

def delta(q,v,N):
    out=defaultdict(F)
    for (a,b),c in q.items():
        for j,coef in enumerate(v):
            if not coef: continue
            for x,y in ((a,b),(b,a)):
                if x==j: continue
                out[(y,min(x,j),max(x,j))]+=c*coef*(1 if x<j else -1)
    return {m:c for m,c in out.items() if c}

def quartic_quotient_checks():
    N=16; Es=[]
    for i,j in combinations(range(4),2):
        for a,b in combinations(range(4),2): Es.append({tuple(sorted((4*i+a,4*j+b))):1,tuple(sorted((4*i+b,4*j+a))):1})
    I=basis([delta(q,[int(k==j) for k in range(N)],N) for q in Es for j in range(N)])
    require(len(I)==560,('quartic-base',len(I)))
    vectors=[[int(k==0) for k in range(N)],[int(k in (0,1,4)) for k in range(N)],[1]*N,[(-1)**k*(k+1) for k in range(N)]]
    ranks=[]
    for v in vectors:
        r=rank(I+[delta({m:1},v,N) for m in mons(N,2)])-560
        require(r==99,('quartic-quotient',v,r)); ranks.append(r)
    return {'base_rank':len(I),'quotient_ranks':ranks}

def negative_controls():
    # Rank-two R invalidates the strengthened small-complement kernel lemma.
    g={(0,1,2):1}; R=[{(0,1):1}]; P=[[0,0,1]]
    require(hessian_rank(R[0],3)==2,'negative-control rank')
    require(symbol_rank([g],R,P,3)==0,'rank-two line must kill g')
    require(any(2 in mon for mon in g),'g must not be supported on ker P')
    # Actual derivatives need not span every formal complementary factor product.
    diagnostics=[]
    for degree,n in ((5,4),(6,5)):
        for support in range(1,n+1):
            factors=[[int(i==j) for j in range(n)] for i in range(n)]+[[int(j<support) for j in range(n)]]
            T=polynomial(factors)
            actual=len(derivative_space(T,n,3))
            formal=rank([polynomial([factors[i] for i in positions]) for positions in combinations(range(degree),3)])
            require(actual<=formal,('actual/formal containment',degree,support))
            diagnostics.append({'degree':degree,'support':support,'actual_cubic_dim':actual,'formal_cubic_dim':formal})
    require(any(x['actual_cubic_dim']<x['formal_cubic_dim'] for x in diagnostics),'retain a genuine actual/formal mismatch')
    return {'rank_two_line_kills_cubic_outside_kernel':True,'actual_vs_formal_diagnostics':diagnostics}

def permanent_prolongations():
    # Build the quotient constraints from row/column positions, not stored bases.
    rows=[]
    for n in (4,5,6):
        N=n*n
        def columns(omit=None):
            for cubic in mons(N,3):
                out={}
                for a in set(cubic):
                    if a==omit: continue
                    rest=list(cubic); rest.remove(a); x,y=rest
                    i,j=divmod(x,n); k,l=divmod(y,n)
                    if i==k or j==l:
                        label=(0,x,y); sign=1
                    else:
                        label=(1,min(i,k),max(i,k),min(j,l),max(j,l))
                        sign=1 if (i-k)*(j-l)>0 else -1
                    out[(a,)+label]=cubic.count(a)*sign
                yield out
        dimension=comb(N+2,3)-rank(columns())
        require(dimension==comb(n,3)**2,('permanent prolongation',n,dimension))
        detail={'n':n,'cubic_monomials':comb(N+2,3),'prolongation_dimension':dimension}
        if n==4:
            missing=[comb(N+2,3)-rank(columns(a)) for a in range(N)]
            require(missing==[17]*16,('missing-coordinate dimensions',missing))
            detail['missing_coordinate_dimensions']=missing
        rows.append(detail)
    return rows

def actual_three_dimensional_intersection():
    # Six variables in a 2-by-3 rectangle; these are the actual E2 intersection.
    n=6; U=[{I:1} for I in combinations(range(n),3)]
    R=[{(0,4):1,(1,3):1},{(0,5):1,(2,3):1},{(1,5):1,(2,4):1}]
    require(rank(R)==3,'actual three-dimensional intersection')
    rng=random.Random(6162026); cases=0; minimum={}
    for d in range(7):
        Ps=[[[int(j==i) for j in range(n)] for i in I] for I in combinations(range(n),d)]
        Ps += [quotient(n,d,rng,1) for _ in range(24)]
        values=[]
        for P in Ps:
            r=symbol_rank(U,R,P,n)
            require(3*r>=10*d,('actual six-variable symbol',d,P,r))
            values.append(r); cases+=1
        minimum[str(d)]=min(values)
    require(minimum['6']==20,'actual full symbol must be injective')
    return {'actual_intersection_dimension':3,'quotient_cases':cases,'minimum_ranks':minimum,'full_rank':20}

def main():
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args()
    start=time.monotonic(); rng=random.Random(20261020)
    result={'proof_premise':False,'implementation':'fresh exact sparse linear algebra over Q; no project imports'}
    for name,fn in [('permanent_prolongations',permanent_prolongations),('actual_sextic_intersection',actual_three_dimensional_intersection),('quartic',quartic_quotient_checks),('squarefree',squarefree_checks),('negative_controls',negative_controls),('sextic_completion',five_span_sextics),('quintic_local',lambda:local_product_checks(5,rng)),('sextic_local',lambda:local_product_checks(6,rng))]:
        print('RUN',name,flush=True); result[name]=fn(); print('PASS',name,json.dumps(result[name]),flush=True)
    result['elapsed_seconds']=round(time.monotonic()-start,3); result['status']='PASS'
    args.output.write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
    print('INDEPENDENT_CHECKS_PASS',result['elapsed_seconds'],flush=True)
if __name__=='__main__': main()
