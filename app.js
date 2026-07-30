const $ = (selector) => document.querySelector(selector);

const DOMAIN_NAVIGATION = [
  { key: "urgent_safety", domains: ["urgent_safety", "safety"], icon: "SG" },
  { key: "context_privacy", domains: ["normalization"], icon: "CP" },
  { key: "autonomy_erosion", domains: ["autonomy_erosion"], icon: "AU" },
  { key: "economic", domains: ["economic"], icon: "EC" },
  { key: "health", domains: ["health"], icon: "SL" },
  { key: "care", domains: ["care", "care_and_health"], icon: "CU" },
  { key: "psychological", domains: ["psychological"], icon: "PS" },
  { key: "social", domains: ["social", "social_isolation"], icon: "SO" },
  { key: "sexual", domains: ["sexual"], icon: "SX" },
  { key: "physical", domains: ["physical"], icon: "FI" },
  { key: "digital", domains: ["digital"], icon: "DI" },
  { key: "institutional", domains: ["institutional"], icon: "IN" }
];

const text = {
  ca: {
    headerSubline: "Suport professional orientatiu",
    profileLabel: "Perfil",
    resetButton: "Nou cas",
    progressTitle: "Itinerari",
    progressLabel: "Progrés",
    answeredLabel: "Respostes",
    pendingLabel: "Pendents",
    domainsTitle: "Dominis explorats",
    trainingTitle: "Formació",
    trainingSelectLabel: "Cas formatiu",
    loadCaseButton: "Carregar relat",
    statusReady: "Sessió efímera preparada",
    statusLoading: "Preparant sessió...",
    statusComplete: "Itinerari completat. Ja pots revisar l'informe.",
    statusExpired: "Sessió expirada o connexió limitada. Revisa el servidor local.",
    noteLabel: "Observació professional opcional",
    noteDescription: "Afegeix context útil per a la valoració professional.",
    privacyNote: "No incloguis dades identificatives que no siguin necessàries.",
    attentionLabel: "Informació orientativa",
    attentionText: "La informació obtinguda és orientativa i no substitueix el criteri professional ni els protocols vigents.",
    reportButton: "Generar informe",
    indicatorTitle: "Indicadors que convé explorar",
    recommendationTitle: "Recomanacions de suport",
    pendingTitle: "Àrees pendents",
    sourcesTitle: "Fonts i protocols",
    limitsTitle: "Limitacions de l'entrevista",
    factTitle: "Text lliure",
    factSubline: "Fets proposats, sempre confirmables per la professional.",
    extractFactsButton: "Extreure fets",
    addFactsButton: "Afegir fets confirmats",
    reportTitle: "Informe orientatiu",
    reportSubline: "Revisable abans de compartir o arxivar.",
    printButton: "Descarregar PDF",
    downloadButton: "Descarregar JSON",
    guideLink: "Guia d'ús",
    privacyLink: "Privacitat",
    projectInfoLink: "Informació del projecte",
    helpCloseButton: "Entesos",
    helpTopics: {
      guide: {
        title: "Guia d'ús",
        intro: "LUCERNA 65 et guia pas a pas durant una entrevista professional. La idea és respondre només allò que pots valorar amb la informació disponible.",
        items: [
          "Tria el perfil professional i l'idioma abans de començar.",
          "Respon la pregunta visible i avança amb calma. Pots deixar una resposta com a “No consta” si no es pot saber ara.",
          "Afegeix notes només quan ajudin a entendre el context professional.",
          "Quan hi hagi prou informació, podràs preparar un informe orientatiu per revisar-lo abans d'usar-lo."
        ],
        note: "Si hi ha risc imminent, segueix el protocol d'emergència del teu centre."
      },
      privacy: {
        title: "Privacitat",
        intro: "La sessió està pensada per treballar amb dades mínimes i de manera efímera. No cal escriure noms, adreces ni identificadors si no són imprescindibles.",
        items: [
          "Evita dades identificatives innecessàries en respostes i observacions.",
          "No copiïs informació sensible que no aporti valor a la valoració professional.",
          "Revisa l'informe abans de compartir-lo, arxivar-lo o incorporar-lo a un expedient.",
          "Aplica sempre les normes de confidencialitat i protecció de dades del teu centre."
        ],
        note: "L'eina no promet seguretat absoluta: és responsabilitat professional usar-la dins un entorn adequat."
      },
      project: {
        title: "Informació del projecte",
        intro: "LUCERNA 65 és un prototip de suport professional orientatiu per ordenar informació i detectar àrees que convé explorar.",
        items: [
          "No diagnostica, no confirma violència i no substitueix el criteri professional.",
          "No és una denúncia, un peritatge ni una resolució administrativa.",
          "Ajuda a documentar indicadors, recomanacions i àrees pendents amb llenguatge prudent.",
          "Les fonts, recursos i protocols s'han de verificar abans d'usar-los en casos reals."
        ],
        note: "Informe pendent de revisió professional abans de compartir o arxivar."
      }
    },
    offlineTitle: "Connexió limitada",
    offlineText: "Algunes funcions poden no estar disponibles fins que l'API local respongui.",
    safetyReminderText: "<strong>Recordatori:</strong> si hi ha risc imminent, activa els protocols d'emergència segons el procediment del teu centre.",
    reviewPending: "Informe pendent de revisió professional",
    reviewReady: "Informe orientatiu preparat",
    newCaseTitle: "Iniciar un nou cas?",
    newCaseText: "Es reiniciarà la sessió efímera i es buidaran les respostes visibles d'aquest itinerari.",
    cancelNewCaseButton: "Cancel·lar",
    confirmNewCaseButton: "Nou cas",
    generateReportTitle: "Generar informe orientatiu",
    generateReportText: "L'informe és un esborrany de suport i queda pendent de revisió professional abans de compartir-lo o arxivar-lo.",
    cancelReportButton: "Cancel·lar",
    confirmReportButton: "Generar esborrany",
    emptyIndicators: "Encara no hi ha indicadors actius.",
    emptyIndicatorsHint: "Els indicadors apareixeran quan les respostes aportin prou context.",
    emptyRecommendations: "Les recomanacions apareixeran quan hi hagi prou context.",
    emptyPending: "No hi ha àrees pendents destacades.",
    emptySources: "Les fonts i protocols apareixeran en l'informe orientatiu.",
    emptyLimits: "Les limitacions es recolliran quan es generi l'informe.",
    noFacts: "No s'han extret fets confirmables.",
    apiError: "No puc contactar amb l'API local.",
    trainingEmpty: "Cas formatiu",
    enoughInfoNeeded: "Cal almenys una resposta professional abans de generar l'informe.",
    answerSaved: "Resposta registrada. Revisió contextual actualitzada.",
    domains: {
      urgent_safety: "Seguretat immediata",
      context_privacy: "Context i privacitat",
      autonomy_erosion: "Autonomia",
      economic: "Econòmic",
      health: "Salut",
      care: "Cures",
      psychological: "Psicològic",
      social: "Social",
      sexual: "Sexual",
      physical: "Físic",
      digital: "Digital",
      institutional: "Institucional",
      normalization: "Normalització",
      care_and_health: "Cures i salut",
      social_isolation: "Aïllament social",
      review: "Revisió"
    },
    domainStatus: {
      pending: "Pendent",
      active: "En curs",
      done: "Explorat",
      not_applicable: "No aplicable"
    },
    priority: {
      urgent: "Urgent",
      high: "Prioritari",
      priority: "Prioritari",
      medium: "Seguiment",
      scheduled: "Seguiment",
      preventive: "Preventiu",
      exploratory: "Preventiu"
    },
    answerDescriptions: {
      yes: "Aquest element es constata o convé explorar-lo amb més detall.",
      yesDanger: "Hi ha risc immediat o necessitat urgent.",
      yesSafe: "Es pot activar el protocol mantenint un espai segur.",
      no: "No s'observa aquest element en la informació disponible.",
      noWarning: "No es pot garantir aquest element; cal valorar alternatives segures.",
      unknown: "No es pot determinar ara.",
      unknownWarning: "No es pot determinar amb seguretat en aquest moment."
    },
    answerLabels: {
      yes: "Sí",
      no: "No",
      unknown: "No consta"
    },
    profiles: {
      health: "Salut",
      social: "Serveis socials",
      psychology: "Psicologia",
      care: "Cures i residències",
      legal: "Àmbit jurídic",
      community: "Comunitari"
    },
    reportSections: {
      facts: "Respostes recollides",
      indicators: "Indicadors que convé explorar",
      pending: "Àrees pendents",
      recommendations: "Recomanacions de suport",
      resources: "Recursos",
      sources: "Fonts i protocols",
      limits: "Limitacions",
      audit: "Auditoria"
    }
  },
  es: {
    headerSubline: "Apoyo profesional orientativo",
    profileLabel: "Perfil",
    resetButton: "Nuevo caso",
    progressTitle: "Itinerario",
    progressLabel: "Progreso",
    answeredLabel: "Respuestas",
    pendingLabel: "Pendientes",
    domainsTitle: "Dominios explorados",
    trainingTitle: "Formación",
    trainingSelectLabel: "Caso formativo",
    loadCaseButton: "Cargar relato",
    statusReady: "Sesión efímera preparada",
    statusLoading: "Preparando sesión...",
    statusComplete: "Itinerario completado. Ya puedes revisar el informe.",
    statusExpired: "Sesión expirada o conexión limitada. Revisa el servidor local.",
    noteLabel: "Observación profesional opcional",
    noteDescription: "Añade contexto útil para la valoración profesional.",
    privacyNote: "No incluyas datos identificativos que no sean necesarios.",
    attentionLabel: "Información orientativa",
    attentionText: "La información obtenida es orientativa y no sustituye el criterio profesional ni los protocolos vigentes.",
    reportButton: "Generar informe",
    indicatorTitle: "Indicadores que conviene explorar",
    recommendationTitle: "Recomendaciones de apoyo",
    pendingTitle: "Áreas pendientes",
    sourcesTitle: "Fuentes y protocolos",
    limitsTitle: "Limitaciones de la entrevista",
    factTitle: "Texto libre",
    factSubline: "Hechos propuestos, siempre confirmables por la profesional.",
    extractFactsButton: "Extraer hechos",
    addFactsButton: "Añadir hechos confirmados",
    reportTitle: "Informe orientativo",
    reportSubline: "Revisable antes de compartir o archivar.",
    printButton: "Descargar PDF",
    downloadButton: "Descargar JSON",
    guideLink: "Guía de uso",
    privacyLink: "Privacidad",
    projectInfoLink: "Información del proyecto",
    helpCloseButton: "Entendido",
    helpTopics: {
      guide: {
        title: "Guía de uso",
        intro: "LUCERNA 65 te guía paso a paso durante una entrevista profesional. La idea es responder solo aquello que puedes valorar con la información disponible.",
        items: [
          "Elige el perfil profesional y el idioma antes de empezar.",
          "Responde la pregunta visible y avanza con calma. Puedes dejar una respuesta como “No consta” si no se puede saber ahora.",
          "Añade notas solo cuando ayuden a entender el contexto profesional.",
          "Cuando haya información suficiente, podrás preparar un informe orientativo para revisarlo antes de usarlo."
        ],
        note: "Si hay riesgo inminente, sigue el protocolo de emergencia de tu centro."
      },
      privacy: {
        title: "Privacidad",
        intro: "La sesión está pensada para trabajar con datos mínimos y de forma efímera. No hace falta escribir nombres, direcciones ni identificadores si no son imprescindibles.",
        items: [
          "Evita datos identificativos innecesarios en respuestas y observaciones.",
          "No copies información sensible que no aporte valor a la valoración profesional.",
          "Revisa el informe antes de compartirlo, archivarlo o incorporarlo a un expediente.",
          "Aplica siempre las normas de confidencialidad y protección de datos de tu centro."
        ],
        note: "La herramienta no promete seguridad absoluta: es responsabilidad profesional usarla dentro de un entorno adecuado."
      },
      project: {
        title: "Información del proyecto",
        intro: "LUCERNA 65 es un prototipo de apoyo profesional orientativo para ordenar información y detectar áreas que conviene explorar.",
        items: [
          "No diagnostica, no confirma violencia y no sustituye el criterio profesional.",
          "No es una denuncia, un peritaje ni una resolución administrativa.",
          "Ayuda a documentar indicadores, recomendaciones y áreas pendientes con lenguaje prudente.",
          "Las fuentes, recursos y protocolos se deben verificar antes de usarlos en casos reales."
        ],
        note: "Informe pendiente de revisión profesional antes de compartir o archivar."
      }
    },
    offlineTitle: "Conexión limitada",
    offlineText: "Algunas funciones pueden no estar disponibles hasta que la API local responda.",
    safetyReminderText: "<strong>Recordatorio:</strong> si hay riesgo inminente, activa los protocolos de emergencia según el procedimiento de tu centro.",
    reviewPending: "Informe pendiente de revisión profesional",
    reviewReady: "Informe orientativo preparado",
    newCaseTitle: "¿Iniciar un nuevo caso?",
    newCaseText: "Se reiniciará la sesión efímera y se vaciarán las respuestas visibles de este itinerario.",
    cancelNewCaseButton: "Cancelar",
    confirmNewCaseButton: "Nuevo caso",
    generateReportTitle: "Generar informe orientativo",
    generateReportText: "El informe es un borrador de apoyo y queda pendiente de revisión profesional antes de compartirlo o archivarlo.",
    cancelReportButton: "Cancelar",
    confirmReportButton: "Generar borrador",
    emptyIndicators: "Aún no hay indicadores activos.",
    emptyIndicatorsHint: "Los indicadores aparecerán cuando las respuestas aporten suficiente contexto.",
    emptyRecommendations: "Las recomendaciones aparecerán cuando haya suficiente contexto.",
    emptyPending: "No hay áreas pendientes destacadas.",
    emptySources: "Las fuentes y protocolos aparecerán en el informe orientativo.",
    emptyLimits: "Las limitaciones se recogerán cuando se genere el informe.",
    noFacts: "No se han extraído hechos confirmables.",
    apiError: "No puedo contactar con la API local.",
    trainingEmpty: "Caso formativo",
    enoughInfoNeeded: "Hace falta al menos una respuesta profesional antes de generar el informe.",
    answerSaved: "Respuesta registrada. Revisión contextual actualizada.",
    domains: {
      urgent_safety: "Seguridad inmediata",
      context_privacy: "Contexto y privacidad",
      autonomy_erosion: "Autonomía",
      economic: "Económico",
      health: "Salud",
      care: "Cuidados",
      psychological: "Psicológico",
      social: "Social",
      sexual: "Sexual",
      physical: "Físico",
      digital: "Digital",
      institutional: "Institucional",
      normalization: "Normalización",
      care_and_health: "Cuidados y salud",
      social_isolation: "Aislamiento social",
      review: "Revisión"
    },
    domainStatus: {
      pending: "Pendiente",
      active: "En curso",
      done: "Explorado",
      not_applicable: "No aplicable"
    },
    priority: {
      urgent: "Urgente",
      high: "Prioritario",
      priority: "Prioritario",
      medium: "Seguimiento",
      scheduled: "Seguimiento",
      preventive: "Preventivo",
      exploratory: "Preventivo"
    },
    answerDescriptions: {
      yes: "Este elemento se constata o conviene explorarlo con más detalle.",
      yesDanger: "Hay riesgo inmediato o necesidad urgente.",
      yesSafe: "Se puede activar el protocolo manteniendo un espacio seguro.",
      no: "No se observa este elemento en la información disponible.",
      noWarning: "No se puede garantizar este elemento; conviene valorar alternativas seguras.",
      unknown: "No se puede determinar ahora.",
      unknownWarning: "No se puede determinar con seguridad en este momento."
    },
    answerLabels: {
      yes: "Sí",
      no: "No",
      unknown: "No consta"
    },
    profiles: {
      health: "Salud",
      social: "Servicios sociales",
      psychology: "Psicología",
      care: "Cuidados y residencias",
      legal: "Ámbito jurídico",
      community: "Comunitario"
    },
    reportSections: {
      facts: "Respuestas recogidas",
      indicators: "Indicadores que conviene explorar",
      pending: "Áreas pendientes",
      recommendations: "Recomendaciones de apoyo",
      resources: "Recursos",
      sources: "Fuentes y protocolos",
      limits: "Limitaciones",
      audit: "Auditoría"
    }
  }
};

