"""PDF presentation layer for LUCERNA 65 reports."""

from __future__ import annotations

from datetime import datetime
from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.platypus import Flowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
from xml.sax.saxutils import escape

PRIMARY = colors.HexColor("#174f4c")
PRIMARY_DARK = colors.HexColor("#103d3b")
PRIMARY_SOFT = colors.HexColor("#dfece8")
BACKGROUND = colors.HexColor("#ffffff")
SURFACE_ALT = colors.HexColor("#faf8f3")
BORDER = colors.HexColor("#d9ddd8")
TEXT = colors.HexColor("#183033")
TEXT_MUTED = colors.HexColor("#667578")
WARNING_BG = colors.HexColor("#f6ecdc")
DANGER = colors.HexColor("#a8473f")
DANGER_SOFT = colors.HexColor("#f8e9e6")
GREY_BOX = colors.HexColor("#f1f2ef")

DOMAIN_LABELS = {
    "urgent_safety": "Seguretat immediata",
    "safety": "Seguretat",
    "normalization": "Context i normalització",
    "psychological": "Psicològic",
    "social_isolation": "Social",
    "social": "Social",
    "physical": "Físic",
    "institutional": "Institucional",
    "digital": "Digital",
    "economic": "Econòmic",
    "care_and_health": "Cures i salut",
    "care": "Cures",
    "sexual": "Sexual",
    "autonomy_erosion": "Autonomia",
}

VALUE_LABELS = {
    "yes": "Sí",
    "no": "No",
    "partial": "Parcialment",
    "unknown": "No consta",
    "skip": "No consta",
    "free_text": "Text lliure",
    "ephemeral": "Efímer",
    "demo": "Demo",
    "interview": "Entrevista",
    "review": "Revisió",
    "training": "Formació",
    "other_person": "Decisió d'una altra persona",
    "other": "Altres",
    "not_applicable": "No aplicable",
    "not_now": "Ara no",
    "does_not_use": "No ho utilitza",
    "health": "Salut",
    "accessibility": "Accessibilitat",
    "resources": "Recursos",
    "mixed": "Mixt",
    "money": "Diners",
    "medication": "Medicació",
    "mobility": "Mobilitat",
    "housing": "Habitatge",
    "phone": "Telèfon",
    "visits": "Visites",
    "sex": "Sexualitat",
    "food": "Alimentació",
    "clothing": "Roba",
    "leisure": "Oci",
    "shopping": "Compres",
    "nothing": "Res",
    "questions": "Preguntes",
    "argument": "Discussió",
    "insults": "Insults",
    "threats": "Amenaces",
    "money_removed": "Retirada de diners",
    "physical_aggression": "Agressió física",
    "withheld_documents": "Retenció de documents",
    "yes_with_consent": "Sí, amb consentiment",
    "yes_without_clear_consent": "Sí, sense consentiment clar",
    "could_choose": "Podia escollir",
    "was_prevented": "Se li va impedir",
    "never_considered": "No s'ho havia plantejat",
    "has_alternatives": "Té alternatives",
    "limited_alternatives": "Alternatives limitades",
    "no_alternatives": "Sense alternatives",
    "discouraged": "Desànim o pressió",
    "prevented": "Impedida",
    "punished": "Càstig",
    "current": "Actual",
    "past_with_current_impact": "Passat amb impacte actual",
    "past_no_current_impact": "Passat sense impacte actual",
    "routine_checkup": "Revisió rutinària",
    "gynecology": "Ginecologia",
    "chronic_followup": "Seguiment crònic",
    "screening": "Cribratge",
    "diagnostic_test": "Prova diagnòstica",
    "yes_once": "Sí, una vegada",
    "yes_repeatedly": "Sí, repetidament",
    "often": "Sovint",
    "sometimes": "De vegades",
    "rarely": "Rarament",
    "never": "Mai",
    "cognitive": "Cognitiu",
    "lack_of_experience": "Manca d'experiència",
    "fear": "Por",
    "long_term_control": "Control sostingut",
    "direct_statement": "Relat directe",
    "professional_observation": "Observació professional",
    "third_party_report": "Relat de terceres persones",
    "document": "Document",
    "privacy": "Privacitat",
    "time": "Temps",
    "communication": "Comunicació",
    "refusal": "Rebuig",
    "third_party_present": "Tercera persona present",
}

STATUS_LABELS = {
    "pending": "Pendent de verificació",
    "placeholder": "Pendent de verificació",
    "pendent_ingestio": "Pendent d'ingestió",
    "pendent_ingestio_i_verificacio": "Pendent d'ingestió i verificació",
    "pendent_identificar_versio_vigent": "Pendent d'identificar la versió vigent",
    "pendent_verificacio": "Pendent de verificació",
    "actualitzacio_continua": "Actualització contínua",
    "vigent_a_verificar": "Vigent a verificar",
    "aplicacio_esglaonada_a_verificar": "Aplicació esglaonada a verificar",
}

