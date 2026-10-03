"""MVA Track 2 extension 1.0.0. Public-data analyses; no therapeutic efficacy claim."""
from pathlib import Path
import sys, os, json, hashlib, itertools, math, warnings, time, traceback, re, gzip, shutil
from datetime import datetime, timezone
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

VERSION = '1.0.0'
SEED = 20260925
MIN_GENES = 5
MIN_COVERAGE = 0.50
EFFECT_BOUND = 0.10

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def dump(path, obj):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name(path.name + '.part')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2, allow_nan=False), encoding='utf-8')
    tmp.replace(path)

def csv(df, path, index=False):
    path = Path(path); path.parent.mkdir(parents=True, exist_ok=True)
    raw=df.to_csv(index=index).encode('utf-8')
    data=gzip.compress(raw,mtime=0) if path.suffix=='.gz' else raw
    tmp=path.with_name(path.name+'.part')
    with tmp.open('wb') as handle:
        handle.write(data); handle.flush(); os.fsync(handle.fileno())
    tmp.replace(path)
    if sha(path)!=hashlib.sha256(data).hexdigest():raise IOError('Output write verification failed: '+str(path))

def bh(values):
    a = np.asarray(values, float); out = np.full(len(a), np.nan)
    good = np.flatnonzero(np.isfinite(a))
    order = good[np.argsort(a[good])]
    if len(order):
        out[order] = np.minimum(1, np.minimum.accumulate((a[order] * len(order) / np.arange(1,len(order)+1))[::-1])[::-1])
    return out

def soft_records(path):
    records=[]; current=None
    for line in Path(path).read_text().splitlines():
        if line.startswith('^SAMPLE = '):
            current={'gsm': line.split(' = ',1)[1]}; records.append(current)
        elif current is not None and line.startswith('!Sample_') and ' = ' in line:
            k,v=line.split(' = ',1); current.setdefault(k[8:],[]).append(v)
    if not records: raise ValueError('No GSM records: '+str(path))
    return records

def characteristics(r):
    return dict(x.split(': ',1) for x in r.get('characteristics_ch1',[]) if ': ' in x)

def validate_counts(c):
    if not c.index.is_unique or not c.columns.is_unique: raise ValueError('Duplicate count identifiers')
    v=c.to_numpy(dtype=float)
    if not np.isfinite(v).all() or (v<0).any() or not np.equal(v,np.floor(v)).all():
        raise ValueError('Input is not finite, non-negative integer raw counts')
    if (c.sum(axis=1)<=0).any(): raise ValueError('Empty library')
    return c.astype('int64')

def reference(root):
    r=json.loads((root/'inputs/reference.json').read_text())
    o=pd.read_csv(root/'inputs/orthology_1to1.csv', keep_default_na=False)
    for col in ['human_id','mouse_id','mouse_symbol']:
        if not o[col].is_unique: raise ValueError('Orthology is not strict one-to-one: '+col)
    return r,o

def qc(c, meta, folder):
    folder.mkdir(parents=True, exist_ok=True)
    q=meta.copy(); q['library_size']=c.sum(axis=1); q['genes_nonzero']=(c>0).sum(axis=1)
    csv(q,folder/'sample_qc.csv',True)
    z=np.log2(c.div(c.sum(axis=1),axis=0)*1e6+0.5)
    z=z.loc[:,z.var()>0]; z=z.loc[:,z.var().nlargest(min(2000,z.shape[1])).index]
    x=z.to_numpy(); x=x-x.mean(axis=0)
    u,s,_=np.linalg.svd(x,full_matrices=False); pcs=u[:,:2]*s[:2]
    fig,ax=plt.subplots(figsize=(8,5))
    for group in sorted(meta['condition'].unique()):
        ids=np.flatnonzero(meta['condition'].to_numpy()==group)
        ax.scatter(pcs[ids,0],pcs[ids,1],label=group,s=55)
        for i in ids: ax.annotate(str(meta.index[i]),pcs[i],fontsize=5,alpha=.7)
    var=s*s/(s*s).sum(); ax.set(xlabel=f'PC1 ({var[0]:.1%})',ylabel=f'PC2 ({var[1]:.1%})',title='QC only: log2 CPM, 2000 variable genes')
    ax.legend(fontsize=7);fig.tight_layout();fig.savefig(folder/'pca.png',dpi=160);plt.close(fig)

