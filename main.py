import typer
import autoDownload

main = typer.Typer()

@main.command()
def test():
    autoDownload.test_mode()
    typer.echo("success")

@main.command()   
def download(file_type: str, tgt_url: str, folder_name: str = typer.Option(None, prompt=True)):
    download_path = f"./download/{folder_name}"
    autoDownload.mkNewDir(download_path)
    
    if (not tgt_url.startswith("https://")): tgt_url = "https://" + tgt_url
    
    if not autoDownload.fileType_is_valid(file_type):
        typer.echo("Error: invlid argument (file type)")
        raise typer.Exit(code=1)
    
    auth = ()
    if autoDownload.auth_reqd(tgt_url):
        userName = typer.prompt("User Name")
        pasword = typer.prompt("Password", hide_input=True)
        auth = (userName, pasword)
        
        if not autoDownload.check_auth(tgt_url, auth): 
            typer.echo("Error: invlid argument")
            raise typer.Exit(code=1)
    
    
    
    typer.echo("success")
    downloader = autoDownload.AutoDownloader(tgt_url, download_path)
    downloader.setAuth(auth)
    
    
    downloader.findLinks(f".{file_type}")
    downloader.downloadFiles()
    
    return 

if __name__ == "__main__":
    main()