LIMITATIONS = [
    "El resultat és orientatiu.",
    "No és un diagnòstic.",
    "No és un peritatge.",
    "No és una denúncia.",
    "No és una resolució administrativa.",
    "Les decisions corresponen a la professional i al circuit del servei.",
    "Les fonts i recursos s'han de verificar abans d'utilitzar casos reals.",
]


SUPPORTED_LOCALES = {"ca", "es", "en"}

PDF_COPY = {
    "ca": {
        "document_title": "LUCERNA 65 - Informe orientatiu",
        "brand_subtitle": "Suport professional orientatiu",
        "report_title": "Informe orientatiu",
        "report_subtitle": "Informació orientativa pendent de revisió professional.",
        "generated_at": "Data de generació",
        "session_id": "Identificador de sessió",
        "status": "Estat",
        "reviewable_status": "Revisable abans de compartir o arxivar",
        "notice_title": "Avís",
        "notice_default": (
            "Aquest document és una guia de suport. No constitueix diagnòstic, peritatge, "
            "denúncia, resolució administrativa ni acreditació de violència."
        ),
        "sections": {
            "answers": "Respostes recollides",
            "indicators": "Indicadors a considerar",
            "pending": "Preguntes o àrees pendents",
            "recommendations": "Recomanacions",
            "resources": "Recursos",
            "sources": "Fonts",
            "limitations": "Limitacions",
            "audit": "Auditoria",
        },
        "answers_empty": "Encara no consten respostes recollides.",
        "answer_prefix": "Resposta",
        "observation_prefix": "Observació",
        "examples_prefix": "Exemples",
        "indicators_empty": "Encara no hi ha indicadors actius.",
        "pending_complete": "No consten àrees pendents en l'itinerari completat.",
        "pending_incomplete": "Hi ha àrees que no s'han pogut explorar amb la informació disponible.",
        "recommendations_empty": "Les recomanacions apareixeran quan hi hagi prou context.",
        "urgent_action": "Actuació prioritària segons protocol aplicable",
        "resources_empty": "No consten recursos associats en aquest moment.",
        "sources_empty": "No consten fonts associades en aquest moment.",
        "territory": "Territori",
        "verification_note": "Pendent de verificació per a ús en casos reals.",
        "unknown_source": "Font pendent d'organisme",
        "version": "Versió",
        "status_label": "Estat",
        "limitations_base": [
            "El resultat és orientatiu.",
            "No és un diagnòstic.",
            "No és un peritatge.",
            "No és una denúncia.",
            "No és una resolució administrativa.",
            "Les decisions corresponen a la professional i al circuit del servei.",
            "Les fonts i recursos s'han de verificar abans d'utilitzar casos reals.",
            "En aquest mode demo no s'han guardat dades personals al servidor.",
        ],
        "audit_session_id": "Identificador de sessió",
        "audit_tree_version": "Versió de l'arbre",
        "audit_data_mode": "Mode de dades",
        "audit_human_review": "Revisió humana",
        "yes": "Sí",
        "no": "No",
        "footer": "LUCERNA 65 · Informe orientatiu · Pàgina {page} de {pages}",
    },
    "es": {
        "document_title": "LUCERNA 65 - Informe orientativo",
        "brand_subtitle": "Apoyo profesional orientativo",
        "report_title": "Informe orientativo",
        "report_subtitle": "Información orientativa pendiente de revisión profesional.",
        "generated_at": "Fecha de generación",
        "session_id": "Identificador de sesión",
        "status": "Estado",
        "reviewable_status": "Revisable antes de compartir o archivar",
        "notice_title": "Aviso",
        "notice_default": (
            "Este documento es una guía de apoyo. No constituye diagnóstico, peritaje, "
            "denuncia, resolución administrativa ni acreditación de violencia."
        ),
        "sections": {
            "answers": "Respuestas recogidas",
            "indicators": "Indicadores a considerar",
            "pending": "Preguntas o áreas pendientes",
            "recommendations": "Recomendaciones",
            "resources": "Recursos",
            "sources": "Fuentes",
            "limitations": "Limitaciones",
            "audit": "Auditoría",
        },
        "answers_empty": "Aún no constan respuestas recogidas.",
        "answer_prefix": "Respuesta",
        "observation_prefix": "Observación",
        "examples_prefix": "Ejemplos",
        "indicators_empty": "Aún no hay indicadores activos.",
        "pending_complete": "No constan áreas pendientes en el itinerario completado.",
        "pending_incomplete": "Hay áreas que no se han podido explorar con la información disponible.",
        "recommendations_empty": "Las recomendaciones aparecerán cuando haya suficiente contexto.",
        "urgent_action": "Actuación prioritaria según el protocolo aplicable",
        "resources_empty": "No constan recursos asociados en este momento.",
        "sources_empty": "No constan fuentes asociadas en este momento.",
        "territory": "Territorio",
        "verification_note": "Pendiente de verificación para uso en casos reales.",
        "unknown_source": "Fuente pendiente de organismo",
        "version": "Versión",
        "status_label": "Estado",
        "limitations_base": [
            "El resultado es orientativo.",
            "No es un diagnóstico.",
            "No es un peritaje.",
            "No es una denuncia.",
            "No es una resolución administrativa.",
            "Las decisiones corresponden a la profesional y al circuito del servicio.",
            "Las fuentes y recursos deben verificarse antes de utilizar casos reales.",
            "En este modo demo no se han guardado datos personales en el servidor.",
        ],
        "audit_session_id": "Identificador de sesión",
        "audit_tree_version": "Versión del árbol",
        "audit_data_mode": "Modo de datos",
        "audit_human_review": "Revisión humana",
        "yes": "Sí",
        "no": "No",
        "footer": "LUCERNA 65 · Informe orientativo · Página {page} de {pages}",
    },
    "en": {
        "document_title": "LUCERNA 65 - Orientative report",
        "brand_subtitle": "Professional orientation support",
        "report_title": "Orientative report",
        "report_subtitle": "Orientative information pending professional review.",
        "generated_at": "Generated on",
        "session_id": "Session identifier",
        "status": "Status",
        "reviewable_status": "Review before sharing or filing",
        "notice_title": "Notice",
        "notice_default": (
            "This document is a support guide. It is not a diagnosis, expert opinion, "
            "complaint, administrative decision or certification of violence."
        ),
        "sections": {
            "answers": "Collected answers",
            "indicators": "Indicators to consider",
            "pending": "Pending questions or areas",
            "recommendations": "Recommendations",
            "resources": "Resources",
            "sources": "Sources",
            "limitations": "Limitations",
            "audit": "Audit",
        },
        "answers_empty": "No collected answers are recorded yet.",
        "answer_prefix": "Answer",
        "observation_prefix": "Observation",
        "examples_prefix": "Examples",
        "indicators_empty": "There are no active indicators yet.",
        "pending_complete": "No pending areas are recorded in the completed pathway.",
        "pending_incomplete": "Some areas could not be explored with the available information.",
        "recommendations_empty": "Recommendations will appear when there is enough context.",
        "urgent_action": "Priority action according to the applicable protocol",
        "resources_empty": "No associated resources are recorded at this time.",
        "sources_empty": "No associated sources are recorded at this time.",
        "territory": "Territory",
        "verification_note": "Pending verification for use in real cases.",
        "unknown_source": "Source pending organization",
        "version": "Version",
        "status_label": "Status",
        "limitations_base": [
            "The result is orientative.",
            "It is not a diagnosis.",
            "It is not an expert opinion.",
            "It is not a complaint.",
            "It is not an administrative decision.",
            "Decisions belong to the professional and the service pathway.",
            "Sources and resources must be verified before use in real cases.",
            "In this demo mode, no personal data has been stored on the server.",
        ],
        "audit_session_id": "Session identifier",
        "audit_tree_version": "Tree version",
        "audit_data_mode": "Data mode",
        "audit_human_review": "Human review",
        "yes": "Yes",
        "no": "No",
        "footer": "LUCERNA 65 · Orientative report · Page {page} of {pages}",
    },
}