Object.assign(text.ca, {
  documentTitle: "LUCERNA 65",
  metaDescription: "Sistema orientatiu de suport professional per explorar indicadors de violències masclistes envers dones grans.",
  skipLink: "Saltar al contingut principal",
  languageAria: "Idioma",
  headerAria: "Capçalera de LUCERNA 65",
  workbenchAria: "Espai de treball professional",
  journeyAria: "Itinerari de preguntes",
  supportInfoAria: "Informació de suport",
  answerPanelAria: "Opcions de resposta",
  safetyAria: "Recordatori professional",
  contextPanelAria: "Informació orientativa",
  notePlaceholder: "Afegeix observacions rellevants sobre el context, actituds, llenguatge no verbal, presència d'altres persones o limitacions de l'entrevista.",
  freeTextPlaceholder: "Enganxa un relat breu o notes professionals per proposar fets confirmables.",
  freeTextAria: "Text lliure per extreure fets confirmables",
  aiModeLocal: "Extracció local determinista.",
  aiModeActive: "Extracció assistida amb IA: {providers}.",
  aiModeOffline: "Mode IA no disponible mentre l'API no respongui.",
  footerAria: "Suport i crèdits de LUCERNA 65",
  donationAria: "Suport al projecte",
  donationActionsAria: "Opcions de donació",
  creditAria: "Autoria",
  footerVersion: "Versió 0.1.0",
  donationText: "Si LUCERNA 65 us resulta útil per sostenir una atenció més clara i curosa, podeu contribuir a mantenir-ne la llum encesa.",
  donatePaypal: "Donar amb PayPal",
  donateGofundme: "Donar a GoFundMe",
  creditText: "CREAT PER JÚLIA ROSELL SALDAÑA - UT ALII VIVANT",
  reportNoticeTitle: "Avís",
  reportDocumentTitle: "Informe orientatiu",
  reportGeneratedAt: "Data de generació",
  reportSessionId: "Identificador de sessió",
  reportStatus: "Estat",
  reportStatusReviewable: "Revisable abans de compartir o arxivar",
  reportLimitationsEmpty: "El resultat és orientatiu i pendent de revisió professional.",
  reportAnswersEmpty: "Encara no consten respostes recollides.",
  reportObservation: "Observació",
  pendingNoneComplete: "No consten àrees pendents en l'itinerari completat.",
  pendingIncomplete: "Hi ha àrees que no s'han pogut explorar amb la informació disponible.",
  urgentActionLabel: "Actuació prioritària segons protocol aplicable",
  resourcesEmpty: "No consten recursos associats en aquest moment.",
  sourcesEmpty: "No consten fonts associades en aquest moment.",
  sourceUnknownOrganism: "Font pendent d'organisme",
  sourceVersionLabel: "Versió",
  sourceStatusLabel: "Estat",
  sourceVerificationNote: "Pendent de verificació per a ús en casos reals.",
  auditSessionId: "Identificador de sessió",
  auditTreeVersion: "Versió de l'arbre",
  auditDataMode: "Mode de dades",
  auditHumanReview: "Revisió humana",
  yesLower: "sí",
  noLower: "no",
  valueLabels: {
    yes: "Sí", no: "No", partial: "Parcialment", unknown: "No consta", free_text: "Text lliure", ephemeral: "Efímer",
    other_person: "Decisió d'una altra persona", discouraged: "Desànim o pressió", accessibility: "Accessibilitat", resources: "Recursos", mixed: "Mixt",
    health: "Salut", money: "Diners", medication: "Medicació", mobility: "Mobilitat", phone: "Telèfon", visits: "Visites", nothing: "Res",
    threats: "Amenaces", insults: "Insults", punished: "Càstig", prevented: "Impedida", urgent: "Urgent", priority: "Prioritari", scheduled: "Seguiment", preventive: "Preventiu"
  },
  statusLabels: {
    pending: "Pendent de verificació", placeholder: "Pendent de verificació", pendent_ingestio: "Pendent d'ingestió",
    pendent_ingestio_i_verificacio: "Pendent d'ingestió i verificació", pendent_identificar_versio_vigent: "Pendent d'identificar la versió vigent",
    pendent_verificacio: "Pendent de verificació", actualitzacio_continua: "Actualització contínua", vigent_a_verificar: "Vigent a verificar",
    aplicacio_esglaonada_a_verificar: "Aplicació esglaonada a verificar"
  }
});

