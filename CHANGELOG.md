# Changelog

## [1.0.1] - 2025-06-24

### Corrigido
#### Backend
- Corrigido erro 500 na listagem de mesas
  - Removido prefixo incorreto 'm.' da coluna cpf_cnpj na consulta SQL da função listar_mesas()

#### Frontend
- Corrigidas referências incorretas de ícones
  - Atualizado 'ft.icons' para 'ft.Icons' em:
    - drawer.py (CLOSE, TABLE_RESTAURANT, INVENTORY_2, LUNCH_DINING, INVENTORY, LOGOUT)
    - painel.py (MENU, SEARCH)
    - abertura_mesa.py (ADD)
    - consumo_utils.py (DELETE, ATTACH_MONEY)
    - detalhes_mesa.py (ADD)
- Removido parâmetro inválido 'height' do componente Dropdown em filtro_abertura.py
- Adicionada importação faltante de inicializar_painel_components em painel.py
- Corrigido parâmetro na função controler_adcionar_pedido (objeto mesa completo ao invés de apenas mesa['nome'])
- Personalização completa da identidade visual:
  - Substituído ícone padrão do Flet pelo logo do fornecedor na janela/aba do navegador
  - Implementada tela de splash personalizada usando ft.AppView com efeitos de animação
  - Configurada logo do fornecedor com escala e opacidade animada
- Removido arquivo index.html não utilizado da pasta assets

### Melhorado
#### Frontend
- Implementada atualização robusta da interface após pagamento de itens
  - Adicionada função atualizar_interface que:
    - Busca dados atualizados da mesa do servidor
    - Atualiza os dados da mesa em memória
    - Atualiza o diálogo de detalhes
    - Força atualização da página para refletir mudanças
  - Substituído callback simples por atualizar_interface no dialogo_pagar_item

### Notas da Versão
Esta atualização resolve problemas críticos de usabilidade e erros do sistema, com foco especial na correção do fluxo de pagamento de itens e na consistência da interface do usuário. As alterações garantem que todas as operações são refletidas corretamente tanto no backend quanto na interface do usuário.