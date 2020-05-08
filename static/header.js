BANNER = `<div id="header"><div id="title">
    <img src="/static/favicon.png" alt="pirate code logo PNG"/>
    <h1>Pirate Code</h1>
</div>
<div id="menu">
    <div id="back">
    <nav id="buttons">
        <a href="/"><li class="${(window.location.pathname == "/")? "select" : "normal"}">home</li></a>
        <a href="/projects"><li class="${(window.location.pathname == "/projects")? "select" : "normal"}">projects</li></a>
        <a href="/about"><li class="${(window.location.pathname == "/about")? "select" : "normal"}">about</li></a>
        <a href="/contact"><li class="${(window.location.pathname == "/contact")? "select" : "normal"}">contact</li></a>
    </nav>
    </div>
</div></div>`;
document.write(BANNER)