DOMAIN_LABELS_BY_LOCALE = {
    "ca": DOMAIN_LABELS,
    "es": {
        "urgent_safety": "Seguridad inmediata",
        "safety": "Seguridad",
        "normalization": "Contexto y normalización",
        "psychological": "Psicológico",
        "social_isolation": "Social",
        "social": "Social",
        "physical": "Físico",
        "institutional": "Institucional",
        "digital": "Digital",
        "economic": "Económico",
        "care_and_health": "Cuidados y salud",
        "care": "Cuidados",
        "sexual": "Sexual",
        "autonomy_erosion": "Autonomía",
    },
    "en": {
        "urgent_safety": "Immediate safety",
        "safety": "Safety",
        "normalization": "Context and normalization",
        "psychological": "Psychological",
        "social_isolation": "Social",
        "social": "Social",
        "physical": "Physical",
        "institutional": "Institutional",
        "digital": "Digital",
        "economic": "Economic",
        "care_and_health": "Care and health",
        "care": "Care",
        "sexual": "Sexual",
        "autonomy_erosion": "Autonomy",
    },
}

VALUE_LABELS_BY_LOCALE = {
    "ca": VALUE_LABELS,
    "es": {
        "yes": "Sí",
        "no": "No",
        "partial": "Parcialmente",
        "unknown": "No consta",
        "skip": "No consta",
        "free_text": "Texto libre",
        "ephemeral": "Efímero",
        "demo": "Demo",
        "interview": "Entrevista",
        "review": "Revisión",
        "training": "Formación",
        "other_person": "Decisión de otra persona",
        "other": "Otros",
        "not_applicable": "No aplicable",
        "not_now": "Ahora no",
        "does_not_use": "No lo utiliza",
        "health": "Salud",
        "accessibility": "Accesibilidad",
        "resources": "Recursos",
        "mixed": "Mixto",
        "money": "Dinero",
        "medication": "Medicación",
        "mobility": "Movilidad",
        "housing": "Vivienda",
        "phone": "Teléfono",
        "visits": "Visitas",
        "sex": "Sexualidad",
        "food": "Alimentación",
        "clothing": "Ropa",
        "leisure": "Ocio",
        "shopping": "Compras",
        "nothing": "Nada",
        "questions": "Preguntas",
        "argument": "Discusión",
        "insults": "Insultos",
        "threats": "Amenazas",
        "money_removed": "Retirada de dinero",
        "physical_aggression": "Agresión física",
        "withheld_documents": "Retención de documentos",
        "yes_with_consent": "Sí, con consentimiento",
        "yes_without_clear_consent": "Sí, sin consentimiento claro",
        "could_choose": "Podía escoger",
        "was_prevented": "Se le impidió",
        "never_considered": "No se lo había planteado",
        "has_alternatives": "Tiene alternativas",
        "limited_alternatives": "Alternativas limitadas",
        "no_alternatives": "Sin alternativas",
        "discouraged": "Desánimo o presión",
        "prevented": "Impedida",
        "punished": "Castigo",
        "current": "Actual",
        "past_with_current_impact": "Pasado con impacto actual",
        "past_no_current_impact": "Pasado sin impacto actual",
        "routine_checkup": "Revisión rutinaria",
        "gynecology": "Ginecología",
        "chronic_followup": "Seguimiento crónico",
        "screening": "Cribado",
        "diagnostic_test": "Prueba diagnóstica",
        "yes_once": "Sí, una vez",
        "yes_repeatedly": "Sí, repetidamente",
        "often": "A menudo",
        "sometimes": "A veces",
        "rarely": "Raramente",
        "never": "Nunca",
        "cognitive": "Cognitivo",
        "lack_of_experience": "Falta de experiencia",
        "fear": "Miedo",
        "long_term_control": "Control sostenido",
        "direct_statement": "Relato directo",
        "professional_observation": "Observación profesional",
        "third_party_report": "Relato de terceras personas",
        "document": "Documento",
        "privacy": "Privacidad",
        "time": "Tiempo",
        "communication": "Comunicación",
        "refusal": "Rechazo",
        "third_party_present": "Tercera persona presente",
        "urgent": "Urgente",
        "priority": "Prioritario",
        "high": "Prioritario",
        "scheduled": "Seguimiento",
        "medium": "Seguimiento",
        "preventive": "Preventivo",
        "low": "Bajo",
    },
    "en": {
        "yes": "Yes",
        "no": "No",
        "partial": "Partially",
        "unknown": "Not known",
        "skip": "Not known",
        "free_text": "Free text",
        "ephemeral": "Ephemeral",
        "demo": "Demo",
        "interview": "Interview",
        "review": "Review",
        "training": "Training",
        "other_person": "Decision by another person",
        "other": "Other",
        "not_applicable": "Not applicable",
        "not_now": "Not now",
        "does_not_use": "Does not use it",
        "health": "Health",
        "accessibility": "Accessibility",
        "resources": "Resources",
        "mixed": "Mixed",
        "money": "Money",
        "medication": "Medication",
        "mobility": "Mobility",
        "housing": "Housing",
        "phone": "Phone",
        "visits": "Visits",
        "sex": "Sexuality",
        "food": "Food",
        "clothing": "Clothing",
        "leisure": "Leisure",
        "shopping": "Shopping",
        "nothing": "Nothing",
        "questions": "Questions",
        "argument": "Argument",
        "insults": "Insults",
        "threats": "Threats",
        "money_removed": "Money removed",
        "physical_aggression": "Physical aggression",
        "withheld_documents": "Withheld documents",
        "yes_with_consent": "Yes, with consent",
        "yes_without_clear_consent": "Yes, without clear consent",
        "could_choose": "Could choose",
        "was_prevented": "Was prevented",
        "never_considered": "Had never considered it",
        "has_alternatives": "Has alternatives",
        "limited_alternatives": "Limited alternatives",
        "no_alternatives": "No alternatives",
        "discouraged": "Discouragement or pressure",
        "prevented": "Prevented",
        "punished": "Punished",
        "current": "Current",
        "past_with_current_impact": "Past, with current impact",
        "past_no_current_impact": "Past, no current impact",
        "routine_checkup": "Routine check-up",
        "gynecology": "Gynecology",
        "chronic_followup": "Chronic follow-up",
        "screening": "Screening",
        "diagnostic_test": "Diagnostic test",
        "yes_once": "Yes, once",
        "yes_repeatedly": "Yes, repeatedly",
        "often": "Often",
        "sometimes": "Sometimes",
        "rarely": "Rarely",
        "never": "Never",
        "cognitive": "Cognitive",
        "lack_of_experience": "Lack of experience",
        "fear": "Fear",
        "long_term_control": "Sustained control",
        "direct_statement": "Direct statement",
        "professional_observation": "Professional observation",
        "third_party_report": "Third-party account",
        "document": "Document",
        "privacy": "Privacy",
        "time": "Time",
        "communication": "Communication",
        "refusal": "Refusal",
        "third_party_present": "Third party present",
        "urgent": "Urgent",
        "priority": "Priority",
        "high": "Priority",
        "scheduled": "Follow-up",
        "medium": "Follow-up",
        "preventive": "Preventive",
        "low": "Low",
    },
}

