---
title: "Admiral · Digital Wallet (legacy .md)"
description: "Sostituito da admiral-pay.mdx. Questo file è draft, non pubblicato."
year: 2023
role: "Lead Designer"
tags: ["deprecated"]
draft: true
---

Sostituito da `admiral-pay.mdx`. Questo file è impostato come draft e non viene pubblicato.

## Contesto

Admiral Pay è un istituto di pagamento digitale con oltre 40.000 rivenditori convenzionati sul territorio italiano. Sulla piattaforma passano carte prepagate, ricariche telefoniche, bollettini, pagoPA, bollo auto, gift card, biglietti per eventi, e operazioni di ricarica, deposito e prelievo sui conti gioco.

L'app esistente aveva accumulato problemi su più fronti: onboarding con tempo effettivo di 48-96 ore prima dell'attivazione dell'account, feature che non funzionavano più come previsto, codice stratificato, CRO bassa, usabilità deludente rispetto ai competitor.

## Cosa ho fatto

Come Lead Designer del progetto:

- **Analisi euristica** completa dell'app in produzione secondo gli 8 criteri Nielsen (carico cognitivo, controllo utente, prevenzione errori, gerarchia tipografica, coerenza grafica) + **benchmarking Satispay** su design pattern, gerarchia visiva e flusso di onboarding
- **Mappatura di due user journey completi** con feedback utente step-by-step, curva emotiva e note di intervento
- **Ridefinizione degli obiettivi di prodotto** in tre aree: rafforzare la brand identity, snellire l'onboarding, migliorare l'esperienza utente generale
- **Redesign del flusso di onboarding** con NFC veloce per l'identificazione (come Satispay, Apple Pay, Fineco), attivazione tramite PIN, riduzione dei dati richiesti in fase di registrazione (posticipando quelli non essenziali all'attivazione)
- **3 sessioni di co-design** con team multidisciplinari del cliente + standup settimanali (approccio Scrum/Lean)
- **Redesign completo dell'interfaccia e nuovo design system** pensato per estendersi ad altri prodotti del gruppo

<figure class="figure--full">
  <img src="/covers/admiral-pay/onboarding-benchmark-08.jpg" alt="Confronto onboarding Satispay vs Admiral Pay: 1h vs 48h" />
  <figcaption>Benchmarking del flusso di onboarding — Satispay chiude in meno di 1 ora con carico cognitivo basso, Admiral Pay richiedeva 48+ ore con carico cognitivo molto alto</figcaption>
</figure>

<figure class="figure--wide">
  <div class="figure-grid">
    <img src="/covers/admiral-pay/user-journey-10.jpg" alt="User journey mapping — parte 1: registrazione e KYC" />
    <img src="/covers/admiral-pay/user-journey-11.jpg" alt="User journey mapping — parte 2: identificazione e attivazione" />
  </div>
  <figcaption>Mappatura dei due user journey completi — feedback utente step-by-step, curva emotiva, note d'intervento</figcaption>
</figure>

<figure class="figure--wide">
  <img src="/covers/admiral-pay/interventi-12.jpg" alt="Diagramma delle tre aree di intervento: UI, usabilità, architettura & service design" />
  <figcaption>Le tre aree d'intervento identificate dall'analisi — strettamente correlate tra loro</figcaption>
</figure>

<figure class="figure--wide">
  <img src="/covers/admiral-pay/new-ui-04.jpg" alt="Nuovo look & feel: home screen e schermata di registrazione" />
  <figcaption>Nuovo look &amp; feel — home screen e onboarding riprogettati per chiarezza e affidabilità percepita</figcaption>
</figure>

<figure class="figure--wide">
  <img src="/covers/admiral-pay/onboarding-nfc-08.jpg" alt="Soluzione onboarding: NFC veloce per l'identificazione + attivazione PIN" />
  <figcaption>Soluzione proposta — NFC veloce (come Satispay, Apple Pay, Fineco) e attivazione PIN diretta nell'app</figcaption>
</figure>

## Risultato

Il redesign è oggi in produzione. Il tempo di onboarding è passato da 48 ore a 5 minuti. La CRO di attivazione account è raddoppiata. Il design system è stato riusato su altri prodotti digitali del gruppo Admiral.
