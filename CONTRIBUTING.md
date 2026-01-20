<p aling="center">
🤝 Guia de Contribuição para o T.A.M.K

Primeiras Palavras

Agradecemos profundamente seu interesse em contribuir com o Termux APK Manager Kit! Este projeto nasceu da necessidade de democratizar o desenvolvimento Android nativo, e cada contribuição nos aproxima desse objetivo. Sua participação é valiosa.
</p>
🏗️ Arquitetura: Entendendo o Motor

Antes de mergulhar no código, é crucial compreender a arquitetura do T.A.M.K:

Fluxo de Dados Principal

```
CLI (main.py)
    ↓
Controller Factory
    ↓
[BuildController | SetupController | InstallController]
    ↓
Template Engine
    ↓
Arquivos Gerados (Kotlin/XML) + SDK Isolada
```

Componentes Chave

1. Motor (CLI): Gerencia argumentos e orquestra os controllers
2. Controllers: Contêm a lógica de negócio específica
3. Template Engine: Substitui placeholders {{VAR}} nos arquivos .tmpl
4. Project Factory: Cria estrutura de pastas isoladas

🎯 Áreas de Contribuição

1. Novos Templates (Prioridade Alta)

Crie novos layouts profissionais em assets/templates/ui_apk/:

Estrutura de Template Exemplo:

```kotlin
// MainActivity.kt.tmpl
package {{PACKAGE_NAME}}

import androidx.appcompat.app.AppCompatActivity
// {{IMPORTS_CUSTOM}} - Placeholder para imports adicionais

class MainActivity : AppCompatActivity() {
    // {{CLASS_VARIABLES}}
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.{{LAYOUT_NAME}})
        // {{SETUP_LOGIC}}
    }
    
    // {{HELPER_METHODS}}
}
```

Tipos de Templates Desejados:

· login_activity.xml.tmpl + LoginActivity.kt.tmpl
· settings_activity.xml.tmpl com PreferenceFragment
· recycler_template.xml.tmpl com adapter base
· compose_activity.tmpl (Jetpack Compose)

2. Melhorias nos Controllers

BuildController (src/controllers/build.py):

```python
# Áreas para otimização:
- Compilação incremental (analisar modificações)
- Cache de dependências entre builds
- Suporte a multithreading para projetos grandes
```

SetupController (src/controllers/setup.py):

```python
# Melhorias potenciais:
- Download paralelo de SDK components
- Validação de checksum SHA-256
- Fallback para mirrors em caso de falha
```

3. Utilitários e Ferramentas

Logger Avançado (src/utils/logger.py):

```python
# Sugestões:
class ProgressLogger:
    def show_progress(self, current, total, unit="MB"):
        # Implementar barra de progresso ASCII
        pass
    
    def spinner(self, message):
        # Indicador de atividade
        pass
```

Scripts de Instalação:

· install.sh para Bash
· install.zsh para Zsh
· install.fish para Fish shell
· Script de desinstalação (uninstall.sh)

4. Testes e Qualidade

· Testes unitários para Template Engine
· Testes de integração para Build Pipeline
· Scripts de benchmark de performance
· Validação de compatibilidade com diferentes versões do Termux

📜 Regras de Estilo e Convenções

Python (PEP 8 Plus)

```python
# ✅ CORRETO
def compile_apk(project_path: str, keystore_pass: str) -> dict:
    """Compila o projeto APK com as credenciais fornecidas.
    
    Args:
        project_path: Caminho absoluto para o projeto
        keystore_pass: Senha da keystore (criptografada)
    
    Returns:
        dict: Resultado da compilação com status e caminho do APK
    """
    # Lógica aqui
    pass

# ❌ EVITAR
def compile(proj, pwd):
    # Documentação ausente
    # Tipagem ausente
    pass
```

Kotlin Templates

```kotlin
// ✅ CORRETO - 4 espaços, nomes descritivos
class {{ACTIVITY_NAME}} : AppCompatActivity() {
    
    private lateinit var binding: ActivityMainBinding
    
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        initializeViews()
        setupListeners()
    }
    
    private fun initializeViews() {
        // Lógica de inicialização
    }
}

// ❌ EVITAR
class A : AppCompatActivity() {
override fun onCreate(s: Bundle?) {
super.onCreate(s)
// Tudo em um método
}
}
```

XML Templates

```xml
<!-- ✅ CORRETO - 4 espaços, atributos organizados -->
<androidx.constraintlayout.widget.ConstraintLayout
    xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:app="http://schemas.android.com/apk/res-auto"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="16dp">
    
    <TextView
        android:id="@+id/title_text"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="{{APP_TITLE}}"
        app:layout_constraintTop_toTopOf="parent"
        app:layout_constraintStart_toStartOf="parent" />
        
</androidx.constraintlayout.widget.ConstraintLayout>
```

Convenções de Placeholders

