from __future__ import annotations

import argparse
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Flowable,
    Frame,
    HRFlowable,
    ListFlowable,
    ListItem,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
FONT_REGULAR = Path(r"C:\Windows\Fonts\msjh.ttc")
FONT_BOLD = Path(r"C:\Windows\Fonts\msjhbd.ttc")

INK = colors.HexColor("#111214")
MUTED = colors.HexColor("#5F646B")
ACCENT = colors.HexColor("#087F73")
ACCENT_SOFT = colors.HexColor("#E8F5F2")
LINE = colors.HexColor("#D9DDDC")
PAPER = colors.white


class LinkChip(Flowable):
    """Compact, clickable contact link with a small vector icon."""

    def __init__(self, label: str, url: str, icon: str, width: float) -> None:
        super().__init__()
        self.label = label
        self.url = url
        self.icon = icon
        self.width = width
        self.height = 8 * mm

    def draw(self) -> None:
        canvas = self.canv
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#C8D5D2"))
        canvas.setFillColor(colors.HexColor("#F7FAF9"))
        canvas.roundRect(0, 0, self.width, self.height, 3 * mm, stroke=1, fill=1)
        icon_x = 4.6 * mm
        icon_y = self.height / 2
        canvas.setStrokeColor(ACCENT)
        canvas.setFillColor(ACCENT)
        canvas.setLineWidth(0.75)

        if self.icon == "mail":
            canvas.roundRect(icon_x - 2.2 * mm, icon_y - 1.55 * mm, 4.4 * mm, 3.1 * mm, 0.5 * mm, stroke=1, fill=0)
            canvas.line(icon_x - 2 * mm, icon_y + 1.1 * mm, icon_x, icon_y - 0.3 * mm)
            canvas.line(icon_x + 2 * mm, icon_y + 1.1 * mm, icon_x, icon_y - 0.3 * mm)
        elif self.icon == "web":
            canvas.circle(icon_x, icon_y, 2.1 * mm, stroke=1, fill=0)
            canvas.ellipse(icon_x - 1.05 * mm, icon_y - 2.1 * mm, icon_x + 1.05 * mm, icon_y + 2.1 * mm, stroke=1, fill=0)
            canvas.line(icon_x - 2 * mm, icon_y, icon_x + 2 * mm, icon_y)
        elif self.icon == "linkedin":
            canvas.roundRect(icon_x - 2.2 * mm, icon_y - 2.2 * mm, 4.4 * mm, 4.4 * mm, 0.6 * mm, stroke=0, fill=1)
            canvas.setFillColor(PAPER)
            canvas.setFont("Helvetica-Bold", 6.8)
            canvas.drawCentredString(icon_x, icon_y - 2.1, "in")
        elif self.icon == "threads":
            canvas.circle(icon_x, icon_y, 2.2 * mm, stroke=1, fill=0)
            canvas.setFont("Helvetica-Bold", 6.6)
            canvas.drawCentredString(icon_x, icon_y - 2.2, "@")
        else:
            canvas.circle(icon_x, icon_y, 2.2 * mm, stroke=0, fill=1)
            canvas.setFillColor(PAPER)
            canvas.setFont("Helvetica-Bold", 5.6)
            canvas.drawCentredString(icon_x, icon_y - 1.9, "GH")

        canvas.setFillColor(INK)
        canvas.setFont("ResumeSans", 7.7)
        canvas.drawString(9 * mm, icon_y - 2.5, self.label)
        canvas.linkURL(self.url, (0, 0, self.width, self.height), relative=1)
        canvas.restoreState()


def register_fonts() -> None:
    pdfmetrics.registerFont(TTFont("ResumeSans", str(FONT_REGULAR)))
    pdfmetrics.registerFont(TTFont("ResumeSansBold", str(FONT_BOLD)))