Object.assign(text.es, {
  documentTitle: "LUCERNA 65",
  metaDescription: "Sistema orientativo de apoyo profesional para explorar indicadores de violencias machistas hacia mujeres mayores.",
  skipLink: "Saltar al contenido principal",
  languageAria: "Idioma",
  headerAria: "Cabecera de LUCERNA 65",
  workbenchAria: "Espacio de trabajo profesional",
  journeyAria: "Itinerario de preguntas",
  supportInfoAria: "Información de apoyo",
  answerPanelAria: "Opciones de respuesta",
  safetyAria: "Recordatorio profesional",
  contextPanelAria: "Información orientativa",
  notePlaceholder: "Añade observaciones relevantes sobre el contexto, actitudes, lenguaje no verbal, presencia de otras personas o limitaciones de la entrevista.",
  freeTextPlaceholder: "Pega un relato breve o notas profesionales para proponer hechos confirmables.",
  freeTextAria: "Texto libre para extraer hechos confirmables",
  aiModeLocal: "Extracción local determinista.",
  aiModeActive: "Extracción asistida con IA: {providers}.",
  aiModeOffline: "Modo IA no disponible mientras la API no responda.",
  footerAria: "Apoyo y créditos de LUCERNA 65",
  donationAria: "Apoyo al proyecto",
  donationActionsAria: "Opciones de donación",
  creditAria: "Autoría",
  footerVersion: "Versión 0.1.0",
  donationText: "Si LUCERNA 65 os resulta útil para sostener una atención más clara y cuidadosa, podéis contribuir a mantener su luz encendida.",
  donatePaypal: "Donar con PayPal",
  donateGofundme: "Donar a GoFundMe",
  creditText: "CREADO POR JÚLIA ROSELL SALDAÑA - UT ALII VIVANT",
  reportNoticeTitle: "Aviso",
  reportDocumentTitle: "Informe orientativo",
  reportGeneratedAt: "Fecha de generación",
  reportSessionId: "Identificador de sesión",
  reportStatus: "Estado",
  reportStatusReviewable: "Revisable antes de compartir o archivar",
  reportLimitationsEmpty: "El resultado es orientativo y pendiente de revisión profesional.",
  reportAnswersEmpty: "Aún no constan respuestas recogidas.",
  reportObservation: "Observación",
  pendingNoneComplete: "No constan áreas pendientes en el itinerario completado.",
  pendingIncomplete: "Hay áreas que no se han podido explorar con la información disponible.",
  urgentActionLabel: "Actuación prioritaria según protocolo aplicable",
  resourcesEmpty: "No constan recursos asociados en este momento.",
  sourcesEmpty: "No constan fuentes asociadas en este momento.",
  sourceUnknownOrganism: "Fuente pendiente de organismo",
  sourceVersionLabel: "Versión",
  sourceStatusLabel: "Estado",
  sourceVerificationNote: "Pendiente de verificación para uso en casos reales.",
  auditSessionId: "Identificador de sesión",
  auditTreeVersion: "Versión del árbol",
  auditDataMode: "Modo de datos",
  auditHumanReview: "Revisión humana",
  yesLower: "sí",
  noLower: "no",
  valueLabels: {
    yes: "Sí", no: "No", partial: "Parcialmente", unknown: "No consta", free_text: "Texto libre", ephemeral: "Efímero",
    other_person: "Decisión de otra persona", discouraged: "Desánimo o presión", accessibility: "Accesibilidad", resources: "Recursos", mixed: "Mixto",
    health: "Salud", money: "Dinero", medication: "Medicación", mobility: "Movilidad", phone: "Teléfono", visits: "Visitas", nothing: "Nada",
    threats: "Amenazas", insults: "Insultos", punished: "Castigo", prevented: "Impedida", urgent: "Urgente", priority: "Prioritario", scheduled: "Seguimiento", preventive: "Preventivo"
  },
  statusLabels: {
    pending: "Pendiente de verificación", placeholder: "Pendiente de verificación", pendent_ingestio: "Pendiente de ingestión",
    pendent_ingestio_i_verificacio: "Pendiente de ingestión y verificación", pendent_identificar_versio_vigent: "Pendiente de identificar la versión vigente",
    pendent_verificacio: "Pendiente de verificación", actualitzacio_continua: "Actualización continua", vigent_a_verificar: "Vigente a verificar",
    aplicacio_esglaonada_a_verificar: "Aplicación escalonada a verificar"
  }
});

