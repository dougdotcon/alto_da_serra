from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import uvicorn

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dados de entrada
class LoginData(BaseModel):
    email: str  # aqui é o campo 'user' do banco
    password: str
class MesaUpdate(BaseModel):
    id: int
    cliente: str
    status: str
    user_id: str
    
class ProdutoData(BaseModel):
    id: int
    nome: str
    preco: float

# Consumo retornado via API
class ConsumoData(BaseModel):
    id: int
    nome: str      # nome do produto
    preco: float   # preço unitário
    quantidade: int
    total: float 

class NovoConsumo(BaseModel):
    produto_id: int
    quantidade: int
    mesa_id: str
    
class AbaterConsumoData(BaseModel):
    consumo_id: int
    mesa_id: str
    quantidade: int

@app.post("/abater_consumo")
def abater_consumo(data: AbaterConsumoData):
    try:
        conn = sqlite3.connect("restaurante.db")
        cursor = conn.cursor()

        # Verifica se o item de consumo existe e pertence à mesa
        cursor.execute("""
            SELECT quantidade, total, produto_id 
            FROM consumo 
            WHERE id = ? AND mesa_id = ?
        """, (data.consumo_id, data.mesa_id))
        row = cursor.fetchone()

        if not row:
            raise HTTPException(status_code=404, detail="Item de consumo não encontrado para essa mesa.")

        quantidade_atual, total_atual, produto_id = row

        if data.quantidade > quantidade_atual:
            raise HTTPException(status_code=400, detail="Quantidade a abater maior que a existente.")

        elif data.quantidade == quantidade_atual:
            # Exclui o item
            cursor.execute("DELETE FROM consumo WHERE id = ?", (data.consumo_id,))
        else:
            # Atualiza a quantidade e o total
            nova_quantidade = quantidade_atual - data.quantidade

            # Busca preço do produto para recalcular total
            cursor.execute("SELECT preco_venda FROM produtos WHERE id = ?", (produto_id,))
            produto = cursor.fetchone()
            if not produto:
                raise HTTPException(status_code=404, detail="Produto não encontrado.")

            preco_unitario = produto[0]
            novo_total = nova_quantidade * preco_unitario

            cursor.execute("""
                UPDATE consumo 
                SET quantidade = ?, total = ?
                WHERE id = ?
            """, (nova_quantidade, novo_total, data.consumo_id))

        conn.commit()
        conn.close()
        return {"mensagem": "Consumo atualizado com sucesso."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao abater consumo: {str(e)}")
        
@app.get("/produtos")
def listar_produtos():
    try:
        conn = sqlite3.connect("restaurante.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id, nome, preco_venda FROM produtos")
        produtos = [
            {
                "id": row[0],
                "nome": row[1],
                "preco": row[2]
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return produtos

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar produtos: {str(e)}")    
     
@app.get("/consumo/{mesa_id}")
def listar_consumo(mesa_id: str):
    try:
        conn = sqlite3.connect("restaurante.db")
        cursor = conn.cursor()

        cursor.execute("""
        SELECT c.id, p.nome, p.preco_venda, c.quantidade, c.total
        FROM consumo c
        JOIN produtos p ON c.produto_id = p.id
        WHERE c.mesa_id = ?
        """, (mesa_id,))

        itens = [
            {
                "id": row[0],
                "nome": row[1],
                "preco": row[2],
                "quantidade": row[3],
                "total": row[4]
            }
            for row in cursor.fetchall()
        ]

        conn.close()
        return itens

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar consumo da mesa: {str(e)}")
            
@app.get("/configuracao")
def get_config():
    return {
        "nome_restaurante": "Alto da Serra",
        "mesas": 30,
        "tipo_usuario": "admin"
    }    
    
@app.post("/atualizar_mesa")
def atualizar_mesa(data: MesaUpdate):
    try:
        conn = sqlite3.connect("restaurante.db")
        cursor = conn.cursor()

        # Verifica se a mesa está em uso por outra pessoa
        cursor.execute("SELECT em_uso_por FROM mesas WHERE id = ?", (f"M{data.id}",))
        row = cursor.fetchone()
        if row and row[0] and row[0] !="livre":
            raise HTTPException(status_code=404, detail=f"Mesa em uso por outro usuário: {row[0]}")

        # Verifica se o status é válido
        cursor.execute("SELECT id FROM status_mesas WHERE LOWER(status) = LOWER(?)", (data.status,))
        status_row = cursor.fetchone()
        if not status_row:
            raise HTTPException(status_code=400, detail="Status inválido.")
        status_id = status_row[0]

        # Atualiza mesa
        cursor.execute("""
            UPDATE mesas
            SET cliente = ?, status_id = ?, data_abertura = CURRENT_TIMESTAMP, em_uso_por = NULL
            WHERE id = ?
        """, (data.cliente, status_id, f"M{data.id}"))

        conn.commit()
        conn.close()

        return {"mensagem": "Mesa atualizada com sucesso."}

    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar mesa: {str(e)}")
      
@app.get("/mesas")
def listar_mesas():
    conn = sqlite3.connect("restaurante.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT m.id, m.cliente, m.cpf_cnpj, s.status, m.valor_total
        FROM mesas m
        JOIN status_mesas s ON m.status_id = s.id
    """)
    mesas = [
        {
            "id": row[0],
            "nome": f"Mesa {row[0]}",
            "cliente": row[1] or "",
            "cpf_cnpj": row[2] or "",
            "status": row[3],
            "total": row[4]
        }
        for row in cursor.fetchall()
    ]
    conn.close()
    return mesas

@app.post("/login")
def login(data: LoginData):
    try:
        conn = sqlite3.connect("restaurante.db")
        cursor = conn.cursor()

        cursor.execute("""
            SELECT u.nome, t.nome, u.user
            FROM usuarios u
            JOIN tipos_usuarios t ON u.tipo_usuario_id = t.id
            WHERE u.user = ? AND u.senha = ?
        """, (data.email, data.password))

        row = cursor.fetchone()
        conn.close()

        if row:
            nome, tipo,user = row
            return {
                "nome": nome,
                "tipo": tipo,
                "user": user,
                "status": "ok"
            }
        else:
            raise HTTPException(status_code=401, detail="Credenciais inválidas")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao consultar o banco: {str(e)}")

# Roda local
if __name__ == "__main__":
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)
