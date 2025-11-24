# Multi-stage build para otimizar tamanho da imagem
FROM python:3.12-slim as builder

# Instalar dependências de sistema
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Estágio final
FROM python:3.12-slim

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && \
    apt-get update && \
    apt-get install -y postgresql-client && \
    rm -rf /var/lib/apt/lists/*

# Diretório de trabalho
WORKDIR /app

# Copiar dependências do builder
COPY --from=builder /root/.local /home/appuser/.local

# Copiar código da aplicação
COPY --chown=appuser:appuser . .

# Adicionar local bin ao PATH
ENV PATH=/home/appuser/.local/bin:$PATH

# Mudar para usuário não-root
USER appuser

# Expor porta
EXPOSE 5001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5001/', timeout=5)" || exit 1

# Comando para rodar aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
