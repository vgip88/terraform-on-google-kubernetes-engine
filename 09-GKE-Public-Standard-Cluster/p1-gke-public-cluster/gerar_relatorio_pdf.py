#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#1A73E8"))
        self.drawString(54, letter[1] - 32, "GOOGLE CLOUD PLATFORM  |  TERRAFORM & GKE")

        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5F6368"))
        self.drawRightString(letter[0] - 54, letter[1] - 32, "Relatório Técnico de Configuração")

        # Header line
        self.setStrokeColor(colors.HexColor("#E0E0E0"))
        self.setLineWidth(0.6)
        self.line(54, letter[1] - 38, letter[0] - 54, letter[1] - 38)

        # Footer line & text
        self.line(54, 42, letter[0] - 54, 42)
        page_str = f"Página {self._pageNumber} de {page_count}"
        self.drawRightString(letter[0] - 54, 30, page_str)
        self.drawString(54, 30, "Documento gerado automaticamente no ambiente Vagrant (servergcp)")
        self.restoreState()

def build_pdf(filename):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=48,
        bottomMargin=48
    )

    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#1A73E8")    # Google Blue
    dark_color = colors.HexColor("#202124")       # Dark Charcoal
    sub_color = colors.HexColor("#5F6368")        # Slate Grey
    bg_light = colors.HexColor("#F8F9FA")         # Light Card Background
    code_bg = colors.HexColor("#1E293B")          # Deep Slate Code Background
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=4
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=sub_color,
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16.5,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13.5,
        textColor=dark_color,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=dark_color,
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#F1F5F9")
    )
    
    alert_style = ParagraphStyle(
        'Alert_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#B3261E")
    )

    story = []

    # Title & Subtitle
    story.append(Paragraph("Relatório de Modificações e Solução de Credenciais", title_style))
    story.append(Paragraph("Resolução de autenticação GCP e inicialização do Terraform no projeto GKE", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=primary_color, spaceAfter=10))

    # Meta Info Table
    meta_data = [
        [Paragraph("<b>Projeto GCP Ativo:</b>", body_style), Paragraph("home-slabs (ID: 671387394008)", body_style),
         Paragraph("<b>Ambiente Host:</b>", body_style), Paragraph("Vagrant Linux (servergcp)", body_style)],
        [Paragraph("<b>Conta do Usuário:</b>", body_style), Paragraph("vgip88@gmail.com", body_style),
         Paragraph("<b>Diretório:</b>", body_style), Paragraph("09-GKE-Public-Standard-Cluster/p1-gke-public-cluster", body_style)],
        [Paragraph("<b>Backend de Estado:</b>", body_style), Paragraph("GCS: terraform-on-gcp-gke-129test", body_style),
         Paragraph("<b>Data da Execução:</b>", body_style), Paragraph("26/10/2026", body_style)],
    ]
    meta_table = Table(meta_data, colWidths=[105, 155, 95, 149])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), bg_light),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#E2E8F0")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#EDF2F7")),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # Section 1: Diagnóstico
    story.append(Paragraph("1. Diagnóstico do Problema", h1_style))
    story.append(Paragraph(
        "Ao executar o comando <code>terraform init</code> no diretório do cluster GKE público, a inicialização falhou imediatamente com o seguinte erro retornado pelo cliente do Cloud Storage:",
        body_style
    ))

    error_box_data = [[
        Paragraph(
            "<b>Error: storage.NewClient() failed: dialing: credentials: could not find default credentials.</b><br/>"
            "See https://cloud.google.com/docs/authentication/external/set-up-adc for more information",
            alert_style
        )
    ]]
    error_table = Table(error_box_data, colWidths=[504])
    error_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#FEF2F2")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#FCA5A5")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(error_table)
    story.append(Spacer(1, 6))

    story.append(Paragraph("<b>Causas Raízes Identificadas na Análise:</b>", h2_style))
    story.append(Paragraph(
        "• <b>gcloud CLI vs. Application Default Credentials (ADC):</b> O comando interativo <code>gcloud auth login</code> autentica apenas as chamadas do utilitário de linha de comando. Ferramentas como o Terraform e os SDKs do Google Cloud utilizam a especificação ADC (armazenada em caminho específico de sistema).",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Ambiente Headless / SSH:</b> Como a máquina virtual opera sem servidor gráfico (DISPLAY ausente e sem navegadores web), o comando <code>gcloud auth application-default login</code> convencional não pôde abrir a tela de autorização.",
        bullet_style
    ))
    story.append(Paragraph(
        "• <b>Inconsistência de Projeto no Código:</b> O arquivo <code>terraform.tfvars</code> estava referenciando o ID de projeto padrão de exemplo (<code>gcplearn9</code>), divergindo do projeto real onde o bucket GCS foi criado (<code>home-slabs</code>).",
        bullet_style
    ))
    story.append(Spacer(1, 8))

    # Section 2: Modificações e Soluções
    story.append(Paragraph("2. Modificações e Soluções Implementadas", h1_style))

    # Sub item A
    story.append(KeepTogether([
        Paragraph("A. Criação da Conta de Serviço (Service Account) dedicada no GCP", h2_style),
        Paragraph("Criamos uma conta de serviço no projeto <code>home-slabs</code> para gerenciar as operações do Terraform:", body_style),
        Table([[
            Paragraph(
                "gcloud iam service-accounts create terraform-sa \\<br/>"
                "&nbsp;&nbsp;--display-name=\"Terraform Admin Service Account\" \\<br/>"
                "&nbsp;&nbsp;--project=home-slabs",
                code_style
            )
        ]], colWidths=[504], style=[('BACKGROUND', (0,0), (-1,-1), code_bg), ('PADDING', (0,0), (-1,-1), 6)]),
        Spacer(1, 6)
    ]))

    # Sub item B
    story.append(KeepTogether([
        Paragraph("B. Atribuição do Papel IAM de Proprietário (Owner)", h2_style),
        Paragraph("Concedemos o papel <code>roles/owner</code> à conta de serviço no projeto ativo, garantindo permissão para criar instâncias GKE, redes VPC, sub-redes, regras de firewall e gravar o estado no bucket GCS:", body_style),
        Table([[
            Paragraph(
                "gcloud projects add-iam-policy-binding home-slabs \\<br/>"
                "&nbsp;&nbsp;--member=\"serviceAccount:terraform-sa@home-slabs.iam.gserviceaccount.com\" \\<br/>"
                "&nbsp;&nbsp;--role=\"roles/owner\"",
                code_style
            )
        ]], colWidths=[504], style=[('BACKGROUND', (0,0), (-1,-1), code_bg), ('PADDING', (0,0), (-1,-1), 6)]),
        Spacer(1, 6)
    ]))

    # Sub item C
    story.append(KeepTogether([
        Paragraph("C. Geração da Chave Privada JSON e Configuração do ADC", h2_style),
        Paragraph("Baixamos a chave criptográfica JSON, configuramos no local oficial do ADC e persistimos a variável de ambiente:", body_style),
        Table([[
            Paragraph(
                "# 1. Geração da chave JSON privada<br/>"
                "gcloud iam service-accounts keys create ~/.config/gcloud/terraform-sa-key.json \\<br/>"
                "&nbsp;&nbsp;--iam-account=terraform-sa@home-slabs.iam.gserviceaccount.com \\<br/>"
                "&nbsp;&nbsp;--project=home-slabs<br/><br/>"
                "# 2. Configuração do arquivo de credenciais padrão (ADC)<br/>"
                "cp ~/.config/gcloud/terraform-sa-key.json ~/.config/gcloud/application_default_credentials.json<br/><br/>"
                "# 3. Persistência da variável de ambiente no perfil do usuário (~/.bashrc)<br/>"
                "echo 'export GOOGLE_APPLICATION_CREDENTIALS=\"/home/vagrant/.config/gcloud/terraform-sa-key.json\"' >> ~/.bashrc",
                code_style
            )
        ]], colWidths=[504], style=[('BACKGROUND', (0,0), (-1,-1), code_bg), ('PADDING', (0,0), (-1,-1), 6)]),
        Spacer(1, 6)
    ]))

    # Sub item D
    diff_data = [
        [Paragraph("<b>Arquivo</b>", body_style), Paragraph("<b>Linha</b>", body_style), Paragraph("<b>Antes</b>", body_style), Paragraph("<b>Depois (Atualizado)</b>", body_style)],
        [Paragraph("terraform.tfvars", body_style), Paragraph("1", body_style), Paragraph("<font color='#B3261E'>- gcp_project = \"gcplearn9\"</font>", body_style),
         Paragraph("<font color='#137333'><b>+ gcp_project = \"home-slabs\"</b></font>", body_style)]
    ]
    t_diff = Table(diff_data, colWidths=[110, 44, 175, 175])
    t_diff.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))
    story.append(KeepTogether([
        Paragraph("D. Correção no Arquivo terraform.tfvars", h2_style),
        Paragraph("Ajustamos a variável de entrada para que todas as chamadas do Terraform apontem para o seu projeto real:", body_style),
        t_diff,
        Spacer(1, 8)
    ]))

    # Section 3: Validação
    result_box = [[
        Paragraph(
            "<b>$ terraform init</b><br/>"
            "<font color='#4ADE80'>✔ Successfully configured the backend \"gcs\"!</font><br/>"
            "<font color='#4ADE80'>✔ Finding hashicorp/google versions matching \">= 5.42.0\"...</font><br/>"
            "<font color='#4ADE80'>✔ Installing hashicorp/google v8.8.1...</font><br/>"
            "<b>Terraform has been successfully initialized!</b><br/><br/>"
            "<b>$ terraform validate</b><br/>"
            "<font color='#4ADE80'>✔ Success! The configuration is valid.</font>",
            code_style
        )
    ]]
    t_result = Table(result_box, colWidths=[504])
    t_result.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#0F172A")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#10B981")),
        ('PADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(KeepTogether([
        Paragraph("3. Validação e Resultados da Execução", h1_style),
        Paragraph("Ambos os comandos essenciais foram validados com êxito absoluto:", body_style),
        t_result,
        Spacer(1, 8)
    ]))

    # Section 4: Próximos Passos
    steps_table_data = [
        [Paragraph("<b>Comando</b>", body_style), Paragraph("<b>Finalidade</b>", body_style)],
        [Paragraph("<code>terraform plan</code>", code_style), Paragraph("Gera e exibe o plano de execução, detalhando a criação da VPC, Sub-rede, Regras de Firewall, Service Account e Cluster GKE.", body_style)],
        [Paragraph("<code>terraform apply</code>", code_style), Paragraph("Executa o provisionamento real de toda a infraestrutura no Google Cloud Platform.", body_style)],
        [Paragraph("<code>gcloud container clusters get-credentials ...</code>", code_style), Paragraph("Configura o <code>kubectl</code> para interagir diretamente com o novo cluster GKE criado.", body_style)],
    ]
    t_steps = Table(steps_table_data, colWidths=[160, 344])
    t_steps.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#E2E8F0")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('PADDING', (0,0), (-1,-1), 5),
    ]))

    story.append(KeepTogether([
        Paragraph("4. Próximos Passos Recomendados", h1_style),
        Paragraph("Com o backend autenticado e validado, o fluxo de implantação pode seguir normalmente:", body_style),
        t_steps
    ]))

    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF build complete:", filename)

if __name__ == "__main__":
    output_path = "/home/vagrant/GKE/Files/terraform-on-google-kubernetes-engine/09-GKE-Public-Standard-Cluster/p1-gke-public-cluster/relatorio_modificacoes_terraform.pdf"
    build_pdf(output_path)
