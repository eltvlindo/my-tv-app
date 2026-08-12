from playwright.sync_api import sync_playwright

def cazar_todos(url_principal):
    print("🕷️ Iniciando la araña en la nube con clic fantasma...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        page.goto(url_principal)
        page.wait_for_timeout(5000) 

        todos_los_enlaces = page.eval_on_selector_all("a", "elements => elements.map(e => e.href)")
        enlaces_canales = set(link for link in todos_los_enlaces if url_principal in link and link != url_principal)

        canales_capturados = {}

        for enlace in list(enlaces_canales):
            print(f"📺 Analizando: {enlace}")
            pestaña_canal = context.new_page()
            m3u8_encontrados = []
            
            pestaña_canal.on("request", lambda request: m3u8_encontrados.append(request.url) if ".m3u8" in request.url else None)

            try:
                pestaña_canal.goto(enlace)
                pestaña_canal.wait_for_timeout(5000) # Espera a que cargue la página
                
                # 💥 MAGIA: Hacemos un clic en el centro de la pantalla para darle "Play" al video
                pestaña_canal.mouse.click(500, 300) 
                
                # Esperamos 10 segundos para que el video arranque bien después del clic
                pestaña_canal.wait_for_timeout(10000) 
            except:
                pass

            if m3u8_encontrados:
                # Evitamos guardar enlaces de publicidad, nos quedamos con el real
                canales_capturados[enlace] = m3u8_encontrados[-1] 
            
            pestaña_canal.close() 
        browser.close()

        with open("mi_tv.m3u", "w", encoding="utf-8") as archivo:
            archivo.write("#EXTM3U\n")
            for canal, m3u8 in canales_capturados.items():
                nombre_canal = canal.split("/")[-1].replace("-", " ").upper()
                if not nombre_canal:
                    nombre_canal = canal.split("/")[-2].replace("-", " ").upper()
                
                archivo.write(f"#EXTINF:-1, {nombre_canal}\n")
                archivo.write(f"{m3u8}\n")

if __name__ == "__main__":
    cazar_todos("https://telelibretv.org/")