def styles() -> dict[str, ParagraphStyle]:
    sample = getSampleStyleSheet()
    base = ParagraphStyle(
        "Base",
        parent=sample["BodyText"],
        fontName="ResumeSans",
        fontSize=9.4,
        leading=15.2,
        textColor=INK,
        wordWrap="CJK",
        spaceAfter=2.5 * mm,
    )
    return {
        "base": base,
        "name": ParagraphStyle(
            "Name",
            parent=base,
            fontName="ResumeSansBold",
            fontSize=25,
            leading=30,
            spaceAfter=1.5 * mm,
        ),
        "role": ParagraphStyle(
            "Role",
            parent=base,
            fontName="ResumeSansBold",
            fontSize=11.5,
            leading=16,
            textColor=ACCENT,
            spaceAfter=0,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=base,
            fontSize=8.5,
            leading=13.5,
            textColor=MUTED,
            alignment=TA_RIGHT,
            spaceAfter=0,
        ),
        "intro": ParagraphStyle(
            "Intro",
            parent=base,
            fontSize=10.2,
            leading=17,
            textColor=colors.HexColor("#30343A"),
            spaceAfter=2.5 * mm,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base,
            fontName="ResumeSansBold",
            fontSize=14,
            leading=19,
            textColor=INK,
            spaceBefore=3 * mm,
            spaceAfter=1.5 * mm,
        ),
        "role_title": ParagraphStyle(
            "RoleTitle",
            parent=base,
            fontName="ResumeSansBold",
            fontSize=11.5,
            leading=16,
            spaceAfter=0,
        ),
        "role_meta": ParagraphStyle(
            "RoleMeta",
            parent=base,
            fontSize=8.5,
            leading=13,
            textColor=MUTED,
            spaceAfter=0,
        ),
        "date": ParagraphStyle(
            "Date",
            parent=base,
            fontSize=8.8,
            leading=14,
            textColor=ACCENT,
            alignment=TA_RIGHT,
            spaceAfter=0,
        ),
        "project": ParagraphStyle(
            "Project",
            parent=base,
            fontName="ResumeSansBold",
            fontSize=10.2,
            leading=15,
            textColor=ACCENT,
            spaceBefore=2.2 * mm,
            spaceAfter=0.8 * mm,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base,
            fontSize=8.5,
            leading=13.5,
            textColor=MUTED,
        ),
        "skill": ParagraphStyle(
            "Skill",
            parent=base,
            fontName="ResumeSansBold",
            fontSize=10.2,
            leading=15,
            textColor=ACCENT,
            spaceAfter=0.8 * mm,
        ),
        "footer": ParagraphStyle(
            "Footer",
            parent=base,
            fontSize=7.8,
            leading=10,
            textColor=MUTED,
        ),
    }


def bullet_list(items: list[str], style: ParagraphStyle, *, compact: bool = False) -> ListFlowable:
    list_items = []
    for item in items:
        item_style = ParagraphStyle(
            f"{style.name}-bullet",
            parent=style,
            spaceAfter=(0.7 if compact else 1.2) * mm,
        )
        list_items.append(ListItem(Paragraph(item, item_style), leftIndent=0))
    return ListFlowable(
        list_items,
        bulletType="bullet",
        start="circle",
        bulletFontName="ResumeSans",
        bulletFontSize=5,
        bulletColor=ACCENT,
        leftIndent=4.8 * mm,
        bulletIndent=0.8 * mm,
        spaceBefore=0,
        spaceAfter=1.2 * mm,
    )


def section(title: str, s: dict[str, ParagraphStyle]) -> list:
    return [
        Spacer(1, 1.5 * mm),
        Paragraph(title, s["section"]),
        HRFlowable(width="100%", thickness=0.8, color=INK, spaceAfter=3 * mm),
    ]


def role_header(
    title: str,
    company: str,
    date: str,
    s: dict[str, ParagraphStyle],
    meta: str = "",
) -> Table:
    left = [Paragraph(title, s["role_title"]), Paragraph(company, s["role_meta"])]
    if meta:
        left.append(Paragraph(meta, s["role_meta"]))
    table = Table([[left, Paragraph(date, s["date"]) ]], colWidths=[128 * mm, 42 * mm])
    table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    return table


