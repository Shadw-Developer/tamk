# 📂 Estrutura Completa do Projeto T.A.M.K

> Este documento mapeia todos os arquivos e diretórios do T.A.M.K, incluindo as adições para o suporte a WebApps. Use-o como referência para navegar no código-fonte.

```
tamk/                                 # Raiz do projeto T.A.M.K
│
├── 📄 .gitignore                    # Arquivos e pastas ignorados pelo Git
├── 📄 .si.json                      # Configuração do SmartIDE
├── 📄 README.md                     # Documentação principal do projeto
├── 📄 CONTRIBUTING.md               # Guia para contribuidores
├── 📄 VERSIONING.md                 # Esquema de versionamento
├── 📄 setup-install.sh              # Script de instalação para Termux
│
├── 📁 documentation/                # Documentação completa do projeto
│   ├── 📄 ARCHITECTURE.md           # Documentação da arquitetura
│   ├── 📄 API_COMPONENTS.md         # Referência de APIs e componentes
│   ├── 📄 CHANGELOG.md              # Histórico de mudanças
│   ├── 📄 CONTRIBUTING.md           # Guia de contribuição para desenvolvedores
│   ├── 📄 DEV_GUIDE.md              # Guia de desenvolvimento e deployment
│   ├── 📄 FAQ.md                    # Perguntas Frequentes
│   ├── 📄 QUICKSTART.md             # Guia rápido de início
│   ├── 📄 STRUCTURE.md              # Este arquivo (estrutura de diretórios)
│   └── 📄 WEBAPP_TEMPLATES.md       # Código-fonte dos templates WebApp
│
├── 📁 assets/                       # Recursos estáticos e templates
│   └── 📁 templates/                # Sistema de templates para geração de projetos
│       │
│       ├── 📁 console/              # Template para aplicativos console (Kotlin puro)
│       │   └── 📄 Main.kt.tmpl      # Template de código para app console
│       │
│       ├── 📁 ui_apk/               # Template para apps Android com UI nativa
│       │   ├── 📄 AndroidManifest.xml.tmpl
│       │   ├── 📄 MainActivity.kt.tmpl
│       │   ├── 📄 activity_main.xml.tmpl
│       │   ├── 📄 strings.xml.tmpl
│       │   ├── 📄 styles.xml.tmpl
│       │   └── 📄 icon.xml.tmpl
│       │
│       └── 📁 webapp/               # Template para WebApps (HTML/CSS/JS em APK)
│           ├── 📄 AndroidManifest.xml.tmpl  # Manifest com permissões de internet
│           ├── 📄 MainActivity.kt.tmpl      # Activity com WebView configurado
│           ├── 📄 index.html.tmpl           # Template HTML de exemplo
│           ├── 📄 strings.xml.tmpl          # Strings de recursos
│           ├── 📄 styles.xml.tmpl           # Estilos do tema Android
│           └── 📄 icon.xml.tmpl             # Ícone padrão do app
│
├── 📁 src/                          # Código-fonte principal do sistema T.A.M.K
│   ├── 📄 main.py                   # Ponto de entrada da CLI - orquestração principal
│   │
│   ├── 📁 config/                   # Configurações e constantes do sistema
│   │   └── 📄 tamk_config.py        # Configurações globais, versões e paths
│   │
│   ├── 📁 controllers/              # Controladores - lógica de negócio principal
│   │   ├── 📄 setup_controller.py   # Configuração inicial e download de SDK
│   │   ├── 📄 build_controller.py   # Compilação, assinatura e build do APK
│   │   ├── 📄 install_controller.py # Instalação no dispositivo Android
│   │   ├── 📄 run_controller.py     # Execução e monitoramento do app
│   │   └── 📄 project_manager.py    # Gerenciamento do ciclo de vida dos projetos
│   │
│   ├── 📁 organization/             # Fábrica e estruturas de organização de projetos
│   │   ├── 📄 factory.py            # Fábrica de projetos - cria estrutura base
│   │   └── 📁 structures/           # Blueprints de diferentes tipos de projeto
│   │       ├── 📄 ui_apk.py         # Estrutura para app Android com interface nativa
│   │       ├── 📄 console.py        # Estrutura para app de linha de comando
│   │       └── 📄 webapp.py         # Estrutura para WebApp (NOVO)
│   │
│   └── 📁 utils/                    # Utilitários e helpers do sistema
│       ├── 📄 logger.py             # Sistema de logging unificado com cores
│       └── 📄 colors.py             # Códigos ANSI para colorização no terminal
│
└── 📁 development/                  # (Criado automaticamente após setup)
    ├── 📁 sdk/                      # SDK do Android (android.jar)
    └── 📁 secret/                   # Keystore de debug global
```

## Estrutura de um Projeto Gerado (Tipo: WebApp)

Quando você executa `tamk --create` e escolhe a opção **WebApp**, o T.A.M.K gera a seguinte estrutura no diretório de destino:

```
meu-webapp/                          # Diretório raiz do projeto gerado
│
├── 📄 AndroidManifest.xml           # Manifesto do aplicativo Android
├── 📄 tamk.config                   # Configuração do projeto (tipo, nome, versão)
│
├── 📁 secret/                       # Chaves de segurança (NÃO VERSIONAR)
│   └── 📄 project.keystore          # Keystore privada para assinatura do APK
│
├── 📁 res/                          # Recursos Android (ícones, estilos, strings)
│   ├── 📁 values/
│   │   ├── 📄 strings.xml
│   │   └── 📄 styles.xml
│   └── 📁 mipmap/
│       ├── 📄 ic_launcher.xml
│       └── 📄 ic_launcher_round.xml
│
├── 📁 src/
│   └── 📁 main/
│       ├── 📁 assets/               # ⭐ COLOQUE SEU SITE AQUI ⭐
│       │   └── 📄 index.html        # Arquivo HTML principal
│       │   └── 📁 css/              # (Exemplo) Seus arquivos CSS
│       │   └── 📁 js/               # (Exemplo) Seus arquivos JavaScript
│       │   └── 📁 images/           # (Exemplo) Suas imagens
│       │
│       └── 📁 kotlin/               # Código nativo do aplicativo
│           └── 📁 com/
│               └── 📁 example/
│                   └── 📁 meuwebapp/
│                       └── 📄 MainActivity.kt  # Activity com WebView
│
├── 📁 development/                  # Ambiente de desenvolvimento local
│   ├── 📁 sdk/                      # SDK do Android (android.jar) - cópia local
│   └── 📁 secret/                   # Keystore de debug (se não houver project.keystore)
│
├── 📁 assets/                       # (Criado durante o build)
│   └── 📁 cache/                    # Cache de compilação (arquivos temporários)
│
└── 📄 app-final.apk                 # APK gerado após o build (assinado e pronto)
```

## Notas Importantes

-   **Pasta `assets/`**: Esta é a pasta mais importante para desenvolvedores de WebApps. Todo o conteúdo desta pasta será empacotado dentro do APK e acessível via `file:///android_asset/` no `WebView`.
-   **Keystore**: A pasta `secret/` contém informações sensíveis. **Adicione-a ao seu `.gitignore` para evitar expor suas chaves de assinatura.**
-   **Cache de Build**: A pasta `assets/cache/` é criada durante o processo de build e contém arquivos temporários. Ela pode ser deletada a qualquer momento sem impactar o código-fonte do seu projeto.
