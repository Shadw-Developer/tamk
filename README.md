<p align="center">
  <b>📱 T.A.M.K — Termux APK Manager Kit</b>
   <br>
   <br>
    
  <img src="https://img.shields.io/badge/Version-2026.1.0-blueviolet?style=for-the-badge" alt="Version">
  <img src="https://img.shields.io/badge/Platform-Termux-orange?style=for-the-badge" alt="Platform">
  <img src="https://img.shields.io/badge/Language-Python%20%26%20Kotlin-blue?style=for-the-badge" alt="Languages">
  <img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge" alt="License">
  <img src="https://img.shields.io/github/last-commit/SEU_USUARIO/SEU_REPOSITORIO?style=for-the-badge" alt="Last Commit">
</p>

📝 Descrição

O T.A.M.K (Termux APK Manager Kit) é um framework de automação profissional para desenvolvimento Android nativo diretamente no Termux. Projetado para desenvolvedores que buscam independência de hardware, ele permite criar, compilar, assinar e instalar aplicativos APK utilizando apenas dispositivos móveis.

Diferente de soluções convencionais, o T.A.M.K implementa um motor de Scaffolding Profissional com separação clara entre lógica do sistema e templates de código. Isso garante que cada projeto gerado seja um ecossistema autônomo, contendo sua própria SDK e chaves de segurança criptografadas.

🚀 Diferenciais Estratégicos

· Isolamento de SDK (development/): Cada projeto possui sua própria cópia do android.jar oficial do Google, garantindo portabilidade total e prevenindo conflitos com atualizações globais do sistema.
· Template Engine Desacoplado: Arquitetura modular que separa a lógica Python dos arquivos XML/Kotlin. Modifique a aparência e comportamento dos apps através da pasta assets/templates sem impactar o núcleo do sistema.
· Pipeline de Build Validado: Verificação antecipada de credenciais (Keystore) antes de iniciar o processo de compilação, otimizando tempo e recursos computacionais.
· Instalação Nativa: Integração direta com o instalador do Android via termux-open, proporcionando experiência fluida do desenvolvimento à implantação.

🏗️ Arquitetura do Projeto

```
tamk/
├── assets/
│   └── templates/           # Arquivos .tmpl (XML, Kotlin, Manifest)
├── src/
│   ├── config/              # Configurações de ambiente e versão
│   ├── controllers/         # Motores: Build, Setup, Install e Run
│   ├── organization/        # Factory e estruturas de projetos
│   ├── utils/               # Logger e auxiliares de sistema
│   └── main.py              # Ponto de entrada (CLI)
└── STRUCTURE.md             # Documentação arquitetural detalhada
```

⚙️ Instalação e Configuração

Pré-requisitos

Certifique-se de ter os pacotes base instalados no Termux:

```bash
pkg update && pkg upgrade
pkg install python openjdk-17 kotlin wget zip apksigner aapt2
pkg install termux-tools termux-api
```

Instalação do Kit

1. Clone o repositório:

```bash
https://github.com/Deep-Shadow/tamk.git
cd tamk
```

1. Configuração do PATH (opcional):

```bash
echo "alias tamk='python3 -B $(pwd)/src/main.py'" >> ~/.bashrc
source ~/.bashrc
```

1. Verificação da instalação:

```bash
python3 src/main.py --version
```

📖 Guia de Uso (CLI)

Criando um Novo Projeto

```bash
tamk --create
```

Siga o assistente interativo para definir:

· Nome do aplicativo e pacote
· Informações do autor
· Versão e build number
· Senha da Keystore (criptografada localmente)

O T.A.M.K baixará automaticamente a SDK oficial do Android para dentro do diretório do projeto.

Build e Assinatura

Na pasta do projeto criado, execute:

```bash
tamk -b -p sua_senha
```

O sistema validará sua senha e credenciais antes de iniciar a pipeline de compilação.

Instalação Direta

```bash
tamk -l
```

Nota: Requer permissões de armazenamento (termux-setup-storage).

Execução Rápida (Build + Install)