def link(label: str, url: str) -> str:
    return f'<link href="{url}" color="#087F73"><u>{label}</u> <font size="7.5">&#8599;</font></link>'


def draw_page(canvas, doc) -> None:
    canvas.saveState()
    width, height = A4
    if doc.page > 1:
        canvas.setStrokeColor(LINE)
        canvas.setLineWidth(0.5)
        canvas.line(20 * mm, height - 13 * mm, width - 20 * mm, height - 13 * mm)
        canvas.setFont("ResumeSans", 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawString(20 * mm, height - 10 * mm, "林芷筠 Olivia Lin · 產品／專案經理 · Product Builder")
    canvas.setStrokeColor(LINE)
    canvas.line(20 * mm, 13 * mm, width - 20 * mm, 13 * mm)
    canvas.setFont("ResumeSans", 7.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 8.5 * mm, "oliviaiii.github.io")
    canvas.drawRightString(width - 20 * mm, 8.5 * mm, f"{doc.page}")
    canvas.restoreState()


def build_story(s: dict[str, ParagraphStyle]) -> list:
    story: list = []

    def chip_pair(left: LinkChip, right: LinkChip) -> Table:
        pair = Table([[left, right]], colWidths=[35 * mm, 35 * mm])
        pair.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 1 * mm),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ]))
        return pair

    header_left = [
        Paragraph("林芷筠 <font size=12 color='#5F646B'>Olivia Lin</font>", s["name"]),
        Paragraph("產品／專案經理 · PRODUCT BUILDER", s["role"]),
        Spacer(1, 2 * mm),
        Paragraph("新北市 · 0988-796-571", s["small"]),
    ]
    header_right = Table(
        [
            [LinkChip("rainy57091224@gmail.com", "mailto:rainy57091224@gmail.com", "mail", 70 * mm)],
            [chip_pair(LinkChip("個人網站", "https://oliviaiii.github.io/", "web", 34 * mm), LinkChip("GitHub", "https://github.com/Oliviaiii", "github", 34 * mm))],
            [chip_pair(LinkChip("LinkedIn", "https://www.linkedin.com/in/oliviaiii1224chihyun/", "linkedin", 34 * mm), LinkChip("Threads", "https://www.threads.com/@pmenance.manager", "threads", 34 * mm))],
        ],
        colWidths=[70 * mm],
    )
    header_right.setStyle(TableStyle([
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 1.2 * mm),
    ]))
    header = Table([[header_left, header_right]], colWidths=[100 * mm, 70 * mm])
    header.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.extend([header, Spacer(1, 4 * mm), HRFlowable(width="100%", thickness=1, color=INK), Spacer(1, 4 * mm)])

    story.append(
        Paragraph(
            "我是 Olivia，同事都叫我 Oli。從餐飲現場、藥局系統支援一路走進產品管理，現在持續往 Product Builder 發展。我擅長理解使用者與商業流程，把模糊需求整理成團隊能執行、能驗收的產品方案，也能搭配 AI 閱讀 Codebase、製作原型並參與實作，讓產品真正落地。",
            s["intro"],
        )
    )
    tag_data = [[
        Paragraph("使用者與現場理解", s["small"]),
        Paragraph("產品規格與系統分析", s["small"]),
        Paragraph("AI-Augmented Workflow", s["small"]),
        Paragraph("合規與交付治理", s["small"]),
    ]]
    tags = Table(tag_data, colWidths=[42.5 * mm] * 4)
    tags.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), ACCENT_SOFT),
                ("TEXTCOLOR", (0, 0), (-1, -1), ACCENT),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6E1")),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C8E6E1")),
                ("TOPPADDING", (0, 0), (-1, -1), 2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2 * mm),
            ]
        )
    )
    story.extend([tags, Spacer(1, 1 * mm)])

    story.extend(section("目前角色", s))
    story.append(role_header("產品／專案經理｜Product Builder", "數位因子網路科技有限公司", "2025.06 至今", s, "跨前端、後端與 UI/UX 團隊 · ISO 27001 管理框架"))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("在同一個角色中負責多條產品線。我的工作不只停在 PRD 與排程，也包含系統流程、介面原型、部分程式實作、Code Review、驗收與發版協調；需要時會先親手做出可操作版本，再和工程團隊一起收斂成正式產品。", s["base"]))

    product_cards = [
        (
            "shinvo-shop｜多租戶電商平台",
            "主導從「一案一站」走向共用平台。負責判斷共用能力與客製邊界，規劃訂單、付款、物流、庫存、優惠、會員、通知與後台編輯體驗，並參與部分前後台功能落地。",
        ),
        (
            "LINERP｜徠能 B2B 供貨 SaaS",
            "重新梳理供應商與商家的合作、商品、訂貨、配送、簽收與對帳流程。結合過去餐飲叫貨經驗，透過自然語言與 AI 協作重構系統，正式部署由工程師接手。",
        ),
        (
            "LINE OA AI 客服｜獨立 RAG 產品",
            "以 LINERP 官方帳號作為實際案例，直接同步 Repository 文件，避免重複維護知識。規劃地端 DGX 模型、檢索與回答邊界，以及多 Bot 隔離、回饋與稽核機制。",
        ),
        (
            "政府 OTT｜影音平台維運與交付",
            "接手網站、App、CMS、影音播放與資料介接需求，負責釐清、規格、排程、驗收及上線；同時協調機關、內部團隊與供應商，整理資安檢測及稽核交付。",
        ),
    ]
    card_rows = []
    for row_start in range(0, len(product_cards), 2):
        row = []
        for title, description in product_cards[row_start:row_start + 2]:
            row.append([Paragraph(title, s["project"]), Paragraph(description, s["base"])])
        card_rows.append(row)
    cards = Table(card_rows, colWidths=[83.5 * mm, 83.5 * mm], hAlign="LEFT")
    cards.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F6F8F7")),
        ("BOX", (0, 0), (-1, -1), 0.5, LINE),
        ("INNERGRID", (0, 0), (-1, -1), 0.5, LINE),
        ("LEFTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("RIGHTPADDING", (0, 0), (-1, -1), 4 * mm),
        ("TOPPADDING", (0, 0), (-1, -1), 3 * mm),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 3 * mm),
    ]))
    story.extend([Spacer(1, 1 * mm), cards])

    story.append(Paragraph("我的工作方式", s["project"]))
    story.append(
        bullet_list(
            [
                "把現場語言翻成清楚的流程、規格與 Issue，也把技術限制翻回利害關係人能做決策的資訊。",
                "建立 GitHub Projects、Issue、PR、PRD、SOP 與版本紀錄，讓需求到上線可以追溯。",
                "讓 AI 協助探索、原型、實作與審查；產品方向、風險判斷與最終驗收仍由我負責。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.append(PageBreak())

    story.extend(section("經歷與領域背景", s))
    story.append(role_header("產品／專案顧問（外部合作）", "藥局系統軟體公司 · 每週 20 小時 · 全遠端", "2025.10 至 2026.01", s))
    story.append(Spacer(1, 2 * mm))
    story.append(
        bullet_list(
            [
                "運用調劑、健保申報、進銷存與現場設備經驗，協助全新雲端藥局系統釐清流程、敏感資料、法規及資安邊界。",
                "把現場需求轉成工程團隊可執行、可驗收的規格，並檢視既有工單與調劑作業的流程斷點。",
                "重整 Repository 權責、Gitflow、需求審查與版本管理，搭配 ISO 27001 要求建立可追溯的協作制度。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.extend([Spacer(1, 2 * mm), HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=3 * mm)])
    story.append(role_header("業務工程師（FAE）｜系統導入與技術顧問", "樺穎資訊科技顧問有限公司", "2023.11 至 2024.12", s, "藥局資訊系統 · ERP · 健保申報 · 現場設備"))
    story.append(Spacer(1, 2 * mm))
    story.append(
        bullet_list(
            [
                "擔任藥局第一線技術窗口，從新店建置、系統導入、操作教學，到 ERP 升級、健保申報與現場異常排除皆直接參與。",
                "處理主機、網路、周邊設備與系統串接，並透過資料庫、Log、庫存及交易資料定位操作、設定、資料或程式問題。",
                "將客戶痛點整理成重現步驟與工程需求，再把技術方案轉成使用者能理解的操作方式；同時協調資料轉換、跨系統介接與上線條件。",
            ],
            s["base"],
            compact=True,
        )
    )
    story.extend([Spacer(1, 2 * mm), HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=3 * mm)])
    story.append(role_header("餐飲營運｜第一線服務與管理", "居酒屋、餐酒館、熱炒店、酒吧與早餐店", "2018 至 2023", s))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("從第一線接待、內場備料與出餐，到成本控管、供應商叫貨、人員管理及現場調度皆有實務經驗。這段經歷讓我熟悉真實營運限制，也建立在高壓環境中判斷優先順序、處理突發狀況與理解使用者感受的能力。", s["base"]))

    story.extend(section("核心能力", s))
    skill_groups = [
        (
            "產品與需求",
            "使用者訪談、需求釐清、流程盤點、PRD／SRS、Roadmap、SOP 與驗收規格；將複雜問題拆成可執行、可測試、可追蹤的 Issue。",
        ),
        (
            "系統與商業流程",
            "電商訂單、付款、物流、庫存、優惠與會員；多租戶、狀態機、Webhook、冪等與例外流程；LINE、金流、物流及第三方 API 串接。",
        ),
        (
            "AI 協作與建置",
            "Claude Code、Codex CLI、Gemini CLI；閱讀 Codebase、前端原型、POC、實作、Code Review 與驗收；Repository 文件同步、RAG、地端 DGX 模型與多 Bot 隔離。",
        ),
        (
            "治理與合規",
            "GitHub Projects、Issue Forms、PR 模板、Gitflow 與版本管理；ISO 27001、政府標案、弱點掃描、App 檢測、風險盤點與稽核證據。",
        ),
    ]
    skill_rows = []
    for title, description in skill_groups:
        skill_rows.append([Paragraph(title, s["skill"]), Paragraph(description, s["base"])])
    skill_table = Table(skill_rows, colWidths=[48 * mm, 122 * mm], repeatRows=0)
    skill_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.3 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.3 * mm),
                ("LINEBELOW", (0, 0), (-1, -2), 0.45, LINE),
            ]
        )
    )
    story.append(skill_table)

    story.extend([Spacer(1, 2 * mm), HRFlowable(width="100%", thickness=0.8, color=INK, spaceAfter=2 * mm)])
    story.append(Paragraph("<b>工具</b>　GitHub／GitHub Actions／Git Worktree／Figma／Mermaid／Jira／Notion／MySQL／PostgreSQL／Docker／AWS S3／Google Cloud Storage", s["small"]))
    story.append(Paragraph("<b>語言與學歷</b>　中文（母語）／台語（精通）／英文（中等）　·　國立臺北大學 公共行政與政策學系", s["small"]))
    return story


def build_pdf(output: Path) -> None:
    register_fonts()
    s = styles()
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = BaseDocTemplate(
        str(output),
        pagesize=A4,
        leftMargin=20 * mm,
        rightMargin=20 * mm,
        topMargin=18 * mm,
        bottomMargin=18 * mm,
        title="林芷筠 Olivia Lin｜產品／專案經理",
        author="林芷筠 Olivia Lin",
        subject="產品／專案經理 · Product Builder 履歷",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="resume")
    doc.addPageTemplates([PageTemplate(id="resume", frames=[frame], onPage=draw_page)])
    doc.build(build_story(s))


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Olivia Lin's Chinese resume PDF")
    parser.add_argument(
        "--output",
        type=Path,
        default=ROOT / "output" / "pdf" / "林芷筠中文履歷.pdf",
    )
    args = parser.parse_args()
    build_pdf(args.output.resolve())
    print(args.output.resolve())


if __name__ == "__main__":
    main()