```python
# SEMPRE MAIÚSCULAS com underscores
CORRETO: {{PACKAGE_NAME}}, {{MIN_SDK_VERSION}}, {{ACTIVITY_NAME}}

# Use prefixos para contexto
{{RES_COLOR_PRIMARY}}    # Recursos
{{CLASS_NAME_MAIN}}      # Classes
{{METHOD_INIT_VIEWS}}    # Métodos
{{VAR_USER_INPUT}}       # Variáveis
```

🚀 Processo de Pull Request

1. Pré-requisitos

```bash
# Certifique-se de que pode rodar os testes
python3 -m pytest tests/ --verbose

# Verifique o linting
python3 -m pylint src/ --rcfile=.pylintrc
```

2. Fluxo de Trabalho

```bash
# 1. Fork e clone
git clone https://github.com/SEU_USUARIO/TAMK.git
cd TAMK

# 2. Branch descritiva
git checkout -b feature/login-template
# ou
git checkout -b fix/build-memory-leak
# ou
git checkout -b docs/update-install-guide

# 3. Desenvolvimento com commits atômicos
git add assets/templates/ui_apk/login_activity.xml.tmpl
git commit -m "feat(templates): add login activity template"
git commit -m "docs(templates): update README with login example"
git commit -m "fix(templates): correct placeholder in login template"

# 4. Mantenha atualizado
git fetch upstream
git rebase upstream/main

# 5. Push e PR
git push origin feature/login-template
```

3. Template de Pull Request

```markdown
## Tipo de Mudança
- [ ] 🚀 Nova funcionalidade (non-breaking change)
- [ ] 🐛 Correção de bug (non-breaking change)
- [ ] 📚 Documentação
- [ ] ♻️ Refatoração
- [ ] ⚡️ Performance
- [ ] ✅ Testes

## Descrição
Descrição clara e concisa das mudanças.

## Motivação
Por que essa mudança é necessária? Link para issue se aplicável.

## Testes Realizados
- [ ] Testado no Termux Android 10+
- [ ] Testado no Termux Android 11+
- [ ] Build bem-sucedido com novo template
- [ ] Instalação funcionando

## Screenshots (se aplicável)

## Checklist
- [ ] Meu código segue as convenções do projeto
- [ ] Adicionei testes relevantes
- [ ] Documentação atualizada
- [ ] Não introduz warnings novos
- [ ] Compatível com versões anteriores
```

🐛 Reportando Bugs

Template de Issue

```markdown
## Ambiente
- Dispositivo: [ex: Samsung Galaxy S21]
- Android: [ex: 12]
- Termux: [ex: v0.118.0]
- T.A.M.K: [ex: v2026.1.0]

## Comando Executado
tamk --create --verbose
```

Comportamento Esperado

Descrição do que deveria acontecer.

Comportamento Atual

Descrição do que está acontecendo.

Logs de Erro

```bash
# Execute com --verbose e cole a saída completa
tamk --create --verbose 2>&1 | tee error.log
```

Passos para Reproduzir

1. Execute '...'
2. Clique em '....'
3. Veja o erro

Contexto Adicional

Qualquer informação adicional sobre o problema.

```

## 🧪 Ambiente de Desenvolvimento

### Setup Rápido
```bash
# Clone e setup
git clone https://github.com/SEU_USUARIO/TAMK.git
cd TAMK

# Instale dependências de desenvolvimento
pip install -r requirements-dev.txt

# Instale pre-commit hooks
pre-commit install

# Execute testes iniciais
python -m pytest tests/ -v
```

Ferramentas Recomendadas

· Editor: VS Code com extensões Python e Kotlin
· Linting: pylint, flake8 para Python
· Formatação: black para Python, ktlint para Kotlin
· Testes: pytest com pytest-cov
· Commit Hooks: pre-commit

🏆 Reconhecimento

Todas as contribuições serão creditadas no arquivo CREDITS.md. Contribuidores regulares serão adicionados à lista de mantenedores.

❓ Dúvidas Frequentes

Q: Posso contribuir mesmo sem experiência com Android?
R: Sim! Há áreas como documentação, testes, scripts de instalação que não requerem conhecimento profundo de Android.

Q: Como testar minhas mudanças localmente?
R: Use o script dev_test.sh que simula um ambiente limpo.

Q: Onde discutir ideias antes de implementar?
R: Abra uma issue com a tag [DISCUSSÃO] para feedback da comunidade.

📞 Contato

· Issues: Para bugs e features
· Discussions: Para ideias e perguntas
· Email: [Seu email] (para assuntos privados)

---

Este documento é vivo e será atualizado conforme o projeto evolui. Última atualização: $(date +'%Y-%m-%d')

Juntos, estamos tornando o desenvolvimento Android acessível para todos! 🚀

---

<div align="center">
  <sub>Feito com ❤️ pela comunidade Termux Developer Community</sub>
</div>