STATUS_LABELS_BY_LOCALE = {
    "ca": STATUS_LABELS,
    "es": {
        "pending": "Pendiente de verificación",
        "placeholder": "Pendiente de verificación",
        "pendent_ingestio": "Pendiente de ingestión",
        "pendent_ingestio_i_verificacio": "Pendiente de ingestión y verificación",
        "pendent_identificar_versio_vigent": "Pendiente de identificar la versión vigente",
        "pendent_verificacio": "Pendiente de verificación",
        "actualitzacio_continua": "Actualización continua",
        "vigent_a_verificar": "Vigente a verificar",
        "aplicacio_esglaonada_a_verificar": "Aplicación escalonada a verificar",
    },
    "en": {
        "pending": "Pending verification",
        "placeholder": "Pending verification",
        "pendent_ingestio": "Pending ingestion",
        "pendent_ingestio_i_verificacio": "Pending ingestion and verification",
        "pendent_identificar_versio_vigent": "Pending identification of current version",
        "pendent_verificacio": "Pending verification",
        "actualitzacio_continua": "Continuous update",
        "vigent_a_verificar": "Current, to be verified",
        "aplicacio_esglaonada_a_verificar": "Staged application, to be verified",
    },
}


class LucernaMark(Flowable):
    width = 14 * mm
    height = 14 * mm

    def draw(self) -> None:
        c = self.canv
        c.setStrokeColor(PRIMARY_DARK)
        c.setFillColor(colors.HexColor("#f4efe7"))
        c.roundRect(0, 0, self.width, self.height, 2.5 * mm, stroke=0, fill=1)
        c.setStrokeColor(PRIMARY)
        c.setLineWidth(1.2)
        c.line(3 * mm, 4 * mm, 11 * mm, 4 * mm)
        c.roundRect(4.2 * mm, 4 * mm, 5.6 * mm, 6.7 * mm, 1 * mm, stroke=1, fill=0)
        c.line(3.2 * mm, 10.5 * mm, 10.8 * mm, 10.5 * mm)
        c.arc(5 * mm, 8.7 * mm, 9 * mm, 13 * mm, 0, 180)
        c.setFillColor(colors.HexColor("#d8a33a"))
        c.circle(7 * mm, 7 * mm, 1.8 * mm, stroke=0, fill=1)


