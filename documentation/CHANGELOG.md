# 📋 Changelog do T.A.M.K

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo. O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/), e este projeto adere ao [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [2026.2.0] - 2026-01-19

### ✨ Adicionado

-   **Suporte a WebApps**: Introdução de um novo tipo de projeto que permite encapsular aplicações web (HTML, CSS, JavaScript) em um APK nativo do Android.
    -   Nova classe `WebAppStructure` em `src/organization/structures/webapp.py`.
    -   Novos templates em `assets/templates/webapp/`:
        -   `AndroidManifest.xml.tmpl` com permissões de internet.
        -   `MainActivity.kt.tmpl` com configuração otimizada de `WebView`.
        -   `index.html.tmpl` como ponto de partida para desenvolvimento web.
    -   Criação automática da pasta `src/main/assets/` em projetos WebApp, onde o desenvolvedor coloca seus arquivos web.
-   **Documentação Completa**: Novos arquivos de documentação para guiar desenvolvedores:
    -   `ARCHITECTURE.md`: Visão geral da arquitetura do sistema.
    -   `API_COMPONENTS.md`: Referência técnica de classes e módulos.
    -   `DEV_GUIDE.md`: Guia prático de desenvolvimento e deployment.
    -   `WEBAPP_TEMPLATES.md`: Código-fonte completo de todos os templates de WebApp.
    -   `CHANGELOG.md`: Este arquivo, para rastrear mudanças de versão.

### 🔧 Modificado

-   **`BuildController`**: Atualizado para detectar e empacotar a pasta `src/main/assets/` durante o build, usando a flag `-A` do `aapt2 link`.
-   **`ProjectFactory`**: Adicionado o mapeamento `"webapp": WebAppStructure()` para suportar a criação de projetos WebApp.
-   **`README.md`**: Atualizado para incluir informações sobre o novo tipo de projeto WebApp e seu fluxo de trabalho.
-   **`STRUCTURE.md`**: Expandido para documentar a estrutura de diretórios de um projeto WebApp gerado.

### 🐛 Corrigido

-   Correção na lógica de detecção de Keystore no `BuildController`, garantindo que a senha correta seja usada para projetos com Keystore privada.

---

## [2026.1.0-alpha] - 2026-01-01

### ✨ Adicionado

-   **Lançamento Inicial**: Primeira versão pública do T.A.M.K.
    -   Suporte para criação de projetos do tipo **UI APK** (aplicativos Android nativos com interface XML).
    -   Suporte para criação de projetos do tipo **Console** (aplicações Kotlin de linha de comando).
    -   Pipeline completo de build: compilação de recursos, código Kotlin, geração de DEX, assinatura e alinhamento de APK.
    -   Sistema de templates modular com placeholders (`{{NAME}}`, `{{PACKAGE}}`, etc.).
    -   Script de instalação `setup-install.sh` para Termux.
    -   Documentação básica em `README.md` e `CONTRIBUTING.md`.

---

## Formato de Versionamento

O T.A.M.K utiliza o esquema de versionamento `AAAA.M.P-estabilidade`:

-   **AAAA**: Ano (ex: 2026)
-   **M**: Major release (mudanças significativas)
-   **P**: Minor release (correções e melhorias)
-   **estabilidade**: `alpha`, `beta`, `rc` (release candidate), ou omitido para versões estáveis

**Exemplo**: `2026.2.0` indica a segunda major release de 2026, versão estável.