def fit_de(c, meta, design, folder):
    from pydeseq2.dds import DeseqDataSet
    from pydeseq2.default_inference import DefaultInference
    from pydeseq2.ds import DeseqStats
    folder.mkdir(parents=True,exist_ok=True)
    meta=meta.loc[c.index].copy()
    import inspect, importlib.metadata as im
    fingerprint=hashlib.sha256(c.to_numpy().tobytes()+c.index.to_series().to_csv().encode()+
        c.columns.to_series().to_csv().encode()+meta.to_csv().encode()+design.encode()+
        inspect.getsource(fit_de).encode()+im.version('pydeseq2').encode()).hexdigest()
    stamp=folder/'FIT_COMPLETE.json'
    if stamp.exists():
        saved=json.loads(stamp.read_text())
        if saved.get('fingerprint')==fingerprint and all((folder/k).is_file() and sha(folder/k)==v for k,v in saved['files'].items()):
            print('  Reusing verified gene model:',folder.name,flush=True)
            return pd.read_csv(folder/'log2_normalized.csv.gz',index_col=0).T, pd.read_csv(folder/'gene_DE.csv.gz',index_col=0)
    nmin=int(meta['condition'].value_counts().min())
    keep=(c>=10).sum(axis=0)>=nmin
    if keep.sum()<500: raise ValueError('Too few expressed genes for stable normalization')
    inference=DefaultInference(n_cpus=1)
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter('always')
        dds=DeseqDataSet(counts=c.loc[:,keep], metadata=meta, design=design,
                        refit_cooks=True, inference=inference, quiet=True)
        dds.deseq2()
        ds=DeseqStats(dds, contrast=['condition','case','control'], inference=inference, quiet=True)
        ds.summary()
    (folder/'model_warnings.txt').write_text('\n'.join(sorted(set(str(w.message) for w in caught))))
    de=ds.results_df.copy();de.index.name='gene_id';csv(de,folder/'gene_DE.csv.gz',True)
    # Size factors fitted on all expressed genes; never on the selected modules alone.
    log=pd.DataFrame(np.log2(dds.layers['normed_counts']+0.5),index=c.index,columns=c.columns[keep])
    csv(meta,folder/'samples.csv',True)
    csv(log.T,folder/'log2_normalized.csv.gz',True)
    dump(folder/'model.json',{'design':design,'n_samples':len(c),'n_genes_input':c.shape[1],
         'n_genes_tested':int(keep.sum()),'min_count':10,'min_samples':nmin,
         'gene_FDR_scope':'BH within this contrast; DESeq2 independent filtering and Cook filtering',
         'warning_count':len(caught),'LFC':'unshrunk case/control',
         'module_normalization':'fixed DESeq2 size factors estimated using all expressed genes'})
    dump(stamp,{'fingerprint':fingerprint,'files':{k:sha(folder/k) for k in
        ['gene_DE.csv.gz','samples.csv','log2_normalized.csv.gz','model.json','model_warnings.txt']}})
    return log,de

def scalar_test(values, meta, paired=False):
    a=np.asarray(values,float)
    if paired:
        frame=meta[['individual','condition']].copy();frame['score']=a
        w=frame.pivot(index='individual',columns='condition',values='score')
        if w[['case','control']].isna().any().any():raise ValueError('Incomplete pair passed to test')
        d=(w['case']-w['control']).to_numpy(); n=len(d); effect=float(d.mean())
        se=float(stats.sem(d)); crit=float(stats.t.ppf(.975,n-1))
        null=np.array([np.mean(d*np.asarray(s)) for s in itertools.product([-1,1],repeat=n)])
        p=float(np.mean(np.abs(null)>=abs(effect)-1e-12))
        loo=np.array([np.delete(d,i).mean() for i in range(n)]) if n>1 else np.array([np.nan])
        return {'effect_log2':effect,'ci_low':effect-crit*se,'ci_high':effect+crit*se,
                'p_exact':p,'n_units_case':n,'n_units_control':n,'n_permutations':len(null),
                'loo_min':float(loo.min()),'loo_max':float(loo.max()),'test':'paired exact sign-flip; assumes symmetric differences; no placebo'}
    case=meta['condition'].to_numpy()=='case';x=a[case];y=a[~case]
    effect=float(x.mean()-y.mean());vx=x.var(ddof=1)/len(x);vy=y.var(ddof=1)/len(y)
    se=math.sqrt(vx+vy); df=(vx+vy)**2/(vx*vx/(len(x)-1)+vy*vy/(len(y)-1)) if vx+vy>0 else len(a)-2
    crit=float(stats.t.ppf(.975,df));null=[]
    for ids in itertools.combinations(range(len(a)),len(x)):
        mask=np.zeros(len(a),bool);mask[list(ids)]=True
        null.append(a[mask].mean()-a[~mask].mean())
    p=float(np.mean(np.abs(null)>=abs(effect)-1e-12))
    loo=[np.delete(x,i).mean()-y.mean() for i in range(len(x))]+[x.mean()-np.delete(y,i).mean() for i in range(len(y))]
    return {'effect_log2':effect,'ci_low':effect-crit*se,'ci_high':effect+crit*se,
            'p_exact':p,'n_units_case':len(x),'n_units_control':len(y),'n_permutations':len(null),
            'loo_min':float(min(loo)),'loo_max':float(max(loo)),'test':'exact label permutation conditional on normalization; exchangeability assumption'}

def module_tests(log, meta, ref, contrast, folder, paired=False):
    rows=[];scores=[]
    for name, definition in ref['modules'].items():
        target=set(definition['human_ids']); genes=sorted(target.intersection(log.columns))
        row={'contrast':contrast,'module':name,'family':definition['family'],
             'n_target':len(target),'n_measured':len(genes),'coverage':len(genes)/len(target) if target else 0,
             'genes_human_ensembl':';'.join(genes)}
        if len(genes)<MIN_GENES or row['coverage']<MIN_COVERAGE:
            row['status']='INSUFFICIENT_COVERAGE'
        else:
            vals=log[genes].mean(axis=1);row.update(scalar_test(vals,meta,paired))
            row['status']='ESTIMATED'
            row['loo_stable_above_bound']=bool(row['loo_min']>EFFECT_BOUND or row['loo_max']<-EFFECT_BOUND)
            for sample,value in vals.items(): scores.append({'contrast':contrast,'module':name,'sample':sample,'score':value})
        rows.append(row)
    csv(pd.DataFrame(scores),folder/'module_sample_scores.csv')
    return pd.DataFrame(rows)

