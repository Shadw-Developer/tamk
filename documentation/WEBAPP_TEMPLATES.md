# 📄 Templates Completos para WebApp

> Este documento contém o código-fonte completo de todos os templates utilizados na criação de projetos do tipo WebApp. Estes arquivos estão localizados em `assets/templates/webapp/`.

## AndroidManifest.xml.tmpl

Este é o manifesto do aplicativo Android, que define as permissões, a atividade principal e outras configurações essenciais.

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" 
    package="{{PACKAGE}}"
    android:versionCode="1"
    android:versionName="{{VERSION}}">

    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="30" />
    
    <!-- Permissão essencial para que o WebView possa acessar conteúdo da internet -->
    <uses-permission android:name="android.permission.INTERNET" />

    <application
        android:allowBackup="true"
        android:icon="@mipmap/ic_launcher"
        android:label="{{NAME}}"
        android:theme="@style/AppTheme"
        android:usesCleartextTraffic="true"
        android:roundIcon="@mipmap/ic_launcher_round">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:configChanges="orientation|screenSize|keyboardHidden"
            android:theme="@style/AppTheme.NoActionBar">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>
```

**Pontos de Destaque:**

-   **`<uses-permission android:name="android.permission.INTERNET" />`**: Fundamental para que o `WebView` possa carregar conteúdo externo, caso seu site precise fazer requisições HTTP/HTTPS.
-   **`android:usesCleartextTraffic="true"`**: Permite que o aplicativo faça requisições HTTP (não criptografadas). Isso é útil durante o desenvolvimento, mas considere removê-lo em produção se seu site usar apenas HTTPS.
-   **`android:configChanges="orientation|screenSize|keyboardHidden"`**: Evita que a atividade seja recriada quando o dispositivo é rotacionado, preservando o estado do `WebView`.

---

## MainActivity.kt.tmpl

Este é o coração do WebApp. A classe `MainActivity` configura e gerencia o `WebView` que renderiza seu site.

```kotlin
package {{PACKAGE}}

import android.app.Activity
import android.os.Bundle
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient

class MainActivity : Activity() {

    private lateinit var webView: WebView

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)

        // Inicializa o WebView
        webView = WebView(this)
        
        // Configurações cruciais para o funcionamento correto
        webView.settings.apply {
            javaScriptEnabled = true        // Habilita JavaScript
            domStorageEnabled = true        // Habilita localStorage e sessionStorage
            allowFileAccess = true          // Permite acesso a arquivos locais (assets)
        }

        // WebViewClient: Garante que links sejam abertos dentro do app
        webView.webViewClient = WebViewClient()
        
        // WebChromeClient: Permite que alert(), confirm() e prompt() funcionem
        webView.webChromeClient = WebChromeClient()

        // Define o WebView como a view principal da Activity
        setContentView(webView)

        // Carrega o arquivo HTML principal da pasta assets
        webView.loadUrl("file:///android_asset/index.html")
    }

    // Permite que o botão "voltar" do Android navegue no histórico do WebView
    override fun onBackPressed() {
        if (webView.canGoBack()) {
            webView.goBack()
        } else {
            super.onBackPressed()
        }
    }
}
```

**Pontos de Destaque:**

-   **`javaScriptEnabled = true`**: Sem esta configuração, nenhum código JavaScript será executado, tornando a maioria dos sites modernos inoperantes.
-   **`domStorageEnabled = true`**: Essencial para frameworks e bibliotecas que utilizam `localStorage` ou `sessionStorage`.
-   **`file:///android_asset/index.html`**: Esta URL especial aponta para a pasta `assets/` dentro do APK. O T.A.M.K empacota todo o conteúdo de `src/main/assets/` nesta localização.
-   **`onBackPressed()`**: Melhora a experiência do usuário, permitindo que ele navegue para trás no histórico do site usando o botão de voltar do Android.

---

## index.html.tmpl

