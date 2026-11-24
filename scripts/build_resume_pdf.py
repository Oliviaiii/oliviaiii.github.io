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
    return f'<link href="{url}" color="#087F73"><u>{label}</u></link>'


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

    header_left = [
        Paragraph("林芷筠 <font size=12 color='#5F646B'>Olivia Lin</font>", s["name"]),
        Paragraph("產品／專案經理 · PRODUCT BUILDER", s["role"]),
    ]
    header_right = Paragraph(
        "<br/>".join(
            [
                link("rainy57091224@gmail.com", "mailto:rainy57091224@gmail.com"),
                "0988-796-571 · 新北市板橋區",
                link("個人網站", "https://oliviaiii.github.io/"),
                link("GitHub", "https://github.com/Oliviaiii") + " · " + link("LinkedIn", "https://www.linkedin.com/in/oliviaiii1224chihyun/"),
                link("Threads @pmenance.manager", "https://www.threads.com/@pmenance.manager"),
            ]
        ),
        s["contact"],
    )
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
            "我是 Olivia，同事都叫我 Oli。從第一線系統支援走進產品管理，目前持續朝 Product Builder 發展。擅長理解使用者、釐清需求，並將混亂的問題整理成可執行、可驗收的成果；也善用 AI 協作，推進產品從規劃到落地。",
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

    story.extend(section("工作經驗", s))
    story.append(role_header("產品／專案經理｜Product Builder", "數位因子網路科技有限公司", "2025.06 至今", s, "跨前端、後端與 UI/UX 團隊 · ISO 27001 管理框架"))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("除了需求與排程管理，也直接參與規格設計、程式實作、Code Review、驗收與發版，持續從 PM 往能親手完成產品的 Product Builder 發展。", s["base"]))

    story.append(Paragraph("shinvo-shop 多租戶電商建站平台", s["project"]))
    story.append(
        bullet_list(
            [
                "主導公司從「一案一站、各自維護」轉型為共用後台、前台可依品牌切換主題與 CSS 的多租戶平台。",
                "判斷共用能力與品牌客製需求，設計可設定、可重複使用的產品流程。",
                "規劃並參與訂單、付款、物流、庫存、優惠、會員與通知等電商核心功能。",
                "實作 Preview-first 三欄式 Widget 編輯器、主題 CSS 架構與多語系素材管理。",
                "建立需求、驗收、發版與正式環境追蹤流程，讓產品變更可回溯、可稽核。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.append(Paragraph("LINERP（徠能 B2B 供貨 SaaS）", s["project"]))
    story.append(
        bullet_list(
            [
                "重新設計並重構既有供貨系統，整合供應商與商家的商品、合作、訂單、配送、簽收與對帳流程。",
                "結合餐飲營運與供應商叫貨經驗，重新定義商業流程、資料關係與操作介面。",
                "透過自然語言與 AI 協作完成系統重構，工程師負責正式環境部署。",
                "將訂單、付款與配送狀態分開管理，補強金流驗簽、冪等處理及租戶資料隔離。",
                "優化 LIFF 登入、手機操作、LINE 通知與新舊系統切換流程。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.append(PageBreak())

    story.append(Paragraph("LINE OA AI 客服平台（RAG）", s["project"]))
    story.append(
        bullet_list(
            [
                "規劃並落地獨立的 LINE 官方帳號 AI 客服產品，LINERP 官方 LINE OA 為目前實際接入案例。",
                "直接同步產品 Repository 內的操作文件，避免額外維護另一份客服知識庫。",
                "使用地端 DGX 模型完成問句改寫、Embedding、Rerank 與回答生成。",
                "設計低信心不臆測、模糊問題先釐清、系統異常與知識未命中分流等回答邊界。",
                "建立多 Bot 隔離、後台設定、知識同步、問題回收、錯誤診斷與稽核紀錄。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.append(Paragraph("政府 OTT 影音平台", s["project"]))
    story.append(
        bullet_list(
            [
                "接手政府影音串流平台的長期維運與產品需求，協調機關、內部團隊及外部供應商完成開發與交付。",
                "負責需求釐清、規格與報價、排程協調、驗收、上線及後續追蹤。",
                "同時處理網站、App、CMS、影音播放、資料介接與內容營運需求。",
                "整理弱點掃描、App 檢測、修正證據、營運報告與稽核文件。",
                "將正式環境異常、資安風險與相容性問題轉成可重現、可追蹤、可驗收的工作項目。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.append(Paragraph("工作方式", s["project"]))
    story.append(
        bullet_list(
            [
                "建立 GitHub Projects、Issue 表單、PR 模板、PRD、SOP 與 ChangeLog 規範，讓需求、開發、驗收與發版都有完整紀錄。",
                "使用 Claude Code、Codex 等 AI 工具並行推進產品工作，由 AI 協助實作、測試與審查，我負責產品判斷、責任邊界與最終驗收。",
                "自行開發 agent-ledger 管理 AI coding agent 的執行狀態、任務紀錄與工作報告，讓 AI 協作成果可以被追蹤與交接。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.extend([Spacer(1, 2 * mm), HRFlowable(width="100%", thickness=0.5, color=LINE, spaceAfter=3 * mm)])
    story.append(role_header("產品／專案顧問（外部合作）", "藥局系統軟體公司 · 每週 20 小時 · 全遠端", "2025.10 至 2026.01", s))
    story.append(Spacer(1, 2 * mm))
    story.append(
        bullet_list(
            [
                "將過去服務藥局累積的調劑、健保申報、進銷存及現場設備經驗，轉化為工程團隊可執行、可驗收的需求。",
                "協助釐清全新雲端系統的敏感資料、法規與資安邊界，以及設備串接、斷線備援和現場流程。",
                "重整 Repository 權責、Gitflow、需求審查與版本管理，建立從需求到發布皆可追蹤的協作流程。",
                "結合 ISO 27001 導入經驗，整理權限、變更、審查與紀錄規範，讓開發流程保留可追溯的稽核證據。",
                "檢視既有工單與調劑作業流程，找出需求、開發及現場操作之間的斷點並提出改善方案。",
            ],
            s["base"],
            compact=True,
        )
    )

    story.append(PageBreak())

    story.extend(section("第一線系統導入與技術顧問經驗", s))
    story.append(role_header("業務工程師（FAE）｜系統導入與技術顧問", "樺穎資訊科技顧問有限公司", "2023.11 至 2024.12", s, "藥局資訊系統 · ERP · 健保申報 · 現場設備"))
    story.append(Spacer(1, 2 * mm))
    story.append(Paragraph("擔任藥局客戶的第一線技術窗口，工作涵蓋需求訪談、售前支援、系統導入、操作教學、問題排除與跨部門協調，同時累積完整的藥局營運與調劑系統 Domain Knowledge。", s["base"]))

    fae_groups = [
        (
            "客戶現場與需求釐清",
            [
                "深入藥局現場了解調劑、進銷存、銷售、庫存與健保申報流程，協助使用者排除操作問題並改善工作方式。",
                "將客戶描述的現場狀況整理成重現步驟與工程需求，再把技術方案轉譯成客戶能理解的操作說明。",
                "區分問題來自操作、設定、資料、設備、網路或程式缺陷，協助團隊找到真正原因。",
            ],
        ),
        (
            "系統導入與教育訓練",
            [
                "從新藥局建置開始，負責系統安裝、資料準備、權限與環境設定、設備串接及操作教學。",
                "協助 ERP 升級、健保藥價調整、健保申報與系統介接，確保調劑、處方箋及銷售流程正常運作。",
                "依不同使用者的工作內容安排教育訓練，協助藥師與門市人員熟悉系統。",
            ],
        ),
        (
            "系統、資料與設備問題排除",
            [
                "處理主機、網路、印表機、掃描設備及周邊硬體的安裝、串接、故障判斷與備品更換。",
                "透過資料庫、系統 Log、庫存與交易資料定位問題，處理資料修正、備份、轉移及環境更換。",
                "排查健保連線、申報資料、雲端控制軟體驗證及診所與藥局間的資料整合問題。",
                "建立可追蹤的問題紀錄與排錯方式，讓現場、客服與工程團隊能接續處理。",
            ],
        ),
        (
            "跨部門專案執行",
            [
                "參與系統轉換與資料移轉專案，協調客戶、工程團隊及內部業務，確認資料格式、轉換結果與上線條件。",
                "協助物流與網路商城訂單串接，將人工轉單流程改為系統自動處理。",
                "整理客戶共通需求與高頻問題，作為後續產品調整、功能規劃與教育文件的依據。",
            ],
        ),
    ]
    for title, items in fae_groups:
        story.append(Paragraph(title, s["project"]))
        story.append(bullet_list(items, s["base"], compact=True))

    story.extend(section("專長", s))
    skill_groups = [
        (
            "產品規劃與需求落地",
            "使用者訪談、需求釐清、流程盤點與問題定義；PRD／SRS／SAD／SDD、Roadmap、SOP 與驗收規格；將複雜需求拆分成可執行、可測試、可追蹤的 Issue；規劃狀態、例外、權限、通知與回退流程；區分平台共用能力與客戶客製需求。",
        ),
        (
            "AI 協作與 Product Building",
            "使用 Claude Code、Codex CLI、Gemini CLI 閱讀 Codebase、實作功能、Code Review 與驗收；以自然語言建立前端原型、POC 與可操作 Demo；使用多 Agent 與 Git Worktree 平行開發及交叉審查；設計 AI 開發規則、Skills、驗收 Agent 與自動檢查流程。",
        ),
        (
            "系統分析與技術協作",
            "電商訂單、付款、物流、庫存、優惠、會員與通知流程；多租戶資料隔離、自訂網域、權限與品牌客製架構；Webhook 驗簽、冪等處理、競態條件、失敗重試與狀態機；LINE Login、LIFF、Messaging API、LINE Pay、綠界與第三方 API 串接。",
        ),
        (
            "RAG 與 AI 客服產品",
            "Repository 文件同步、知識切片、Embedding、向量檢索與 Rerank；低信心 Fallback、模糊問題釐清、未命中回收及題外問題分流；地端 DGX 模型服務；多 Bot 資料隔離、知識同步、錯誤診斷、稽核紀錄與用量管理。",
        ),
        (
            "專案治理、資安與合規",
            "GitHub Projects、Issue Forms、PR 模板、分支策略與版本管理；需求、開發、驗收、發版及正式環境可追溯流程；Root Cause Analysis、技術 Spike、風險盤點與回退計畫；ISO 27001、政府標案、弱點掃描、App 檢測與稽核證據。",
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

    story.extend(section("工具、領域與學歷", s))
    details = [
        [Paragraph("產品與協作", s["skill"]), Paragraph("GitHub、GitHub Actions、Git Worktree、Figma、Mermaid、Jira、Notion", s["base"])],
        [Paragraph("資料與環境", s["skill"]), Paragraph("MySQL、PostgreSQL／pgvector、AWS S3、Google Cloud Storage、Google Analytics、Search Console", s["base"])],
        [Paragraph("領域知識", s["skill"]), Paragraph("電商平台、B2B 供貨 SaaS、LINE 生態、RAG 客服、政府 OTT、藥局 ERP、健保申報與餐飲營運", s["base"])],
        [Paragraph("語言", s["skill"]), Paragraph("中文（母語）、台語（精通）、英文（中等）", s["base"])],
        [Paragraph("學歷", s["skill"]), Paragraph("國立臺北大學｜公共行政與政策學系｜2019.09 至 2021.11", s["base"])],
    ]
    details_table = Table(details, colWidths=[42 * mm, 128 * mm])
    details_table.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3 * mm),
                ("TOPPADDING", (0, 0), (-1, -1), 2.2 * mm),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
                ("LINEBELOW", (0, 0), (-1, -2), 0.45, LINE),
            ]
        )
    )
    story.append(details_table)
    story.append(Spacer(1, 6 * mm))
    story.append(
        Paragraph(
            "完整案例、AI 工作方式與可操作作品：" + link("https://oliviaiii.github.io/", "https://oliviaiii.github.io/"),
            s["base"],
        )
    )
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