def adjust_modules(df):
    df=df.copy(); df['q_family_all_contrasts']=np.nan
    for family in df.family.unique():
        ix=df.index[df.family==family]
        df.loc[ix,'q_family_all_contrasts']=bh(df.loc[ix,'p_exact'])
    df['FDR_signal']=(df.q_family_all_contrasts<=.05)&df.loo_stable_above_bound.fillna(False)
    return df

def heatmap(df,path,title):
    p=df.pivot(index='module',columns='contrast',values='effect_log2')
    vals=p.to_numpy(); lim=max(.2,float(np.nanmax(np.abs(vals))))
    fig,ax=plt.subplots(figsize=(max(8,len(p.columns)*1.45),max(6,len(p)*.32)))
    im=ax.imshow(np.ma.masked_invalid(vals),aspect='auto',cmap='RdBu_r',vmin=-lim,vmax=lim)
    ax.set_xticks(range(len(p.columns)),p.columns,rotation=45,ha='right',fontsize=7)
    ax.set_yticks(range(len(p)),p.index,fontsize=7);ax.set_title(title,fontsize=10)
    fig.colorbar(im,ax=ax,label='Mean gene log2 difference (expression, not pathway activity)')
    fig.tight_layout();fig.savefig(path,dpi=170);plt.close(fig)

def nb11(root, config):
    ref,orth=reference(root)
    resolution=pd.read_csv(root/'inputs/mouse_symbol_resolution.csv',keep_default_na=False)
    valid=resolution[resolution.human_id!='']
    mapping=dict(zip(valid.source_symbol,valid.human_id))
    all_rows=[]; registry=[]
    for series in ['GSE134780','GSE134781']:
        raw=pd.read_csv(root/f'inputs/{series}_counts.txt.gz',sep='\t',index_col=0)
        c=validate_counts(raw.T)
        records={r['title'][0]:r for r in soft_records(root/f'inputs/{series}_gsm.soft')}
        if set(c.index)!=set(records):raise ValueError('GEO sample title / count mismatch')
        data=[]
        for sample in c.index:
            mt=re.fullmatch(r'(10mo|3mo)_(skM|fat)_(WT|HL1002P|HH|hetL1002P|hetX753)_(\d+)',sample)
            if not mt:raise ValueError('Unexpected sample title '+sample)
            ch=characteristics(records[sample])
            data.append({'sample':sample,'gsm':records[sample]['gsm'],'age_title':mt[1],
                         'tissue':mt[2],'genotype':mt[3],'replicate_label':mt[4],
                         'author_genotype':ch.get('genotype',''),'author_age':ch.get('age',''),
                         'condition':mt[3]})
        meta=pd.DataFrame(data).set_index('sample');csv(meta,root/f'{series}_metadata.csv',True)
        qc(c,meta,root/'qc'/series)
        for tissue in meta.tissue.unique():
            for genotype in sorted(set(meta.loc[meta.tissue==tissue,'genotype'])-{'WT'}):
                cid=f'{series}_{tissue}_{genotype}_vs_WT'
                folder=root/'contrasts'/cid
                sub=meta.loc[(meta.tissue==tissue)&meta.genotype.isin(['WT',genotype])].copy()
                sub['condition']=np.where(sub.genotype==genotype,'case','control')
                print('NB11 fitting',cid,'n=',sub.condition.value_counts().to_dict(),flush=True)
                log,de=fit_de(c.loc[sub.index],sub,'~condition',folder)
                gene_mapping=pd.Series({x:mapping.get(x,'') for x in c.columns})
                duplicate=gene_mapping.ne('') & gene_mapping.duplicated(keep=False)
                safe_symbols=gene_mapping.index[gene_mapping.ne('') & ~duplicate]
                mapped=log.loc[:,log.columns.isin(safe_symbols)].rename(columns=mapping)
                if not mapped.columns.is_unique:raise ValueError('Ambiguous ortholog projection')
                csv(mapped.T,folder/'human_ortholog_log2.csv.gz',True)
                all_rows.append(module_tests(mapped,sub,ref,cid,folder))
                # Sensitivity uses the original NB02 no-IEA gene sets, never a post-hoc set.
                noiea={'modules':{k:{**v,'human_ids':v.get('human_ids_noIEA',v['human_ids'])} for k,v in ref['modules'].items()}}
                sen=module_tests(mapped,sub,noiea,cid,folder/'noIEA')
                csv(sen,folder/'noIEA_sensitivity.csv')
                registry.append({'contrast':cid,'series':series,'tissue':tissue,'genotype':genotype,
                                 'log_file':str((folder/'human_ortholog_log2.csv.gz').relative_to(root)),
                                 'metadata_file':str((folder/'samples.csv').relative_to(root))})
                audit=resolution.set_index('source_symbol').reindex(c.columns).rename_axis('mouse_symbol').reset_index()
                audit['duplicate_target_excluded']=audit.mouse_symbol.isin(gene_mapping.index[duplicate])
                audit['expression_filter_pass']=audit.mouse_symbol.isin(log.columns)
                csv(audit,folder/'orthology_coverage.csv')
    effects=adjust_modules(pd.concat(all_rows,ignore_index=True));csv(effects,root/'NB11_MODULE_EFFECTS.csv')
    heatmap(effects,root/'NB11_MODULE_EFFECTS.png','NB11: genotype- and tissue-specific expression effects')
    h=pd.read_csv(root/'inputs/GSE277997_H_v_WT.csv.gz')
    if not {'gene','log2FC','pvalue','padj'}.issubset(h.columns):raise ValueError('Heart is a DE table, unexpected schema')
    if h.gene.duplicated().any():raise ValueError('Duplicate heart gene identifiers')
    h['human_id']=h.gene.map(mapping)
    dup=h.human_id.notna() & h.human_id.duplicated(keep=False)
    h['duplicate_target_excluded']=dup;h.loc[dup,'human_id']=np.nan
    csv(h,root/'NB11_HEART_AUTHOR_DE_MAPPED.csv.gz')
    heart=[]
    for name,v in ref['modules'].items():
        ss=h.loc[h.human_id.isin(v['human_ids'])]
        heart.append({'module':name,'n_genes':len(ss),'median_author_log2FC':ss.log2FC.median(),
                      'n_author_gene_padj_lt05':int((ss.padj<.05).sum()),
                      'module_pvalue':np.nan,'interpretation':'descriptive author DE only; no sample-level module test'})
    csv(pd.DataFrame(heart),root/'NB11_HEART_DESCRIPTIVE.csv')
    decisions=[]
    for name,g in effects.groupby('module'):
        sig=g[g.FDR_signal]
        if (g.status=='INSUFFICIENT_COVERAGE').all():state='INSUFFICIENT_COVERAGE'
        elif len(sig):state='MODEL_SPECIFIC_FDR_SIGNAL'
        else:state='NO_FDR_SUPPORTED_SIGNAL'
        decisions.append({'module':name,'status':state,'FDR_contrasts':sig.contrast.tolist(),
                          'independent_replication_claim':False})
    handoff={'schema':'MVA_NB11_HANDOFF_1.0','reference_sha256':sha(root/'inputs/reference.json'),
             'mouse_symbol_resolution_sha256':sha(root/'inputs/mouse_symbol_resolution.csv'),
             'orthology_sha256':sha(root/'inputs/orthology_1to1.csv'),'contrasts':registry,'decisions':decisions,
             'scope':'Related mouse models; not the child genotype. Shared controls are not independent replication.'}
    dump(root/'NB11_HANDOFF.json',handoff)
    report=['# NB11 — wynik wykonania','',f'Wykonano {len(registry)} kontrastów; genowy PyDESeq2 i dokładne testy modułów na poziomie próbek.',
            f'Moduły z FDR <= 0.05 i stabilnym efektem > {EFFECT_BOUND}: {int(effects.FDR_signal.sum())} kontrastów modułowych.',
            '','Nie jest to pomiar funkcji mitochondriów, NAD+, SIRT2 ani skuteczności terapii. Nie opisujemy wspólnych kontroli jako niezależnych replikacji.',
            'Brak FDR-supported signal przy małych n nie dowodzi braku efektu. Przedziały t/Welcha są przybliżone; permutacje warunkują na oszacowanej normalizacji.',
            'Serce: wyłącznie opis wyników autorów; nie wykonano ponownego DE z tabeli log2FC.',
            'L1002P u myszy nie jest ludzkim N1002K. Różnice wieku, tkanki, allelu i składu komórek ograniczają transfer.',
            '', '## Decyzje modułowe']
    report += ['- '+x['module']+': '+x['status'] for x in decisions]
    (root/'RESULT_SUMMARY.md').write_text('\n'.join(report),encoding='utf-8')