text.en = {
  headerSubline: "Professional orientation support",
  profileLabel: "Profile",
  resetButton: "New case",
  progressTitle: "Pathway",
  progressLabel: "Progress",
  answeredLabel: "Answered",
  pendingLabel: "Pending",
  domainsTitle: "Explored domains",
  trainingTitle: "Training",
  trainingSelectLabel: "Training case",
  loadCaseButton: "Load account",
  statusReady: "Ephemeral session ready",
  statusLoading: "Preparing session...",
  statusComplete: "Pathway complete. You can now review the report.",
  statusExpired: "Session expired or limited connection. Check the local server.",
  noteLabel: "Optional professional observation",
  noteDescription: "Add useful context for professional review.",
  privacyNote: "Do not include identifying data unless necessary.",
  attentionLabel: "Orientative information",
  attentionText: "The information obtained is orientative and does not replace professional judgement or current protocols.",
  reportButton: "Generate report",
  indicatorTitle: "Indicators worth exploring",
  recommendationTitle: "Support recommendations",
  pendingTitle: "Pending areas",
  sourcesTitle: "Sources and protocols",
  limitsTitle: "Interview limitations",
  factTitle: "Free text",
  factSubline: "Proposed facts, always confirmable by the professional.",
  extractFactsButton: "Extract facts",
  addFactsButton: "Add confirmed facts",
  reportTitle: "Orientative report",
  reportSubline: "Review before sharing or filing.",
  printButton: "Download PDF",
  downloadButton: "Download JSON",
  guideLink: "User guide",
  privacyLink: "Privacy",
  projectInfoLink: "Project information",
  helpCloseButton: "Understood",
  offlineTitle: "Limited connection",
  offlineText: "Some functions may not be available until the local API responds.",
  safetyReminderText: "<strong>Reminder:</strong> if there is imminent risk, activate emergency protocols according to your centre's procedure.",
  reviewPending: "Report pending professional review",
  reviewReady: "Orientative report ready",
  newCaseTitle: "Start a new case?",
  newCaseText: "The ephemeral session will restart and visible answers in this pathway will be cleared.",
  cancelNewCaseButton: "Cancel",
  confirmNewCaseButton: "New case",
  generateReportTitle: "Generate orientative report",
  generateReportText: "The report is a support draft and remains pending professional review before sharing or filing.",
  cancelReportButton: "Cancel",
  confirmReportButton: "Generate draft",
  emptyIndicators: "There are no active indicators yet.",
  emptyIndicatorsHint: "Indicators will appear when the answers provide enough context.",
  emptyRecommendations: "Recommendations will appear when there is enough context.",
  emptyPending: "There are no highlighted pending areas.",
  emptySources: "Sources and protocols will appear in the orientative report.",
  emptyLimits: "Limitations will be collected when the report is generated.",
  noFacts: "No confirmable facts have been extracted.",
  apiError: "I cannot contact the local API.",
  trainingEmpty: "Training case",
  enoughInfoNeeded: "At least one professional answer is needed before generating the report.",
  answerSaved: "Answer recorded. Contextual review updated.",
  helpTopics: {
    guide: {
      title: "User guide",
      intro: "LUCERNA 65 guides you step by step during a professional interview. Answer only what you can assess with the information available.",
      items: [
        "Choose the professional profile and language before starting.",
        "Answer the visible question and proceed calmly. Use “Not known” if it cannot be determined now.",
        "Add notes only when they help understand the professional context.",
        "When there is enough information, you can prepare an orientative report to review before using it."
      ],
      note: "If there is imminent risk, follow your centre's emergency protocol."
    },
    privacy: {
      title: "Privacy",
      intro: "The session is designed to work with minimal data and in an ephemeral way. Names, addresses or identifiers are not needed unless strictly necessary.",
      items: [
        "Avoid unnecessary identifying data in answers and observations.",
        "Do not copy sensitive information that does not add value to the professional review.",
        "Review the report before sharing it, filing it or adding it to a case record.",
        "Always apply your centre's confidentiality and data protection rules."
      ],
      note: "The tool does not promise absolute security: it must be used within an appropriate professional environment."
    },
    project: {
      title: "Project information",
      intro: "LUCERNA 65 is an orientative professional-support prototype for organizing information and identifying areas worth exploring.",
      items: [
        "It does not diagnose, confirm violence or replace professional judgement.",
        "It is not a complaint, expert opinion or administrative decision.",
        "It helps document indicators, recommendations and pending areas with cautious language.",
        "Sources, resources and protocols must be verified before use in real cases."
      ],
      note: "Report pending professional review before sharing or filing."
    }
  },
  domains: {
    urgent_safety: "Immediate safety", context_privacy: "Context and privacy", autonomy_erosion: "Autonomy", economic: "Economic", health: "Health", care: "Care",
    psychological: "Psychological", social: "Social", sexual: "Sexual", physical: "Physical", digital: "Digital", institutional: "Institutional",
    normalization: "Normalization", care_and_health: "Care and health", social_isolation: "Social isolation", review: "Review"
  },
  domainStatus: { pending: "Pending", active: "In progress", done: "Explored", not_applicable: "Not applicable" },
  priority: { urgent: "Urgent", high: "Priority", priority: "Priority", medium: "Follow-up", scheduled: "Follow-up", preventive: "Preventive", exploratory: "Preventive" },
  answerDescriptions: {
    yes: "This element is present or should be explored in more detail.",
    yesDanger: "There is immediate risk or urgent need.",
    yesSafe: "The protocol can be activated while maintaining a safe space.",
    no: "This element is not observed in the available information.",
    noWarning: "This element cannot be guaranteed; safe alternatives should be assessed.",
    unknown: "It cannot be determined now.",
    unknownWarning: "It cannot be determined safely at this time."
  },
  answerLabels: { yes: "Yes", no: "No", unknown: "Not known" },
  profiles: {
    health: "Health", social: "Social services", psychology: "Psychology", care: "Care and residential services", legal: "Legal field", community: "Community"
  },
  reportSections: {
    facts: "Collected answers", indicators: "Indicators worth exploring", pending: "Pending areas", recommendations: "Support recommendations",
    resources: "Resources", sources: "Sources and protocols", limits: "Limitations", audit: "Audit"
  },
  documentTitle: "LUCERNA 65",
  metaDescription: "Orientative professional-support system for exploring indicators of gender-based violence against older women.",
  skipLink: "Skip to main content",
  languageAria: "Language",
  headerAria: "LUCERNA 65 header",
  workbenchAria: "Professional workspace",
  journeyAria: "Question pathway",
  supportInfoAria: "Support information",
  answerPanelAria: "Answer options",
  safetyAria: "Professional reminder",
  contextPanelAria: "Orientative information",
  notePlaceholder: "Add relevant observations about context, attitudes, non-verbal language, the presence of other people or interview limitations.",
  freeTextPlaceholder: "Paste a brief account or professional notes to propose confirmable facts.",
  freeTextAria: "Free text for extracting confirmable facts",
  aiModeLocal: "Deterministic local extraction.",
  aiModeActive: "AI-assisted extraction: {providers}.",
  aiModeOffline: "AI mode unavailable while the API is not responding.",
  footerAria: "Support and credits for LUCERNA 65",
  donationAria: "Project support",
  donationActionsAria: "Donation options",
  creditAria: "Authorship",
  footerVersion: "Version 0.1.0",
  donationText: "If LUCERNA 65 helps you sustain clearer and more careful attention, you can contribute to keeping its light on.",
  donatePaypal: "Donate with PayPal",
  donateGofundme: "Donate to GoFundMe",
  creditText: "CREATED BY JÚLIA ROSELL SALDAÑA - UT ALII VIVANT",
  reportNoticeTitle: "Notice",
  reportDocumentTitle: "Orientative report",
  reportGeneratedAt: "Generated on",
  reportSessionId: "Session identifier",
  reportStatus: "Status",
  reportStatusReviewable: "Review before sharing or filing",
  reportLimitationsEmpty: "The result is orientative and pending professional review.",
  reportAnswersEmpty: "No collected answers are recorded yet.",
  reportObservation: "Observation",
  pendingNoneComplete: "No pending areas are recorded in the completed pathway.",
  pendingIncomplete: "Some areas could not be explored with the available information.",
  urgentActionLabel: "Priority action according to the applicable protocol",
  resourcesEmpty: "No associated resources are recorded at this time.",
  sourcesEmpty: "No associated sources are recorded at this time.",
  sourceUnknownOrganism: "Source pending organization",
  sourceVersionLabel: "Version",
  sourceStatusLabel: "Status",
  sourceVerificationNote: "Pending verification for use in real cases.",
  auditSessionId: "Session identifier",
  auditTreeVersion: "Tree version",
  auditDataMode: "Data mode",
  auditHumanReview: "Human review",
  yesLower: "yes",
  noLower: "no",
  valueLabels: {
    yes: "Yes", no: "No", partial: "Partially", unknown: "Not known", free_text: "Free text", ephemeral: "Ephemeral",
    other_person: "Decision by another person", discouraged: "Discouragement or pressure", accessibility: "Accessibility", resources: "Resources", mixed: "Mixed",
    health: "Health", money: "Money", medication: "Medication", mobility: "Mobility", phone: "Phone", visits: "Visits", nothing: "Nothing",
    threats: "Threats", insults: "Insults", punished: "Punishment", prevented: "Prevented", urgent: "Urgent", priority: "Priority", scheduled: "Follow-up", preventive: "Preventive"
  },
  statusLabels: {
    pending: "Pending verification", placeholder: "Pending verification", pendent_ingestio: "Pending ingestion",
    pendent_ingestio_i_verificacio: "Pending ingestion and verification", pendent_identificar_versio_vigent: "Pending identification of current version",
    pendent_verificacio: "Pending verification", actualitzacio_continua: "Continuous update", vigent_a_verificar: "Current, to be verified",
    aplicacio_esglaonada_a_verificar: "Staged application, to be verified"
  }
};

const state = {
  locale: "ca",
  session: null,
  currentNode: null,
  progress: null,
  capabilities: null,
  report: null,
  facts: [],
  cases: [],
  selectedAnswer: null,
  currentHelpTopic: "guide",
  lastMode: "demo"
};

const pdfValueLabels = {
  yes: "Sí",
  no: "No",
  partial: "Parcialment",
  unknown: "No consta",
  free_text: "Text lliure",
  ephemeral: "Efímer",
  other_person: "Decisió d'una altra persona",
  discouraged: "Desànim o pressió",
  accessibility: "Accessibilitat",
  resources: "Recursos",
  mixed: "Mixt",
  health: "Salut",
  money: "Diners",
  medication: "Medicació",
  mobility: "Mobilitat",
  phone: "Telèfon",
  visits: "Visites",
  nothing: "Res",
  threats: "Amenaces",
  insults: "Insults",
  punished: "Càstig",
  prevented: "Impedida",
  urgent: "Urgent",
  priority: "Prioritari",
  scheduled: "Seguiment",
  preventive: "Preventiu"
};

const pdfStatusLabels = {
  pending: "Pendent de verificació",
  placeholder: "Pendent de verificació",
  pendent_ingestio: "Pendent d'ingestió",
  pendent_ingestio_i_verificacio: "Pendent d'ingestió i verificació",
  pendent_identificar_versio_vigent: "Pendent d'identificar la versió vigent",
  pendent_verificacio: "Pendent de verificació",
  actualitzacio_continua: "Actualització contínua",
  vigent_a_verificar: "Vigent a verificar",
  aplicacio_esglaonada_a_verificar: "Aplicació esglaonada a verificar"
};

