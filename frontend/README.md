# Alto da Serra - Frontend Django

Este é o frontend Django para o sistema de gerenciamento de restaurante Alto da Serra, desenvolvido para substituir a interface Flet original.

## 🚀 Características

- **Interface Web Responsiva**: Desenvolvida com Bootstrap 5
- **Integração com API**: Conecta-se ao backend FastAPI existente
- **Gestão de Mesas**: Visualização e controle completo das mesas
- **Sistema de Pedidos**: Adição, edição e remoção de pedidos
- **Pagamentos**: Sistema completo de finalização de contas
- **Dashboard Interativo**: Estatísticas em tempo real
- **Design Moderno**: Interface limpa e intuitiva

## 📋 Pré-requisitos

- Python 3.8+
- Django 4.2+
- Backend FastAPI rodando na porta 8000

## 🛠️ Instalação

1. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

2. **Executar migrações**:
```bash
python manage.py migrate
```

3. **Iniciar servidor de desenvolvimento**:
```bash
python manage.py runserver 8080
```

4. **Acessar aplicação**:
```
http://127.0.0.1:8080
```

## 📁 Estrutura do Projeto

```
frontend/
├── restaurante_frontend/          # Configurações do Django
│   ├── settings.py               # Configurações principais
│   ├── urls.py                   # URLs principais
│   └── wsgi.py                   # WSGI config
├── mesas/                        # App principal
│   ├── views.py                  # Views e APIs
│   ├── urls.py                   # URLs do app
│   └── models.py                 # Modelos (não utilizados)
├── templates/                    # Templates HTML
│   ├── base.html                 # Template base
│   └── mesas/                    # Templates específicos
│       ├── login.html            # Página de login
│       ├── dashboard.html        # Dashboard principal
│       ├── mesa_detail.html      # Detalhes da mesa
│       └── produtos.html         # Catálogo de produtos
├── static/                       # Arquivos estáticos
│   ├── css/
│   │   └── custom.css           # CSS personalizado
│   └── js/
│       ├── dashboard.js         # JavaScript do dashboard
│       └── pedidos.js           # JavaScript dos pedidos
└── requirements.txt              # Dependências Python
```

## 🔧 Configuração

### Settings.py
- **API_BASE_URL**: URL do backend FastAPI (padrão: http://127.0.0.1:8000)
- **CORS**: Configurado para permitir comunicação com o backend
- **Sessões**: Configuradas para autenticação

### URLs Principais
- `/` - Redireciona para login
- `/login/` - Página de autenticação
- `/dashboard/` - Dashboard principal
- `/mesa/<id>/` - Detalhes da mesa
- `/produtos/` - Catálogo de produtos
- `/api/` - APIs para integração JavaScript

## 🎯 Funcionalidades

### Dashboard
- Visualização de todas as mesas
- Filtros por mesa, cliente e status
- Estatísticas em tempo real
- Atualização automática

### Gestão de Mesas
- Status: Livre, Ocupada, Reservada
- Informações do cliente
- Total de consumo
- Histórico de pedidos

### Sistema de Pedidos
- Adição de produtos às mesas
- Controle de quantidade
- Cálculo automático de totais
- Remoção/abatimento de itens

### Pagamentos
- Múltiplas formas de pagamento
- Cálculo de desconto
- Cálculo de troco
- Finalização de contas

## 🔌 APIs Integradas

### Endpoints Utilizados
- `GET /mesas` - Lista todas as mesas
- `GET /consumo/{mesa_id}` - Consumo de uma mesa
- `GET /produtos` - Lista de produtos
- `POST /adicionar_pedido` - Adiciona pedido
- `POST /abater_consumo` - Remove/abate consumo
- `POST /atualizar_mesa` - Atualiza dados da mesa
- `POST /finalizar_conta` - Finaliza conta
- `POST /login` - Autenticação

## 🎨 Interface

### Design System
- **Cores**: Gradientes modernos
- **Tipografia**: Segoe UI
- **Componentes**: Bootstrap 5
- **Ícones**: Bootstrap Icons
- **Responsividade**: Mobile-first

### Temas
- **Status das Mesas**:
  - Verde: Mesa livre
  - Vermelho: Mesa ocupada
  - Amarelo: Mesa reservada

## 📱 Responsividade

O sistema é totalmente responsivo e funciona em:
- Desktop (1200px+)
- Tablet (768px - 1199px)
- Mobile (< 768px)

## 🔒 Segurança

- **CSRF Protection**: Tokens CSRF em todas as requisições POST
- **Sessões**: Controle de sessão para autenticação
- **Validação**: Validação de dados no frontend e backend

## 🚀 Deploy

### Desenvolvimento
```bash
python manage.py runserver 8080
```

### Produção
1. Configure `DEBUG = False` em settings.py
2. Configure `ALLOWED_HOSTS`
3. Colete arquivos estáticos: `python manage.py collectstatic`
4. Use servidor WSGI (Gunicorn, uWSGI)

## 🤝 Integração com Backend

O frontend se comunica com o backend FastAPI através de:
- **Requisições HTTP**: Para operações CRUD
- **Sessões**: Para manter estado de autenticação
- **JSON**: Formato de dados padrão

## 📝 Logs e Debug

- **Django Debug**: Ativado em desenvolvimento
- **Console Logs**: JavaScript logs no navegador
- **Network Tab**: Para debug de APIs

## 🔄 Atualizações Futuras

- [ ] Relatórios avançados
- [ ] Notificações push
- [ ] Modo offline
- [ ] Impressão de comandas
- [ ] Integração com impressoras

## 📞 Suporte

Para suporte técnico ou dúvidas sobre o sistema, consulte a documentação do backend ou entre em contato com a equipe de desenvolvimento.

---

**Desenvolvido com Django 4.2 e Bootstrap 5**