Um template HTML minimalista que serve como ponto de partida. Você pode substituir este arquivo completamente pelo seu próprio site.

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{NAME}}</title>
    <style>
        body { 
            font-family: sans-serif; 
            background-color: #121212; 
            color: #ffffff; 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0; 
        }
        button {
            padding: 10px 20px;
            background-color: #6200EE;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <h1>Olá, WebApp!</h1>
    <p>Rodando nativamente no Android via T.A.M.K</p>
    <button onclick="alert('JavaScript funcionando!')">Testar JS</button>
</body>
</html>
```

**Pontos de Destaque:**

-   **`<meta name="viewport" content="width=device-width, initial-scale=1.0">`**: Crucial para que o site seja responsivo em dispositivos móveis.
-   **`onclick="alert('JavaScript funcionando!')"`**: Um teste simples para verificar se o JavaScript está habilitado e funcionando no `WebView`.

---

## strings.xml.tmpl

Define as strings de recursos do aplicativo. Útil para internacionalização (i18n).

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">{{NAME}}</string>
    <string name="welcome_msg">Bem-vindo ao {{NAME}}!</string>
    <string name="author_credit">Desenvolvido por: {{AUTHOR}}</string>
</resources>
```

---

## styles.xml.tmpl

Define os estilos e temas do aplicativo Android.

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="AppTheme" parent="android:Theme.Material.Light">
        <item name="android:colorPrimary">#6200EE</item>
        <item name="android:colorPrimaryDark">#3700B3</item>
        <item name="android:colorAccent">#03DAC5</item>
    </style>

    <style name="AppTheme.NoActionBar" parent="AppTheme">
        <item name="android:windowNoTitle">true</item>
        <item name="android:windowActionBar">false</item>
    </style>
</resources>
```

**Pontos de Destaque:**

-   **`AppTheme.NoActionBar`**: Remove a barra de título padrão do Android, dando ao `WebView` (e, portanto, ao seu site) controle total sobre a interface.

---

## icon.xml.tmpl

Um ícone vetorial simples. Você pode substituí-lo por um ícone personalizado.

```xml
<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#6200EE"
        android:pathData="M0,0h108v108h-108z" />
    <path
        android:fillColor="#FFFFFF"
        android:pathData="M30,30h48v48h-48z" />
</vector>
```

---

## Código Python: `webapp.py`

Este é o código Python responsável por orquestrar a criação de um projeto WebApp.

```python
import os
import subprocess
from utils.logger import log

class WebAppStructure:
    def setup(self, name, version, author, password):
        self.base = os.path.join(os.getcwd(), name)
        self.package = f"com.example.{name.lower().replace('-', '')}"
        # Usa templates da pasta webapp
        self.tmpl_dir = os.path.join(os.path.dirname(__file__), "../../../assets/templates/webapp")
        
        # Vamos pegar ícones e estilos do ui_apk como fallback se não criarmos específicos
        self.common_tmpl_dir = os.path.join(os.path.dirname(__file__), "../../../assets/templates/ui_apk")

        # 1. Criação de pastas (Incluindo assets/ para o HTML)
        self._create_folders()

        # 2. Segurança
        self._generate_keystore(password, author)

        # 3. Mapeamento
        mappings = {
            "AndroidManifest.xml": (self.tmpl_dir, "AndroidManifest.xml.tmpl"),
            f"src/main/kotlin/{self.package.replace('.', '/')}/MainActivity.kt": (self.tmpl_dir, "MainActivity.kt.tmpl"),
            "src/main/assets/index.html": (self.tmpl_dir, "index.html.tmpl"),
            
            # Reutilizando recursos visuais básicos do UI APK para não duplicar agora
            "res/values/styles.xml": (self.common_tmpl_dir, "styles.xml.tmpl"),
            "res/mipmap/ic_launcher.xml": (self.common_tmpl_dir, "icon.xml.tmpl"),
            "res/mipmap/ic_launcher_round.xml": (self.common_tmpl_dir, "icon.xml.tmpl"),
        }
        
        # Mapeamento simples para strings (pode ser específico depois)
        mappings["res/values/strings.xml"] = (self.common_tmpl_dir, "strings.xml.tmpl")

        replacements = {
            "{{NAME}}": name,
            "{{PACKAGE}}": self.package,
            "{{VERSION}}": version,
            "{{AUTHOR}}": author
        }

        log("Processando templates de WebApp...", "STEP")
        for dest, (source_dir, tmpl_name) in mappings.items():
            self._generate_file(source_dir, tmpl_name, dest, replacements)

        # 4. Finalização
        self._run_local_setup()

        log(f"✅ WebApp '{name}' criado! Coloque seus arquivos HTML/JS em src/main/assets/", "SUCCESS")
        return True

    def _create_folders(self):
        paths = [
            f"src/main/kotlin/{self.package.replace('.', '/')}",
            "src/main/assets",  # <--- Importante para WebApps
            "res/values", "res/mipmap", "secret"
        ]
        for p in paths:
            os.makedirs(os.path.join(self.base, p), exist_ok=True)

    def _generate_file(self, source_dir, tmpl_name, dest_path, reps):
        src = os.path.join(source_dir, tmpl_name)
        if not os.path.exists(src):
            log(f"Aviso: Template {tmpl_name} não encontrado em {source_dir}.", "WARNING")
            return

        with open(src, "r") as f:
            content = f.read()

        for key, value in reps.items():
            content = content.replace(key, value)

        final_path = os.path.join(self.base, dest_path)
        with open(final_path, "w") as f:
            f.write(content)

    def _generate_keystore(self, password, author):
        ks_path = os.path.join(self.base, "secret/project.keystore")
        log("Gerando Keystore privada...", "INFO")
        cmd = (f"keytool -genkey -v -keystore {ks_path} -alias project_key "
               f"-keyalg RSA -keysize 2048 -validity 10000 "
               f"-storepass {password} -keypass {password} "
               f"-dname 'CN={author},O=TAMK-Web,C=BR'")
        subprocess.run(cmd, shell=True, capture_output=True)

    def _run_local_setup(self):
        old_cwd = os.getcwd()
        os.chdir(self.base)
        from controllers.setup_controller import SetupController
        SetupController().setup_environment()
        os.chdir(old_cwd)
```