function t(key, fallback = key) {
  const parts = key.split(".");
  let value = text[state.locale];
  for (const part of parts) {
    value = value?.[part];
  }
  if (value == null) {
    value = text.ca;
    for (const part of parts) {
      value = value?.[part];
    }
  }
  return value ?? fallback;
}

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function repairText(value) {
  let output = String(value ?? "");
  if (output.trim() === "S?" || output.trim() === "Si") return "Sí";
  if (/[ÃÂ]/.test(output)) {
    try {
      output = decodeURIComponent(escape(output));
    } catch {
      output = output
        .replace(/Ã€/g, "À")
        .replace(/Ã /g, "à")
        .replace(/Ã /g, "à")
        .replace(/Ã¨/g, "è")
        .replace(/Ã©/g, "é")
        .replace(/Ã­/g, "í")
        .replace(/Ã¯/g, "ï")
        .replace(/Ã²/g, "ò")
        .replace(/Ã³/g, "ó")
        .replace(/Ãº/g, "ú")
        .replace(/Ã¼/g, "ü")
        .replace(/Ã§/g, "ç")
        .replace(/Â·/g, "·");
    }
  }
  const replacements = {
    "S?": "Sí",
    "Des?nim o pressi?": "Desànim o pressió",
    "Medicaci?": "Medicació",
    "Tel?fon": "Telèfon",
    "Alimentaci?": "Alimentació",
    "C?stig": "Càstig",
    "violencies": "violències",
    "verificacio": "verificació",
    "salut comunitaria": "salut comunitària",
    "diagnostic": "diagnòstic",
    "denuncia": "denúncia",
    "resolucio": "resolució",
    "Sessio": "Sessió",
    "Revisio": "Revisió"
  };
  for (const [bad, good] of Object.entries(replacements)) {
    output = output.replaceAll(bad, good);
  }
  return output;
}

async function api(path, payload) {
  const response = await fetch(path, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || response.statusText);
  }
  return data;
}

async function getJson(path) {
  const response = await fetch(path);
  if (!response.ok) {
    throw new Error(response.statusText);
  }
  return response.json();
}

function AppHeader() {
  renderProfileOptions();
  setCopy();
}

function ProfessionalProfileSelector() {
  renderProfileOptions();
}

function LanguageSwitcher() {
  document.querySelectorAll("#localeToggle button").forEach((button) => {
    const active = button.dataset.locale === state.locale;
    button.classList.toggle("isActive", active);
    button.setAttribute("aria-pressed", String(active));
  });
}

function NewCaseButton() {
  $("#resetButtonText").textContent = t("resetButton");
}

function JourneySidebar() {
  ProgressSummary();
  DomainNavigation();
}

function ProgressSummary() {
  const progress = state.progress || { answered: 0, pending: 0, completionRatio: 0 };
  const percent = Math.round((progress.completionRatio || 0) * 100);
  $("#progressPercent").textContent = `${percent}%`;
  $("#progressBar").style.width = `${percent}%`;
  $("#answeredCount").textContent = progress.answered || 0;
  $("#pendingCount").textContent = progress.pending || 0;
}

function DomainNavigation() {
  const progress = state.progress || { domains: [] };
  const currentKey = currentDomainKey();
  $("#domainList").innerHTML = DOMAIN_NAVIGATION
    .map((item) => DomainNavigationItem(item, currentKey, progress.domains || []))
    .join("");
}

function DomainNavigationItem(item, currentKey, completedDomains) {
  const isActive = item.key === currentKey;
  const isDone = item.domains.some((domain) => completedDomains.includes(domain));
  const status = isActive ? "active" : isDone ? "done" : "pending";
  const label = t(`domains.${item.key}`, item.key);
  const statusLabel = t(`domainStatus.${status}`, status);
  return `
    <div class="domainItem is-${status}" aria-current="${isActive ? "step" : "false"}">
      <span class="domainIcon" aria-hidden="true">${escapeHtml(item.icon)}</span>
      <span class="domainName">${escapeHtml(label)}</span>
      <span class="domainState">${escapeHtml(statusLabel)}</span>
    </div>
  `;
}

function QuestionCard() {
  renderCurrentNode();
}

function QuestionHeader(node) {
  const domainLabel = t(`domains.${currentDomainKey()}`, node?.domain || "Context");
  const attention = priorityMeta(node?.priority || "exploratory");
  $("#domainPill").textContent = domainLabel;
  $("#priorityPill").textContent = attention.label;
  $("#priorityPill").dataset.attention = attention.key;
}

function AnswerOption(answer, node) {
  const label = answerLabel(answer);
  const description = answerDescription(answer, node);
  const tone = visualTone(answer, node);
  const icon = answerIcon(answer, tone);
  const selected = state.selectedAnswer === answer.id;
  return `
    <button
      type="button"
      class="answerOption ${selected ? "isSelected" : ""}"
      data-answer="${escapeHtml(answer.id)}"
      data-tone="${escapeHtml(tone)}"
      aria-pressed="${selected ? "true" : "false"}"
    >
      <span class="answerIcon" aria-hidden="true">${escapeHtml(icon)}</span>
      <span>
        <strong>${escapeHtml(label)}</strong>
        <small>${escapeHtml(description)}</small>
      </span>
    </button>
  `;
}

function ProfessionalNotes() {
  const length = $("#noteInput").value.length;
  $("#noteCounter").textContent = `${length} / 1200`;
}

function ContextPanel() {
  renderReview();
}

function AttentionNotice(report) {
  const attention = report?.attention || {};
  const meta = priorityMeta(attention.level || state.currentNode?.priority || "exploratory");
  $("#attentionValue").textContent = repairText(attention.label || meta.panelLabel);
  $("#attentionValue").dataset.attention = meta.key;
  $("#reportButton").dataset.attention = meta.key;
}

function IndicatorsPanel(report) {
  renderStack("#indicatorList", report?.indicators, EmptyState("ID", t("emptyIndicators"), t("emptyIndicatorsHint")), (item) => `
    <article class="listItem">
      <h3>${escapeHtml(repairText(item.label))}</h3>
      <p>${escapeHtml(repairText(item.rationale || ""))}</p>
    </article>
  `);
}

function RecommendationsPanel(report) {
  renderStack("#recommendationList", report?.recommendations, EmptyState("RC", t("emptyRecommendations"), ""), (item) => `
    <article class="listItem">
      <h3>${escapeHtml(priorityMeta(item.priority || "scheduled").label)}</h3>
      <p>${escapeHtml(repairText(item.text || ""))}</p>
    </article>
  `);
}

function PendingAreasPanel(report) {
  renderStack("#pendingList", report?.pending_questions, EmptyState("AP", t("emptyPending"), ""), (item) => `
    <article class="listItem compactListItem">
      <p>${escapeHtml(repairText(item))}</p>
    </article>
  `);
}

function SourcesPanel(report) {
  renderStack("#sourcesList", report?.sources, EmptyState("FP", t("emptySources"), ""), (item) => `
    <article class="listItem">
      <h3>${escapeHtml(repairText(item.organism || item.title || ""))}</h3>
      <p>${escapeHtml(repairText([item.title, item.status].filter(Boolean).join(" · ")))}</p>
    </article>
  `);
}

function LimitationsPanel(report) {
  renderStack("#limitsList", report?.limitations, EmptyState("LI", t("emptyLimits"), ""), (item) => `
    <article class="listItem compactListItem">
      <p>${escapeHtml(repairText(item))}</p>
    </article>
  `);
}

function EmptyState(icon, title, hint) {
  return `
    <div class="emptyState">
      <span class="emptyIcon" data-icon="${escapeHtml(icon)}" aria-hidden="true"></span>
      <p>${escapeHtml(title)}</p>
      ${hint ? `<small>${escapeHtml(hint)}</small>` : ""}
    </div>
  `;
}

function SafetyReminder() {
  $("#safetyReminderText").innerHTML = t("safetyReminderText");
}

function Footer() {
  // Static footer text is intentionally conservative: it avoids promising guarantees that are not implemented.
}

function InfoDialog(topic) {
  const topics = t("helpTopics", text.ca.helpTopics);
  const content = topics?.[topic] || topics?.guide;
  if (!content) return;

  state.currentHelpTopic = topic;
  $("#helpDialogTitle").textContent = repairText(content.title);
  $("#helpDialogBody").innerHTML = `
    <p>${escapeHtml(repairText(content.intro))}</p>
    <ul>
      ${(content.items || []).map((item) => `<li>${escapeHtml(repairText(item))}</li>`).join("")}
    </ul>
    ${content.note ? `<p class="infoDialogNote">${escapeHtml(repairText(content.note))}</p>` : ""}
  `;
  showDialog("#helpDialog");
}

function ConfirmNewCaseModal() {
  showDialog("#newCaseDialog");
}

function GenerateReportModal() {
  if (!canGenerateReport()) {
    $("#statusLine").textContent = t("enoughInfoNeeded");
    return;
  }
  showDialog("#generateReportDialog");
}

function renderProfileOptions() {
  const selected = $("#profileSelect").value || "health";
  $("#profileSelect").innerHTML = Object.entries(t("profiles", text.ca.profiles))
    .map(([value, label]) => `<option value="${escapeHtml(value)}">${escapeHtml(label)}</option>`)
    .join("");
  $("#profileSelect").value = selected;
}

