# 🚀 Guia Rápido de Início

> Este guia o levará de zero a um WebApp funcionando em menos de 10 minutos.

## Pré-requisitos

Certifique-se de que você tem o Termux instalado no seu dispositivo Android. Abra o Termux e execute os seguintes comandos para atualizar o sistema e instalar as dependências:

```bash
pkg update && pkg upgrade
pkg install -y python openjdk-21 kotlin wget zip apksigner aapt2 termux-tools git
```

## Passo 1: Instalar o T.A.M.K

Clone o repositório do T.A.M.K e execute o script de instalação:

```bash
git clone https://github.com/Shadw-Developer/tamk.git
cd tamk
bash setup-install.sh
```

Aguarde a conclusão da instalação. Ao final, você verá uma mensagem de sucesso. Verifique se o comando `tamk` está disponível:

```bash
tamk --version
```

Você deve ver algo como `✨ T.A.M.K Version: 2026.2.0`.

## Passo 2: Criar um Projeto WebApp

Inicie o assistente de criação de projetos:

```bash
tamk --create
```

Quando solicitado, escolha a opção **WebApp** (geralmente a opção 3). Forneça as seguintes informações:

-   **Nome do Aplicativo**: `MeuPrimeiroWebApp`
-   **Versão**: `1.0.0` (ou deixe o padrão)
-   **Autor**: Seu nome
-   **Senha da Keystore**: Escolha uma senha segura e **anote-a**. Você precisará dela para fazer o build.

O T.A.M.K criará a estrutura do projeto e baixará a SDK do Android. Isso pode levar alguns minutos na primeira vez.

## Passo 3: Adicionar Seu Conteúdo Web

Navegue até o diretório do projeto recém-criado:

```bash
cd MeuPrimeiroWebApp
```

Abra a pasta `src/main/assets/` e edite o arquivo `index.html`:

```bash
nano src/main/assets/index.html
```

Você pode modificar o HTML de exemplo ou substituí-lo completamente pelo seu próprio site. Para este guia rápido, vamos fazer uma pequena alteração:

```html
<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Meu Primeiro WebApp</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            justify-content: center; 
            height: 100vh; 
            margin: 0; 
        }
        h1 { font-size: 2.5em; margin-bottom: 10px; }
        p { font-size: 1.2em; }
        button {
            margin-top: 20px;
            padding: 15px 30px;
            background-color: white;
            color: #667eea;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <h1>🎉 Olá, Mundo!</h1>
    <p>Este é o meu primeiro WebApp criado com T.A.M.K</p>
    <button onclick="alert('Você clicou no botão!')">Clique Aqui</button>
</body>
</html>
```

Salve o arquivo (no `nano`, pressione `Ctrl+O`, depois `Enter`, e então `Ctrl+X` para sair).

## Passo 4: Compilar o APK

Agora, vamos compilar o projeto em um APK. Execute o comando de build, fornecendo a senha da Keystore que você definiu no Passo 2:

```bash
tamk --build -p SUA_SENHA_AQUI
```

O T.A.M.K irá:

1.  Validar sua senha.
2.  Compilar os recursos Android (ícones, estilos).
3.  Empacotar seus arquivos web da pasta `assets/`.
4.  Compilar o código Kotlin do `WebView`.
5.  Gerar o arquivo DEX (código executável Android).
6.  Assinar e alinhar o APK.

Ao final, você verá a mensagem: `✅ SUCESSO: app-final.apk gerado corretamente!`

## Passo 5: Instalar e Testar

Com o APK gerado, instale-o no seu dispositivo:

```bash
tamk --install
```

O Android abrirá o instalador de pacotes. Confirme a instalação. Após a conclusão, procure pelo ícone do aplicativo **MeuPrimeiroWebApp** na sua tela inicial ou gaveta de aplicativos.

Abra o aplicativo. Você deverá ver a página HTML que você criou, com o gradiente roxo e o botão interativo. Clique no botão para testar a funcionalidade JavaScript.

## Próximos Passos

Parabéns! Você criou, compilou e instalou seu primeiro WebApp com o T.A.M.K. Agora você pode:

-   **Explorar Frameworks**: Experimente usar React, Vue ou Angular. Compile seu projeto para arquivos estáticos e copie-os para `src/main/assets/`.
-   **Personalizar o Ícone**: Substitua os arquivos em `res/mipmap/` por ícones personalizados.
-   **Adicionar Mais Páginas**: Crie uma estrutura de navegação no seu site. O `WebView` suporta navegação entre páginas HTML.
-   **Ler a Documentação Completa**: Consulte `documentation/DEV_GUIDE.md`, `documentation/API_COMPONENTS.md` e `documentation/FAQ.md` para aprender técnicas avançadas.

Divirta-se desenvolvendo!