class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, locale: str = "ca", **kwargs):
        super().__init__(*args, **kwargs)
        self.locale = _normalize_locale(locale)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        page_count = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_footer(page_count)
            super().showPage()
        super().save()

    def _draw_footer(self, page_count: int) -> None:
        self.saveState()
        self.setStrokeColor(BORDER)
        self.setLineWidth(0.35)
        self.line(20 * mm, 14 * mm, A4[0] - 20 * mm, 14 * mm)
        self.setFillColor(TEXT_MUTED)
        self.setFont("Helvetica", 8)
        self.drawCentredString(
            A4[0] / 2,
            9 * mm,
            _copy(self.locale, "footer").format(page=self._pageNumber, pages=page_count),
        )
        self.restoreState()


def render_report_pdf(report: dict, state: dict) -> bytes:
    locale = _report_locale(report, state)
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=20 * mm,
        title=_copy(locale, "document_title"),
        author="LUCERNA 65",
    )
    styles = _styles()
    story = []
    story.extend(_document_header(report, styles, doc.width, locale))
    story.extend(_notice_section(report, styles, doc.width, locale))
    story.extend(_answers_section(state, styles, doc.width, locale))
    story.extend(_indicators_section(report, styles, doc.width, locale))
    story.extend(_pending_section(report, state, styles, doc.width, locale))
    story.extend(_recommendations_section(report, styles, doc.width, locale))
    story.extend(_resources_section(report, styles, doc.width, locale))
    story.extend(_sources_section(report, styles, doc.width, locale))
    story.extend(_limitations_section(report, styles, doc.width, locale))
    story.extend(_audit_section(report, styles, doc.width, locale))
    doc.build(story, canvasmaker=lambda *args, **kwargs: NumberedCanvas(*args, locale=locale, **kwargs))
    return buffer.getvalue()