function setCopy() {
  const bindings = {
    headerSubline: "headerSubline",
    profileLabel: "profileLabel",
    progressTitle: "progressTitle",
    progressLabel: "progressLabel",
    answeredLabel: "answeredLabel",
    pendingLabel: "pendingLabel",
    domainsTitle: "domainsTitle",
    trainingTitle: "trainingTitle",
    trainingSelectLabel: "trainingSelectLabel",
    loadCaseButton: "loadCaseButton",
    noteLabel: "noteLabel",
    noteDescription: "noteDescription",
    privacyNote: "privacyNote",
    attentionLabel: "attentionLabel",
    attentionText: "attentionText",
    reportButton: "reportButton",
    indicatorTitle: "indicatorTitle",
    recommendationTitle: "recommendationTitle",
    pendingTitle: "pendingTitle",
    sourcesTitle: "sourcesTitle",
    limitsTitle: "limitsTitle",
    factTitle: "factTitle",
    factSubline: "factSubline",
    extractFactsButton: "extractFactsButton",
    addFactsButton: "addFactsButton",
    reportTitle: "reportTitle",
    reportSubline: "reportSubline",
    printButton: "printButton",
    downloadButton: "downloadButton",
    guideLink: "guideLink",
    privacyLink: "privacyLink",
    projectInfoLink: "projectInfoLink",
    offlineTitle: "offlineTitle",
    offlineText: "offlineText",
    reviewStatus: canGenerateReport() ? "reviewReady" : "reviewPending",
    newCaseTitle: "newCaseTitle",
    newCaseText: "newCaseText",
    cancelNewCaseButton: "cancelNewCaseButton",
    confirmNewCaseButton: "confirmNewCaseButton",
    generateReportTitle: "generateReportTitle",
    generateReportText: "generateReportText",
    cancelReportButton: "cancelReportButton",
    confirmReportButton: "confirmReportButton",
    closeHelpDialogButton: "helpCloseButton"
  };

  for (const [id, key] of Object.entries(bindings)) {
    const element = $(`#${id}`);
    if (element) element.textContent = repairText(t(key));
  }

  const textBindings = [
    [".skipLink", "skipLink"],
    [".sidebarFooter span", "footerVersion"],
    [".donationFooter p", "donationText"],
    [".donationActions a:nth-child(1)", "donatePaypal"],
    [".donationActions a:nth-child(2)", "donateGofundme"],
    [".creditFooter span", "creditText"]
  ];
  for (const [selector, key] of textBindings) {
    const element = $(selector);
    if (element) element.textContent = repairText(t(key));
  }

  const attrBindings = [
    [".appHeader", "aria-label", "headerAria"],
    ["#localeToggle", "aria-label", "languageAria"],
    [".workbench", "aria-label", "workbenchAria"],
    [".journeySidebar", "aria-label", "journeyAria"],
    [".sidebarFooter", "aria-label", "supportInfoAria"],
    ["#answerPanel", "aria-label", "answerPanelAria"],
    [".safetyReminder", "aria-label", "safetyAria"],
    [".contextPanel", "aria-label", "contextPanelAria"],
    ["#noteInput", "placeholder", "notePlaceholder"],
    ["#freeTextInput", "placeholder", "freeTextPlaceholder"],
    ["#freeTextInput", "aria-label", "freeTextAria"],
    [".appFooter", "aria-label", "footerAria"],
    [".donationFooter", "aria-label", "donationAria"],
    [".donationActions", "aria-label", "donationActionsAria"],
    [".creditFooter", "aria-label", "creditAria"]
  ];
  for (const [selector, attribute, key] of attrBindings) {
    const element = $(selector);
    if (element) element.setAttribute(attribute, repairText(t(key)));
  }

  document.title = repairText(t("documentTitle"));
  const description = $('meta[name="description"]');
  if (description) description.setAttribute("content", repairText(t("metaDescription")));

  NewCaseButton();
  ProfessionalProfileSelector();
  LanguageSwitcher();
  SafetyReminder();
  ProfessionalNotes();
  renderAiStatus();
  renderFactList();
  document.documentElement.lang = state.locale;
}

async function boot() {
  AppHeader();
  bindEvents();
  await Promise.all([loadCapabilities(), loadTrainingCases()]);
  await startSession();
}

function bindEvents() {
  $("#resetButton").addEventListener("click", () => {
    if ((state.progress?.answered || 0) > 0) {
      ConfirmNewCaseModal();
    } else {
      startSession();
    }
  });
  $("#confirmNewCaseButton").addEventListener("click", () => {
    closeDialog("#newCaseDialog");
    startSession();
  });
  $("#cancelNewCaseButton").addEventListener("click", () => closeDialog("#newCaseDialog"));
  $("#profileSelect").addEventListener("change", () => {
    if ((state.progress?.answered || 0) > 0) {
      ConfirmNewCaseModal();
    } else {
      startSession();
    }
  });
  $("#reportButton").addEventListener("click", GenerateReportModal);
  $("#confirmReportButton").addEventListener("click", async () => {
    closeDialog("#generateReportDialog");
    await generateReport();
  });
  $("#cancelReportButton").addEventListener("click", () => closeDialog("#generateReportDialog"));
  $("#extractFactsButton").addEventListener("click", extractFacts);
  $("#addFactsButton").addEventListener("click", addSelectedFacts);
  $("#printButton").addEventListener("click", downloadPdf);
  $("#downloadButton").addEventListener("click", downloadReport);
  $("#loadCaseButton").addEventListener("click", loadSelectedCase);
  $("#noteInput").addEventListener("input", ProfessionalNotes);
  $("#closeHelpDialogButton").addEventListener("click", () => closeDialog("#helpDialog"));

  document.querySelectorAll("[data-help-topic]").forEach((link) => {
    link.addEventListener("click", (event) => {
      event.preventDefault();
      InfoDialog(link.dataset.helpTopic);
    });
  });

  document.querySelectorAll("#localeToggle button").forEach((button) => {
    button.addEventListener("click", async () => {
      await changeLocale(button.dataset.locale);
    });
  });
}

async function changeLocale(locale) {
  if (!locale || locale === state.locale) return;
  state.locale = locale;
  setCopy();
  renderTrainingCases();

  if (!state.session) {
    JourneySidebar();
    QuestionCard();
    ContextPanel();
    return;
  }

  try {
    const payload = await api("/api/session/locale", { state: state.session, locale });
    applySessionPayload(payload);
    await refreshReport();
    if (!$("#reportPanel").hidden && state.report) {
      $("#reportContent").innerHTML = renderReportV2(state.report);
    }
    if ($("#helpDialog")?.open) {
      InfoDialog(state.currentHelpTopic);
    }
  } catch (error) {
    showErrorState(`${t("apiError")} ${error.message}`);
  }
}

async function loadCapabilities() {
  try {
    const response = await fetch("/api/capabilities");
    state.capabilities = await response.json();
    $("#offlineBanner").hidden = true;
  } catch {
    state.capabilities = { mode: "offline" };
    $("#offlineBanner").hidden = false;
  }
  renderAiStatus();
}

function renderAiStatus() {
  const element = $("#aiStatusLine");
  if (!element) return;
  const caps = state.capabilities || {};
  if (caps.mode === "offline") {
    element.textContent = repairText(t("aiModeOffline"));
    element.dataset.mode = "offline";
    return;
  }
  const providers = caps.llm?.providers || [];
  if (caps.llm?.enabled && providers.length) {
    element.textContent = repairText(t("aiModeActive")).replace("{providers}", providers.join(", "));
    element.dataset.mode = "ai";
    return;
  }
  element.textContent = repairText(t("aiModeLocal"));
  element.dataset.mode = "local";
}

async function loadTrainingCases() {
  try {
    const data = await getJson("content/training_cases/cases.json");
    state.cases = Array.isArray(data) ? data : [];
  } catch {
    state.cases = [];
  }
  renderTrainingCases();
}

function renderTrainingCases() {
  const select = $("#trainingSelect");
  select.innerHTML = `<option value="">${escapeHtml(t("trainingEmpty"))}</option>`;
  for (const item of state.cases) {
    const title = repairText(item[`title_${state.locale}`] || item.title_ca || item.id);
    select.insertAdjacentHTML("beforeend", `<option value="${escapeHtml(item.id)}">${escapeHtml(title)}</option>`);
  }
}

function loadSelectedCase() {
  const selected = state.cases.find((item) => item.id === $("#trainingSelect").value);
  if (!selected) return;
  const brief = repairText(selected[`brief_${state.locale}`] || selected.brief_ca || "");
  $("#freeTextInput").value = brief;
  $("#profileSelect").value = selected.profile || $("#profileSelect").value;
  startSession("training");
}

async function startSession(mode = "demo") {
  state.lastMode = mode;
  state.selectedAnswer = null;
  $("#statusLine").textContent = t("statusLoading");
  $("#reportPanel").hidden = true;
  $("#noteInput").value = "";
  ProfessionalNotes();
  state.report = null;
  state.facts = [];
  renderFactList();
  setCopy();
  updateReportAction();

  try {
    const payload = await api("/api/session/start", {
      profile: $("#profileSelect").value,
      locale: state.locale,
      mode
    });
    $("#offlineBanner").hidden = true;
    applySessionPayload(payload);
    await refreshReport();
    $("#statusLine").textContent = t("statusReady");
  } catch (error) {
    showErrorState(`${t("apiError")} ${error.message}`);
  }
}

function applySessionPayload(payload) {
  state.session = payload.state;
  state.currentNode = payload.currentNode;
  state.progress = payload.progress;
  JourneySidebar();
  QuestionCard();
}

