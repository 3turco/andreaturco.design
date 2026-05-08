---
title: "Sistema di design per una piattaforma fintech"
description: "Progettazione di un design system scalabile per una startup fintech italiana: componenti, tokens, documentazione e governance."
year: 2024
role: "Lead Product Designer"
tags: ["Design System", "UI Design", "Figma", "Fintech"]
client: "Confidenziale"
draft: false
---

## Il contesto

Una startup fintech in rapida crescita si trovava ad affrontare un problema classico: tre team di prodotto che sviluppavano in parallelo, componenti duplicati ovunque, inconsistenze visive tra le diverse aree dell'app. Il risultato era un'esperienza frammentata per l'utente e un debito di design che rallentava ogni nuova feature.

Il mio incarico era costruire un sistema di design condiviso che diventasse la lingua comune tra design e sviluppo.

## L'approccio

Ho iniziato con un audit completo dell'esistente: ho catalogato ogni componente in produzione, identificato le duplicazioni, mappato le inconsistenze. Da questo lavoro è emerso un inventario di circa 140 componenti unici — ridotti poi a 60 nella versione sistematizzata.

Il sistema è stato costruito su tre livelli:

**Fondamenta (tokens)** — Colori, tipografia, spaziatura, ombre, border radius. Tutto come variabili con naming semantico: `color.feedback.error` invece di `red.500`.

**Componenti base** — Button, Input, Select, Modal, Toast, Badge. Ogni componente con varianti documentate, stati di interazione, specifiche di accessibilità.

**Pattern composti** — Form complessi, layout di dashboard, flussi di onboarding. I mattoni assembled in combinazioni ricorrenti.

## Il risultato

Il sistema è stato adottato da tutti e tre i team nel giro di sei mesi. La velocità di prototipazione è aumentata sensibilmente: i designer non ripartono da zero, i developer hanno specifiche chiare e token già mappati nel codice.

La parte più importante del lavoro, però, è stata la governance: ho istituito un processo di review per i contributi al sistema, una cadenza mensile di aggiornamento, e documentazione sempre aggiornata su Notion.
