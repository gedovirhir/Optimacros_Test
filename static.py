from config import WEB_PORT

index_html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>Factorial</title>
    </head>
    <body>
        <h1>WebSocket Factorial counting</h1>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:{WEB_PORT}/ws/factorial");
            ws.onmessage = function(event) {{
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                
                let resp = JSON.parse(event.data);
                console.log(resp)
                if (resp["code"] == 200) {{
                    let body = resp["body"]
                    var content = document.createTextNode(resp["message"] + ": " + body["result"])
                }} else {{
                    var content = document.createTextNode(resp["message"] + ": ERROR " + resp["code"])
                }}
                message.appendChild(content)
                messages.appendChild(message)
            }};
            function sendMessage(event) {{
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }}
        </script>
    </body>
</html>
"""