function renderCurrentNode() {
  const node = state.currentNode;
  if (!node) {
    $("#domainPill").textContent = t("domains.review");
    $("#priorityPill").textContent = t("priority.preventive");
    $("#priorityPill").dataset.attention = "preventive";
    $("#questionText").textContent = t("statusComplete");
    $("#helpText").textContent = "";
    $("#answerPanel").innerHTML = "";
    $("#statusLine").textContent = t("statusComplete");
    updateReportAction();
    return;
  }

  QuestionHeader(node);
  $("#questionText").textContent = repairText(node.question);
  $("#helpText").textContent = repairText(node.help || "");
  $("#noteInput").value = "";
  ProfessionalNotes();
  state.selectedAnswer = null;
  $("#answerPanel").innerHTML = node.answers.map((answer) => AnswerOption(answer, node)).join("");
  document.querySelectorAll(".answerOption").forEach((button) => {
    button.addEventListener("click", () => submitAnswer(button.dataset.answer));
  });
  updateReportAction();
}

async function submitAnswer(answerId) {
  if (!state.session) return;
  state.selectedAnswer = answerId;
  renderSelectedAnswerState();
  setAnswerButtonsDisabled(true);

  try {
    const payload = await api("/api/session/answer", {
      state: state.session,
      answer_id: answerId,
      note: $("#noteInput").value
    });
    applySessionPayload(payload);
    await refreshReport();
    $("#statusLine").textContent = t("answerSaved");
    if (state.currentNode?.id === "review_free_text_01") {
      $("#freeTextInput").focus();
    }
  } catch (error) {
    $("#statusLine").textContent = repairText(error.message);
    setAnswerButtonsDisabled(false);
  }
}

function renderSelectedAnswerState() {
  document.querySelectorAll(".answerOption").forEach((button) => {
    const selected = button.dataset.answer === state.selectedAnswer;
    button.classList.toggle("isSelected", selected);
    button.setAttribute("aria-pressed", String(selected));
  });
}

function setAnswerButtonsDisabled(disabled) {
  document.querySelectorAll(".answerOption").forEach((button) => {
    button.disabled = disabled;
  });
}

async function refreshReport() {
  if (!state.session) return;
  try {
    state.report = await api("/api/report", { state: state.session, confirmed_facts: [] });
    $("#reviewStatus").textContent = canGenerateReport() ? t("reviewReady") : t("reviewPending");
    ContextPanel();
  } catch (error) {
    $("#statusLine").textContent = repairText(error.message);
  }
}

function renderReview() {
  const report = state.report;
  AttentionNotice(report);
  IndicatorsPanel(report);
  RecommendationsPanel(report);
  PendingAreasPanel(report);
  SourcesPanel(report);
  LimitationsPanel(report);
  updateReportAction();
}

function renderStack(selector, items, emptyMarkup, template) {
  const target = $(selector);
  const listItems = Array.isArray(items) ? items.filter(Boolean) : [];
  if (!listItems.length) {
    target.innerHTML = emptyMarkup;
    return;
  }
  target.innerHTML = listItems.map(template).join("");
}

async function extractFacts() {
  const value = $("#freeTextInput").value.trim();
  if (!value) {
    state.facts = [];
    renderFactList();
    return;
  }
  $("#extractFactsButton").disabled = true;
  $("#extractFactsButton").classList.add("isLoading");
  try {
    const data = await api("/api/text/facts", { text: value, locale: state.locale });
    state.facts = [...(data.facts || []), ...(data.observations || [])].slice(0, 8).map(repairText);
    renderFactList();
  } catch (error) {
    $("#factList").innerHTML = EmptyState("AV", repairText(error.message), "");
  } finally {
    $("#extractFactsButton").disabled = false;
    $("#extractFactsButton").classList.remove("isLoading");
  }
}

function renderFactList() {
  if (!state.facts.length) {
    $("#factList").innerHTML = EmptyState("FT", t("noFacts"), "");
    return;
  }
  $("#factList").innerHTML = state.facts.map((fact, index) => `
    <label class="factItem">
      <input type="checkbox" value="${index}" checked>
      <span>${escapeHtml(repairText(fact))}</span>
    </label>
  `).join("");
}

async function addSelectedFacts() {
  const selected = Array.from(document.querySelectorAll("#factList input:checked"))
    .map((input) => state.facts[Number(input.value)])
    .filter(Boolean);
  if (!selected.length || !state.session) return;
  try {
    const payload = await api("/api/session/facts", { state: state.session, facts: selected });
    applySessionPayload(payload);
    await refreshReport();
  } catch (error) {
    $("#statusLine").textContent = repairText(error.message);
  }
}

async function generateReport() {
  if (!state.session) return;
  await refreshReport();
  const report = state.report;
  if (!report) return;
  $("#reportPanel").hidden = false;
  $("#reportContent").innerHTML = renderReportV2(report);
  $("#reviewStatus").textContent = canGenerateReport() ? t("reviewReady") : t("reviewPending");
  $("#reportPanel").scrollIntoView({ behavior: reducedMotion() ? "auto" : "smooth", block: "start" });
}

function renderReport(report) {
  const labels = t("reportSections", text.ca.reportSections);
  return [
    reportBox(t("reportNoticeTitle"), `<p>${escapeHtml(repairText(report.mandatory_disclaimer || ""))}</p>`, "full"),
    reportBox(labels.facts, list(report.facts_confirmed), "full"),
    reportBox(labels.indicators, list(report.indicators?.map((item) => `${repairText(item.label)}: ${repairText(item.rationale)}`))),
    reportBox(labels.pending, list(report.pending_questions)),
    reportBox(labels.recommendations, list(report.recommendations?.map((item) => repairText(item.text))), "full"),
    reportBox(labels.resources, list(report.resources?.map((item) => `${repairText(item.name)}: ${repairText(item.description)}`))),
    reportBox(labels.sources, list(report.sources?.map((item) => `${repairText(item.organism)}. ${repairText(item.title)} (${repairText(item.status)})`))),
    reportBox(labels.limits, list(report.limitations), "full"),
    reportBox(labels.audit, list([
      `${t("auditSessionId")}: ${report.session_id}`,
      `${t("auditTreeVersion")}: ${report.audit?.tree_version}`,
      `${t("auditDataMode")}: ${humanReportValue(report.audit?.data_mode)}`,
      `${t("auditHumanReview")}: ${report.audit?.human_review_required ? t("yesLower") : t("noLower")}`
    ]), "full")
  ].join("");
}

function reportBox(title, body, extraClass = "") {
  return `<section class="reportSection ${extraClass}"><h3>${escapeHtml(repairText(title))}</h3>${body}</section>`;
}

function list(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return `<p class="emptyText">-</p>`;
  return `<ul>${clean.map((item) => `<li>${escapeHtml(repairText(item))}</li>`).join("")}</ul>`;
}

function renderReportV2(report) {
  const labels = t("reportSections", text.ca.reportSections);
  return [
    renderReportDocumentHeader(report),
    reportBox(t("reportNoticeTitle"), `<p>${escapeHtml(repairText(report.mandatory_disclaimer || ""))}</p>`, "full noticeReportSection"),
    reportBox(labels.facts, renderAnswerRecords(), "full answersReportSection"),
    reportBox(labels.indicators, renderIndicatorReportItems(report.indicators), "full"),
    reportBox(labels.pending, renderPendingReportItems(report.pending_questions), "full"),
    reportBox(labels.recommendations, renderRecommendationReportItems(report.recommendations), "full recommendationsReportSection"),
    reportBox(labels.resources, renderResourceReportItems(report.resources), "full"),
    reportBox(labels.sources, renderSourceReportItems(report.sources), "full"),
    reportBox(labels.limits, reportList(report.limitations, t("reportLimitationsEmpty")), "full limitationsReportSection"),
    reportBox(labels.audit, auditList(report), "full auditReportSection")
  ].join("");
}

function renderReportDocumentHeader(report) {
  return `
    <section class="reportDocumentHeader">
      <div class="reportBrandLine">
        <img src="assets/lucerna-mark.svg" alt="" class="reportMark">
        <div>
          <strong>LUCERNA 65</strong>
          <span>${escapeHtml(t("headerSubline"))}</span>
        </div>
      </div>
      <div class="reportMetaLine">
        <h3>${escapeHtml(t("reportDocumentTitle"))}</h3>
        <dl>
          <div><dt>${escapeHtml(t("reportGeneratedAt"))}</dt><dd>${escapeHtml(formatReportDate(report.generated_at))}</dd></div>
          <div><dt>${escapeHtml(t("reportSessionId"))}</dt><dd>${escapeHtml(report.session_id || "-")}</dd></div>
          <div><dt>${escapeHtml(t("reportStatus"))}</dt><dd>${escapeHtml(t("reportStatusReviewable"))}</dd></div>
        </dl>
      </div>
    </section>
  `;
}

function renderAnswerRecords() {
  const answered = state.session?.answered || [];
  if (!answered.length) return `<p class="emptyText">${escapeHtml(t("reportAnswersEmpty"))}</p>`;
  return answered.map((record) => `
    <article class="answerReportItem">
      <p>${escapeHtml(repairText(record.question || ""))}</p>
      <strong>${escapeHtml(humanReportValue(record.answer_id, record.answer_label))}</strong>
      ${record.note ? `<small>${escapeHtml(t("reportObservation"))}: ${escapeHtml(repairText(record.note))}</small>` : ""}
    </article>
  `).join("");
}

