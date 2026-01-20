#!/bin/bash

# Define a variável PREFIX se ela não estiver configurada
: "${PREFIX:=/data/data/com.termux/files/usr}"

# Cores e Estilos
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'
BOLD='\033[1m'

# Instala toilet se não existir
if ! command -v toilet &> /dev/null; then
    if command -v pkg &> /dev/null; then
        pkg install toilet -y &> /dev/null
    fi
fi

center_block() {
    local input="$1"
    local cols=$(tput cols 2>/dev/null || echo 80)
    while IFS= read -r line; do
        local clean_line=$(echo -e "$line" | sed 's/\x1b\[[0-9;]*m//g')
        local length=${#clean_line}
        local padding=$(( (cols - length) / 2 ))
        [ $padding -lt 0 ] && padding=0
        printf "%${padding}s" ""
        echo -e "$line"
    done <<< "$input"
}

show_banner() {
    clear
    local art=$(toilet -f standard -F metal "T.A.M.K")
    center_block "$art"
    center_block "${BLUE}===========================================${NC}"
    center_block "${BLUE}Termux Apk Manager Kit • Installer (2026)${NC}"
    center_block "${BLUE}===========================================${NC}"
    echo ""
}

loading_animation() {
    local pid=$1
    local spin='⣷⣯⣟⡿⢿⣻⣽⣾'
    while kill -0 "$pid" 2>/dev/null; do
        for i in {0..7}; do
            printf "\r${YELLOW}[${spin:$i:1}]${NC} Processando... "
            sleep 0.1
        done
    done
    wait "$pid"
}

# --- INÍCIO ---
show_banner

if [[ "$PREFIX" == *"/org.smartide.code"* ]]; then
    env_name="SmartIDE"
else
    env_name="Termux"
fi

echo -e "${BLUE}==>${NC} Ambiente detectado: ${GREEN}$env_name${NC}"

# 1. Dependências
echo -e "${YELLOW}[1/3]${NC} Validando dependências..."
if command -v pkg &> /dev/null; then
    (pkg install -y python termux-tools aapt2 apksigner openjdk-21 zip > /dev/null 2>&1) &
    loading_animation $!
    echo -e " ${GREEN}[OK]${NC}"
fi

# 2. Configuração de Diretórios (OPÇÃO 3)
echo -e "${YELLOW}[2/3]${NC} Instalando arquivos em $PREFIX/opt/tamk..."
INSTALL_PATH="$PREFIX/opt/tamk"
mkdir -p "$INSTALL_PATH"

# Copia tudo da pasta atual para o diretório de destino (incluindo src e outras pastas)
cp -rf . "$INSTALL_PATH/"

# 3. Criação do Executável Global
echo -e "${YELLOW}[3/3]${NC} Criando link no sistema..."
cat << EOF > "$PREFIX/bin/tamk"
#!/bin/bash
# T.A.M.K Global Executor (2026)
export TAMK_HOME="$INSTALL_PATH"
python3 "\$TAMK_HOME/src/main.py" "\$@"
EOF

chmod +x "$PREFIX/bin/tamk"
echo -e " ${GREEN}[OK]${NC}"

# --- FINALIZAÇÃO ---
clear
echo ""
art_sucesso=$(toilet -f standard -F metal "SUCESSO")
center_block "$art_sucesso"

center_block "${GREEN}===========================================${NC}"
center_block "${BOLD}   INSTALAÇÃO NO $env_name CONCLUÍDA!     ${NC}"
center_block "${GREEN}===========================================${NC}"
echo ""
echo -e "${BLUE}==>${NC} O comando ${YELLOW}tamk${NC} agora está disponível globalmente."
echo -e "${BLUE}==>${NC} Local da instalação: ${NC}$INSTALL_PATH"
echo -e "${BLUE}==>${NC} Teste agora digitando: ${GREEN}tamk --version${NC}"
echo ""
