
var ws=new WebSocket('ws://127.0.0.1:10083');
function send(){
    if(document.getElementById("chat-input").value){
        var date = new Date();
        document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper reverse"><div class="message-box-wrapper"><div class="message-box">'+ document.getElementById("chat-input").value +'</div><span>'+date+'</span></div></div>';
        if(ws){
             ws.send(document.getElementById("chat-input").value)
        }
         ws.onmessage=function(evt){
             console.log("fdsa")
             document.getElementById('chat-wrapper').innerHTML += '<div class="message-wrapper"><div class="message-box-wrapper"><div class="message-box">'+evt.data +'</div><span>'+date+'</span></div></div>';
        }
    }else{
        alert("Empty message is not allowed!");
    }
    document.getElementById("chat-input").value = "";
}