function renderIndicatorReportItems(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return `<p class="emptyText">${escapeHtml(t("emptyIndicators"))}</p>`;
  return clean.map((item) => `
    <article class="indicatorReportItem" data-severity="${escapeHtml(item.severity || "medium")}">
      <h4>${escapeHtml(repairText(item.label || ""))}</h4>
      <p>${escapeHtml(repairText(item.rationale || ""))}</p>
    </article>
  `).join("");
}

function renderPendingReportItems(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) {
    const complete = Boolean(state.session?.complete);
    return `<p class="emptyText">${escapeHtml(complete ? t("pendingNoneComplete") : t("pendingIncomplete"))}</p>`;
  }
  return reportList(clean);
}

function renderRecommendationReportItems(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return `<p class="emptyText">${escapeHtml(t("emptyRecommendations"))}</p>`;
  return clean.map((item) => {
    const urgent = item.priority === "urgent";
    return `
      <article class="recommendationReportItem ${urgent ? "isUrgent" : ""}">
        <strong>${urgent ? escapeHtml(t("urgentActionLabel")) : escapeHtml(humanReportValue(item.priority))}</strong>
        <p>${escapeHtml(repairText(item.text || ""))}</p>
        ${item.rationale ? `<small>${escapeHtml(repairText(item.rationale))}</small>` : ""}
      </article>
    `;
  }).join("");
}

function renderResourceReportItems(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return `<p class="emptyText">${escapeHtml(t("resourcesEmpty"))}</p>`;
  return clean.map((item) => `
    <article class="sourceReportItem">
      <h4>${escapeHtml(repairText(item.name || ""))}</h4>
      <p>${escapeHtml(repairText(item.description || ""))}</p>
      <small>${escapeHtml(repairText(item.territory || ""))} · ${escapeHtml(humanReportStatus(item.verification_status))}. ${escapeHtml(t("sourceVerificationNote"))}</small>
    </article>
  `).join("");
}

function renderSourceReportItems(items) {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return `<p class="emptyText">${escapeHtml(t("sourcesEmpty"))}</p>`;
  return clean.map((item) => `
    <article class="sourceReportItem">
      <h4>${escapeHtml(repairText(item.organism || t("sourceUnknownOrganism")))}</h4>
      <p>${escapeHtml(repairText(item.title || ""))}</p>
      <small>${escapeHtml(t("sourceVersionLabel"))}: ${escapeHtml(humanReportStatus(item.version))} · ${escapeHtml(t("sourceStatusLabel"))}: ${escapeHtml(humanReportStatus(item.status))}. ${escapeHtml(t("sourceVerificationNote"))}</small>
    </article>
  `).join("");
}

function auditList(report) {
  return reportList([
    `${t("auditSessionId")}: ${report.session_id || "-"}`,
    `${t("auditTreeVersion")}: ${report.audit?.tree_version || "-"}`,
    `${t("auditDataMode")}: ${humanReportValue(report.audit?.data_mode) || "-"}`,
    `${t("auditHumanReview")}: ${report.audit?.human_review_required ? t("yesLower") : t("noLower")}`
  ]);
}

function reportList(items, emptyText = "-") {
  const clean = (items || []).filter(Boolean);
  if (!clean.length) return `<p class="emptyText">${escapeHtml(emptyText)}</p>`;
  return `<ul>${clean.map((item) => `<li>${escapeHtml(repairText(item))}</li>`).join("")}</ul>`;
}

function humanReportValue(value, fallback = "") {
  const raw = String(value ?? "");
  const cleaned = repairText(fallback || raw);
  const labels = t("valueLabels", pdfValueLabels);
  if (labels[raw]) return labels[raw];
  if (labels[cleaned]) return labels[cleaned];
  if (cleaned && cleaned !== raw && !cleaned.includes("?")) return cleaned;
  return raw.replaceAll("_", " ").trim() || cleaned;
}

function humanReportStatus(value) {
  const raw = String(value ?? "");
  const cleaned = repairText(raw);
  const labels = t("statusLabels", pdfStatusLabels);
  return labels[raw] || labels[cleaned] || humanReportValue(cleaned);
}

function formatReportDate(value) {
  const localeMap = { ca: "ca-ES", es: "es-ES", en: "en-GB" };
  const activeLocale = localeMap[state.locale] || "ca-ES";
  if (!value) return new Date().toLocaleString(activeLocale, { dateStyle: "short", timeStyle: "short" });
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return repairText(value);
  return parsed.toLocaleString(activeLocale, { dateStyle: "short", timeStyle: "short" });
}

function downloadReport() {
  if (!state.report) return;
  const blob = new Blob([JSON.stringify(state.report, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const anchor = document.createElement("a");
  anchor.href = url;
  anchor.download = `lucerna65-${state.report.session_id || "report"}.json`;
  anchor.click();
  URL.revokeObjectURL(url);
}

function answerLabel(answer) {
  return t(`answerLabels.${answer.id}`, repairText(answer.label));
}

function answerDescription(answer, node) {
  if (node?.id === "Q001" && answer.id === "yes") return t("answerDescriptions.yesSafe");
  if (node?.id === "Q001" && answer.id === "no") return t("answerDescriptions.noWarning");
  if (node?.id === "Q001" && answer.id === "unknown") return t("answerDescriptions.unknownWarning");
  if (answer.actions?.includes("ACTION_URGENT_SAFE")) return t("answerDescriptions.yesSafe");
  if (answer.id === "yes" && answer.tone === "danger") return t("answerDescriptions.yesDanger");
  if (answer.id === "no" && answer.tone === "warning") return t("answerDescriptions.noWarning");
  if (answer.id === "unknown" && answer.tone === "warning") return t("answerDescriptions.unknownWarning");
  return t(`answerDescriptions.${answer.id}`, t("answerDescriptions.yes"));
}

function answerIcon(answer, tone) {
  if (tone === "danger") return "!";
  if (tone === "warning") return "?";
  if (answer.id === "yes") return "✓";
  if (answer.id === "no") return "○";
  return "?";
}

function visualTone(answer, node) {
  const tone = answer.tone || "neutral";
  if (node?.id === "Q001" && answer.id === "yes") return "neutral";
  if (node?.id === "Q001" && (answer.id === "no" || answer.id === "unknown")) return "warning";
  if (answer.actions?.includes("ACTION_URGENT_SAFE")) return "neutral";
  if (tone === "danger" || node?.priority === "urgent") return tone === "neutral" ? "neutral" : "danger";
  if (tone === "warning") return "warning";
  return "neutral";
}

function priorityMeta(value) {
  const raw = value || "exploratory";
  const key = raw === "high" || raw === "priority" ? "priority"
    : raw === "medium" || raw === "scheduled" ? "scheduled"
    : raw === "urgent" ? "urgent"
    : raw === "preventive" ? "preventive"
    : "exploratory";
  return {
    key,
    label: t(`priority.${raw}`, t(`priority.${key}`, raw)),
    panelLabel: key === "urgent" ? "Nivell d'atenció orientatiu urgent"
      : key === "priority" ? "Nivell d'atenció orientatiu prioritari"
      : key === "scheduled" ? "Nivell d'atenció orientatiu de seguiment"
      : "Nivell d'atenció orientatiu preventiu"
  };
}

function currentDomainKey() {
  const node = state.currentNode;
  if (!node) return "review";
  if (node.id === "Q010" || node.id === "Q011") return "context_privacy";
  const match = DOMAIN_NAVIGATION.find((item) => item.domains.includes(node.domain));
  return match?.key || node.domain || "context_privacy";
}

function canGenerateReport() {
  return Boolean(state.session && state.report && (state.progress?.answered || 0) > 0);
}

function updateReportAction() {
  const enabled = canGenerateReport();
  const button = $("#reportButton");
  button.disabled = !enabled;
  button.setAttribute("aria-disabled", String(!enabled));
  button.title = enabled ? t("reportButton") : t("enoughInfoNeeded");
}

function showErrorState(message) {
  $("#offlineBanner").hidden = false;
  $("#statusLine").textContent = message || t("statusExpired");
  $("#domainPill").textContent = t("domains.review");
  $("#priorityPill").textContent = t("statusExpired");
  $("#questionText").textContent = t("statusExpired");
  $("#helpText").textContent = t("offlineText");
  $("#answerPanel").innerHTML = EmptyState("AV", t("apiError"), message || "");
  updateReportAction();
}

function showDialog(selector) {
  const dialog = $(selector);
  if (dialog?.open) return;
  if (dialog?.showModal) {
    dialog.showModal();
  } else if (dialog) {
    dialog.setAttribute("open", "");
  }
}

function closeDialog(selector) {
  const dialog = $(selector);
  if (dialog?.close) {
    dialog.close();
  } else if (dialog) {
    dialog.removeAttribute("open");
  }
}

function reducedMotion() {
  return window.matchMedia("(prefers-reduced-motion: reduce)").matches;
}

async function downloadPdf() {
  if (!state.session || !state.report) return;
  const button = $("#printButton");
  button.disabled = true;
  button.classList.add("isLoading");
  try {
    const response = await fetch("/api/report/pdf", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ state: state.session, confirmed_facts: [] })
    });
    if (!response.ok) throw new Error(response.statusText);
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = `lucerna65-${state.report.session_id || "informe"}.pdf`;
    anchor.click();
    URL.revokeObjectURL(url);
  } catch (error) {
    $("#statusLine").textContent = `${t("apiError")} ${repairText(error.message)}`;
    window.print();
  } finally {
    button.disabled = false;
    button.classList.remove("isLoading");
  }
}

boot();