def _styles() -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    return {
        "brand": ParagraphStyle(
            "LucernaBrand",
            parent=base["Normal"],
            fontName="Times-Bold",
            fontSize=22,
            leading=24,
            textColor=PRIMARY_DARK,
            spaceAfter=1,
        ),
        "subtitle": ParagraphStyle(
            "LucernaSubtitle",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.6,
            leading=12,
            textColor=TEXT_MUTED,
        ),
        "title": ParagraphStyle(
            "DocumentTitle",
            parent=base["Title"],
            fontName="Times-Bold",
            fontSize=23,
            leading=27,
            textColor=PRIMARY_DARK,
            alignment=TA_CENTER,
            spaceBefore=8,
            spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=10.6,
            leading=15,
            textColor=TEXT,
            spaceAfter=5,
        ),
        "muted": ParagraphStyle(
            "Muted",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.2,
            leading=12.5,
            textColor=TEXT_MUTED,
        ),
        "meta": ParagraphStyle(
            "Meta",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=11.5,
            textColor=TEXT_MUTED,
            alignment=TA_RIGHT,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Times-Bold",
            fontSize=15.2,
            leading=18,
            textColor=PRIMARY,
            spaceBefore=12,
            spaceAfter=7,
            keepWithNext=True,
        ),
        "question": ParagraphStyle(
            "Question",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=9.7,
            leading=13.4,
            textColor=TEXT_MUTED,
            spaceAfter=2,
        ),
        "answer": ParagraphStyle(
            "Answer",
            parent=base["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10.2,
            leading=13.4,
            textColor=PRIMARY_DARK,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["BodyText"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=11.2,
            textColor=TEXT_MUTED,
        ),
    }


def _document_header(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    session_id = _clean(report.get("session_id") or "-", locale)
    generated_at = _format_date(report.get("generated_at"), locale)
    meta = (
        f"<b>{_e(_copy(locale, 'generated_at'), locale)}</b><br/>{_e(generated_at, locale)}<br/>"
        f"<b>{_e(_copy(locale, 'session_id'), locale)}</b><br/>{_e(session_id, locale)}<br/>"
        f"<b>{_e(_copy(locale, 'status'), locale)}</b><br/>{_e(_copy(locale, 'reviewable_status'), locale)}"
    )
    table = Table(
        [
            [
                LucernaMark(),
                [Paragraph("LUCERNA 65", styles["brand"]), Paragraph(_e(_copy(locale, "brand_subtitle"), locale), styles["subtitle"])],
                Paragraph(meta, styles["meta"]),
            ]
        ],
        colWidths=[17 * mm, width - 78 * mm, 61 * mm],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("LINEBELOW", (0, 0), (-1, -1), 0.45, BORDER),
    ]))
    return [
        table,
        Paragraph(_e(_copy(locale, "report_title"), locale), styles["title"]),
        Paragraph(_e(_copy(locale, "report_subtitle"), locale), styles["subtitle"]),
        Spacer(1, 5 * mm),
    ]


def _notice_section(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    text = _clean(report.get("mandatory_disclaimer"), locale) or _copy(locale, "notice_default")
    box = _box(
        [
            Paragraph(_e(_copy(locale, "notice_title"), locale), styles["section"]),
            Paragraph(_e(text, locale), styles["body"]),
        ],
        width,
        WARNING_BG,
    )
    return [KeepTogether(box), Spacer(1, 3 * mm)]


def _answers_section(state: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    answered = state.get("answered", [])
    story = [Paragraph(_e(_section(locale, "answers"), locale), styles["section"])]
    if not answered:
        story.append(Paragraph(_e(_copy(locale, "answers_empty"), locale), styles["body"]))
        return story

    grouped: dict[str, list[dict]] = {}
    for record in answered:
        grouped.setdefault(record.get("domain", "context"), []).append(record)

    for domain, records in grouped.items():
        first_record = True
        for record in records:
            question = _clean(record.get("question"), locale)
            answer = _answer_label(record.get("answer_id"), record.get("answer_label"), locale)
            note = _clean(record.get("note"), locale)
            rows = [
                Paragraph(_e(question, locale), styles["question"]),
                Paragraph(f"{_e(_copy(locale, 'answer_prefix'), locale)}: <b>{_e(answer, locale)}</b>", styles["answer"]),
            ]
            if note:
                rows.append(Paragraph(f"{_e(_copy(locale, 'observation_prefix'), locale)}: {_e(note, locale)}", styles["small"]))
            box = _box(rows, width, colors.white, left_line=PRIMARY_SOFT)
            if first_record:
                story.append(KeepTogether([Paragraph(_e(_domain_label(domain, locale), locale), styles["muted"]), *box]))
                first_record = False
            else:
                story.append(KeepTogether(box))
            story.append(Spacer(1, 2 * mm))
    return story


def _indicators_section(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    story = [Paragraph(_e(_section(locale, "indicators"), locale), styles["section"])]
    indicators = report.get("indicators") or []
    if not indicators:
        story.append(Paragraph(_e(_copy(locale, "indicators_empty"), locale), styles["body"]))
        return story
    for item in indicators:
        parts = [
            Paragraph(f"<b>{_e(_clean(item.get('label'), locale), locale)}</b>", styles["body"]),
            Paragraph(_e(_clean(item.get("rationale"), locale), locale), styles["muted"]),
        ]
        examples = item.get(f"examples_{locale}") or item.get("examples") or item.get("examples_ca") or []
        if examples:
            clean_examples = "; ".join(_clean(x, locale) for x in examples)
            parts.append(Paragraph(f"{_e(_copy(locale, 'examples_prefix'), locale)}: {_e(clean_examples, locale)}", styles["small"]))
        story.append(KeepTogether(_box(parts, width, colors.white, left_line=_severity_color(item.get("severity")))))
        story.append(Spacer(1, 1.7 * mm))
    return story


def _pending_section(report: dict, state: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    story = [Paragraph(_e(_section(locale, "pending"), locale), styles["section"])]
    pending = report.get("pending_questions") or []
    if pending:
        story.extend(_bullet_list(pending, styles, locale=locale))
    elif state.get("complete"):
        story.append(Paragraph(_e(_copy(locale, "pending_complete"), locale), styles["body"]))
    else:
        story.append(Paragraph(_e(_copy(locale, "pending_incomplete"), locale), styles["body"]))
    return story


def _recommendations_section(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    story = [Paragraph(_e(_section(locale, "recommendations"), locale), styles["section"])]
    recommendations = report.get("recommendations") or []
    if not recommendations:
        story.append(Paragraph(_e(_copy(locale, "recommendations_empty"), locale), styles["body"]))
        return story
    for item in recommendations:
        priority = _clean(item.get("priority"), locale)
        urgent = priority == "urgent"
        heading = _clean(item.get("text"), locale)
        prefix = _copy(locale, "urgent_action") if urgent else _human_value(priority, locale).capitalize()
        rows = [
            Paragraph(f"<b>{_e(prefix, locale)}</b>", styles["answer"]),
            Paragraph(_e(heading, locale), styles["body"]),
        ]
        rationale = _clean(item.get("rationale"), locale)
        if rationale:
            rows.append(Paragraph(_e(rationale, locale), styles["muted"]))
        story.append(KeepTogether(_box(rows, width, DANGER_SOFT if urgent else SURFACE_ALT, left_line=DANGER if urgent else PRIMARY)))
        story.append(Spacer(1, 2 * mm))
    return story


def _resources_section(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    story = [Paragraph(_e(_section(locale, "resources"), locale), styles["section"])]
    resources = report.get("resources") or []
    if not resources:
        story.append(Paragraph(_e(_copy(locale, "resources_empty"), locale), styles["body"]))
        return story
    for item in resources:
        status = _status_label(item.get("verification_status"), locale)
        lines = [
            Paragraph(f"<b>{_e(_clean(item.get('name'), locale), locale)}</b>", styles["body"]),
            Paragraph(_e(_clean(item.get("description"), locale), locale), styles["muted"]),
            Paragraph(
                f"{_e(_copy(locale, 'territory'), locale)}: {_e(_clean(item.get('territory'), locale), locale)} · "
                f"{_e(status, locale)}. {_e(_copy(locale, 'verification_note'), locale)}",
                styles["small"],
            ),
        ]
        story.append(KeepTogether(_box(lines, width, colors.white)))
        story.append(Spacer(1, 1.5 * mm))
    return story


def _sources_section(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    story = [Paragraph(_e(_section(locale, "sources"), locale), styles["section"])]
    sources = report.get("sources") or []
    if not sources:
        story.append(Paragraph(_e(_copy(locale, "sources_empty"), locale), styles["body"]))
        return story
    for item in sources:
        organism = _clean(item.get("organism"), locale) or _copy(locale, "unknown_source")
        title = _clean(item.get("title"), locale)
        version = _status_label(item.get("version"), locale)
        status = _status_label(item.get("status"), locale)
        lines = [
            Paragraph(f"<b>{_e(organism, locale)}</b>", styles["body"]),
            Paragraph(_e(title, locale), styles["muted"]),
            Paragraph(
                f"{_e(_copy(locale, 'version'), locale)}: {_e(version, locale)} · "
                f"{_e(_copy(locale, 'status_label'), locale)}: {_e(status, locale)}. "
                f"{_e(_copy(locale, 'verification_note'), locale)}",
                styles["small"],
            ),
        ]
        story.append(KeepTogether(_box(lines, width, colors.white)))
        story.append(Spacer(1, 1.5 * mm))
    return story


def _limitations_section(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    story = [Paragraph(_e(_section(locale, "limitations"), locale), styles["section"])]
    limitations = []
    base = _copy(locale, "limitations_base")
    for item in base:
        clean = _clean(item, locale)
        if clean and clean not in limitations:
            limitations.append(clean)
    box = _box(_bullet_list(limitations, styles, compact=True, locale=locale), width, GREY_BOX)
    story.append(KeepTogether(box))
    return story


def _audit_section(report: dict, styles: dict[str, ParagraphStyle], width: float, locale: str) -> list:
    audit = report.get("audit") or {}
    rows = [
        [_copy(locale, "audit_session_id"), _clean(report.get("session_id"), locale)],
        [_copy(locale, "audit_tree_version"), _clean(audit.get("tree_version"), locale)],
        [_copy(locale, "audit_data_mode"), _human_value(audit.get("data_mode"), locale)],
        [_copy(locale, "audit_human_review"), _copy(locale, "yes") if audit.get("human_review_required") else _copy(locale, "no")],
    ]
    table = Table(
        [[Paragraph(_e(label, locale), styles["small"]), Paragraph(_e(value or "-", locale), styles["small"])] for label, value in rows],
        colWidths=[42 * mm, width - 42 * mm],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.25, BORDER),
        ("BACKGROUND", (0, 0), (0, -1), SURFACE_ALT),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return [Paragraph(_e(_section(locale, "audit"), locale), styles["section"]), table]


def _box(flowables: list, width: float, background, left_line=None) -> list:
    table = Table([[flowables]], colWidths=[width])
    style = [
        ("BACKGROUND", (0, 0), (-1, -1), background),
        ("BOX", (0, 0), (-1, -1), 0.35, BORDER),
        ("LEFTPADDING", (0, 0), (-1, -1), 8),
        ("RIGHTPADDING", (0, 0), (-1, -1), 8),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if left_line:
        style.append(("LINEBEFORE", (0, 0), (-1, -1), 2.4, left_line))
    table.setStyle(TableStyle(style))
    return [table]


def _report_locale(report: dict, state: dict) -> str:
    return _normalize_locale((report or {}).get("locale") or (state or {}).get("locale"))


def _normalize_locale(locale: str | None) -> str:
    value = str(locale or "ca").strip().lower().split("-")[0]
    return value if value in SUPPORTED_LOCALES else "ca"


def _copy(locale: str, key: str):
    locale = _normalize_locale(locale)
    fallback = PDF_COPY["ca"].get(key, key)
    return PDF_COPY.get(locale, PDF_COPY["ca"]).get(key, fallback)


def _section(locale: str, key: str) -> str:
    sections = _copy(locale, "sections")
    fallback = PDF_COPY["ca"]["sections"].get(key, key)
    return sections.get(key, fallback) if isinstance(sections, dict) else fallback


def _value_labels(locale: str) -> dict[str, str]:
    return VALUE_LABELS_BY_LOCALE.get(_normalize_locale(locale), VALUE_LABELS)


def _status_labels(locale: str) -> dict[str, str]:
    return STATUS_LABELS_BY_LOCALE.get(_normalize_locale(locale), STATUS_LABELS)


def _bullet_list(items: list, styles: dict[str, ParagraphStyle], compact: bool = False, locale: str = "ca") -> list:
    out = []
    style = styles["small"] if compact else styles["body"]
    for item in items:
        out.append(Paragraph(f"- {_e(_clean(item, locale), locale)}", style))
    return out


def _format_date(value: str | None, locale: str = "ca") -> str:
    if not value:
        return datetime.now().astimezone().strftime("%d/%m/%Y %H:%M")
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        parsed = parsed.astimezone()
        return parsed.strftime("%d/%m/%Y %H:%M")
    except Exception:  # noqa: BLE001
        return _clean(value, locale)


def _severity_color(value: str | None):
    if value == "urgent":
        return DANGER
    if value == "high":
        return colors.HexColor("#b2763d")
    return PRIMARY_SOFT


def _domain_label(value: str | None, locale: str) -> str:
    labels = DOMAIN_LABELS_BY_LOCALE.get(_normalize_locale(locale), DOMAIN_LABELS)
    return labels.get(str(value or ""), _human_value(value, locale))


def _answer_label(answer_id, answer_label, locale: str) -> str:
    candidate = _clean(answer_label, locale)
    mapped = _value_labels(locale).get(str(answer_id or ""))
    if mapped and (not candidate or candidate == str(answer_id) or "?" in candidate or candidate.lower() in {"other person"}):
        return mapped
    return mapped or candidate or _human_value(answer_id, locale)


def _human_value(value, locale: str = "ca") -> str:
    if value is None:
        return ""
    raw = str(value)
    value_labels = _value_labels(locale)
    status_labels = _status_labels(locale)
    if raw in value_labels:
        return value_labels[raw]
    if raw in status_labels:
        return status_labels[raw]
    text = _clean(raw, locale)
    return value_labels.get(text, status_labels.get(text, text.replace("_", " ").strip().capitalize()))


def _status_label(value, locale: str = "ca") -> str:
    raw = "" if value is None else str(value)
    status_labels = _status_labels(locale)
    if raw in status_labels:
        return status_labels[raw]
    text = _clean(raw, locale)
    return status_labels.get(text, _human_value(text, locale))


def _clean(value, locale: str = "ca") -> str:
    text = "" if value is None else str(value)
    text = _repair_mojibake(text)
    locale = _normalize_locale(locale)
    replacements = {"S?": "Sí"}
    if locale == "ca":
        replacements.update({
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
            "Revisio": "Revisió",
        })
    elif locale == "es":
        replacements.update({
            "Des?nimo o presi?n": "Desánimo o presión",
            "Medicacion": "Medicación",
            "Telefono": "Teléfono",
            "Alimentacion": "Alimentación",
            "verificacion": "verificación",
            "diagnostico": "diagnóstico",
            "resolucion": "resolución",
            "Sesion": "Sesión",
            "Revision": "Revisión",
        })
    for old, new in replacements.items():
        text = text.replace(old, new)
    return " ".join(text.split())


def _repair_mojibake(text: str) -> str:
    if "Ã" in text or "Â" in text:
        try:
            return text.encode("latin1").decode("utf-8")
        except UnicodeError:
            pass
    return text.replace("Â«", "«").replace("Â»", "»").replace("Â·", "·")


def _e(value, locale: str = "ca") -> str:
    return escape(_clean(value, locale), {"'": "&apos;", '"': "&quot;"})