def nb12(root,config):
    from Bio import SeqIO
    record=SeqIO.read(root/'inputs/BUB1B_NM_001211.6.gb','genbank')
    feat=[f for f in record.features if f.type=='CDS']
    if len(feat)!=1:raise ValueError('Expected one CDS in versioned RefSeq')
    feature=feat[0];cds=feature.extract(record.seq);protein=str(cds.translate(to_stop=True))
    up=SeqIO.read(root/'inputs/BUB1B_O60566.fasta','fasta')
    if record.id!='NM_001211.6' or protein!=str(up.seq) or len(protein)!=1050:
        raise ValueError('RefSeq / UniProt canonical sequence mismatch')
    if str(cds[-3:]) not in ['TAA','TAG','TGA'] or len(cds)!=3153:
        raise ValueError('Unexpected CDS / stop codon')
    if protein[736]!='L' or protein[1001]!='N':raise ValueError('Protein reference residues do not match reported labels')
    (root/'BUB1B_verified_CDS.fasta').write_text(f'>{record.id}|CDS|{feature.qualifiers.get("protein_id",[""])[0]}\n{cds}\n')
    (root/'BUB1B_verified_protein.fasta').write_text(f'>{up.id}\n{protein}\n')
    dump(root/'REFERENCE_AUDIT.json',{'transcript':record.id,'protein_refseq':feature.qualifiers.get('protein_id'),
        'cds_start_1based':int(feature.location.start)+1,'cds_end_1based':int(feature.location.end),
        'cds_length_with_stop':len(cds),'amino_acids':len(protein),'uniprot_match':True,
        'source_sha256':{p.name:sha(p) for p in (root/'inputs').glob('BUB1B*')}})
    budgets=[]
    # Explicit design envelopes: lengths below are assumptions, not validated promoter constructs.
    for promoter in [250,500,800,1200]:
        for utr in [100,250]:
            for polyA in [100,250]:
                total=2*145+len(cds)+promoter+utr+polyA
                budgets.append({'promoter_nt_assumed':promoter,'UTR_total_nt_assumed':utr,
                    'polyA_nt_assumed':polyA,'ITR_total_nt':290,'CDS_nt':len(cds),'WPRE_nt':0,
                    'total_nt':total,'capacity_nt_assumed':4700,'remaining_nt':4700-total,
                    'fits_size_envelope':total<=4700,'validated_construct':False})
    b=pd.DataFrame(budgets);csv(b,root/'AAV_PAYLOAD_ENVELOPES.csv')
    fig,ax=plt.subplots(figsize=(8,4))
    for (u,p),g in b.groupby(['UTR_total_nt_assumed','polyA_nt_assumed']):
        ax.plot(g.promoter_nt_assumed,g.remaining_nt,marker='o',label=f'UTR={u}, polyA={p} nt')
    ax.axhline(0,color='black',ls='--');ax.set(xlabel='Assumed promoter length (nt)',ylabel='Remaining space (nt)',title='ssAAV capacity arithmetic; delivery and expression unvalidated')
    ax.legend(fontsize=8);fig.tight_layout();fig.savefig(root/'AAV_PAYLOAD_ENVELOPES.png',dpi=160);plt.close(fig)
    csv(pd.DataFrame([
        ['Endogenous allele correction','potentially durable in edited progenitors','exact variant, phase, cell delivery, editing and off-target validation','CONDITIONAL'],
        ['WT cDNA / ssAAV','CDS fits some regulatory size envelopes','division-related dilution, tissue delivery, expression timing and dose','SIZE_ONLY_FEASIBLE'],
        ['WT mRNA','transient biological rescue benchmark','delivery efficiency and repeated expression; no durable correction','PRECLINICAL_REFERENCE'],
        ['CRISPRa','may increase transcription of existing allele','requires allele with useful function; could amplify dysfunctional protein','FUNCTION_DEPENDENT'],
        ['XIST chromosome silencing','not evaluated as a BUB1B restoration route','heterogeneous aneuploidies and chromosome-wide dosage consequences','NOT_PRIORITIZED']],
        columns=['modality','potential_advantage','unresolved_requirements','status']),root/'MODALITY_COMPARISON.csv')
    # Optional exact cDNA substitutions are local-only inputs. No variant is guessed from a protein label.
    template={'reference_transcript':'NM_001211.6','phase':'UNRESOLVED','variants':[],
        'example_schema_only':{'id':'local_label','cdna_position_1based':None,'ref':None,'alt':None,'verified_source':None},
        'note':'Supply verified single-nucleotide cDNA substitutions only. No genomic liftOver or phase inference.'}
    dump(root/'VARIANTS_TEMPLATE.json',template)
    user=config.get('variant_json_path','')
    variant_rows=[]
    if user:
        v=json.loads(Path(user).read_text())
        if v.get('reference_transcript')!=record.id:raise ValueError('Variant transcript must exactly match versioned RefSeq')
        for a in v.get('variants',[]):
            pos=int(a['cdna_position_1based']);ref=a['ref'].upper();alt=a['alt'].upper()
            if len(ref)!=1 or len(alt)!=1 or ref==alt or ref not in 'ACGT' or alt not in 'ACGT':
                raise ValueError('This audit supports single-nucleotide substitutions only')
            if not 1<=pos<=len(cds) or str(cds[pos-1])!=ref:raise ValueError('Variant reference nucleotide mismatch')
            if not a.get('verified_source'):raise ValueError('Record the local source used to verify each variant')
            mut=str(cds)[:pos-1]+alt+str(cds)[pos:];i=(pos-1)//3
            from Bio.Seq import Seq
            aa_ref=str(cds[i*3:i*3+3].translate());aa_alt=str(Seq(mut[i*3:i*3+3]).translate())
            correction=alt+'>'+ref
            classical='ABE chemistry-compatible on one strand' if correction in ['A>G','T>C'] else 'CBE chemistry-compatible on one strand' if correction in ['C>T','G>A'] else 'not a classical ABE/CBE single-base conversion'
            variant_rows.append({'variant_id':a.get('id',''),'c_position':pos,'ref':ref,'alt':alt,
                'protein_position':i+1,'protein_ref':aa_ref,'protein_alt':aa_alt,
                'correction_change':correction,'chemistry_class':classical,
                'guide_PAM_editing_window_bystanders':'NOT_EVALUATED','off_target':'NOT_EVALUATED',
                'phase':v.get('phase','UNRESOLVED'),'status':'CHEMISTRY_ONLY_NOT_EDITABILITY'})
    columns=['variant_id','c_position','ref','alt','protein_position','protein_ref','protein_alt','correction_change','chemistry_class','guide_PAM_editing_window_bystanders','off_target','phase','status']
    csv(pd.DataFrame(variant_rows,columns=columns),root/'VARIANT_CHEMISTRY_AUDIT.csv')
    gate='COMPLETED_CHEMISTRY_ONLY' if variant_rows else 'NOT_RUN_NO_VERIFIED_CDNA_VARIANTS'
    dump(root/'NB12_HANDOFF.json',{'schema':'MVA_NB12_HANDOFF_1.0','sequence_audit':'PASS',
        'payload_audit':'COMPLETED_DESIGN_ENVELOPES_ONLY','variant_audit':gate,
        'delivery':'UNVALIDATED','clinical_readiness':False,'partial_correction_threshold':'NOT_ESTIMATED'})
    (root/'RESULT_SUMMARY.md').write_text('\n'.join([
        '# NB12 — wynik wykonania','',f'RefSeq {record.id}: {len(cds)} nt CDS, {len(protein)} aa; zgodność z UniProt O60566.',
        'Pozostaje 1257 nt na wszystkie pozostałe elementy poza CDS i ITR przy założonym limicie 4700 nt.',
        f'Z {len(b)} jawnie hipotetycznych konfiguracji długości {int(b.fits_size_envelope.sum())} mieści się w budżecie.',
        'To nie są zaprojektowane ani zwalidowane sekwencje promotorów/wektorów. Nie zawierają WPRE.',
        'Pełne BUB1B nie mieści się w typowym budżecie self-complementary AAV; tabela dotyczy ssAAV.',
        f'Audyt wariantów: {gate}. Brak dokładnych wariantów nie blokuje audytu sekwencji i pojemności.',
        'Nie wyznaczono guide RNA, okna edycji, efektów ubocznych edycji ani bezpieczeństwa.',
        'W dzielących się komórkach trwałość AAV wymaga osobnego dowodu. BUBR1 działa wewnątrzkomórkowo.',
        'Nie oszacowano odsetka komórek potrzebnego do terapii. Brak danych do kalibracji takiego progu.',
        'Ograniczenie nowych błędów nie naprawia automatycznie istniejącej aneuploidii ani następstw rozwojowych.']),encoding='utf-8')

