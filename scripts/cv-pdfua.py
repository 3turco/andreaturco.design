"""Rifinisce il PDF del CV stampato da Chrome perché rispetti PDF/UA-1.

Chrome tagga il contenuto ma lascia tre lacune:
- il contenuto con aria-hidden e gli sfondi CSS restano fuori da ogni tag:
  qui diventano artefatti (/Artifact);
- gli elementi di lista (LI) contengono NonStruct: qui diventano LBody;
- i metadati XMP non hanno titolo, lingua e identificativo PDF/UA.
Aggiunge anche una descrizione (/Contents) ai link.

Uso: python3 scripts/cv-pdfua.py public/cv-andrea-turco.pdf
Richiede pikepdf: python3 -m pip install pikepdf
"""
import sys

try:
    import pikepdf
except ImportError:
    sys.exit('Manca pikepdf. Installa con: python3 -m pip install pikepdf')

# Operatori che disegnano o costruiscono tracciati e testo.
DISEGNO = {
    'm', 'l', 'c', 'v', 'y', 'h', 're',
    'S', 's', 'f', 'F', 'f*', 'B', 'B*', 'b', 'b*', 'n', 'W', 'W*',
    'Tj', 'TJ', "'", '"', 'Do', 'sh', 'BI',
}
# Confini che una sequenza marcata non deve attraversare.
CONFINI = {'BT', 'ET', 'q', 'Q', 'BMC', 'BDC', 'EMC'}

DESCRIZIONI_LINK = {
    'tel:': 'Phone: ',
    'mailto:': 'Email: ',
}


def marca_artefatti(pdf, pagina):
    istruzioni = pikepdf.parse_content_stream(pagina)
    nuove = []
    profondita = 0
    aperto = False

    def chiudi():
        nonlocal aperto
        if aperto:
            nuove.append(pikepdf.ContentStreamInstruction([], pikepdf.Operator('EMC')))
            aperto = False

    for istruzione in istruzioni:
        immagine = isinstance(istruzione, pikepdf.ContentStreamInlineImage)
        nome = 'BI' if immagine else str(istruzione.operator)
        if nome in CONFINI:
            chiudi()
        if profondita == 0 and nome in DISEGNO and not aperto:
            nuove.append(pikepdf.ContentStreamInstruction(
                [pikepdf.Name('/Artifact')], pikepdf.Operator('BMC')))
            aperto = True
        nuove.append(istruzione)
        if nome in ('BMC', 'BDC'):
            profondita += 1
        elif nome == 'EMC':
            profondita -= 1
    chiudi()
    pagina.Contents = pdf.make_stream(pikepdf.unparse_content_stream(nuove))


def corpo_degli_elementi_lista(pdf, nodo, visti):
    """Ogni LI può contenere solo Lbl e LBody: NonStruct diventa LBody,
    gli altri figli (per esempio Link) finiscono dentro un LBody nuovo."""
    if not isinstance(nodo, pikepdf.Dictionary) or nodo.objgen in visti:
        return
    if nodo.objgen != (0, 0):
        visti.add(nodo.objgen)
    figli = nodo.get('/K')
    if isinstance(figli, pikepdf.Dictionary):
        figli = nodo.K = pikepdf.Array([figli])
    if not isinstance(figli, pikepdf.Array):
        return
    for indice, figlio in enumerate(list(figli)):
        if not isinstance(figlio, pikepdf.Dictionary) or '/S' not in figlio:
            continue
        if nodo.get('/S') == '/LI' and figlio.S not in ('/Lbl', '/LBody'):
            if figlio.S == '/NonStruct':
                figlio.S = pikepdf.Name('/LBody')
            else:
                corpo = pdf.make_indirect(pikepdf.Dictionary(
                    Type=pikepdf.Name('/StructElem'), S=pikepdf.Name('/LBody'),
                    P=nodo, K=pikepdf.Array([figlio])))
                figlio.P = corpo
                figli[indice] = corpo
        corpo_degli_elementi_lista(pdf, figlio, visti)


def descrivi_link(pagina):
    for annotazione in pagina.obj.get('/Annots', []):
        if annotazione.get('/Subtype') != '/Link' or '/Contents' in annotazione:
            continue
        uri = str(annotazione.get('/A', {}).get('/URI', ''))
        etichetta = 'Website: '
        for prefisso, testo in DESCRIZIONI_LINK.items():
            if uri.startswith(prefisso):
                etichetta, uri = testo, uri[len(prefisso):]
        annotazione.Contents = pikepdf.String(etichetta + uri.rstrip('/'))


def main(percorso):
    pdf = pikepdf.open(percorso, allow_overwriting_input=True)
    for pagina in pdf.pages:
        marca_artefatti(pdf, pagina)
        descrivi_link(pagina)
    corpo_degli_elementi_lista(pdf, pdf.Root.StructTreeRoot, set())

    titolo = str(pdf.docinfo.get('/Title', 'Andrea Turco – Curriculum Vitae'))
    pdf.docinfo['/Author'] = 'Andrea Turco'
    with pdf.open_metadata(set_pikepdf_as_editor=False) as xmp:
        xmp['dc:title'] = titolo
        xmp['dc:creator'] = ['Andrea Turco']
        xmp['dc:language'] = [str(pdf.Root.get('/Lang', 'en'))]
        xmp['pdfuaid:part'] = '1'
    pdf.save(percorso)
    print(f'PDF/UA: rifinito {percorso}')


if __name__ == '__main__':
    if len(sys.argv) != 2:
        sys.exit('Uso: python3 scripts/cv-pdfua.py <file.pdf>')
    main(sys.argv[1])
