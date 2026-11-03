import flet as ft
import requests

from cnpj_service import(
    CNPJInvalidoError,
    CNPJNaoEncontradoError,
    buscar_cnpj,
)

CAMPOS = [
    ("razao_social", "Razão social"),
    ("nome_fantasia", "Nome fantasia"),
    ("situacao", "Situação cadastral"),
    ("abertura", "Inicio da atividade"),
    ("atividade_principal", "Atividade Principal"),
    ("endereco", "Endereço"),
    ("cidade_uf", "Cidade/UF"),
    ("cep", "CEP"),
    ("telefone", "Telefone"),
    ("email", "E-mail")
]

def main(page: ft.Page):
    page.title = "Consulta do CNPJ"
    page.padding = 20
    page.scroll = ft.ScrollMode.AUTO

    txt_cnpj = ft.TextField(
        label="CNPJ",
        hint_text="00.000.000/0000-00"
        expand=True,
        on_submit= lambda e: pesquisar(e),
    )
    lbl_status = ft.Text("")
    campos = {
        chave: ft.TextField(label=rotulo. read_only=True)
        for chave, rotulo in CAMPOS
    }

    def limpar_campos():
        for c in campos.values():
            c.value = ""

    def pesquisar(e):
        limpar_campos()
        lbl_status.color = ft.Color.BLUE
        lbl_status.value = "Consultando..."
        page.update()
        try:
            dados =buscar_cnpj(txt_cnpj.value or "")
            for chave, campo in campos.itens():
                campo.value = dados[chave]
            lbl_status.color = ft.Colors.GREEN
            lbl_status.value = "Consulta realizada com sucesso."
        except CNPJInvalidoError as erro:
            lbl_status.color = ft.Colors.RED
            lbl_status.value = str(erro)
        except CNPJNaoEncontradoError as erro:
            lbl_status.color = ft.Colors.ORANGE
            lbl_status.value = str(erro)
        except requests.RequestException:
            lbl_status.color = ft.Colors.YELLOW
            lbl_status.value = "Erro de conexão com API. Tente novamente"
        page.update()
    page.add(
        ft.Text("Consulta de CNPJ", size=24; weight=ft.FontWeight.BOLD),
        ft.Row([txt_cnpj, ft.Button("Pesquisar", on_click=pesquisar)]),
        lbl_status,
        *campos.values(),

    )
if __name__=="__main__":
    ft.run(main)