def niacin_metadata(root, columns):
    rows=[]
    for r in soft_records(root/'inputs/GSE129811_gsm.soft'):
        candidates=[x for x in r.get('description',[]) if re.fullmatch(r'AWVM\d+_[CP]\d+',x)]
        if len(candidates)!=1:raise ValueError('Ambiguous AWVM-to-GSM match')
        ch=characteristics(r);individual=ch.get('individual','')
        if not re.fullmatch(r'(Control|Patient)\d+',individual):raise ValueError('Unknown donor '+individual)
        month=int(re.fullmatch(r'(\d+) months?',ch['time'])[1])
        group='patient' if individual.startswith('Patient') else 'control'
        rows.append({'sample':candidates[0],'gsm':r['gsm'],'individual':individual,'month':month,
                     'group':group,'condition':group+'_'+str(month),'author_genotype':ch.get('genotype','')})
    meta=pd.DataFrame(rows).set_index('sample')
    if not meta.index.is_unique or set(meta.index)!=set(columns):raise ValueError('Count/GSM library mapping is not bijective')
    if meta.duplicated(['individual','month']).any():raise ValueError('Duplicate donor-timepoint')
    meta=meta.loc[columns];csv(meta,root/'GSE129811_SAMPLE_CROSSWALK.csv',True)
    return meta

def verify_completed_run(path):
    path=Path(path).resolve();m=json.loads((path/'RUN_MANIFEST.json').read_text())
    if m.get('status')!='COMPLETED':raise ValueError('Upstream run is not complete')
    if json.loads((path/'RUN_STATUS.json').read_text()).get('status')!='COMPLETED':
        raise ValueError('Run status does not confirm completion')
    for rel,digest in m['files'].items():
        p=(path/rel).resolve()
        if not p.is_relative_to(path) or not p.is_file() or sha(p)!=digest:
            raise ValueError('Upstream checksum mismatch: '+rel)
    return m

def nb13(root,config):
    ref,orth=reference(root)
    raw=pd.read_csv(root/'inputs/GSE129811_AWVM29samples.HTSeq.counts.tsv.gz',sep='\t')
    if raw.GeneID.duplicated().any():raise ValueError('Duplicate human Ensembl IDs')
    c=validate_counts(raw.drop(columns=['GeneName']).set_index('GeneID').T)
    meta=niacin_metadata(root,c.index);qc(c,meta,root/'qc'/'niacin')
    all_rows=[];paired_data={};pair_audit=[]
    for group,month in [('patient',4),('patient',10),('control',4)]:
        cid=f'{group}_{month}m_vs_0m'
        selected=meta[(meta.group==group)&meta.month.isin([0,month])].copy()
        eligible=selected.groupby('individual').month.apply(lambda x:set(x)=={0,month})
        donors=eligible[eligible].index
        for individual in meta.loc[meta.group==group,'individual'].unique():
            pair_audit.append({'contrast':cid,'individual':individual,'complete_pair':individual in donors,
                               'reason':'included' if individual in donors else 'missing one of required timepoints'})
        sub=selected[selected.individual.isin(donors)].copy()
        sub['condition']=np.where(sub.month==month,'case','control')
        if len(donors)<3:raise ValueError('Fewer than 3 complete donor pairs in '+cid)
        print('NB13 fitting',cid,'complete pairs',len(donors),flush=True)
        folder=root/'contrasts'/cid
        log,de=fit_de(c.loc[sub.index],sub,'~individual + condition',folder)
        all_rows.append(module_tests(log,sub,ref,cid,folder,True))
        paired_data[cid]=(log,sub)
    csv(pd.DataFrame(pair_audit),root/'NB13_COMPLETE_PAIRS.csv')
    effects=adjust_modules(pd.concat(all_rows,ignore_index=True));csv(effects,root/'NB13_MODULE_EFFECTS.csv')
    heatmap(effects,root/'NB13_MODULE_EFFECTS.png','NB13: paired niacin/time-associated expression changes; no placebo')
    # Baseline disease comparison: equal-weight matched patients, never treat their multiple controls as patients.
    match_text=(root/'inputs/GSE129811_Readme_PatientControlMatching.txt').read_text()
    baseline=[]
    # Frozen author matching is a separate auditable reference; no numeric-ID guessing.
    matching=ref['niacin_patient_control_matching']
    base=meta[meta.month==0]
    size_c=c.loc[base.index]
    from pydeseq2.preprocessing import deseq2_norm
    normalized,_=deseq2_norm(size_c.to_numpy())
    bl=pd.DataFrame(np.log2(normalized+0.5),index=size_c.index,columns=size_c.columns)
    for name,v in ref['modules'].items():
        genes=sorted(set(v['human_ids']).intersection(bl.columns))
        expressed=(size_c[genes]>=10).sum()>=min(3,len(size_c))
        genes=expressed[expressed].index.tolist()
        if len(genes)<MIN_GENES:continue
        vals=bl[genes].mean(axis=1)
        for patient,controls in matching.items():
            pp=base.index[base.individual==patient];cc=base.index[base.individual.isin(controls)]
            if len(pp)!=1 or len(cc)==0:continue
            baseline.append({'module':name,'patient':patient,'n_matched_controls':len(cc),
                'baseline_difference_log2':float(vals.loc[pp].iloc[0]-vals.loc[cc].mean()),'n_genes':len(genes)})
    csv(pd.DataFrame(baseline),root/'NB13_BASELINE_MATCHED_DESCRIPTIVE.csv')
    # Composition and proliferation sensitivity: descriptive markers, not an identified deconvolution model.
    marker_sets=ref['composition_markers']
    sen=[]
    for cid,(log,sub) in paired_data.items():
        for name,genes in marker_sets.items():
            keep=sorted(set(genes).intersection(log.columns))
            if len(keep)>=2:
                row=scalar_test(log[keep].mean(axis=1),sub,True)
                sen.append({'contrast':cid,'marker_panel':name,'n_genes':len(keep),**row})
    csv(pd.DataFrame(sen),root/'NB13_COMPOSITION_SENSITIVITY.csv')
    integration='NOT_RUN_NB11_NOT_PROVIDED';alignment=[]
    upstream=config.get('nb11_run','')
    if upstream:
        up=Path(upstream);verify_completed_run(up)
        hand=json.loads((up/'NB11_HANDOFF.json').read_text())
        if hand['reference_sha256']!=sha(root/'inputs/reference.json') or hand['orthology_sha256']!=sha(root/'inputs/orthology_1to1.csv'):
            raise ValueError('NB11 and NB13 use different frozen modules/orthology')
        upstream_effects=pd.read_csv(up/'NB11_MODULE_EFFECTS.csv')
        for d in hand['contrasts']:
            if d['tissue']!='skM':continue
            mouse=pd.read_csv(up/d['log_file'],index_col=0).T
            mm=pd.read_csv(up/d['metadata_file'],index_col=0)
            for cid in ['patient_4m_vs_0m','patient_10m_vs_0m']:
                human,hm=paired_data[cid]
                for name,v in ref['modules'].items():
                    genes=sorted(set(v['human_ids']).intersection(mouse.columns).intersection(human.columns))
                    if len(genes)<MIN_GENES or len(genes)/len(v['human_ids'])<MIN_COVERAGE:continue
                    mr=scalar_test(mouse[genes].mean(axis=1),mm)
                    hr=scalar_test(human[genes].mean(axis=1),hm,True)
                    status='SMALL_OR_UNSTABLE_EFFECT'
                    stable=(mr['loo_min']>EFFECT_BOUND or mr['loo_max']<-EFFECT_BOUND) and (hr['loo_min']>EFFECT_BOUND or hr['loo_max']<-EFFECT_BOUND)
                    if stable: status='OPPOSITE_STABLE_DIRECTIONS' if mr['effect_log2']*hr['effect_log2']<0 else 'SAME_STABLE_DIRECTION'
                    u=upstream_effects[(upstream_effects.contrast==d['contrast'])&(upstream_effects.module==name)]
                    alignment.append({'mouse_contrast':d['contrast'],'niacin_contrast':cid,'module':name,
                        'n_identical_orthologs':len(genes),'mouse_effect_log2':mr['effect_log2'],
                        'niacin_effect_log2':hr['effect_log2'],'mouse_p_exact':mr['p_exact'],
                        'niacin_p_exact':hr['p_exact'],'direction_status':status,
                        'original_NB11_FDR_signal':bool(len(u) and bool(u.FDR_signal.iloc[0])),
                        'interpretation':'exploratory expression comparison; opposite direction is not rescue or synergy'})
        integration='COMPLETED_EXPLORATORY_ALIGNMENT'
    cols=['mouse_contrast','niacin_contrast','module','n_identical_orthologs','mouse_effect_log2','niacin_effect_log2','mouse_p_exact','niacin_p_exact','direction_status','original_NB11_FDR_signal','interpretation']
    csv(pd.DataFrame(alignment,columns=cols),root/'NB13_CROSS_MODEL_ALIGNMENT.csv')
    # No automatic pharmacological PASS is inferred from transcriptomic anti-correlation.
    gates=[
        ['niacin_nicotinic_acid','human muscle intervention data; indirect NAD+/SIRT2 rationale','NOT_TESTED_IN_MVA','UNKNOWN_TARGET_TISSUE_EXPOSURE','UNKNOWN_CURRENT_TRACK2_PRODUCT_ELIGIBILITY','CONDITIONAL_PRECLINICAL_CANDIDATE'],
        ['NAC','human aged-fibroblast redox/segregation data, 5 mM in vitro','NOT_TESTED_IN_BUB1B_MVA','UNKNOWN_RELEVANT_EXPOSURE','UNKNOWN_CURRENT_TRACK2_PRODUCT_ELIGIBILITY','COMPARATOR_ONLY']]
    csv(pd.DataFrame(gates,columns=['candidate','support','mechanism_gate','exposure_gate','product_gate','status']),root/'NB13_CANDIDATE_GATE_LEDGER.csv')
    dump(root/'NB13_HANDOFF.json',{'schema':'MVA_NB13_HANDOFF_1.0','paired_analysis':'COMPLETED',
        'NB11_integration':integration,'clean_rescue_proven':False,'synergy_proven':False,
        'clinical_recommendation':False,'patient_4m_complete_pairs':int((pd.DataFrame(pair_audit).query("contrast == 'patient_4m_vs_0m'").complete_pair).sum()),
        'gate_rule':'No automatic PASS. Existing NB09 and NB10 logic is not a biological efficacy validation.'})
    pairs=pd.DataFrame(pair_audit).groupby('contrast').complete_pair.sum().to_dict()
    (root/'RESULT_SUMMARY.md').write_text('\n'.join([
        '# NB13 — wynik wykonania','',f'Pełne pary dawców: {pairs}. 29 bibliotek nie oznacza 29 osób.',
        f'Integracja NB11: {integration}.',f'Kontrasty modułowe z FDR <= 0.05 i stabilnym efektem: {int(effects.FDR_signal.sum())}.',
        'Przy 3 parach minimalne dwustronne p sign-flip = 0.25; przy 4 parach = 0.125. Brak istotności nie rozstrzyga braku efektu.',
        'Dane są otwarte i bez placebo: czas, pobranie i niacyna nie są w pełni rozdzielone.',
        'Główny punkt: 4 miesiące. 10 miesięcy jest analizą wtórną na osobnym zestawie pełnych par.',
        'Porównanie międzygatunkowe wykorzystuje identyczny zestaw ortologów jeden-do-jednego w każdej parze modułowej.',
        'Przeciwne kierunki ekspresji nie dowodzą normalizacji, rescue ani synergii; sygnatury choroby mogą być kompensacyjne.',
        'NAD+ nie jest tu mierzone. RNA nie dowodzi aktywacji SIRT2, stabilizacji BUBR1 ani poprawy N1002K.',
        'Markery składu komórek są analizą opisową; małe n nie pozwala wiarygodnie odseparować wszystkich współzmiennych.',
        'Dla wybranego dodatku: kontrola / przywrócenie BUB1B / dodatek / kombinacja; osobno segregacja na zakończony podział i funkcja mitochondrialna.']),encoding='utf-8')

def finish(root,config,elapsed):
    import importlib.metadata as im
    versions={x:im.version(x) for x in ['numpy','pandas','scipy','matplotlib','pydeseq2','anndata','biopython']}
    dump(root/'RUNTIME.json',{'python':sys.version,'versions':versions,'elapsed_seconds':elapsed,'utc':datetime.now(timezone.utc).isoformat()})
    # Logs can still be open while the subprocess exits; exclude them from the immutable handoff.
    files={str(p.relative_to(root)):sha(p) for p in sorted(root.rglob('*')) if p.is_file() and p.name not in ['RUN_MANIFEST.json','RUN_STATUS.json','RESULTS.zip'] and p.suffix not in ['.log','.part']}
    dump(root/'RUN_MANIFEST.json',{'schema':'MVA_EXTENSION_RUN_1.0','notebook':config['notebook'],'version':VERSION,'status':'COMPLETED','files':files})
    dump(root/'RUN_STATUS.json',{'status':'COMPLETED','elapsed_seconds':elapsed})
    parent=Path(config['project_root'])/config['notebook']
    dump(parent/'latest_success.json',{'run_dir':str(root),'manifest_sha256':sha(root/'RUN_MANIFEST.json'),'notebook':config['notebook']})
    import zipfile
    with zipfile.ZipFile(root/'RESULTS.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in sorted(root.rglob('*')):
            if p.is_file() and p.name!='RESULTS.zip' and p.suffix not in ['.part','.log']:
                z.write(p,p.relative_to(root))

def main():
    root=Path(sys.argv[1]).resolve();config=json.loads((root/'config.json').read_text())
    start=time.monotonic()
    if (root/'RUN_MANIFEST.json').exists():
        try:
            verify_completed_run(root)
            print('Verified completed run; reusing saved outputs.',flush=True)
            return
        except Exception as exc:print('Saved run requires recomputation:',exc,flush=True)
    dump(root/'RUN_STATUS.json',{'status':'RUNNING'})
    (root/'ERROR_TRACEBACK.txt').unlink(missing_ok=True)
    try:
        for name,digest in config['input_hashes'].items():
            if sha(root/'inputs'/name)!=digest:raise ValueError('Frozen input checksum mismatch: '+name)
        {'NB11':nb11,'NB12':nb12,'NB13':nb13}[config['notebook']](root,config)
        finish(root,config,time.monotonic()-start)
        print((root/'RESULT_SUMMARY.md').read_text(),flush=True)
        print('COMPLETED:',root,flush=True)
    except BaseException as exc:
        dump(root/'RUN_STATUS.json',{'status':'FAILED','error':str(exc)})
        (root/'ERROR_TRACEBACK.txt').write_text(traceback.format_exc())
        raise

if __name__=='__main__':main()
